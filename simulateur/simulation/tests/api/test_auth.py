from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from simulation.models import Team, UserProfile

class UpdateMemberRoleTests(TestCase):

    def setUp(self):
        # Create a test user and team
        self.user = User.objects.create_user(username='testuser', password='password')
        self.user_profile, _ = UserProfile.objects.get_or_create(user=self.user)
        self.team = Team.objects.create(name='Test Team')
        self.team.members.add(self.user_profile)
        self.user_profile.teams.set([self.team])

        # Create another user to be updated
        self.target_user = User.objects.create_user(username='targetuser', password='password')
        self.target_profile, _ = UserProfile.objects.get_or_create(user=self.target_user)
        self.team.members.add(self.target_profile)
        self.target_profile.teams.set([self.team])

        # Set up the client
        self.client = APIClient()
        self.client.login(username='testuser', password='password')

    def tearDown(self):
        # Cleanup users and teams
        User.objects.all().delete()
        Team.objects.all().delete()
        UserProfile.objects.all().delete()

    def test_update_member_role_success(self):
        url = f'/api/team/update-role/{self.team.id}/{self.target_user.id}/'
        data = {'role': 'team_leader'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['message'], 'User role updated successfully')

        self.target_profile.refresh_from_db()
        self.assertEqual(self.target_profile.role, 'team_leader')

    def test_update_member_role_not_in_team(self):
        # Create a new user who is not part of the team
        new_user = User.objects.create_user(username='newuser', password='password')
        new_profile, _ = UserProfile.objects.get_or_create(user=new_user)

        url = f'/api/team/update-role/{self.team.id}/{new_user.id}/'
        data = {'role': 'team_leader'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['status'], 'error')
        self.assertEqual(response.data['message'], 'User is not a member of this team')

    def test_update_member_role_user_not_authorized(self):
        # Log out the current user and log in as a new user who is not part of the team
        self.client.logout()
        new_user = User.objects.create_user(username='newuser', password='password')
        new_profile, _ = UserProfile.objects.get_or_create(user=new_user)
        self.client.login(username='newuser', password='password')

        url = f'/api/team/update-role/{self.team.id}/{self.target_user.id}/'
        data = {'role': 'team_leader'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['status'], 'error')
        self.assertEqual(response.data['message'], 'You are not a member of this team')

    def test_update_member_role_invalid_role(self):
        url = f'/api/team/update-role/{self.team.id}/{self.target_user.id}/'
        data = {'role': 'invalid_role'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('role', response.data)
