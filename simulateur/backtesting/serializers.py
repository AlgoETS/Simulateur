from rest_framework import serializers
from .models import Strategy, Backtest, StockBacktest, StrategyOutput, Chart


class StrategySerializer(serializers.ModelSerializer):
    class Meta:
        model = Strategy
        fields = ['id', 'name', 'description', 'file_name', 'created_at', 'created_by']

class BacktestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Backtest
        fields = ['id', 'strategy', 'stock', 'start_date', 'end_date', 'status', 'result_file', 'created_at']

class StockBacktestSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockBacktest
        fields = ['id', 'ticker', 'name', 'sector', 'exchange', 'created_at']

class StrategyOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = StrategyOutput
        fields = ['id', 'strategy', 'ticker', 'output_type', 'file', 'created_at']

class ChartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chart
        fields = ['id', 'backtest', 'chart_file', 'created_at']