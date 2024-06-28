from django.db import models

class TransactionHistory(models.Model):
    portfolio = models.ForeignKey('Portfolio', on_delete=models.CASCADE)
    asset = models.CharField(max_length=100, default='')
    transaction_type = models.CharField(max_length=100, default='')
    amount = models.FloatField(default=0.0)
    price = models.FloatField(default=0.0)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Transaction on {self.asset}'

    class Meta:
        verbose_name_plural = "Transaction Histories"
