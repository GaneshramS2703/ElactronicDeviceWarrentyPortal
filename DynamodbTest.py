import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

# Initialize DynamoDB with default Cloud9 credentials and region
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table_name = 'ProductWarrantyTable'
table = dynamodb.Table(table_name)

def create_product(user_id, serial_number, product_name, purchase_date, warranty_period, description):
    """Add a new product to DynamoDB."""
    try:
        item = {
            'PK': f"USER#{user_id}",
            'SK': f"PRODUCT#{serial_number}",
            'ProductName': product_name,
            'PurchaseDate': purchase_date,
            'WarrantyPeriod': warranty_period,
            'Description': description
        }
        table.put_item(Item=item)
        print(f"Product '{serial_number}' added successfully.")
    except ClientError as e:
        print(f"Error creating product: {e}")

def get_product(user_id, serial_number):
    """Retrieve a product by serial number."""
    try:
        response = table.get_item(Key={'PK': f"USER#{user_id}", 'SK': f"PRODUCT#{serial_number}"})
        return response.get('Item', {})
    except ClientError as e:
        print(f"Error retrieving product: {e}")
        return None

def create_claim(serial_number, claim_id, description):
    """Add a new claim to DynamoDB."""
    try:
        item = {
            'PK': f"PRODUCT#{serial_number}",
            'SK': f"CLAIM#{claim_id}",
            'Description': description,
            'Status': 'Pending'
        }
        table.put_item(Item=item)
        print(f"Claim '{claim_id}' added successfully.")
    except ClientError as e:
        print(f"Error creating claim: {e}")

def get_claim(serial_number, claim_id):
    """Retrieve a claim by claim ID."""
    try:
        response = table.get_item(Key={'PK': f"PRODUCT#{serial_number}", 'SK': f"CLAIM#{claim_id}"})
        return response.get('Item', {})
    except ClientError as e:
        print(f"Error retrieving claim: {e}")
        return None

if __name__ == "__main__":
    # Example usage
    create_product('1', 'SN123456', 'Test Product', '2024-01-01', 12, 'Test description')
    print(get_product('1', 'SN123456'))
