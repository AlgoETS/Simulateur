from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from simulation.models import Scenario

class ScenarioManagementTests(APITestCase):

    def setUp(self):
        self.scenario = Scenario.objects.create(
            name="Test Scenario",
            description="This is a test scenario.",
            backstory="Test backstory.",
            duration=30
        )
        self.create_url = reverse('create_scenario')  # Make sure this URL name matches your urls.py
        self.manage_url = reverse('manage_scenario', kwargs={'scenario_id': self.scenario.id})

    def test_create_scenario(self):
        """Test creating a scenario via POST request."""
        data = {
            'name': 'New Scenario',
            'description': 'New scenario description.',
            'backstory': 'New scenario backstory.',
            'duration': 45
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Scenario.objects.count(), 2)
        self.assertEqual(Scenario.objects.get(id=response.data['data']['id']).name, 'New Scenario')

    def test_create_scenario_invalid(self):
        """Test creating a scenario with invalid data (missing name)."""
        data = {
            'description': 'Scenario without a name.',
            'backstory': 'Backstory without a name.',
            'duration': 60
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_single_scenario(self):
        """Test retrieving a single scenario via GET request."""
        response = self.client.get(self.manage_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['name'], self.scenario.name)

    def test_get_all_scenarios(self):
        """Test retrieving all scenarios via GET request."""
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 1)
        self.assertEqual(response.data['data'][0]['name'], self.scenario.name)

    def test_update_scenario(self):
        """Test updating a scenario via PUT request."""
        data = {
            'name': 'Updated Scenario Name',
            'description': 'Updated description.',
            'duration': 60
        }
        response = self.client.put(self.manage_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.scenario.refresh_from_db()
        self.assertEqual(self.scenario.name, 'Updated Scenario Name')
        self.assertEqual(self.scenario.description, 'Updated description.')
        self.assertEqual(self.scenario.duration, 60)

    def test_delete_scenario(self):
        """Test deleting a scenario via DELETE request."""
        response = self.client.delete(self.manage_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Scenario.objects.count(), 0)
