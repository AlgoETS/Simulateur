import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
import numpy as np
from django.test import TestCase
from django.utils import timezone
from channels.layers import get_channel_layer
from simulation.models import StockPriceHistory
from simulation.logic.utils import (
    is_market_open, send_ohlc_update, get_mid_prices_in_range, get_stock_volatility
)

class UtilityFunctionsTests(TestCase):

    def setUp(self):
        self.channel_layer = get_channel_layer()

    def test_is_market_open_during_open_hours(self):
        current_time = timezone.now().replace(hour=10, minute=0)
        self.assertTrue(is_market_open(current_time))

    def test_is_market_open_during_closed_hours(self):
        current_time = timezone.now().replace(hour=17, minute=0)
        self.assertFalse(is_market_open(current_time))

    def test_is_market_open_on_weekend(self):
        # Assuming Saturday (weekday=5)
        current_time = timezone.now().replace(hour=10, minute=0, weekday=5)
        self.assertFalse(is_market_open(current_time))

    @patch('simulation.logic.utils.async_to_sync')
    def test_send_ohlc_update(self, mock_async_to_sync):
        update = {
            'id': 1,
            'ticker': 'TEST',
            'name': 'Test Company',
            'open': 100,
            'high': 110,
            'low': 90,
            'close': 105,
            'current': 105,
            'timestamp': timezone.now().isoformat(),
        }
        send_ohlc_update(self.channel_layer, update, 'stock')

        # Verify that the message was sent to the channel layer
        mock_async_to_sync.assert_called_once()
        args = mock_async_to_sync.call_args[0][0]
        self.assertEqual(args['type'], 'simulation_update')
        self.assertEqual(args['message']['ticker'], 'TEST')

    def test_get_mid_prices_in_range(self):
        current_time = timezone.now()
        StockPriceHistory.objects.create(stock_id=1, high_price=110, low_price=90, timestamp=current_time)
        StockPriceHistory.objects.create(stock_id=1, high_price=120, low_price=100, timestamp=current_time)
        StockPriceHistory.objects.create(stock_id=1, high_price=130, low_price=110, timestamp=current_time)

        mid_prices = get_mid_prices_in_range(1, timedelta(hours=1))
        expected_mid_prices = [(110 + 90) / 2, (120 + 100) / 2, (130 + 110) / 2]

        self.assertEqual(mid_prices, expected_mid_prices)

    def test_get_stock_volatility_with_sufficient_data(self):
        prices = [100, 105, 110, 115, 120]
        log_returns = np.log(np.array(prices[1:]) / np.array(prices[:-1]))
        expected_volatility = np.std(log_returns)

        volatility = get_stock_volatility(MagicMock(), 'TEST', prices)
        self.assertAlmostEqual(volatility, expected_volatility)

    def test_get_stock_volatility_with_insufficient_data(self):
        prices = [100]
        volatility = get_stock_volatility(MagicMock(), 'TEST', prices)
        self.assertEqual(volatility, 0)