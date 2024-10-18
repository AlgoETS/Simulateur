import numpy as np
import pandas as pd
from simulation.logic.noise_patterns.noise_strategy import NoiseStrategy

class HestonModel(NoiseStrategy):
    def __init__(self, kappa, theta, xi, rho):
        self.kappa = kappa  # Speed of mean reversion for volatility
        self.theta = theta  # Long-term variance (volatility squared)
        self.xi = xi        # Volatility of volatility
        self.rho = rho      # Correlation between price and volatility

    def generate_noise(self, price, variance, drift, dt=1.0):
        open_price = price
        # Simulate correlated Wiener processes for price and volatility
        dw1 = np.random.normal()
        dw2 = np.random.normal()
        correlated_dw2 = self.rho * dw1 + np.sqrt(1 - self.rho**2) * dw2

        # Heston model for variance (volatility squared)
        variance_change = self.kappa * (self.theta - variance) * dt + self.xi * np.sqrt(variance) * correlated_dw2
        variance = max(variance + variance_change, 0)  # Ensure variance is non-negative
        
        # Heston model for price
        price_change = drift * open_price * dt + np.sqrt(variance) * open_price * dw1
        close_price = open_price + price_change

        high_price = max(open_price, close_price) + np.random.uniform(0, np.sqrt(variance))
        low_price = min(open_price, close_price) - np.random.uniform(0, np.sqrt(variance))
        
        return {'Open': open_price, 'High': high_price, 'Low': low_price, 'Close': close_price, 'Variance': variance}
