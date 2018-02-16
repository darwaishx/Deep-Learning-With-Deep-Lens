# Create Lambda Functions
### 4.1 Create the “StartWorkflow” Lambda Function
1. In the AWS Console, click on “Services” in the top, left-hand corner of the screen, and click on “Lambda” (you can find it by typing lambda into the search field at the top of the screen).
2. Click “Create a function”, and enter the following details:
- Name: StartWorkflow
- Runtime: Python 3.6
- Role: Choose an existing role
- Role name: AI_ML_Lambda_Role
3. Click “Create function”.
4. In the "Add Triggers" section on the left-hand side of the page, click "S3".
5. In the "Configure triggers" section that appears at the bottom of the screen, configure the
following details:
o Bucket: [Select the name of the bucket you created in section 1, step 2 above] o Event type: Object Created (All)
o Enable trigger: Yes [Checked]
6. Click "Add" (at the bottom of the page), and then click "Save" (at the top of the page).
7. Take note of your AWS Account number that is displayed at the top of the screen (e.g. "
ARN - arn:aws:lambda:us-west-2:111111111111:function:StartWorkflow"). You will use
this in step 10 below. Copy it into a text file for use in later steps also.
8. Now click on the "StartWorkflow" icon in the center of the screen, and a "Function code"
section will appear at the bottom of the screen (scroll down).
9. Delete the existing code in that section, and replace it with [this code ](lambda.py).
10. In the code that you have just pasted, you will see two instances of the following string
(search for them): 111111111111
11. You must replace those instances with your own AWS Account number, which you
noted in step 7 above.
12. Also in the code that you have just pasted, you will see one instance of the following
string (it's near the end of the code): ki-aiweek-web
13. You must replace that with name of the bucket you created in section 1.2, step 1 above.
14. Also in the code that you have just pasted, you will see the following lines:
 SENDER = "kashii@amazon.com"
 RECIPIENT = "kashii@amazon.com"
15. You must replace those email addresses with your own email address (the same one you used in section 3 above).
16. Click "Save".
