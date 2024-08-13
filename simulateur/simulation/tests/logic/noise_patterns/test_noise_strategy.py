import unittest
from simulation.logic.noise_patterns.noise_strategy import NoiseStrategy


class TestNoiseStrategy(unittest.TestCase):

    def test_abstract_method(self):
        # Attempt to instantiate the abstract class should raise a TypeError
        with self.assertRaises(TypeError):
            noise_strategy = NoiseStrategy()

    def test_generate_noise_must_be_implemented(self):
        # Create a subclass that does not implement the abstract method
        class IncompleteNoiseStrategy(NoiseStrategy):
            pass

        # Attempt to instantiate the subclass should raise a TypeError
        with self.assertRaises(TypeError):
            incomplete_strategy = IncompleteNoiseStrategy()

    def test_concrete_implementation(self):
        # Create a subclass that implements the abstract method
        class ConcreteNoiseStrategy(NoiseStrategy):
            def generate_noise(self, price, fluctuation_rate, time_index=None):
                return {'Open': price, 'High': price + fluctuation_rate, 'Low': price - fluctuation_rate,
                        'Close': price}

        # Ensure that the subclass can be instantiated and works as expected
        concrete_strategy = ConcreteNoiseStrategy()
        result = concrete_strategy.generate_noise(100, 5)

        # Validate the result
        self.assertEqual(result['Open'], 100)
        self.assertEqual(result['High'], 105)
        self.assertEqual(result['Low'], 95)
        self.assertEqual(result['Close'], 100)


if __name__ == "__main__":
    unittest.main()
