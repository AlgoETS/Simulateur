from django.contrib.auth.management.commands import createsuperuser
from django.core.management import CommandError
from django.contrib.auth import get_user_model

class Command(createsuperuser.Command):
    help = 'Create a superadmin user with a password non-interactively'

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument(
            '--password', dest='password', default=None,
            help='Specifies the password for the superuser.',
        )

    def handle(self, *args, **options):
        User = get_user_model()
        username = options.get('username')
        password = options.get('password')
        email = options.get('email')
        database = options.get('database')

        if not username:
            raise CommandError("--username is required")
        if not email:
            raise CommandError("--email is required")

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
            super(Command, self).handle(*args, **options)
            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" created successfully.'))
