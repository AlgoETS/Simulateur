from datetime import datetime
import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import HttpResponseRedirect, HttpResponseBadRequest, JsonResponse
from yahoofinancials import YahooFinancials
import pandas as pd

from .forms import StrategyForm
from .models import Strategy, StrategyOutput, DataSource, StockBacktest, SandboxData


class StrategyManagementView(View):
    def get(self, request):
        form = StrategyForm()
        strategies = Strategy.objects.all()
        context = {
            'form': form,
            'strategies': strategies
        }
        return render(request, 'strategy_management.html', context)

    def post(self, request):
        form = StrategyForm(request.POST, request.FILES)
        if form.is_valid():
            strategy = form.save(commit=False)
            strategy.created_by = request.user
            strategy.save()

            # Get additional fields from the form
            ticker = request.POST.get('ticker')
            time_range = request.POST.get('time_range')
            data_source = request.POST.get('data_source')
            script_content = request.POST.get('script_content', '# Your strategy logic here')

            # Handle creating or saving strategy file content
            strategy.create_script_file(content=script_content)

            return HttpResponseRedirect(request.path_info)

        strategies = Strategy.objects.filter(created_by=request.user)
        context = {
            'form': form,
            'strategies': strategies
        }
        return render(request, 'strategy_management.html', context)


class SearchChartView(View):
    def get(self, request):
        strategies = Strategy.objects.all()
        strategy_outputs = StrategyOutput.objects.none()

        selected_strategy_id = request.GET.get('strategy')
        ticker = request.GET.get('ticker')

        if selected_strategy_id and ticker:
            strategy_outputs = StrategyOutput.objects.filter(
                strategy_id=selected_strategy_id,
                ticker=ticker
            )

        context = {
            'strategies': strategies,
            'strategy_outputs': strategy_outputs,
        }
        return render(request, 'search_chart.html', context)


class SandboxView(View):
    @login_required
    def get(self, request):
        return render(request, 'sandbox_chart.html')

    @login_required
    def post(self, request):
        ticker = request.POST.get('ticker', 'AAPL')
        start_date = request.POST.get('start_date', '2018-01-01')
        end_date = request.POST.get('end_date', '2024-01-01')
        interval = request.POST.get('interval', 'weekly')
        overlay = request.POST.get('overlay', '')  # e.g., 'ema,sma,bollinger'

        # Indicator parameters
        ema_periods = json.loads(request.POST.get('ema_periods', '[]'))
        sma_periods = json.loads(request.POST.get('sma_periods', '[]'))
        bollinger_periods = json.loads(request.POST.get('bollinger_periods', '[]'))
        bollinger_stddevs = json.loads(request.POST.get('bollinger_stddevs', '[]'))

        # Convert periods to integers and standard deviations to floats
        ema_periods = [int(period) for period in ema_periods if isinstance(period, (str, int))]
        sma_periods = [int(period) for period in sma_periods if isinstance(period, (str, int))]
        bollinger_periods = [int(period) for period in bollinger_periods if isinstance(period, (str, int))]
        bollinger_stddevs = [float(stddev) for stddev in bollinger_stddevs if isinstance(stddev, (str, float))]

        # Check if the data already exists in the database
        existing_data = SandboxData.objects.filter(
            user=request.user,
            ticker=ticker,
            start_date=start_date,
            end_date=end_date,
            interval=interval,
            overlay=overlay
        ).first()

        if existing_data:
            # Return the existing data if found
            return JsonResponse({
                'chart_data': existing_data.chart_data,
                'indicators_data': existing_data.indicators_data,
                'crossings': existing_data.crossings
            })

        try:
            # Fetch new data if not already stored
            stock_data = self.get_stock_data(ticker, start_date, end_date, interval)
            if stock_data is None or stock_data.empty:
                return HttpResponseBadRequest("No data found for the provided ticker and date range.")

            chart_data = self.transform_stock_data(stock_data)
            indicators_data = self.calculate_indicators(
                overlay, stock_data, ema_periods, sma_periods, bollinger_periods, bollinger_stddevs
            )
            crossings = self.calculate_crossings(indicators_data)

            # Save the new data to the database
            SandboxData.objects.create(
                user=request.user,
                ticker=ticker,
                start_date=start_date,
                end_date=end_date,
                interval=interval,
                overlay=overlay,
                chart_data=chart_data,
                indicators_data=indicators_data,
                crossings=crossings
            )

            return JsonResponse({
                'chart_data': chart_data,
                'indicators_data': indicators_data,
                'crossings': crossings
            })

        except Exception as e:
            return HttpResponseBadRequest(f"An error occurred: {str(e)}")

    def get_stock_data(self, ticker, start_date, end_date, interval):
        stock = YahooFinancials(ticker)
        historical_data = stock.get_historical_price_data(start_date, end_date, interval)

        if historical_data and ticker in historical_data and historical_data[ticker]['prices']:
            prices = pd.DataFrame(historical_data[ticker]['prices'])
            prices['formatted_date'] = pd.to_datetime(prices['formatted_date'])
            if prices.empty:
                return None
            return prices
        return None

    def transform_stock_data(self, prices):
        return [
            {
                'time': int(row['formatted_date'].timestamp()),
                'open': round(row['open'], 2),
                'high': round(row['high'], 2),
                'low': round(row['low'], 2),
                'close': round(row['close'], 2),
                'volume': int(row['volume'])
            }
            for _, row in prices.iterrows()
        ]

    def calculate_indicators(self, overlay, prices, ema_periods, sma_periods, bollinger_periods, bollinger_stddevs):
        indicators_data = {}

        if 'ema' in overlay:
            indicators_data['ema'] = self.calculate_ema(prices, ema_periods)

        if 'sma' in overlay:
            indicators_data['sma'] = self.calculate_sma(prices, sma_periods)

        if 'bollinger' in overlay and bollinger_periods and bollinger_stddevs:
            indicators_data['bollinger'] = self.calculate_bollinger(prices, bollinger_periods, bollinger_stddevs)

        return indicators_data

    def calculate_ema(self, prices, ema_periods):
        ema_data = []
        for period in ema_periods:
            ema_label = f"EMA_{period}"
            prices[ema_label] = prices['close'].ewm(span=period, adjust=False).mean()
            ema_data.append({
                'period': period,
                'values': [
                    {'time': int(row['formatted_date'].timestamp()), 'value': round(row[ema_label], 2)}
                    for _, row in prices.iterrows()
                ]
            })
        return ema_data

    def calculate_sma(self, prices, sma_periods):
        sma_data = []
        for period in sma_periods:
            sma_label = f"SMA_{period}"
            prices[sma_label] = prices['close'].rolling(window=period).mean()
            sma_data.append({
                'period': period,
                'values': [
                    {'time': int(row['formatted_date'].timestamp()), 'value': round(row[sma_label], 2)}
                    for _, row in prices.iterrows()
                ]
            })
        return sma_data

    def calculate_bollinger(self, prices, bollinger_periods, bollinger_stddevs):
        bollinger_data = []
        for period, stddev in zip(bollinger_periods, bollinger_stddevs):
            prices[f'MA_{period}'] = prices['close'].rolling(window=period).mean()
            prices['stddev'] = prices['close'].rolling(window=period).std()
            prices['upper'] = prices[f'MA_{period}'] + (prices['stddev'] * stddev)
            prices['lower'] = prices[f'MA_{period}'] - (prices['stddev'] * stddev)
            bollinger_data.append({
                'period': period,
                'upper': [
                    {'time': int(row['formatted_date'].timestamp()), 'value': round(row['upper'], 2)}
                    for _, row in prices.iterrows()
                ],
                'lower': [
                    {'time': int(row['formatted_date'].timestamp()), 'value': round(row['lower'], 2)}
                    for _, row in prices.iterrows()
                ]
            })
        return bollinger_data

    def calculate_crossings(self, indicators_data):
        crossings = []
        ema_series = indicators_data.get('ema', [])
        sma_series = indicators_data.get('sma', [])

        if len(ema_series) > 1:
            crossings.extend(self._detect_crossings_between_series(ema_series, "EMA"))

        if len(sma_series) > 1:
            crossings.extend(self._detect_crossings_between_series(sma_series, "SMA"))

        if ema_series and sma_series:
            ema_values = ema_series[0]['values']
            sma_values = sma_series[0]['values']
            crossings.extend(self._detect_ema_sma_crossings(ema_values, sma_values))

        return crossings

    def _detect_crossings_between_series(self, series_list, label):
        crossings = []
        # Compare each series against every other series in the list
        for i in range(len(series_list)):
            for j in range(i + 1, len(series_list)):
                series_a = series_list[i]['values']
                series_b = series_list[j]['values']
                crossings.extend(self._detect_crossings_between_two_series(series_a, series_b,
                                                                           f"{label}_{series_list[i]['period']}_vs_{series_list[j]['period']}"))
        return crossings

    def _detect_crossings_between_two_series(self, series_a, series_b, label):
        crossings = []
        for i in range(1, len(series_a)):
            previous_a = series_a[i - 1]['value']
            current_a = series_a[i]['value']
            previous_b = series_b[i - 1]['value']
            current_b = series_b[i]['value']

            if previous_a < previous_b and current_a > current_b:
                crossings.append({
                    'time': series_a[i]['time'],
                    'type': f'cross_above'
                })
            elif previous_a > previous_b and current_a < current_b:
                crossings.append({
                    'time': series_a[i]['time'],
                    'type': f'cross_below'
                })
        return crossings

    def _detect_ema_sma_crossings(self, ema_values, sma_values):
        crossings = []
        for i in range(1, len(ema_values)):
            previous_ema = ema_values[i - 1]['value']
            current_ema = ema_values[i]['value']
            previous_sma = sma_values[i - 1]['value']
            current_sma = sma_values[i]['value']

            if previous_ema < previous_sma and current_ema > current_sma:
                crossings.append({
                    'time': ema_values[i]['time'],
                    'type': 'ema_cross_above_sma'
                })
            elif previous_ema > previous_sma and current_ema < current_sma:
                crossings.append({
                    'time': ema_values[i]['time'],
                    'type': 'ema_cross_below_sma'
                })
        return crossings
