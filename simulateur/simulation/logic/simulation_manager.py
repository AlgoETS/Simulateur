import logging
import time
import random
import numpy as np
import noise
from django.utils import timezone
from channels.layers import get_channel_layer
from simulation.models import Scenario, SimulationData, Stock, TransactionHistory
from simulation.logic.utils import is_market_open, send_ohlc_update, TIME_UNITS

# Set up logging
logger = logging.getLogger(__name__)

class SimulationManager:
    """
    Manages the simulation of stock prices based on various algorithms.
    """
    def __init__(self, scenario_id, run_duration=100000):
        self.scenario = Scenario.objects.get(id=scenario_id)
        self.channel_layer = get_channel_layer()
        self.running = False
        self.simulation_data = None
        self.run_duration = run_duration

        settings = self.scenario.simulation_settings
        self.time_step = settings.timer_step * TIME_UNITS[settings.timer_step_unit]
        self.interval = settings.interval * TIME_UNITS[settings.interval_unit]
        self.close_stock_market_at_night = settings.close_stock_market_at_night
        self.fluctuation_rate = settings.fluctuation_rate
        self.noise_function = settings.noise_function.lower()

        self.stock_prices = {stock.company.name: [] for stock in Stock.objects.all()}

        logger.info(f'Starting simulation for scenario {self.scenario} with time step {self.time_step} seconds')

    def start_simulation(self):
        """
        Starts the simulation.
        """
        self.running = True
        self.simulation_data = SimulationData.objects.create(scenario=self.scenario)
        start_time = timezone.now()
        try:
            while self.running:
                current_time = timezone.now()
                elapsed_time = (current_time - start_time).total_seconds()

                if elapsed_time >= self.run_duration:
                    logger.info('Run duration reached, stopping simulation')
                    break

                if self.close_stock_market_at_night and not is_market_open(current_time):
                    logger.info('Stock market is closed')
                else:
                    self.update_prices(current_time)
                self.broadcast_updates()
                time.sleep(self.time_step)
        except KeyboardInterrupt:
            logger.info('Simulation stopped by user')
        except Exception as e:
            logger.error(f'Error occurred during simulation: {e}', exc_info=True)
        finally:
            self.stop_simulation()

    def pause_simulation(self):
        """
        Pauses the simulation.
        """
        self.running = False
        logger.info('Simulation paused')

    def stop_simulation(self):
        """
        Stops the simulation and updates the simulation data.
        """
        if self.simulation_data:
            self.simulation_data.stop_simulation()
        self.running = False
        logger.info('Simulation stopped')

    def update_prices(self, current_time):
        """
        Updates the prices of stocks.
        """
        for company in self.scenario.companies.all():
            if stock := company.stock_set.first():
                self.apply_changes(stock, current_time)
                self.stock_prices[stock.company.name].append(stock.close_price)

        self.simulation_data.end_time = current_time
        self.simulation_data.save()

    def apply_changes(self, asset, current_time):
        """
        Applies changes to the asset prices using the chosen noise function.
        """
        if self.noise_function == 'brownian':
            change = generate_brownian_motion_candle(asset.price, self.fluctuation_rate)
        elif self.noise_function == 'perlin':
            change = generate_perlin_noise_candle(asset.price, len(asset.value_history), self.fluctuation_rate)
        elif self.noise_function == 'random_walk':
            change = generate_random_walk_candle(asset.price, self.fluctuation_rate)
        else:
            change = generate_random_candle(asset.price, self.fluctuation_rate)

        asset.open_price = change['Open']
        asset.high_price = change['High']
        asset.low_price = change['Low']
        asset.close_price = change['Close']
        asset.price = change['Close']

        asset.value_history.append(asset.price)
        asset.save()


    def broadcast_updates(self):
        """
        Broadcasts the latest price updates to the front-end.
        """
        for company in self.scenario.companies.all():
            if stock := company.stock_set.first():
                send_ohlc_update(self.channel_layer, stock, 'stock')


class SimulationManagerSingleton:
    """
    Singleton class for managing simulation instances.
    """
    _instances = {}

    @classmethod
    def get_instance(cls, scenario_id):
        if scenario_id not in cls._instances:
            cls._instances[scenario_id] = SimulationManager(scenario_id)
        return cls._instances[scenario_id]

    @classmethod
    def remove_instance(cls, scenario_id):
        if scenario_id in cls._instances:
            del cls._instances[scenario_id]


def generate_brownian_motion_candle(price, fluctuation_rate):
    """
    Generates a single Brownian motion candle.
    """
    open_price = price
    change = np.random.normal(loc=0, scale=fluctuation_rate)
    close_price = open_price + change
    high_price = max(open_price, close_price) + np.random.uniform(0, fluctuation_rate * 2)
    low_price = min(open_price, close_price) - np.random.uniform(0, fluctuation_rate * 2)
    return {'Open': open_price, 'High': high_price, 'Low': low_price, 'Close': close_price}

def generate_perlin_noise_candle(price, i, fluctuation_rate):
    """
    Generates a single Perlin noise candle.
    """
    open_price = price
    change = noise.pnoise1(i * 0.1) * fluctuation_rate * 10
    close_price = open_price + change
    high_price = max(open_price, close_price) + np.random.uniform(0, fluctuation_rate * 2)
    low_price = min(open_price, close_price) - np.random.uniform(0, fluctuation_rate * 2)
    return {'Open': open_price, 'High': high_price, 'Low': low_price, 'Close': close_price}

def generate_random_walk_candle(price, fluctuation_rate):
    """
    Generates a single random walk candle.
    """
    open_price = price
    change = np.random.choice([-1, 1]) * np.random.uniform(0, fluctuation_rate * 5)
    close_price = open_price + change
    high_price = max(open_price, close_price)
    low_price = min(open_price, close_price)
    return {'Open': open_price, 'High': high_price, 'Low': low_price, 'Close': close_price}

def generate_random_candle(price, fluctuation_rate):
    """
    Generates a single random candle.
    """
    open_price = price
    high_price = open_price + np.random.uniform(0, fluctuation_rate * 5)
    low_price = open_price - np.random.uniform(0, fluctuation_rate * 5)
    close_price = low_price + np.random.uniform(0, (high_price - low_price))
    return {'Open': open_price, 'High': high_price, 'Low': low_price, 'Close': close_price}


def update_ohlc(asset):
    """
    Updates the OHLC (Open, High, Low, Close) values for the asset.
    """
    if not asset.open_price:
        asset.open_price = asset.price
    if not asset.high_price or asset.price > asset.high_price:
        asset.high_price = asset.price
    if not asset.low_price or asset.price < asset.low_price:
        asset.low_price = asset.price
    asset.close_price = asset.price
    asset.save()

def log_transactions(transactions):
    """
    Logs the transactions to the database.
    """
    for transaction in transactions:
        TransactionHistory.objects.create(
            portfolio=transaction['portfolio'],
            asset=transaction['asset'],
            transaction_type=transaction['transaction_type'],
            amount=transaction['amount'],
            price=transaction['price']
        )
