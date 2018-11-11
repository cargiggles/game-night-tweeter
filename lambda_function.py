# Andrew Cargill
# Game Night Tweeter
# 2018-11-10 - v2.0 - Conversion From Python 2 to 3

import boto3 
import os
import random
import twitter

# AWS Constants
BUCKET_NAME = os.environ['BUCKET_NAME']
PHONE_NUMBER = os.environ['PHONE_NUMBER']

# Twitter Constants
ACCESS_KEY_TOKEN = os.environ['ACCESS_KEY_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']
CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']

def send_sns_sms(phone_number, message):
    sns = boto3.client('sns')
    print(sns.publish(PhoneNumber = phone_number, Message = message))

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
        quote = quote_list.pop(random.randrange(len(quote_list))).capitalize()
        twitter_post(quote)
    else:
        message = "The quote well's run dry!"
        send_sns_sms(PHONE_NUMBER, message)

    with open(quotes_file, "w", encoding = "utf-8") as wf:
        wf.write("\n".join(quote_list))

    s3.meta.client.upload_file(quotes_file, BUCKET_NAME, "quotes.txt")
