import boto3
from botocore.exceptions import NoCredentialsError

AWS_ACCESS_KEY_ID = "AKIAZQ3DTYDUZCZCDGWH"
AWS_SECRET_ACCESS_KEY = "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"
AWS_REGION = "eu-north-1" 
BUCKET_NAME = "urmil"
FILE_PATH = "Videos/video_1.mp4"
UPLOAD_KEY = "Upload/out_1.mp4"
  
def upload_to_s3(file_path, bucket_name, upload_key):
    s3 = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION
    )
    try:
        # Upload file
        s3.upload_file(file_path, bucket_name, upload_key)
        print(f"File '{file_path}' successfully uploaded to S3 as '{upload_key}'.")
    except FileNotFoundError:
        print("Error: The file was not found.")
    except NoCredentialsError:
        print("Error: Credentials not available.")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    upload_to_s3(FILE_PATH, BUCKET_NAME, UPLOAD_KEY)