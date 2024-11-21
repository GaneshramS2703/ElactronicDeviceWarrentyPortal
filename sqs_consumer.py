import boto3
import json

# Initialize SNS
sns = boto3.client('sns')
SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:454329490259:ClaimStatusNotification"

def lambda_handler(event, context):
    for record in event['Records']:
        # Parse the SQS message
        message = json.loads(record['body'])
        claim_id = message.get('claim_id')
        serial_number = message.get('serial_number')
        status = message.get('status')
        user_email = message.get('user_email')

        # Send SNS notification
        try:
            sns.publish(
                TopicArn=SNS_TOPIC_ARN,
                Message=f"Your claim {claim_id} for product {serial_number} has been updated to: {status}.",
                Subject="Claim Status Update",
                MessageAttributes={
                    'user_email': {
                        'DataType': 'String',
                        'StringValue': user_email
                    }
                }
            )
            print(f"Notification sent for claim {claim_id}.")
        except Exception as e:
            print(f"Failed to send notification for claim {claim_id}: {e}")
