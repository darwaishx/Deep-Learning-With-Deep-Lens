# Detect faces, crop them and store in S3 from DeepLens

## Create S3 Bucket

_This is the bucket to which cropped faces coming from DeepLens will be stored._

1. Go to S3 in AWS Console at https://s3.console.aws.amazon.com/s3/home?region=us-east-1.
2. Click "Create bucket", and enter the following details:
*	Bucket name: _[Your name or username]-dl-faces_
*	Region: US East (N. Virginia)
3.	Click "Create".

## Inference Lambda function to Crop Faces and Send to S3

In this section you will update the lambda function that is part of face detection project to crop faces and send to S3.

1. Using your browser, open the AWS Lambda console at https://console.aws.amazon.com/lambda/home?region=us-east-1#/functions.
2. In the search box type deeplens-face-detection to find the lambda function for your project and click on the name of your lambda function.
3. Replace code in lambda function with code from [facecrop.py](facecrop.py) and click Save.
4. Click on Action and then Publish a new version.
5. Enter version description and click Publish.

## Create Your Project

1. Using your browser, open the AWS DeepLens console at https://console.aws.amazon.com/deeplens/.
2. Choose Projects, then choose Create new project.
3. On the Choose project type screen
- Choose Use a project template, then choose Face detection.

![](images/dlprojecttemplate.png)

- Scroll to the bottom of the screen, then choose Next.
4. On the Specify project details screen
   - In the Project information section:
      - Either accept the default name for the project, or type a name you prefer.
      - Either accept the default description for the project, or type a description you prefer.
   - In the Project content section:
      - Model—make sure the model is deeplens-face-detection. If it isn't, remove the current model then choose Add model. From the list of models, choose deeplens-face-detection.
      - Function—make sure the function is deeplens-face-detection. If it isn't, remove the current function then choose Add function. From the list of functions, choose deeplens-face-detection.

      ![](images/dlprojectcontent.png)

      ![](images/lambdaversion.png)

  - Under Version, select the current version that you just published.    
  - Choose Create.

This returns you to the Projects screen where the project you just created is listed with your other projects.

## Deploy your project

Next you will deploy the Face Detection project you just created.

1. From Deeplens console, On the Projects screen, choose the radio button to the left of your project name, then choose Deploy to device.

![](images/dlprojecthome.png)

2. On the Target device screen, from the list of AWS DeepLens devices, choose the radio button to the left of the device that you want to deploy this project to. An AWS DeepLens device can have only one project deployed to it at a time.

![](images/dlprojecttargetdevice.png)

3. Choose Review.

   This will take you to the Review and deploy screen.

   If a project is already deployed to the device, you will see an error message
   "There is an existing project on this device. Do you want to replace it?
   If you Deploy, AWS DeepLens will remove the current project before deploying the new project."

4. On the Review and deploy screen, review your project and choose Deploy to deploy the project.

   This will take you to to device screen, which shows the progress of your project deployment.

## View your project output

1. You need mplayer to view the project output from Deeplens device. For Windows, follow the installation instructions at this link: http://www.mplayerhq.hu/design7/dload.html
For Mac, install mplayer by using command below in the terminal window:

```
brew install mplayer
```

2. Wait until the project is deployed and you see the message Deployment of project Face-detection, version 0 succeeded. After project is successfully deployed, use the command below from terminal window to view project output stream:

```
ssh aws_cam@<IP Address of your deeplens device> cat /tmp/results.mjpeg | mplayer -demuxer lavf -lavfdopts format=mjpeg:probesize=32 -
```
Example:
```
ssh aws_cam@192.168.86.120 cat /tmp/results.mjpeg | mplayer -demuxer lavf -lavfdopts format=mjpeg:probesize=32 -
```

### Verify DeepLens is sending faces to S3
Go to S3 bucket _[Your name or username]-dl-faces_ and you should now see images coming from Deeplens.

## Completion
You have successfully created and deployed a face detection project on DeepLens. You also modified the default project so when DeepLens detects a human face, it will crop the face and store as image in S3. In the next activity, [Identify Emotions](../2-IdentifyEmotions), you will learn how Amazon Rekognition provides Deep learning-based image and video analysis capabilities including facial analysis in the cloud.
