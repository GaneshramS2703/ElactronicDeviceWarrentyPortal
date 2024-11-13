import boto3
from botocore.exceptions import ClientError

# Initialize the DynamoDB resource
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

def create_dynamodb_table():
    """Creates a DynamoDB table with a Partition Key (PK) and Sort Key (SK)."""
    table_name = "ProductWarrantyTable"

    try:
        # Define the table schema and create the table
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'PK',  # Partition Key
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'SK',  # Sort Key
                    'KeyType': 'RANGE'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'PK',
                    'AttributeType': 'S'  # 'S' indicates string type
                },
                {
                    'AttributeName': 'SK',
                    'AttributeType': 'S'
                }
            ],
            BillingMode='PAY_PER_REQUEST'  # On-demand mode for development
        )

        # Wait until the table is active
        print(f"Creating table {table_name}...")
        table.wait_until_exists()
        print(f"Table {table_name} created successfully.")

    except ClientError as e:
        print(f"Error creating table: {e}")
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print(f"Table {table_name} already exists.")

if __name__ == "__main__":
    create_dynamodb_table()
