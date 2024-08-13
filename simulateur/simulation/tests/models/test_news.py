from datetime import datetime

from django.test import TestCase
from simulation.models import News, Event


class NewsModelTest(TestCase):

    def setUp(self):
        # Create an Event instance that will be linked to the News instance
        self.event = Event.objects.create(
            name="Annual Conference",
            description="A conference on technology and innovation.",
            type="Conference",
            date=datetime(2024, 12, 25, 10, 0, 0)
        )

        # Create a News instance linked to the Event
        self.news = News.objects.create(
            title="Tech Conference Announced",
            content="The annual tech conference will be held in December.",
            event=self.event
        )

    def tearDown(self):
        self.news.delete()

    def test_news_creation(self):
        # Test if the News object was created successfully
        self.assertEqual(self.news.title, "Tech Conference Announced")
        self.assertEqual(self.news.content, "The annual tech conference will be held in December.")
        self.assertEqual(self.news.event, self.event)
        self.assertIsNotNone(self.news.published_date)

    def test_news_str_method(self):
        # Test the __str__ method of the News model
        self.assertEqual(str(self.news), "Tech Conference Announced")

    def test_news_related_event(self):
        # Test if the related event is correctly associated with the news item
        self.assertEqual(self.news.event.name, "Annual Conference")
        self.assertIn(self.news, self.event.news_items.all())

    def test_news_default_values(self):
        # Test if the default values are set correctly
        news_default = News.objects.create(event=self.event)
        self.assertEqual(news_default.title, "")
        self.assertEqual(news_default.content, "")
        self.assertIsNotNone(news_default.published_date)
