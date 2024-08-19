import decimal
import json
from collections import defaultdict
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from simulation.logic.BuySellQueue import buy_sell_queue
from simulation.models import Portfolio, Stock, Order, TransactionHistory, SimulationManager, StockPriceHistory, \
    StockPortfolio
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
            simulation_manager = SimulationManager.objects.get(id=data['simulation_manager_id'])
            amount = int(data['amount'])

            # Get the latest price from StockPriceHistory
            latest_price_history = StockPriceHistory.objects.filter(stock=stock).order_by('-timestamp').first()
            if not latest_price_history:
                return JsonResponse({'status': 'error', 'message': 'No price history available for this stock'},
                                    status=404)

            # Ensure the price is a valid decimal
            try:
                price = Decimal(data.get('price', latest_price_history.close_price))
            except (ValueError, decimal.InvalidOperation) as e:
                return JsonResponse({'status': 'error', 'message': f'Invalid price value: {str(e)}'}, status=400)

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
                    quantity=amount,
                    price=price,
                    transaction_type='BUY'
                )

                # Logic to buy stock
                buy_sell_queue.add_to_buy_queue(user_profile, stock, amount, price, simulation_manager)

                # Deduct the amount from the user's balance
                user_profile.portfolio.balance -= total_cost
                user_profile.portfolio.save()

                # Add the stock to the StockPortfolio or update the existing quantity
                stock_portfolio, created = StockPortfolio.objects.get_or_create(
                    portfolio=user_profile.portfolio,
                    stock=stock,
                    defaults={'quantity': amount, 'latest_price_history': latest_price_history}
                )

                if not created:
                    stock_portfolio.quantity += amount
                    stock_portfolio.latest_price_history = latest_price_history  # Update the latest price history
                    stock_portfolio.save()

                # Retrieve the transaction history record and add the order
                transaction_history = TransactionHistory.objects.get(simulation_manager=simulation_manager)
                transaction_history.orders.add(order)

            return JsonResponse({'status': 'success', 'order_id': order.id})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)
        except Stock.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Stock not found'}, status=404)
        except SimulationManager.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Simulation manager not found'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


class SellStock(View):
    @method_decorator(login_required)
    def post(self, request):
        try:
            data = json.loads(request.body)
            user_profile = request.user.userprofile
            stock = Stock.objects.get(id=data['stock_id'])
            simulation_manager = SimulationManager.objects.get(id=data['simulation_manager_id'])
            amount = int(data['amount'])

            if amount <= 0:
                return JsonResponse({'status': 'error', 'message': 'Amount must be greater than zero'}, status=400)

            portfolio = Portfolio.objects.filter(owner=user_profile, simulation_manager=simulation_manager).first()
            if not portfolio:
                return JsonResponse({'status': 'error', 'message': 'Portfolio not found for this simulation manager'},
                                    status=404)

            stock_portfolio = StockPortfolio.objects.filter(portfolio=portfolio, stock=stock).first()
            if not stock_portfolio or stock_portfolio.quantity < amount:
                return JsonResponse({'status': 'error', 'message': 'Insufficient stock holdings'}, status=400)

            latest_price_history = StockPriceHistory.objects.filter(stock=stock).order_by('-timestamp').first()
            if not latest_price_history:
                return JsonResponse({'status': 'error', 'message': 'No price history available for this stock'},
                                    status=404)

            price = Decimal(data.get('price', latest_price_history.close_price))

            with transaction.atomic():
                order = Order.objects.create(
                    user=user_profile,
                    stock=stock,
                    quantity=amount,
                    price=price,
                    transaction_type='SELL'
                )

                buy_sell_queue.add_to_sell_queue(user_profile, stock, amount, price, simulation_manager)

                portfolio.balance += amount * price
                portfolio.save()

                stock_portfolio.quantity -= amount
                stock_portfolio.save()

                if stock_portfolio.quantity == 0:
                    stock_portfolio.delete()

                transaction_history = TransactionHistory.objects.get(simulation_manager=simulation_manager)
                transaction_history.orders.add(order)

            return JsonResponse({'status': 'success', 'order_id': order.id})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)
        except Stock.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Stock not found'}, status=404)
        except SimulationManager.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Simulation manager not found'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


class StockPrice(View):
    def get(self, request, stock_id):
        try:
            stock = Stock.objects.get(id=stock_id)
            latest_price_history = StockPriceHistory.objects.filter(stock=stock).order_by('-timestamp').first()
            if not latest_price_history:
                return JsonResponse({'status': 'error', 'message': 'No price history available for this stock'},
                                    status=404)

            return JsonResponse({'price': latest_price_history.close_price})

        except Stock.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Stock not found'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


class StockHoldings(View):
    @method_decorator(login_required)
    def post(self, request):
        try:
            data = json.loads(request.body)
            user_profile = request.user.userprofile
            simulation_manager_id = data.get('simulation_manager_id')

            # Validate simulation manager
            simulation_manager = SimulationManager.objects.get(id=simulation_manager_id)

            # Find the correct portfolio based on the simulation manager and user profile
            portfolio = Portfolio.objects.filter(owner=user_profile, simulation_manager=simulation_manager).first()
            if not portfolio:
                return JsonResponse({'status': 'error', 'message': 'Portfolio not found for this simulation manager'},
                                    status=404)

            # Get all stock portfolios related to this portfolio
            stock_portfolios = StockPortfolio.objects.filter(portfolio=portfolio)

            holdings_data = []

            # Iterate over each stock in the portfolio to calculate additional stats
            for stock_portfolio in stock_portfolios:
                stock = stock_portfolio.stock

                # Get the latest price history
                latest_price_history = StockPriceHistory.objects.filter(stock=stock).order_by('-timestamp').first()
                latest_price = latest_price_history.close_price if latest_price_history else None

                # Calculate the price when bought (initial price)
                initial_price = stock_portfolio.latest_price_history.close_price if stock_portfolio.latest_price_history else None

                # Calculate the price difference and percentage change
                if initial_price and latest_price:
                    price_difference = latest_price - initial_price
                    percentage_change = (price_difference / initial_price) * 100
                else:
                    price_difference = None
                    percentage_change = None

                # Append the stock data to the holdings list
                holdings_data.append({
                    'stock': stock.ticker,
                    'company': stock.company.name,
                    'quantity': stock_portfolio.quantity,
                    'initial_price': initial_price,
                    'latest_price': latest_price,
                    'price_difference': price_difference,
                    'percentage_change': percentage_change
                })

            return JsonResponse({'status': 'success', 'holdings': holdings_data})
        except SimulationManager.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Simulation manager not found'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


class GroupedPerformanceView(View):
    @method_decorator(login_required)
    def post(self, request):
        try:
            data = json.loads(request.body)
            simulation_manager_id = data.get('simulation_manager_id')
            group_by = data.get('group_by', 'sector')  # Default to 'sector' if not provided

            # Validate simulation manager
            simulation_manager = SimulationManager.objects.get(id=simulation_manager_id)

            # Validate grouping criteria
            valid_groupings = ['sector', 'industry', 'country']
            if group_by not in valid_groupings:
                return JsonResponse({'status': 'error', 'message': 'Invalid grouping criterion'}, status=400)

            # Filter stock portfolios for the current user and the selected simulation manager
            user_profile = request.user.userprofile
            stock_portfolios = StockPortfolio.objects.filter(
                portfolio__owner=user_profile,
                portfolio__simulation_manager=simulation_manager
            )

            # Group stock data by the specified criterion
            groups = defaultdict(lambda: {"value": 0, "stocks": []})

            for stock_portfolio in stock_portfolios:
                stock = stock_portfolio.stock
                group_value = getattr(stock.company, group_by, 'Unknown')  # Get the attribute dynamically

                # Get the latest price for the stock
                latest_price_history = stock_portfolio.latest_price_history
                latest_price = latest_price_history.close_price if latest_price_history else 0

                # Calculate the total value of the stock in the portfolio
                group_value_total = latest_price * stock_portfolio.quantity

                # Add the value to the appropriate group
                groups[group_value]["value"] += group_value_total
                groups[group_value]["stocks"].append({
                    "ticker": stock.ticker,
                    "company": stock.company.name,
                    "value": group_value_total
                })

            # Prepare data for the chart
            group_labels = list(groups.keys())
            group_values = [groups[group]["value"] for group in groups]

            return JsonResponse({
                "status": "success",
                "group_labels": group_labels,
                "group_values": group_values
            })

        except SimulationManager.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Simulation manager not found'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


class PortfolioBalanceView(View):
    @method_decorator(login_required)
    def get(self, request):
        try:
            user_profile = request.user.userprofile
            portfolio = Portfolio.objects.get(owner=user_profile)

            return JsonResponse({'status': 'success', 'balance': str(portfolio.balance)}, status=200)
        except Portfolio.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Portfolio not found'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
