from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from simulation.models import Company, Stock, News, Scenario, SimulationSettings

class InteractWithOllamaTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('interact-with-ollama')
        self.valid_payload = {'data': 'Tell me a joke'}

    def test_valid_interact_with_ollama(self):
        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)

    def test_invalid_interact_with_ollama(self):
        response = self.client.post(self.url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class CreateNewsAITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.company = Company.objects.create(name='Test Company', backstory='Test Backstory', sector='Test Sector', country='Test Country', industry='Test Industry')
        self.stock = Stock.objects.create(company=self.company, ticker='TEST', price=100.0, open_price=100.0, high_price=100.0, low_price=100.0, close_price=100.0, partial_share=1.0, complete_share=1)
        self.url = reverse('create-news-ai')
        self.valid_payload = {'company_id': self.company.id, 'stock_id': self.stock.id}

    def test_valid_create_news_ai(self):
        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)

    def test_invalid_create_news_ai(self):
        response = self.client.post(self.url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class CreateEventAITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.company = Company.objects.create(name='Test Company', backstory='Test Backstory', sector='Test Sector', country='Test Country', industry='Test Industry')
        self.stock = Stock.objects.create(company=self.company, ticker='TEST', price=100.0, open_price=100.0, high_price=100.0, low_price=100.0, close_price=100.0, partial_share=1.0, complete_share=1)
        self.url = reverse('create-event-ai')
        self.valid_payload = {'company_id': self.company.id, 'stock_id': self.stock.id}

    def test_valid_create_event_ai(self):
        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)

    def test_invalid_create_event_ai(self):
        response = self.client.post(self.url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class CreateTriggerAITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.company = Company.objects.create(name='Test Company', backstory='Test Backstory', sector='Test Sector', country='Test Country', industry='Test Industry')
        self.stock = Stock.objects.create(company=self.company, ticker='TEST', price=100.0, open_price=100.0, high_price=100.0, low_price=100.0, close_price=100.0, partial_share=1.0, complete_share=1)
        self.url = reverse('create-trigger-ai')
        self.valid_payload = {'company_id': self.company.id, 'stock_id': self.stock.id}

    def test_valid_create_trigger_ai(self):
        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)

    def test_invalid_create_trigger_ai(self):
        response = self.client.post(self.url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class CreateCompanyAndStockAITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('create-company-stock-ai')

    def test_valid_create_company_and_stock_ai(self):
        response = self.client.post(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('company', response.data)
        self.assertIn('stock', response.data)

    def test_invalid_create_company_and_stock_ai(self):
        response = self.client.post(self.url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class CreateScenarioAITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('create-scenario-ai')

    def test_valid_create_scenario_ai(self):
        response = self.client.post(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('data', response.data)

    def test_invalid_create_scenario_ai(self):
        response = self.client.post(self.url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
