import boto3
from botocore.exceptions import ClientError
import datetime
import json
import csv
iam_client = boto3.client('iam')
ssm_client = boto3.client('ssm')

def lambda_handler(event, context):
 users_list = []
 details = iam_client.list_users(MaxItems=300)
 #print(details)
 users = details['Users']
 for user in users:
    username = user['UserName']
    userdetails=iam_client.get_user(UserName=username)
    #print(userdetails)
    userdetails= userdetails['User']
    if 'Tags' in userdetails.keys():
     tags= userdetails['Tags']
     for tag in tags:
        if 'email' in tag['Key']:
            tagvalue = tag['Value']
            #print("Email Address " + tagvalue)
        else:
            users_list.append(username)
    else:
     users_list.append(username) 
 print(users_list)
 users_list = str(users_list)
 ssm_response = ssm_client.put_parameter(
        Name='userlist',
        Overwrite=True,
        Value=users_list
    )
             