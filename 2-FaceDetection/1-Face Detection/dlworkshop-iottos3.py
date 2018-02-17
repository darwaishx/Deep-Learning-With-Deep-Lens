import boto3
import base64
import time

def lambda_handler(event, context):

    face = base64.b64decode(event['face'])

    s3 = boto3.client('s3')

    file_name = 'ggtest/dc/image-'+time.strftime("%Y%m%d-%H%M%S")+'.jpg'

    response = s3.put_object(ACL='public-read', Body=face,Bucket='ki-aiweek',Key=file_name)

    file_url = 'https://s3-us-west-2.amazonaws.com/ki-aiweek/'+file_name

    return file_url
