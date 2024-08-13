from datetime import timedelta

from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from simulation.models import Team, JoinLink, UserProfile


class TeamTests(APITestCase):

    def setUp(self):
        self.client = APIClient()

        # Create a user and their profile
        self.user = User.objects.create_user(username='testuser', password='password')
        self.user_profile, _ = UserProfile.objects.get_or_create(user=self.user)

        # Authenticate the user
        self.client.force_authenticate(user=self.user)

        # Create a team and add the user to it
        self.team = Team.objects.create(name='Test Team')
        self.team.members.add(self.user_profile)
        self.user_profile.teams.add(self.team)
        self.user_profile.save()
        self.team.save()

        # Create a join link
        self.join_link = JoinLink.objects.create(
            team=self.team,
            key='testkey123',
            expires_at=timezone.now() + timedelta(days=1)
        )

    def test_join_team_valid_link(self):
        url = reverse('join_team', kwargs={'team_id': self.team.id, 'key': self.join_link.key})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_join_team_invalid_link(self):
        url = reverse('join_team', kwargs={'team_id': self.team.id, 'key': 'invalidkey'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_join_team_link_expired(self):
        self.join_link.expires_at = timezone.now() - timedelta(days=1)
        self.join_link.save()

        url = reverse('join_team', kwargs={'team_id': self.team.id, 'key': self.join_link.key})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_remove_team_member(self):
        # Add another user to the team
        other_user = User.objects.create_user(username='otheruser', password='password')
        other_user_profile = UserProfile.objects.create(user=other_user)
        self.team.members.add(other_user_profile)

        url = reverse('remove_team_member', kwargs={'team_id': self.team.id, 'user_id': other_user.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(self.team.members.filter(id=other_user_profile.id).exists())

    def test_remove_team_member_not_in_team(self):
        other_user = User.objects.create_user(username='otheruser', password='password')
        other_user_profile = UserProfile.objects.create(user=other_user)

        url = reverse('remove_team_member', kwargs={'team_id': self.team.id, 'user_id': other_user.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_team_name(self):
        url = reverse('update_team_name', kwargs={'team_id': self.team.id})
        data = {'name': 'New Team Name'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.team.refresh_from_db()
        self.assertEqual(self.team.name, 'New Team Name')

    def test_generate_join_link(self):
        url = reverse('generate_join_link', kwargs={'team_id': self.team.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('join_link', response.data)

    def test_generate_join_link_not_in_team(self):
        other_team = Team.objects.create(name='Other Team')
        url = reverse('generate_join_link', kwargs={'team_id': other_team.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def tearDown(self):
        User.objects.all().delete()
        UserProfile.objects.all().delete()
        Team.objects.all().delete()
        JoinLink.objects.all().delete()
