import json
import pprint
import sys
import time

from arango import ArangoClient
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

reload(sys)
sys.setdefaultencoding('utf8')

consumer_key = "FhiyBRb0cz4zOoDfcHNVOyBDS"
consumer_secret = "Q7MsbrPbFVzrwztW2KFH5JDGVpnSMhBlztwfJrLQeIGG591LST"
access_token = "755868887300780032-FqY1RAUiznqmVMToIotldxavDEKdEe9"
access_secret = "DV3O14tD9nTR1cVThyY1wriLMarXQoNQoudbZMHnUxYBP"

writer = None
f = None
csv_name = ""
db_name = "sma-proj"
collection_name = "misleads"
tweets = None

# Initialize the client for ArangoDB
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
    global tweets

    def on_data(self, data):
        global count
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

            # write_tweet([id, user_id, user_name, text, in_reply_status_id, fave_count, coordinates, source,
            #        in_reply_name, in_reply_user_id, is_rt, rt_count, geo, time, place])

            tweets.insert({'tweet_id': id,
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
        return True

    def on_error(self, status):
        client.shutdown()
        print status
        print (time.strftime("%I:%M:%S"))
        return False


def write_tweet(info_list):
    global writer
    writer.writerow(info_list)


def clean_text(text):
    text = text.decode()
    text = text.encode('ascii', 'ignore')
    text = text.encode("utf-8")
    text = text.strip()
    text = text.replace('\n', '')
    return text


def main():
    global f
    global writer
    global count
    global csv_name
    global tweets

    date_str = time.strftime('%m-%d-%Y')
    date_str = date_str.replace(' ', '-')

    print "Setting up database..."
    try:
        db = client.create_database(db_name)
    except:
        db = client.database(db_name)

    try:
        tweets = db.create_collection(collection_name)
    except:
        db.delete_collection(collection_name)
        tweets = db.create_collection(collection_name)

    tweets.add_hash_index(fields=['tweet_id'])
    tweets.add_hash_index(fields=['user_id'])
    tweets.add_hash_index(fields=['in_reply_to_status_id'])
    tweets.add_hash_index(fields=['in_reply_to_user_id'])
    tweets.add_fulltext_index(fields=['user_name'])
    tweets.add_fulltext_index(fields=['text'])
    tweets.add_fulltext_index(fields=['source'])
    tweets.add_fulltext_index(fields=['in_reply_to_screen_name'])
    tweets.add_fulltext_index(fields=['is_retweet'])
    tweets.add_skiplist_index(fields=['favorite_count'])
    tweets.add_skiplist_index(fields=['retweet_count'])
    tweets.add_skiplist_index(fields=['created_at'])
    tweets.add_skiplist_index(fields=['place'])
    tweets.add_geo_index(fields=['geo'])
    tweets.add_geo_index(fields=['coordinates'])

    keyword = ['https://t.co/RBoKNShF4R',
               'https://t.co/SEO4CUuzjq',
               'https://t.co/1d7odPvUuO',
               'https://t.co/PDn8QgW2pR',
               'https://t.co/dDYtCmbrPU',
               'https://t.co/QALrndA3xc',
               'https://t.co/sPhLIiVp3d',
               'https://t.co/KWP7X2aLiN',
               'https://t.co/TRJVkebsW8',
               'https://t.co/JSKgunUCz4',
               'https://t.co/wlP2Sryw5t']

    print "Getting tweets..."

    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    stream = Stream(auth, l)
    stream.filter(track=keyword)


if __name__ == '__main__':
    main()
