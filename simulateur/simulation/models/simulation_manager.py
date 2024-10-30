from django.db import models


class SimulationManager(models.Model):
    
    
    simulations = models.ForeignKey('Simulation', on_delete=models.CASCADE, related_name='simulation_manager')
    

    def __str__(self):
        return f'Scenario Manager: {self.scenario.name}'

    class Meta:
        verbose_name_plural = "Simulation Managers"

