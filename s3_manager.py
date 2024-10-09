import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

class S3Manager:
    def __init__(self, access_key, secret_key, region):
        print("Init of S3Manager")
        self.access_key = access_key
        self.secret_key = secret_key
        self.region = region
        self.s3 = None
        self.connect_to_s3()
        

    # Establish connection to S3
    def connect_to_s3(self):
        try:
            self.s3 = boto3.client(
                's3',
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_key,
                region_name=self.region
            )
            print(f"Using region: {self.s3.meta.region_name}")
        except (NoCredentialsError, PartialCredentialsError) as e:
            print(f"Error: {e}")
    
    # List all S3 buckets
    def list_buckets(self):
        try:
            response = self.s3.list_buckets()
            bucket_names = [bucket['Name'] for bucket in response['Buckets']]
            return bucket_names  # Ensure you're returning an array of bucket names
        except Exception as e:
            print(f"Error listing buckets: {e}")
            return None

    # List files (objects) in a specific bucket
    def list_files(self, bucket_name):
        try:
            response = self.s3.list_objects_v2(Bucket=bucket_name)
            if 'Contents' in response:
                file_names = [file['Key'] for file in response['Contents']]
                return file_names
            else:
                return []  # Return an empty list if no files found
        except Exception as e:
            print(f"Error listing files in bucket {bucket_name}: {e}")
            return None
