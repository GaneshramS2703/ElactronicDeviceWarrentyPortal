import zipfile

def create_lambda_package():
    with zipfile.ZipFile('claim_processor.zip', 'w') as z:
        z.write('claim_processor.py')

create_lambda_package()
print("Lambda package created: claim_processor.zip")
