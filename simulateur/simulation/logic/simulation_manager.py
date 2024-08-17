import logging
import time
from channels.layers import get_channel_layer
from django.conf import settings
from django.core.cache import cache
from django.utils import timezone
from simulation.logic.broker import broker
from simulation.logic.noise_patterns.brownian_motion import BrownianMotion
from simulation.logic.noise_patterns.fbm import Fbm
from simulation.logic.noise_patterns.perlin import Perlin
from simulation.logic.noise_patterns.random_candle import RandomCandle
from simulation.logic.noise_patterns.random_walk import RandomWalk
from simulation.logic.utils import is_market_open, send_ohlc_update, TIME_UNITS
from simulation.models import SimulationManager as SM, StockPriceHistory

logger = logging.getLogger(__name__)

CACHE_TTL = getattr(settings, "CACHE_TTL", 15)  # 15 minutes default


class SimulationManager:
    def __init__(self, simulation_manager):
        self.simulation_manager = simulation_manager
        self.scenario = simulation_manager.scenario
        self.channel_layer = get_channel_layer()
        self.running = False
        self.run_duration = 100000
        self.time_step = (
            simulation_manager.simulation_settings.timer_step
            * TIME_UNITS[simulation_manager.simulation_settings.timer_step_unit]
        )
        self.interval = (
            simulation_manager.simulation_settings.interval
            * TIME_UNITS[simulation_manager.simulation_settings.interval_unit]
        )
        self.close_stock_market_at_night = (
            simulation_manager.simulation_settings.close_stock_market_at_night
        )
        self.fluctuation_rate = simulation_manager.simulation_settings.fluctuation_rate
        self.noise_function = simulation_manager.simulation_settings.noise_function.lower()
        self.time_index = 0
        self.noise_strategy = self.get_noise_strategy(self.noise_function)
        self.trading_strategy = simulation_manager.simulation_settings.stock_trading_logic
        self.broker = broker

        logger.info(
            f"Starting simulation for scenario {self.scenario} with time step {self.time_step} seconds"
        )

    def get_noise_strategy(self, noise_function):
        if noise_function == "brownian":
            return BrownianMotion()
        elif noise_function == "perlin":
            return Perlin()
        elif noise_function == "random_walk":
            return RandomWalk()
        elif noise_function == "fbm":
            return Fbm()
        elif noise_function == "random":
            return RandomCandle()
        else:
            raise ValueError(f"Unsupported noise function: {noise_function}")

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

                if self.close_stock_market_at_night and not is_market_open(current_time):
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
        cache_key = f"stocks_for_scenario_{self.simulation_manager.id}"
        stocks = cache.get(cache_key)

        if not stocks:
            stocks = list(self.simulation_manager.stocks.all())
            cache.set(cache_key, stocks, timeout=CACHE_TTL)

        return stocks

    def apply_changes(self, stock, current_time):
        last_price_entry = stock.price_history.order_by('-timestamp').first()
        last_price = last_price_entry.close_price if last_price_entry else 0.0

        change = self.noise_strategy.generate_noise(
            last_price, self.fluctuation_rate, self.time_index
        )
        self.time_index += 1

        logger.info(f"Updated stock {stock.ticker} with new price: {change['Close']} at {current_time}")

        return {
            "ticker": stock.ticker,
            "open": change["Open"],
            "high": change["High"],
            "low": change["Low"],
            "close": change["Close"],
            "time": current_time.isoformat(),
        }

    def broadcast_update(self, stock, current_time):
        # Retrieve the latest price history entry for the stock
        last_price_entry = stock.price_history.order_by('-timestamp').first()

        if not last_price_entry:
            logger.warning(f"No price history found for stock {stock.ticker} at {current_time}")
            return

        update = {
            "id": stock.id,
            "ticker": stock.ticker,
            "name": stock.company.name,
            "type": "stock",
            "open": last_price_entry.open_price,
            "high": last_price_entry.high_price,
            "low": last_price_entry.low_price,
            "close": last_price_entry.close_price,
            "current": last_price_entry.close_price,  # Use the close price as the current price
            "timestamp": current_time.isoformat(),
        }

        logger.info(f"Broadcasting update: {update}")

        send_ohlc_update(self.channel_layer, update, "stock")


class SimulationManagerSingleton:
    _instances = {}

    @classmethod
    def get_instance(cls, simulation_manager_id):
        if simulation_manager_id not in cls._instances:
            simulation_manager = SM.objects.get(id=simulation_manager_id)
            cls._instances[simulation_manager_id] = SimulationManager(simulation_manager)
        return cls._instances[simulation_manager_id]

    @classmethod
    def remove_instance(cls, simulation_manager_id):
        if simulation_manager_id in cls._instances:
            del cls._instances[simulation_manager_id]
