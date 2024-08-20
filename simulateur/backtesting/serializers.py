from rest_framework import serializers
from .models import Chart, Strategy

class ChartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chart
        fields = ['id', 'chart_file', 'backtest']

class StrategySerializer(serializers.ModelSerializer):
    class Meta:
        model = Strategy
        fields = ['id', 'name', 'description', 'parameters', 'script_path', 'created_at']
