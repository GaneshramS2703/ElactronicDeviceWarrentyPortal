from datetime import datetime, timedelta

#class to validate if a product is still under warranty based on the purchase date and warranty period in months.

class WarrantyValidator:
    def __init__(self, purchase_date, warranty_period_months):
        
        #purchase_date (str): The purchase date of the product in "YYYY-MM-DD" format.
        #warranty_period_months (int): The warranty period in months.
        
        self.purchase_date = datetime.strptime(purchase_date, "%Y-%m-%d")
        self.warranty_period_months = warranty_period_months
        
# Determine if the product is still under warranty.

    def is_under_warranty(self):
        
#Calculates the expiration date by adding the warranty period (in days)to the purchase date. 
#Compares the current date to the expiration date.

        expiration_date = self.purchase_date + timedelta(days=self.warranty_period_months * 30)
        print(f"Debug: Purchase Date: {self.purchase_date}, Expiration Date: {expiration_date}, Current Date: {datetime.now()}")
        return datetime.now() <= expiration_date
        
#class to calculate the remaining warranty period for a product based on the purchase date and warranty period in months.
class WarrantyCoverageCalculator:
    def __init__(self, purchase_date, warranty_period_months):
        
        #purchase_date (str): The purchase date of the product in "YYYY-MM-DD" format.
        #warranty_period_months (int): The warranty period in months.
        
        self.purchase_date = datetime.strptime(purchase_date, "%Y-%m-%d")
        self.warranty_period_months = warranty_period_months
        
#Calculate the remaining days in the warranty period.
    def remaining_warranty(self):
        
        #Computes the expiration date by adding the warranty period (in days)to the purchase date.
        #Determines the difference between the expiration date and the current date.
        
        expiration_date = self.purchase_date + timedelta(days=self.warranty_period_months * 30)
        remaining_days = (expiration_date - datetime.now()).days
        print(f"Debug: Purchase Date: {self.purchase_date}, Expiration Date: {expiration_date}, Remaining Days: {remaining_days}")
        return max(remaining_days, 0)
