from django.test import TestCase
from unittest.mock import MagicMock
from collections import deque
from django.utils import timezone
from simulation.models import UserProfile, Stock, Order, TransactionHistory, Portfolio, Scenario, SimulationSettings
from simulation.logic.broker import BuySellQueue


class BuySellQueueTests(TestCase):

    def setUp(self):
        # Set up necessary mock data
        self.scenario = Scenario.objects.create(name="Test Scenario", description="Test", duration=100)
        self.simulation_settings = SimulationSettings.objects.create(
            timer_step=10,
            timer_step_unit='minute',
            interval=20,
            interval_unit='minute',
            max_interval=3000,
            fluctuation_rate=0.1,
            close_stock_market_at_night=True,
            noise_function='brownian',
            stock_trading_logic='dynamic',
        )
        self.scenario.simulation_settings = self.simulation_settings
        self.scenario.save()

        self.stock = Stock.objects.create(company_id=1, ticker="TEST", volatility=0.05, liquidity=0.5, price=100)
        self.portfolio1 = Portfolio.objects.create(owner=None, balance=1000)
        self.portfolio2 = Portfolio.objects.create(owner=None, balance=1000)

        self.user_profile1 = UserProfile.objects.create(user_id=1, portfolio=self.portfolio1)
        self.user_profile2 = UserProfile.objects.create(user_id=2, portfolio=self.portfolio2)

        self.buy_sell_queue = BuySellQueue()

    def test_add_to_buy_queue(self):
        self.buy_sell_queue.add_to_buy_queue(self.user_profile1, self.stock, 10, 100, self.scenario)
        self.assertEqual(len(self.buy_sell_queue.buy_queue), 1)
        self.assertEqual(self.buy_sell_queue.buy_queue[0], (self.user_profile1, self.stock, 10, 100, self.scenario))

    def test_add_to_sell_queue(self):
        self.buy_sell_queue.add_to_sell_queue(self.user_profile2, self.stock, 5, 95, self.scenario)
        self.assertEqual(len(self.buy_sell_queue.sell_queue), 1)
        self.assertEqual(self.buy_sell_queue.sell_queue[0], (self.user_profile2, self.stock, 5, 95, self.scenario))

    def test_process_queues_with_matching_prices(self):
        self.buy_sell_queue.add_to_buy_queue(self.user_profile1, self.stock, 10, 100, self.scenario)
        self.buy_sell_queue.add_to_sell_queue(self.user_profile2, self.stock, 10, 100, self.scenario)

        transactions = self.buy_sell_queue.process_queues()

        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0]['buyer'], self.user_profile1.user.username)
        self.assertEqual(transactions[0]['seller'], self.user_profile2.user.username)
        self.assertEqual(transactions[0]['asset'], self.stock.name)
        self.assertEqual(transactions[0]['amount'], 10)
        self.assertEqual(transactions[0]['price'], 100)

    def test_partial_transaction(self):
        self.buy_sell_queue.add_to_buy_queue(self.user_profile1, self.stock, 10, 100, self.scenario)
        self.buy_sell_queue.add_to_sell_queue(self.user_profile2, self.stock, 5, 100, self.scenario)

        transactions = self.buy_sell_queue.process_queues()

        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0]['amount'], 5)
        self.assertEqual(len(self.buy_sell_queue.buy_queue), 1)  # Remaining 5 in buy queue

    def test_complete_transaction(self):
        self.buy_sell_queue.add_to_buy_queue(self.user_profile1, self.stock, 5, 100, self.scenario)
        self.buy_sell_queue.add_to_sell_queue(self.user_profile2, self.stock, 5, 100, self.scenario)

        transactions = self.buy_sell_queue.process_queues()

        self.assertEqual(len(transactions), 1)
        self.assertEqual(len(self.buy_sell_queue.buy_queue), 0)
        self.assertEqual(len(self.buy_sell_queue.sell_queue), 0)

    def test_process_queues_with_non_matching_prices(self):
        self.buy_sell_queue.add_to_buy_queue(self.user_profile1, self.stock, 10, 90, self.scenario)
        self.buy_sell_queue.add_to_sell_queue(self.user_profile2, self.stock, 10, 100, self.scenario)

        transactions = self.buy_sell_queue.process_queues()

        self.assertEqual(len(transactions), 0)  # No transactions should occur

    def test_log_transaction(self):
        self.buy_sell_queue.log_transaction = MagicMock()
        self.buy_sell_queue.add_to_buy_queue(self.user_profile1, self.stock, 10, 100, self.scenario)
        self.buy_sell_queue.add_to_sell_queue(self.user_profile2, self.stock, 10, 100, self.scenario)

        transactions = self.buy_sell_queue.process_queues()

        self.assertTrue(self.buy_sell_queue.log_transaction.called)

if __name__ == "__main__":
    unittest.main()
