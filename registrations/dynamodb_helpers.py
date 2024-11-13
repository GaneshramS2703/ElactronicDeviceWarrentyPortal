from boto3.dynamodb.conditions import Key
import boto3

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('ProductWarrantyTable')

def get_product(serial_number):
    """Retrieve a product from DynamoDB by serial number."""
    response = table.get_item(
        Key={
            'PK': f"USER#{user_id}",
            'SK': f"PRODUCT#{serial_number}"
        }
    )
    return response.get('Item')

def get_claims_for_product(serial_number):
    """Retrieve all claims for a given product."""
    response = table.query(
        KeyConditionExpression=Key('PK').eq(f"PRODUCT#{serial_number}") &
                               Key('SK').begins_with("CLAIM")
    )
    return response['Items']
