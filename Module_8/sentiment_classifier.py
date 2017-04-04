# Beatrice Garcia
# March 30, 2017
# Module 8

import praw
import twitter
import nltk
import json
import sys
import csv
import pprint

negative_tweets = []
positive_tweets = []
rcomments = []
word_features = dict()
orioles_tweet = []

reload(sys)
sys.setdefaultencoding('utf-8')


def get_reddit_comments():
    print "Getting some Reddit data..."
    global rcomments
    client_id = "kPDOhCZFMTgJEw"
    client_secret = "nXHOnn76HS1DsSJ_CrHI-C-k2RU"
    user_agent ="webapp:philbert:v.1.0.0"
    username = "turtlephilbert"

    reddit = praw.Reddit(client_id=client_id,
                         client_secret=client_secret,
                         user_agent=user_agent, username=username)

    # get an Orioles-related subreddit
    subreddits = reddit.subreddits.search_by_name("orioles", include_nsfw=False)
    subredditComments = subreddits[0].comments(limit=50)

    for comment in subredditComments:
        rcomments.append(comment.body.encode("UTF-8"))


def get_tweets():
    print "Getting some tweets..."
    global orioles_tweet
    consumer_key = "lWwcZksOC8MhoesnaZw6gLXrh"
    consumer_secret = "jZSHcmzZJc1po9Af77SauPAIEoC1HxQfAZlLVPwSKTvzn8EJGD"
    access_token = "755868887300780032-f7yUJ4uJ7Fl6nsChQQrmpIXdDjMkUKy"
    access_secret = "x5E7C1v8maJ5XB31mU3T4B8EeRdM5TyEUhEyFWtSDY9I2"

    # set up access and get tweets
    api = twitter.Api(consumer_key=consumer_key, consumer_secret=consumer_secret, access_token_key=access_token,
                      access_token_secret=access_secret)
    retrieved_tweets = api.GetSearch(term="orioles", result_type="tweet", count=50)

    for x in range(len(retrieved_tweets)):
        orioles_tweet.append(retrieved_tweets[x].text.encode("UTF-8"))


def parse_training_data():
    print "Parsing Training data..."
    with open('negative_tweets.json') as data_file:
        data = json.load(data_file)
        for tweet in data:
            text = tweet["text"].encode('utf-8')
            neg_tweet = (text, "negative")
            negative_tweets.append(neg_tweet)

    with open('positive_tweets.json') as data_file:
        data = json.load(data_file)
        for tweet in data:
            text = tweet["text"].encode('utf-8')

            pos_tweet = (text, "positive")
            positive_tweets.append(pos_tweet)


def clean_tweets(tweets):
    print "Cleaning data..."
    big_string = ""
    for (words, sentiment) in tweets:
        sentence = " ".join(words)
        sentence = ''.join([i if ord(i) < 128 else ' ' for i in sentence])
        sentence = sentence.replace("\"", "")
        big_string = big_string + " " + sentence
    return big_string


def extract_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features


def main():
    global orioles_tweet
    global rcomments

    # Gets data
    get_reddit_comments()
    get_tweets()

    parse_training_data()

    # layout and train data
    print "Gathering training data..."
    tweets = []
    for (words, sentiment) in positive_tweets + negative_tweets:
        words_filtered = [e.lower() for e in words.split() if len(e) >= 3 and e.startswith("@") is False and e.startswith("http") is False]
        tweets.append((words_filtered, sentiment))

    all_words = clean_tweets(tweets)

    tokens = nltk.tokenize.word_tokenize(all_words)
    fdist = nltk.FreqDist(tokens)
    global word_features
    word_features = fdist.keys()

    print "Training the classifier..."
    training_set = nltk.classify.apply_features(extract_features, tweets)

    # classify data
    print "Classifying training set...This takes a while..."
    classifier = nltk.NaiveBayesClassifier.train(training_set)

    # write submissions and its comments in a CSV file
    with open('classified_orioles_tweets.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Result', 'Tweet'])
        for orioles_tweet in orioles_tweet:
            result = classifier.classify(extract_features(orioles_tweet.split()))
            writer.writerow([result, orioles_tweet])
            pprint.pprint([result, orioles_tweet])

    with open('classified_orioles_reddit_comments.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Result', 'Comment'])
        for comment in rcomments:
            result = classifier.classify(extract_features(comment.split()))
            writer.writerow([result, comment])
            pprint.pprint([result, comment])


if __name__ == "__main__": main()
