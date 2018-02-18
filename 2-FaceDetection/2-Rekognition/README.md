
# Rekognition (Deep learning-based image and video analysis)

## Prerequisites
1.	Install the AWS CLI by following the instructions at the following link: https://docs.aws.amazon.com/cli/latest/userguide/installing.html
2.	Configure the AWS CLI by following the instructions at the following link: https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html
3.	Log into the AWS Console before proceeding with the steps below: https://console.aws.amazon.com

## Create Rekognition Collection

_Rekognition will be consulted in order to check whether a face in the image sent by DeepLens is recognized (i.e. whether it exists in our Rekognition collection)._

1.	On your laptop, either open a terminal window (Mac) or cmd (Windows) in order to use the AWS CLI.
2.	Type the following AWS CLI command to create a Rekognition collection:
```
aws rekognition create-collection --collection-id "dl-faces" --region us-east-1
```
3.	Verify that your Rekognition collection has been created:
```
aws rekognition list-collections --region us-east-1
```
4.	With the following command, you will see that there are currently no faces in your newly-created collection:
```
aws rekognition list-faces --collection-id "dl-faces" --region us-east-1
```
5.	Add a face to your collection by using an image from S3 bucket you created in previous module.
```
aws rekognition index-faces --image '{"S3Object":{"Bucket":"[Your name or username]-dl-faces","Name":"[image_name]"}}' --collection-id "dl-faces" --detection-attributes "ALL" --region us-east-1
```
6.	Now list the faces in your collection again:
```
aws rekognition list-faces --collection-id "aiweek" --region us-east-1
```
7. To delete a face from your collection, use the face-id
```
aws rekognition delete-faces --collection-id "dl-faces" --face-ids "FACE-ID-To-DELETE, GET FaceID FROM list-faces"
```
