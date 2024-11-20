import boto3

def deploy_lambda_function(lambda_role_arn):
    lambda_client = boto3.client('lambda')
    with open('claim_processor.zip', 'rb') as f:
        zip_content = f.read()

    response = lambda_client.create_function(
        FunctionName='ClaimProcessor',
        Runtime='python3.10',
        Role=lambda_role_arn,
        Handler='claim_processor.lambda_handler',
        Code={'ZipFile': zip_content},
        Timeout=15,
        MemorySize=128
    )
    print("Lambda function created:", response)

if __name__ == "__main__":
    # Replace with the actual role ARN
    deploy_lambda_function('arn:aws:iam::454329490259:role/LabRole')
