from django.core.management.base import BaseCommand
from simulation.models.simulation_manager import SimulationManager as SM
from simulation.logic.simulation_manager import SimulationManagerSingleton
import signal
import sys
import time
import threading

class Command(BaseCommand):
    help = 'Start and monitor multiple simulations based on simulation manager IDs'

    def add_arguments(self, parser):
        parser.add_argument(
            'simulation_manager_ids',
            nargs='+',
            type=int,
            help='The IDs of the simulation managers to monitor and simulate'
        )

    def handle(self, *args, **kwargs):
        simulation_manager_ids = kwargs['simulation_manager_ids']

        def stop_all_simulations(signal_received, frame):
            for simulation_manager in running_simulations:
                if simulation_manager:
                    # Change the state to STOPPED for each simulation
                    simulation_manager.simulation_manager.state = SM.ScenarioState.STOPPED
                    simulation_manager.simulation_manager.save()
                    simulation_manager.stop_simulation()
            self.stdout.write(self.style.SUCCESS('All simulations stopped successfully'))
            sys.exit(0)

        # Register the signal handler for Ctrl+C
        signal.signal(signal.SIGINT, stop_all_simulations)

        running_simulations = []

        def monitor_and_run_simulation(simulation_manager_id):
            try:
                simulation_manager = SimulationManagerSingleton.get_instance(simulation_manager_id)
                running_simulations.append(simulation_manager)

                previous_settings = None

                while True:
                    # Continuously monitor the state and settings of the simulation
                    simulation_manager.simulation_manager.refresh_from_db()

                    if simulation_manager.simulation_manager.state == SM.ScenarioState.ONGOING:
                        # Start the simulation if it's not already running
                        if not simulation_manager.running:
                            self.stdout.write(self.style.SUCCESS(f'Starting simulation {simulation_manager_id}...'))
                            simulation_manager.start_simulation()

                        # Check if the settings have changed
                        current_settings = simulation_manager.simulation_manager.simulation_settings
                        if previous_settings is None or previous_settings != current_settings:
                            self.stdout.write(self.style.WARNING(f'Updating settings for simulation {simulation_manager_id}...'))
                            # Logic to apply new settings to the running simulation
                            simulation_manager.apply_new_settings(current_settings)
                            previous_settings = current_settings

                    elif simulation_manager.simulation_manager.state == SM.ScenarioState.STOPPED:
                        # Stop the simulation if it's running
                        if simulation_manager.running:
                            self.stdout.write(self.style.WARNING(f'Stopping simulation {simulation_manager_id}...'))
                            simulation_manager.stop_simulation()

                    # Exit if the state is set to FINISHED
                    elif simulation_manager.simulation_manager.state == SM.ScenarioState.FINISHED:
                        self.stdout.write(self.style.SUCCESS(f'Simulation {simulation_manager_id} is finished. Exiting...'))
                        break

                    # Poll every 5 seconds to check for state and settings changes
                    time.sleep(5)

            except SM.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Scenario with ID {simulation_manager_id} does not exist.'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error occurred for simulation {simulation_manager_id}: {e}'))

        # Start a separate thread for each simulation manager
        for simulation_manager_id in simulation_manager_ids:
            threading.Thread(target=monitor_and_run_simulation, args=(simulation_manager_id,), daemon=True).start()

        # Keep the main thread alive to catch signals and manage the simulation lifecycle
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            stop_all_simulations(signal.SIGINT, None)  # Graceful stop on Ctrl+C
