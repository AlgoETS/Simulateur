from django.db import models

class Scenario(models.Model):
    name = models.CharField(max_length=100, default='')
    description = models.TextField(default='')
    backstory = models.TextField(default='')
    duration = models.IntegerField(default=0)
    companies = models.ManyToManyField('Company', related_name='scenarios')
    stocks = models.ManyToManyField('Stock', related_name='scenarios')
    users = models.ManyToManyField('UserProfile', related_name='scenarios')
    teams = models.ManyToManyField('Team', related_name='scenarios')
    events = models.ManyToManyField('Event', related_name='scenarios')
    triggers = models.ManyToManyField('Trigger', related_name='scenarios')
    simulation_settings = models.OneToOneField('SimulationSettings', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Scenarios"
