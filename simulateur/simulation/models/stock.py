from django.db import models


class Stock(models.Model):
    company = models.ForeignKey(
        "Company", on_delete=models.CASCADE, related_name="stocks"
    )
    ticker = models.CharField(max_length=10, default="")
    timestamp = models.DateTimeField(auto_now_add=True)
    volatility = models.FloatField(default=0.0)
    liquidity = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.company.name} Stock"

    class Meta:
        verbose_name_plural = "Stocks"
        ordering = ["timestamp"]

class StockPriceHistory(models.Model):
    stock = models.ForeignKey(
        Stock, on_delete=models.CASCADE, related_name="price_history"
    )
    open_price = models.FloatField(default=0.0)
    high_price = models.FloatField(default=0.0)
    low_price = models.FloatField(default=0.0)
    close_price = models.FloatField(default=0.0)
    timestamp = models.DateTimeField(auto_now_add=True)
    volatility = models.FloatField(default=0.0)
    liquidity = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.stock.company.name} Price at {self.timestamp}"

    class Meta:
        verbose_name_plural = "Stock Price Histories"
        ordering = ["timestamp"]
