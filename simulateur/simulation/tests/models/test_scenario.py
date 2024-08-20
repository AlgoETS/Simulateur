from django.test import TestCase
from simulation.models import Scenario


class ScenarioModelTest(TestCase):

    def setUp(self):
        self.scenario = Scenario.objects.create(
            name="Apocalyptic World",
            description="A scenario set in a post-apocalyptic world.",
            backstory="The world has been devastated by a global catastrophe.",
            duration=365
        )

    def tearDown(self):
        self.scenario.delete()

    def test_scenario_creation(self):
        # Test if the Scenario object was created successfully
        self.assertEqual(self.scenario.name, "Apocalyptic World")
        self.assertEqual(self.scenario.description, "A scenario set in a post-apocalyptic world.")
        self.assertEqual(self.scenario.backstory, "The world has been devastated by a global catastrophe.")
        self.assertEqual(self.scenario.duration, 365)

    def test_scenario_str_method(self):
        # Test the __str__ method of the Scenario model
        self.assertEqual(str(self.scenario), "Apocalyptic World")

    def test_scenario_default_values(self):
        # Test if the default values are set correctly
        scenario_default = Scenario.objects.create()
        self.assertEqual(scenario_default.name, "")
        self.assertEqual(scenario_default.description, "")
        self.assertEqual(scenario_default.backstory, "")
        self.assertEqual(scenario_default.duration, 0)
