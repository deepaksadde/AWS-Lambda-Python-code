import boto3
from botocore.exceptions import ClientError
import datetime
import json
import csv
iam_client = boto3.client('iam')
ssm_client = boto3.client('ssm')

def lambda_handler(event, context):
 #ssm_response = ssm_client.get_parameters(
                            #  Names=[
                      #       'userlist',])
 #users_list_not_rotate = ssm_response['Parameters'][0]['Value']
 users_list = []
 details = iam_client.list_users(MaxItems=300)
 #print(details)
 users = details['Users']
 for user in users:
    username = user['UserName']
    userdetails=iam_client.get_user(UserName=username)
    userdetails= userdetails['User']
    #print(userdetails)
    if 'Tags' in userdetails.keys():
     tags= userdetails['Tags']
     print(tags)
     print(username)
     for tag in tags:
        if 'email' in tag['Key']:
            tagvalue = tag['Value']
            break
            #print("Email Address " + tagvalue)
        else:
            if 'generac.com' in username:
             response = iam_client.tag_user(
                        UserName=username,
                         Tags=[
                              {
                          'Key': 'email',
                          'Value': username
                           },
                          ]
                          )
               
            else:
              users_list.append(username)
    else:
      if 'generac.com' in username:
             response = iam_client.tag_user(
                        UserName=username,
                         Tags=[
                              {
                          'Key': 'email',
                          'Value': username
                           },
                          ]
                          )
               
      else:
             users_list.append(username)
 print(users_list)
 users_list = str(users_list)
 ssm_response = ssm_client.put_parameter(
        Name='userlist',
        Overwrite=True,
        Value=users_list
    )
             