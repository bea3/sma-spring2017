from nltk.tokenize import TweetTokenizer
from nltk.stem import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer
import string
import os

tknzr = TweetTokenizer()

all_files = os.listdir("./text_files")

for f in all_files:
    if ".py" not in f:
        all_tweets = []

        # convert text file into an array of tweets
        with open("./text_files/" + f, 'r') as myfile:
            all_tweets = myfile.read().split('\n')

        # 1. Tokenize
        print "Tokenizing " + f + "..."
        tokenized_tweets = []
        for i in range(len(all_tweets)):
            tweet = all_tweets[i]
            tweet = tweet.strip()
            if len(tweet) > 0:
                tweet = tknzr.tokenize(all_tweets[i])
                tokenized_tweets = tweet + tokenized_tweets

        # 2. Stemming
        print "Stemming " + f + "..."
        stemmer = SnowballStemmer('english')
        stemmed_tweets = []
        for tweet in tokenized_tweets:
            stemmed_tweets.append(stemmer.stem(tweet))

        # 3. Lemmatization
        print "Lemmatizing " + f + "..."
        lemmatizer = WordNetLemmatizer()
        lemmatized_tweets = []
        for tweet in stemmed_tweets:
            if tweet not in string.punctuation:
                lemmatized_tweets.append(lemmatizer.lemmatize(tweet, 'v'))

        new_file = open('./processed_files/processed_' + f, 'w')
        for x in range(len(lemmatized_tweets)):
            new_file.write(lemmatized_tweets[x].encode("UTF-8") + "\n")
        new_file.close()

        print "Saved in the processed_files directory\n"
