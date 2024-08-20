from django.db import models


class Scenario(models.Model):
    name = models.CharField(max_length=100, default='')
    description = models.TextField(default='')
    backstory = models.TextField(default='')
    duration = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Scenarios"
