from django.test import TestCase
from warranty_lib.warranty import WarrantyValidator, WarrantyCoverageCalculator
from datetime import datetime, timedelta

class WarrantyLibraryTestCase(TestCase):
    def test_product_under_warranty(self):
        # Simulate a product purchased 6 months ago with a 12-month warranty
        purchase_date = (datetime.now() - timedelta(days=180)).strftime("%Y-%m-%d")
        warranty_period = 12  # months
        validator = WarrantyValidator(purchase_date, warranty_period)
        self.assertTrue(validator.is_under_warranty(), "Product should be under warranty")

    def test_warranty_expired(self):
        # Simulate a product purchased 18 months ago with a 12-month warranty
        purchase_date = (datetime.now() - timedelta(days=540)).strftime("%Y-%m-%d")
        warranty_period = 12  # months
        validator = WarrantyValidator(purchase_date, warranty_period)
        self.assertFalse(validator.is_under_warranty(), "Product warranty should be expired")

    def test_remaining_warranty(self):
        # Simulate a product purchased 6 months ago with a 12-month warranty
        purchase_date = (datetime.now() - timedelta(days=180)).strftime("%Y-%m-%d")
        warranty_period = 12  # months
        calculator = WarrantyCoverageCalculator(purchase_date, warranty_period)
        self.assertGreater(calculator.remaining_warranty(), 0, "Remaining warranty should be positive")
