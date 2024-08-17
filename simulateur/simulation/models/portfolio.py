from django.db import models
from simulation.models import StockPriceHistory


class Portfolio(models.Model):
    owner = models.OneToOneField(
        "UserProfile",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="portfolio",
    )
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    simulation_manager = models.ForeignKey("SimulationManager", on_delete=models.CASCADE, related_name='portfolios')

    def __str__(self):
        return f"Portfolio for {self.owner}"

    class Meta:
        verbose_name_plural = "Portfolios"


class StockPortfolio(models.Model):
    stock = models.ForeignKey("Stock", on_delete=models.CASCADE, blank=True)
    portfolio = models.ForeignKey("Portfolio", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    latest_price_history = models.ForeignKey(
        "StockPriceHistory", on_delete=models.CASCADE, null=True, blank=True, related_name="stock_portfolios"
    )

    def update_latest_price(self):
        """Update the latest price history based on the most recent StockPriceHistory for the stock."""
        self.latest_price_history = StockPriceHistory.objects.filter(stock=self.stock).order_by('-timestamp').first()
        self.save()

    def __str__(self):
        return f"{self.quantity} of {self.stock.ticker} in {self.portfolio}"

    class Meta:
        unique_together = ("stock", "portfolio")
