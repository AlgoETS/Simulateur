from datetime import timedelta, timezone, datetime
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.crypto import get_random_string

class Company(models.Model):
    name = models.CharField(max_length=100, default='')
    backstory = models.TextField(default='')
    sector = models.CharField(max_length=100, default='')
    country = models.CharField(max_length=100, default='')
    industry = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Companies"

class Stock(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    ticker = models.CharField(max_length=10, default='')
    price = models.FloatField(default=0.0)
    open_price = models.FloatField(default=0.0)
    high_price = models.FloatField(default=0.0)
    low_price = models.FloatField(default=0.0)
    close_price = models.FloatField(default=0.0)
    partial_share = models.FloatField(default=0.0)
    complete_share = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.company.name} Stock'

    class Meta:
        verbose_name_plural = "Stocks"

class Team(models.Model):
    name = models.CharField(max_length=100, default='')
    balance = models.FloatField(default=100000)
    members = models.ManyToManyField('UserProfile', related_name='teams')

    def __str__(self):
        return self.name

    def generate_join_link(self):
        unique_key = get_random_string(32)  # Generate a unique key for the link
        join_link = JoinLink.objects.create(team=self, key=unique_key)
        return join_link.get_absolute_url()

    class Meta:
        verbose_name_plural = "Teams"

class JoinLink(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='join_links')
    key = models.CharField(max_length=32, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(hours=1)  # Set expiration time to 1 hour
        super().save(*args, **kwargs)

    def is_expired(self):
        return timezone.now() > self.expires_at

    def get_absolute_url(self):
        return reverse('join_team', kwargs={'team_id': self.team.id, 'key': self.key})

    class Meta:
        verbose_name_plural = "Join Links"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.FloatField(default=10000)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True, related_name='user_profiles')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = "User Profiles"

class Event(models.Model):
    name = models.CharField(max_length=100, default='')
    description = models.TextField(default='')
    event_type = models.CharField(max_length=100, default='')
    trigger_date = models.DateTimeField()
    scenario = models.ForeignKey('Scenario', on_delete=models.CASCADE, related_name='scenario_events')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Events"

class Trigger(models.Model):
    name = models.CharField(max_length=100, default='')
    description = models.TextField(default='')
    trigger_type = models.CharField(max_length=100, default='')
    trigger_value = models.FloatField(default=0.0)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_triggers')
    scenario = models.ForeignKey('Scenario', on_delete=models.CASCADE, related_name='scenario_triggers')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Triggers"

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
        ('other', 'Other')
    ]

    max_users = models.IntegerField(default=100)
    max_companies = models.IntegerField(default=50)
    timer_step = models.IntegerField(default=10)
    timer_step_unit = models.CharField(max_length=6, choices=TIME_UNIT_CHOICES, default='minute')
    interval = models.IntegerField(default=20)
    interval_unit = models.CharField(max_length=6, choices=TIME_UNIT_CHOICES, default='minute')
    max_interval = models.IntegerField(default=3000)  # Maximum interval in seconds
    fluctuation_rate = models.FloatField(default=0.1)  # Rate of random fluctuation
    time_unit = models.CharField(max_length=6, choices=TIME_UNIT_CHOICES, default='minute')
    close_stock_market_at_night = models.BooleanField(default=True)
    noise_function = models.CharField(max_length=20, choices=NOISE_FUNCTION_CHOICES, default='brownian')

    def __str__(self):
        return f'Simulation Settings:\n' \
               f'  Max users: {self.max_users}\n' \
               f'  Max companies: {self.max_companies}\n' \
               f'  Timer step: {self.timer_step} {self.get_timer_step_unit_display()}\n' \
               f'  Interval: {self.interval} {self.get_interval_unit_display()}\n' \
               f'  Max interval: {self.max_interval} seconds\n' \
               f'  Fluctuation rate: {self.fluctuation_rate}\n' \
               f'  Time unit: {self.get_time_unit_display()}\n' \
               f'  Close stock market at night: {"Yes" if self.close_stock_market_at_night else "No"}\n' \
               f'  Noise function: {self.get_noise_function_display()}'

    class Meta:
        verbose_name_plural = "Simulation Settings"

class Scenario(models.Model):
    name = models.CharField(max_length=100, default='')
    description = models.TextField(default='')
    backstory = models.TextField(default='')
    difficulty_level = models.CharField(max_length=100, default='')
    duration = models.IntegerField(default=0)  # Duration in seconds
    companies = models.ManyToManyField(Company, related_name='scenarios')
    stocks = models.ManyToManyField(Stock, related_name='scenarios')
    users = models.ManyToManyField(UserProfile, related_name='scenarios')
    teams = models.ManyToManyField(Team, related_name='scenarios')
    events = models.ManyToManyField(Event, related_name='scenarios')
    triggers = models.ManyToManyField(Trigger, related_name='scenarios')
    simulation_settings = models.OneToOneField(SimulationSettings, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Scenarios"

class Portfolio(models.Model):
    owner = models.OneToOneField(UserProfile, on_delete=models.CASCADE, null=True, blank=True, related_name='portfolio')
    team = models.OneToOneField(Team, on_delete=models.CASCADE, null=True, blank=True, related_name='portfolio')
    stocks = models.ManyToManyField(Stock)

    def __str__(self):
        return f'Portfolio for {self.owner or self.team}'

    class Meta:
        verbose_name_plural = "Portfolios"

class TransactionHistory(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    asset = models.CharField(max_length=100, default='')
    transaction_type = models.CharField(max_length=100, default='')
    amount = models.FloatField(default=0.0)
    price = models.FloatField(default=0.0)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Transaction on {self.asset}'

    class Meta:
        verbose_name_plural = "Transaction Histories"

class SimulationData(models.Model):
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE)
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

class Order(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    ticker = models.CharField(max_length=100, default='')
    quantity = models.IntegerField(default=0)
    price = models.FloatField(default=0.0)
    transaction_type = models.CharField(max_length=10, default='buy')
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Order for {self.ticker}'

    class Meta:
        verbose_name_plural = "Orders"

class News(models.Model):
    title = models.CharField(max_length=100, default='')
    content = models.TextField(default='')
    published_date = models.DateTimeField(auto_now=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='news_items')
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE, related_name='news_items')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Market News"
