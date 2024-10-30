import numpy as np
import pandas as pd
from simulation.logic.noise_patterns.noise_strategy import NoiseStrategy

# Geometric Brownian Motion (GBM) Class
class GeometricBrownianMotion(NoiseStrategy):
    def generate_noise(self, price, drift, volatility, time_index=None):
        open_price = price
        # GBM process: S(t+dt) = S(t) * exp((mu - 0.5 * sigma^2) * dt + sigma * sqrt(dt) * N(0,1))
        dt = 1.0
        change = (drift - 0.5 * volatility**2) * dt + volatility * np.sqrt(dt) * np.random.normal()
        close_price = open_price * np.exp(change)
        high_price = max(open_price, close_price) + np.random.uniform(0, volatility)
        low_price = min(open_price, close_price) - np.random.uniform(0, volatility)
        return {'Open': open_price, 'High': high_price, 'Low': low_price, 'Close': close_price}
