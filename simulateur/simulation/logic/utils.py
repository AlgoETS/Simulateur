from asgiref.sync import async_to_sync  # Add this import
import logging
from datetime import timedelta

import numpy as np
from asgiref.sync import async_to_sync  # Add this import
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


def is_market_open(current_time):
    """Check if the stock market is open based on the current time."""
    if current_time.hour < 9 or current_time.hour >= 16:
        return False
    return current_time.weekday() < 5


def send_ohlc_update(channel_layer, update, stock_type):
    """Send an OHLC update to the specified WebSocket channel."""
    data = {
        'id': update['id'],
        'ticker': update['ticker'],
        'name': update['name'],
        'type': stock_type,
        'open': update['open'],
        'high': update['high'],
        'low': update['low'],
        'close': update['close'],
        'current': update['current'],
        'timestamp': timezone.now().isoformat()
    }
    async_to_sync(channel_layer.group_send)(
        f'simulation_{stock_type}',
        {
            'type': 'simulation_update',
            'message': data
        }
    )


def get_mid_prices_in_range(stock_id: int, time_delta: timedelta):
    end_time = timezone.now()
    start_time = end_time - time_delta
    mid_prices = StockPriceHistory.objects.filter(
        stock_id=stock_id,
        timestamp__range=(start_time, end_time)
    ).values_list('high_price', 'low_price')

    return [(high + low) / 2 for high, low in mid_prices]


def get_stock_volatility(self, ticker, prices):
    if ticker not in self.price_history or len(self.price_history[ticker]) < 2:
        return 0
    # prices = self.price_history[ticker]
    log_returns = np.log(np.array(prices[1:]) / np.array(prices[:-1]))
    return np.std(log_returns)
