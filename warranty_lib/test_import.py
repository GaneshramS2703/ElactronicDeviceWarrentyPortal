from warranty_lib import WarrantyValidator, WarrantyCoverageCalculator

# Create an instance of WarrantyValidator
validator = WarrantyValidator(purchase_date="2023-01-01", warranty_period_months=12)

# Check if the product is under warranty
print("Is under warranty:", validator.is_under_warranty())

# Create an instance of WarrantyCoverageCalculator
calculator = WarrantyCoverageCalculator(purchase_date="2023-01-01", warranty_period_months=12)

# Get the remaining warranty
print("Remaining warranty:", calculator.remaining_warranty(), "days")
