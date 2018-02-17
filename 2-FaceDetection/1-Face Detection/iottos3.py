import boto3
import base64
import time

def lambda_handler(event, context):

    bucket = "YOUR-S3-BUCKET-NAME"

    face = base64.b64decode(event['face'])

    s3 = boto3.client('s3')

    file_name = 'image-'+time.strftime("%Y%m%d-%H%M%S")+'.jpg'

    response = s3.put_object(ACL='public-read', Body=face,Bucket=bucket,Key=file_name)

    file_url = 'https://s3.amazonaws.com/' + bucket + '/' + file_name

    return file_url
