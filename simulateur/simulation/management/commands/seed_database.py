import csv
from datetime import datetime
import pytz
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction, IntegrityError
from django.utils.timezone import make_aware
from simulation.models import (
    Company, Stock, Team, UserProfile, Event, Trigger, SimulationSettings,
    Scenario, Portfolio, TransactionHistory, Order, SimulationManager,
    StockPortfolio, StockPriceHistory, News, JoinLink
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
        self.seed_events()
        self.seed_triggers()
        self.seed_simulation_settings()
        self.seed_scenarios()
        self.seed_simulation_manager()
        self.seed_teams()
        self.seed_portfolios()
        self.seed_orders()
        self.seed_stock_price_history()
        self.seed_stock_portfolios()
        self.seed_news()
        self.seed_join_links()
        self.seed_transactions()

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
                    if created:
                        UserProfile.objects.get_or_create(
                            user=user,
                            defaults={'role': 'member'}
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
                        defaults={
                            'volatility': float(row['volatility']),
                            'liquidity': float(row['liquidity'])
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
                    naive_datetime = datetime.strptime(row['date'], '%Y-%m-%d %H:%M:%S')
                    aware_datetime = make_aware(naive_datetime, timezone=pytz.UTC)
                    Event.objects.get_or_create(
                        name=row['name'],
                        defaults={
                            'description': row['description'],
                            'type': row['type'],
                            'date': aware_datetime
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
                        timer_step=int(row['timer_step']),
                        timer_step_unit=row['timer_step_unit'],
                        interval=int(row['interval']),
                        interval_unit=row['interval_unit'],
                        max_interval=int(row['max_interval']),
                        fluctuation_rate=float(row['fluctuation_rate']),
                        close_stock_market_at_night=row['close_stock_market_at_night'].lower() == 'true',
                        noise_function=row['noise_function'],
                        stock_trading_logic=row['stock_trading_logic']
                    )
            self.stdout.write(self.style.SUCCESS('Seeded simulation settings'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error seeding simulation settings: {e}'))

    def seed_scenarios(self):
        try:
            with open('data/scenarios.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    Scenario.objects.get_or_create(
                        name=row['name'],
                        defaults={
                            'description': row['description'],
                            'backstory': row['backstory'],
                            'duration': int(row['duration'])
                        }
                    )
            self.stdout.write(self.style.SUCCESS('Seeded scenarios'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error seeding scenarios: {e}'))

    def seed_portfolios(self):
        try:
            with open('data/portfolios.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    try:
                        owner = UserProfile.objects.get(user__username=row['owner'])
                        simulation_manager = SimulationManager.objects.get(id=row['simulation_manager'])

                        Portfolio.objects.get_or_create(
                            owner=owner,
                            simulation_manager=simulation_manager,
                            defaults={'balance': float(row['balance'])}
                        )
                    except UserProfile.DoesNotExist:
                        self.stdout.write(self.style.ERROR(f"UserProfile for owner {row['owner']} does not exist"))
                    except SimulationManager.DoesNotExist:
                        self.stdout.write(
                            self.style.ERROR(f"SimulationManager with id {row['simulation_manager']} does not exist"))
                    except IntegrityError as e:
                        self.stdout.write(self.style.ERROR(f"Error seeding portfolios: {e}"))
                self.stdout.write(self.style.SUCCESS('Seeded portfolios'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error seeding portfolios: {e}'))

    def seed_orders(self):
        try:
            with open('data/orders.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    try:
                        user_profile = UserProfile.objects.get(user__username=row['user'])
                        stock = Stock.objects.get(ticker=row['stock'])
                        naive_datetime = datetime.strptime(row['timestamp'], '%Y-%m-%d %H:%M:%S')
                        aware_datetime = make_aware(naive_datetime, timezone=pytz.UTC)

                        Order.objects.create(
                            user=user_profile,
                            stock=stock,
                            quantity=int(row['quantity']),
                            price=float(row['price']),
                            transaction_type=row['transaction_type'],
                            timestamp=aware_datetime
                        )
                    except UserProfile.DoesNotExist:
                        self.stdout.write(self.style.ERROR(f"UserProfile {row['user']} does not exist"))
                    except Stock.DoesNotExist:
                        self.stdout.write(self.style.ERROR(f"Stock {row['stock']} does not exist"))
                self.stdout.write(self.style.SUCCESS('Seeded orders'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error seeding orders: {e}'))

    def seed_transactions(self):
        try:
            with open('data/transaction_histories.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    try:
                        order_ids = row['orders'].split(';')
                        orders = Order.objects.filter(id__in=order_ids)
                        simulation_manager = SimulationManager.objects.get(id=row['simulation_manager'])

                        if not orders.exists():
                            self.stdout.write(self.style.ERROR(
                                f"No valid orders found for simulation_manager {row['simulation_manager']}"
                            ))
                            continue

                        # Validate all stocks and events
                        missing_stocks = []
                        for order in orders:
                            if not Stock.objects.filter(id=order.stock.id).exists():
                                missing_stocks.append(order.stock.ticker)

                        if missing_stocks:
                            self.stdout.write(self.style.ERROR(
                                f"Stock(s) {', '.join(missing_stocks)} do not exist for orders {row['orders']}"
                            ))
                            continue

                        # Create the transaction history
                        transaction_history = TransactionHistory.objects.create(simulation_manager=simulation_manager)
                        transaction_history.orders.set(orders)
                        transaction_history.save()

                    except SimulationManager.DoesNotExist:
                        self.stdout.write(self.style.ERROR(f"SimulationManager {row['simulation_manager']} does not exist"))
                    except Stock.DoesNotExist:
                        self.stdout.write(self.style.ERROR(
                            f"Stock matching query does not exist for one of the orders in {row['orders']}"
                        ))
                    except Event.DoesNotExist:
                        self.stdout.write(self.style.ERROR(
                            f"Event matching query does not exist for one of the transactions"
                        ))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'Error seeding transactions: {e}'))
            self.stdout.write(self.style.SUCCESS('Seeded transactions'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error seeding transactions: {e}'))

    def seed_simulation_manager(self):
        try:
            with open('data/simulation_manager.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    try:
                        # Retrieve related objects by name
                        scenario = Scenario.objects.get(name=row['scenario'])

                        # Fetch SimulationSettings by id
                        simulation_settings = SimulationSettings.objects.get(id=row['simulation_settings'])

                        simulation_manager, created = SimulationManager.objects.get_or_create(
                            scenario=scenario,
                            simulation_settings=simulation_settings,
                            state=row['state']
                        )

                        if created:
                            # Fetch related objects using names
                            stocks = Stock.objects.filter(ticker__in=row['stocks'].split(';'))
                            teams = Team.objects.filter(name__in=row['teams'].split(';'))
                            events = Event.objects.filter(name__in=row['events'].split(';'))
                            triggers = Trigger.objects.filter(name__in=row['triggers'].split(';'))
                            news = News.objects.filter(title__in=row['news'].split(';'))

                            # Assign related objects
                            simulation_manager.stocks.set(stocks)
                            simulation_manager.teams.set(teams)
                            simulation_manager.events.set(events)
                            simulation_manager.triggers.set(triggers)
                            simulation_manager.news.set(news)
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'Error seeding simulation manager: {e}'))
            self.stdout.write(self.style.SUCCESS('Seeded simulation manager'))
        except Scenario.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Scenario {row['scenario']} does not exist"))
        except SimulationSettings.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"SimulationSettings {row['simulation_settings']} does not exist"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error seeding simulation manager: {e}'))

    def seed_stock_portfolios(self):
        try:
            with open('data/stock_portfolios.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    try:
                        portfolio = Portfolio.objects.get(id=row['portfolio'])
                        stock = Stock.objects.get(ticker=row['stock'])
                        StockPortfolio.objects.get_or_create(
                            portfolio=portfolio,
                            stock=stock,
                            defaults={
                                'quantity': int(row['quantity']),
                                'latest_price_history': StockPriceHistory.objects.get(id=row['latest_price_history'])
                            }
                        )
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'Error seeding transactions: {e}'))
            self.stdout.write(self.style.SUCCESS('Seeded stock portfolios'))
        except Portfolio.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Portfolio {row['portfolio']} does not exist"))
        except Stock.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Stock {row['stock']} does not exist"))
        except StockPriceHistory.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"StockPriceHistory {row['latest_price_history']} does not exist"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error seeding stock portfolios: {e}'))

    def seed_stock_price_history(self):
        try:
            with open('data/stock_price_history.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    stock = Stock.objects.get(ticker=row['stock'])
                    timestamp = make_aware(datetime.strptime(row['timestamp'], '%Y-%m-%d %H:%M:%S'), timezone=pytz.UTC)
                    StockPriceHistory.objects.get_or_create(
                        stock=stock,
                        timestamp=timestamp,
                        defaults={
                            'open_price': float(row['open_price']),
                            'high_price': float(row['high_price']),
                            'low_price': float(row['low_price']),
                            'close_price': float(row['close_price']),
                            'volatility': float(row['volatility']),
                            'liquidity': float(row['liquidity'])
                        }
                    )
            self.stdout.write(self.style.SUCCESS('Seeded stock price history'))
        except Stock.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Stock {row['stock']} does not exist"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error seeding stock price history: {e}'))

    def seed_news(self):
        try:
            with open('data/news.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    try:
                        naive_datetime = datetime.strptime(row['published_date'], '%Y-%m-%d %H:%M:%S')
                        aware_datetime = make_aware(naive_datetime, timezone=pytz.UTC)
                        event = Event.objects.get(name=row['event']) if row['event'] else None
                        News.objects.get_or_create(
                            title=row['title'],
                            defaults={
                                'content': row['content'],
                                'event': event,
                                'published_date': aware_datetime
                            }
                        )
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'Error seeding transactions: {e}'))
            self.stdout.write(self.style.SUCCESS('Seeded news'))
        except Event.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Event {row['event']} does not exist"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error seeding news: {e}'))

    def seed_join_links(self):
        try:
            with open('data/join_links.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    try:
                        team = Team.objects.get(name=row['team'])
                        JoinLink.objects.get_or_create(
                            team=team,
                            key=row['key'],
                            defaults={
                                'created_at': make_aware(datetime.strptime(row['created_at'], '%Y-%m-%d %H:%M:%S'), timezone=pytz.UTC),
                                'expires_at': make_aware(datetime.strptime(row['expires_at'], '%Y-%m-%d %H:%M:%S'), timezone=pytz.UTC)
                            }
                        )
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'Error seeding transactions: {e}'))
            self.stdout.write(self.style.SUCCESS('Seeded join links'))
        except Team.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Team {row['team']} does not exist"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error seeding join links: {e}'))
