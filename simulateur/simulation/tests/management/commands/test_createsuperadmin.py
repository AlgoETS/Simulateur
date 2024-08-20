from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase


class CreateSuperAdminCommandTest(TestCase):

    def setUp(self):
        self.User = get_user_model()
        self.username = 'testsuperadmin'
        self.email = 'testsuperadmin@example.com'
        self.password = 'supersecretpassword'

    def test_create_superadmin_successfully(self):
        # Test creating a superadmin with all required arguments
        call_command(
            'createsuperadmin',
            username=self.username,
            email=self.email,
            password=self.password,
            interactive=False,
        )
        user = self.User.objects.get(username=self.username)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.check_password(self.password))

    def test_create_superadmin_missing_username(self):
        # Test creating a superadmin without specifying a username
        with self.assertRaises(CommandError) as cm:
            call_command(
                'createsuperadmin',
                email=self.email,
                password=self.password,
                interactive=False,
            )
        self.assertEqual(str(cm.exception), "--username is required")

    def test_create_superadmin_missing_email(self):
        # Test creating a superadmin without specifying an email
        with self.assertRaises(CommandError) as cm:
            call_command(
                'createsuperadmin',
                username=self.username,
                password=self.password,
                interactive=False,
            )
        self.assertEqual(str(cm.exception), "--email is required")

    def test_superadmin_already_exists(self):
        # Create a superadmin first
        self.User.objects.create_superuser(
            username=self.username,
            email=self.email,
            password='oldpassword',
        )

        # Test that running the command again updates the password
        call_command(
            'createsuperadmin',
            username=self.username,
            email=self.email,
            password=self.password,
            interactive=False,
        )
        user = self.User.objects.get(username=self.username)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.check_password(self.password))
        self.assertNotEqual(user.password, 'oldpassword')

    def test_superadmin_no_password_update(self):
        # Create a superadmin first
        self.User.objects.create_superuser(
            username=self.username,
            email=self.email,
            password='oldpassword',
        )

        # Test that running the command without specifying a password doesn't update the password
        call_command(
            'createsuperadmin',
            username=self.username,
            email=self.email,
            interactive=False,
        )
        user = self.User.objects.get(username=self.username)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.check_password('oldpassword'))
