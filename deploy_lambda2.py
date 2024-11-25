import boto3

def update_lambda_function():
    lambda_client = boto3.client('lambda')

    # Load the updated Lambda deployment package
    with open('claim_processor.zip', 'rb') as f:
        zip_content = f.read()

    # Update the existing Lambda function's code
    response = lambda_client.update_function_code(
        FunctionName='ClaimProcessor',
        ZipFile=zip_content
    )
    print("Lambda function updated:", response)

if __name__ == "__main__":
    update_lambda_function()
