import boto3
from botocore.exceptions import ClientError

# Initialize the S3 client
s3 = boto3.client('s3', region_name='us-east-1')
BUCKET_NAME = 'warranty-documents-electronicdevices'  # Replace with your bucket name

def upload_file(file, object_key):
    """Upload a file to the S3 bucket."""
    try:
        s3.upload_fileobj(
            Fileobj=file,
            Bucket=BUCKET_NAME,
            Key=object_key,
        )
        return f"https://{BUCKET_NAME}.s3.amazonaws.com/{object_key}"
    except ClientError as e:
        print(f"Error uploading file: {e}")
        raise

def generate_presigned_url(object_key, expiration=3600):
    """Generate a presigned URL to access a file in the S3 bucket."""
    try:
        response = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': BUCKET_NAME, 'Key': object_key},
            ExpiresIn=expiration
        )
        return response
    except ClientError as e:
        print(f"Error generating presigned URL: {e}")
        return None
