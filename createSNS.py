import boto3

def create_sns_topic():
    sns = boto3.client('sns')
    response = sns.create_topic(Name="ClaimStatusNotification")
    topic_arn = response['TopicArn']
    print(f"Created SNS Topic with ARN: {topic_arn}")
    return topic_arn

sns_topic_arn = create_sns_topic()
