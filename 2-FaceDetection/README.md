# End-to-end solution for face detection, recognition and verification

- Building face detection, recognition and verification system, including:
   - Deploy the face detection model to the device
   - Modify the lambda function to crop faces and send them to the S3 bucket
   - Check if face exists in Rekognition collection
   - If it is a new face, use step function to start an approval process to add face to collection

![](Architecture.png)

This lab has following 4 modules:
- [1-Face Detection](1-FaceDetection)
- [2-Rekognition](2-Rekognition)
- [3-ApprovalWorkflow](3-ApprovalWorkflow)
- [4-BringingItAllTogether](4-BringingItAllTogether)
