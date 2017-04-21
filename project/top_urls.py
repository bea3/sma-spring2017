
from arango import ArangoClient
import re
import pprint
import operator


def add_urls(urls, doc):
    """
    :param urls: dictionary object used to keep track of number of times a URL appears
    :param doc: tweet text to examine, parse, and add to the urls dictionary
    :return: 
    """
    regex_pattern = re.compile('https:\/\/t.co\/.*')
    doc = doc['text']
    matches = re.findall(regex_pattern, doc)
    matches = matches[0].split()
    for i in range(len(matches)):
        url = matches[i]
        if i == 0 or url.startswith("https://t.co/"):
            if url.startswith("https://t.co/"):
                url = url.replace("https://t.co/", '')
            if url not in urls.keys():
                urls[url] = 1
            else:
                urls[url] += 1


def get_top_urls(collection_name):
    client = ArangoClient(
        protocol='http',
        host='localhost',
        port=8529,
        username='root',
        password='',
        enable_logging=True
    )

    db = client.database('sma-proj')
    db.collection(collection_name)

    query = 'FOR tweet IN ' + collection_name + ' FILTER tweet.text LIKE "%https:\/\/t.co\/%" return {text: tweet.text}'

    cursor = db.aql.execute(query)
    batch = cursor.batch()
    tweet_count = len(batch)

    urls = {}

    for doc in batch:
        add_urls(urls, doc)

    while cursor.has_more():
        batch = cursor.next()
        tweet_count = tweet_count + len(batch)
        if isinstance(batch, dict):
            add_urls(urls, batch)
        elif isinstance(batch, list):
            for doc in batch:
                add_urls(urls, doc)

    pprint.pprint("Found " + str(tweet_count) + " tweets that match the query.")
    sorted_x = dict(sorted(urls.items(), key=operator.itemgetter(1), reverse=True)[:10])
    pprint.pprint(sorted_x)

if __name__ == '__main__':
    get_top_urls("trump")