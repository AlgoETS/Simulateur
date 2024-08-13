import unittest
import numpy as np
import noise
from simulation.logic.noise_patterns.perlin import Perlin

class TestPerlinNoiseStrategy(unittest.TestCase):

    def setUp(self):
        self.perlin = Perlin()

    def test_generate_noise(self):
        price = 100
        fluctuation_rate = 0.05
        time_index = 1

        result = self.perlin.generate_noise(price, fluctuation_rate, time_index)

        # Check that the result is a dictionary with the expected keys
        self.assertIsInstance(result, dict)
        self.assertIn("Open", result)
        self.assertIn("High", result)
        self.assertIn("Low", result)
        self.assertIn("Close", result)

        # Check that the open price is correct
        self.assertEqual(result["Open"], price)

        # Check that high, low, and close prices are valid
        self.assertGreaterEqual(result["High"], result["Open"])
        self.assertGreaterEqual(result["High"], result["Close"])
        self.assertLessEqual(result["Low"], result["Open"])
        self.assertLessEqual(result["Low"], result["Close"])

    def test_fluctuation_rate_impact(self):
        price = 100
        low_fluctuation_rate = 0.01
        high_fluctuation_rate = 0.1
        time_index = 1

        low_fluctuation_result = self.perlin.generate_noise(price, low_fluctuation_rate, time_index)
        high_fluctuation_result = self.perlin.generate_noise(price, high_fluctuation_rate, time_index)

        # The change in price should be smaller with a lower fluctuation rate
        low_fluctuation_change = abs(low_fluctuation_result["Close"] - low_fluctuation_result["Open"])
        high_fluctuation_change = abs(high_fluctuation_result["Close"] - high_fluctuation_result["Open"])

        self.assertLess(low_fluctuation_change, high_fluctuation_change)

    def test_time_index_effect(self):
        price = 100
        fluctuation_rate = 0.05

        result_1 = self.perlin.generate_noise(price, fluctuation_rate, 1)
        result_10 = self.perlin.generate_noise(price, fluctuation_rate, 10)
        result_50 = self.perlin.generate_noise(price, fluctuation_rate, 50)

        # Ensure that time index has an effect on the result
        self.assertNotEqual(result_1["Close"], result_10["Close"])
        self.assertNotEqual(result_1["Close"], result_50["Close"])
        self.assertNotEqual(result_10["Close"], result_50["Close"])

if __name__ == "__main__":
    unittest.main()
