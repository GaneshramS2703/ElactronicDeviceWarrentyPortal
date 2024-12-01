import boto3
from botocore.exceptions import ClientError

# Initialize the S3 client
s3 = boto3.client('s3', region_name='us-east-1')
BUCKET_NAME = 'warranty-documents-electronicdevices'  # bucket name

#Upload a file to the specified S3 bucket.
def upload_file(file, object_key):
    try:
        # Upload the file to the specified bucket with the provided key
        s3.upload_fileobj(
            Fileobj=file,
            Bucket=BUCKET_NAME,
            Key=object_key,
        )
         # Return the public URL of the uploaded file
        return f"https://{BUCKET_NAME}.s3.amazonaws.com/{object_key}"
    except ClientError as e:
        print(f"Error uploading file: {e}")
        raise
    
#Generate a presigned URL to access a file in the S3 bucket.
def generate_presigned_url(object_key, expiration=3600):
    
    try:
        #Generate a presigned URL to access a file in the S3 bucket.
        response = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': BUCKET_NAME, 'Key': object_key},
            ExpiresIn=expiration
        )
        return response
    except ClientError as e:
        print(f"Error generating presigned URL: {e}")
        return None
