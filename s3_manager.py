import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError

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
        
    # Method to create a bucket
    def create_bucket(self, bucket_name):
        try:
            self.s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={
                'LocationConstraint': self.region
            })
            print(f"Bucket {bucket_name} created successfully.")
            return True
        except Exception as e:
            print(f"Error creating bucket {bucket_name}: {e}")
            return False

    # Method to delete a bucket
    def delete_bucket(self, bucket_name):
        try:
            self.s3.delete_bucket(Bucket=bucket_name)
            print(f"Bucket {bucket_name} deleted successfully.")
            return True
        except Exception as e:
            print(f"Error deleting bucket {bucket_name}: {e}")
            return False
        
    # Method to delete files from a bucket
    def delete_files(self, bucket_name, files):
        try:
            delete_objects = [{'Key': file_name} for file_name in files]  # Prepare the list of files to delete
            response = self.s3.delete_objects(
                Bucket=bucket_name,
                Delete={'Objects': delete_objects}
            )
            print(f"Files deleted successfully from {bucket_name}.")
            return True
        except Exception as e:
            print(f"Error deleting files from bucket {bucket_name}: {e}")
            return False
        
    # Method to upload files to a bucket
    def upload_files(self, bucket_name, files):
        try:
            for file in files:
                self.s3.put_object(Bucket=bucket_name, 
                                   Key=file.filename, 
                                   Body=file,
                                   CacheControl="no-cache, no-store, must-revalidate")
            print(f"Files uploaded successfully to {bucket_name}.")
            return True
        except Exception as e:
            print(f"Error uploading files to bucket {bucket_name}: {e}")
            return False
        
     # Method to generate pre-signed URLs for files
    def generate_presigned_url(self, bucket_name, file_name, expiration=3600):
        print("generating url ...:", file_name)
        try:
            response = self.s3.generate_presigned_url(
                'get_object',
                Params={'Bucket': bucket_name, 'Key': file_name},
                ExpiresIn=expiration  # URL expires in 1 hour by default
            )
            return response
        except ClientError as e:
            print(f"Error generating pre-signed URL: {e}")
            return None

