from django.db import models

class Event(models.Model):
    name = models.CharField(max_length=100, default='')
    description = models.TextField(default='')
    type = models.CharField(max_length=100, default='')
    date = models.DateTimeField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Events"
