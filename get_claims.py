import boto3

def get_claims_for_serial(serial_number):
    """
    Retrieve all claims for a given product's serial number from DynamoDB.
    """
    try:
        # Initialize DynamoDB resource
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('ProductWarrantyTable')

        # Query the table for claims associated with the product
        response = table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key('PK').eq(f"PRODUCT#{serial_number}")
        )

        # Print claim details
        items = response.get('Items', [])
        if not items:
            print(f"No claims found for Serial Number: {serial_number}")
        else:
            for item in items:
                print(f"Claim ID: {item['SK'].split('#')[1]}")
                print(f"Claim Details: {item}")

    except Exception as e:
        print(f"Error fetching claims: {e}")

# Replace with the actual serial number of the product
get_claims_for_serial('1234')
