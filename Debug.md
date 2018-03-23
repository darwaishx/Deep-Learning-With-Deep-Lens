#Local Resources

##Path for lambda deployment
/opt/awscam/greengrass/ggc/deployemnent (should see arn of lambda)

#Stop Greegrass service
sudo systemctl stop greengrassd.service

#Start Greengrass service
sudo systemctl start greengrassd.service

#Install AWS SDK
sudo pip install boto3

#Open File EXplorer with admin rights to see other related directories
sudo nautilus
