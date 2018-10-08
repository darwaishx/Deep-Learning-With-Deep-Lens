# Deep Learning With DeepLens and SageMaker

AI, Machine Learning and IoT projects are becoming ever more important for enterprises and startups alike. These advanced technologies have been the key innovation engine for businesses such as Amazon Go, Alexa, Amazon Robotics. In this one-day workshop, we will cover the scenarios of AI and IoT working together.

- Building and training deep learning models in the cloud using Amazon SageMaker.  
- Deploying AI models to devices like the AWS DeepLens.

We will provide a hands-on learning experience by build an end-to-end systems for face detection, recognition and verification. The workshop is designed for developers that are curious about these new technologies with no ML background assumed.   

Basic requirement: Hands-on experience with python, and basic understanding of AWS services such as S3 and Lambda.

## Agenda

### 09:00 AM - 10:30 AM
[Get to know your Device](1-KnowYourDevice)
   - Register you DeepLens device
   - Object detection with DeepLens
### 10:30 AM - 12:00 PM
[Amazon Sage Maker](2-SageMaker)
   - Launch your notebook instance and open its Jupyter interface
   - Amazon Algorithms - Reliable ML in Scale
   - Training Models with a Training Job
   - Tuning Models with Hyper-parameter Optimization (HPO)
   - Hosting Inference Endpoint
   - Build, train and deploy face detection model with Amazon SageMaker
### 12:00 PM - 01:00 PM
[Sentiment Analysis](3-SentimentAnalysis)
  - Face detection with DeepLens
  - Sentiment analysis using Rekognition
### 01:00 PM - 03:00 PM
[End-to-end solution for face detection, recognition and verification](4-FaceDetectionAndVerification)
   - Face detection with DeepLens
   - Rekognition
   - Approval Workflow
   - Bring it all together
### 02:45 PM - 03:00 PM
[Additional project ideas/Hackathon](5-ProjectIdeas)

## Clean Up
After completing the labs in this workshop ensure you delete all the resources created in your AWS account during the labs so that no further costs are incurred. Any labs where you create SageMaker instance and publish and model using SageMaker, you should also delete the endpoint (this also deletes the ML compute instance or instances, the endpoint configuration, the model and the the notebook instance. You will need to stop the instance before deleting it.
