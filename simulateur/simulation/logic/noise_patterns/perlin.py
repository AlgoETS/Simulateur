from simulateur.simulation.logic.noise_patterns.noise_strategy import *



class Perlin(NoiseStrategy):


    def generate_noise(self, price, fluctuation_rate, time_index=None):
        
        """Generate a candlestick using Perlin noise."""
        open_price = price
        change = noise.pnoise1(time_index * 0.1) * fluctuation_rate * 10
        close_price = open_price + change
        high_price = max(open_price, close_price) + np.random.uniform(0, fluctuation_rate * 2)
        low_price = min(open_price, close_price) - np.random.uniform(0, fluctuation_rate * 2)
        return {'Open': open_price, 'High': high_price, 'Low': low_price, 'Close': close_price}


