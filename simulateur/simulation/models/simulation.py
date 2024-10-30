from django.db import models


class Simulation(models.Model):
    class ScenarioState(models.TextChoices):
        INITIALIZED = 'initialized', 'Initialized'
        CREATED = 'created', 'Created'
        PUBLISHED = 'published', 'Published'
        ONGOING = 'ongoing', 'Ongoing'
        STOPPED = 'stopped', 'Stopped'
        FINISHED = 'finished', 'Finished'

    scenario = models.OneToOneField('Scenario', on_delete=models.CASCADE, related_name='simulation_manager')
    teams = models.ForeignKey('Team', related_name='scenarios_teams')
    triggers = models.ForeignKey('Trigger', related_name='scenarios_triggers')
    news = models.ForeignKey('News', related_name='scenarios_news')
    simulation_settings = models.OneToOneField('SimulationSettings', on_delete=models.CASCADE)
    state = models.CharField(
        max_length=20,
        choices=ScenarioState.choices,
        default=ScenarioState.INITIALIZED,
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Scenario Manager: {self.scenario.name}'

    class Meta:
        verbose_name_plural = "Simulation Managers"

