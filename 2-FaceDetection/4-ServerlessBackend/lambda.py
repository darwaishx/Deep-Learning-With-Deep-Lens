import boto3
import uuid
import json
import urllib
from botocore.exceptions import ClientError


def faceExists(client, bucket, imageName, rekognitionCollection):
    result = False

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
        result = True

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


def saveRequest(token, bucket, imageName, s3url):
    client = boto3.client('dynamodb')
    response = client.put_item(
    TableName='MLApprovals',
    Item={
        'Token' : {'S': token},
        'Bucket' : {'S': bucket},
        'ImageName' : {'S': imageName},
        'S3Url' : {'S': s3url}
    })

def sendEmail(approveUrl, rejectUrl, s3url, SENDER, RECIPIENT, SUBJECT):
    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = ("Go to url below to approve imagel \r\n" + approveUrl)
    BODY_TEXT += ("Go to url below to reject imagel \r\n" + rejectUrl)

    # The HTML body of the email.
    BODY_HTML = """<html>
    <head></head>
    <body>
      <h1>Approval needed for image</h1>"""
    BODY_HTML += "<img src='" + s3url + "' alt='face'><br>"
    BODY_HTML += "<a href='"
    BODY_HTML += approveUrl
    BODY_HTML +=  "'>Approve Image</a><br><br>"
    BODY_HTML += "<a href='"
    BODY_HTML += rejectUrl
    BODY_HTML +=  "'>Reject Image</a>"
    BODY_HTML += """</body>
        </html>"""

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
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
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


def lambda_handler(event, context):

    #API Gateway end point URL
    apiGatewayUrl = 'https://YOURAPI.execute-api.us-east-1.amazonaws.com/respond/'
    #URL for S3 Hosted Approval Website
    approvalWebsiteUrl = 'http://YOURS3WebSite.s3-website-us-east-1.amazonaws.com'
    #Rekognition Collection Name
    rekognitionCollection = 'YOUR-RekognitionCollection'
    #Step Function State Machine Arn
    stateMachineArn = 'YOUR-STATEMachineArn'
    #Step Function Activity Arn
    activityArn = 'YOUR-ACTIVITYArn'
    #Email information
    emailSender = "kashii@amazon.com"
    emailRecipient = "kashii@amazon.com"
    emailSubject = "Approval needed for new image"

    bucket = event['Records'][0]['s3']['bucket']['name']
    imageName = event['Records'][0]['s3']['object']['key']

    client = boto3.client('rekognition')

    result = ""
    url = ""
    taskToken = ""

    if(faceExists(client, bucket, imageName, rekognitionCollection)):
        result = "Found face, so not indexing."
    else:
        #Start Step function Workflow
        runWorkflow(bucket, imageName, stateMachineArn)

        ###Stateless Worker Process
        #Get Task Activity
        taskInput, taskToken = getTask(activityArn)

        #Set bucket and image name from activity task
        bucket = taskInput["bucket"]
        imageName = taskInput["imageName"]

        #Approval and rejection URL
        approveUrl = approvalWebsiteUrl + '?taskToken=' + urllib.parse.quote(taskToken, safe='')
        rejectUrl = apiGatewayUrl + 'fail?taskToken=' + urllib.parse.quote(taskToken, safe='')

        #Presigned Url
        s3url = getS3PreSignedUrl(bucket, imageName)

        #Save Request in DDB
        saveRequest(taskToken, bucket, imageName, s3url)

        #Send email
        sendEmail(approveUrl, rejectUrl, s3url, emailSender, emailRecipient, emailSubject)

        url = approveUrl + ", " + rejectUrl

    return result + " @ " + urllib.parse.quote(taskToken, safe='')
