from django.test import TestCase
from simulation.models import (
    Company,
    Stock,
)
from simulation.serializers import (
    CompanySerializer,
    StockSerializer,
    EventSerializer,
    SimulationSettingsSerializer,
    TeamSerializer,
    TriggerSerializer,
    NewsSerializer,
    ScenarioSerializer,
    StockPriceHistorySerializer,
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
            "volatility": 0.5,
            "liquidity": 1.0,
        }
        self.stock_price_history_data = {
            "open_price": 90.0,
            "high_price": 110.0,
            "low_price": 85.0,
            "close_price": 95.0,
            "stock": self.stock_data
        }
        self.event_data = {
            "name": "Test Event",
            "date": "2024-07-01T12:00:00Z",
            "description": "This is a test event",
        }
        self.simulation_settings_data = {
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

    def test_stock_price_history_serializer(self):
        company = Company.objects.create(**self.company_data)
        stock = Stock.objects.create(**self.stock_data)
        stock.company_id = company.id
        self.stock_data["company"] = company.id
        self.stock_price_history_data["stock"] = stock.id
        serializer = StockPriceHistorySerializer(data=self.stock_price_history_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["open_price"], self.stock_price_history_data["open_price"])

    def test_event_serializer(self):
        serializer = EventSerializer(data=self.event_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["name"], self.event_data["name"])

    def test_simulation_settings_serializer(self):
        serializer = SimulationSettingsSerializer(data=self.simulation_settings_data)
        self.assertTrue(serializer.is_valid())

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
        scenario_data = {
            "name": "Test Scenario",
            "description": "This is a test scenario",
            "backstory": "This is a test backstory",
            "duration": 60
        }

        serializer = ScenarioSerializer(data=scenario_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["name"], scenario_data["name"])
