from django.contrib.auth.models import User, AnonymousUser
from django.http import HttpResponse
from django.test import TestCase, RequestFactory
from simulation.decorators import admin_required, user_required, team_required
from simulation.models import UserProfile, Team


# Dummy view functions to apply decorators to
@admin_required
def admin_view(request):
    return HttpResponse('Admin View')


@user_required
def user_view(request):
    return HttpResponse('User View')


@team_required
def team_view(request):
    return HttpResponse('Team View')


class DecoratorTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.admin_user = User.objects.create_user(username='admin', password='password', is_superuser=True)
        self.normal_user = User.objects.create_user(username='user', password='password')
        self.team = Team.objects.create(name="Test Team")
        self.user_profile, _ = UserProfile.objects.get_or_create(user=self.normal_user)
        self.user_profile.teams.set([self.team])
        self.team.members.set([self.user_profile])
        self.anonymous_user = AnonymousUser()

    def test_admin_required_with_admin_user(self):
        request = self.factory.get('/admin/')
        request.user = self.admin_user
        response = admin_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'Admin View')

    def test_admin_required_with_non_admin_user(self):
        request = self.factory.get('/admin/')
        request.user = self.normal_user
        response = admin_view(request)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/admin/login/', response.url)

    def test_user_required_with_authenticated_user(self):
        request = self.factory.get('/user/')
        request.user = self.normal_user
        response = user_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'User View')

    def test_user_required_with_anonymous_user(self):
        request = self.factory.get('/user/')
        request.user = self.anonymous_user
        response = user_view(request)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_team_required_with_user_in_team(self):
        request = self.factory.get('/team/')
        request.user = self.normal_user
        response = team_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'Team View')

    def test_team_required_with_user_not_in_team(self):
        self.user_profile.teams.clear()  # Remove user from all teams
        request = self.factory.get('/team/')
        request.user = self.normal_user
        response = team_view(request)
        self.assertEqual(response.status_code, 403)
        self.assertJSONEqual(response.content.decode(), {'error': 'User is not part of a team'})

    def test_team_required_with_no_user_profile(self):
        self.user_profile.delete()
        request = self.factory.get('/team/')
        request.user = self.normal_user
        response = team_view(request)
        self.assertEqual(response.status_code, 403)
        self.assertJSONEqual(response.content.decode(), {'error': 'User profile does not exist'})
