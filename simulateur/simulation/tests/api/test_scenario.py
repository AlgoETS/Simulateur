from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from simulation.models import Scenario, Stock, Company, News, Trigger, Event, StockPriceHistory
from django.utils import timezone


class ScenarioTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.scenario = Scenario.objects.create(name="Test Scenario", description="Test Description")
        self.company = Company.objects.create(name="Test Company", sector="Tech", country="USA", industry="Software", timestamp=timezone.now())
        self.stock = Stock.objects.create(ticker="TST", company=self.company, volatility=0.5, liquidity=1000)
        self.price_history = StockPriceHistory.objects.create(stock=self.stock, open_price=100, close_price=105)
        self.news = News.objects.create(headline="Test News", content="Test Content", timestamp=timezone.now())
        self.event = Event.objects.create(name="Test Event", description="Test Event Description", timestamp=timezone.now())
        self.trigger = Trigger.objects.create(name="Test Trigger", condition="Test Condition", action="Test Action")

    def test_create_scenario(self):
        url = reverse('create_scenario')  # You may need to adjust the name to match your URL configuration
        data = {
            "name": "New Scenario",
            "description": "A new scenario",
            "backstory": "Test backstory",
            "duration": 30
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Scenario.objects.count(), 2)

    def test_publish_scenario(self):
        url = reverse('publish_scenario', kwargs={'scenario_id': self.scenario.id})  # Adjust the URL name
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.scenario.refresh_from_db()
        self.assertIsNotNone(self.scenario.published_date)

    def test_get_scenario_stocks(self):
        url = reverse('scenario_stocks', kwargs={'scenario_id': self.scenario.id})  # Adjust the URL name
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)  # Assuming no stocks are linked directly to the scenario

    def test_get_stock_history(self):
        url = reverse('stock_history', kwargs={'stock_id': self.stock.id})  # Adjust the URL name
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_published_scenarios(self):
        self.scenario.published_date = timezone.now()
        self.scenario.save()
        url = reverse('get_published_scenarios')  # Adjust the URL name
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_company_and_stock(self):
        url = reverse('create_company_and_stock')  # Adjust the URL name
        data = {
            "company": {
                "name": "New Company",
                "sector": "Finance",
                "country": "UK",
                "industry": "Banking",
                "timestamp": timezone.now().isoformat()
            },
            "stock": {
                "ticker": "NEW",
                "volatility": 0.2,
                "liquidity": 5000
            }
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Company.objects.count(), 2)
        self.assertEqual(Stock.objects.count(), 2)

    def test_create_news(self):
        url = reverse('create_news')  # Adjust the URL name
        data = {
            "headline": "Breaking News",
            "content": "This is breaking news content.",
            "timestamp": timezone.now().isoformat()
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(News.objects.count(), 2)

    def test_create_event(self):
        url = reverse('create_event')  # Adjust the URL name
        data = {
            "name": "New Event",
            "description": "This is a new event description.",
            "timestamp": timezone.now().isoformat()
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(), 2)

    def test_create_trigger(self):
        url = reverse('create_trigger')  # Adjust the URL name
        data = {
            "name": "New Trigger",
            "condition": "If stock price > 100",
            "action": "Send alert"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Trigger.objects.count(), 2)

    def test_add_company_stock_to_scenario(self):
        url = reverse('add_company_stock')  # Adjust the URL name
        data = {
            "scenario_id": self.scenario.id,
            "companies": [
                {
                    "name": "Another Company",
                    "sector": "Energy",
                    "country": "Canada",
                    "industry": "Oil",
                    "stock": {
                        "ticker": "ENE",
                        "volatility": 0.3,
                        "liquidity": 3000
                    }
                }
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Company.objects.count(), 2)
        self.assertEqual(Stock.objects.count(), 2)

    def test_add_events_news_triggers_to_scenario(self):
        url = reverse('add_events_news_triggers')  # Adjust the URL name
        data = {
            "scenario_id": self.scenario.id,
            "events": [
                {"name": "Event 1", "description": "Description 1", "timestamp": timezone.now().isoformat()}
            ],
            "news": [
                {"headline": "News 1", "content": "Content 1", "timestamp": timezone.now().isoformat()}
            ],
            "triggers": [
                {"name": "Trigger 1", "condition": "Condition 1", "action": "Action 1"}
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Event.objects.count(), 2)
        self.assertEqual(News.objects.count(), 2)
        self.assertEqual(Trigger.objects.count(), 2)

    def test_review_submit_scenario(self):
        url = reverse('review_submit_scenario')  # Adjust the URL name
        data = {"scenario_id": self.scenario.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Scenario submitted successfully")

