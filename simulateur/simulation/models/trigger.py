from django.db import models

class Trigger(models.Model):
    name = models.CharField(max_length=100, default='')
    description = models.TextField(default='')
    type = models.CharField(max_length=100, default='')
    value = models.FloatField(default=0.0)
    events = models.ManyToManyField('Event', blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Triggers"
