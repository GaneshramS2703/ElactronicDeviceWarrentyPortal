from boto3.dynamodb.conditions import Key
import boto3
from botocore.exceptions import ClientError


# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('ProductWarrantyTable')

#Retrieve a product from DynamoDB by user ID and serial number.
def get_product(user_id, serial_number):
    
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


#Retrieve all claims for a given product.
def get_claims_for_product(serial_number):
   
    try:
        response = table.query(
            KeyConditionExpression=Key('PK').eq(f"PRODUCT#{serial_number}") &
                                   Key('SK').begins_with("CLAIM#")
        )
        return response['Items']
    except Exception as e:
        print(f"Debug: Retrieved claims: {response['Items']}")

        return []
        
#Delete a product from DynamoDB.
def delete_product_dynamodb(user_id, serial_number):
    
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


#Retrieve a generic item from DynamoDB by primary and sort keys.
def get_item(pk, sk):
    """Retrieve a generic item from DynamoDB by PK and SK."""
    try:
        response = table.get_item(Key={'PK': pk, 'SK': sk})
        return response.get('Item', None)
    except Exception as e:
        print(f"Error retrieving item: {e}")
        return None

#Save a new product to DynamoDB.        
def save_product(user_id, serial_number, product_name, purchase_date, warranty_period):
    
    table.put_item(
        Item={
            'PK': f"USER#{user_id}",
            'SK': f"PRODUCT#{serial_number}",
            'ProductName': product_name,
            'PurchaseDate': purchase_date,
            'WarrantyPeriod': warranty_period
        }
    )
    
#Retrieve all products for a user.
def get_user_products(user_id):
    
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

#Save a claim to DynamoDB."""
def put_item(PK, SK, description, status, user_email):
    
    table.put_item(
        Item={
            'PK': PK,
            'SK': SK,
            'Description': description,  # Note case-sensitive 'Description'
            'Status': status,  # Note case-sensitive 'Status'
            'user_email': user_email
        }
    )

#Delete an item from DynamoDB by primary and sort keys
def delete_item(PK, SK):

    try:
        print(f"Debug: Attempting to delete item with PK={PK} and SK={SK}")
        response = table.delete_item(
            Key={
                'PK': PK,
                'SK': SK
            },
            ReturnValues='ALL_OLD'
        )
        if 'Attributes' in response:
            print("Debug: Item deleted successfully.")
        else:
            print("Debug: Item not found for deletion.")
    except Exception as e:
        print(f"Debug: Error deleting item - {e}")
        raise


#Save a product to DynamoDB with an associated S3 file key.
def save_product_with_file(user_id, serial_number, product_name, purchase_date, warranty_period, file_key):
    
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
    
#Fetch a specific claim by its ID from DynamoDB.
def get_claim_by_id(claim_id):
    """Fetch a claim by its ID from DynamoDB."""
    # Adjust query logic to filter by claim_id
    response = table.query(
        KeyConditionExpression=Key('SK').eq(f"CLAIM#{claim_id}")
    )
    return response.get('Items', [])[0] if response.get('Items') else None
