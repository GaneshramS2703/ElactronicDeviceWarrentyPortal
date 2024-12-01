import boto3

# Enables DynamoDB Streams for the specified table.


def enable_dynamodb_stream():
    dynamodb = boto3.client('dynamodb')
    response = dynamodb.update_table(
        TableName='ProductWarrantyTable', #My table name
        StreamSpecification={
            'StreamEnabled': True, # Enable the stream.
            'StreamViewType': 'NEW_IMAGE' # Capture the new state of items after modifications.
        }
    )
    print("DynamoDB Streams enabled:", response)
    
# Retrieves the Amazon Resource Name (ARN) of the DynamoDB Stream.

def get_stream_arn():
    dynamodb = boto3.client('dynamodb')
    response = dynamodb.describe_table(TableName='ProductWarrantyTable') # My table name
    return response['Table']['LatestStreamArn'] # Retrieves the Amazon Resource Name (ARN) of the DynamoDB Stream.


if __name__ == "__main__":
    enable_dynamodb_stream()
    stream_arn = get_stream_arn()
    print("Stream ARN:", stream_arn)
