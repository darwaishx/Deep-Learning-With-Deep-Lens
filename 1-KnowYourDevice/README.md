# Morning Session - Get to know your Device

- Registering the device.
- Creating a DeepLens project using the object detection template.
- Deploying model to the device.
- Checking the output on the IoT console and on the video stream.
- Modifying the model to focus on new objects using SageMaker
- Deploying the new model to the device
- Extending the output of the model to send SMS message using SNS

## Register your device 
Plug in the device and go to https://aws.amazon.com/camera

{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Editing a model in Amazon SageMaker \n",
    "\n",
    "In this lab you will learn to edit a pre-trained object recognition model to perform a binary classification to classify an object as either a Hotdog or Not Hotdog. This fun exercise is based on a popular sitcom and demonstrates the extensibility of AWS DeepLens. We will edit the model in Amazon SageMaker. Amazon SageMaker is an end to end machine learning platform to train and host your models to production. \n",
    "\n",
    "In this exercise, you will learn to:\n",
    "\n",
    "1. Load your notebook into Amazon SageMaker notebook instance\n",
    "2. Train your model in the notebook\n",
    "3. Save your model artifacts into your S3 bucket\n",
    "4. Import the model artifacts to DeepLens\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Step 1- Create a bucket in S3\n",
    "\n",
    "1. Visit https://s3.console.aws.amazon.com/s3/home?region=us-east-1# to access Amazon S3 console\n",
    "2. Make sure you are on US East (N.Virginia) region\n",
    "3. Click on Create a bucket. \n",
    "4. Name the bucket- deeplens-sagemaker-your-full-name (Please note: It is important that is prefixed with deeplens-sagemaker prefix, else these services cannot access. Click Next\n",
    "5. Give the bucket public read and write access. A new bucket will be created in the account.\n",
    "6. After you create the bucket, create a folder in the bucket and name it test. "
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "collapsed": true
   },
   "source": [
    "## Step 2- Amazon SageMaker console\n",
    "\n",
    "1. Visit https://console.aws.amazon.com/sagemaker/home?region=us-east-1#/dashboard to access Amazon SageMaker console\n",
    "\n",
    "2. Make sure you are on US East (N. Virginia) region\n",
    "\n",
    "3. Click on notebook instances and choose Create notebook instance.\n",
    "\n",
    "4. Enter an instance name, choose the instance type (ml.t2.medium) and specify the IAM role for the notebook instance. Note that you will be charged for the notebook instance. \n",
    "\n",
    "5. Verify that your instance's status changes to InService.\n",
    "\n",
    "![image.png](https://raw.githubusercontent.com/aws-samples/reinvent-2017-deeplens-workshop/master/lab%20session%203/assets/1.png?token=AKs8xvmYa6FaKJhnRIeFYthghNhNIDAJks5aKA1OwA%3D%3D)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Step 3- Open Notebook instance\n",
    "\n",
    "1. Choose the notebook instance and click on Open \n",
    "\n",
    "2. The Jupyter notebook instance will open. \n",
    "\n",
    "6. Download the deeplens-hotdog-or-not-hotdog.ipynb notebook from https://github.com/aws-samples/reinvent-2017-deeplens-workshop/blob/master/lab%20session%203/deeplens-hotdog-or-not-hotdog.ipynb. Upload it to the notebook instance by choosing the Upload option. \n",
    "\n",
    "4. Once uploaded, click on the notebook to launch it."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Step 4- Execute the notebook\n",
    "\n",
    "1. Read through the notebook\n",
    "2. Execute each cell by using the play button on the navigation bar or using shift+ enter or cmd + enter\n",
    "\n",
    "![image.png](https://raw.githubusercontent.com/aws-samples/reinvent-2017-deeplens-workshop/master/lab%20session%203/assets/2.png?token=AKs8xt7roxuqN3uel75y9ZGA8cBW5Jgtks5aKB3cwA%3D%3D)\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Step 5- Provide S3 bucket name\n",
    "\n",
    "1. In the last cell, you need to provide the name of the S3 bucket you created earlier\n",
    "\n",
    "2. your s3 file path will be deeplens-sagemaker-your-full-name\n",
    "\n",
    "3. Your prefix path for key variable will be key= 'folder-name/hotdog_or_not...' In our case, since the folder is named as test, it will be key= 'test/hotdog_or_not...'\n",
    "\n",
    "4. After making the above changes, execute the cell.\n",
    "\n",
    "5. The json and params file have been uploaded to your S3 bucket. It takes a couple of minutes for the json and params file to be created.\n",
    "\n",
    "6. Your trained artifacts are available on S3.\n",
    "\n",
    "![image.png](https://raw.githubusercontent.com/aws-samples/reinvent-2017-deeplens-workshop/master/lab%20session%203/assets/3.png?token=AKs8xvZ54zFdfiKoWqYq8gdxNfjR9TXMks5aKB4WwA%3D%3D)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Since these models are not yet optimized, they will run on the CPU and will be very slow. For the purpose of this exercise, we have provided the optimized version of the machine learning model and a lambda function that does inference on your AWS DeepLens. This optimized model runs on the on-board GPU to provide accurate and responsive inferences."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Step 8- Create a lambda function\n",
    "\n",
    "1. Navigate to Lambda console: https://console.aws.amazon.com/lambda/home?region=us-east-1#/functions\n",
    "2. Make sure you are on US East-1- N.Virginia region\n",
    "3. Click on Create function\n",
    "4. Click Author from scratch\n",
    "5. Name it deeplens-hotdog-no-hotdog-your-full-name (deeplens-hotdog-not-hotdog should be the prefix)\n",
    "6. Choose an existing role\n",
    "7. Choose the existing deeplens_lambda role\n",
    "8. Click Create function"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Step 9- Configure your lambda function\n",
    "\n",
    "1. In the Runtime, change it to python 2.7\n",
    "2. In the handler box, change it to greengrassHelloWorld.function_handler\n",
    "3. In the code entry type, choose Upload a file from Amazon S3. copy paste this S3 link: https://s3.amazonaws.com/deeplens-managed-resources/lambdas/hotdog-no-hotdog/new_hot_dog_lambda.zip\n",
    "\n",
    "4. Click Save\n",
    "5. Make sure you verify the code you copied exists in the function\n",
    "\n",
    "## Step 9a- Publish your function\n",
    "1. In Actions tab, click publish and provide your name_sagemaker as the description"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Step 10- Create a Project\n",
    "\n",
    "1. Navigate to Projects in the AWS DeepLens console\n",
    "\n",
    "2. Click on Create a new project\n",
    "\n",
    "3. Click on Create a new blank project template\n",
    "\n",
    "4. Give the project a name: hotdog- gpu- your full name-\n",
    "\n",
    "5. Click on add model and choose the deeplens-squeezenet\n",
    "\n",
    "6. Click on Add function and choose the deeplens-hotdog-no-hotdog-your-full-name function\n",
    "\n",
    "7. Create project\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Step 11- Deploy project to AWS DeepLens\n",
    "\n",
    "1. Choose the project you just created\n",
    "\n",
    "2. Click deploy to device\n",
    "\n",
    "3. Choose your device\n",
    "\n",
    "4. Review and hit deploy\n",
    "\n",
    "\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Step 12- View the output\n",
    "\n",
    "1. open the terminal. You can access the top left search icon on Ubuntu and type Terminal\n",
    "\n",
    "2. copy paste the following command: mplayer -demuxer lavf -lavfdopts format=mjpeg:probesize=32 /tmp/results.mjpeg"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "This optimized model will let you access the GPU for running inference. Show a hotdog to your AWS DeepLens and watch its prediction. "
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.6.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
