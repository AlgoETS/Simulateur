import os
from unittest import skipUnless

import ollama
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from simulation.models import Company, Stock


def check_ollama_service():
    model_name = os.environ.get('OLLAMA_MODEL', 'llama3')
    try:
        response = ollama.chat(model=model_name, messages=[{'role': 'user', 'content': 'Test message'}])
        return True
    except ollama.ResponseError as e:
        if e.status_code == 404 and f'model {model_name} not found' in e.error:
            return False
        return False
    except Exception as e:
        return False


@skipUnless(check_ollama_service(), "Ollama service is not available")
class InteractWithOllamaTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('interact-with-ollama')
        self.valid_payload = {'data': 'Tell me a joke'}

    @skipUnless(check_ollama_service(), "Ollama service is not available")
    def test_valid_interact_with_ollama(self):
        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)

    @skipUnless(check_ollama_service(), "Ollama service is not available")
    def test_invalid_interact_with_ollama(self):
        response = self.client.post(self.url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


@skipUnless(check_ollama_service(), "Ollama service is not available")
class CreateNewsAITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.company = Company.objects.create(name='Test Company', backstory='Test Backstory', sector='Test Sector',
                                              country='Test Country', industry='Test Industry')
        self.stock = Stock.objects.create(company=self.company, ticker='TEST')
        self.url = reverse('create-news-ai')
        self.valid_payload = {'company_id': self.company.id, 'stock_id': self.stock.id}

    @skipUnless(check_ollama_service(), "Ollama service is not available")
    def test_valid_create_news_ai(self):
        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)

    @skipUnless(check_ollama_service(), "Ollama service is not available")
    def test_invalid_create_news_ai(self):
        response = self.client.post(self.url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


@skipUnless(check_ollama_service(), "Ollama service is not available")
class CreateEventAITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.company = Company.objects.create(name='Test Company', backstory='Test Backstory', sector='Test Sector',
                                              country='Test Country', industry='Test Industry')
        self.stock = Stock.objects.create(company=self.company, ticker='TEST')
        self.url = reverse('create-event-ai')
        self.valid_payload = {'company_id': self.company.id, 'stock_id': self.stock.id}

    @skipUnless(check_ollama_service(), "Ollama service is not available")
    def test_valid_create_event_ai(self):
        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)

    @skipUnless(check_ollama_service(), "Ollama service is not available")
    def test_invalid_create_event_ai(self):
        response = self.client.post(self.url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


@skipUnless(check_ollama_service(), "Ollama service is not available")
class CreateTriggerAITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.company = Company.objects.create(name='Test Company', backstory='Test Backstory', sector='Test Sector',
                                              country='Test Country', industry='Test Industry')
        self.stock = Stock.objects.create(company=self.company, ticker='TEST')
        self.url = reverse('create-trigger-ai')
        self.valid_payload = {'company_id': self.company.id, 'stock_id': self.stock.id}

    def test_valid_create_trigger_ai(self):
        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)

    def test_invalid_create_trigger_ai(self):
        response = self.client.post(self.url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


@skipUnless(check_ollama_service(), "Ollama service is not available")
class CreateCompanyAndStockAITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('create-company-stock-ai')

    @skipUnless(check_ollama_service(), "Ollama service is not available")
    def test_valid_create_company_and_stock_ai(self):
        response = self.client.post(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('company', response.data)
        self.assertIn('stock', response.data)

    @skipUnless(check_ollama_service(), "Ollama service is not available")
    def test_invalid_create_company_and_stock_ai(self):
        response = self.client.post(self.url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


@skipUnless(check_ollama_service(), "Ollama service is not available")
class CreateScenarioAITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('create-scenario-ai')

    @skipUnless(check_ollama_service(), "Ollama service is not available")
    def test_valid_create_scenario_ai(self):
        response = self.client.post(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('data', response.data)

    @skipUnless(check_ollama_service(), "Ollama service is not available")
    def test_invalid_create_scenario_ai(self):
        response = self.client.post(self.url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)