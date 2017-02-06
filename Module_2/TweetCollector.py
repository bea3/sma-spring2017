# Beatrice Garcia
# January 31, 2017
# Module 2 HW

#This script collects 100 tweets about Trump and dumps them into a file called trump_tweets.txt

import twitter

consumer_key = "FhiyBRb0cz4zOoDfcHNVOyBDS"
consumer_secret = "Q7MsbrPbFVzrwztW2KFH5JDGVpnSMhBlztwfJrLQeIGG591LST"
access_token = "755868887300780032-FqY1RAUiznqmVMToIotldxavDEKdEe9"
access_secret = "DV3O14tD9nTR1cVThyY1wriLMarXQoNQoudbZMHnUxYBP"

#set up access and get tweets
api = twitter.Api(consumer_key=consumer_key, consumer_secret=consumer_secret, access_token_key=access_token, access_token_secret=access_secret)
trump_tweets = api.GetSearch(term="taylorswift", result_type="tweet", count=100)

#open up file and write tweets to it
f = open('taylor_swift_tweets.txt', 'w')
for x in range(len(trump_tweets)):
    f.write(trump_tweets[x].text.encode("UTF-8") + "\n")