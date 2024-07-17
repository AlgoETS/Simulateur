from simulateur.simulation.logic.noise_patterns.noise_strategy import *



class RandomCandle(NoiseStrategy):


    def generate_noise(self, price, fluctuation_rate, time_index=None):
        """Generate a candlestick using random values."""
        open_price = price
        high_price = open_price + np.random.uniform(0, fluctuation_rate * 5)
        low_price = open_price - np.random.uniform(0, fluctuation_rate * 5)
        close_price = low_price + np.random.uniform(0, (high_price - low_price))
        return {'Open': open_price, 'High': high_price, 'Low': low_price, 'Close': close_price}