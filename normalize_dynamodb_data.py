import boto3

def normalize_status_field():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('ProductWarrantyTable')

    # Scan for all items
    response = table.scan()
    items = response.get('Items', [])

    for item in items:
        if 'Status' in item:  # Check for uppercase 'Status'
            new_status = item['Status']
            print(f"Normalizing status for {item['SK']}")

            # Using ExpressionAttributeNames to alias the reserved keyword
            table.update_item(
                Key={
                    'PK': item['PK'],
                    'SK': item['SK']
                },
                UpdateExpression="SET #status = :status REMOVE #reserved",
                ExpressionAttributeNames={
                    "#status": "status",       # Alias for the lowercase field
                    "#reserved": "Status"      # Alias for the reserved keyword
                },
                ExpressionAttributeValues={
                    ":status": new_status      # Assign the existing value to 'status'
                }
            )

    print("Data normalization complete.")

# Run the normalization script
normalize_status_field()
