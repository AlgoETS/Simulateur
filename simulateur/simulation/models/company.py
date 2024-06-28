from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=100, default='')
    backstory = models.TextField(default='')
    sector = models.CharField(max_length=100, default='')
    country = models.CharField(max_length=100, default='')
    industry = models.CharField(max_length=100, default='')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Companies"
