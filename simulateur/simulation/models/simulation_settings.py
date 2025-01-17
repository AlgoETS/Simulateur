from django.db import models


class SimulationSettings(models.Model):
    TIME_UNIT_CHOICES = [
        ('millisecond', 'Millisecond'),
        ('centisecond', 'Centisecond'),
        ('decisecond', 'Decisecond'),
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

    STOCK_TRADING_CHOICES = [
        ('dynamic', 'Dynamic'),
        ('static', 'Static')
    ]

    timer_step = models.IntegerField(default=10)
    timer_step_unit = models.CharField(max_length=20, choices=TIME_UNIT_CHOICES, default='second')
    interval = models.IntegerField(default=20)
    interval_unit = models.CharField(max_length=20, choices=TIME_UNIT_CHOICES, default='second')
    max_interval = models.IntegerField(default=3000)
    fluctuation_rate = models.FloatField(default=0.1)
    close_stock_market_at_night = models.BooleanField(default=True)
    noise_function = models.CharField(max_length=20, choices=NOISE_FUNCTION_CHOICES, default='brownian')
    stock_trading_logic = models.CharField(max_length=20, choices=STOCK_TRADING_CHOICES, default='static')

    def __str__(self):
        return f'Simulation Settings: {self.id}'

    class Meta:
        verbose_name_plural = "Simulation Settings"
