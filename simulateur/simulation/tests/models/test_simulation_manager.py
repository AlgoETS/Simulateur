from django.test import TestCase
from django.utils import timezone
from simulation.models import ScenarioManager, Scenario, Stock, Team, Event, Trigger, News, SimulationSettings, Company


class ScenarioManagerModelTest(TestCase):

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

        # Create ScenarioManager instance
        self.scenario_manager = ScenarioManager.objects.create(
            scenario=self.scenario,
            simulation_settings=self.simulation_settings
        )

    def tearDown(self):
        self.scenario_manager.delete()
        self.simulation_settings.delete()
        self.scenario.delete()
        self.company.delete()

    def test_scenario_manager_creation(self):
        # Test if the ScenarioManager object was created successfully
        self.assertEqual(self.scenario_manager.scenario, self.scenario)
        self.assertEqual(self.scenario_manager.simulation_settings, self.simulation_settings)
        self.assertEqual(self.scenario_manager.state, ScenarioManager.ScenarioState.INITIALIZED)
        self.assertIsNotNone(self.scenario_manager.timestamp)
        self.assertIsNotNone(self.scenario_manager.published_date)

    def test_scenario_manager_state_change(self):
        # Test changing the state of the ScenarioManager
        self.scenario_manager.state = ScenarioManager.ScenarioState.ONGOING
        self.scenario_manager.save()
        self.assertEqual(self.scenario_manager.state, ScenarioManager.ScenarioState.ONGOING)

    def test_scenario_manager_relationships(self):
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

        # Add related objects to ScenarioManager
        self.scenario_manager.stocks.add(stock)
        self.scenario_manager.teams.add(team)
        self.scenario_manager.events.add(event)
        self.scenario_manager.triggers.add(trigger)
        self.scenario_manager.news.add(news)

        self.assertIn(stock, self.scenario_manager.stocks.all())
        self.assertIn(team, self.scenario_manager.teams.all())
        self.assertIn(event, self.scenario_manager.events.all())
        self.assertIn(trigger, self.scenario_manager.triggers.all())
        self.assertIn(news, self.scenario_manager.news.all())

    def test_scenario_manager_str_method(self):
        self.assertEqual(str(self.scenario_manager), f'Scenario Manager: {str(self.scenario.name)}')
