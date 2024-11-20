import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ProductWarrantyTable')

def lambda_handler(event, context):
    for record in event['Records']:
        if record['eventName'] == 'INSERT':
            new_image = record['dynamodb']['NewImage']
            serial_number = new_image['PK']['S'].split('#')[1]
            claim_id = new_image['SK']['S'].split('#')[1]
            description = new_image['description']['S']

            status = "Approved" if "valid" in description.lower() else "Rejected"

            table.update_item(
                Key={
                    'PK': f"PRODUCT#{serial_number}",
                    'SK': f"CLAIM#{claim_id}"
                },
                UpdateExpression="SET #status = :status",
                ExpressionAttributeNames={"#status": "status"},
                ExpressionAttributeValues={":status": status}
            )
    return {"statusCode": 200, "body": "Claims processed successfully"}
