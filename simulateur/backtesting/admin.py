from django.contrib import admin
from .models import Strategy, Backtest, StockBacktest, Chart, DataSource, SandboxData


@admin.register(Strategy)
class StrategyAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'created_at')
    search_fields = ('name', 'created_by__username')
    list_filter = ('created_by', 'created_at')
    ordering = ('-created_at',)

@admin.register(StockBacktest)
class StockBacktestAdmin(admin.ModelAdmin):
    list_display = ('ticker', 'name', 'sector', 'exchange', 'created_at')
    search_fields = ('ticker', 'name', 'sector', 'exchange')
    list_filter = ('sector', 'exchange', 'created_at')
    ordering = ('ticker',)

@admin.register(Backtest)
class BacktestAdmin(admin.ModelAdmin):
    list_display = ('strategy', 'stock', 'status', 'start_date', 'end_date', 'created_at')
    search_fields = ('strategy__name', 'stock__name', 'instrument')
    list_filter = ('status', 'created_at', 'start_date', 'end_date')
    ordering = ('-created_at',)

@admin.register(Chart)
class ChartAdmin(admin.ModelAdmin):
    list_display = ('backtest', 'chart_file')
    search_fields = ('backtest__strategy__name', 'backtest__stock__name')
    list_filter = ('backtest__created_at',)

@admin.register(DataSource)
class DataSourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'api_url', 'created_at')
    search_fields = ('name', 'api_url')
    list_filter = ('created_at',)