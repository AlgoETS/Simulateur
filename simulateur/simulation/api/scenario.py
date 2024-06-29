from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone

from simulation.models import Scenario, Stock, StockPriceHistory
from simulation.serializers import (
    ScenarioSerializer,
    StockSerializer,
    StockPriceHistorySerializer,
)


class CreateScenario(generics.GenericAPIView):
    serializer_class = ScenarioSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": "success", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"status": "error", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class PublishScenario(APIView):
    def post(self, request, scenario_id, *args, **kwargs):
        scenario = get_object_or_404(Scenario, id=scenario_id)
        scenario.published_date = timezone.now()
        scenario.save()
        return Response(
            {"status": "success", "message": "Scenario published successfully"},
            status=status.HTTP_200_OK,
        )


class ScenarioStocks(APIView):
    def get(self, request, scenario_id):
        scenario = get_object_or_404(Scenario, id=scenario_id)
        stocks = scenario.stocks.all()
        serializer = StockSerializer(stocks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StockHistory(APIView):
    def get(self, request, stock_id):
        stock = get_object_or_404(Stock, id=stock_id)
        price_history = StockPriceHistory.objects.filter(stock=stock)
        serializer = StockPriceHistorySerializer(price_history, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetPublishedScenarios(APIView):
    def get(self, request):
        scenarios = Scenario.objects.filter(published_date__isnull=False)
        serializer = ScenarioSerializer(scenarios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
