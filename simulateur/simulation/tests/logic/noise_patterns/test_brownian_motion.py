import unittest
import numpy as np
from simulation.logic.noise_patterns.brownian_motion import BrownianMotion


class TestBrownianMotion(unittest.TestCase):

    def setUp(self):
        self.noise_strategy = BrownianMotion()

    def test_generate_noise(self):
        price = 100.0
        fluctuation_rate = 0.5
        result = self.noise_strategy.generate_noise(price, fluctuation_rate)

        # Check if keys are in the result
        self.assertIn('Open', result)
        self.assertIn('High', result)
        self.assertIn('Low', result)
        self.assertIn('Close', result)

        # Check if the open price is the same as the input price
        self.assertEqual(result['Open'], price)

        # Check that the close price is within the fluctuation range
        self.assertGreaterEqual(result['Close'], price - fluctuation_rate)
        self.assertLessEqual(result['Close'], price + fluctuation_rate)

        # Check that high price is at least as large as the open and close prices
        self.assertGreaterEqual(result['High'], max(result['Open'], result['Close']))

        # Check that low price is at most as small as the open and close prices
        self.assertLessEqual(result['Low'], min(result['Open'], result['Close']))

    def test_fluctuation_range(self):
        price = 100.0
        fluctuation_rate = 1.0
        result = self.noise_strategy.generate_noise(price, fluctuation_rate)

        # Ensure that close price is within the correct range
        self.assertTrue(price - fluctuation_rate <= result['Close'] <= price + fluctuation_rate)

    def test_high_and_low_prices(self):
        price = 100.0
        fluctuation_rate = 0.5
        result = self.noise_strategy.generate_noise(price, fluctuation_rate)

        # Check high price
        self.assertGreaterEqual(result['High'], result['Close'])
        self.assertGreaterEqual(result['High'], result['Open'])

        # Check low price
        self.assertLessEqual(result['Low'], result['Close'])
        self.assertLessEqual(result['Low'], result['Open'])