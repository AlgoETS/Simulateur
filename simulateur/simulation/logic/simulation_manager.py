import logging
import time
import threading
from channels.layers import get_channel_layer
from django.conf import settings
from django.utils import timezone
from django.core.cache import cache
from simulation.logic.broker import broker
from simulation.logic.noise_patterns.brownian_motion import BrownianMotion
from simulation.logic.noise_patterns.fbm import Fbm
from simulation.logic.noise_patterns.perlin import Perlin
from simulation.logic.noise_patterns.random_candle import RandomCandle
from simulation.logic.noise_patterns.random_walk import RandomWalk
from simulation.logic.noise_patterns.monte_carlo import MonteCarlo
from simulation.logic.utils import is_market_open, send_ohlc_update, TIME_UNITS
from simulation.models import SimulationManager as SM, StockPriceHistory

logger = logging.getLogger(__name__)

CACHE_TTL = getattr(settings, "CACHE_TTL", 0)


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
            f"Initializing simulation for scenario {self.scenario} with time step {self.time_step} seconds"
        )

    def apply_new_settings(self, new_settings):
        """
        Apply the new settings to the running simulation.
        """
        self.simulation_manager.simulation_settings = new_settings
        self.time_step = (
            new_settings.timer_step * TIME_UNITS[new_settings.timer_step_unit]
        )
        self.interval = (
            new_settings.interval * TIME_UNITS[new_settings.interval_unit]
        )
        self.close_stock_market_at_night = new_settings.close_stock_market_at_night
        self.fluctuation_rate = new_settings.fluctuation_rate
        self.noise_function = new_settings.noise_function.lower()
        self.noise_strategy = self.get_noise_strategy(self.noise_function)
        self.trading_strategy = new_settings.stock_trading_logic

        logger.info(
            f"Updated simulation settings for scenario {self.scenario} with time step {self.time_step} seconds"
        )

    def get_noise_strategy(self, noise_function):
        strategies = {
            "brownian": BrownianMotion,
            "perlin": Perlin,
            "random_walk": RandomWalk,
            "fbm": Fbm,
            "random": RandomCandle,
            "monte_carlo": MonteCarlo
        }
        strategy_class = strategies.get(noise_function)
        if not strategy_class:
            raise ValueError(f"Unsupported noise function: {noise_function}")
        return strategy_class()

    def monitor_state_and_start(self):
        """ Continuously monitors the state and starts or restarts the simulation if it becomes ONGOING. """
        while True:
            self.simulation_manager.refresh_from_db()  # Refresh state from the database

            # If the state is ONGOING, start or restart the simulation
            if self.simulation_manager.state == SM.ScenarioState.ONGOING:
                if not self.running:
                    logger.info(f"State changed to ONGOING. Starting simulation for scenario {self.scenario}.")
                    self.start_simulation()

            # If the state is FINISHED, exit the monitoring loop
            elif self.simulation_manager.state == SM.ScenarioState.FINISHED:
                logger.info("Simulation is in FINISHED state. Monitoring loop will exit.")
                break

            # Wait before checking the state again
            time.sleep(5)

    def start_simulation(self):
        self.running = True
        start_time = timezone.now()
        try:
            while self.running:
                self.simulation_manager.refresh_from_db()
                if self.simulation_manager.state == SM.ScenarioState.STOPPED:
                    logger.info("State changed to STOPPED. Halting simulation.")
                    break
                elif self.simulation_manager.state == SM.ScenarioState.FINISHED:
                    logger.info("State changed to FINISHED. Ending simulation.")
                    break

                current_time = timezone.now()
                elapsed_time = (current_time - start_time).total_seconds()

                if elapsed_time >= self.run_duration:
                    logger.info("Run duration reached, stopping simulation")
                    self.simulation_manager.state = SM.ScenarioState.FINISHED
                    self.simulation_manager.save()
                    break

                if self.close_stock_market_at_night and not is_market_open(current_time):
                    logger.info("Stock market is closed")
                else:
                    if self.trading_strategy == "static":
                        self.update_prices(current_time)
                    else:
                        self.broker.process_queues()
                    logger.debug(
                        f"Simulation time ({self.simulation_manager.id}): Elapsed time: {elapsed_time}"
                    )
                logger.debug(f"Sleeping for {self.time_step} seconds")
                time.sleep(self.time_step)
        except KeyboardInterrupt:
            logger.info("Simulation stopped by user")
            self.simulation_manager.state = SM.ScenarioState.STOPPED
            self.simulation_manager.save()
        except Exception as e:
            logger.error(f"Error occurred during simulation: {e}", exc_info=True)
        finally:
            self.stop_simulation()

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

        return {
            "ticker": stock.ticker,
            "open": change["Open"],
            "high": change["High"],
            "low": change["Low"],
            "close": change["Close"],
            "time": current_time.isoformat(),
        }

    def broadcast_update(self, stock, current_time):
        last_price_entry = stock.price_history.order_by('-timestamp').first()

        if not last_price_entry:
            logger.warning(f"No price history found for stock {stock.ticker} at {current_time}")
            return

        update = {
            "simulation_manager": self.simulation_manager.id,
            "id": stock.id,
            "ticker": stock.ticker,
            "name": stock.company.name,
            "type": "stock",
            "open": last_price_entry.open_price,
            "high": last_price_entry.high_price,
            "low": last_price_entry.low_price,
            "close": last_price_entry.close_price,
            "current": last_price_entry.close_price,
            "timestamp": current_time.isoformat(),
        }

        logger.debug(f"Preparing to broadcast update: {update}")

        try:
            send_ohlc_update(self.channel_layer, update, f'{self.simulation_manager.id}')
            logger.debug(f"Broadcast update sent successfully.")
        except Exception as e:
            logger.error(f"Error sending broadcast update: {e}")


class SimulationManagerSingleton:
    _instances = {}
    _threads = {}

    @classmethod
    def get_instance(cls, simulation_manager_id):
        if simulation_manager_id not in cls._instances:
            simulation_manager = SM.objects.get(id=simulation_manager_id)
            manager_instance = SimulationManager(simulation_manager)
            cls._instances[simulation_manager_id] = manager_instance

            # Start a monitoring thread for this simulation
            monitoring_thread = threading.Thread(
                target=manager_instance.monitor_state_and_start,
                daemon=True
            )
            cls._threads[simulation_manager_id] = monitoring_thread
            monitoring_thread.start()

        return cls._instances[simulation_manager_id]

    @classmethod
    def remove_instance(cls, simulation_manager_id):
        if simulation_manager_id in cls._instances:
            del cls._instances[simulation_manager_id]
        if simulation_manager_id in cls._threads:
            cls._threads[simulation_manager_id].join(timeout=1)  # Ensure the thread is stopped
            del cls._threads[simulation_manager_id]