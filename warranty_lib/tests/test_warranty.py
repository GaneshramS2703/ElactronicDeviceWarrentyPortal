import unittest
from datetime import date
from warranty_lib.warranty import WarrantyValidator, WarrantyCoverageCalculator

class TestWarrantyValidator(unittest.TestCase):
    def test_calculate_expiration_date(self):
        validator = WarrantyValidator(date(2023, 1, 15), 12)
        self.assertEqual(validator.calculate_expiration_date(), date(2024, 1, 15))

    def test_is_valid(self):
        validator = WarrantyValidator(date(2023, 1, 15), 12)
        self.assertTrue(validator.is_valid(date(2023, 12, 31)))
        self.assertFalse(validator.is_valid(date(2025, 1, 1)))

class TestWarrantyCoverageCalculator(unittest.TestCase):
    def test_remaining_coverage(self):
        calculator = WarrantyCoverageCalculator(date(2023, 1, 15), 12)
        self.assertEqual(calculator.remaining_coverage(date(2023, 6, 15)), 214)  # Example: Days left

if __name__ == "__main__":
    unittest.main()
