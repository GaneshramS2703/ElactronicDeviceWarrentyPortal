from boto3.dynamodb.conditions import Key
import boto3

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
        return response.get('Item')
    except Exception as e:
        print(f"Error retrieving product: {e}")
        return None

def get_claims_for_product(serial_number):
    """Retrieve all claims for a given product."""
    try:
        response = table.query(
            KeyConditionExpression=Key('PK').eq(f"PRODUCT#{serial_number}") &
                                   Key('SK').begins_with("CLAIM")
        )
        return response['Items']
    except Exception as e:
        print(f"Error retrieving claims: {e}")
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
        print(f"Deleted product: {serial_number}")
    except Exception as e:
        print(f"Error deleting product: {e}")
