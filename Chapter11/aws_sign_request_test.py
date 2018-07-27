import os
import requests
from requests_aws_sign import AWSV4Sign
from boto3 import session

# You must provide a credentials object as per http://boto3.readthedocs.io/en/latest/guide/configuration.html#configuring-credentials
# This example attempts to get credentials based upon the local environment
# e.g. Environment Variables, assume role profiles, EC2 Instance IAM profiles
session = session.Session(
    aws_access_key_id=os.environ['aws_access_key_id'],
    aws_secret_access_key=os.environ['aws_secret_access_key'])
credentials = session.get_credentials()

# You must provide an AWS region
region = session.region_name or 'ap-south-1'

# You must provide the AWS service.  E.g. 'es' for Elasticsearch, 's3' for S3, etc.
service = 'execute-api'

url = "https://random-quote-iam.abdulwahid.info/"
auth=AWSV4Sign(credentials, region, service)
response = requests.get(url, auth=auth)

print (response.content)