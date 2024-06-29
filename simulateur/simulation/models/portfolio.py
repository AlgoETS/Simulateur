from django.db import models

class Portfolio(models.Model):
    owner = models.OneToOneField('UserProfile', on_delete=models.CASCADE, null=True, blank=True, related_name='portfolio')
    teams = models.ManyToManyField('Team', related_name='portfolios', blank=True)
    balance = models.FloatField(default=0.0)
    stocks = models.ManyToManyField('Stock', through='StockPortfolio')
    transactions = models.ManyToManyField('TransactionHistory', related_name='portfolios', blank=True)

    def __str__(self):
        return f'Portfolio for {self.owner or self.team}'

    class Meta:
        verbose_name_plural = "Portfolios"

class StockPortfolio(models.Model):
    stock = models.ForeignKey('Stock', on_delete=models.CASCADE)
    portfolio = models.ForeignKey('Portfolio', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    class Meta:
        unique_together = ('stock', 'portfolio')
