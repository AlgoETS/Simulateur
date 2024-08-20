from django.test import TestCase
from unittest.mock import patch, MagicMock
from simulation.logic.broker import Broker
from simulation.models import Stock, UserProfile, Scenario, Portfolio, SimulationSettings
from simulation.logic import BuySellQueue


class BrokerTests(TestCase):

    def setUp(self):
        # Set up necessary mock data
        self.scenario = Scenario.objects.create(name="Test Scenario", description="Test Description", duration=100)
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

        self.stock = Stock.objects.create(company_id=1, ticker="TEST", volatility=0.05, liquidity=0.5, price=100,
                                          low_price=95, high_price=105)
        self.portfolio = Portfolio.objects.create(owner=None, balance=1000)
        self.user_profile = UserProfile.objects.create(user_id=1, portfolio=self.portfolio)

        self.broker = Broker("Algo")

    def test_get_queue_creates_new_queue(self):
        queue = self.broker.get_queue(self.stock.ticker)
        self.assertIsInstance(queue, BuySellQueue)
        self.assertEqual(len(self.broker.queues), 1)

    def test_adjust_client_price_buy(self):
        best_bid, best_ask = 100, 105
        spread = 0.5
        adjusted_price = self.broker.adjust_client_price(best_bid, best_ask, spread, "buy")
        self.assertEqual(adjusted_price, 102.75)

    def test_adjust_client_price_sell(self):
        best_bid, best_ask = 100, 105
        spread = 0.5
        adjusted_price = self.broker.adjust_client_price(best_bid, best_ask, spread, "sell")
        self.assertEqual(adjusted_price, 102.25)

    @patch('simulation.logic.broker.Stock.objects.get')
    def test_get_best_prices(self, mock_get):
        mock_get.return_value = self.stock
        best_bid, best_ask = self.broker.get_best_prices(self.stock.ticker)
        self.assertEqual(best_bid, self.stock.low_price)
        self.assertEqual(best_ask, self.stock.high_price)

    @patch('simulation.logic.broker.Stock.objects.get')
    def test_add_to_buysell_queue_buy(self, mock_get):
        mock_get.return_value = self.stock
        self.broker.add_to_buysell_queue(self.user_profile, self.stock.ticker, 10, 100, "buy")
        queue = self.broker.get_queue(self.stock.ticker)

        self.assertEqual(len(queue.buy_queue), 1)
        self.assertEqual(queue.buy_queue[0][0], self.user_profile)
        self.assertEqual(queue.buy_queue[0][1], self.stock.ticker)

    @patch('simulation.logic.broker.Stock.objects.get')
    def test_add_to_buysell_queue_sell(self, mock_get):
        mock_get.return_value = self.stock
        self.broker.add_to_buysell_queue(self.user_profile, self.stock.ticker, 10, 100, "sell")
        queue = self.broker.get_queue(self.stock.ticker)

        self.assertEqual(len(queue.sell_queue), 1)
        self.assertEqual(queue.sell_queue[0][0], self.user_profile)
        self.assertEqual(queue.sell_queue[0][1], self.stock.ticker)

    @patch('simulation.logic.broker.Stock.objects.get')
    def test_add_to_buysell_queue_adjusts_high_price(self, mock_get):
        mock_get.return_value = self.stock
        self.broker.add_to_buysell_queue(self.user_profile, self.stock.ticker, 10, 110, "buy")
        self.stock.refresh_from_db()
        self.assertEqual(self.stock.high_price, 110)

    @patch('simulation.logic.broker.Stock.objects.get')
    def test_add_to_buysell_queue_adjusts_low_price(self, mock_get):
        mock_get.return_value = self.stock
        self.broker.add_to_buysell_queue(self.user_profile, self.stock.ticker, 10, 90, "sell")
        self.stock.refresh_from_db()
        self.assertEqual(self.stock.low_price, 90)

    @patch('simulation.logic.broker.BuySellQueue.process_queues')
    def test_process_queues(self, mock_process_queues):
        queue = self.broker.get_queue(self.stock.ticker)
        self.broker.process_queues()

        self.assertTrue(mock_process_queues.called)

if __name__ == "__main__":
    unittest.main()
