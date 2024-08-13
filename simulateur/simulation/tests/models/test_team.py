from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from simulation.models import Team, JoinLink, UserProfile
from django.contrib.auth.models import User

class TeamModelTest(TestCase):

    def setUp(self):
        # Create a User and UserProfile
        self.user = User.objects.create_user(username='testuser', password='password')
        self.user_profile = UserProfile.objects.create(user=self.user)

        # Create a Team instance
        self.team = Team.objects.create(name="Test Team")
        self.team.members.add(self.user_profile)

    def test_team_creation(self):
        # Test if the Team object was created successfully
        self.assertEqual(self.team.name, "Test Team")
        self.assertIn(self.user_profile, self.team.members.all())

    def test_team_str_method(self):
        # Test the __str__ method of Team
        self.assertEqual(str(self.team), "Test Team")

    def test_generate_join_link(self):
        # Test the generate_join_link method
        join_link = self.team.generate_join_link()
        self.assertEqual(join_link.team, self.team)
        self.assertEqual(len(join_link.key), 32)
        self.assertTrue(timezone.now() < join_link.expires_at)
        self.assertTrue(timezone.now() + timedelta(hours=24) - join_link.expires_at < timedelta(seconds=1))

class JoinLinkModelTest(TestCase):

    def setUp(self):
        # Create a Team instance
        self.team = Team.objects.create(name="Test Team")

        # Create a JoinLink instance
        self.join_link = JoinLink.objects.create(
            team=self.team,
            key="testkey123456789012345678901234567890",
            expires_at=timezone.now() + timedelta(hours=24)
        )

    def test_join_link_creation(self):
        # Test if the JoinLink object was created successfully
        self.assertEqual(self.join_link.team, self.team)
        self.assertEqual(self.join_link.key, "testkey123456789012345678901234567890")
        self.assertTrue(timezone.now() < self.join_link.expires_at)

    def test_join_link_str_method(self):
        # Test the __str__ method of JoinLink (if it exists)
        self.assertEqual(str(self.join_link), f"Join link for {self.team.name}")

    def test_is_expired(self):
        # Test the is_expired method when the link is not expired
        self.assertFalse(self.join_link.is_expired())

        # Test the is_expired method when the link is expired
        self.join_link.expires_at = timezone.now() - timedelta(hours=1)
        self.join_link.save()
        self.assertTrue(self.join_link.is_expired())

    def test_get_absolute_url(self):
        # Test the get_absolute_url method
        expected_url = reverse('join_team', kwargs={'team_id': self.team.id, 'key': self.join_link.key})
        self.assertEqual(self.join_link.get_absolute_url(), expected_url)
