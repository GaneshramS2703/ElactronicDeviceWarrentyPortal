import boto3

def create_sqs_queue(queue_name):
    sqs = boto3.client('sqs')
    response = sqs.create_queue(
        QueueName=queue_name,
        Attributes={
            'VisibilityTimeout': '60',  # Time (in seconds) a message is hidden after being received
        }
    )
    print(f"Queue URL: {response['QueueUrl']}")
    return response['QueueUrl']

if __name__ == "__main__":
    queue_name = "ClaimStatusQueue"
    create_sqs_queue(queue_name)
