# Get to know your Device

- Registering the device.
- Creating a DeepLens project using the object detection template.
- Deploying model to the device.
- Checking the output on the IoT console and on the video stream.
- Modifying the model to focus on new objects using SageMaker
- Deploying the new model to the device
- Extending the output of the model to send SMS message using SNS

## Register your device
Plug in the device and go to https://aws.amazon.com/camera

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
