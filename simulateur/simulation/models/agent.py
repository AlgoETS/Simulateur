from django.db import models
from django.contrib.auth.models import User


class Agent(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    linked_simulation = models.ForeignKey("SimulationManager", on_delete=models.SET_NULL, null=True, blank=True,
                                          related_name='agents')
    strategy_configuration = models.JSONField(default=dict)  # Store strategy config in JSON format
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Agents"


class Script(models.Model):
    agent = models.ForeignKey(Agent, related_name='scripts', on_delete=models.CASCADE)
    language = models.CharField(max_length=50, default="python")  # Assuming Python for now, can be extended
    code = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Script for {self.agent.name}"


class ScriptExecution(models.Model):
    script = models.ForeignKey(Script, related_name='executions', on_delete=models.CASCADE)
    input_data = models.JSONField()  # Data received from the WebSocket or any other source
    output_data = models.JSONField(blank=True, null=True)
    error = models.TextField(blank=True, null=True)
    executed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Execution of {self.script.agent.name} on {self.executed_at}"


class Indicator(models.Model):
    """
    Store individual indicators that might be used by a strategy, linked to an agent.
    """
    agent = models.ForeignKey(Agent, related_name='indicators', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    indicator_type = models.CharField(max_length=50)  # e.g., SMA, EMA, RSI
    parameters = models.JSONField(default=dict)  # Store indicator-specific parameters in JSON format
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.indicator_type}) for {self.agent.name}"


class StrategyLog(models.Model):
    """
    Keep track of strategy decisions (buy/sell) made by agents during a simulation.
    """
    agent = models.ForeignKey(Agent, related_name='strategy_logs', on_delete=models.CASCADE)
    action = models.CharField(max_length=50)  # e.g., buy, sell, hold
    stock = models.CharField(max_length=50)  # Stock ticker or asset name
    price = models.DecimalField(max_digits=12, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.agent.name} - {self.action} {self.stock} at {self.price} on {self.timestamp}"
