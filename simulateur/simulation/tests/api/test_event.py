from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from simulation.models import Event

class EventManagementTests(APITestCase):

    def setUp(self):
        self.create_url = reverse('create_event')
        self.event_data = {
            'name': 'Test Event',
            'description': 'This is a test event',
            'date': '2024-08-20T10:00:00Z'
        }
        self.event = Event.objects.create(
            name='Existing Event',
            description='This is an existing event',
            date='2024-08-15T10:00:00Z'
        )
        self.update_url = reverse('manage_event', kwargs={'event_id': self.event.id})

    def test_create_event(self):
        """Test creating an event via POST request."""
        response = self.client.post(self.create_url, self.event_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(), 2)  # Check that a new event was created
        new_event = Event.objects.get(name='Test Event')
        self.assertEqual(new_event.description, 'This is a test event')
        self.assertEqual(new_event.date.isoformat(), '2024-08-20T10:00:00+00:00')

    def test_update_event(self):
        """Test updating an event via PUT request."""
        updated_data = {
            'name': 'Updated Event Name',
            'description': 'Updated description',
            'date': '2024-08-22T10:00:00Z'
        }
        response = self.client.put(self.update_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.event.refresh_from_db()
        self.assertEqual(self.event.name, 'Updated Event Name')
        self.assertEqual(self.event.description, 'Updated description')
        self.assertEqual(self.event.date.isoformat(), '2024-08-22T10:00:00+00:00')

    def test_delete_event(self):
        """Test deleting an event via DELETE request."""
        response = self.client.delete(self.update_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Event.objects.count(), 0)  # Check that the event was deleted

    def test_get_all_events(self):
        """Test retrieving all events via GET request."""
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 1)
        self.assertEqual(response.data['data'][0]['name'], 'Existing Event')

