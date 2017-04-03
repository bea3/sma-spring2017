# Christine Sowa
# Social Media Analytics Class
# Module 8
# Sentiment Analysis of Reddit and Twitter data

from tweepy import OAuthHandler
import tweepy
import urllib2
import json
from unidecode import unidecode

CKEY = 'z4BiE0xRkkbFO7EzMC5sF6Utf'
CSECRET = 'fsAng9rf8ubixgg7SCdJNECEo1futVHCcAIQqApRZGwR0Sw1ZU'
ATOKEN = '356578335-M92lqZaoGuGmp3gNRLi8DDpNTz6Qv62KPY5WJz0Q'
ATOKENSECRET = 'VQNFrxu905eZMHbIZhatUupRkkdFfNv2ofAYywGM6LO0M'

URL_SENTIMENT140 = "http://www.sentiment140.com/api/bulkClassifyJson"

POLITICIAN = "Trump"
LIMIT = 2500
LANGUAGE = 'es'


def parse_response(json_response):
    negative_tweets, positive_tweets = 0, 0
    for j in json_response["data"]:
        if int(j["polarity"]) == 0:
            negative_tweets += 1
        elif int(j["polarity"]) == 4:
            positive_tweets += 1
    return negative_tweets, positive_tweets


def parse_response_text(json_response):
    negative_tweets_text = []
    positive_tweets_text = []
    for j in json_response["data"]:
        if int(j["polarity"]) == 0:
            negative_tweets_text.append(j)
        elif int(j["polarity"]) == 4:
            positive_tweets_text.append(j)
    return negative_tweets_text, positive_tweets_text


def main():
    auth = OAuthHandler(CKEY, CSECRET)
    auth.set_access_token(ATOKEN, ATOKENSECRET)
    api = tweepy.API(auth)
    tweets = []

    for tweet in tweepy.Cursor(api.search,
                               q=POLITICIAN,
                               result_type='recent',
                               include_entities=True,
                               lang=LANGUAGE).items(LIMIT):
        aux = {"text": unidecode(tweet.text.replace('"', '')), "language": LANGUAGE, "query": POLITICIAN,
               "id": tweet.id}
        tweets.append(aux)

    result = {"data": tweets}

    req = urllib2.Request(URL_SENTIMENT140)
    req.add_header('Content-Type', 'application/json')
    response = urllib2.urlopen(req, str(result))
    json_response = json.loads(response.read())
    negative_tweets, positive_tweets = parse_response(json_response)
    negative_tweets_text, positive_tweets_text = parse_response_text(json_response)

    # print "Positive Tweets: " + str(positive_tweets)
    # print "Negative Tweets: " + str(negative_tweets)
    print "Positive Tweets: "
    for tweet in positive_tweets_text:
        print tweet
    print "Negative Tweets: " + negative_tweets_text


if __name__ == '__main__':
    main()

