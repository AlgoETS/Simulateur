import logging
import time
from django.utils import timezone
from django.core.cache import cache
from django.conf import settings
from channels.layers import get_channel_layer
from simulation.logic.noise_patterns.noise_strategy import NoiseStrategy
from simulation.logic.noise_patterns.fbm import Fbm
from simulation.logic.noise_patterns.brownian_motion import BrownianMotion
from simulation.logic.noise_patterns.perlin import Perlin
from simulation.logic.noise_patterns.random_candle import RandomCandle
from simulation.logic.noise_patterns.random_walk import RandomWalk
from simulation.models import Scenario, Stock, StockPriceHistory
from simulation.logic.broker import broker
from simulation.logic.utils import is_market_open, send_ohlc_update, TIME_UNITS


logger = logging.getLogger(__name__)

CACHE_TTL = getattr(settings, "CACHE_TTL", 15)  # 15 minutes default


class SimulationManager:
    def __init__(self, scenario):
        self.scenario = scenario
        self.channel_layer = get_channel_layer()
        self.running = False
        self.run_duration = 100000
        self.time_step = (
            scenario.simulation_settings.timer_step
            * TIME_UNITS[scenario.simulation_settings.timer_step_unit]
        )
        self.interval = (
            scenario.simulation_settings.interval
            * TIME_UNITS[scenario.simulation_settings.interval_unit]
        )
        self.close_stock_market_at_night = (
            scenario.simulation_settings.close_stock_market_at_night
        )
        self.fluctuation_rate = scenario.simulation_settings.fluctuation_rate
        self.noise_function = scenario.simulation_settings.noise_function.lower()
        self.time_index = 0
        self.noise_strategy = BrownianMotion()
        self.trading_strategy = self.scenario.simulation_settings.stock_trading_logic
        self.broker = broker

        logger.info(
            f"Starting simulation for scenario {self.scenario} with time step {self.time_step} seconds"
        )

    def start_simulation(self):
        self.running = True
        start_time = timezone.now()
        try:
            while self.running:
                current_time = timezone.now()
                elapsed_time = (current_time - start_time).total_seconds()

                if elapsed_time >= self.run_duration:
                    logger.info("Run duration reached, stopping simulation")
                    break

                if self.close_stock_market_at_night and not is_market_open(
                    current_time
                ):
                    logger.info("Stock market is closed")
                else:
                    if self.trading_strategy == "static":
                        self.update_prices(current_time)
                    else:
                        self.broker.process_queues()
                    logger.info(
                        f"Simulation time: {current_time}, elapsed time: {elapsed_time}"
                    )
                logger.info(f"Sleeping for {self.time_step} seconds")
                time.sleep(self.time_step)
        except KeyboardInterrupt:
            logger.info("Simulation stopped by user")
        except Exception as e:
            logger.error(f"Error occurred during simulation: {e}", exc_info=True)
        finally:
            self.stop_simulation()

    def pause_simulation(self):
        self.running = False
        logger.info("Simulation paused")

    def stop_simulation(self):
        self.running = False
        logger.info("Simulation stopped")

    def update_prices(self, current_time):
        stocks = self.get_stocks()
        for stock in stocks:
            change = self.apply_changes(stock, current_time)
            StockPriceHistory.objects.create(
                stock=stock,
                open_price=change["open"],
                high_price=change["high"],
                low_price=change["low"],
                close_price=change["close"],
                timestamp=current_time,
            )
            self.broadcast_update(stock, current_time)

    def get_stocks(self):
        cache_key = f"stocks_for_scenario_{self.scenario.id}"
        stocks = cache.get(cache_key)

        if not stocks:
            stocks = list(self.scenario.stocks.all())
            cache.set(cache_key, stocks, timeout=CACHE_TTL)

        return stocks

    def apply_changes(self, stock, current_time):
        if self.noise_function == "brownian":
            self.noise_strategy = BrownianMotion()
        elif self.noise_function == "perlin":
            self.noise_strategy = Perlin()
        elif self.noise_function == "random_walk":
            self.noise_strategy = RandomWalk()
        elif self.noise_function == "fbm":
            self.noise_strategy = Fbm()
        elif self.noise_function == "random":
            self.noise_strategy = RandomCandle()
        else:
            raise ValueError(f"Unsupported noise function: {self.noise_function}")

        change = self.noise_strategy.generate_noise(
            stock.price, self.fluctuation_rate, self.time_index
        )
        self.time_index += 1
        stock.open_price = change["Open"]
        stock.high_price = change["High"]
        stock.low_price = change["Low"]
        stock.close_price = change["Close"]
        stock.price = change["Close"]
        stock.save()

        # Invalidate the cache for the stocks query when changes are applied
        cache_key = f"stocks_for_scenario_{self.scenario.id}"
        cache.delete(cache_key)

        return {
            "ticker": stock.ticker,
            "open": stock.open_price,
            "high": stock.high_price,
            "low": stock.low_price,
            "close": stock.close_price,
            "time": current_time.isoformat(),
        }

    def broadcast_update(self, stock, current_time):
        update = {
            "id": stock.id,
            "ticker": stock.ticker,
            "name": stock.company.name,
            "type": "stock",
            "open": stock.open_price,
            "high": stock.high_price,
            "low": stock.low_price,
            "close": stock.close_price,
            "current": stock.price,
            "timestamp": current_time.isoformat(),
        }

        logger.info(f"Broadcasting update: {update}")

        send_ohlc_update(self.channel_layer, update, "stock")


class SimulationManagerSingleton:
    _instances = {}

    @classmethod
    def get_instance(cls, scenario_id):
        if scenario_id not in cls._instances:
            scenario = Scenario.objects.get(id=scenario_id)
            cls._instances[scenario_id] = SimulationManager(scenario)
        return cls._instances[scenario_id]

    @classmethod
    def remove_instance(cls, scenario_id):
        if scenario_id in cls._instances:
            del cls._instances[scenario_id]
