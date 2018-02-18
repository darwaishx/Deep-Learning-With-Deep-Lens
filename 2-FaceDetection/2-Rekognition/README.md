
# Lab 3 - Rekognition (including IAM and SES setup)

## Prerequisites
1.	Install the AWS CLI by following the instructions at the following link: https://docs.aws.amazon.com/cli/latest/userguide/installing.html
2.	Configure the AWS CLI by following the instructions at the following link: https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html
3.	Log into the AWS Console before proceeding with the steps below: https://console.aws.amazon.com
4.	For all steps (except IAM steps), ensure that the "US East (N Virginia)" region is selected in the top, right-hand corner of console screen (see screen-shot below).

![](images/Region.png)


## 2. Register Your Email Address With SES

_SES will be used to send an email from the “StartWorkflow” Lambda function we will create later in this workshop.  In order to do this, your email address must be registered with SES._

1.	In the AWS Console, click on “Services” in the top, left-hand corner of the screen, and click on “Simple Email Service” (you can find it by typing _ses_ into the search field at the top of the screen).
2.	Click on “Manage Identities”
3.	On the left-hand side of the page, click “Email Addresses”, and then click “Verify a New Email Address”.
4.	Enter your email address and click “Verify This Email Address”.
5.	A verification email will be sent to your email address.  Open your email and click the verification link in that email.


## 3. Create Rekognition Collection

_Rekognition will be consulted in order to check whether a face in the image sent by DeepLens is recognized (i.e. whether it exists in our Rekognition collection)._

1.	On your laptop, either open a terminal window (Mac) or cmd (Windows) in order to use the AWS CLI.
2.	Type the following AWS CLI command to create a Rekognition collection:
```aws rekognition create-collection --collection-id "aiweek" --region us-east-1```
3.	Verify that your Rekognition collection has been created:
```aws rekognition list-collections --region us-east-1```
4.	With the following command, you will see that there are currently no faces in your newly-created collection:
```aws rekognition list-faces --collection-id "aiweek" --region us-east-1```
5.	Add a face to your collection (use the image from the S3 bucket that you created in Lab 2)
```aws rekognition index-faces --image '{"S3Object":{"Bucket":"[Your name or username]-ml-bucket","Name":"[image_name]"}}' --collection-id "aiweek" --detection-attributes "ALL" --region us-east-1```
6.	Now list the faces in your collection again:
```aws rekognition list-faces --collection-id "aiweek" --region us-east-1```


_**Lab 3 Complete!  [Next: Lab 4 - Approval Verification Website](../4-Approval%20Verification%20Website/README.md)**_
