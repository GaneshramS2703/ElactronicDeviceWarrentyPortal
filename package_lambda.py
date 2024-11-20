import zipfile

def create_lambda_package():
    with zipfile.ZipFile('claim_processor.zip', 'w') as z:
        z.write('claim_processor.py')  # Add the Lambda code file to the ZIP package

if __name__ == "__main__":
    create_lambda_package()
    print("Lambda package created as claim_processor.zip.")
