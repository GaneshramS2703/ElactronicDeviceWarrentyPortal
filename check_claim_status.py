import boto3

def get_claim(serial_number, claim_id):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('ProductWarrantyTable')
    response = table.get_item(
        Key={
            'PK': f"PRODUCT#{serial_number}",
            'SK': f"CLAIM#{claim_id}"
        }
    )
    print("Claim Details:", response.get('Item'))

# Replace with actual serial number and claim ID
get_claim('444', '459b671a')
