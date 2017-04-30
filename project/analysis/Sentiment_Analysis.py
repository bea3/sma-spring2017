import csv
import json
import os
import pprint
import nltk
import re

negative_tweets = []
positive_tweets = []
word_features = dict()

dataset_name = "../data/white-house.csv"


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
    limit = 3000
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


def condense_csvs():
    tweets = []
    print "Condensing Replies with tweets.json..."
    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, '../data/tweets.json')
    with open(filename) as data_file:
        df = json.load(data_file)
        for data in df:
            # get tweet text
            text = data['text']
            if text.startswith("RT") == False:
                # get urls in text
                regex_pattern = re.compile('https:\/\/t.co\/.*')
                matches = re.findall(regex_pattern, text)
                if (len(matches) > 0):
                    matches = matches[0].split()
                    # for each url, find the appropriate dictionary
                    for i in range(len(matches)):
                        url = matches[i]
                        if i == 0 or url.startswith("https://t.co/"):
                            url = url.replace("https://t.co/", '')
                            if url == 'SEO4CUuzjq' or url == 'RBoKNShF4R':
                                dir = os.path.dirname(__file__)
                                filename = os.path.join(dir, dataset_name)
                                csvFile = open(filename, 'a')
                                csvWriter = csv.writer(csvFile)
                                csvWriter.writerow([data['created_at'], text.encode('utf-8')])
                                csvFile.close()
                            elif url == 'd7OGHbmu71' or url == '5BjokX7HQ5':
                                dir = os.path.dirname(__file__)
                                filename = os.path.join(dir, '../retrieve-data/mental-illness.csv')
                                csvFile = open(filename, 'a')
                                csvWriter = csv.writer(csvFile)
                                csvWriter.writerow([data['created_at'], text.encode('utf-8')])
                                csvFile.close()
                            elif url == '6kE6GvulfI':
                                dir = os.path.dirname(__file__)
                                filename = os.path.join(dir, '../retrieve-data/white-house.csv')
                                csvFile = open(filename, 'a')
                                csvWriter = csv.writer(csvFile)
                                csvWriter.writerow([data['created_at'], text.encode('utf-8')])
                                csvFile.close()
                            elif url == 'C8HrSJjeFw':
                                dir = os.path.dirname(__file__)
                                filename = os.path.join(dir, '../retrieve-data/march-for-science-replies.csv')
                                csvFile = open(filename, 'a')
                                csvWriter = csv.writer(csvFile)
                                csvWriter.writerow([data['created_at'], text.encode('utf-8')])
                                csvFile.close()
                            else:
                                pass


def parse_dataset(filename):
    tweets = []
    print "Parsing dataset " + filename + "..."
    dir = os.path.dirname(__file__)
    f = os.path.join(dir, filename)
    with open(f, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            if row[1] is not None or len(row[1]) > 0:
                tweets.append(row[1])

    return tweets


if __name__ == "__main__":
    negative_tweets, positive_tweets = parse_training_data()
    condense_csvs()
    all_tweets = parse_dataset(dataset_name)

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

    pos_count = 0
    neg_count = 0

    # write submissions and its comments in a CSV file
    with open('classified_tweets.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Result', 'Tweet'])
        for t in all_tweets:
            result = classifier.classify(extract_features(t.split()))
            if result == "positive":
                pos_count += 1
            elif result == "negative":
                neg_count += 1
            writer.writerow([result, t])

    print "(+) " + str(pos_count)
    print "(-) " + str(neg_count)
