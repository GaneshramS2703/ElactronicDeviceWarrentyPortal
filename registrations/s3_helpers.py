import boto3
from botocore.exceptions import ClientError

s3 = boto3.client('s3')

def upload_document(file_path, bucket_name, object_key):
    """Upload a file to S3."""
    try:
        with open(file_path, 'rb') as file:
            s3.upload_fileobj(file, bucket_name, object_key)
        print(f"File uploaded to {bucket_name}/{object_key}")
    except FileNotFoundError:
        print(f"File {file_path} not found.")
    except ClientError as e:
        print(f"Error uploading file: {e}")

def get_document_url(bucket_name, object_key):
    """Generate a presigned URL to access an S3 object."""
    try:
        url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': object_key},
            ExpiresIn=3600
        )
        return url
    except ClientError as e:
        print(f"Error generating URL: {e}")
        return None
