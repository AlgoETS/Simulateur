from django.db import models


class SimulationData(models.Model):
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    price_changes = models.JSONField(default=list)
    transactions = models.JSONField(default=list)

    class Meta:
        verbose_name_plural = "Simulation Data"
