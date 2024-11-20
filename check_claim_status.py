import boto3

def check_claim_status(serial_number, claim_id):
    """
    Retrieve and display the status of a specific claim in DynamoDB.
    """
    try:
        # Initialize DynamoDB resource
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('ProductWarrantyTable')

        # Get the item from DynamoDB
        response = table.get_item(
            Key={
                'PK': f"PRODUCT#{serial_number}",
                'SK': f"CLAIM#{claim_id}"
            }
        )
        
        # Retrieve and print claim details
        claim = response.get('Item')
        if not claim:
            print(f"No claim found for Serial Number: {serial_number} and Claim ID: {claim_id}")
            return

        # Print claim details
        print(f"Claim Details: {claim}")
        status = claim.get('Status') or claim.get('status')  # Check for both capitalized and lowercase versions
        if status:
            print(f"Status: {status}")
        else:
            print("Status field is missing in the claim data.")

    except Exception as e:
        print(f"Error fetching claim status: {e}")

# Replace these with actual values
check_claim_status('1234', '42cd701d')
