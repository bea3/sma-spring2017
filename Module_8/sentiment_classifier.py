# Beatrice Garcia
# March 30, 2017
# Module 8

import praw
import twitter
import os
from nltk.sentiment import SentimentAnalyzer

tweets = []
rcomments = []

def get_reddit_comments():
    client_id = "kPDOhCZFMTgJEw"
    client_secret = "nXHOnn76HS1DsSJ_CrHI-C-k2RU"
    user_agent ="webapp:philbert:v.1.0.0"
    username = "turtlephilbert"

    reddit = praw.Reddit(client_id=client_id,
                         client_secret=client_secret,
                         user_agent=user_agent, username=username)

    # get a random subreddit and its comments
    subreddit = reddit.random_subreddit(nsfw=False)
    subredditComments = subreddit.comments(limit=100)

    f = open(subreddit.title.encode("UTF-8") + '.txt', 'w')

    counter = 1

    for comment in subredditComments:
        f.write(comment.body.encode("UTF-8") + "\n\n")
        rcomments.append(comment.body.encode("UTF-8"))
        counter += 1

    f.close()


def get_tweets():
    consumer_key = "FhiyBRb0cz4zOoDfcHNVOyBDS"
    consumer_secret = "Q7MsbrPbFVzrwztW2KFH5JDGVpnSMhBlztwfJrLQeIGG591LST"
    access_token = "755868887300780032-FqY1RAUiznqmVMToIotldxavDEKdEe9"
    access_secret = "DV3O14tD9nTR1cVThyY1wriLMarXQoNQoudbZMHnUxYBP"

    # set up access and get tweets
    api = twitter.Api(consumer_key=consumer_key, consumer_secret=consumer_secret, access_token_key=access_token,
                      access_token_secret=access_secret)
    trump_tweets = api.GetSearch(term="trump", result_type="tweet", count=500)

    # open up file and write tweets to it
    f = open('trump_tweets.txt', 'w')

    count = 1
    for x in range(len(trump_tweets)):
        f.write(trump_tweets[x].text.encode("UTF-8") + "\n")
        tweets.append(trump_tweets[x].text.encode("UTF-8"))
        count += 1

    f.close()


def main():
    # Deletes old files to get new data
    filelist = [f for f in os.listdir(".") if f.endswith(".txt")]
    for f in filelist:
        os.remove(f)

    # Gets data
    get_reddit_comments()
    get_tweets()


if __name__ == "__main__": main()
