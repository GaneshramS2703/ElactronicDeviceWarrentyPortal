import boto3

# Creates an event source mapping for an AWS Lambda function.

def create_event_source_mapping(stream_arn):
    lambda_client = boto3.client('lambda')
    response = lambda_client.create_event_source_mapping(
        EventSourceArn=stream_arn,
        FunctionName='ClaimProcessor', # The name of the Lambda function.
        StartingPosition='LATEST' # Start processing from the latest event.
    )
    print("Event source mapping created:", response)

if __name__ == "__main__":
    # Replace with the actual stream ARN
    create_event_source_mapping('arn:aws:dynamodb:us-east-1:454329490259:table/ProductWarrantyTable/stream/2024-11-20T16:31:21.007')
