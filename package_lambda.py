import zipfile

def create_lambda_package():
    with zipfile.ZipFile('sqs_consumer.zip', 'w') as z:
        z.write('sqs_consumer.py')

create_lambda_package()
print("Lambda package created: sqs_consumer.zip")
