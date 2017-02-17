from nltk.tokenize import TweetTokenizer
from nltk.stem import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer
import string

tknzr = TweetTokenizer()

all_tweets = []

# convert text file into an array of tweets
with open('trump_tweets.txt', 'r') as myfile:
    all_tweets = myfile.read().split('\n')

# 1. Tokenize
tokenized_tweets = []
for i in range(len(all_tweets)):
    tweet = all_tweets[i]
    tweet = tweet.strip()
    if len(tweet) > 0:
        tweet = tknzr.tokenize(all_tweets[i])
        tokenized_tweets = tweet + tokenized_tweets

# 2. Stemming
stemmer = SnowballStemmer('english')
stemmed_tweets = []
for tweet in tokenized_tweets:
    stemmed_tweets.append(stemmer.stem(tweet))

# 3. Lemmatization
lemmatizer = WordNetLemmatizer()
lemmatized_tweets = []
for tweet in stemmed_tweets:
    if tweet not in string.punctuation:
        lemmatized_tweets.append(lemmatizer.lemmatize(tweet, 'v'))

f = open('trump_processed.txt', 'w')
for x in range(len(lemmatized_tweets)):
    f.write(lemmatized_tweets[x].encode("UTF-8") + "\n")
f.close()





