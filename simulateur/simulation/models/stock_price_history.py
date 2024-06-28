from django.db import models

class StockPriceHistory(models.Model):
    stock = models.ForeignKey('Stock', on_delete=models.CASCADE, related_name='price_history')
    price = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.stock.company.name} Price at {self.timestamp}'

    class Meta:
        verbose_name_plural = "Stock Price Histories"
        ordering = ['timestamp']
