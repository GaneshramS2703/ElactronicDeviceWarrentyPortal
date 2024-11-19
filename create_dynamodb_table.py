import boto3
from botocore.exceptions import ClientError

def create_dynamodb_table():
    """Creates a DynamoDB table with a Partition Key (PK) and Sort Key (SK)."""
    table_name = 'ProductWarrantyTable'
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

    try:
        # Define the table schema and create the table
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {'AttributeName': 'PK', 'KeyType': 'HASH'},  # Partition Key
                {'AttributeName': 'SK', 'KeyType': 'RANGE'}  # Sort Key
            ],
            AttributeDefinitions=[
                {'AttributeName': 'PK', 'AttributeType': 'S'},  # 'S' indicates string type
                {'AttributeName': 'SK', 'AttributeType': 'S'}
            ],
            BillingMode='PAY_PER_REQUEST'  # On-demand mode
        )

        # Wait until the table is active
        print(f"Creating table {table_name}...")
        table.wait_until_exists()
        print(f"Table {table_name} created successfully.")

    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print(f"Table {table_name} already exists.")
        else:
            print(f"Error creating table: {e}")

if __name__ == "__main__":
    create_dynamodb_table()
