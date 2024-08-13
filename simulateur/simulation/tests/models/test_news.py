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

    def tearDown(self):
        News.objects.all().delete()
        Event.objects.all().delete()

    def test_news_creation_with_event(self):
        # Create a News instance linked to the Event
        news = News.objects.create(
            title="Tech Conference Announced",
            content="The annual tech conference will be held in December.",
            event=self.event
        )

        # Test if the News object was created successfully with an event
        self.assertEqual(news.title, "Tech Conference Announced")
        self.assertEqual(news.content, "The annual tech conference will be held in December.")
        self.assertEqual(news.event, self.event)
        self.assertIsNotNone(news.published_date)

    def test_news_creation_without_event(self):
        # Create a News instance without linking to an Event
        news = News.objects.create(
            title="Breaking News",
            content="A major update has occurred.",
            event=None
        )

        # Test if the News object was created successfully without an event
        self.assertEqual(news.title, "Breaking News")
        self.assertEqual(news.content, "A major update has occurred.")
        self.assertIsNone(news.event)
        self.assertIsNotNone(news.published_date)

    def test_news_str_method(self):
        # Create a News instance
        news = News.objects.create(
            title="Tech Conference Announced",
            content="The annual tech conference will be held in December.",
            event=self.event
        )

        # Test the __str__ method of the News model
        self.assertEqual(str(news), "Tech Conference Announced")

    def test_news_related_event(self):
        # Create a News instance linked to the Event
        news = News.objects.create(
            title="Tech Conference Announced",
            content="The annual tech conference will be held in December.",
            event=self.event
        )

        # Test if the related event is correctly associated with the news item
        self.assertEqual(news.event.name, "Annual Conference")
        self.assertIn(news, self.event.news_items.all())

    def test_news_default_values(self):
        # Test if the default values are set correctly
        news_default = News.objects.create(event=self.event)
        self.assertEqual(news_default.title, "")
        self.assertEqual(news_default.content, "")
        self.assertIsNotNone(news_default.published_date)
