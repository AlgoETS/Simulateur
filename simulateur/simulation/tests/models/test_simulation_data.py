from django.test import TestCase
from datetime import datetime, timezone, timedelta
from simulation.models import SimulationData, Scenario
from simulation.models.simulation_manager import ScenarioManager

class SimulationDataModelTest(TestCase):

    def setUp(self):
        # Create necessary related objects
        self.scenario = Scenario.objects.create(
            name="Test Scenario",
            description="A test scenario",
            backstory="This is a test backstory",
            duration=10
        )

        self.scenario_manager = ScenarioManager.objects.create(
            scenario=self.scenario  # Adjust based on actual fields in ScenarioManager
        )

        # Create a SimulationData instance
        self.simulation_data = SimulationData.objects.create(
            scenario_manager=self.scenario_manager,
            is_active=True,
            price_changes=[],
            transactions=[]
        )

    def test_simulation_data_creation(self):
        # Test if the SimulationData object was created successfully
        self.assertEqual(self.simulation_data.scenario_manager, self.scenario_manager)
        self.assertTrue(self.simulation_data.is_active)
        self.assertEqual(self.simulation_data.price_changes, [])
        self.assertEqual(self.simulation_data.transactions, [])
        self.assertIsNotNone(self.simulation_data.start_time)
        self.assertIsNone(self.simulation_data.end_time)

    def test_stop_simulation(self):
        # Test the stop_simulation method
        self.simulation_data.stop_simulation()
        self.assertFalse(self.simulation_data.is_active)
        self.assertIsNotNone(self.simulation_data.end_time)
        self.assertTrue(self.simulation_data.end_time > self.simulation_data.start_time)

    def test_duration_while_active(self):
        # Test the duration property when the simulation is active
        duration = self.simulation_data.duration
        self.assertTrue(duration > timedelta(seconds=0))

    def test_duration_after_stopping(self):
        # Test the duration property after stopping the simulation
        self.simulation_data.stop_simulation()
        duration = self.simulation_data.duration
        expected_duration = self.simulation_data.end_time - self.simulation_data.start_time
        self.assertEqual(duration, expected_duration)

    def test_duration_with_no_end_time(self):
        # Test the duration property when end_time is not set and the simulation is inactive
        self.simulation_data.is_active = False
        self.simulation_data.end_time = None
        self.simulation_data.save()
        duration = self.simulation_data.duration
        self.assertEqual(duration, timedelta(seconds=0))
