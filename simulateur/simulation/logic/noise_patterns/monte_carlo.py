import numpy as np
from simulation.logic.noise_patterns.noise_strategy import NoiseStrategy


class MonteCarlo(NoiseStrategy):

    def __init__(self, num_simulations=100, time_horizon=1):
        """
        Initializes the Monte Carlo strategy.

        :param num_simulations: Number of paths to simulate (more paths give more accurate results)
        :param time_horizon: Number of time steps (typically representing days) to forecast
        """
        self.num_simulations = num_simulations
        self.time_horizon = time_horizon

    def generate_noise(self, price, fluctuation_rate, time_index=None):
        """
        Generate noise based on a Monte Carlo simulation.

        :param price: The current price of the asset.
        :param fluctuation_rate: The volatility or standard deviation of the asset's returns.
        :param time_index: Optional index to represent the time (not used in this example).
        :return: A dictionary containing the open, high, low, and close prices.
        """
        dt = 1 / self.time_horizon  # Assuming daily steps
        simulated_paths = np.zeros((self.time_horizon, self.num_simulations))
        simulated_paths[0] = price

        # Run the simulation
        for t in range(1, self.time_horizon):
            random_shocks = np.random.normal(loc=0, scale=1, size=self.num_simulations)
            simulated_paths[t] = simulated_paths[t - 1] * np.exp(
                (0 - 0.5 * fluctuation_rate ** 2) * dt + fluctuation_rate * np.sqrt(dt) * random_shocks
            )

        # Extract the final simulated prices and calculate OHLC
        final_prices = simulated_paths[-1]
        close_price = np.mean(final_prices)
        high_price = np.max(final_prices)
        low_price = np.min(final_prices)
        open_price = price

        return {'Open': open_price, 'High': high_price, 'Low': low_price, 'Close': close_price}
