from django.test import TestCase
from django.contrib.auth.models import User
from simulation.models import UserProfile, Team


class UserProfileModelTest(TestCase):

    def setUp(self):
        # Create a User instance
        self.user = User.objects.create_user(username='testuser', password='password')

        # Create a Team instance
        self.team = Team.objects.create(name="Test Team")

        # Create a UserProfile instance
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            team=self.team,
            role='member'
        )

    def test_user_profile_creation(self):
        # Test if the UserProfile object was created successfully
        self.assertEqual(self.user_profile.user, self.user)
        self.assertEqual(self.user_profile.team, self.team)
        self.assertEqual(self.user_profile.role, 'member')
        self.assertIsNotNone(self.user_profile.timestamp)
        self.assertIsNone(self.user_profile.avatar)  # Avatar should be None by default

    def test_user_profile_str_method(self):
        # Test the __str__ method of UserProfile
        self.assertEqual(str(self.user_profile), self.user.username)

    def test_user_profile_default_role(self):
        # Test the default role of the UserProfile
        user_profile_default_role = UserProfile.objects.create(
            user=self.user,
            team=self.team
        )
        self.assertEqual(user_profile_default_role.role, 'member')

    def test_user_profile_with_avatar(self):
        # Test creating a UserProfile with an avatar
        user_profile_with_avatar = UserProfile.objects.create(
            user=self.user,
            team=self.team,
            avatar='avatars/test_avatar.png'
        )
        self.assertEqual(user_profile_with_avatar.avatar, 'avatars/test_avatar.png')

    def test_user_profile_team_relationship(self):
        # Test the relationship between UserProfile and Team
        self.assertIn(self.user_profile, self.team.user_profiles.all())
