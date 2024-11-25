import boto3
import json

sns = boto3.client('sns')
SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:454329490259:ClaimStatusNotification"

def lambda_handler(event, context):
    print(f"Received event: {json.dumps(event)}")  # Debug log

    for record in event['Records']:
        try:
            # Parse the SQS message
            message_body = record['body']
            print(f"Raw message body: {message_body}")  # Log raw message
            message = json.loads(message_body)  # Attempt to parse JSON
            print(f"Parsed message: {message}")  # Log parsed message

            # Extract data from message
            claim_id = message.get('claim_id')
            serial_number = message.get('serial_number')
            status = message.get('status')
            user_email = message.get('user_email')

            if not claim_id or not serial_number or not user_email:
                print(f"Invalid message data: {message}")
                continue

            # Publish to SNS
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
        except json.JSONDecodeError as e:
            print(f"JSON decode error for record: {record}. Error: {e}")
        except Exception as e:
            print(f"Failed to process message: {e}")
