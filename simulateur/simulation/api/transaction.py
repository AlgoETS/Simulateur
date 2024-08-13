import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from simulation.models import Portfolio, Stock, Order, TransactionHistory, Scenario, StockPriceHistory
from simulation.models import UserProfile



class UserOrders(View):
    @method_decorator(login_required)
    def post(self, request):
        try:
            data = json.loads(request.body)
            user_profile = request.user.userprofile
            scenario = Scenario.objects.get(id=data['scenario_id'])
            transaction_history = TransactionHistory.objects.filter(scenario_manager=scenario.scenario_manager).first()
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
