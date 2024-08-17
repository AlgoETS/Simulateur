from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from simulation.models import Portfolio, SimulationManager, UserProfile, Stock, Scenario, SimulationSettings, StockPortfolio, StockPriceHistory, Company


class PortfolioModelTest(TestCase):

    def setUp(self):
        # Create a Scenario instance
        self.scenario = Scenario.objects.create(
            name="Test Scenario",
            description="A test scenario",
            backstory="This is just a test",
            duration=30
        )

        # Create SimulationSettings instance
        self.simulation_settings = SimulationSettings.objects.create()

        # Create SimulationManager instance
        self.simulation_manager = SimulationManager.objects.create(
            scenario=self.scenario,
            simulation_settings=self.simulation_settings,
        )

        # Create multiple UserProfiles with unique Users
        self.user_profile1 = self.create_or_get_user_profile("TestUser1")
        self.user_profile2 = self.create_or_get_user_profile("TestUser2")

        # Create a Portfolio instance
        self.portfolio = Portfolio.objects.create(
            owner=self.user_profile1,
            balance=Decimal("10000.00"),
            simulation_manager=self.simulation_manager
        )

        # Create a Company instance
        self.company = Company.objects.create(
            name="TestCompagny",
            backstory="This is just a test",
            sector="TestSector",
            country="TestCountry",
            industry="TestIndustry",
            timestamp=timezone.now(),
        )

        # Create a Stock instance
        self.stock = Stock.objects.create(
            company=self.company,
            ticker="TST",
            volatility=0.05,
            liquidity=1000
        )

        # Create StockPriceHistory instance
        self.price_history = StockPriceHistory.objects.create(
            stock=self.stock,
            open_price=100.00,
            high_price=110.00,
            low_price=95.00,
            close_price=105.00,
        )

        # Create a StockPortfolio instance
        self.stock_portfolio = StockPortfolio.objects.create(
            stock=self.stock,
            portfolio=self.portfolio,
            quantity=10,
            latest_price_history=self.price_history
        )

    def tearDown(self):
        try:
            self.stock_portfolio.delete()
            self.price_history.delete()
            self.stock.delete()
            self.company.delete()
            self.portfolio.delete()
            self.user_profile1.delete()
            self.user_profile2.delete()
            self.simulation_manager.delete()
            self.simulation_settings.delete()
            self.scenario.delete()
        except Exception as e:
            self.fail(f"Teardown failed: {str(e)}")

    def create_or_get_user_profile(self, username):
        """Helper function to create or get a UserProfile."""
        user, created = User.objects.get_or_create(username=username)
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        return user_profile

    def test_portfolio_creation(self):
        """Test if the Portfolio object was created successfully."""
        self.assertEqual(self.portfolio.owner, self.user_profile1)
        self.assertEqual(self.portfolio.balance, Decimal("10000.00"))
        self.assertEqual(self.portfolio.simulation_manager, self.simulation_manager)

    def test_portfolio_str_method(self):
        """Test the __str__ method of the Portfolio model."""
        self.assertEqual(str(self.portfolio), f"Portfolio for {self.user_profile1}")

    def test_portfolio_default_balance(self):
        """Test the default balance of a Portfolio."""
        portfolio_default = Portfolio.objects.create(
            owner=self.user_profile2,
            simulation_manager=self.simulation_manager
        )
        self.assertEqual(portfolio_default.balance, Decimal("0.00"))

    def test_stock_portfolio_creation(self):
        """Test if the StockPortfolio object was created successfully."""
        self.assertEqual(self.stock_portfolio.stock, self.stock)
        self.assertEqual(self.stock_portfolio.portfolio, self.portfolio)
        self.assertEqual(self.stock_portfolio.quantity, 10)
        self.assertEqual(self.stock_portfolio.latest_price_history, self.price_history)

    def test_stock_portfolio_update_latest_price(self):
        """Test the update_latest_price method of the StockPortfolio model."""
        # Create a new price history to simulate an update in price
        new_price_history = StockPriceHistory.objects.create(
            stock=self.stock,
            open_price=105.00,
            high_price=115.00,
            low_price=100.00,
            close_price=110.00,
        )

        # Update the latest price in the stock portfolio
        self.stock_portfolio.update_latest_price()

        # Check if the latest price history has been updated
        self.assertEqual(self.stock_portfolio.latest_price_history, new_price_history)

    def test_stock_portfolio_str_method(self):
        """Test the __str__ method of the StockPortfolio model."""
        self.assertEqual(str(self.stock_portfolio), f"10 of {self.stock.ticker} in {self.portfolio}")

    def test_unique_together_constraint(self):
        """Test the unique_together constraint of the StockPortfolio model."""
        with self.assertRaises(Exception):
            # Attempt to create a duplicate StockPortfolio entry
            StockPortfolio.objects.create(
                stock=self.stock,
                portfolio=self.portfolio,
                quantity=5
            )
