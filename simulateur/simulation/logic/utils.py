from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.utils import timezone
from simulation.models import Stock

TIME_UNITS = {
    'second': 1,
    'minute': 60,
    'hour': 3600,
    'day': 86400,
    'month': 2592000,
    'year': 31536000
}

def is_market_open(current_time):
    open_time = current_time.replace(hour=9, minute=0, second=0, microsecond=0)
    close_time = current_time.replace(hour=16, minute=0, second=0, microsecond=0)
    return open_time <= current_time <= close_time

def send_ohlc_update(channel_layer, asset, room_name):
    group_name = f'simulation_{room_name}'
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'simulation_update',
            'data': {
                'id': asset.id,
                'name': asset.company.name if isinstance(asset, Stock) else asset.name,
                'type': 'Stock' if isinstance(asset, Stock) else 'Cryptocurrency',
                'open': asset.open_price,
                'high': asset.high_price,
                'low': asset.low_price,
                'close': asset.close_price,
                'current': asset.price,
                'timestamp': timezone.now().isoformat()
            }
        }
    )

