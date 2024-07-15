from django.db import models
from datetime import datetime, timezone, timedelta

class SimulationData(models.Model):
    scenario = models.ForeignKey('Scenario', on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    price_changes = models.JSONField(default=list)
    transactions = models.JSONField(default=list)

    def __str__(self):
        return f'Simulation for {self.scenario.name}'

    def stop_simulation(self):
        self.end_time = datetime.now(timezone.utc)
        self.is_active = False
        self.save()

    @property
    def duration(self):
        if self.is_active:
            return timezone.now() - self.start_time
        elif self.end_time:
            return self.end_time - self.start_time
        else:
            return timedelta(seconds=0)

    class Meta:
        verbose_name_plural = "Simulation Data"
