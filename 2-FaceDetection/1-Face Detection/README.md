# Lab 1 - Face Detection Using Deep Lens

## Create Your Project

1. Using your browser, open the AWS DeepLens console at https://console.aws.amazon.com/deeplens/.
2. Choose Projects, then choose Create new project.
3. On the Choose project type screen
- Choose Use a project template, then choose Face detection.
- Scroll to the bottom of the screen, then choose Next.
4. On the Specify project details screen
  a. In the Project information section:
   - Either accept the default name for the project, or type a name you prefer.
   - Either accept the default description for the project, or type a description you prefer.
  b. In the Project content section:
   - Model—make sure the model is deeplens-object-detection. If it isn't, remove the current model then choose Add model. From the list of models, choose deeplens-object-detection.
   - Function—make sure the function is deeplens-object-detection. If it isn't, remove the current function then choose Add function. From the list of functions, choose deeplens-object-detection.
  c. Choose Create.

This returns you to the Projects screen where the project you just created is listed with your other projects.

## Deploy your project

In this walkthrough, you deploy the Object Detection project.

Your web browser is the interface between you and your AWS DeepLens device. You perform all of the following activities on your browser after logging on to AWS:

1. On the Projects screen, choose the radio button to the left of your project name, then choose Deploy to device.

2. On the Target device screen, from the list of AWS DeepLens devices, choose the radio button to the left of the device that you want to deploy this project to. An AWS DeepLens device can have only one project deployed to it at a time.

3. Choose Review.

   If a project is already deployed to the device, you will see an error message that deploying this project will overwrite the project that is already running on the device. Choose Continue project.

   This will take you to the Review and deploy screen.

4. On the Review and deploy screen, review your project and choose either Previous to go back and make changes, or Deploy to deploy the project.

Important
Deploying a project incurs costs for the AWS services that are used to run the project.

For instructions on viewing your project's output, see Viewing AWS DeepLens Project Output.
