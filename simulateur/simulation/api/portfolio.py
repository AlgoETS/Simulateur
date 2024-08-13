import json
from decimal import Decimal
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db import transaction
from simulation.models import Portfolio, Stock, Order, TransactionHistory, Scenario,StockPortfolio
from simulation.logic.BuySellQueue import buy_sell_queue
from simulation.logic.broker import broker
from simulation.serializers import PortfolioSerializer
from simulation.models import UserProfile


class PortfolioView(View):
    @method_decorator(login_required)
    def get(self, request, user_id):
        try:
            portfolio = Portfolio.objects.get(owner__user_id=user_id)
            serializer = PortfolioSerializer(portfolio)
            return JsonResponse(serializer.data, safe=False)
        except Portfolio.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Portfolio not found'}, status=404)


class BuyStock(View):
    @method_decorator(login_required)
    def post(self, request):
        try:
            data = json.loads(request.body)
            user_profile = request.user.userprofile
            stock = Stock.objects.get(id=data['stock_id'])
            scenario = Scenario.objects.get(id=data['scenario_id'])
            amount = int(data['amount'])
            price = Decimal(data.get('price', stock.price))  # Default to stock price if price not provided

            if amount <= 0:
                return JsonResponse({'status': 'error', 'message': 'Amount must be greater than zero'}, status=400)

            total_cost = amount * price
            if user_profile.portfolio.balance < total_cost:
                return JsonResponse({'status': 'error', 'message': 'Insufficient funds'}, status=400)

            with transaction.atomic():
                # Create an order
                order = Order.objects.create(
                    user=user_profile,
                    stock=stock,
                    # scenario=scenario,
                    quantity=amount,
                    price=price,
                    transaction_type='BUY'
                )

                stock_portfolio, created = StockPortfolio.objects.get_or_create(
                    portfolio=user_profile.portfolio,
                    stock=stock,
                    defaults={'quantity': 0, 'average_stock_price': 0}
                )

                # Update the stock portfolio
                new_total_quantity = stock_portfolio.quantity + amount
                new_average_price = (
                    (stock_portfolio.quantity * stock_portfolio.average_holding_price) + (amount * price)
                ) / new_total_quantity

                stock_portfolio.quantity = new_total_quantity
                stock_portfolio.average_holding_price = new_average_price
                stock_portfolio.save()

                # Logic to buy stock
                buy_sell_queue.add_to_buy_queue(user_profile, stock, amount, price, scenario)

               # Deduct the amount from the user's balance
                user_profile.portfolio.balance -= total_cost
                user_profile.portfolio.save()

                # Create a transaction history record
                transaction_history = TransactionHistory.objects.get(scenario=scenario)
                ## how to add the order to the transaction history record:
                transaction_history.orders.add(order)

            return JsonResponse({'status': 'success', 'order_id': order.id})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)
        except Stock.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Stock not found'}, status=404)
        except Scenario.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Scenario not found'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


class SellStock(View):
    @method_decorator(login_required)
    def post(self, request):
        try:
            data = json.loads(request.body)
            user_profile = request.user.userprofile
            stock = Stock.objects.get(id=data['stock_id'])
            scenario = Scenario.objects.get(id=data['scenario_id'])
            amount = int(data['amount'])
            price = Decimal(data.get('price', stock.price))  # Default to stock price if price not provided

            if amount <= 0:
                return JsonResponse({'status': 'error', 'message': 'Amount must be greater than zero'}, status=400)

            stock_portfolio = user_profile.portfolio.stockportfolio_set.filter(stock=stock).first()
            if not stock_portfolio or stock_portfolio.quantity < amount:
                return JsonResponse({'status': 'error', 'message': 'Insufficient stock holdings'}, status=400)

            with transaction.atomic():
                # Create an order
                order = Order.objects.create(
                    user=user_profile,
                    stock=stock,
                    # scenario=scenario,
                    quantity=amount,
                    price=price,
                    transaction_type='SELL'
                )

                # Update the stock portfolio
                stock_portfolio.quantity -= amount
                stock_portfolio.market_value = stock_portfolio.quantity * price
                stock_portfolio.save()

                if stock_portfolio.quantity == 0:
                    stock_portfolio.delete()

                # Logic to sell stock
                buy_sell_queue.add_to_sell_queue(user_profile, stock, amount, price)

                # Add the amount to the user's balance
                user_profile.portfolio.balance += amount * price
                user_profile.portfolio.save()

                # Create a transaction history record
                transaction_history = TransactionHistory.objects.get(scenario=scenario)
                transaction_history.orders.add(order)

            return JsonResponse({'status': 'success', 'order_id': order.id})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)
        except Stock.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Stock not found'}, status=404)
        except Scenario.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Scenario not found'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

class StockPrice(View):
    def get(self, request, stock_id):
        try:
            stock = Stock.objects.filter(id=stock_id)
            if stock.exists():
                return JsonResponse({'price': stock.first().price})
            
        except Stock.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Stock not found'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


class UserOrders(View):
    @method_decorator(login_required)
    def post(self, request):
        try:
            data = json.loads(request.body)
            user_profile = request.user.userprofile
            scenario = Scenario.objects.get(id=data['scenario_id'])
            transaction_history = TransactionHistory.objects.filter(scenario=scenario).first()
            orders = transaction_history.orders.filter(user=user_profile).order_by('-timestamp')

            
            # Prepare the data to send to the frontend
            orders_data = [{
                'transaction_type': order.transaction_type,
                'quantity': order.quantity,
                'ticker': order.stock.ticker,
                'price': order.price,
                'timestamp': order.timestamp.strftime('%B %d, %Y, %I:%M %p')
            } for order in orders]
            

            return JsonResponse({'status': 'success', 'orders': orders_data})
        except UserProfile.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User profile does not exist'}, status=404)
        except Scenario.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Scenario not found'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


# TODO add the two new urls for the dynamic picing.

