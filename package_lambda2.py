import zipfile

# Create a ZIP file package.
# The package includes the 'claim_processor.py' file, which contains the Lambda function's code.

def create_lambda_package():
    # Open a ZIP file in write mode and add the 'claim_processor.py' file to it
    with zipfile.ZipFile('claim_processor.zip', 'w') as z:
        z.write('claim_processor.py')

# Call the function to create the Lambda package
create_lambda_package()


print("Lambda package created: claim_processor.zip")

