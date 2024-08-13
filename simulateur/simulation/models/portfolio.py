from django.db import models

class Portfolio(models.Model):
    owner = models.OneToOneField(
        "UserProfile",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="portfolio",
    )
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    scenario = models.ManyToManyField(
        "Scenario", blank=True
    )
    

    def __str__(self):
        return f"Portfolio for {self.owner or 'Unknown'}"

    class Meta:
        verbose_name_plural = "Portfolios"


class StockPortfolio(models.Model):
    stock = models.ForeignKey("Stock", on_delete=models.CASCADE, blank=True)
    portfolio = models.ForeignKey("Portfolio", on_delete=models.CASCADE, related_name="stock_portfolios")
    average_holding_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    quantity = models.IntegerField(default=0)

    class Meta:
        unique_together = ("stock", "portfolio")
