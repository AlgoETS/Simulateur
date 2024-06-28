from django.db import models

class Portfolio(models.Model):
    owner = models.OneToOneField('UserProfile', on_delete=models.CASCADE, null=True, blank=True, related_name='portfolio')
    team = models.OneToOneField('Team', on_delete=models.CASCADE, null=True, blank=True, related_name='portfolio')
    stocks = models.ManyToManyField('Stock')

    def __str__(self):
        return f'Portfolio for {self.owner or self.team}'

    class Meta:
        verbose_name_plural = "Portfolios"
