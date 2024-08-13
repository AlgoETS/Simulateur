from django.test import TestCase
from simulation.models import Trigger, Event

class TriggerModelTest(TestCase):

    def setUp(self):
        # Create Event instances
        self.event1 = Event.objects.create(
            name="Event 1",
            description="First Event",
            type="Type A",
            date="2024-11-15 09:00:00"
        )
        self.event2 = Event.objects.create(
            name="Event 2",
            description="Second Event",
            type="Type B",
            date="2024-12-25 10:00:00"
        )

        # Create a Trigger instance
        self.trigger = Trigger.objects.create(
            name="Test Trigger",
            description="This is a test trigger",
            type="Threshold",
            value=50.0
        )

        # Add events to the Trigger instance
        self.trigger.events.add(self.event1, self.event2)

    def test_trigger_creation(self):
        # Test if the Trigger object was created successfully
        self.assertEqual(self.trigger.name, "Test Trigger")
        self.assertEqual(self.trigger.description, "This is a test trigger")
        self.assertEqual(self.trigger.type, "Threshold")
        self.assertEqual(self.trigger.value, 50.0)
        self.assertIsNotNone(self.trigger.timestamp)

    def test_trigger_events_relationship(self):
        # Test the many-to-many relationship with Event
        self.assertIn(self.event1, self.trigger.events.all())
        self.assertIn(self.event2, self.trigger.events.all())

    def test_trigger_str_method(self):
        # Test the __str__ method of Trigger
        self.assertEqual(str(self.trigger), "Test Trigger")
