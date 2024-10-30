from django.test import TestCase
from django.utils import timezone
from simulation.models import Simulation, Scenario, Stock, Team, Event, Trigger, News, SimulationSettings, Company


class SimulationManagerModelTest(TestCase):

    def setUp(self):
        self.company = Company.objects.create(
            name="Test Company",
            backstory="A test backstory for the company",
            sector="Technology",
            country="Test Country",
            industry="Software",
            timestamp=timezone.now()
        )

        self.scenario = Scenario.objects.create(
            name="Test Scenario",
            description="A test scenario",
            backstory="This is a test backstory",
            duration=10,
        )

        self.simulation_settings = SimulationSettings.objects.create(
        )

        # Create SimulationManager instance
        self.simulation_manager = Simulation.objects.create(
            scenario=self.scenario,
            simulation_settings=self.simulation_settings
        )

    def tearDown(self):
        self.simulation_manager.delete()
        self.simulation_settings.delete()
        self.scenario.delete()
        self.company.delete()

    def test_simulation_manager_creation(self):
        # Test if the SimulationManager object was created successfully
        self.assertEqual(self.simulation_manager.scenario, self.scenario)
        self.assertEqual(self.simulation_manager.simulation_settings, self.simulation_settings)
        self.assertEqual(self.simulation_manager.state, Simulation.ScenarioState.INITIALIZED)
        self.assertIsNotNone(self.simulation_manager.timestamp)
        self.assertIsNotNone(self.simulation_manager.published_date)

    def test_simulation_manager_state_change(self):
        # Test changing the state of the SimulationManager
        self.simulation_manager.state = Simulation.ScenarioState.ONGOING
        self.simulation_manager.save()
        self.assertEqual(self.simulation_manager.state, Simulation.ScenarioState.ONGOING)

    def test_simulation_manager_relationships(self):
        # Create necessary related objects
        company = Company.objects.create(
            name="Test Company",
            backstory="A test backstory",
            sector="Technology",
            country="Test Country",
            industry="Software",
            timestamp=timezone.now()
        )

        stock = Stock.objects.create(
            company=company,
            ticker="TEST",
            volatility=0.5,
            liquidity=100000
        )

        team = Team.objects.create(name="Test Team")

        event = Event.objects.create(
            name="Test Event",
            description="Event Description",
            type="Type",
            date=timezone.now()
        )

        trigger = Trigger.objects.create(
            name="Test Trigger",
            description="Trigger Description",
            type="Type",
            value=1.0
        )

        news = News.objects.create(
            title="Test News",
            content="News content",
            event=event
        )

        # Add related objects to SimulationManager
        self.simulation_manager.stocks.add(stock)
        self.simulation_manager.teams.add(team)
        self.simulation_manager.events.add(event)
        self.simulation_manager.triggers.add(trigger)
        self.simulation_manager.news.add(news)

        self.assertIn(stock, self.simulation_manager.stocks.all())
        self.assertIn(team, self.simulation_manager.teams.all())
        self.assertIn(event, self.simulation_manager.events.all())
        self.assertIn(trigger, self.simulation_manager.triggers.all())
        self.assertIn(news, self.simulation_manager.news.all())

    def test_simulation_manager_str_method(self):
        self.assertEqual(str(self.simulation_manager), f'Scenario Manager: {str(self.scenario.name)}')
