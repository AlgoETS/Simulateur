import csv
import json
from datetime import datetime
import logging
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction
from simulation.models import (
    Company, Stock, Team, UserProfile, Event, Trigger, SimulationSettings,
    Scenario, Portfolio, TransactionHistory
)

class Command(BaseCommand):
    help = 'Seed the database with initial data from CSV files'

    def handle(self, *args, **kwargs):
        try:
            with transaction.atomic():
                self.seed_database()
            self.stdout.write(self.style.SUCCESS('Successfully seeded the database'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error occurred: {e}'))

    def seed_database(self):
        self.seed_users()
        self.seed_companies()
        self.seed_stocks()
        self.seed_teams()
        self.seed_events()
        self.seed_triggers()
        self.seed_simulation_settings()
        self.seed_scenarios()
        self.seed_portfolios()

    def seed_users(self):
        try:
            with open('data/users.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    user, created = User.objects.get_or_create(
                        username=row['username'],
                        defaults={
                            'email': row['email'],
                            'password': row['password']
                        }
                    )
                    UserProfile.objects.get_or_create(
                        user=user,
                        defaults={'balance': float(row['balance'])}
                    )
            self.stdout.write(self.style.SUCCESS('Seeded users'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error seeding users: {e}'))

    def seed_companies(self):
        try:
            with open('data/companies.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    Company.objects.get_or_create(
                        name=row['name'],
                        defaults={
                            'backstory': row['backstory'],
                            'sector': row['sector'],
                            'country': row['country'],
                            'industry': row['industry']
                        }
                    )
            self.stdout.write(self.style.SUCCESS('Seeded companies'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error seeding companies: {e}'))

    def seed_stocks(self):
        try:
            with open('data/stocks.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    company = Company.objects.get(name=row['company'])
                    Stock.objects.get_or_create(
                        company=company,
                        ticker=row['ticker'],
                        open_price=float(row['open_price']),
                        high_price=float(row['high_price']),
                        low_price=float(row['low_price']),
                        close_price=float(row['close_price']),
                        defaults={
                            'price': float(row['price']),
                            'partial_share': float(row['partial_share']),
                            'complete_share': int(row['complete_share'])
                        }
                    )
            self.stdout.write(self.style.SUCCESS('Seeded stocks'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error seeding stocks: {e}'))

    def seed_teams(self):
        try:
            with open('data/teams.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    team, created = Team.objects.get_or_create(
                        name=row['name'],
                    )
                    if created:
                        members = UserProfile.objects.filter(user__username__in=row['members'].split(';'))
                        team.members.set(members)
            self.stdout.write(self.style.SUCCESS('Seeded teams'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error seeding teams: {e}'))

    def seed_events(self):
        try:
            with open('data/events.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    Event.objects.get_or_create(
                        name=row['name'],
                        defaults={
                            'description': row['description'],
                            'type': row['type'],
                            'date': datetime.strptime(row['date'], '%Y-%m-%d %H:%M:%S')
                        }
                    )
            self.stdout.write(self.style.SUCCESS('Seeded events'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error seeding events: {e}'))

    def seed_triggers(self):
        try:
            with open('data/triggers.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    event_names = row['events'].split(';') if row['events'] else []
                    events = Event.objects.filter(name__in=event_names) if event_names else []
                    trigger, created = Trigger.objects.get_or_create(
                        name=row['name'],
                        defaults={
                            'description': row['description'],
                            'type': row['type'],
                            'value': float(row['value'])
                        }
                    )

                    if created:
                        trigger.events.set(events)
                        trigger.save()
            self.stdout.write(self.style.SUCCESS('Seeded triggers'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error seeding triggers: {e}'))

    def seed_simulation_settings(self):
        try:
            with open('data/simulation_settings.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    SimulationSettings.objects.get_or_create(
                        max_users=int(row['max_users']),
                        max_companies=int(row['max_companies']),
                        timer_step=int(row['timer_step']),
                        timer_step_unit=row['timer_step_unit'],
                        interval=int(row['interval']),
                        interval_unit=row['interval_unit'],
                        defaults={
                            'max_interval': int(row['max_interval']),
                            'fluctuation_rate': float(row['fluctuation_rate']),
                            'close_stock_market_at_night': row['close_stock_market_at_night'].lower() == 'true',
                            'noise_function': row['noise_function']
                        }
                    )
            self.stdout.write(self.style.SUCCESS('Seeded simulation settings'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error seeding simulation settings: {e}'))

    def seed_scenarios(self):
        try:
            with open('data/scenarios.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    simulation_settings = SimulationSettings.objects.first()
                    scenario, created = Scenario.objects.get_or_create(
                        name=row['name'],
                        defaults={
                            'description': row['description'],
                            'backstory': row['backstory'],
                            'duration': int(row['duration']),
                            'simulation_settings': simulation_settings
                        }
                    )
                    if created:
                        stocks = Stock.objects.filter(ticker__in=row['stocks'].split(';'))
                        users = UserProfile.objects.filter(user__username__in=row['users'].split(';'))
                        teams = Team.objects.filter(name__in=row['teams'].split(';'))
                        events = Event.objects.filter(name__in=row['events'].split(';'))
                        triggers = Trigger.objects.filter(name__in=row['triggers'].split(';'))
                        scenario.stocks.set(stocks)
                        scenario.users.set(users)
                        scenario.teams.set(teams)
                        scenario.events.set(events)
                        scenario.triggers.set(triggers)
            self.stdout.write(self.style.SUCCESS('Seeded scenarios'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error seeding scenarios: {e}'))

    def seed_portfolios(self):
        try:
            with open('data/portfolios.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    owner = UserProfile.objects.get(user__username=row['owner']) if row['owner'] else None
                    team_names = row['team'].split(';') if row['team'] else []
                    teams = Team.objects.filter(name__in=team_names)
                    portfolio, created = Portfolio.objects.get_or_create(
                        owner=owner
                    )
                    if created:
                        portfolio.teams.set(teams)
                        stocks = Stock.objects.filter(ticker__in=row['stocks'].split(';'))
                        portfolio.stocks.set(stocks)
                        portfolio.balance = float(row['balance'])
                        portfolio.save()
            self.stdout.write(self.style.SUCCESS('Seeded portfolios'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error seeding portfolios: {e}'))
