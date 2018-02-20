# Get to know your Device

- Registering the device.
- Creating a DeepLens project using the object detection template.
- Deploying model to the device.
- Checking the output on the IoT console and on the video stream.
- Modifying the model to focus on new objects using SageMaker
- Deploying the new model to the device
- Extending the output of the model to send SMS message using SNS

## Register your device

1. Sign in to the AWS Management Console and open the AWS DeepLens console at https://console.aws.amazon.com/deeplens/home?region=us-east-1#firstrun.
2. Choose Register device.
3. For Device name, type a name for your AWS DeepLens, then choose Next. Use only alphanumeric characters and dashes (-).
4. If this is your first time registering an AWS DeepLens device, create the following AWS Identity and Access Management (IAM) roles. They give AWS DeepLens the permissions it needs to perform tasks on your behalf. If you have already created these roles, skip to step 5.
- IAM role for AWS DeepLens
   - From the list, choose AWSDeepLensServiceRole. If AWSDeepLensServiceRole isn't listed, choose Create role in IAM and follow these steps in the IAM console.
   - Accept the DeepLens service and DeepLens use case by choosing Next: Permissions.
   - Accept the AWSDeepLensServiceRolePolicy policy by choosing Next: Review.
   - Accept the role name AWSDeepLensServiceRole and the provided description by choosing Create role. Do not change the role name.
   - Close the IAM window.

- IAM role for AWS Greengrass service
   - From the list, choose AWSDeepLensGreengrassRole. If AWSDeepLensGreengrassRole isn't listed, choose Create role in IAM and follow these steps in the IAM console.
   - Accept the Greengrass service and Greengrass use case by choosing Next: Permissions.
   - Accept the AWSGreengrassResourceAccessRolePolicy policy by choosing Next: Review.
   - Accept the role name AWSDeepLensGreengrassRole and the provided description by choosing Create role. Do not change the role name.
  - Close the IAM window.

- IAM role for AWS Greengrass device groups.
   - From the list, choose AWSDeepLensGreengrassGroupRole. If AWSDeepLensGreengrassGroupRole isn't listed, choose Create role in IAM and follow these steps in the IAM console.
   - Accept the DeepLens service and the DeepLens - Greengrass Lambda use case by choosing Next: Permissions.
   - Accept the AWSDeepLensLambdaFunctionAccessPolicy policy by choosing Next: Review.
   - Accept the role name AWSDeepLensGreengrassGroupRole and the provided description by choose Create role. Do not change the role name.
   - Close the IAM window.

- IAM role for Amazon SageMaker
   - From the list, choose AWSDeepLensSagemakerRole. If AWSDeepLensSagemakerRole isn't listed, choose Create role in IAM and follow these steps in the IAM console.
   - Accept the SageMaker service and the SageMaker - Execution use case by choosing Next: Permissions.
   - Accept the AmazonSageMakerFullAccess policy by choosing Next: Review.
   - Accept the role name AWSDeepLensSageMakerRole and the provided description by choosing Create role. Do not change the role name.
   - Close the IAM window.

- IAM role for AWS Lambda
   - From the list, choose AWSDeepLensLambdaRole. If AWSDeepLensLambdaRole isn't listed, choose Create role in IAM and follow these steps i the IAM console.
   - Accept the Lambda service and the Lambda use case by choosing Next: Permissions.
   - Accept the AWSLambdaFullAccess policy by choosing Next: Review.
   - Accept the role name AWSDeepLensLambdaRole and the provided description by choosing Create role. Do not change the role name.
   - Close the IAM window.

5. In AWS DeepLens, on the Set permissions page, choose Refresh IAM roles, then do the following:
   - For IAM role for AWS DeepLens, choose AWSDeepLensServiceRole.
   - For IAM role for AWS Greengrass service, choose AWSDeepLensGreengrassRole.
   - For IAM role for AWS Greengrass device groups, choose AWSDeepLensGreegrassGroupRole.
   - For IAM role for Amazon SageMaker, choose AWSDeepLensSagemakerRole.
   - For IAM role for AWS Lambda, choose AWSDeepLensLambdaRole.

   _Important, Attach the roles exactly as described. Otherwise, you might have trouble deploying models to AWS DeepLens._

   If any of the lists do not have the speified role, find that role in step 4, follow the directions to create the role, choose Refresh IAM roles, and return to where you were in step 5.

6. Choose Next.
7. On the Download certificate page, choose Download certificate, then choose Save File. Note where you save the certificate file because you need it later.
8. After the certificated has been downloaded, choose Register. You should see success message about your device registration like one below.

   _Important: The certificate is a .zip file. You attach it to AWS DeepLens in .zip format, so don’t unzip it. Certificates aren't reusable. You need to generate a new certificate every time you register your device._

![](assets/deviceregs1.png)

### Connect Your AWS DeepLens Device

1. Start your AWS DeepLens device by plugging the power cord into an outlet and the other end into the back of your device. Turn on the AWS DeepLens by pressing the On/Off button on the front of the device.
2. On your computer, choose the SSID for your AWS DeepLens from the list of available networks. The SSID and password are on the bottom of your device.

![](assets/ssid-connect.png)

3. Wi-Fi light should be blinking at this time. If Wi-Fi light is not blinking, you need to reset the device using a pin and restart the device.
4. If Wi-Fi light is blinking, connect to the wifi network of the device.

### Set Up Your AWS DeepLens Device

1. In a browser, open a new tab and navigate to http://192.168.0.1.

2. On the Device page:
- Connect to the network.
   - Choose your local network, type the password, then choose Next. If you are using Ethernet to connect to AWS DeepLens, choose the Ethernet option.
- Upload the certificate.
   - Locate and choose the certificate that you downloaded from the AWS DeepLens console, then choose Upload certificate.
   - The certificate is saved as a .zip file in your Downloads directory. Don't unzip the file. You attach the certificate as a .zip file.
- Configure device access.
   - Create a password for the device—You need this password to access and update your AWS DeepLens.
   - SSH server— Enable SSH as in the lab you will use SSH to connect to the device in later modules. SSH allows you to log in without using the AWS DeepLens console.
   - Automatic updates— Enable this option. Enabling automatic updates keeps your device's software up-to-date.
- Review the settings and finish setting up the device.
   - To modify settings, choose Edit for the setting that you want to change.
3. Choose Finish.

### Verify That Your AWS DeepLens Is Connected

After you set up your device, your computer automatically connects to the internet. This can take a few seconds. When your device is connected, you see the following message:

After the connection is established, you can return to the AWS DeepLens console. You are now ready to deploy an AWS DeepLens project. For more information, see Creating and Deploying an AWS DeepLens Sample Project.

![](assets/device-verified.png)

If you fail to establish a connection, return to Connect AWS DeepLens to the Network and repeat the steps for setting up your device and connecting it to the network.

# Editing a model in Amazon SageMaker

In this lab you will learn to edit a pre-trained object recognition model to perform a binary classification to classify an object as either a Hotdog or Not Hotdog. This fun exercise is based on a popular sitcom and demonstrates the extensibility of AWS DeepLens. We will edit the model in Amazon SageMaker. Amazon SageMaker is an end to end machine learning platform to train and host your models to production.

In this exercise, you will learn to:

   1. Load your notebook into an Amazon SageMaker notebook instance.
   2. Train your model in the notebook.
   3. Save your model artifacts into your S3 bucket.
   4. Import the model artifacts to DeepLens.

## Step 1- Create a bucket in S3

   1. Visit https://s3.console.aws.amazon.com/s3/home?region=us-east-1# to access Amazon S3 console.
   2. Make sure you are on the US East (N.Virginia) region. (This can be selected in the top, right-hand corner of the screen.)
   3. Click on "Create bucket".
   4. Name the bucket deeplens-sagemaker-your-full-name (Please note: It is important that is prefixed with deeplens-sagemaker prefix, else these services cannot access. Click "Next" twice.
   5. In the "Manage public permissions" section, choose "Grant public read access", and click "Next".
   6. Click "Create bucket".
   6. After you create the bucket, click on that bucket in your S3 bucket list, and create a folder named "test" in the bucket.

## Step 2- Amazon SageMaker console

   1. Visit https://console.aws.amazon.com/sagemaker/home?region=us-east-1#/dashboard to access Amazon SageMaker console.
   2. Make sure you are on the US East (N. Virginia) region.
   3. Click on notebook instances and choose Create notebook instance.
   4. Enter an instance name, choose the instance type (ml.t2.medium). Note that you will be charged for the notebook instance.
   5. For IAM role, choose "Create new role".
   6. In the screen that appears, click "Any S3 bucket", and click "Create role".
   7. Click "Create notebook instance".
   8. Verify that your instance's status changes to InService.

   ![image.png](https://raw.githubusercontent.com/aws-samples/reinvent-2017-deeplens-workshop/master/lab%20session%203/assets/1.png?token=AKs8xvmYa6FaKJhnRIeFYthghNhNIDAJks5aKA1OwA%3D%3D)

## Step 3- Open Notebook instance
   1. Choose the notebook instance and click on Open
   2. The Jupyter notebook instance will open.
   3. Download the deeplens-hotdog-or-not-hotdog.ipynb notebook from https://github.com/aws-samples/reinvent-2017-deeplens-workshop/blob/master/lab%20session%203/deeplens-hotdog-or-not-hotdog.ipynb.
   4. Open the file in a text editor and search for the string "your s3 bucket name here".  Replace that string with the name of the S3 bucket you created in the previous section.
   5. Upload it to the notebook instance by choosing the Upload option.
   4. Once uploaded, click on the notebook to launch it.

## Step 4- Execute the notebook

   1. Read through the notebook.
   2. Execute each cell by using the play button on the navigation bar or using shift+ enter or cmd + enter

   ![image.png](https://raw.githubusercontent.com/aws-samples/reinvent-2017-deeplens-workshop/master/lab%20session%203/assets/2.png?token=AKs8xt7roxuqN3uel75y9ZGA8cBW5Jgtks5aKB3cwA%3D%3D)

   3. This will result in the json and params files being uploaded to your S3 bucket (it takes a couple of minutes for the json and params file to be created).
   4. The executions have completedf when you see the following output at the end:
   ```s3.Object(bucket_name='deeplens-sagemaker-your-full-name', key='test/hotdog_or_not_model-0000.params')```
   5. Now your trained artifacts are available on S3.

Since these models are not yet optimized, they will run on the CPU and will be very slow. For the purpose of this exercise, we have provided the optimized version of the machine learning model and a lambda function that does inference on your AWS DeepLens. This optimized model runs on the on-board GPU to provide accurate and responsive inferences.

## Step 5- Create a lambda function

   1. Navigate to Lambda console: https://console.aws.amazon.com/lambda/home?region=us-east-1#/functions
   2. Make sure you are on US East-1- N.Virginia region
   3. Click on "Create function".
   4. Click "Author from scratch".
   5. Name it deeplens-hotdog-no-hotdog-your-full-name (deeplens-hotdog-not-hotdog should be the prefix)
   6. In the Runtime, change it to python 2.7
   7. Click "Choose an existing role"
   8. Choose the existing deeplens_lambda role
   9. Click "Create function".

## Step 6- Configure your lambda function

   1. In the handler box, change it to greengrassHelloWorld.function_handler
   2. In the code entry type, choose Upload a file from Amazon S3. copy paste this S3 link: https://s3.amazonaws.com/deeplens-managed-resources/lambdas/hotdog-no-hotdog/new_hot_dog_lambda.zip
   3. Click Save
   4. Make sure you verify the code you copied exists in the function

### Step 6a- Publish your function
   1. In Actions tab, click publish and provide your name_sagemaker as the description

## Step 7- Create a Project
   1. Navigate to Projects in the AWS DeepLens console
   2. Click on Create a new project
   3. Click on Create a new blank project template
   4. Give the project a name: hotdog-gpu-your-full-name
   5. Click on add model and choose the deeplens-squeezenet
   6. Click on Add function and choose the deeplens-hotdog-no-hotdog-your-full-name function
   7. Create project

## Step 8- Deploy project to AWS DeepLens

   1. Choose the project you just created
   2. Click deploy to device
   3. Choose your device
   4. Review and hit deploy

## Step 9- View the output

   1. Open the terminal. You can access the top left search icon on Ubuntu and type Terminal
   2. Copy paste the following command: mplayer -demuxer lavf -lavfdopts format=mjpeg:probesize=32 /tmp/results.mjpeg

This optimized model will let you access the GPU for running inference. Show a hotdog to your AWS DeepLens and watch its prediction.
