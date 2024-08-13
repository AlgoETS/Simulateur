from django.contrib.auth.models import User
from django.test import TestCase
from simulation.models import TransactionHistory, Order, ScenarioManager, Stock, UserProfile, Company, Scenario, \
    SimulationSettings


class OrderModelTest(TestCase):

    def setUp(self):
        # Create a Company and Stock instance
        self.company = Company.objects.create(
            name="Test Company",
            backstory="Test backstory",
            sector="Technology",
            country="USA",
            industry="Software"
        )
        self.stock = Stock.objects.create(
            company=self.company,
            ticker="TEST",
            volatility=0.5,
            liquidity=1.0
        )

        # Create a User and UserProfile
        self.user = User.objects.create_user(username='testuser', password='password')
        self.user_profile, created = UserProfile.objects.get_or_create(user=self.user)

        # Create an Order instance
        self.order = Order.objects.create(
            user=self.user_profile,
            stock=self.stock,
            quantity=10,
            price=100.0,
            transaction_type='BUY'
        )

    def tearDown(self):
        self.order.delete()
        self.company.delete()
        self.stock.delete()
        self.user.delete()
        self.user_profile.delete()

    def test_order_creation(self):
        # Test if the Order object was created successfully
        self.assertEqual(self.order.user, self.user_profile)
        self.assertEqual(self.order.stock, self.stock)
        self.assertEqual(self.order.quantity, 10)
        self.assertEqual(self.order.price, 100.0)
        self.assertEqual(self.order.transaction_type, 'BUY')
        self.assertIsNotNone(self.order.timestamp)

    def test_order_str_method(self):
        # Test the __str__ method of Order
        self.assertEqual(str(self.order), f'Order for {self.stock.ticker} by {self.user.username}')


class TransactionHistoryModelTest(TestCase):

    def setUp(self):
        # Create a Company and Stock instance
        self.company = Company.objects.create(
            name="Test Company",
            backstory="Test backstory",
            sector="Technology",
            country="USA",
            industry="Software"
        )
        self.stock = Stock.objects.create(
            company=self.company,
            ticker="TEST",
            volatility=0.5,
            liquidity=1.0
        )

        # Create a User and UserProfile
        self.user = User.objects.create_user(username='testuser', password='password')
        self.user_profile, created = UserProfile.objects.get_or_create(user=self.user)

        # Create an Order instance
        self.order = Order.objects.create(
            user=self.user_profile,
            stock=self.stock,
            quantity=10,
            price=100.0,
            transaction_type='BUY'
        )

        # Create a Scenario and ScenarioManager instance
        self.scenario = Scenario.objects.create(
            name="Test Scenario",
            description="A test scenario",
            backstory="Test backstory",
            duration=10,
        )

        self.scenario_manager = ScenarioManager.objects.create(
            scenario=self.scenario,
            simulation_settings=SimulationSettings.objects.create(),
        )

        # Create a TransactionHistory instance and add the Order
        self.transaction_history = TransactionHistory.objects.create(
            scenario_manager=self.scenario_manager
        )
        self.transaction_history.orders.add(self.order)

    def tearDown(self):
        self.scenario_manager.delete()
        self.company.delete()
        self.stock.delete()
        self.user.delete()
        self.user_profile.delete()
        self.order.delete()
        self.scenario.delete()

    def test_transaction_history_creation(self):
        # Test if the TransactionHistory object was created successfully
        self.assertEqual(self.transaction_history.scenario_manager, self.scenario_manager)
        self.assertIn(self.order, self.transaction_history.orders.all())

    def test_transaction_history_str_method(self):
        # Test the __str__ method of TransactionHistory
        self.assertEqual(str(self.transaction_history), f'Transaction for {self.order.stock.ticker}')
