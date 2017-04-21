from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import csv
import json
import pprint
import time
import sys
import operator
from arango import ArangoClient
import re

reload(sys)
sys.setdefaultencoding('utf8')

consumer_key = "FhiyBRb0cz4zOoDfcHNVOyBDS"
consumer_secret = "Q7MsbrPbFVzrwztW2KFH5JDGVpnSMhBlztwfJrLQeIGG591LST"
access_token = "755868887300780032-FqY1RAUiznqmVMToIotldxavDEKdEe9"
access_secret = "DV3O14tD9nTR1cVThyY1wriLMarXQoNQoudbZMHnUxYBP"

writer = None
f = None
count = 0
csv_name = ""
db_name = "sma-proj"
trump = None
db = None

client = ArangoClient(
    protocol='http',
    host='localhost',
    port=8529,
    username='root',
    password='',
    enable_logging=True
)


class StdOutListener(StreamListener):
    global f
    global writer

    def on_data(self, data):
        global count
        global trump
        data = json.loads(data)

        try:
            data['limit']
        except KeyError:
            try:
                id = data['id']
            except KeyError:
                id = ""

            try:
                data['user']
                user_id = data['user']['id']
                user_name = data['user']['screen_name'] if data['user']['screen_name'] is not None else ""
                user_name = clean_text(user_name)
            except KeyError:
                print ("Error with tweet id/screen name: ")
                pprint.pprint(data)
                user_id = ""
                user_name = ""
            except:
                print "Error (not KeyError nor UnicodeEncodeError) with tweet screen name: "
                pprint.pprint(data)
                user_id = ""
                user_name = ""

            try:
                text = data['text'] if data['text'] is not None else ""
                text = clean_text(text)
            except KeyError or UnicodeEncodeError:
                print ("Error with tweet text: ")
                pprint.pprint(data)
                text = ""
            except:
                print "Error (not KeyError nor UnicodeEncodeError) with tweet text: "
                pprint.pprint(data)
                text = ""

            try:
                in_reply_status_id = data['in_reply_to_status_id'] if data['in_reply_to_status_id'] is not None else ""
            except KeyError:
                in_reply_status_id = ""

            try:
                fave_count = data['favorite_count'] if data['favorite_count'] is not None else ""
            except KeyError:
                fave_count = ""

            try:
                is_rt = data['retweeted'] if data['retweeted'] is not None else ""
            except KeyError:
                is_rt = ""

            try:
                coordinates = data['coordinates'] if data['coordinates'] is not None else ""
            except KeyError:
                coordinates = ""

            try:
                source = data['source'].encode("utf-8") if data['source'] is not None else ""
                source = clean_text(source)
            except KeyError or UnicodeEncodeError:
                print ("Error with tweet source: ")
                pprint.pprint(data)
                source = ""

            try:
                in_reply_name = data['in_reply_to_screen_name'].encode("utf-8") if data[
                                                                                       'in_reply_to_screen_name'] is not None else ""
                in_reply_name = clean_text(in_reply_name)
            except KeyError or UnicodeEncodeError:
                print ("Error with tweet reply-to-screen-name: ")
                pprint.pprint(data)
                in_reply_name = ""
            except:
                print "Error (not KeyError nor UnicodeEncodeError) with tweet reply-to name: "
                pprint.pprint(data)
                in_reply_name = ""

            try:
                in_reply_user_id = data['in_reply_to_user_id'] if data['in_reply_to_user_id'] is not None else ""
            except KeyError:
                in_reply_user_id = ""

            try:
                rt_count = data['retweet_count'] if data['retweet_count'] is not None else ""
            except KeyError:
                rt_count = ""

            try:
                geo = data['geo'] if data['geo'] is not None else ""
            except KeyError:
                geo = ""

            try:
                time = data['created_at'] if data['created_at'] is not None else ""
            except KeyError:
                time = ""

            try:
                place = data['place']['full_name'] if data['place'] is not None else ""
                place = clean_text(place)
            except KeyError:
                place = ""

            # row = [id, user_id, user_name, text, in_reply_status_id, fave_count, coordinates, source,
            #        in_reply_name, in_reply_user_id, is_rt, rt_count, geo, time, place]
            # writer.writerow(row)

            trump.insert({'tweet_id': id,
                          'user_id': user_id,
                          'user_name': user_name,
                          'text': text,
                          'in_reply_to_status_id': in_reply_status_id,
                          'favorite_count': fave_count,
                          'source': source,
                          'in_reply_to_screen_name': in_reply_name,
                          'is_retweet': is_rt,
                          'retweet_count': rt_count,
                          'in_reply_to_user_id': in_reply_user_id,
                          'created_at': time,
                          'place': place,
                          'geo': geo,
                          'coordinates': coordinates})

            count += 1

            if count >= 100000:
                # close_csv()
                get_top_urls()
                return False
        return True

    def on_error(self, status):
        # close_csv()
        get_top_urls()
        print status


def clean_text(text):
    text = text.decode()
    text = text.encode('ascii', 'ignore')
    text = text.encode("utf-8")
    text = text.strip()
    text = text.replace('\n', '')
    return text


def close_csv():
    global f
    print "Closing CSV"
    f.close()


def get_top_urls():
    global csv_name

    print "Getting Top Urls..."

    urls = {}

    # with open(csv_name, 'rb') as csvfile:
    #     reader = csv.reader(csvfile, delimiter='|')
    #     for row in reader:
    #         text = row[3]
    #         text_urls = [word for word in text.split() if word.startswith('https://t.co/')]
    #         for t in text_urls:
    #             if t not in urls.keys():
    #                 urls[t] = 1
    #             else:
    #                 urls[t] += 1
    #
    # sorted_x = sorted(urls.items(), key=operator.itemgetter(1), reverse=True)
    # pprint.pprint(sorted_x)

    global db
    cursor = db.aql.execute('FOR tweet IN tweets filter tweet.text like "%https:\/\/t.co\/%" return '
                            '{text: tweet.text}')
    batch = cursor.batch()

    for doc in batch:
        regex_pattern = re.compile('https://t.co/(.*)')
        doc = doc['text']
        doc = clean_text(doc)
        matches = re.findall(regex_pattern, doc)
        matches = matches[0].split()
        for i in range(len(matches)):
            url = matches[i]
            if i == 0 or url.startswith('https://t.co/'):
                if url.startswith('https://t.co/'):
                    url = url.replace('https://t.co/', '')
                if url not in urls.keys():
                    urls[url] = 1
                else:
                    urls[url] += 1

    while cursor.has_more():
        batch = cursor.next()
        for doc in batch:
            doc = doc['text']
            doc = clean_text(doc)
            regex_pattern = re.compile('https://t.co/(.*)')
            text_urls = re.findall(regex_pattern, doc)
            for t in text_urls:
                if t not in urls.keys():
                    urls[t] = 1
                else:
                    urls[t] += 1

    sorted_x = sorted(urls.items(), key=operator.itemgetter(1), reverse=True)
    pprint.pprint(sorted_x)


def main():
    global f
    global writer
    global count
    global csv_name
    global trump
    global db

    date_str = time.strftime('%m-%d-%Y')
    date_str = date_str.replace(' ', '-')

    try:
        db = client.create_database(db_name)
    except:
        db = client.database(db_name)

    try:
        trump = db.create_collection('trump-' + date_str)
    except:
        trump = db.collection('trump-' + date_str)

    trump.add_hash_index(fields=['tweet_id'])
    trump.add_hash_index(fields=['user_id'])
    trump.add_hash_index(fields=['in_reply_to_status_id'])
    trump.add_hash_index(fields=['in_reply_to_user_id'])
    trump.add_fulltext_index(fields=['user_name'])
    trump.add_fulltext_index(fields=['text'])
    trump.add_fulltext_index(fields=['source'])
    trump.add_fulltext_index(fields=['in_reply_to_screen_name'])
    trump.add_fulltext_index(fields=['is_retweet'])
    trump.add_skiplist_index(fields=['favorite_count'])
    trump.add_skiplist_index(fields=['retweet_count'])
    trump.add_skiplist_index(fields=['created_at'])
    trump.add_skiplist_index(fields=['place'])
    trump.add_geo_index(fields=['geo'])
    trump.add_geo_index(fields=['coordinates'])

    keyword = ["trump"]

    # # create the CSVs
    # f = open(csv_name, 'wb')
    # csv_name = "trump.csv"
    # writer = csv.writer(f, delimiter='|', quoting=csv.QUOTE_MINIMAL)
    #
    # print "CSV Name: " + csv_name
    #
    # # write information into CSVs
    # header = ['id', 'user_id', 'user_name', 'text', 'contributors', 'in_reply_to_status_id',
    #           'favorite_count', 'coordinates', 'source', 'in_reply_to_screen_name',
    #           'in_reply_to_user_id', 'is_retweet', 'retweet_count', 'geo', 'created_at', 'place']
    # writer.writerow(header)

    print "Getting tweets..."

    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    stream = Stream(auth, l)
    stream.filter(track=keyword)


if __name__ == '__main__':
    main()
