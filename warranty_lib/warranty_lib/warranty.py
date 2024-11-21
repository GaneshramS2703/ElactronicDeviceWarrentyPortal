from datetime import datetime, timedelta

class WarrantyValidator:
    def __init__(self, purchase_date, warranty_period_months):
        self.purchase_date = datetime.strptime(purchase_date, "%Y-%m-%d")
        self.warranty_period_months = warranty_period_months

    def is_under_warranty(self):
        expiration_date = self.purchase_date + timedelta(days=self.warranty_period_months * 30)
        print(f"Debug: Purchase Date: {self.purchase_date}, Expiration Date: {expiration_date}, Current Date: {datetime.now()}")
        return datetime.now() <= expiration_date

class WarrantyCoverageCalculator:
    def __init__(self, purchase_date, warranty_period_months):
        self.purchase_date = datetime.strptime(purchase_date, "%Y-%m-%d")
        self.warranty_period_months = warranty_period_months

    def remaining_warranty(self):
        expiration_date = self.purchase_date + timedelta(days=self.warranty_period_months * 30)
        remaining_days = (expiration_date - datetime.now()).days
        print(f"Debug: Purchase Date: {self.purchase_date}, Expiration Date: {expiration_date}, Remaining Days: {remaining_days}")
        return max(remaining_days, 0)
