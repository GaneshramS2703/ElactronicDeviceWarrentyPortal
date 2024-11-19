import boto3
from botocore.exceptions import ClientError

def create_s3_bucket(bucket_name, region='us-east-1'):
    """Create an S3 bucket in the specified region."""
    try:
        s3 = boto3.client('s3', region_name=region)

        if region == 'us-east-1':
            # Create bucket without LocationConstraint for us-east-1
            s3.create_bucket(Bucket=bucket_name)
        else:
            # Create bucket with LocationConstraint for other regions
            s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': region}
            )

        print(f"Bucket '{bucket_name}' created successfully in region '{region}'")

    except ClientError as e:
        if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
            print(f"Bucket '{bucket_name}' already exists and is owned by you.")
        else:
            print(f"Error: {e}")

if __name__ == "__main__":
    # Replace with your bucket name
    bucket_name = "warranty-documents-electronicdevices"
    region = "us-east-1"  # Adjust region if needed
    create_s3_bucket(bucket_name, region)
