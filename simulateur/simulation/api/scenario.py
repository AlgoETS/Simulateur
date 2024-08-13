from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from simulation.models import Scenario, Stock, StockPriceHistory, Company, News, Trigger, Event
from simulation.serializers import ScenarioSerializer, StockSerializer, StockPriceHistorySerializer

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
class CreateCompanyAndStock(APIView):
    def post(self, request):
        company_data = request.data.get('company', {})
        stock_data = request.data.get('stock', {})
        company = Company.objects.create(**company_data)
        stock = Stock.objects.create(company=company, **stock_data)
        return Response(
            {"status": "success", "message": "Company and stock created successfully"},
            status=status.HTTP_201_CREATED,
)

class CreateNews(APIView):
    def post(self, request):
        news_data = request.data
        news = News.objects.create(**news_data)
        return Response(
            {"status": "success", "message": "News created successfully"},
            status=status.HTTP_201_CREATED,
)

class CreateEvent(APIView):
    def post(self, request):
        event_data = request.data
        event = Event.objects.create(**event_data)
        return Response(
            {"status": "success", "message": "Event created successfully"},
            status=status.HTTP_201_CREATED,
)

class CreateTrigger(APIView):
    def post(self, request):
        trigger_data = request.data
        trigger = Trigger.objects.create(**trigger_data)
        return Response(
            {"status": "success", "message": "Trigger created successfully"},
            status=status.HTTP_201_CREATED,
)

class CreateScenarioView(APIView):
    def post(self, request):
        serializer = ScenarioSerializer(data=request.data)
        if serializer.is_valid():
            scenario = serializer.save()
            return Response({"scenario_id": scenario.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AddCompanyStockView(APIView):
    def post(self, request):
        scenario_id = request.data.get('scenario_id')
        scenario = Scenario.objects.get(id=scenario_id)
        companies_data = request.data.get('companies', [])

        for company_data in companies_data:
            company = Company.objects.create(**company_data)
            scenario.companies.add(company)
            if 'stock' in company_data:
                stock = Stock.objects.create(company=company, **company_data['stock'])
                scenario.stocks.add(stock)

        return Response({"scenario_id": scenario.id}, status=status.HTTP_200_OK)

class AddTeamsView(APIView):
    def post(self, request):
        scenario_id = request.data.get('scenario_id')
        scenario = Scenario.objects.get(id=scenario_id)
        teams_data = request.data.get('teams', [])

        for team_data in teams_data:
            team = Team.objects.create(**team_data)
            scenario.teams.add(team)

        return Response({"scenario_id": scenario.id}, status=status.HTTP_200_OK)

class AddEventsNewsTriggersView(APIView):
    def post(self, request):
        scenario_id = request.data.get('scenario_id')
        scenario = Scenario.objects.get(id=scenario_id)

        events_data = request.data.get('events', [])
        for event_data in events_data:
            event = Event.objects.create(**event_data)
            scenario.events.add(event)

        news_data = request.data.get('news', [])
        for news_item in news_data:
            news = News.objects.create(**news_item)
            scenario.news.add(news)

        triggers_data = request.data.get('triggers', [])
        for trigger_data in triggers_data:
            trigger = Trigger.objects.create(**trigger_data)
            scenario.triggers.add(trigger)

        return Response({"scenario_id": scenario.id}, status=status.HTTP_200_OK)


class ReviewSubmitScenarioView(APIView):
    def post(self, request):
        scenario_id = request.data.get('scenario_id')
        scenario = Scenario.objects.get(id=scenario_id)
        # Any additional logic for final submission can be added here
        return Response({"message": "Scenario submitted successfully", "scenario_id": scenario.id},
                        status=status.HTTP_200_OK)
