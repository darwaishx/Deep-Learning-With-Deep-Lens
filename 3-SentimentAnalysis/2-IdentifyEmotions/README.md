# Identify Emotions

## Create DynamoDB Table

- Go to DynamoDB Console at https://console.aws.amazon.com/dynamodb/home?region=us-east-1#
- Click on Create Table.
 - Table name: recognize-emotions-your-name
 - Primary key: s3key
- Click "Create" to create DynamoDB table.

## Create a role for Lambda function

- Go to IAM Console at https://console.aws.amazon.com/iam/home?region=us-east-1#
- Choose 'Create Role'
- Select “AWS Service”
- Select “Lambda” and choose "Next:Permissions"
- Attach the following policies:
  - AmazonDynamoDBFullAcces
  - AmazonS3FullAccess
  - AmazonRekognitionFullAccess
  - CloudWatchFullAccess
- Click Next
- Provide a name for the role: rekognizeEmotions
- Choose 'Create role'

## Create a Lambda function to Detect Emotions

1. Go to Lambda Console at https://console.aws.amazon.com/lambda/home?region=us-east-1
2. Click 'Create function'
3. Choose 'Author from scratch'
 - Name the function: recognize-emotion-your-name.  
 - Runtime: Choose Python 2.7
 - Role: Choose an existing role
 - Existing role: rekognizeEmotions
 - Choose Create function
4. Replace the default script with the script in [recognize-emotions.py](rekognize-emotions.py).
5. Update the table name in lambda function with the name of DynamoDB table your created earlier.
6. Next, we need to add the event that triggers this lambda function. This will be an “S3:ObjectCreated” event that happens every time a face is uploaded to the face S3 bucket. Add S3 trigger from designer section on the left.
7. Configure with the following:
 - Bucket name: face-detection-your-name (you created this bucket earlier)
 - Event type- Object Created
 - Prefix- faces/
 - Filter- .jpg
 - Enable trigger- ON (keep the checkbox on)
8. Save the lambda function
9. Under 'Actions' tab choose **Publish**

## View emotions in CloudWatch Dashboard

- Go to CloudWatch Console at https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#
- Create a dashboard called “sentiment-dashboard-your-name”
- Choose Line in the widget
- Under Custom Namespaces, select “string”, “Metrics with no dimensions”, and then select all metrics.
- Next, set “Auto-refresh” to the smallest interval possible (1h), and change the “Period” to whatever works best for you (1 second or 5 seconds)

NOTE: These metrics will only appear once they have been sent to Cloudwatch via the Rekognition Lambda. It may take some time for them to appear after your model is deployed and running locally. If they do not appear, then there is a problem somewhere in the pipeline.

## Completion
You have successfully created and deployed a face detection project on DeepLens. You also modified the default project to detect faces and perform sentiment analysis on those faces.
