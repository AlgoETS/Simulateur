from django.test import TestCase
from simulation.models import Stock, StockPriceHistory, Company


class StockModelTest(TestCase):

    def setUp(self):
        self.company = Company.objects.create(
            name="Test Company",
            backstory="Test backstory",
            sector="Technology",
            country="USA",
            industry="Software"
        )

        # Create a Stock instance
        self.stock = Stock.objects.create(
            company=self.company,
            ticker="TEST",
            volatility=0.5,
            liquidity=1.0
        )

    def tearDown(self):
        self.company.delete()
        self.stock.delete()

    def test_stock_creation(self):
        # Test if the Stock object was created successfully
        self.assertEqual(self.stock.company, self.company)
        self.assertEqual(self.stock.ticker, "TEST")
        self.assertEqual(self.stock.volatility, 0.5)
        self.assertEqual(self.stock.liquidity, 1.0)
        self.assertIsNotNone(self.stock.timestamp)

    def test_stock_str_method(self):
        # Test the __str__ method of Stock
        self.assertEqual(str(self.stock), "Test Company Stock")


class StockPriceHistoryModelTest(TestCase):

    def setUp(self):
        # Create a Company instance
        self.company = Company.objects.create(
            name="Test Company",
            backstory="Test backstory",
            sector="Technology",
            country="USA",
            industry="Software"
        )

        # Create a Stock instance
        self.stock = Stock.objects.create(
            company=self.company,
            ticker="TEST",
            volatility=0.5,
            liquidity=1.0
        )

        # Create a StockPriceHistory instance
        self.stock_price_history = StockPriceHistory.objects.create(
            stock=self.stock,
            open_price=100.0,
            high_price=105.0,
            low_price=95.0,
            close_price=102.0,
            volatility=0.4,
            liquidity=0.8
        )

    def test_stock_price_history_creation(self):
        # Test if the StockPriceHistory object was created successfully
        self.assertEqual(self.stock_price_history.stock, self.stock)
        self.assertEqual(self.stock_price_history.open_price, 100.0)
        self.assertEqual(self.stock_price_history.high_price, 105.0)
        self.assertEqual(self.stock_price_history.low_price, 95.0)
        self.assertEqual(self.stock_price_history.close_price, 102.0)
        self.assertEqual(self.stock_price_history.volatility, 0.4)
        self.assertEqual(self.stock_price_history.liquidity, 0.8)
        self.assertIsNotNone(self.stock_price_history.timestamp)

    def test_stock_price_history_str_method(self):
        # Test the __str__ method of StockPriceHistory
        expected_str = f"Test Company Price at {self.stock_price_history.timestamp}"
        self.assertEqual(str(self.stock_price_history), expected_str)
