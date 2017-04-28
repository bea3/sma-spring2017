import csv
import json
import os
import pprint
import nltk

negative_tweets = []
positive_tweets = []
word_features = dict()


def extract_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features


def clean_tweets(tweets):
    print "Cleaning data..."
    big_string = ""
    for (words, sentiment) in tweets:
        sentence = " ".join(words)
        sentence = ''.join([i if ord(i) < 128 else ' ' for i in sentence])
        sentence = sentence.replace("\"", "")
        big_string = big_string + " " + sentence
    return big_string


def parse_training_data():
    limit = 50000
    print "Parsing Training data with " + str(limit) + " tweets..."
    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, '../analysis/sentiment-analysis-dataset.csv')
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            if len(negative_tweets) >= limit and len(positive_tweets) >= limit:
                break
            else:
                if row[1] == "0":
                    neg_tweet = (row[3], "negative")
                    negative_tweets.append(neg_tweet)
                elif row[1] == "1":
                    pos_tweet = (row[3], "positive")
                    positive_tweets.append(pos_tweet)

    return negative_tweets, positive_tweets


def parse_dataset():
    tweets = []
    print "Parsing Dataset..."
    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, '../data/tweets.json')
    with open(filename) as data_file:
        df = json.load(data_file)
        for data in df:
            # get tweet text
            text = data['text']
            if text.startswith("RT") == False:
                tweets.append(data['text'])
    return tweets

if __name__ == "__main__":
    negative_tweets, positive_tweets = parse_training_data()
    all_tweets = parse_dataset()

    # layout and train data
    print "Gathering training data..."
    tweets = []
    for (words, sentiment) in positive_tweets + negative_tweets:
        words_filtered = [e.lower() for e in words.split() if
                          len(e) >= 3 and e.startswith("@") is False and e.startswith("http") is False]
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
    with open('classified_tweets.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Result', 'Tweet'])
        for t in all_tweets:
            result = classifier.classify(extract_features(t.split()))
            writer.writerow([result, t])
            pprint.pprint([result, t])

