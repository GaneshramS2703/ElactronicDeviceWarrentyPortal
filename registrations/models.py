from datetime import datetime
from django.db import models
from django.contrib.auth import get_user_model
from botocore.exceptions import ClientError
import boto3

# Initialize DynamoDB resource and table
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('ProductWarrantyTable')

# Use Django's user model
User = get_user_model()

class Product(models.Model):
    # Define the fields for the Product model
    serial_number = models.CharField(max_length=100, unique=True)  # Unique product identifier
    purchase_date = models.DateField()  # Date the product was purchased
    warranty_period = models.PositiveIntegerField(help_text="Warranty period in months")  # Warranty duration
    product_name = models.CharField(max_length=100)  # Name of the product
    description = models.TextField(blank=True, null=True)  # Optional description of the product
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the user who owns the product

    def save(self, *args, **kwargs):
        """
        Override the save method to sync product data with DynamoDB.
        Adds or updates the product information in the DynamoDB table.
        """
        item = {
            'PK': f"USER#{self.user.id}",  # Partition key based on user ID
            'SK': f"PRODUCT#{self.serial_number}",  # Sort key based on product serial number
            'ProductName': self.product_name,  # Product name
            'PurchaseDate': self.purchase_date.strftime("%Y-%m-%d"),  # Purchase date in string format
            'WarrantyPeriod': self.warranty_period,  # Warranty duration in months
            'Description': self.description or "",  # Optional description
            'UserID': str(self.user.id),  # User ID as string
        }
        try:
            table.put_item(Item=item)  # Insert or update the item in DynamoDB
            print(f"Product {self.serial_number} saved to DynamoDB.")
        except ClientError as e:
            print(f"Error saving to DynamoDB: {e}")
        super().save(*args, **kwargs)  # Save the object in the Django database

    def delete(self, *args, **kwargs):
        """
        Override the delete method to sync product data with DynamoDB.
        Removes the product information from the DynamoDB table.
        """
        try:
            table.delete_item(
                Key={
                    'PK': f"USER#{self.user.id}",  # Partition key
                    'SK': f"PRODUCT#{self.serial_number}"  # Sort key
                }
            )
            print(f"Product {self.serial_number} deleted from DynamoDB.")
        except ClientError as e:
            print(f"Error deleting from DynamoDB: {e}")
        super().delete(*args, **kwargs)  # Delete the object from the Django database

    def __str__(self):
        # String representation of the product
        return f"{self.product_name} ({self.serial_number})"
