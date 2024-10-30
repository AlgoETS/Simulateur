import json
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from simulation.models import (
    Portfolio, Stock, Order, TransactionHistory, Scenario, UserProfile,
    StockPriceHistory, Company, Simulation, SimulationSettings
)

class BuyStockTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='password')

        # Manual check and create UserProfile if not exists
        if not UserProfile.objects.filter(user=self.user).exists():
            self.user_profile = UserProfile.objects.create(user=self.user)
        else:
            self.user_profile = UserProfile.objects.get(user=self.user)

        # Create necessary scenario-related models
        self.scenario = Scenario.objects.create(name="Test Scenario")
        self.simulation_settings = SimulationSettings.objects.create()
        self.simulation_manager = Simulation.objects.create(
            scenario=self.scenario,
            simulation_settings=self.simulation_settings,
        )

        # Create the portfolio with simulation_manager
        self.portfolio = Portfolio.objects.create(
            owner=self.user_profile,
            balance=Decimal("1000.00"),
            simulation_manager=self.simulation_manager
        )

        self.company = Company.objects.create(name="Test Company")
        self.stock = Stock.objects.create(ticker="AAPL", company=self.company)
        StockPriceHistory.objects.create(stock=self.stock, close_price=Decimal("100.00"))

        self.client.login(username='testuser', password='password')

    def tearDown(self):
        self.client.logout()
        User.objects.all().delete()
        Portfolio.objects.all().delete()
        UserProfile.objects.all().delete()
        Scenario.objects.all().delete()
        Simulation.objects.all().delete()
        SimulationSettings.objects.all().delete()
        Stock.objects.all().delete()
        StockPriceHistory.objects.all().delete()

    def test_buy_stock_success(self):
        url = reverse('buy_stock')
        data = {
            'stock_id': self.stock.id,
            'scenario_id': self.scenario.id,
            'amount': 5,
            'price': 100.00
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('order_id', response.json())

    def test_buy_stock_insufficient_funds(self):
        url = reverse('buy_stock')
        data = {
            'stock_id': self.stock.id,
            'scenario_id': self.scenario.id,
            'amount': 20,
            'price': 100.00
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['message'], 'Insufficient funds')

    def test_buy_stock_invalid_amount(self):
        url = reverse('buy_stock')
        data = {
            'stock_id': self.stock.id,
            'scenario_id': self.scenario.id,
            'amount': -5,
            'price': 100.00
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['message'], 'Amount must be greater than zero')

    def test_buy_stock_invalid_stock(self):
        url = reverse('buy_stock')
        data = {
            'stock_id': 999,
            'scenario_id': self.scenario.id,
            'amount': 5,
            'price': 100.00
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json()['message'], 'Stock not found')


class SellStockTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='password')

        # Manual check and create UserProfile if not exists
        if not UserProfile.objects.filter(user=self.user).exists():
            self.user_profile = UserProfile.objects.create(user=self.user)
        else:
            self.user_profile = UserProfile.objects.get(user=self.user)

        # Create necessary scenario-related models
        self.scenario = Scenario.objects.create(name="Test Scenario")
        self.simulation_settings = SimulationSettings.objects.create()
        self.simulation_manager = Simulation.objects.create(
            scenario=self.scenario,
            simulation_settings=self.simulation_settings,
        )

        # Create the portfolio with simulation_manager
        self.portfolio = Portfolio.objects.create(
            owner=self.user_profile,
            balance=Decimal("1000.00"),
            simulation_manager=self.simulation_manager
        )

        self.company = Company.objects.create(name="Test Company")
        self.stock = Stock.objects.create(ticker="AAPL", company=self.company)
        StockPriceHistory.objects.create(stock=self.stock, close_price=Decimal("100.00"))

        self.client.login(username='testuser', password='password')

    def tearDown(self):
        self.client.logout()
        User.objects.all().delete()
        Portfolio.objects.all().delete()
        UserProfile.objects.all().delete()
        Scenario.objects.all().delete()
        Simulation.objects.all().delete()
        SimulationSettings.objects.all().delete()
        Stock.objects.all().delete()
        StockPriceHistory.objects.all().delete()

    def test_sell_stock_success(self):
        # Assuming user already owns the stock, create a StockPortfolio entry
        self.portfolio.stockportfolio_set.create(stock=self.stock, quantity=10)

        url = reverse('sell_stock')
        data = {
            'stock_id': self.stock.id,
            'scenario_id': self.scenario.id,
            'amount': 5,
            'price': 100.00
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('order_id', response.json())

    def test_sell_stock_insufficient_holdings(self):
        url = reverse('sell_stock')
        data = {
            'stock_id': self.stock.id,
            'scenario_id': self.scenario.id,
            'amount': 50,
            'price': 100.00
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['message'], 'Insufficient stock holdings')


class UserOrdersTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='password')

        # Manual check and create UserProfile if not exists
        if not UserProfile.objects.filter(user=self.user).exists():
            self.user_profile = UserProfile.objects.create(user=self.user)
        else:
            self.user_profile = UserProfile.objects.get(user=self.user)

        self.scenario = Scenario.objects.create(name="Test Scenario")
        self.simulation_settings = SimulationSettings.objects.create()
        self.simulation_manager = Simulation.objects.create(
            scenario=self.scenario,
            simulation_settings=self.simulation_settings,
        )

        self.company = Company.objects.create(name="Test Company")
        self.stock = Stock.objects.create(ticker="AAPL", company=self.company)
        self.transaction_history = TransactionHistory.objects.create(simulation_manager=self.simulation_manager)
        self.order = Order.objects.create(user=self.user_profile, stock=self.stock, quantity=10, price=100.00,
                                          transaction_type='BUY')
        self.transaction_history.orders.add(self.order)

        self.client.login(username='testuser', password='password')

    def tearDown(self):
        self.client.logout()
        User.objects.all().delete()
        UserProfile.objects.all().delete()
        Scenario.objects.all().delete()
        Simulation.objects.all().delete()
        SimulationSettings.objects.all().delete()
        Company.objects.all().delete()
        Stock.objects.all().delete()
        TransactionHistory.objects.all().delete()
        Order.objects.all().delete()

    def test_get_user_orders_success(self):
        url = reverse('user_orders')
        data = {'scenario_id': self.scenario.id}
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['orders']), 1)

    def test_get_user_orders_no_orders(self):
        self.transaction_history.orders.clear()
        url = reverse('user_orders')
        data = {'scenario_id': self.scenario.id}
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['orders']), 0)
