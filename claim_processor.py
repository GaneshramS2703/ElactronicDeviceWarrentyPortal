import boto3

# Initialize the DynamoDB resource and specify the table
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ProductWarrantyTable')

def lambda_handler(event, context):
    for record in event['Records']:
        if record['eventName'] == 'INSERT':  # Process only new claims
            new_image = record.get('dynamodb', {}).get('NewImage', {})

            # Safely extract fields
            serial_number = new_image.get('PK', {}).get('S', '').split('#')[1]
            claim_id = new_image.get('SK', {}).get('S', '').split('#')[1]

            if not serial_number or not claim_id:
                print(f"Invalid record: {record}")
                continue

            # Simplified logic: All claims are marked as "Processed"
            status = "Processed"

            # Update the claim status in DynamoDB
            try:
                table.update_item(
                    Key={
                        'PK': f"PRODUCT#{serial_number}",
                        'SK': f"CLAIM#{claim_id}"
                    },
                    UpdateExpression="SET #status = :status",
                    ExpressionAttributeNames={"#status": "status"},
                    ExpressionAttributeValues={":status": status}
                )
                print(f"Updated claim {claim_id} with status {status}")
            except Exception as e:
                print(f"Failed to update claim {claim_id}: {e}")

    return {"statusCode": 200, "body": "Claims processed successfully"}
