from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.utils import timezone
import logging
import noise
import numpy as np
from simulation.models.stock import StockPriceHistory
from datetime import datetime, timedelta


logger = logging.getLogger(__name__)

TIME_UNITS = {
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

def send_ohlc_update(channel_layer, stock, stock_type):
    """Send an OHLC update to the specified WebSocket channel."""
    data = {
        'id': stock.id,
        'ticker': stock.ticker,
        'name': stock.company.name,
        'type': stock_type,
        'open': stock.open_price,
        'high': stock.high_price,
        'low': stock.low_price,
        'close': stock.close_price,
        'current': stock.price,
        'timestamp': timezone.now().isoformat()
    }
    async_to_sync(channel_layer.group_send)(
        f'simulation_{stock_type}',
        {
            'type': 'simulation_update',
            'message': data
        }
    )

# def generate_brownian_motion_candle(price, fluctuation_rate):
#     open_price = price
#     change = np.random.normal(loc=0, scale=fluctuation_rate)
#     close_price = open_price + change
#     high_price = max(open_price, close_price) + np.random.uniform(0, fluctuation_rate * 2)
#     low_price = min(open_price, close_price) - np.random.uniform(0, fluctuation_rate * 2)
#     return {'Open': open_price, 'High': high_price, 'Low': low_price, 'Close': close_price}

# def generate_perlin_noise_candle(price, i, fluctuation_rate):
#     """Generate a candlestick using Perlin noise."""
#     open_price = price
#     change = noise.pnoise1(i * 0.1) * fluctuation_rate * 10
#     close_price = open_price + change
#     high_price = max(open_price, close_price) + np.random.uniform(0, fluctuation_rate * 2)
#     low_price = min(open_price, close_price) - np.random.uniform(0, fluctuation_rate * 2)
#     return {'Open': open_price, 'High': high_price, 'Low': low_price, 'Close': close_price}

# def generate_random_walk_candle(price, fluctuation_rate):
#     """Generate a candlestick using a random walk."""
#     open_price = price
#     change = np.random.choice([-1, 1]) * np.random.uniform(0, fluctuation_rate * 5)
#     close_price = open_price + change
#     high_price = max(open_price, close_price)
#     low_price = min(open_price, close_price)
#     return {'Open': open_price, 'High': high_price, 'Low': low_price, 'Close': close_price}

# def generate_random_candle(price, fluctuation_rate):
#     """Generate a candlestick using random values."""
#     open_price = price
#     high_price = open_price + np.random.uniform(0, fluctuation_rate * 5)
#     low_price = open_price - np.random.uniform(0, fluctuation_rate * 5)
#     close_price = low_price + np.random.uniform(0, (high_price - low_price))
#     return {'Open': open_price, 'High': high_price, 'Low': low_price, 'Close': close_price}

# def generate_fbm_candles(price, fluctuation_rate):
#     """Generate a candlestick using fractional Brownian motion."""
#     open_price = price
#     high_price = open_price + np.random.uniform(0, fluctuation_rate * 5)
#     low_price = open_price - np.random.uniform(0, fluctuation_rate * 5)
#     close_price = low_price + np.random.uniform(0, (high_price - low_price))
#     return {'Open': open_price, 'High': high_price, 'Low': low_price, 'Close': close_price}


def get_mid_prices_in_range(stock_id: int, time_delta: timedelta):
    end_time = timezone.now()
    start_time = end_time - time_delta
    mid_prices = StockPriceHistory.objects.filter(
        stock_id=stock_id,
        timestamp__range=(start_time, end_time)
    ).values_list('high_price', 'low_price')

    return [(high + low) / 2 for high, low in mid_prices]


def get_stock_volatility(self,ticker,prices):
        if ticker not in self.price_history or len(self.price_history[ticker]) < 2:
            return 0
        # prices = self.price_history[ticker]
        log_returns = np.log(np.array(prices[1:]) / np.array(prices[:-1]))
        return np.std(log_returns)


