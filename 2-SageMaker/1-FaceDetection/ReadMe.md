# Build, train and deploy Face Detection model using Amazon SageMaker

In this module, you will learn how to build and train a face detection model using Amazon SageMaker.

## Create SageMaker Notebook Instance

1. Go to SageMaker console at https://console.aws.amazon.com/sagemaker/home?region=us-east-1#/landing
  ___Make sure you have us-east-1 selected as region.___

2. Click on Create Notebook instance

![](assets/sm01.png)

3. Under Notebook instance settings:
- Notebook instance name: Enter a name eg: DeepLearning
- Notebook instance type: ml.t2.medium
- IAM role: Click on 'Create a new role'
  - Under Create an IAM role: Select "Any S3 bucket" and click "Create role".
  ![](assets/sm02.png)
- Leave defaults for VPC, Lifecycle configuration and encryption key:
![](assets/sm03.png)
- Click 'Create notebook instance'
- You should see message on the next screen that your notebook instance is being created.
![](assets/sm04.png)

## View notebook instances

You can view all your notebook instances by choosing Notebook on the left menu. It will take couple of minutes for the notebook instance to be created.

![instances](https://user-images.githubusercontent.com/11222214/38314549-541e9140-37db-11e8-89eb-ec9be1677271.JPG)

### Step 4- Upload and Open notebook

Choose Upload button on the jupyter page

Find the SSD_Object_Detection_SageMaker_v3.ipynb file (You can find it in the sagemaker lab directory of the extracted repo. You downloaded and extracted the zip file earlier in the process)

Choose Upload

You can choose your uploaded notebook and click on 'Open'.

This will open your Jupyter notebook.

![jupyter](https://user-images.githubusercontent.com/11222214/38314946-427aa6e4-37dc-11e8-91bf-658ebe7b2a7b.JPG)

### Step 5- Execute notebook

1. Execute the cells by clicking on run button or using shift+ enter on your keyboard

![run](https://user-images.githubusercontent.com/11222214/38316244-21a07194-37df-11e8-9821-21d5d6e57976.JPG)
