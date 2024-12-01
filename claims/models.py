import boto3
from django.db import models
from registrations.models import Product
from botocore.exceptions import ClientError

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
claims_table = dynamodb.Table('ClaimsTable')

#Django model representing a warranty claim for a product.
class Claim(models.Model):
     # Links the claim to a specific product. If the product is deleted, associated claims are also removed.
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # Automatically sets the claim's creation date and time.
    claim_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')],
        default='Pending'
    )
    description = models.TextField()
    
#Override save to store claim data in DynamoDB."""
def save(self, *args, **kwargs):
        """Override save method to store claim data in DynamoDB."""
        # Define the structure of the DynamoDB item for the claim
        item = {
            'PK': f"PRODUCT#{self.product.serial_number}",  # Partition key links the claim to a specific product
            'SK': f"CLAIM#{self.claim_date.strftime('%Y-%m-%d %H:%M:%S')}",  # Sort key for ordering claims
            'Status': self.status,  # Status of the claim
            'Description': self.description,  # Detailed description of the claim
            'ClaimDate': self.claim_date.strftime('%Y-%m-%d %H:%M:%S'),  # Date and time of the claim
        }

        # Attempt to save the claim data to DynamoDB
        try:
            claims_table.put_item(Item=item)
            print(f"Claim for product {self.product.serial_number} saved to DynamoDB.")
        except ClientError as e:
            print(f"Error saving claim to DynamoDB: {e}")

        # Call the parent class's save method to persist data in the Django database
        super().save(*args, **kwargs)