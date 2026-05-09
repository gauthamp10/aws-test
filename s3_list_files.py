import boto3
from botocore.exceptions import NoCredentialsError, ClientError

# Path to your AWS credentials file
# Example format:
# [default]
# aws_access_key_id = YOUR_ACCESS_KEY
# aws_secret_access_key = YOUR_SECRET_KEY
# region = us-east-2
CREDENTIALS_FILE = "./credentials"

# S3 bucket name
BUCKET_NAME = "your-bucket-name"


def list_s3_files(bucket_name: str):
    try:
        # Create session using shared credentials file
        session = boto3.Session(
            profile_name="default"
        )

        s3_client = session.client("s3")

        paginator = s3_client.get_paginator("list_objects_v2")

        print(f"Files in bucket: {bucket_name}\n")

        found = False
        for page in paginator.paginate(Bucket=bucket_name):
            for obj in page.get("Contents", []):
                found = True
                print(obj["Key"])

        if not found:
            print("Bucket is empty or no files found.")

    except NoCredentialsError:
        print("AWS credentials not found.")
    except ClientError as e:
        print(f"AWS Client Error: {e}")
    except Exception as e:
        print(f"Unexpected Error: {e}")


if __name__ == "__main__":
    # Export custom credentials file path if needed:
    # Linux/macOS:
    # export AWS_SHARED_CREDENTIALS_FILE=./credentials
    #
    # Windows PowerShell:
    # $env:AWS_SHARED_CREDENTIALS_FILE="./credentials"

    list_s3_files(BUCKET_NAME)
