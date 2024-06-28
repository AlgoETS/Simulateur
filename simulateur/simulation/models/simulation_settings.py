from django.db import models

class SimulationSettings(models.Model):
    TIME_UNIT_CHOICES = [
        ('second', 'Second'),
        ('minute', 'Minute'),
        ('hour', 'Hour'),
        ('day', 'Day'),
        ('month', 'Month'),
        ('year', 'Year')
    ]

    NOISE_FUNCTION_CHOICES = [
        ('brownian', 'Brownian Motion'),
        ('monte_carlo', 'Monte Carlo'),
        ('perlin', 'Perlin Noise'),
        ('random_walk', 'Random Walk'),
        ('fbm', 'Fractional Brownian Motion'),
        ('other', 'Other')
    ]

    max_users = models.IntegerField(default=100)
    max_companies = models.IntegerField(default=50)
    timer_step = models.IntegerField(default=10)
    timer_step_unit = models.CharField(max_length=6, choices=TIME_UNIT_CHOICES, default='minute')
    interval = models.IntegerField(default=20)
    interval_unit = models.CharField(max_length=6, choices=TIME_UNIT_CHOICES, default='minute')
    max_interval = models.IntegerField(default=3000)
    fluctuation_rate = models.FloatField(default=0.1)
    close_stock_market_at_night = models.BooleanField(default=True)
    noise_function = models.CharField(max_length=20, choices=NOISE_FUNCTION_CHOICES, default='brownian')

    def __str__(self):
        return f'Simulation Settings: Max users: {self.max_users}, Max companies: {self.max_companies}'

    class Meta:
        verbose_name_plural = "Simulation Settings"
