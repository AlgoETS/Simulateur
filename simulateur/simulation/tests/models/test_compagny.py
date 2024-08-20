from django.test import TestCase
from simulation.models import Company


class CompanyModelTest(TestCase):

    def setUp(self):
        self.company = Company.objects.create(
            name="TechCorp",
            backstory="A leading technology company.",
            sector="Technology",
            country="USA",
            industry="Software"
        )

    def tearDown(self):
        self.company.delete()

    def test_company_creation(self):
        # Test if the company object was created successfully
        self.assertEqual(self.company.name, "TechCorp")
        self.assertEqual(self.company.backstory, "A leading technology company.")
        self.assertEqual(self.company.sector, "Technology")
        self.assertEqual(self.company.country, "USA")
        self.assertEqual(self.company.industry, "Software")
        self.assertIsNotNone(self.company.timestamp)

    def test_company_str_method(self):
        # Test the __str__ method of the Company model
        self.assertEqual(str(self.company), "TechCorp")

    def test_company_default_values(self):
        # Test if the default values are set correctly
        company_default = Company.objects.create()
        self.assertEqual(company_default.name, "")
        self.assertEqual(company_default.backstory, "")
        self.assertEqual(company_default.sector, "")
        self.assertEqual(company_default.country, "")
        self.assertEqual(company_default.industry, "")
