import boto3

def list_items():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('ProductWarrantyTable')

    response = table.scan()  # Fetch all items
    items = response.get('Items', [])
    print("Items in Table:")
    for item in items:
        print(item)

list_items()
