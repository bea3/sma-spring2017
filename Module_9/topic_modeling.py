# Beatrice Garcia
# April 13, 2017
# Module 9 Homework

import twitter
import gensim
import nltk
import pprint
import string
import pyLDAvis.gensim
import IPython

consumer_key = "FhiyBRb0cz4zOoDfcHNVOyBDS"
consumer_secret = "Q7MsbrPbFVzrwztW2KFH5JDGVpnSMhBlztwfJrLQeIGG591LST"
access_token = "755868887300780032-FqY1RAUiznqmVMToIotldxavDEKdEe9"
access_secret = "DV3O14tD9nTR1cVThyY1wriLMarXQoNQoudbZMHnUxYBP"

#set up access and get tweets
api = twitter.Api(consumer_key=consumer_key, consumer_secret=consumer_secret, access_token_key=access_token, access_token_secret=access_secret)
trump_tweets = api.GetSearch(term="trump", result_type="tweet", count=100)

tweets = []

for x in range(len(trump_tweets)):
    tweets.append(trump_tweets[x].text.encode("UTF-8"))

# clean up tweets
all_words = ""
for t in tweets:
    t = t.replace('\n', '')
    t = t.replace(',', ' ')
    t = t.strip()
    t = t.translate(None, string.punctuation)
    t = t.lower()

    # remove stop words
    word_list = t.split(" ")
    filtered_words = [word for word in word_list if word not in nltk.corpus.stopwords.words('english')]
    t = " ".join(filtered_words)

    sentence = ''.join([i if ord(i) < 128 else ' ' for i in t])
    sentence = sentence.replace("\"", "")
    all_words = all_words + " " + sentence

# tokenize tweets
tokens = nltk.tokenize.word_tokenize(all_words)

tokens = [tokens]

################################

dictionary = gensim.corpora.Dictionary(tokens)

corpus = [dictionary.doc2bow(text) for text in tokens]

lda = gensim.models.LdaModel(corpus, id2word=dictionary, alpha='auto', num_topics=10)

topic_vis = pyLDAvis.gensim.prepare(lda, corpus, dictionary)

pyLDAvis.display(topic_vis)





