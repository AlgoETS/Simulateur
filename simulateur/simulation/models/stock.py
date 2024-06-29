from django.db import models

class Stock(models.Model):
    company = models.ForeignKey('Company', on_delete=models.CASCADE)
    ticker = models.CharField(max_length=10, default='')
    price = models.FloatField(default=0.0)
    open_price = models.FloatField(default=0.0)
    high_price = models.FloatField(default=0.0)
    low_price = models.FloatField(default=0.0)
    close_price = models.FloatField(default=0.0)
    partial_share = models.FloatField(default=0.0)
    complete_share = models.IntegerField(default=0)
    stock_price_history = models.ForeignKey('StockPriceHistory', on_delete=models.CASCADE, null=True, blank=True, related_name='stocks_history')  # Provide a unique related_name
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.company.name} Stock'

    class Meta:
        verbose_name_plural = "Stocks"
        ordering = ['timestamp']

class StockPriceHistory(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='price_history')  # Provide a unique related_name
    price = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.stock.company.name} Price at {self.timestamp}'

    class Meta:
        verbose_name_plural = "Stock Price Histories"
        ordering = ['timestamp']
