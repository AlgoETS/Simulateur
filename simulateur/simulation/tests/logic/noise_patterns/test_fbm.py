import unittest
import numpy as np
from simulation.logic.noise_patterns.fbm import Fbm


class TestFbm(unittest.TestCase):

    def setUp(self):
        self.noise_strategy = Fbm()

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

        # Check that high price is greater than or equal to the open price
        self.assertGreaterEqual(result['High'], result['Open'])

        # Check that low price is less than or equal to the open price
        self.assertLessEqual(result['Low'], result['Open'])

        # Check that the close price is between the low and high prices
        self.assertGreaterEqual(result['Close'], result['Low'])
        self.assertLessEqual(result['Close'], result['High'])

    def test_fluctuation_range(self):
        price = 100.0
        fluctuation_rate = 1.0
        result = self.noise_strategy.generate_noise(price, fluctuation_rate)

        # Ensure that high price and low price are within the correct fluctuation range
        self.assertTrue(result['High'] <= price + fluctuation_rate * 5)
        self.assertTrue(result['Low'] >= price - fluctuation_rate * 5)

    def test_close_price_within_range(self):
        price = 100.0
        fluctuation_rate = 0.5
        result = self.noise_strategy.generate_noise(price, fluctuation_rate)

        # Ensure that close price is between the low and high prices
        self.assertGreaterEqual(result['Close'], result['Low'])
        self.assertLessEqual(result['Close'], result['High'])
