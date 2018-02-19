import boto3
import uuid
import json
import urllib
from botocore.exceptions import ClientError


def faceExists(client, bucket, imageName, rekognitionCollection):
    result = ""

    response = client.search_faces_by_image(
        CollectionId=rekognitionCollection,
        Image={
            'S3Object': {
                'Bucket': bucket,
                'Name': imageName
            }
        },
        MaxFaces=1,
        FaceMatchThreshold=90
    )

    if(len(response["FaceMatches"]) > 0):
        result = response["FaceMatches"][0]["Face"]["ExternalImageId"]

    return result

def runWorkflow(bucket, imageName, smArn):
    data = {}
    data['bucket'] = bucket
    data['imageName'] = imageName
    json_data = json.dumps(data)

    client = boto3.client(service_name='stepfunctions', region_name='us-east-1')
    response = client.start_execution(stateMachineArn=smArn,
        name= str(uuid.uuid1()),
        input= json_data)

def getTask(actArn):
    client = boto3.client(service_name='stepfunctions', region_name='us-east-1')
    response = client.get_activity_task(
        activityArn=actArn,
        workerName='Lambda'
    )

    data = json.loads(response['input'])
    taskToken = response['taskToken']
    taskInput = json.loads(response['input'])

    return taskInput, taskToken


def saveRequest(imageId, token, bucket, imageName, s3url, dynamoTable):
    client = boto3.client('dynamodb')
    response = client.put_item(
    TableName= dynamoTable,
    Item={
        'ImageId' : {'S' : imageId},
        'Token' : {'S': token},
        'Bucket' : {'S': bucket},
        'ImageName' : {'S': imageName},
        'S3Url' : {'S': s3url}
    })

def sendEmail(MESSAGE, SENDER, RECIPIENT, SUBJECT):
    BODY_HTML = MESSAGE

    # The character encoding for the email.
    CHARSET = "UTF-8"

    # Create a new SES resource and specify a region.
    client = boto3.client('ses',region_name='us-east-1')

    # Try to send the email.
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['ResponseMetadata']['RequestId'])

def sendApprovalMessage(approveUrl, rejectUrl, s3url, SENDER, RECIPIENT, SUBJECT):
    BODY_HTML = """<html>
    <head></head>
    <body>
      <h1>Approval needed to add face to collection</h1>"""
    BODY_HTML += "- <a href='"
    BODY_HTML += approveUrl
    BODY_HTML +=  "'>Approve - Add below image to my collection of known people</a><br><br>"
    BODY_HTML += "- <a href='"
    BODY_HTML += rejectUrl
    BODY_HTML +=  "'>Reject - Do not add image below to my collection of known people</a>"
    BODY_HTML += "<br><br><img src='" + s3url + "' alt='face'><br>"
    BODY_HTML += """</body>
        </html>"""

    sendEmail(BODY_HTML, SENDER, RECIPIENT, SUBJECT)

def getS3PreSignedUrl(bucket, imageName):
    s3client = boto3.client('s3')
    s3url = s3client.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': bucket,
            'Key': imageName
        }
    )

    return s3url

def sendFaceMatchMessage(item, SENDER, RECIPIENT):

    bucket = item['Item']['Bucket']['S']
    imageName = item['Item']['ImageName']['S']
    personsName = item['Item']['PersonsName']['S']

    #Presigned Url
    s3url = getS3PreSignedUrl(bucket, imageName)

    BODY_HTML = """<html>
    <head></head>
    <body>
      <h1>Detected """
    BODY_HTML += personsName
    BODY_HTML +=  "</h1>"
    BODY_HTML += "<br><br><img src='" + s3url + "' alt='face'><br>"
    BODY_HTML += """</body>
        </html>"""

    sendEmail(BODY_HTML, SENDER, RECIPIENT, "Detected " + personsName)

def lambda_handler(event, context):

    #########Update according to your environment #########################
    #API Gateway end point URL
    apiGatewayUrl = 'https://YOUR-APIGW-ENDPOINT.execute-api.us-east-1.amazonaws.com/respond/'
    #URL for S3 Hosted Approval Website
    approvalWebsiteUrl = 'http://YOUR-S3BUCKET-web.s3-website-us-east-1.amazonaws.com'
    #Rekognition Collection Name
    rekognitionCollection = 'YOUR-REKOGNITION-COLLECTION'
    #Step Function State Machine Arn
    stateMachineArn = 'arn:aws:states:us-east-1:YOUR-AWS-ACCOUNT-ID:stateMachine:MLApprovalProcess'
    #Step Function Activity Arn
    activityArn = 'arn:aws:states:us-east-1:YOUR-AWS-ACCOUND-ID:activity:ManualStep'
    #Email information
    emailSender = "YOUR-EMAIL-ADDRESS"
    emailRecipient = "YOUR-EMAIL-ADDRESS"
    emailSubject = "Approval needed for image"
    #DynamoDB Table
    dynamoTable = 'YOUR-DYNAMODB-TABLE'
    #########Update according to your environment #########################

    bucket = event['Records'][0]['s3']['bucket']['name']
    imageName = event['Records'][0]['s3']['object']['key']

    client = boto3.client('rekognition')

    result = ""
    url = ""
    taskToken = ""

    fid = faceExists(client, bucket, imageName, rekognitionCollection)

    if(fid):
        result = "Found face, so not indexing. Face Id:" + fid
        ddb = boto3.client('dynamodb')
        response = ddb.get_item(
            TableName=dynamoTable,
            Key={
                'ImageId' : {'S': fid}
        })
        if 'Item' in response:
            sendFaceMatchMessage(response, emailSender, emailRecipient)

    else:
        #Start Step function Workflow
        runWorkflow(bucket, imageName, stateMachineArn)

        ###Stateless Worker Process
        #Get Task Activity
        taskInput, taskToken = getTask(activityArn)

        #Set bucket and image name from activity task
        bucket = taskInput["bucket"]
        imageName = taskInput["imageName"]

        #Create unique image ID for request
        imageId = str(uuid.uuid1())

        #Approval and rejection URL
        approveUrl = approvalWebsiteUrl + '?ImageId=' + urllib.parse.quote(imageId, safe='') +  '&taskToken=' + urllib.parse.quote(taskToken, safe='')
        rejectUrl = apiGatewayUrl + 'fail?ImageId=' + urllib.parse.quote(imageId, safe='') + '&taskToken=' + urllib.parse.quote(taskToken, safe='')

        #Presigned Url
        s3url = getS3PreSignedUrl(bucket, imageName)

        #Save Request in DDB
        saveRequest(imageId, taskToken, bucket, imageName, s3url, dynamoTable)

        #Send email
        sendApprovalMessage(approveUrl, rejectUrl, s3url, emailSender, emailRecipient, emailSubject)

        url = approveUrl + ", " + rejectUrl

    return result + " @ " + urllib.parse.quote(taskToken, safe='')
