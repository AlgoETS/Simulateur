from django.test import TestCase
from simulation.models import SimulationData, Scenario, SimulationSettings, ScenarioManager


class SimulationDataModelTest(TestCase):

    def setUp(self):
        # Create necessary related objects
        self.scenario = Scenario.objects.create(
            name="Test Scenario",
            description="A test scenario",
            backstory="This is a test backstory",
            duration=10
        )

        self.simulation_settings = SimulationSettings.objects.create()  # Adjust based on actual fields in SimulationSettings

        # Create a SimulationData instance without scenario_manager
        self.simulation_data = SimulationData.objects.create(
            is_active=True,
            price_changes=[],
            transactions=[]
        )

        # Create ScenarioManager instance
        self.scenario_manager = ScenarioManager.objects.create(
            scenario=self.scenario,
            simulation_settings=self.simulation_settings,
            simulation_data=self.simulation_data
        )

    def tearDown(self):
        self.scenario.delete()
        self.simulation_settings.delete()
        self.simulation_data.delete()
        self.scenario_manager.delete()

    def test_simulation_data_creation(self):
        # Test if the SimulationData object was created successfully
        self.assertTrue(self.simulation_data.is_active)
        self.assertEqual(self.simulation_data.price_changes, [])
        self.assertEqual(self.simulation_data.transactions, [])
        self.assertIsNotNone(self.simulation_data.start_time)
        self.assertIsNone(self.simulation_data.end_time)
