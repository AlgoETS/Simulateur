import logging
import asyncio
from django.utils import timezone
from channels.layers import get_channel_layer
from asgiref.sync import sync_to_async
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

logger = logging.getLogger(__name__)

class SimulationManager:
    def __init__(self, scenario_id, run_duration=100000):
        self.scenario = None
        self.channel_layer = get_channel_layer()
        self.running = False
        self.run_duration = run_duration
        self.time_step = None
        self.interval = None
        self.close_stock_market_at_night = None
        self.fluctuation_rate = None
        self.noise_function = None
        self.time_index = 0
        asyncio.run(self.initialize_scenario(scenario_id))
        logger.info(f'Starting simulation for scenario {self.scenario} with time step {self.time_step} seconds')

    async def initialize_scenario(self, scenario_id):
        self.scenario = await sync_to_async(Scenario.objects.get)(id=scenario_id)
        self.settings = self.scenario.simulation_settings
        self.time_step = self.settings.timer_step * TIME_UNITS[self.settings.timer_step_unit]
        self.interval = self.settings.interval * TIME_UNITS[self.settings.interval_unit]
        self.close_stock_market_at_night = self.settings.close_stock_market_at_night
        self.fluctuation_rate = self.settings.fluctuation_rate
        self.noise_function = self.settings.noise_function.lower()

    async def start_simulation(self):
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
                    await self.update_prices(current_time)
                    logger.info(f'Simulation time: {current_time}, elapsed time: {elapsed_time}')
                logger.info(f'Sleeping for {self.time_step} seconds')
                await asyncio.sleep(self.time_step)
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

    async def update_prices(self, current_time):
        stocks = await sync_to_async(list)(Scenario.objects.get(id=self.scenario.id).stocks.all())
        for stock in stocks:
            change = self.apply_changes(stock, current_time)
            await sync_to_async(StockPriceHistory.objects.create)(
                stock=stock,
                open_price=change['open'],
                high_price=change['high'],
                low_price=change['low'],
                close_price=change['close'],
                timestamp=current_time
            )
            await self.broadcast_update(stock, current_time)

    def apply_changes(self, stock, current_time):
        if self.noise_function == 'brownian':
            change = generate_brownian_motion_candle(stock.price, self.fluctuation_rate)
        elif self.noise_function == 'perlin':
            change = generate_perlin_noise_candle(stock.price, self.time_index, self.fluctuation_rate)
        elif self.noise_function == 'random_walk':
            change = generate_random_walk_candle(stock.price, self.fluctuation_rate)
        elif self.noise_function == 'fbm':
            change = generate_fbm_candles(stock.price, self.time_index, self.fluctuation_rate)
        elif self.noise_function == 'random':
            change = generate_random_candle(stock.price, self.fluctuation_rate)
        else:
            raise ValueError(f"Unsupported noise function: {self.noise_function}")

        self.time_index += 1
        stock.open_price = change['Open']
        stock.high_price = change['High']
        stock.low_price = change['Low']
        stock.close_price = change['Close']
        stock.price = change['Close']
        sync_to_async(stock.save)()  # Save stock price asynchronously

        return {
            'ticker': stock.ticker,
            'open': stock.open_price,
            'high': stock.high_price,
            'low': stock.low_price,
            'close': stock.close_price,
            'time': current_time.isoformat()
        }

    async def broadcast_update(self, stock, current_time):
        update = {
            'id': stock.id,
            'ticker': stock.ticker,
            'name': stock.company.name,
            'type': 'stock',
            'open': stock.open_price,
            'high': stock.high_price,
            'low': stock.low_price,
            'close': stock.close_price,
            'current': stock.price,
            'timestamp': current_time.isoformat()
        }

        await self.send_ohlc_update([update])

    async def send_ohlc_update(self, updates):
        for update in updates:
            await send_ohlc_update(self.channel_layer, update, 'stock')


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
