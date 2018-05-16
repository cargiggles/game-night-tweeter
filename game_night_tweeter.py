# Andrew Cargill
# Game Night Tweeter
# 2018-05-06

import os
import random

dir = os.path.dirname(__file__)
quotes_file = os.path.join(dir, 'quotes.txt')

with open (quotes_file, 'r') as quotes:
    quotes = quotes.read()

# Each new line in the file is now an entry in the quote_array array
quote_array = quotes.splitlines()
quote = quote_array.pop(random.randrange(len(quote_array)))
print quote

# the quote has been saved in that string but removed from the array. The "quote_array" can now be saved back into s3
#print quote_array
