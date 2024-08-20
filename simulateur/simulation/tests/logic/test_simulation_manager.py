from django.test import TestCase
from django.utils import timezone
from simulation.models import Scenario, Stock, StockPriceHistory, SimulationSettings
from simulation.logic.simulation_manager import SimulationManager
from simulation.models import Company


class SimulationManagerTests(TestCase):

    def setUp(self):
        # Set up a company for the stocks
        self.company = Company.objects.create(
            name="Test Company",
            backstory="This is a test company."
        )

        # Set up the simulation settings for testing
        self.simulation_settings = SimulationSettings.objects.create(
            timer_step=10,
            timer_step_unit='second',
            interval=20,
            interval_unit='second',
            max_interval=3000,
            fluctuation_rate=0.1,
            close_stock_market_at_night=False,
            noise_function='brownian',
            stock_trading_logic='static'
        )

        # Set up multiple scenarios and stocks for testing
        self.scenario1 = Scenario.objects.create(
            name="Test Scenario 1",
            description="Test Description 1",
            backstory="Test 1",
            duration=1000
        )
        self.stock1 = Stock.objects.create(
            company=self.company,
            ticker="TEST1",
            volatility=0.05,
            liquidity=0.5,
            price=100  # Initial price for testing
        )
        self.scenario1.stocks.add(self.stock1)

        self.scenario2 = Scenario.objects.create(
            name="Test Scenario 2",
            description="Test Description 2",
            backstory="Test 2",
            duration=1000
        )
        self.stock2 = Stock.objects.create(
            company=self.company,
            ticker="TEST2",
            volatility=0.05,
            liquidity=0.5,
            price=200  # Initial price for testing
        )
        self.scenario2.stocks.add(self.stock2)

        # Initialize SimulationManagers for both scenarios
        self.simulation_manager1 = SimulationManager(self.scenario1)
        self.simulation_manager2 = SimulationManager(self.scenario2)

    def tearDown(self):
        # Clean up after each test
        StockPriceHistory.objects.all().delete()
        Stock.objects.all().delete()
        Scenario.objects.all().delete()
        SimulationSettings.objects.all().delete()
        Company.objects.all().delete()

    def test_update_prices(self):
        current_time = timezone.now()
        self.simulation_manager1.update_prices(current_time)

        self.stock1.refresh_from_db()
        self.assertGreaterEqual(self.stock1.price, self.stock1.low_price)
        self.assertLessEqual(self.stock1.price, self.stock1.high_price)

    def test_start_simulation(self):
        self.simulation_manager1.run_duration = 1  # Set short duration to end simulation quickly
        self.simulation_manager1.start_simulation()

        self.stock1.refresh_from_db()
        self.assertTrue(self.stock1.price > 0)

    def test_get_stocks_with_cache(self):
        stocks = self.simulation_manager1.get_stocks()
        self.assertEqual(stocks, [self.stock1])

    def test_broadcast_update(self):
        current_time = timezone.now()
        self.simulation_manager1.broadcast_update(self.stock1, current_time)

    def test_apply_changes(self):
        current_time = timezone.now()
        change = self.simulation_manager1.apply_changes(self.stock1, current_time)

        self.assertTrue(change["open"] >= 0)
        self.assertTrue(change["close"] >= 0)
        self.stock1.refresh_from_db()
        self.assertEqual(self.stock1.price, change["close"])

    def test_pause_simulation(self):
        self.simulation_manager1.pause_simulation()
        self.assertFalse(self.simulation_manager1.running)

    def test_stop_simulation(self):
        self.simulation_manager1.stop_simulation()
        self.assertFalse(self.simulation_manager1.running)

    def test_multiple_scenarios_simulation(self):
        # Test that both scenarios can run simultaneously without interfering with each other
        self.simulation_manager1.run_duration = 1
        self.simulation_manager2.run_duration = 1

        self.simulation_manager1.start_simulation()
        self.simulation_manager2.start_simulation()

        self.stock1.refresh_from_db()
        self.stock2.refresh_from_db()

        self.assertTrue(self.stock1.price > 0)
        self.assertTrue(self.stock2.price > 0)
        self.assertNotEqual(self.stock1.price, self.stock2.price)
