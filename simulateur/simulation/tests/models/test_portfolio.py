from django.test import TestCase
from django.core.exceptions import ValidationError
from decimal import Decimal
from simulation.models import Portfolio, StockPortfolio, ScenarioManager, UserProfile, Stock


class PortfolioModelTest(TestCase):

    def setUp(self):
        # Create necessary related objects
        self.scenario_manager = ScenarioManager.objects.create(
            scenario_name="Test Scenario"  # Assuming ScenarioManager has a scenario_name field
        )
        self.user_profile = UserProfile.objects.create(
            user_name="TestUser"  # Assuming UserProfile has a user_name field
        )

        # Create a Portfolio instance
        self.portfolio = Portfolio.objects.create(
            owner=self.user_profile,
            balance=Decimal("10000.00"),
            scenario_manager=self.scenario_manager
        )

    def test_portfolio_creation(self):
        # Test if the Portfolio object was created successfully
        self.assertEqual(self.portfolio.owner, self.user_profile)
        self.assertEqual(self.portfolio.balance, Decimal("10000.00"))
        self.assertEqual(self.portfolio.scenario_manager, self.scenario_manager)

    def test_portfolio_str_method(self):
        # Test the __str__ method of the Portfolio model
        self.assertEqual(str(self.portfolio), f"Portfolio for {self.user_profile}")

    def test_portfolio_default_balance(self):
        # Test that the default balance is correctly set
        portfolio_default = Portfolio.objects.create(
            owner=self.user_profile,
            scenario_manager=self.scenario_manager
        )
        self.assertEqual(portfolio_default.balance, Decimal("0.00"))


class StockPortfolioModelTest(TestCase):

    def setUp(self):
        # Create necessary related objects
        self.scenario_manager = ScenarioManager.objects.create(
            scenario_name="Test Scenario"
        )
        self.user_profile = UserProfile.objects.create(
            user_name="TestUser"
        )
        self.portfolio = Portfolio.objects.create(
            owner=self.user_profile,
            balance=Decimal("10000.00"),
            scenario_manager=self.scenario_manager
        )
        self.stock = Stock.objects.create(
            company_name="Test Company",  # Assuming Stock has a company_name field
            ticker="TC"
        )

        # Create a StockPortfolio instance
        self.stock_portfolio = StockPortfolio.objects.create(
            stock=self.stock,
            portfolio=self.portfolio,
            quantity=50
        )

    def test_stock_portfolio_creation(self):
        # Test if the StockPortfolio object was created successfully
        self.assertEqual(self.stock_portfolio.stock, self.stock)
        self.assertEqual(self.stock_portfolio.portfolio, self.portfolio)
        self.assertEqual(self.stock_portfolio.quantity, 50)

    def test_unique_together_constraint(self):
        # Test the unique_together constraint
        with self.assertRaises(ValidationError):
            StockPortfolio.objects.create(
                stock=self.stock,
                portfolio=self.portfolio,
                quantity=100
            )

    def test_stock_portfolio_default_quantity(self):
        # Test that the default quantity is correctly set
        stock_portfolio_default = StockPortfolio.objects.create(
            stock=self.stock,
            portfolio=self.portfolio
        )
        self.assertEqual(stock_portfolio_default.quantity, 0)
