from django.test import TestCase
from simulation.models import (
    Company,
    Stock,
    StockPriceHistory,
    UserProfile,
    Event,
    SimulationSettings,
    Scenario,
    Team,
    Portfolio,
    TransactionHistory,
    Trigger,
    News,
)
from simulation.serializers import (
    CompanySerializer,
    StockSerializer,
    EventSerializer,
    SimulationSettingsSerializer,
    TeamSerializer,
    PortfolioSerializer,
    TransactionHistorySerializer,
    TriggerSerializer,
    NewsSerializer,
    ScenarioSerializer,
)


class SerializerTests(TestCase):
    def setUp(self):
        self.company_data = {
            "name": "Test Company",
            "backstory": "This is a test company",
            "sector": "Technology",
            "country": "USA",
            "industry": "Software",
        }
        self.stock_data = {
            "ticker": "TEST",
            "price": 100.0,
            "open_price": 90.0,
            "high_price": 110.0,
            "low_price": 85.0,
            "close_price": 95.0,
        }
        self.event_data = {
            "name": "Test Event",
            "date": "2024-07-01T12:00:00Z",
            "description": "This is a test event",
        }
        self.simulation_settings_data = {
            "max_users": 100,
            "max_companies": 50,
            "timer_step": 10,
            "timer_step_unit": "minute",
            "interval": 20,
            "interval_unit": "minute",
            "max_interval": 3000,
            "fluctuation_rate": 0.1,
            "close_stock_market_at_night": True,
            "noise_function": "brownian",
        }
        self.team_data = {"name": "Test Team"}
        self.news_data = {
            "title": "Test News",
            "content": "This is a test news article",
            "published_date": "2024-07-01T12:00:00Z",
        }
        self.trigger_data = {
            "name": "Test Trigger",
            "type": "price",
            "value": 100.0,
            "timestamp": "2024-07-01T12:00:00Z",
        }

    def test_company_serializer(self):
        serializer = CompanySerializer(data=self.company_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["name"], self.company_data["name"])

    def test_stock_serializer(self):
        company = Company.objects.create(**self.company_data)
        self.stock_data["company"] = company.id
        serializer = StockSerializer(data=self.stock_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["ticker"], self.stock_data["ticker"])

    def test_event_serializer(self):
        serializer = EventSerializer(data=self.event_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["name"], self.event_data["name"])

    def test_simulation_settings_serializer(self):
        serializer = SimulationSettingsSerializer(data=self.simulation_settings_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(
            serializer.validated_data["max_users"],
            self.simulation_settings_data["max_users"],
        )

    def test_team_serializer(self):
        serializer = TeamSerializer(data=self.team_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["name"], self.team_data["name"])

    def test_news_serializer(self):
        serializer = NewsSerializer(data=self.news_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["title"], self.news_data["title"])

    def test_trigger_serializer(self):
        serializer = TriggerSerializer(data=self.trigger_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["name"], self.trigger_data["name"])

    def test_scenario_serializer(self):
        company = Company.objects.create(**self.company_data)
        stock = Stock.objects.create(company=company, **self.stock_data)
        event = Event.objects.create(**self.event_data)
        simulation_settings = SimulationSettings.objects.create(
            **self.simulation_settings_data
        )
        team = Team.objects.create(**self.team_data)
        news = News.objects.create(**self.news_data)
        trigger = Trigger.objects.create(**self.trigger_data)

        scenario_data = {
            "name": "Test Scenario",
            "description": "This is a test scenario",
            "backstory": "This is a test backstory",
            "duration": 60,
            "stocks": [StockSerializer(stock).data],
            "teams": [TeamSerializer(team).data],
            "news": [NewsSerializer(news).data],
            "events": [EventSerializer(event).data],
            "triggers": [TriggerSerializer(trigger).data],
            "simulation_settings": SimulationSettingsSerializer(
                simulation_settings
            ).data,
        }

        serializer = ScenarioSerializer(data=scenario_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["name"], scenario_data["name"])
