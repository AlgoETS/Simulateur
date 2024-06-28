from django.db import models

class Order(models.Model):
    user = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    ticker = models.CharField(max_length=100, default='')
    quantity = models.IntegerField(default=0)
    price = models.FloatField(default=0.0)
    transaction_type = models.CharField(
        max_length=100, default='')
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Order for {self.ticker}'

    class Meta:
        verbose_name_plural = "Orders"
