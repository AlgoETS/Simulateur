from django.db import models
from simulateur.simulation.models.simulation import Simulation


class TransactionHistory(models.Model):
    simulation_manager = models.ForeignKey(Simulation, related_name='transactions', on_delete=models.CASCADE)
    orders = models.ManyToManyField('Order', related_name='transactions')

    def __str__(self):
        return f'Transaction for {self.orders.first().stock.ticker if self.orders.exists() else "N/A"}'

    class Meta:
        verbose_name_plural = "Transaction Histories"


class Order(models.Model):
    user = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    stock = models.ForeignKey('Stock', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    price = models.FloatField(default=0.0)
    transaction_type = models.CharField(max_length=100, choices=[('BUY', 'Buy'), ('SELL', 'Sell')], default='BUY')
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Order for {self.stock.ticker} by {self.user.user.username}'

    class Meta:
        verbose_name_plural = "Orders"
