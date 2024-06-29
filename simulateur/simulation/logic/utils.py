from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.utils import timezone
import logging
import noise
import numpy as np

<<<<<<< HEAD
from simulation.models.stock import StockPriceHistory

=======
>>>>>>> origin/main
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
<<<<<<< HEAD
    """Check if the stock market is open based on the current time."""
    if current_time.hour < 9 or current_time.hour >= 16:
        return False
    return current_time.weekday() < 5

def send_ohlc_update(channel_layer, stock, stock_type):
    """Send an OHLC update to the specified WebSocket channel."""
    data = {
        'id': stock.id,
        'ticker': stock.ticker,
=======
    # check timezone
    if current_time.hour < 9 or current_time.hour >= 16:
        return False
    # check if it's a weekend
    if current_time.weekday() >= 5:
        return False
    open_time = current_time.replace(hour=9, minute=0, second=0, microsecond=0)
    close_time = current_time.replace(hour=16, minute=0, second=0, microsecond=0)
    return open_time <= current_time <= close_time

def send_ohlc_update(channel_layer, stock, stock_type):
    data = {
        'id': stock.id,
>>>>>>> origin/main
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

def generate_brownian_motion_candle(price, fluctuation_rate):
<<<<<<< HEAD
    """Generate a candlestick using Brownian motion."""
=======
>>>>>>> origin/main
    open_price = price
    change = np.random.normal(loc=0, scale=fluctuation_rate)
    close_price = open_price + change
    high_price = max(open_price, close_price) + np.random.uniform(0, fluctuation_rate * 2)
    low_price = min(open_price, close_price) - np.random.uniform(0, fluctuation_rate * 2)
    return {'Open': open_price, 'High': high_price, 'Low': low_price, 'Close': close_price}

<<<<<<< HEAD

def generate_perlin_noise_candle(price, i, fluctuation_rate):
    """Generate a candlestick using Perlin noise."""
=======
def generate_perlin_noise_candle(price, i, fluctuation_rate):
>>>>>>> origin/main
    open_price = price
    change = noise.pnoise1(i * 0.1) * fluctuation_rate * 10
    close_price = open_price + change
    high_price = max(open_price, close_price) + np.random.uniform(0, fluctuation_rate * 2)
    low_price = min(open_price, close_price) - np.random.uniform(0, fluctuation_rate * 2)
    return {'Open': open_price, 'High': high_price, 'Low': low_price, 'Close': close_price}

<<<<<<< HEAD

def generate_random_walk_candle(price, fluctuation_rate):
    """Generate a candlestick using a random walk."""
=======
def generate_random_walk_candle(price, fluctuation_rate):
>>>>>>> origin/main
    open_price = price
    change = np.random.choice([-1, 1]) * np.random.uniform(0, fluctuation_rate * 5)
    close_price = open_price + change
    high_price = max(open_price, close_price)
    low_price = min(open_price, close_price)
    return {'Open': open_price, 'High': high_price, 'Low': low_price, 'Close': close_price}

<<<<<<< HEAD

def generate_random_candle(price, fluctuation_rate):
    """Generate a candlestick using random values."""
=======
def generate_random_candle(price, fluctuation_rate):
>>>>>>> origin/main
    open_price = price
    high_price = open_price + np.random.uniform(0, fluctuation_rate * 5)
    low_price = open_price - np.random.uniform(0, fluctuation_rate * 5)
    close_price = low_price + np.random.uniform(0, (high_price - low_price))
    return {'Open': open_price, 'High': high_price, 'Low': low_price, 'Close': close_price}

<<<<<<< HEAD

def generate_fbm_candles(price, fluctuation_rate):
    """Generate a candlestick using fractional Brownian motion."""
=======
def generate_fbm_candles(price, fluctuation_rate):
>>>>>>> origin/main
    open_price = price
    high_price = open_price + np.random.uniform(0, fluctuation_rate * 5)
    low_price = open_price - np.random.uniform(0, fluctuation_rate * 5)
    close_price = low_price + np.random.uniform(0, (high_price - low_price))
    return {'Open': open_price, 'High': high_price, 'Low': low_price, 'Close': close_price}
