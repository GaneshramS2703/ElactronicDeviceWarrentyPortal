import boto3

def list_items():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('ProductWarrantyTable')

    response = table.scan()  # Fetch all items
    items = response.get('Items', []) # Retrieve the list of items, default to an empty list if none.
    print("Items in Table:")
    print("Items in Table:")
    for item in items:
        print(item)

list_items()
