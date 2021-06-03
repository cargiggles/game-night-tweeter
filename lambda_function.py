# Andrew Cargill
# Game Night Tweeter
# 2021-06-01 - v2.1 - Migrating From SNS to Twilio To Send SMS Messages

import base64
import boto3 
import os
import random
import requests
import twitter

# AWS Constants
BUCKET_NAME = os.environ['BUCKET_NAME']

# Twitter Constants
ACCESS_KEY_TOKEN = os.environ['ACCESS_KEY_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']
CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']

# Twilio Constants
TWILIO_ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
TWILIO_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
TWILIO_PHONE_NUMBER = os.environ['TWILIO_PHONE_NUMBER']
MY_PHONE_NUMBER = os.environ['MY_PHONE_NUMBER']

def get_auth_header():
   auth_string = TWILIO_ACCOUNT_SID + ":" + TWILIO_AUTH_TOKEN
   auth_string_bytes = auth_string.encode("ascii")
   auth_base_64_bytes = base64.b64encode(auth_string_bytes)
   auth_base_64_string = auth_base_64_bytes.decode("ascii")

   return "Basic " + auth_base_64_string

def send_twilio_sms(message):
   url = "https://api.twilio.com/2010-04-01/Accounts/" + TWILIO_ACCOUNT_SID + "/Messages"
   payload="To=" + MY_PHONE_NUMBER + "&From=" + TWILIO_PHONE_NUMBER + "&Body=" + message
   headers = {
      "Authorization": get_auth_header(),
      "Content-Type": "application/x-www-form-urlencoded"
   }
   response = requests.request("POST", url, headers = headers, data = payload)
   print(response.text)

def twitter_post(quote):
    api = twitter.Api(consumer_key = CONSUMER_KEY,
    consumer_secret = CONSUMER_SECRET,
    access_token_key = ACCESS_KEY_TOKEN,
    access_token_secret = ACCESS_TOKEN_SECRET)

    status = api.PostUpdate(quote)
    print((status.text))

def lambda_handler(event, context):
    s3 = boto3.resource('s3')
    s3.Bucket(BUCKET_NAME).download_file("quotes.txt", "/tmp/quotes.txt")

    quotes_file = "/tmp/quotes.txt"

    with open(quotes_file, "r", encoding = "utf-8") as rf:
        quotes = rf.read()

    quote_list = [_f for _f in quotes.splitlines() if _f]

    if quote_list: # If quote_list contains items
        quote = quote_list.pop(random.randrange(len(quote_list)))
        twitter_post(quote)
    else:
        message = "The quote well's run dry!"
        send_twilio_sms(message)

    with open(quotes_file, "w", encoding = "utf-8") as wf:
        wf.write("\n".join(quote_list))

    s3.meta.client.upload_file(quotes_file, BUCKET_NAME, "quotes.txt")
