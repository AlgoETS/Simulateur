from simulateur.simulation.logic.noise_patterns.noise_strategy import Noise
import numpy as np

class BrownianMotion(Noise):

    def generate_noise(self,price, fluctuation_rate,time_index=None):
        open_price = price
        change = np.random.normal(loc=0, scale=fluctuation_rate)
        close_price = open_price + change
        high_price = max(open_price, close_price) + np.random.uniform(0, fluctuation_rate * 2)
        low_price = min(open_price, close_price) - np.random.uniform(0, fluctuation_rate * 2)
        return {'Open': open_price, 'High': high_price, 'Low': low_price, 'Close': close_price}


