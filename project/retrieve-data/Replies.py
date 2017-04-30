import tweepy
import json
import pprint
import csv

consumer_key = "2jxfVRFSTyufjuUuHPJfC05nD"
consumer_secret = "44lH62J3EplREpoUcODGvDiV4k1jgNHwvH0vnEToj2SY6dJofF"
access_token = "755868887300780032-pUEIgbhVw6R21zjINyKlTml6iQF7sAJ"
access_secret = "Bp8rsLKGwI8Rks1FzTVzJSu7ccoAkgDFbXqSc0CzyIFvT"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)
max_tweets = 100

query="to:sarahnferris @sarahnferris"

#Use csv writer
for tweet in tweepy.Cursor(api.search,
                           q = query,
                           since = "2017-04-22",
                           until = "2017-04-25",
                           lang = "en").items():
    csvFile = open('white-house.csv', 'a')
    csvWriter = csv.writer(csvFile)
    # print tweet.in_reply_to_status_id
    if tweet.in_reply_to_status_id == 855497861655605253:
        csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8')])
    # print tweet.created_at, tweet.text
    csvFile.close()