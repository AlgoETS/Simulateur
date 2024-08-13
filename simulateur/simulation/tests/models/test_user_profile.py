from django.test import TestCase
from django.contrib.auth.models import User
from simulation.models import UserProfile, Team

class UserProfileModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.team = Team.objects.create(name="Test Team")
        # Ensure only one UserProfile is created
        self.user_profile, created = UserProfile.objects.get_or_create(user=self.user)
        # Add the team to the user's profile
        self.user_profile.teams.add(self.team)

    def tearDown(self):
        self.user.delete()
        self.team.delete()
        self.user_profile.delete()

    def test_user_profile_creation(self):
        self.assertEqual(self.user_profile.user, self.user)
        self.assertIn(self.team, self.user_profile.teams.all())  # Check if the team is correctly associated
        self.assertEqual(self.user_profile.role, 'member')
        self.assertIsNotNone(self.user_profile.timestamp)
        self.assertFalse(self.user_profile.avatar)  # Check if the avatar field is empty

    def test_user_profile_str_method(self):
        self.assertEqual(str(self.user_profile), self.user.username)

    def test_user_profile_default_role(self):
        new_user = User.objects.create_user(username='newuser', password='password')
        user_profile_default_role, created = UserProfile.objects.get_or_create(
            user=new_user
        )
        user_profile_default_role.teams.add(self.team)  # Add the team to the new user's profile
        self.assertEqual(user_profile_default_role.role, 'member')

    def test_user_profile_with_avatar(self):
        new_user = User.objects.create_user(username='avataruser', password='password')
        user_profile_with_avatar, created = UserProfile.objects.get_or_create(
            user=new_user
        )
        user_profile_with_avatar.avatar = 'avatars/test_avatar.png'
        user_profile_with_avatar.save()  # Save the profile with the avatar
        self.assertEqual(str(user_profile_with_avatar.avatar), 'avatars/test_avatar.png')

    def test_user_profile_team_relationship(self):
        # Ensure the user profile is associated with the team
        self.assertIn(self.user_profile, self.team.user_profiles.all())
