import boto3

def enable_dynamodb_stream():
    dynamodb = boto3.client('dynamodb')
    response = dynamodb.update_table(
        TableName='ProductWarrantyTable',
        StreamSpecification={
            'StreamEnabled': True,
            'StreamViewType': 'NEW_IMAGE'
        }
    )
    print("DynamoDB Streams enabled:", response)

def get_stream_arn():
    dynamodb = boto3.client('dynamodb')
    response = dynamodb.describe_table(TableName='ProductWarrantyTable')
    return response['Table']['LatestStreamArn']

if __name__ == "__main__":
    enable_dynamodb_stream()
    stream_arn = get_stream_arn()
    print("Stream ARN:", stream_arn)
