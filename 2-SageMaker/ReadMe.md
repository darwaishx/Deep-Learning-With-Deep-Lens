# Amazon SageMaker

Amazon SageMaker is a fully-managed platform that enables developers and data scientists to quickly and easily build, train, and deploy machine learning models at any scale. Amazon SageMaker removes all the barriers that typically slow down developers who want to use machine learning.

Amazon SageMaker removes the complexity that holds back developer success with each of these steps. Amazon SageMaker includes modules that can be used together or independently to build, train, and deploy your machine learning models.

![](assets/sm.png)

## Learning Objectives of This Lab

In this lab you will learn the following:

- Launch your notebook instance and open its Jupyter interface
- Amazon Algorithms - Reliable ML in Scale
- Training Models with a Training Job
- Tuning Models with Hyper-parameter Optimization (HPO)
- Hosting Inference Endpoint
- Build, train and deploy face detection model with Amazon SageMaker

## Modules

This lab has following module:

- [Build Face Detection model using Amazon SageMaker](1-FaceDetection)

## Clean Up
After completing the labs in this workshop ensure you delete all the resources created in your AWS account during the labs so that no further costs are incurred. For SageMaker, you should delete the endpoint (this also deletes the ML compute instance or instances, the endpoint configuration, the model and the the notebook instance. You will need to stop the instance before deleting it.
