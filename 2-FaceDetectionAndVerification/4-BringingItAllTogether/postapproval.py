import boto3
import urllib

def saveFace(client, bucket, imageName, imageId, rekognitionCollection):

    print(bucket)
    print(imageName)
    print(imageId)
    print(rekognitionCollection)

    response = client.index_faces(
        CollectionId=rekognitionCollection,
        Image={
            'S3Object': {
                'Bucket': bucket,
                'Name': imageName,
            }
        },
        ExternalImageId=imageId
    )

def lambda_handler(event, context):
    rekognitionCollection = 'YOUR-REKOGNITION-COLLECTION'
    dynamodbTableName = 'YOUR-DYNAMODB-TABLE'

    approval = event['approval']
    urlEncodedTaskToken = event['taskToken']
    taskToken = urllib.parse.unquote(urlEncodedTaskToken)
    urlEncodedImageId = event['ImageId']
    imageId = urllib.parse.unquote(urlEncodedImageId)

    bucket = ""
    imageName = ""

    ddb = boto3.client('dynamodb')
    response = ddb.get_item(
        TableName=dynamodbTableName,
        Key={
            'ImageId' : {'S': imageId}
    })

    if 'Item' in response:
        bucket = response['Item']['Bucket']['S']
        imageName = response['Item']['ImageName']['S']

        #SHOULD ALSO VERIFY THAT IMAGEID AND TOKEN MATCH SO BUT LET USER DO ADDITIONAL CHECKS

        if(approval == 'approved'):
            name = event['name']
            client = boto3.client('rekognition')
            saveFace(client, bucket, imageName, imageId, rekognitionCollection)

            client = boto3.client('dynamodb')
            response = ddb.update_item(
                TableName=dynamodbTableName,
                Key={
                    'ImageId' : {'S': imageId}
            },

            UpdateExpression='SET PersonsName = :val1',
            ExpressionAttributeValues={
                ':val1': { 'S' : name}
            })
    else:
        print('item does not exist.')

    return bucket + '/' + imageName
