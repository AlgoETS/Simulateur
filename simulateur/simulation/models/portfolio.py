from django.db import models

from simulation.models.simulation_manager import ScenarioManager


class Portfolio(models.Model):
    owner = models.OneToOneField(
        "UserProfile",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="portfolio",
    )
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    scenario_manager = models.ForeignKey(ScenarioManager, on_delete=models.CASCADE)

    def __str__(self):
        return f"Portfolio for {self.owner or self.team}"

    class Meta:
        verbose_name_plural = "Portfolios"


class StockPortfolio(models.Model):
    stock = models.ForeignKey("Stock", on_delete=models.CASCADE, blank=True)
    portfolio = models.ForeignKey("Portfolio", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    class Meta:
        unique_together = ("stock", "portfolio")
