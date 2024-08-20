from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from simulation.models import Company

class CompanyManagementTests(APITestCase):

    def setUp(self):
        self.company = Company.objects.create(
            name="Test Company",
            backstory="This is a test backstory.",
            sector="Technology",
            country="USA",
            industry="Software"
        )
        self.create_url = reverse('create_company')  # You'll need to ensure that this URL name is correct in your urls.py
        self.manage_url = reverse('manage_company', kwargs={'company_id': self.company.id})

    def test_create_company(self):
        """Test creating a company via POST request."""
        data = {
            'name': 'New Company',
            'backstory': 'New backstory.',
            'sector': 'Healthcare',
            'country': 'Canada',
            'industry': 'Pharmaceuticals'
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Company.objects.count(), 2)
        self.assertEqual(Company.objects.get(id=response.data['data']['id']).name, 'New Company')

    def test_create_company_invalid(self):
        """Test creating a company with invalid data (missing name)."""
        data = {
            'backstory': 'No name provided.',
            'sector': 'Finance',
            'country': 'UK',
            'industry': 'Banking'
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_company(self):
        """Test updating a company via PUT request."""
        data = {
            'name': 'Updated Company Name',
            'backstory': 'Updated backstory.',
        }
        response = self.client.put(self.manage_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.company.refresh_from_db()
        self.assertEqual(self.company.name, 'Updated Company Name')
        self.assertEqual(self.company.backstory, 'Updated backstory.')

    def test_delete_company(self):
        """Test deleting a company via DELETE request."""
        response = self.client.delete(self.manage_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Company.objects.count(), 0)

    def test_get_single_company(self):
        """Test retrieving a single company via GET request."""
        response = self.client.get(self.manage_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['name'], self.company.name)

    def test_get_all_companies(self):
        """Test retrieving all companies via GET request."""
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 1)
        self.assertEqual(response.data['data'][0]['name'], self.company.name)
