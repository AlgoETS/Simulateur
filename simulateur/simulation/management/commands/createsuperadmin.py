from django.contrib.auth.management.commands.createsuperuser import Command as CreateSuperUserCommand
from django.core.management import CommandError
from django.contrib.auth import get_user_model
from simulation.models import UserProfile


class Command(CreateSuperUserCommand):
    help = 'Create a superadmin user with a password non-interactively'

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            '--password',
            dest='password',
            default=None,
            help='Specifies the password for the superuser.',
        )

    def handle(self, *args, **options):
        User = get_user_model()
        username = options.get('username')
        password = options.get('password')
        email = options.get('email')
        database = options.get('database')

        if not username:
            raise CommandError("--username is required.")
        if not email:
            raise CommandError("--email is required.")
        if not password:
            raise CommandError("--password is required.")

        try:
            user = User.objects.filter(username=username).first()

            if user:
                self.stdout.write(self.style.WARNING(f'Superuser "{username}" already exists.'))
                if password:
                    user.set_password(password)
                    user.save()
                    self.stdout.write(self.style.SUCCESS(f'Password for superuser "{username}" was updated successfully.'))
            else:
                options['interactive'] = False
                options['email'] = email
                super().handle(*args, **options)

                user = User.objects.get(username=username)
                user.set_password(password)
                user.save()

                # Create associated UserProfile
                user_profile, created = UserProfile.objects.get_or_create(user=user)
                if created:
                    user_profile.save()
                    self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" created successfully along with the UserProfile.'))
                else:
                    self.stdout.write(self.style.WARNING(f'UserProfile for "{username}" already exists.'))

        except CommandError as e:
            raise CommandError(f"Error creating superuser: {e}")
        except Exception as e:
            raise CommandError(f"An unexpected error occurred: {str(e)}")
