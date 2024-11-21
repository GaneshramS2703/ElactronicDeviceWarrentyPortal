import boto3

# Initialize AWS Services
dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')
table = dynamodb.Table('ProductWarrantyTable')

# Replace with your SNS topic ARN
SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:454329490259:ClaimStatusNotification"

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

                # Publish notification to SNS
                message = (
                    f"Your claim (ID: {claim_id}) for product (Serial: {serial_number}) has been updated to: {status}."
                )
                sns.publish(
                    TopicArn=SNS_TOPIC_ARN,
                    Message=message,
                    Subject="Claim Status Update"
                )
                print(f"Notification sent for claim {claim_id}")

            except Exception as e:
                print(f"Error processing claim {claim_id}: {e}")

    return {"statusCode": 200, "body": "Claims processed and notifications sent"}
