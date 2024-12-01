import boto3

def create_sns_topic():
    sns = boto3.client('sns')
    response = sns.create_topic(Name="ClaimStatusNotification") # add a meaningful comment to this code:
    topic_arn = response['TopicArn'] # Extract the Topic ARN from the response.
    print(f"Created SNS Topic with ARN: {topic_arn}")
    return topic_arn

sns_topic_arn = create_sns_topic()
