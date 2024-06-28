import logging
import time
import random
import numpy as np
import noise
from django.utils import timezone
from channels.layers import get_channel_layer
from simulation.models import Scenario, SimulationData, Stock, TransactionHistory
from simulation.logic.utils import is_market_open, send_ohlc_update, TIME_UNITS

logger = logging.getLogger(__name__)

class SimulationManager:
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
                    logger.info(f'Simulation time: {current_time}, elapsed time: {elapsed_time}')
                self.broadcast_updates()
                logger.info(f'Sleeping for {self.time_step} seconds')
                time.sleep(self.time_step)
        except KeyboardInterrupt:
            logger.info('Simulation stopped by user')
        except Exception as e:
            logger.error(f'Error occurred during simulation: {e}', exc_info=True)
        finally:
            self.stop_simulation()

    def pause_simulation(self):
        self.running = False
        logger.info('Simulation paused')

    def stop_simulation(self):
        if self.simulation_data:
            self.simulation_data.stop_simulation()
        self.running = False
        logger.info('Simulation stopped')

    def update_prices(self, current_time):
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
        elif self.noise_function == 'fbm':
            change = generate_fbm_candles(asset.price, self.fluctuation_rate)
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
        for company in self.scenario.companies.all():
            if stock := company.stock_set.first():
                send_ohlc_update(self.channel_layer, stock, 'stock')

class SimulationManagerSingleton:
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
    open_price = price
    change = np.random.normal(loc=0, scale=fluctuation_rate)
    close_price = open_price + change
    high_price = max(open_price, close_price) + np.random.uniform(0, fluctuation_rate * 2)
    low_price = min(open_price, close_price) - np.random.uniform(0, fluctuation_rate * 2)
    return {'Open': open_price, 'High': high_price, 'Low': low_price, 'Close': close_price}

def generate_perlin_noise_candle(price, i, fluctuation_rate):
    open_price = price
    change = noise.pnoise1(i * 0.1) * fluctuation_rate * 10
    close_price = open_price + change
    high_price = max(open_price, close_price) + np.random.uniform(0, fluctuation_rate * 2)
    low_price = min(open_price, close_price) - np.random.uniform(0, fluctuation_rate * 2)
    return {'Open': open_price, 'High': high_price, 'Low': low_price, 'Close': close_price}

def generate_random_walk_candle(price, fluctuation_rate):
    open_price = price
    change = np.random.choice([-1, 1]) * np.random.uniform(0, fluctuation_rate * 5)
    close_price = open_price + change
    high_price = max(open_price, close_price)
    low_price = min(open_price, close_price)
    return {'Open': open_price, 'High': high_price, 'Low': low_price, 'Close': close_price}

def generate_random_candle(price, fluctuation_rate):
    open_price = price
    high_price = open_price + np.random.uniform(0, fluctuation_rate * 5)
    low_price = open_price - np.random.uniform(0, fluctuation_rate * 5)
    close_price = low_price + np.random.uniform(0, (high_price - low_price))
    return {'Open': open_price, 'High': high_price, 'Low': low_price, 'Close': close_price}

def generate_fbm_candles(price, fluctuation_rate):
    open_price = price
    high_price = open_price + np.random.uniform(0, fluctuation_rate * 5)
    low_price = open_price - np.random.uniform(0, fluctuation_rate * 5)
    close_price = low_price + np.random.uniform(0, (high_price - low_price))
    return {'Open': open_price, 'High': high_price, 'Low': low_price, 'Close': close_price}


