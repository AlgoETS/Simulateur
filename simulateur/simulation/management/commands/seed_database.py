import csv
import json
from datetime import datetime
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
        self.seed_transaction_history()

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
                    UserProfile.objects.create(
                        user=user,
                        balance=float(row['balance'])
                    )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error seeding users: {e}'))

    def seed_companies(self):
        try:
            with open('data/companies.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    Company.objects.create(
                        name=row['name'],
                        backstory=row['backstory'],
                        sector=row['sector'],
                        country=row['country'],
                        industry=row['industry']
                    )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error seeding companies: {e}'))

    def seed_stocks(self):
        try:
            with open('data/stocks.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    company = Company.objects.get(name=row['company'])
                    Stock.objects.create(
                        company=company,
                        ticker=row['ticker'],
                        price=float(row['price']),
                        partial_share=float(row['partial_share']),
                        complete_share=int(row['complete_share'])
                    )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error seeding stocks: {e}'))

    def seed_teams(self):
        try:
            with open('data/teams.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    team = Team.objects.create(
                        name=row['name'],
                        balance=float(row['balance'])
                    )
                    members = UserProfile.objects.filter(user__username__in=row['members'].split(';'))
                    team.members.set(members)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error seeding teams: {e}'))

    def seed_events(self):
        try:
            with open('data/events.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    scenario = Scenario.objects.get(name=row['scenario'])
                    Event.objects.create(
                        name=row['name'],
                        description=row['description'],
                        event_type=row['event_type'],
                        trigger_date=datetime.strptime(row['trigger_date'], '%Y-%m-%d %H:%M:%S'),
                        scenario=scenario
                    )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error seeding events: {e}'))

    def seed_triggers(self):
        try:
            with open('data/triggers.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    event = Event.objects.get(name=row['event'])
                    scenario = Scenario.objects.get(name=row['scenario'])
                    Trigger.objects.create(
                        name=row['name'],
                        description=row['description'],
                        trigger_type=row['trigger_type'],
                        trigger_value=float(row['trigger_value']),
                        event=event,
                        scenario=scenario
                    )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error seeding triggers: {e}'))

    def seed_simulation_settings(self):
        try:
            with open('data/simulation_settings.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    SimulationSettings.objects.create(
                        max_users=int(row['max_users']),
                        max_companies=int(row['max_companies']),
                        timer_step=int(row['timer_step']),
                        timer_step_unit=row['timer_step_unit'],
                        interval=int(row['interval']),
                        interval_unit=row['interval_unit'],
                        max_interval=int(row['max_interval']),
                        fluctuation_rate=float(row['fluctuation_rate']),
                        time_unit=row['time_unit'],
                        close_stock_market_at_night=row['close_stock_market_at_night'].lower() == 'true',
                        noise_function=row['noise_function']
                    )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error seeding simulation settings: {e}'))

    def seed_scenarios(self):
        try:
            with open('data/scenarios.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    simulation_settings = SimulationSettings.objects.first()  # Get the first SimulationSettings instance
                    scenario = Scenario.objects.create(
                        name=row['name'],
                        description=row['description'],
                        backstory=row['backstory'],
                        difficulty_level=row['difficulty_level'],
                        duration=int(row['duration']),
                        simulation_settings=simulation_settings
                    )
                    companies = Company.objects.filter(name__in=row['companies'].split(';'))
                    stocks = Stock.objects.filter(company__name__in=row['stocks'].split(';'))
                    users = UserProfile.objects.filter(user__username__in=row['users'].split(';'))
                    teams = Team.objects.filter(name__in=row['teams'].split(';'))
                    events = Event.objects.filter(name__in=row['events'].split(';'))
                    triggers = Trigger.objects.filter(name__in=row['triggers'].split(';'))
                    scenario.companies.set(companies)
                    scenario.stocks.set(stocks)
                    scenario.users.set(users)
                    scenario.teams.set(teams)
                    scenario.events.set(events)
                    scenario.triggers.set(triggers)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error seeding scenarios: {e}'))

    def seed_portfolios(self):
        try:
            with open('data/portfolios.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    owner = UserProfile.objects.get(user__username=row['owner']) if row['owner'] else None
                    team = Team.objects.get(name=row['team']) if row['team'] else None
                    portfolio = Portfolio.objects.create(
                        owner=owner,
                        team=team
                    )
                    stocks = Stock.objects.filter(company__name__in=row['stocks'].split(';'))
                    portfolio.stocks.set(stocks)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error seeding portfolios: {e}'))

    def seed_transaction_history(self):
        try:
            with open('data/transaction_history.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    portfolio = Portfolio.objects.get(owner__user__username=row['portfolio_owner'])
                    TransactionHistory.objects.create(
                        portfolio=portfolio,
                        asset=row['asset'],
                        transaction_type=row['transaction_type'],
                        amount=float(row['amount']),
                        price=float(row['price']),
                        date=datetime.strptime(row['date'], '%Y-%m-%d %H:%M:%S')
                    )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error seeding transaction history: {e}'))