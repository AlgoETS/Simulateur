import logging
import time
from django.utils import timezone
from channels.layers import get_channel_layer
from simulation.models import Scenario, Stock, StockPriceHistory
from simulation.logic.noise_patterns.strategies import *
from simulation.logic.broker import broker
from simulation.logic.utils import (
    is_market_open,
    send_ohlc_update,
    TIME_UNITS
)


logger = logging.getLogger(__name__)

class SimulationManager:
    def __init__(self, scenario_id, run_duration=100000):
        self.scenario = Scenario.objects.get(id=scenario_id)
        self.channel_layer = get_channel_layer()
        self.running = False
        self.run_duration = run_duration
        self.settings = self.scenario.simulation_settings
        self.time_step = self.settings.timer_step * TIME_UNITS[self.settings.timer_step_unit]
        self.interval = self.settings.interval * TIME_UNITS[self.settings.interval_unit]
        self.close_stock_market_at_night = self.settings.close_stock_market_at_night
        self.fluctuation_rate = self.settings.fluctuation_rate
        self.noise_function = self.settings.noise_function.lower()
        self.time_index = 0
        self.noise_strategy = NoiseStrategy()
        self.trading_strategy = self.settings.stock_trading_logic
        self.broker = broker

        logger.info(f'Starting simulation for scenario {self.scenario} with time step {self.time_step} seconds')

    def start_simulation(self):
        self.running = True
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
                    if self.trading_strategy == 'static': 
                        self.update_prices(current_time)
                    else :
                        self.broker.processQueues()
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
        self.running = False
        logger.info('Simulation stopped')

    def update_prices(self, current_time):
        stocks = Scenario.objects.get(id=self.scenario.id).stocks.all()
        for stock in stocks:
            change = self.apply_changes(stock, current_time)
            StockPriceHistory.objects.create(
                stock=stock,
                open_price=change['open'],
                high_price=change['high'],
                low_price=change['low'],
                close_price=change['close'],
                timestamp=current_time
            )

    def apply_changes(self, stock, current_time):
        if self.noise_function == 'brownian':
            self.noise_strategy = BrownianMotion()
        elif self.noise_function == 'perlin':
            self.noise_strategy = Perlin()
        elif self.noise_function == 'random_walk':
            self.noise_strategy = RandomWalk()
        elif self.noise_function == 'fbm':
            self.noise_strategy = Fbm()
        elif self.noise_function == 'random':
            self.noise_strategy = RandomCandle()
        else:
            raise ValueError(f"Unsupported noise function: {self.noise_function}")
        
        change = self.noise_strategy.generate_noise(stock.price,self.fluctuation_rate,self.time_index)
        self.time_index += 1
        stock.open_price = change['Open']
        stock.high_price = change['High']
        stock.low_price = change['Low']
        stock.close_price = change['Close']
        stock.price = change['Close']
        stock.save()

        return {
            'ticker': stock.ticker,
            'open': stock.open_price,
            'high': stock.high_price,
            'low': stock.low_price,
            'close': stock.close_price,
            'time': current_time.isoformat()
        }

    def broadcast_updates(self):
        stocks = Scenario.objects.get(id=self.scenario.id).stocks.all()
        for stock in stocks:
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
