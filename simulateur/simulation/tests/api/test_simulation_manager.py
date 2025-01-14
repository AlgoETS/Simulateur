from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from simulation.models import SimulationManager, Scenario, Stock, Team, Event, Trigger, News, SimulationSettings, Company
class SimulationManagerBaseTest(APITestCase):
    def setUp(self):
        # Create a company
        self.company = Company.objects.create(name="Test Company")

        # Create a scenario
        self.scenario = Scenario.objects.create(
            name="Test Scenario",
            description="This is a test scenario.",
            backstory="Test backstory.",
            duration=30
        )

        # Create related entities
        self.stock = Stock.objects.create(ticker="TEST", company=self.company)
        self.team = Team.objects.create(name="Test Team")
        self.event = Event.objects.create(name="Test Event", description="Test event", type="Test", date="2024-08-15T10:00:00Z")
        self.trigger = Trigger.objects.create(name="Test Trigger", description="Test trigger", type="Test", value=1.0)
        self.news = News.objects.create(title="Test News", content="Test content", published_date="2024-08-15T10:00:00Z")
        self.simulation_settings = SimulationSettings.objects.create()

        # Create URLs
        self.create_url = reverse('create_simulation_manager')
        self.simulation_manager = SimulationManager.objects.create(
            scenario=self.scenario,
            simulation_settings=self.simulation_settings,
            state=SimulationManager.ScenarioState.INITIALIZED
        )
        self.manage_url = reverse('manage_simulation_manager', kwargs={'simulation_manager_id': self.simulation_manager.id})
        self.change_state_url = reverse('change_state', kwargs={'simulation_manager_id': self.simulation_manager.id})

class CreateSimulationManagerTests(SimulationManagerBaseTest):
    def test_create_simulation_manager(self):
        """Test creating a scenario manager via POST request."""
        data = {
            'scenario_id': self.scenario.id,
            'stocks': [self.stock.id],
            'teams': [self.team.id],
            'events': [self.event.id],
            'triggers': [self.trigger.id],
            'news': [self.news.id],
            'simulation_settings': {
                "timer_step": 10,
                "timer_step_unit": "second",
                "interval": 20,
                "interval_unit": "second",
                "max_interval": 3000,
                "fluctuation_rate": 0.1,
                "close_stock_market_at_night": True,
                "noise_function": "brownian",
                "stock_trading_logic": "static"
            },
            'state': SimulationManager.ScenarioState.INITIALIZED
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SimulationManager.objects.count(), 2)
        self.assertEqual(SimulationManager.objects.get(id=response.data['data']['id']).scenario.name, 'Test Scenario')

class UpdateSimulationManagerTests(SimulationManagerBaseTest):
    def test_update_simulation_manager(self):
        """Test updating a scenario manager via PUT request."""
        data = {
            'stocks': [self.stock.id],
            'teams': [self.team.id],
            'events': [self.event.id],
            'triggers': [self.trigger.id],
            'news': [self.news.id],
            'state': SimulationManager.ScenarioState.CREATED
        }
        response = self.client.put(self.manage_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.simulation_manager.refresh_from_db()
        self.assertEqual(self.simulation_manager.state, SimulationManager.ScenarioState.CREATED)

class DeleteSimulationManagerTests(SimulationManagerBaseTest):
    def test_delete_simulation_manager(self):
        """Test deleting a scenario manager via DELETE request."""
        response = self.client.delete(self.manage_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(SimulationManager.objects.count(), 0)

class RetrieveSimulationManagerTests(SimulationManagerBaseTest):
    def test_get_single_simulation_manager(self):
        """Test retrieving a single scenario manager via GET request."""
        response = self.client.get(self.manage_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['scenario'], self.simulation_manager.scenario.name)

    def test_get_all_simulation_managers(self):
        """Test retrieving all scenario managers via GET request."""
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 1)
        self.assertEqual(response.data['data'][0]['scenario'], self.simulation_manager.scenario.name)

class ChangeSimulationManagerStateTests(SimulationManagerBaseTest):
    def test_valid_state_transition(self):
        """Test a valid state transition from INITIALIZED to CREATED."""
        data = {'new_state': SimulationManager.ScenarioState.CREATED}
        response = self.client.post(self.change_state_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.simulation_manager.refresh_from_db()
        self.assertEqual(self.simulation_manager.state, SimulationManager.ScenarioState.CREATED)

    def test_invalid_state_transition(self):
        """Test an invalid state transition from INITIALIZED to PUBLISHED."""
        data = {'new_state': SimulationManager.ScenarioState.PUBLISHED}
        response = self.client.post(self.change_state_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.simulation_manager.refresh_from_db()
        self.assertEqual(self.simulation_manager.state, SimulationManager.ScenarioState.INITIALIZED)
