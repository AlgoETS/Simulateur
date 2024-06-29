import logging
import time
from django.utils import timezone
from channels.layers import get_channel_layer
<<<<<<< HEAD
from simulation.models import Scenario, Stock, StockPriceHistory
from simulation.logic.utils import (
    generate_brownian_motion_candle,
    generate_fbm_candles,
    generate_perlin_noise_candle,
    generate_random_candle,
    generate_random_walk_candle,
    is_market_open,
    send_ohlc_update,
    TIME_UNITS
)
=======
from simulation.models import Scenario, SimulationData, Stock, StockPriceHistory
from simulation.logic.utils import generate_brownian_motion_candle, is_market_open, send_ohlc_update, TIME_UNITS, generate_perlin_noise_candle, generate_random_walk_candle, generate_fbm_candles, generate_random_candle
>>>>>>> origin/main

logger = logging.getLogger(__name__)

class SimulationManager:
    def __init__(self, scenario_id, run_duration=100000):
        self.scenario = Scenario.objects.get(id=scenario_id)
        self.channel_layer = get_channel_layer()
        self.running = False
        self.run_duration = run_duration
<<<<<<< HEAD
        self.settings = self.scenario.simulation_settings
        self.time_step = self.settings.timer_step * TIME_UNITS[self.settings.timer_step_unit]
        self.interval = self.settings.interval * TIME_UNITS[self.settings.interval_unit]
        self.close_stock_market_at_night = self.settings.close_stock_market_at_night
        self.fluctuation_rate = self.settings.fluctuation_rate
        self.noise_function = self.settings.noise_function.lower()
        self.time_index = 0
=======

        settings = self.scenario.simulation_settings
        self.time_step = settings.timer_step * TIME_UNITS[settings.timer_step_unit]
        self.interval = settings.interval * TIME_UNITS[settings.interval_unit]
        self.close_stock_market_at_night = settings.close_stock_market_at_night
        self.fluctuation_rate = settings.fluctuation_rate
        self.noise_function = settings.noise_function.lower()
>>>>>>> origin/main

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
<<<<<<< HEAD
=======
        if self.simulation_data:
            self.simulation_data.stop_simulation()
>>>>>>> origin/main
        self.running = False
        logger.info('Simulation stopped')

    def update_prices(self, current_time):
<<<<<<< HEAD
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
=======
        price_changes = []
        for company in self.scenario.companies.all():
            if stock := company.stock_set.first():
                change = self.apply_changes(stock, current_time)
                price_changes.append(change)
                StockPriceHistory.objects.create(stock=stock, price=stock.price, timestamp=current_time)

        self.simulation_data.price_changes = price_changes
        self.simulation_data.end_time = current_time
        self.simulation_data.save()

    def apply_changes(self, asset, current_time):
>>>>>>> origin/main
        if self.noise_function == 'brownian':
            change = generate_brownian_motion_candle(stock.price, self.fluctuation_rate)
        elif self.noise_function == 'perlin':
<<<<<<< HEAD
            change = generate_perlin_noise_candle(stock.price, self.time_index, self.fluctuation_rate)
        elif self.noise_function == 'random_walk':
            change = generate_random_walk_candle(stock.price, self.fluctuation_rate)
        elif self.noise_function == 'fbm':
            change = generate_fbm_candles(stock.price, self.time_index, self.fluctuation_rate)
        elif self.noise_function == 'random':
            change = generate_random_candle(stock.price, self.fluctuation_rate)
=======
            change = generate_perlin_noise_candle(asset.price, len(asset.price_history.all()), self.fluctuation_rate)
        elif self.noise_function == 'random_walk':
            change = generate_random_walk_candle(asset.price, self.fluctuation_rate)
        elif self.noise_function == 'fbm':
            change = generate_fbm_candles(asset.price, self.fluctuation_rate)
>>>>>>> origin/main
        else:
            raise ValueError(f"Unsupported noise function: {self.noise_function}")

<<<<<<< HEAD
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
=======
        asset.open_price = change['Open']
        asset.high_price = change['High']
        asset.low_price = change['Low']
        asset.close_price = change['Close']
        asset.price = change['Close']
        asset.save()

        return {
            'ticker': asset.ticker,
            'open': asset.open_price,
            'high': asset.high_price,
            'low': asset.low_price,
            'close': asset.close_price,
>>>>>>> origin/main
            'time': current_time.isoformat()
        }

    def broadcast_updates(self):
<<<<<<< HEAD
        stocks = Scenario.objects.get(id=self.scenario.id).stocks.all()
        for stock in stocks:
            send_ohlc_update(self.channel_layer, stock, 'stock')

=======
        for company in self.scenario.companies.all():
            if stock := company.stock_set.first():
                send_ohlc_update(self.channel_layer, stock, 'stock')
>>>>>>> origin/main

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
<<<<<<< HEAD
            del cls._instances[scenario_id]
=======
            del cls._instances[scenario_id]
>>>>>>> origin/main
