import zipfile

# Create a ZIP file package.
# The package includes the 'sqs_consumer.py' file, which contains the Lambda function's code.

def create_lambda_package():
    # Open a ZIP file in write mode and add the 'sqs_consumer.py' file to it
    with zipfile.ZipFile('sqs_consumer.zip', 'w') as z:
        z.write('sqs_consumer.py')

create_lambda_package()
print("Lambda package created: sqs_consumer.zip")
