import numpy as np
import pandas as pd
from simulation.logic.noise_patterns.noise_strategy import NoiseStrategy

# Vasicek Noise Class
class VasicekNoise(NoiseStrategy):
    def __init__(self, theta=2.0, mu=0.05, sigma=0.02, r0=0.03, dt=1.0):
        self.theta = theta  # Speed of reversion to the mean
        self.mu = mu        # Long-term mean rate
        self.sigma = sigma  # Volatility
        self.r0 = r0        # Initial rate
        self.dt = dt        # Time step

    def generate_noise(self, price=None, fluctuation_rate=None, time_index=None):
        if price is None:
            price = self.r0  # Use initial rate if none is provided
        open_price = price
        # Vasicek process: dr(t) = theta*(mu - r(t))*dt + sigma*sqrt(dt)*N(0,1)
        change = self.theta * (self.mu - price) * self.dt + self.sigma * np.sqrt(self.dt) * np.random.normal()
        close_price = open_price + change
        # Relative intraday volatility based on sigma
        intraday_vol = self.sigma * np.random.uniform(0.5, 1.5)
        high_price = max(open_price, close_price) + intraday_vol
        low_price = min(open_price, close_price) - intraday_vol
        return {'Open': open_price, 'High': high_price, 'Low': low_price, 'Close': close_price}
