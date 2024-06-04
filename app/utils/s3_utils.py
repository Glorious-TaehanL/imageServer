import boto3
import os

# AWS S3 연결 설정 함수
def s3_connection():
    s3 = boto3.client(
        service_name = 's3',
        aws_access_key_id = os.environ['AWS_ACCESS_KEY'],
        aws_secret_access_key = os.environ['AWS_SECRET_KEY'],
        region_name = os.environ['AWS_S3_REGION_NAME']
    )
    return s3