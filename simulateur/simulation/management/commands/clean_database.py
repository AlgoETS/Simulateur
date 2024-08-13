# simulation/management/commands/clean_database.py
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from simulation.models import Company, Stock, Team, Event, Trigger, SimulationSettings, Scenario, Portfolio, \
    TransactionHistory, UserProfile


class Command(BaseCommand):
    help = 'Clean the database, excluding admin and staff user data'

    def handle(self, *args, **kwargs):
        self.clean_database()

    def clean_database(self):
        # Models to clean excluding User and UserProfile
        models_to_clean = [
            Company,
            Stock,
            Team,
            Event,
            Trigger,
            SimulationSettings,
            Scenario,
            Portfolio,
            TransactionHistory,
        ]

        # Clean the models
        for model_class in models_to_clean:
            try:
                model_class.objects.all().delete()
                self.stdout.write(self.style.SUCCESS(f'Successfully cleaned {model_class.__name__}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error cleaning {model_class.__name__}: {e}'))

        # Clean UserProfile while excluding profiles linked to admin or staff users
        try:
            UserProfile.objects.exclude(user__is_staff=True).delete()
            self.stdout.write(self.style.SUCCESS(f'Successfully cleaned UserProfile'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error cleaning UserProfile: {e}'))

        # Clean User while excluding superusers and staff users
        try:
            User.objects.exclude(is_superuser=True).exclude(is_staff=True).delete()
            self.stdout.write(self.style.SUCCESS(f'Successfully cleaned User'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error cleaning User: {e}'))
