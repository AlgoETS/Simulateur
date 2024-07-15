import asyncio
from django.core.management.base import BaseCommand
from simulation.models.scenario import Scenario
from simulation.logic.simulation_manager import SimulationManagerSingleton
from asgiref.sync import sync_to_async

class Command(BaseCommand):
    help = 'Start the simulation based on a scenario'

    def add_arguments(self, parser):
        parser.add_argument('scenario_id', type=int, help='The ID of the scenario to simulate')

    @sync_to_async
    def handle(self, *args, **kwargs):
        scenario_id = kwargs['scenario_id']
        try:
            asyncio.run(self.start_simulation(scenario_id))
        except Scenario.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Scenario with ID {scenario_id} does not exist.'))
        except KeyboardInterrupt:
            self.stdout.write(self.style.SUCCESS('Simulation stopped successfully'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error occurred: {e}'))

    async def start_simulation(self, scenario_id):
        simulation_manager = await SimulationManagerSingleton.get_instance(scenario_id)
        await simulation_manager.start_simulation()