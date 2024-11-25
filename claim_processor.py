import boto3
import json

# Initialize SQS and DynamoDB
sqs = boto3.client('sqs')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ProductWarrantyTable')

# SQS Queue URL
SQS_QUEUE_URL = "https://sqs.us-east-1.amazonaws.com/454329490259/ClaimStatusQueue"

def lambda_handler(event, context):
    for record in event['Records']:
        if record['eventName'] == 'INSERT':  # Process only new claims
            new_image = record.get('dynamodb', {}).get('NewImage', {})

            # Safely extract fields
            serial_number = new_image.get('PK', {}).get('S', '').split('#')[1]
            claim_id = new_image.get('SK', {}).get('S', '').split('#')[1]
            description = new_image.get('description', {}).get('S', 'No description')
            user_email = new_image.get('user_email', {}).get('S', 'No email provided')

            if not serial_number or not claim_id:
                print(f"Invalid record: {record}")
                continue

            # Business logic for claim status
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

                # Send the claim notification to SQS
                message_body = {
                    "serial_number": serial_number,
                    "claim_id": claim_id,
                    "status": status,
                    "user_email": user_email
                }
                sqs.send_message(
                    QueueUrl=SQS_QUEUE_URL,
                    MessageBody=json.dumps(message_body)
                )
                print(f"Claim {claim_id} message sent to SQS.")

            except Exception as e:
                print(f"Failed to update claim {claim_id}: {e}")

    return {"statusCode": 200, "body": "Claims processed and sent to SQS"}
