import boto3  

def subscribe_user_to_sns(email):
    """
    Subscribe a user to the AWS SNS Topic using their email.
    """
    sns_client = boto3.client('sns')

    # My SNS Topic ARN
    sns_topic_arn = "arn:aws:sns:us-east-1:454329490259:ClaimStatusNotification"

    try:
        response = sns_client.subscribe(
            TopicArn=sns_topic_arn,
            Protocol='email',  # Protocol can be 'email' or 'sms'
            Endpoint=email  # Email address to subscribe
        )
        print(f"Subscription ARN: {response['SubscriptionArn']}")
        print(f"User {email} subscribed successfully to {sns_topic_arn}")

    except Exception as e:
        print(f"Failed to subscribe {email} to SNS: {str(e)}")

# Example Usage
subscribe_user_to_sns("ganeshramsundari@gmail.com")
