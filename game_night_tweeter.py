# Andrew Cargill
# Game Night Tweeter
# 2018-05-06

import os
import random
import twitter

dir = os.path.dirname(__file__)
quotes_file = os.path.join(dir, 'quotes.txt')

with open (quotes_file, 'r') as quotes:
    quotes = quotes.read()

# Each new line in the file is now an entry in the quote_array array
quote_list = quotes.splitlines()
quote = quote_list.pop(random.randrange(len(quote_list)))
print quote

# def twitter_post(quote):
    # insert code here

# def save_file():
    # insert code to save quote_list back into quotes.txt line by line
    # note: the quote posted online has been saved in the "quote" variable, but removed from the "quote_list" when we re-save it

# def save_to_s3():
    # insert code to save quote_list into s3 instead using boto3 for AWS
