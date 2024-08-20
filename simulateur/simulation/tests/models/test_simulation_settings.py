from django.test import TestCase
from simulation.models import SimulationSettings


class SimulationSettingsModelTest(TestCase):

    def setUp(self):
        self.simulation_settings = SimulationSettings.objects.create(
            timer_step=15,
            timer_step_unit='minute',
            interval=30,
            interval_unit='minute',
            max_interval=3600,
            fluctuation_rate=0.05,
            close_stock_market_at_night=False,
            noise_function='perlin',
            stock_trading_logic='dynamic'
        )

    def tearDown(self):
        self.simulation_settings.delete()

    def test_simulation_settings_creation(self):
        # Test if the SimulationSettings object was created successfully
        self.assertEqual(self.simulation_settings.timer_step, 15)
        self.assertEqual(self.simulation_settings.timer_step_unit, 'minute')
        self.assertEqual(self.simulation_settings.interval, 30)
        self.assertEqual(self.simulation_settings.interval_unit, 'minute')
        self.assertEqual(self.simulation_settings.max_interval, 3600)
        self.assertEqual(self.simulation_settings.fluctuation_rate, 0.05)
        self.assertFalse(self.simulation_settings.close_stock_market_at_night)
        self.assertEqual(self.simulation_settings.noise_function, 'perlin')
        self.assertEqual(self.simulation_settings.stock_trading_logic, 'dynamic')

    def test_default_values(self):
        # Test the default values of fields
        simulation_settings_default = SimulationSettings.objects.create()
        self.assertEqual(simulation_settings_default.timer_step, 10)
        self.assertEqual(simulation_settings_default.timer_step_unit, 'second')
        self.assertEqual(simulation_settings_default.interval, 20)
        self.assertEqual(simulation_settings_default.interval_unit, 'second')
        self.assertEqual(simulation_settings_default.max_interval, 3000)
        self.assertEqual(simulation_settings_default.fluctuation_rate, 0.1)
        self.assertTrue(simulation_settings_default.close_stock_market_at_night)
        self.assertEqual(simulation_settings_default.noise_function, 'brownian')
        self.assertEqual(simulation_settings_default.stock_trading_logic, 'static')

    def test_simulation_settings_str_method(self):
        # Test the __str__ method
        expected_str = 'Simulation Settings: 1'
        self.assertEqual(str(self.simulation_settings), expected_str)
