from boto3.dynamodb.conditions import Key
import boto3
from botocore.exceptions import ClientError


# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('ProductWarrantyTable')

def get_product(user_id, serial_number):
    """Retrieve a product from DynamoDB by user ID and serial number."""
    try:
        response = table.get_item(
            Key={
                'PK': f"USER#{user_id}",
                'SK': f"PRODUCT#{serial_number}"
            }
        )
        print(f"Debug: DynamoDB response for USER#{user_id}, PRODUCT#{serial_number}: {response}")
        return response.get('Item', None)  # Return None if the product is not found
    except Exception as e:
        print(f"Error retrieving product: {e}")
        return None



def get_claims_for_product(serial_number):
    """Retrieve all claims for a given product."""
    try:
        response = table.query(
            KeyConditionExpression=Key('PK').eq(f"PRODUCT#{serial_number}") &
                                   Key('SK').begins_with("CLAIM#")
        )
        return response['Items']
    except Exception as e:
        print(f"Debug: Retrieved claims: {response['Items']}")

        return []

def delete_product_dynamodb(user_id, serial_number):
    """Delete a product from DynamoDB."""
    try:
        table.delete_item(
            Key={
                'PK': f"USER#{user_id}",
                'SK': f"PRODUCT#{serial_number}"
            }
        )
        print(f"Debug: Successfully deleted USER#{user_id}, PRODUCT#{serial_number}")
    except Exception as e:
        print(f"Error deleting product: {e}")
        raise



def get_item(pk, sk):
    """Retrieve a generic item from DynamoDB by PK and SK."""
    try:
        response = table.get_item(Key={'PK': pk, 'SK': sk})
        return response.get('Item', None)
    except Exception as e:
        print(f"Error retrieving item: {e}")
        return None

        
def save_product(user_id, serial_number, product_name, purchase_date, warranty_period):
    """
    Save a new product to DynamoDB.
    Args:
        user_id (str): The ID of the user.
        serial_number (str): The serial number of the product.
        product_name (str): The name of the product.
        purchase_date (str): The date of purchase.
        warranty_period (int): The warranty period in months.
    """
    table.put_item(
        Item={
            'PK': f"USER#{user_id}",
            'SK': f"PRODUCT#{serial_number}",
            'ProductName': product_name,
            'PurchaseDate': purchase_date,
            'WarrantyPeriod': warranty_period
        }
    )

def get_user_products(user_id):
    """Retrieve all products for a user."""
    try:
        response = table.query(
            KeyConditionExpression=Key('PK').eq(f"USER#{user_id}") & Key('SK').begins_with("PRODUCT")
        )
        products = response['Items']
        # Debug to ensure FileKey is included
        for product in products:
            print(f"Debug: Retrieved product with FileKey: {product.get('FileKey')}")
        return products
    except Exception as e:
        print(f"Error retrieving products: {e}")
        return []


def put_item(PK, SK, description, status):
    """Save a claim to DynamoDB."""
    table.put_item(
        Item={
            'PK': PK,
            'SK': SK,
            'Description': description,  # Note case-sensitive 'Description'
            'Status': status  # Note case-sensitive 'Status'
        }
    )






def delete_item(PK, SK):
    """Delete an item from DynamoDB based on its primary and sort keys."""
    try:
        response = table.delete_item(
            Key={
                'PK': PK,
                'SK': SK
            }
        )
        print(f"Debug: Deleted item with PK={PK}, SK={SK}, Response: {response}")
    except ClientError as e:
        print(f"Error deleting item: {e}")
        raise

def save_product_with_file(user_id, serial_number, product_name, purchase_date, warranty_period, file_key):
    """Save a product to DynamoDB with an associated file."""
    table.put_item(
        Item={
            'PK': f"USER#{user_id}",
            'SK': f"PRODUCT#{serial_number}",
            'ProductName': product_name,
            'PurchaseDate': purchase_date,
            'WarrantyPeriod': warranty_period,
            'FileKey': file_key  # Save the S3 file key
        }
    )
