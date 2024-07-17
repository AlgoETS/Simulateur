import json
from decimal import Decimal
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db import transaction
from simulation.models import Portfolio, Stock, Order, TransactionHistory, Scenario
from simulation.logic.BuySellQueue import buy_sell_queue
from simulation.logic.broker import broker
from simulation.serializers import PortfolioSerializer


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
                # Create an order in the broker's queue
                broker.add_to_buysell_queue(user_profile, stock.ticker, amount, price, "buy")

                # Create an order
                order = Order.objects.create(
                    user=user_profile,
                    stock=stock,
                    quantity=amount,
                    price=price,
                    transaction_type='BUY'
                )

                # Create or get a transaction history record
                transaction_history = TransactionHistory.objects.get(
                    scenario=scenario
                )
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
                # Create an order in the broker's queue
                broker.add_to_buysell_queue(user_profile, stock.ticker, amount, price, "sell")

                # Create an order
                order = Order.objects.create(
                    user=user_profile,
                    stock=stock,
                    quantity=amount,
                    price=price,
                    transaction_type='SELL'
                )

                # Create or get a transaction history record
                transaction_history = TransactionHistory.objects.get(
                    scenario=scenario
                )
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

#TODO add the two new urls to the simulator
# class BuyStocKDynamic:

#     def post(self,request):

#         data = json.loads(request.body)
#         user_profile = request.user.userprofile
#         stock = Stock.objects.get(id=data['stock_id'])
#         scenario = Scenario.objects.get(id=data['scenario_id'])
#         amount = int(data['amount'])
#         price = Decimal(data.get('price', stock.price))  # Default to stock price if price not provided

#         broker.add_to_buysell_queue(user_profile,stock,amount,price,"buy")

# class SellStockDynamic:

#     def post(self,request):

#         data = json.loads(request.body)
#         user_profile = request.user.userprofile
#         stock = Stock.objects.get(id=data['stock_id'])
#         scenario = Scenario.objects.get(id=data['scenario_id'])
#         amount = int(data['amount'])
#         price = Decimal(data.get('price', stock.price))  # Default to stock price if price not provided

#         broker.add_to_buysell_queue(user_profile,stock,amount,price,"sell")


