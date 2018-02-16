import boto3
import uuid
import json
import urllib
from botocore.exceptions import ClientError
def faceExists(client, bucket, imageName, rekognitionCollection): result = False
response = client.search_faces_by_image( CollectionId=rekognitionCollection, Image={
'S3Object': {
'Bucket': bucket, 'Name': imageName
} },
MaxFaces=1,
FaceMatchThreshold=90 )
if(len(response["FaceMatches"]) > 0): result = True
return result
def runWorkflow(bucket, imageName): data = {}
data['bucket'] = bucket data['imageName'] = imageName json_data = json.dumps(data)
client = boto3.client(service_name='stepfunctions', region_name='us-west-2')
response = client.start_execution(stateMachineArn='arn:aws:states:us-west-2:111111111111:stateMachine:MLApprovalProcess',
name= str(uuid.uuid1()), input= json_data)
def getTaskToken():
client = boto3.client(service_name='stepfunctions', region_name='us-west-2') response = client.get_activity_task(
activityArn='arn:aws:states:us-west-2:111111111111:activity:ManualStep',
workerName='Lambda' )
data = json.loads(response['input']) taskToken = response['taskToken']
return taskToken
def saveRequest(token, bucket, imageName, s3url): client = boto3.client('dynamodb')
response = client.put_item( TableName='MLApprovals',
Item={
'Token' : {'S': token},
'Bucket' : {'S': bucket}, 'ImageName' : {'S': imageName}, 'S3Url' : {'S': s3url}
})
def sendEmail(approveUrl, rejectUrl, s3url):

SENDER = "kashii@amazon.com"
 RECIPIENT = "kashii@amazon.com"
 SUBJECT = "Approval needed for image"
# The email body for recipients with non-HTML email clients. BODY_TEXT = ("Go to url below to approve imagel \r\n" + approveUrl) BODY_TEXT += ("Go to url below to reject imagel \r\n" + rejectUrl)
# The HTML body of the email. BODY_HTML = """<html> <head></head>
<body>
<h1>Approval needed for image</h1>"""
BODY_HTML += "<img src='" + s3url + "' alt='face'><br>" BODY_HTML += "<a href='"
BODY_HTML += approveUrl
BODY_HTML += "'>Approve Image</a><br><br>" BODY_HTML += "<a href='"
BODY_HTML += rejectUrl
BODY_HTML += "'>Reject Image</a>"
BODY_HTML += """</body>
</html>"""
# The character encoding for the email. CHARSET = "UTF-8"
# Create a new SES resource and specify a region. client = boto3.client('ses',region_name='us-west-2')
# Try to send the email. try:
#Provide the contents of the email. response = client.send_email(
Destination={ 'ToAddresses': [
RECIPIENT, ],
}, Message={
'Body': { 'Html': {
'Charset': CHARSET,
'Data': BODY_HTML, },
'Text': {
'Charset': CHARSET, 'Data': BODY_TEXT,
}, },
'Subject': {
'Charset': CHARSET, 'Data': SUBJECT,
}, },
Source=SENDER )
# Display an error if something goes wrong. except ClientError as e:
print(e.response['Error']['Message']) else:
print("Email sent! Message ID:"), print(response['ResponseMetadata']['RequestId'])
def getS3PreSignedUrl(bucket, imageName): s3client = boto3.client('s3')
s3url = s3client.generate_presigned_url(

ClientMethod='get_object', Params={
'Bucket': bucket,
'Key': imageName }
)
return s3url
def lambda_handler(event, context):
bucket = event['Records'][0]['s3']['bucket']['name'] imageName = event['Records'][0]['s3']['object']['key']
rekognitionCollection = 'aiweek'
#bucket = 'ki-aiweek' #imageName = 'kashifimran.jpg' #imageName = 'andy.png'
client = boto3.client('rekognition')
result = ""
url = "" taskToken = ""
if(faceExists(client, bucket, imageName, rekognitionCollection)): result = "Found face, so not indexing."
else:
result = "Did not find face so started approval process." runWorkflow(bucket, imageName)
taskToken = getTaskToken()
#approveUrl = 'https://1o1bhkc8r9.execute-api.us-west-2.amazonaws.com/respond/succeed?name=andy&taskToken=' + urllib.parse.quote(taskToken, safe='')
approveUrl = 'http://ki-aiweek-web.s3-website-us-west-2.amazonaws.com?taskToken=' + urllib.parse.quote(taskToken, safe='')
#rejectUrl = 'https://1o1bhkc8r9.execute-api.us-west-2.amazonaws.com/respond/fail?taskToken=' + urllib.parse.quote(taskToken, safe='')
rejectUrl = 'https://1o1bhkc8r9.execute-api.us-west-2.amazonaws.com/respond/fail?taskToken=' + urllib.parse.quote(taskToken, safe='')
s3url = getS3PreSignedUrl(bucket, imageName) saveRequest(taskToken, bucket, imageName, s3url) sendEmail(approveUrl, rejectUrl, s3url)
url = approveUrl + ", " + rejectUrl
return result + " @ " + urllib.parse.quote(taskToken, safe='')
