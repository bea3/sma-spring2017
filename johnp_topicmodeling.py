
# coding: utf-8

# In[4]:

# %load /Users/piorkja1/Documents/PycharmProjects/Platform_Access/RedditTopicModeler.py

__author__ = 'piorkja1'

# First Part is to Read Reddit and store comments
# Simple PRAW Script to Read SubRedit on Hopkins
import praw
import json
import gensim
import pprint

# setup for tokenization and stopwords
from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize
from gensim import corpora, models, similarities
#from collections import defaultdict

client_id = "kPDOhCZFMTgJEw"
client_secret = "nXHOnn76HS1DsSJ_CrHI-C-k2RU"
user_agent ="webapp:philbert:v.1.0.0"
username = "turtlephilbert"

stop_words = set(stopwords.words('english'))
stop_words.update(['.',  ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}','year']) # remove it if you need punctuation

# collect JHU Posts from REDDIT
file = open("redditprocess.txt", "w")
r = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent, username=username)
for post in r.subreddit('jhu').submissions():
    pprint.pprint(post)
    file.write(post.body + '\n')
    words = [i.lower() for i in wordpunct_tokenize(post.body) if i.lower() not in stop_words]
    #print (words)
    all_tokens = ' '.join(words)
#print (words)
#dictionary = corpora.Dictionary(words)
#print (dictionary)

# Remove words that appear only once

texts = words
# remove words that appear only once
#all_tokens = sum(texts, [])
tokens_once = set(words for words in set(all_tokens) if all_tokens.count(words) == 1)
#print(tokens_once)
texts = [[words for words in texts if words not in tokens_once]
         for words in all_tokens]
print (texts)

    #file.write(text + '\n')

#    file.write(post.body + '\n')

# Setup for Document Matrix

#Setup gensim dictionary

dictionary = corpora.Dictionary(texts)


corpus = [dictionary.doc2bow(text) for text in texts]
corpora.MmCorpus.serialize('reddit.mm', corpus)
#print(corpus)

lda = gensim.models.LdaModel(corpus, id2word=dictionary, alpha='auto', num_topics=10)
for i in lda.show_topics():
    print (i)
#convert ot BOW vectors

import pyLDAvis.gensim

topic_vis = pyLDAvis.gensim.prepare(lda, corpus, dictionary)

pyLDAvis.display(topic_vis)

file.close






# In[5]:

pyLDAvis.display(topic_vis)

