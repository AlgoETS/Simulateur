from django.core.management.base import BaseCommand
from simulation.logic.simulation_manager import SimulationManager

class Command(BaseCommand):
    help = 'Start the simulation based on a scenario'

    def add_arguments(self, parser):
        parser.add_argument('scenario_id', type=int, help='The ID of the scenario to simulate')

    def handle(self, *args, **kwargs):
        scenario_id = kwargs['scenario_id']
        simulation_manager = SimulationManager(scenario_id)
        try:
            simulation_manager.start_simulation()
        except KeyboardInterrupt:
            simulation_manager.stop_simulation()
            self.stdout.write(self.style.SUCCESS('Simulation stopped successfully'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error occurred: {e}'))
