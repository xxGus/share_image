import os

import boto3

def upload_image(image_data, filename):
    s3_client = boto3.client("s3",
    aws_access_key_id=os.environ.get("ACCESS_KEY"),
    aws_secret_access_key=os.environ.get("SECRET_KEY"),
    region_name='sa-east-1')
    
    bucket = os.environ.get("BUCKET_NAME")

    s3_client.upload_fileobj(image_data, bucket, filename)

    s3_client = boto3.resource("s3")
    object_acl = s3_client.ObjectAcl(bucket, filename)
    object_acl.put(ACL="public-read")
    return f"https://{bucket}.s3.amazonaws.com/{filename}"