import boto3
from django.db import models
from registrations.models import Product
from datetime import datetime

# Initialize DynamoDB table resource
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('ProductWarrantyTable')

class Claim(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    claim_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')],
        default='Pending'
    )
    description = models.TextField()

    def save(self, *args, **kwargs):
        """Override save to store claim data in DynamoDB."""
        item = {
            'PK': f"PRODUCT#{self.product.serial_number}",
            'SK': f"CLAIM#{self.claim_date.strftime('%Y-%m-%d %H:%M:%S')}",
            'Status': self.status,
            'Description': self.description,
            'ClaimDate': self.claim_date.strftime('%Y-%m-%d %H:%M:%S'),
        }
        table.put_item(Item=item)
        super().save(*args, **kwargs)  # Optionally save in Django's database
