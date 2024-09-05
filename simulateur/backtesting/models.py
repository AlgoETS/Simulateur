from django.db import models
from django.contrib.auth.models import User


class Strategy(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    file_name = models.FileField(upload_to='strategies/', help_text="Strategy file stored in MinIO")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Strategy"
        verbose_name_plural = "Strategies"
        ordering = ['-created_at']

    def __str__(self):
        return f"Strategy: {self.name} by {self.created_by.username}"


class StrategyOutput(models.Model):
    strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE, related_name="outputs")
    ticker = models.CharField(max_length=50)
    output_type = models.CharField(
        max_length=50,
        choices=[
            ('chart', 'Chart'),
            ('raw', 'Raw Data'),
            ('complete', 'Complete Data')
        ]
    )
    file = models.FileField(upload_to='strategy_outputs/', help_text="Output file stored in MinIO")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.strategy.name} - {self.ticker} ({self.output_type})"


class DataSource(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    api_url = models.URLField(blank=True, null=True, help_text="URL for the data source API")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Data Source"
        verbose_name_plural = "Data Sources"
        ordering = ['name']

    def __str__(self):
        return self.name


class StockBacktest(models.Model):
    ticker = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)
    sector = models.CharField(max_length=255, null=True, blank=True)
    exchange = models.CharField(max_length=255, null=True, blank=True)
    data_source = models.ForeignKey(DataSource, on_delete=models.CASCADE, related_name="stocks")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Stock"
        verbose_name_plural = "Stocks"
        ordering = ['ticker']

    def __str__(self):
        return f"{self.name} ({self.ticker}) - {self.exchange} - Source: {self.data_source.name}"


class Backtest(models.Model):
    strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE, related_name="backtests")
    stock = models.ForeignKey(StockBacktest, on_delete=models.CASCADE, related_name="backtests")
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('running', 'Running'),
            ('completed', 'Completed'),
            ('failed', 'Failed')
        ],
        default='pending'
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    result_file = models.FileField(upload_to='backtest_results/', null=True, blank=True,
                                   help_text="Backtest result file stored in MinIO")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Backtest"
        verbose_name_plural = "Backtests"
        ordering = ['-created_at']

    def __str__(self):
        return f"Backtest: {self.strategy.name} on {self.stock.name} ({self.instrument})"


class Chart(models.Model):
    backtest = models.ForeignKey(Backtest, on_delete=models.CASCADE, related_name="charts")
    chart_file = models.FileField(upload_to='backtest_charts/', null=True, blank=True,
                                  help_text="Chart image stored in MinIO")

    class Meta:
        verbose_name = "Chart"
        verbose_name_plural = "Charts"

    def __str__(self):
        return f"Chart for {self.backtest.strategy.name} - {self.backtest.stock.ticker}"


class SandboxData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sandbox_data")
    ticker = models.CharField(max_length=10, help_text="Ticker symbol of the stock")
    start_date = models.DateField()
    end_date = models.DateField()
    interval = models.CharField(max_length=10, choices=[
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly')
    ], default='daily')
    overlay = models.JSONField(blank=True, null=True, help_text="Selected overlays like EMA, SMA, Bollinger Bands")
    chart_data = models.JSONField(blank=True, null=True, help_text="Stored chart data in JSON format")
    indicators_data = models.JSONField(blank=True, null=True, help_text="Stored indicator data in JSON format")
    crossings = models.JSONField(blank=True, null=True, help_text="Stored crossings information in JSON format")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Sandbox Data"
        verbose_name_plural = "Sandbox Data"
        ordering = ['-created_at']

    def __str__(self):
        return f"Sandbox Data for {self.ticker} ({self.interval}) by {self.user.username}"
