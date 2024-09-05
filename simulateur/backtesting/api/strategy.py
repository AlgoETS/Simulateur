from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from backtesting.models import StockBacktest
from backtesting.serializers import StrategySerializer
from backtesting.tasks import run_strategy
from django.core.cache import cache

class StrategyAPIView(APIView):
    def post(self, request):
        # Check rate limit (example: 1 request per minute per user)
        user_key = f"strategy_rate_limit_{request.user.id}"
        if cache.get(user_key):
            return JsonResponse({"error": "Rate limit exceeded. Please wait a minute before trying again."},
                                status=status.HTTP_429_TOO_MANY_REQUESTS)

        serializer = StrategySerializer(data=request.data)
        if serializer.is_valid():
            strategy = serializer.save(created_by=request.user)

            # Trigger the Celery task
            stock_id = request.data.get('stock_id')
            if not stock_id:
                return JsonResponse({"error": "Stock ID is required to run the strategy"}, status=status.HTTP_400_BAD_REQUEST)

            # Ensure the stock exists
            try:
                stock = StockBacktest.objects.get(id=stock_id)
            except StockBacktest.DoesNotExist:
                return JsonResponse({"error": "Stock not found"}, status=status.HTTP_404_NOT_FOUND)

            # Run the strategy using Celery
            result = run_strategy.delay(strategy.id, stock.id)

            # Set the rate limit (e.g., 60 seconds)
            cache.set(user_key, True, timeout=60)

            return JsonResponse({"status": "strategy scheduled", "task_id": result.id}, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
