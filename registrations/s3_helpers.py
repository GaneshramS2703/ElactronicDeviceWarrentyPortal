import boto3
from botocore.exceptions import ClientError

s3 = boto3.client('s3')

def upload_document(file_path, bucket_name, object_key):
    """Upload a file to S3."""
    try:
        s3.upload_file(file_path, bucket_name, object_key)
        print(f"File uploaded to {bucket_name}/{object_key}")
    except ClientError as e:
        print(f"Error uploading file: {e}")

def get_document_url(bucket_name, object_key):
    """Generate a presigned URL to access an S3 object."""
    try:
        url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': object_key},
            ExpiresIn=3600  # URL valid for 1 hour
        )
        return url
    except ClientError as e:
        print(f"Error generating URL: {e}")
        return None
