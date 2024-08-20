from django.db import models
from django.contrib.auth.models import User

class Strategy(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    file_name = models.CharField(max_length=255, help_text="Name of the strategy file stored in MinIO")
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
    file_path = models.CharField(max_length=255)  # Path to where the output is stored
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.strategy.name} - {self.ticker} ({self.output_type})"


class StockBacktest(models.Model):
    ticker = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)
    sector = models.CharField(max_length=255, null=True, blank=True)
    exchange = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Stock"
        verbose_name_plural = "Stocks"
        ordering = ['ticker']

    def __str__(self):
        return f"{self.name} ({self.ticker}) - {self.exchange}"


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
    instrument = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    result_file = models.FileField(upload_to='backtest_results/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Backtest"
        verbose_name_plural = "Backtests"
        ordering = ['-created_at']

    def __str__(self):
        return f"Backtest: {self.strategy.name} on {self.stock.name} ({self.instrument})"


class Chart(models.Model):
    backtest = models.ForeignKey(Backtest, on_delete=models.CASCADE, related_name="charts")
    chart_file = models.FileField(upload_to='backtest_charts/', null=True, blank=True)

    class Meta:
        verbose_name = "Chart"
        verbose_name_plural = "Charts"

    def __str__(self):
        return f"Chart for {self.backtest.strategy.name} - {self.backtest.stock.ticker}"
