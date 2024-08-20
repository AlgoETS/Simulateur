from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .tasks import run_strategy_batch

class RunBacktestsAPIView(APIView):
    def post(self, request):
        strategy_names = request.data.get("strategies", [])
        instruments = request.data.get("instruments", [])

        if not strategy_names or not instruments:
            return Response({"error": "Strategies and instruments are required"}, status=status.HTTP_400_BAD_REQUEST)

        # Trigger the batch backtesting with Celery
        result = run_strategy_batch.delay(strategy_names, instruments)

        return Response({"status": "Backtesting scheduled", "task_id": result.id}, status=status.HTTP_200_OK)
