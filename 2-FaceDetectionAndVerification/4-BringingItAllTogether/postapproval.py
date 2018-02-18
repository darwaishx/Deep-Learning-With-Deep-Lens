import boto3
import urllib

def saveFace(client, bucket, imageName, name, rekognitionCollection):

    response = client.index_faces(
        CollectionId=rekognitionCollection,
        Image={
            'S3Object': {
                'Bucket': bucket,
                'Name': imageName,
            }
        },
        ExternalImageId=name
    )

def lambda_handler(event, context):

    rekognitionCollection = 'YOUR-REKOGNITION-COLLECTION'

    approval = event['approval']
    urlEncodedTaskToken = event['taskToken']
    taskToken = urllib.parse.unquote(urlEncodedTaskToken)

    bucket = ""
    imageName = ""

    client = boto3.client('dynamodb')
    response = client.get_item(
        TableName='MLApprovals',
        Key={
            'Token' : {'S': taskToken}
    })

    if 'Item' in response:
        bucket = response['Item']['Bucket']['S']
        imageName = response['Item']['ImageName']['S']

        if(approval == 'approved'):
            name = event['name']
            client = boto3.client('rekognition')
            saveFace(client, bucket, imageName, name, rekognitionCollection)
    else:
        print('item does not exist.')

    return bucket + '/' + imageName
