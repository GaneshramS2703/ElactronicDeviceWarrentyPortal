import boto3
from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime

# Initialize DynamoDB table resource
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('ProductWarrantyTable')

User = get_user_model()  # Get the User model

class Product(models.Model):
    serial_number = models.CharField(max_length=100, unique=True)
    purchase_date = models.DateField()
    warranty_period = models.PositiveIntegerField(help_text="Warranty period in months")
    product_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        """Override save to store product data in DynamoDB."""
        item = {
            'PK': f"USER#{self.user.id}",
            'SK': f"PRODUCT#{self.serial_number}",
            'ProductName': self.product_name,
            'PurchaseDate': self.purchase_date.strftime("%Y-%m-%d"),
            'WarrantyPeriod': self.warranty_period,
            'Description': self.description,
            'UserID': str(self.user.id),
        }
        # Store the item in DynamoDB
        table.put_item(Item=item)
        super().save(*args, **kwargs)  # Optionally save in Django's database
