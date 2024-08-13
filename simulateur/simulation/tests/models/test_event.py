from django.test import TestCase
from simulation.models import Event
from datetime import datetime

class EventModelTest(TestCase):

    def setUp(self):
        # Create an Event instance that will be used in the tests
        self.event = Event.objects.create(
            name="Tech Summit",
            description="An annual summit discussing the latest in technology.",
            type="Summit",
            date=datetime(2024, 11, 15, 9, 0, 0)
        )

    def tearDown(self):
        self.event.delete()

    def test_event_creation(self):
        # Test if the Event object was created successfully
        self.assertEqual(self.event.name, "Tech Summit")
        self.assertEqual(self.event.description, "An annual summit discussing the latest in technology.")
        self.assertEqual(self.event.type, "Summit")
        self.assertEqual(self.event.date, datetime(2024, 11, 15, 9, 0, 0))
        self.assertIsNotNone(self.event.timestamp)

    def test_event_str_method(self):
        # Test the __str__ method of the Event model
        self.assertEqual(str(self.event), "Tech Summit")

    def test_event_default_values(self):
        # Test if the default values are set correctly
        event_default = Event.objects.create(date=datetime(2024, 11, 15, 9, 0, 0))
        self.assertEqual(event_default.name, "")
        self.assertEqual(event_default.description, "")
        self.assertEqual(event_default.type, "")
        self.assertEqual(event_default.date, datetime(2024, 11, 15, 9, 0, 0))
        self.assertIsNotNone(event_default.timestamp)
