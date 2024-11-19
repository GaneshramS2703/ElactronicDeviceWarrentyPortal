from datetime import datetime
from django.db import models
from django.contrib.auth import get_user_model
from botocore.exceptions import ClientError
import boto3

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('ProductWarrantyTable')

User = get_user_model()

class Product(models.Model):
    serial_number = models.CharField(max_length=100, unique=True)
    purchase_date = models.DateField()
    warranty_period = models.PositiveIntegerField(help_text="Warranty period in months")
    product_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        """Save product data to DynamoDB."""
        item = {
            'PK': f"USER#{self.user.id}",
            'SK': f"PRODUCT#{self.serial_number}",
            'ProductName': self.product_name,
            'PurchaseDate': self.purchase_date.strftime("%Y-%m-%d"),
            'WarrantyPeriod': self.warranty_period,
            'Description': self.description or "",
            'UserID': str(self.user.id),
        }
        try:
            table.put_item(Item=item)
            print(f"Product {self.serial_number} saved to DynamoDB.")
        except ClientError as e:
            print(f"Error saving to DynamoDB: {e}")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Delete product data from DynamoDB."""
        try:
            table.delete_item(
                Key={
                    'PK': f"USER#{self.user.id}",
                    'SK': f"PRODUCT#{self.serial_number}"
                }
            )
            print(f"Product {self.serial_number} deleted from DynamoDB.")
        except ClientError as e:
            print(f"Error deleting from DynamoDB: {e}")
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.product_name} ({self.serial_number})"
