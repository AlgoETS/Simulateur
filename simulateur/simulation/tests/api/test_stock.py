from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from simulation.models import Stock, StockPriceHistory, Company


class StockManagementTests(APITestCase):

    def setUp(self):
        # Create a company to associate with stocks
        self.company = Company.objects.create(
            name="Test Company",
            backstory="This is a test company.",
            sector="Technology",
            country="USA",
            industry="Software"
        )

        # Create a stock associated with the company
        self.stock = Stock.objects.create(
            company=self.company,
            ticker="TEST",
            volatility=1.5,
            liquidity=1000.0
        )

        # URLs for StockManagement
        self.create_url = reverse('create_stock')
        self.manage_url = reverse('manage_stock', kwargs={'stock_id': self.stock.id})

    def test_create_stock(self):
        """Test creating a stock via POST request."""
        data = {
            'company': self.company.id,
            'ticker': 'NEW',
            'volatility': 2.0,
            'liquidity': 5000.0
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Stock.objects.count(), 2)
        self.assertEqual(Stock.objects.get(id=response.data['data']['id']).ticker, 'NEW')

    def test_update_stock(self):
        """Test updating a stock via PUT request."""
        updated_data = {
            'ticker': 'UPDATED',
            'volatility': 3.0,
            'liquidity': 7500.0
        }
        response = self.client.put(self.manage_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.stock.refresh_from_db()
        self.assertEqual(self.stock.ticker, 'UPDATED')
        self.assertEqual(self.stock.volatility, 3.0)
        self.assertEqual(self.stock.liquidity, 7500.0)

    def test_delete_stock(self):
        """Test deleting a stock via DELETE request."""
        response = self.client.delete(self.manage_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Stock.objects.count(), 0)

    def test_get_single_stock(self):
        """Test retrieving a single stock via GET request."""
        response = self.client.get(self.manage_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['ticker'], self.stock.ticker)

    def test_get_all_stocks(self):
        """Test retrieving all stocks via GET request."""
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 1)
        self.assertEqual(response.data['data'][0]['ticker'], self.stock.ticker)


class StockPriceHistoryManagementTests(APITestCase):

    def setUp(self):
        # Create a company and a stock
        self.company = Company.objects.create(
            name="Test Company",
            backstory="This is a test company.",
            sector="Technology",
            country="USA",
            industry="Software"
        )
        self.stock = Stock.objects.create(
            company=self.company,
            ticker="TEST",
            volatility=1.5,
            liquidity=1000.0
        )
        # Create a stock price history
        self.price_history = StockPriceHistory.objects.create(
            stock=self.stock,
            open_price=100.0,
            high_price=110.0,
            low_price=90.0,
            close_price=105.0,
            volatility=1.2,
            liquidity=800.0
        )

        # URLs for StockPriceHistoryManagement
        self.get_url = reverse('price_history_detail', kwargs={'price_history_id': self.price_history.id})

    def test_get_single_price_history(self):
        """Test retrieving a single stock price history via GET request."""
        response = self.client.get(self.get_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['open_price'], self.price_history.open_price)

    def test_get_all_price_histories(self):
        """Test retrieving all stock price histories via GET request."""
        response = self.client.get(reverse('price_history_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 1)
        self.assertEqual(response.data['data'][0]['stock'], self.stock.ticker)
