from io import StringIO
from unittest.mock import patch, mock_open

from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase
from simulation.models import Company, Stock, UserProfile, Event, Team, Trigger, SimulationSettings, Scenario, \
    Portfolio, TransactionHistory, UserProfile


class SeedDatabaseCommandTest(TestCase):

    def setUp(self):
        self.out = StringIO()

    def test_seed_users_success(self):
        mock_csv_data = StringIO("""username,email,password,balance
        testuser1,testuser1@example.com,password1,1000.00
        testuser2,testuser2@example.com,password2,1500.00
        """)
        with patch('builtins.open', mock_open(read_data=mock_csv_data.getvalue())), \
                patch('sys.stdout', new=self.out):
            call_command('seed_database')
            self.assertIn('Seeded users', self.out.getvalue())
            self.assertEqual(UserProfile.objects.count(), 2)

    def test_seed_companies_success(self):
        mock_csv_data = StringIO("""name,backstory,sector,country,industry
        TestCompany,This is a test company,Tech,USA,Software
        """)
        with patch('builtins.open', mock_open(read_data=mock_csv_data.getvalue())), \
                patch('sys.stdout', new=self.out):
            call_command('seed_database')
            self.assertIn('Seeded companies', self.out.getvalue())
            self.assertEqual(Company.objects.count(), 1)

    def test_seed_stocks_success(self):
        # Prepare data
        company = Company.objects.create(name="TestCompany", backstory="Backstory", sector="Tech", country="USA",
                                         industry="Software")

        mock_csv_data = StringIO(f"""company,ticker,open_price,high_price,low_price,close_price,price,partial_share,complete_share
        {company.name},TST,100.0,110.0,90.0,105.0,105.0,0.5,100
        """)
        with patch('builtins.open', mock_open(read_data=mock_csv_data.getvalue())), \
                patch('sys.stdout', new=self.out):
            call_command('seed_database')
            self.assertIn('Seeded stocks', self.out.getvalue())
            self.assertEqual(Stock.objects.count(), 1)

    def test_seed_users_file_not_found(self):
        with patch('builtins.open', side_effect=FileNotFoundError), \
                patch('sys.stdout', new=self.out):
            with self.assertRaises(FileNotFoundError):
                call_command('seed_database')
            self.assertIn('Error seeding users', self.out.getvalue())

    def test_seed_database_with_transaction(self):
        mock_csv_data = StringIO("""username,email,password,balance
        testuser1,testuser1@example.com,password1,1000.00
        """)
        with patch('builtins.open', mock_open(read_data=mock_csv_data.getvalue())), \
                patch('sys.stdout', new=self.out), \
                patch('simulation.management.commands.seed_database.Command.seed_companies',
                      side_effect=Exception("Test Error")):
            with self.assertRaises(Exception):
                call_command('seed_database')
            self.assertEqual(UserProfile.objects.count(), 0)  # Ensure no data was committed due to the exception

    def test_seed_scenarios_with_simulation_settings(self):
        # Prepare SimulationSettings data
        SimulationSettings.objects.create(
            timer_step=10,
            timer_step_unit='minute',
            interval=20,
            interval_unit='minute',
            max_interval=3000,
            fluctuation_rate=0.1,
            close_stock_market_at_night=True,
            noise_function='brownian',
        )

        mock_csv_data = StringIO("""name,description,backstory,duration,stocks,users,teams,events,triggers
        Test Scenario,This is a test scenario,Backstory,60,,,
        """)
        with patch('builtins.open', mock_open(read_data=mock_csv_data.getvalue())), \
                patch('sys.stdout', new=self.out):
            call_command('seed_database')
            self.assertIn('Seeded scenarios', self.out.getvalue())
            self.assertEqual(Scenario.objects.count(), 1)

    def test_seed_events_success(self):
        mock_csv_data = StringIO("""name,description,type,date
        Test Event,This is a test event,Test,2024-08-13 12:00:00
        """)
        with patch('builtins.open', mock_open(read_data=mock_csv_data.getvalue())), \
                patch('sys.stdout', new=self.out):
            call_command('seed_database')
            self.assertIn('Seeded events', self.out.getvalue())
            self.assertEqual(Event.objects.count(), 1)

    def test_seed_teams_success(self):
        mock_csv_data = StringIO("""name,members
        Test Team,testuser1;testuser2
        """)
        user1 = User.objects.create_user(username='testuser1', password='password')
        user2 = User.objects.create_user(username='testuser2', password='password')
        UserProfile.objects.create(user=user1)
        UserProfile.objects.create(user=user2)

        with patch('builtins.open', mock_open(read_data=mock_csv_data.getvalue())), \
                patch('sys.stdout', new=self.out):
            call_command('seed_database')
            self.assertIn('Seeded teams', self.out.getvalue())
            self.assertEqual(Team.objects.count(), 1)
            self.assertEqual(Team.objects.first().members.count(), 2)

    def test_seed_triggers_success(self):
        # Create event that will be linked to the trigger
        Event.objects.create(name='Test Event', description='Description', type='Test', date='2024-08-13 12:00:00')

        mock_csv_data = StringIO("""name,description,type,value,events
        Test Trigger,This is a test trigger,price,100.0,Test Event
        """)
        with patch('builtins.open', mock_open(read_data=mock_csv_data.getvalue())), \
                patch('sys.stdout', new=self.out):
            call_command('seed_database')
            self.assertIn('Seeded triggers', self.out.getvalue())
            self.assertEqual(Trigger.objects.count(), 1)
            self.assertEqual(Trigger.objects.first().events.count(), 1)

    def test_seed_simulation_settings_success(self):
        mock_csv_data = StringIO("""timer_step,timer_step_unit,interval,interval_unit,max_interval,fluctuation_rate,close_stock_market_at_night,noise_function,stock_trading_logic
        10,minute,20,minute,3000,0.1,True,brownian,static
        """)
        with patch('builtins.open', mock_open(read_data=mock_csv_data.getvalue())), \
                patch('sys.stdout', new=self.out):
            call_command('seed_database')
            self.assertIn('Seeded simulation settings', self.out.getvalue())
            self.assertEqual(SimulationSettings.objects.count(), 1)
            self.assertEqual(SimulationSettings.objects.first().timer_step, 10)

    def test_seed_portfolios_success(self):
        # Prepare data
        user = User.objects.create_user(username='testuser1', password='password')
        user_profile = UserProfile.objects.create(user=user)
        team = Team.objects.create(name='Test Team')
        stock = Stock.objects.create(
            company=Company.objects.create(name="TestCompany", backstory="Backstory", sector="Tech", country="USA",
                                           industry="Software"),
            ticker='TST', open_price=100.0, high_price=110.0, low_price=90.0, close_price=105.0,
        )

        mock_csv_data = StringIO(f"""owner,team,stocks,balance
        testuser1,{team.name},{stock.ticker},1000.0
        """)

        with patch('builtins.open', mock_open(read_data=mock_csv_data.getvalue())), \
                patch('sys.stdout', new=self.out):
            call_command('seed_database')
            self.assertIn('Seeded portfolios', self.out.getvalue())
            self.assertEqual(Portfolio.objects.count(), 1)
            self.assertEqual(Portfolio.objects.first().balance, 1000.0)
            self.assertEqual(Portfolio.objects.first().stocks.count(), 1)

    def test_seed_orders_success(self):
        # Prepare data
        user = User.objects.create_user(username='testuser1', password='password')
        user_profile = UserProfile.objects.create(user=user)
        stock = Stock.objects.create(
            company=Company.objects.create(name="TestCompany", backstory="Backstory", sector="Tech", country="USA",
                                           industry="Software"),
            ticker='TST', open_price=100.0, high_price=110.0, low_price=90.0, close_price=105.0,
        )

        mock_csv_data = StringIO(f"""user,stock,quantity,price,transaction_type,timestamp
        testuser1,TST,10,100.0,BUY,2024-08-13 12:00:00
        """)

        with patch('builtins.open', mock_open(read_data=mock_csv_data.getvalue())), \
                patch('sys.stdout', new=self.out):
            call_command('seed_database')
            self.assertIn('Seeded orders', self.out.getvalue())
            self.assertEqual(TransactionHistory.objects.count(), 1)
            self.assertEqual(TransactionHistory.objects.first().orders.count(), 1)

    def test_seed_transactions_success(self):
        # Prepare data
        scenario = Scenario.objects.create(
            name='Test Scenario', description='This is a test scenario', backstory='Backstory', duration=60,
            simulation_settings=SimulationSettings.objects.create(timer_step=10, timer_step_unit='minute', interval=20,
                                                                  interval_unit='minute')
        )
        order = TransactionHistory.objects.create(scenario=scenario)

        mock_csv_data = StringIO(f"""orders,scenario
        {order.id},Test Scenario
        """)

        with patch('builtins.open', mock_open(read_data=mock_csv_data.getvalue())), \
                patch('sys.stdout', new=self.out):
            call_command('seed_database')
            self.assertIn('Seeded transactions', self.out.getvalue())
            self.assertEqual(TransactionHistory.objects.count(), 1)
