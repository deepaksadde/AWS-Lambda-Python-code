import requests
import json

slack_baseUrl = "https://slack.com/api/"
email_to_lookup = "pradipta.sanyal@generac.com"
slack_lookup_url = slack_baseUrl + "users.lookupByEmail?email=" + email_to_lookup
slack_bot_token = "Bearer xoxb-2936479164-2759427076709-dhgsdyabvdghrig0Qlw"


payload = ""
lookup_headers = {"Authorization": slack_bot_token}

# Retrieve Slack User Id from Email
response = requests.request(
    "GET", slack_lookup_url, headers=lookup_headers, data=payload
)
print(response.text)

slack_lookup_response = json.loads(response.text)
slack_user_id = slack_lookup_response["user"]["id"]
print("Slack User Id: " + slack_user_id)

# Send Slack Message

slack_dm_url = (
    slack_baseUrl
    + "chat.postMessage?channel="
    + slack_user_id
    + "&text=Hello! Your AWS Credentials have been rotated.&as_user=true"
)
payload = {}
dm_headers = {"Accept": "application/json", "Authorization": slack_bot_token}

slack_dm_response = requests.request(
    "POST", slack_dm_url, headers=dm_headers, data=payload
)

print(slack_dm_response.text)
