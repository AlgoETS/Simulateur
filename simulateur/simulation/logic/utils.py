from asgiref.sync import async_to_sync
import logging
from datetime import datetime, time, timedelta
import pytz

import numpy as np
from django.utils import timezone
from simulation.models.stock import StockPriceHistory

logger = logging.getLogger(__name__)

TIME_UNITS = {
    'millisecond': 0.001,
    'centisecond': 0.01,
    'decisecond': 0.1,
    'second': 1,
    'minute': 60,
    'hour': 3600,
    'day': 86400,
    'month': 2592000,
    'year': 31536000
}


def is_market_open(current_time, timezone_str='America/New_York'):
    """
    Check if the stock market is open based on the current time in the specified time zone.

    :param current_time: A timezone-aware datetime object. If not timezone-aware, it will be converted.
    :param timezone_str: The time zone to use (default is 'America/New_York').
    :return: True if the market is open, False otherwise.
    """
    # Define market open and close times
    market_open = time(9, 0)  # 09:00 AM
    market_close = time(16, 0)  # 04:00 PM

    # Get the time zone
    tz = pytz.timezone(timezone_str)

    # Ensure current_time is timezone-aware
    if current_time.tzinfo is None:
        current_time = tz.localize(current_time)

    # Convert current_time to the specified time zone
    current_time = current_time.astimezone(tz)

    # Check if the market is open
    if current_time.weekday() >= 5:  # Saturday or Sunday
        return False

    if current_time.time() < market_open or current_time.time() >= market_close:
        return False

    return True


def send_ohlc_update(channel_layer, update, simulation_id):
    """Send an OHLC update to the specified WebSocket channel."""
    data = {
        'id': update['id'],
        'simulation_manager': update['simulation_manager'],
        'ticker': update['ticker'],
        'name': update['name'],
        'type': update['type'],
        'open': update['open'],
        'high': update['high'],
        'low': update['low'],
        'close': update['close'],
        'current': update['current'],
        'timestamp': str(timezone.now().isoformat())
    }
    logger.debug(f"Sending OHLC update: {data}")

    async_to_sync(channel_layer.group_send)(
        f"simulation_{simulation_id}",
        {
            "type": "stock_update",  # Updated to match the consumer method
            "message": data
        }
    )
    logger.debug(f"OHLC update sent to group 'simulation_{simulation_id}'")


def get_mid_prices_in_range(stock_id: int, time_delta: timedelta):
    """
    Get the mid prices of a stock in the given time range.

    :param stock_id: The ID of the stock.
    :param time_delta: The time range to look back from now.
    :return: A list of mid prices.
    """
    end_time = timezone.now()
    start_time = end_time - time_delta
    mid_prices = StockPriceHistory.objects.filter(
        stock_id=stock_id,
        timestamp__range=(start_time, end_time)
    ).values_list('high_price', 'low_price')

    return [(high + low) / 2 for high, low in mid_prices]


def get_stock_volatility(prices):
    """
    Calculate the volatility of a stock based on its price history.

    :param prices: A list of stock prices.
    :return: The volatility of the stock.
    """
    if len(prices) < 2:
        return 0

    log_returns = np.log(np.array(prices[1:]) / np.array(prices[:-1]))
    return np.std(log_returns)
