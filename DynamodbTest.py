import boto3
from boto3.dynamodb.conditions import Key
import os

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('ProductWarrantyTable')

def create_product(user_id, serial_number, product_name, purchase_date, warranty_period, description):
    """Add a new product to DynamoDB."""
    item = {
        'PK': f"USER#{user_id}",
        'SK': f"PRODUCT#{serial_number}",
        'ProductName': product_name,
        'PurchaseDate': purchase_date,
        'WarrantyPeriod': warranty_period,
        'Description': description
    }
    table.put_item(Item=item)

def get_product(user_id, serial_number):
    """Retrieve a product by serial number."""
    response = table.get_item(Key={'PK': f"USER#{user_id}", 'SK': f"PRODUCT#{serial_number}"})
    return response.get('Item')

def create_claim(serial_number, claim_id, description):
    """Add a new claim to DynamoDB."""
    item = {
        'PK': f"PRODUCT#{serial_number}",
        'SK': f"CLAIM#{claim_id}",
        'Description': description,
        'Status': 'Pending'
    }
    table.put_item(Item=item)

def get_claim(serial_number, claim_id):
    """Retrieve a claim by claim ID."""
    response = table.get_item(Key={'PK': f"PRODUCT#{serial_number}", 'SK': f"CLAIM#{claim_id}"})
    return response.get('Item')
