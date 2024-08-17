from django.core.management.base import BaseCommand
from simulation.models.scenario import Scenario
from simulation.logic.simulation_manager import SimulationManagerSingleton


class Command(BaseCommand):
    help = 'Start the simulation based on a simulation manager id'

    def add_arguments(self, parser):
        parser.add_argument('simulation_manager_id', type=int, help='The ID of the simulation manager to simulate')

    def handle(self, *args, **kwargs):
        simulation_manager_id = kwargs['simulation_manager_id']
        try:
            simulation_manager = SimulationManagerSingleton.get_instance(simulation_manager_id)
            simulation_manager.start_simulation()
        except Scenario.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Scenario with ID {simulation_manager_id} does not exist.'))
        except KeyboardInterrupt:
            self.stdout.write(self.style.SUCCESS('Simulation stopped successfully'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error occurred: {e}'))
