#!/usr/bin/python3.6
import urllib3
import boto3
from botocore.exceptions import ClientError
import datetime
import json
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
iam_client = boto3.client('iam')
sns_client = boto3.client('sns')
http = urllib3.PoolManager()
def list_access_key(user, days_filter, status_filter):
    keydetails=iam_client.list_access_keys(UserName=user)
    key_details={}
    user_iam_details=[]
   
    # Some user may have 2 access keys.
    for keys in keydetails['AccessKeyMetadata']:
        if (days:=time_diff(keys['CreateDate'])) >= days_filter and keys['Status']==status_filter:
            key_details['UserName']=keys['UserName']
            key_details['AccessKeyId']=keys['AccessKeyId']
            key_details['days']=days
            key_details['status']=keys['Status']
            user_iam_details.append(key_details)
            key_details={}
   
    return user_iam_details
    
def get_user_info(username):
    print("username " + username)
    userdetails=iam_client.get_user(UserName=username)
    tags= userdetails['User']['Tags']
    for tag in tags:
        if 'email' in tag['Key']:
            tagvalue = tag['Value']
    logger.info(f"Email Address {tagvalue}")
    
    return tagvalue

def send_access_secret_key(emailid):

    #message = {"Access Key" : access_key, "Secret Key " : secret_key}
    message = {"Email" : emailid}
    message1 = json.dumps(message)
    
    url = "https://hooks.slack.com/services/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"
    msg = {
        "channel": "#slacknotificationfromsns",
        "username": "WEBHOOK_USERNAME",
        "text": message1,
        "icon_emoji": ""
    }
    
    encoded_msg = json.dumps(msg).encode('utf-8')
    resp = http.request('POST',url, body=encoded_msg)
    print({
        "message": message1, 
        "status_code": resp.status, 
        "response": resp.data
    })
    
    
    
    #sns_client.publish(
    #TargetArn="arn:aws:sns:us-east-1:647587844964:new_posts",
   # Message=json.dumps(message))
    #logger.info("Message has been published to SNS topic")
    
    
def time_diff(keycreatedtime):
    now=datetime.datetime.now(datetime.timezone.utc)
    diff=now-keycreatedtime
    return diff.days
def create_key(username):
    access_key_metadata = iam_client.create_access_key(UserName=username)
    access_key = access_key_metadata['AccessKey']['AccessKeyId']
    secret_key = access_key_metadata['AccessKey']['SecretAccessKey']
    print(access_key + " Access key has been created")
    print(secret_key + " Secret key has been created")
    
    return access_key,secret_key
def disable_key(access_key, username):
    try:
        iam_client.update_access_key(UserName=username, AccessKeyId=access_key, Status="Inactive")
        print(access_key + " has been disabled.")
    except ClientError as e:
        print("The access key with id %s cannot be found" % access_key)
def delete_key(access_key, username):
    try:
        iam_client.delete_access_key(UserName=username, AccessKeyId=access_key)
        print (access_key + " has been deleted.")
    except ClientError as e:
        print("The access key with id %s cannot be found" % access_key)
def lambda_handler(event, context):
    # details = iam_client.list_users(MaxItems=300)
    # print(details)
    #users = details['Users']
    #for user in users:
      #user_iam_details=list_access_key(user=user, days_filter=90, status_filter='Inactive')
    user='terraform_user'
    user_iam_details=list_access_key(user=user,days_filter=0,status_filter='Active')
    for _ in user_iam_details:
        emailid = get_user_info(username=_['UserName'])
        #disable_key(access_key=_['AccessKeyId'], username=_['UserName'])
        #delete_key(access_key=_['AccessKeyId'], username=_['UserName'])
        #access_key,secret_key = create_key(username=_['UserName'])
        send_access_secret_key(emailid)
        
    
   
    return {
        'statusCode': 200,
        'body': list_access_key(user=user,days_filter=0,status_filter='Active')
    }