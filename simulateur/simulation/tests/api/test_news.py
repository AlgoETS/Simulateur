from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from simulation.models import News

class NewsManagementTests(APITestCase):

    def setUp(self):
        self.news = News.objects.create(
            title="Initial News",
            content="Initial content",
            published_date="2024-08-20T10:00:00Z"
        )
        self.create_url = reverse('create_news')
        self.manage_url = reverse('manage_news', kwargs={'news_id': self.news.id})

    def test_create_news(self):
        """Test creating a news item via POST request."""
        data = {
            'title': 'New News',
            'content': 'New content for the news',
            'published_date': '2024-08-21T10:00:00Z'
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(News.objects.count(), 2)
        self.assertEqual(News.objects.get(id=response.data['data']['id']).title, 'New News')

    def test_create_news_invalid(self):
        """Test creating a news item with invalid data."""
        data = {
            'content': 'Content without a title',
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_news(self):
        """Test updating a news item via PUT request."""
        data = {
            'title': 'Updated Title',
            'content': 'Updated content'
        }
        response = self.client.put(self.manage_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.news.refresh_from_db()
        self.assertEqual(self.news.title, 'Updated Title')
        self.assertEqual(self.news.content, 'Updated content')

    def test_delete_news(self):
        """Test deleting a news item via DELETE request."""
        response = self.client.delete(self.manage_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(News.objects.count(), 0)

    def test_get_single_news(self):
        """Test retrieving a single news item via GET request."""
        response = self.client.get(self.manage_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['title'], self.news.title)

    def test_get_all_news(self):
        """Test retrieving all news items via GET request."""
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 1)
        self.assertEqual(response.data['data'][0]['title'], self.news.title)
