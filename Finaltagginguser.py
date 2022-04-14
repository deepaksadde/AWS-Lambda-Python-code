import boto3
from botocore.exceptions import ClientError
import datetime
import json
import sys
import csv
iam_client = boto3.client('iam')
ssm_client = boto3.client('ssm')

def tag_user(username):
 
  response = iam_client.tag_user(
                        UserName=username,
                         Tags=[
                              {
                          'Key': 'email',
                          'Value': username
                           },
                          ]
                          )
               
 
def lambda_handler(event, context):
 users_list = []
 users = []
 #details = iam_client.list_users(MaxItems=300)
 marker = None
 while True:
    if marker:
        response_iterator = iam_client.list_users(
            Marker=marker
        )
    else:
        response_iterator = iam_client.list_users(
            MaxItems=5
        )
    print("Next Page : {} ".format(response_iterator['IsTruncated']))
    for user in response_iterator['Users']:
      usr = (user['UserName'])
      users.append(usr)
    if response_iterator['IsTruncated'] == True:
        marker = response_iterator['Marker']
    else:
        break

 #print(response_iterator)
 #print(users)
 #users = details['Users']
 for username in users:
    #username = user['UserName']
    userdetails=iam_client.get_user(UserName=username)
    #print(userdetails)
    userdetails= userdetails['User']
    #print(userdetails)
    tag_list = []
    if 'Tags' in userdetails.keys():
     tags= userdetails['Tags']
     print(username)
     print(tags)
     for tag in tags:
        tag_list.append(tag['Key'])
     print(tag_list)
     if 'email' in tag_list:
            tagvalue = tag['Value']
            #print("Email Address " + tagvalue)
     else:
            if 'generac.com' in username:
              tag_user(username)
            else:
              users_list.append(username)
            
    else:
      if 'generac.com' in username:
             tag_user(username)  
               
      else:
             users_list.append(username)
 print(users_list)
 users_list = str(users_list)
 ssm_response = ssm_client.put_parameter(
        Name='userlist',
        Overwrite=True,
        Value=users_list
    )
             