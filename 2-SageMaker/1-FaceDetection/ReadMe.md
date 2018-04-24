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

- Leave defaults for VPC, Lifecycle configuration and encryption key and click 'Create notebook instance'.

![](assets/sm03.png)

- You should see message on the next screen that your notebook instance is being created.

![](assets/sm04.png)

## View Notebook Instance

Once the status of your notebook instance is in InService, click on link "Open" under Actions.

![](assets/sm05.png)

You should see Jupyter UI with sample-notebooks folder that contains various sample notebooks.

![](assets/sm06.png)

## Upload and Open Notebook

You can upload individual notebooks using Jypyter UI, but in this lab we will use git to bring notebook in our SageMaker instance.

- Click on New and choose Terminal from the drop down list.

![](assets/sm07.png)

- You should get a console in a new browser tab:

![](assets/sm08.png)

- Type: "cd SageMaker" command to go to SageMaker directory.
- Type: "git clone https://github.com/darwaishx/Deep-Learning-With-Deep-Lens.git" command to clone github repo.
- Type: "ls" command and you should now see a folder "Deep-Learning-With-Deep-Lens"

![](assets/sm09.png)

- Go back to Jupyter UI, and you should see folder "Deep-Learning-With-Deep-Lens".
- Click on "Deep-Learning-With-Deep-Lens", then "2-SageMaker", then "1-FaceDetection" and click on notebook FaceDetection.ipyb


Choose Upload button on the jupyter page

Find the SSD_Object_Detection_SageMaker_v3.ipynb file (You can find it in the sagemaker lab directory of the extracted repo. You downloaded and extracted the zip file earlier in the process)

Choose Upload

You can choose your uploaded notebook and click on 'Open'.

This will open your Jupyter notebook.

![jupyter](https://user-images.githubusercontent.com/11222214/38314946-427aa6e4-37dc-11e8-91bf-658ebe7b2a7b.JPG)

### Step 5- Execute notebook

1. Execute the cells by clicking on run button or using shift+ enter on your keyboard

![run](https://user-images.githubusercontent.com/11222214/38316244-21a07194-37df-11e8-9821-21d5d6e57976.JPG)
