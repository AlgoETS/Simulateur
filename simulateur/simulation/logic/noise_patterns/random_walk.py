from simulation.logic.noise_patterns.noise_strategy import NoiseStrategy
import numpy as np

class RandomWalk(NoiseStrategy):

    def generate_noise(self, price, fluctuation_rate, time_index=None):
        """Generate a candlestick using a random walk."""
        open_price = price
        change = np.random.choice([-1, 1]) * np.random.uniform(0, fluctuation_rate * 5)
        close_price = open_price + change
        high_price = max(open_price, close_price)
        low_price = min(open_price, close_price)
        return {'Open': open_price, 'High': high_price, 'Low': low_price, 'Close': close_price}