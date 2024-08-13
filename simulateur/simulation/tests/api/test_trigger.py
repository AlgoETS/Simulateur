from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from simulation.models import Trigger, Event

class TriggerManagementTests(APITestCase):

    def setUp(self):
        self.create_url = reverse('create_trigger')
        self.trigger_data = {
            'name': 'Test Trigger',
            'description': 'This is a test trigger',
            'type': 'threshold',
            'value': 100.0
        }
        self.event = Event.objects.create(
            name='Test Event',
            description='This is a test event',
            date='2024-08-20T10:00:00Z'
        )
        self.trigger = Trigger.objects.create(
            name='Existing Trigger',
            description='This is an existing trigger',
            type='threshold',
            value=50.0
        )
        self.trigger.events.add(self.event)
        self.update_url = reverse('manage_trigger', kwargs={'trigger_id': self.trigger.id})

    def test_create_trigger(self):
        """Test creating a trigger via POST request."""
        self.trigger_data['events'] = [self.event.id]
        response = self.client.post(self.create_url, self.trigger_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Trigger.objects.count(), 2)
        new_trigger = Trigger.objects.get(name='Test Trigger')
        self.assertEqual(new_trigger.description, 'This is a test trigger')
        self.assertEqual(new_trigger.type, 'threshold')
        self.assertEqual(new_trigger.value, 100.0)
        self.assertIn(self.event, new_trigger.events.all())

    def test_update_trigger(self):
        """Test updating a trigger via PUT request."""
        updated_data = {
            'name': 'Updated Trigger Name',
            'description': 'Updated trigger description',
            'type': 'limit',
            'value': 200.0,
            'events': [self.event.id]
        }
        response = self.client.put(self.update_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.trigger.refresh_from_db()
        self.assertEqual(self.trigger.name, 'Updated Trigger Name')
        self.assertEqual(self.trigger.description, 'Updated trigger description')
        self.assertEqual(self.trigger.type, 'limit')
        self.assertEqual(self.trigger.value, 200.0)
        self.assertIn(self.event, self.trigger.events.all())

    def test_delete_trigger(self):
        """Test deleting a trigger via DELETE request."""
        response = self.client.delete(self.update_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Trigger.objects.count(), 0)

    def test_get_all_triggers(self):
        """Test retrieving all triggers via GET request."""
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 1)
        self.assertEqual(response.data['data'][0]['name'], 'Existing Trigger')

    def test_get_single_trigger(self):
        """Test retrieving a single trigger via GET request."""
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['name'], 'Existing Trigger')
        self.assertEqual(response.data['data']['description'], 'This is an existing trigger')
