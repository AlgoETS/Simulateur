import numpy as np
import pandas as pd
from simulation.logic.noise_patterns.noise_strategy import NoiseStrategy

# Ornstein-Uhlenbeck Noise Class
class OrnsteinUhlenbeckNoise(NoiseStrategy):
    def __init__(self, theta=0.7, mu=100, sigma=2.0, X0=100.0, dt=1.0):
        self.theta = theta  # Speed of reversion to the mean
        self.mu = mu        # Long-term mean price level
        self.sigma = sigma  # Volatility
        self.X0 = X0        # Initial price
        self.dt = dt        # Time step

    def generate_noise(self, price=None, fluctuation_rate=None, time_index=None):
        if price is None:
            price = self.X0  # Use initial price if none is provided
        open_price = price
        # OU process: X(t+dt) = X(t) + theta*(mu - X(t))*dt + sigma*sqrt(dt)*N(0,1)
        change = self.theta * (self.mu - price) * self.dt + self.sigma * np.sqrt(self.dt) * np.random.normal()
        close_price = open_price + change
        high_price = max(open_price, close_price) + np.random.uniform(0, 1)
        low_price = min(open_price, close_price) - np.random.uniform(0, 1)
        return {'Open': open_price, 'High': high_price, 'Low': low_price, 'Close': close_price}
