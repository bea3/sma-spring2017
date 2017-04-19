from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import csv
import json
import pprint
import time
import sys
import os
from arango import ArangoClient

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

# Initialize the client for ArangoDB
client = ArangoClient(
    protocol='http',
    host='localhost',
    port=8529,
    username='root',
    password='',
    enable_logging=True
)
db = client.database(db_name)
tweets = db.collection('tweets')

class StdOutListener(StreamListener):
    global f
    global writer

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
                in_reply_name = data['in_reply_to_screen_name'].encode("utf-8") if data['in_reply_to_screen_name'] is not None else ""
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

            row = [id, user_id, user_name, text, in_reply_status_id, fave_count, coordinates, source,
                   in_reply_name, in_reply_user_id, is_rt, rt_count, geo, time, place]
            writer.writerow(row)

            # count += 1

            # if count >= 5000:
            #     close_csv()
            #     return False
        return True

    def on_error(self, status):
        close_csv()
        client.shutdown()
        print status


def close_csv():
    global f
    print "Closing CSV"
    f.close()


def clean_text(text):
    text = text.decode()
    # text = text.decode("utf-8")
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

    # hash index - good for quick access
    # skiplist index - keeps it sorted
    # persisted index - keeps it in memory, therefore doesn't have to be rebuilt in memory
    # geo index - keeps geo:
    # { "latitude": 50.9406645, "longitude": 6.9599115 }
    # or { "coords": [ 50.9406645, 6.9599115 ] }
    # fulltext - used to index all words

    # # create CSV
    # csv_name = 'top10'
    # keyword = ['https://t.co/r8uFthZWBj',
    #            'https://t.co/sRHak6gnUT',
    #            'https://t.co/DjeMPPHKu4',
    #            'https://t.co/xdQ5eOGh14',
    #            'https://t.co/plqoSMaixV',
    #            'https://t.co/XZDLFK7E0X',
    #            'https://t.co/uDxnyXZp1p',
    #            'https://t.co/BkhSU8PKfs',
    #            'https://t.co/CtX7XQZmZH',
    #            'https://t.co/x59B9R3fji',
    #            'https://t.co/cQiIXTL5N4']
    #
    # csv_name = csv_name + ".csv"
    # date_str = time.strftime('%m-%d-%Y')
    # date_str = date_str.replace(' ', '-')
    #
    # if not os.path.exists(date_str):
    #     os.makedirs(date_str)
    #
    # f = open(date_str + "/" + csv_name, 'wb')
    # writer = csv.writer(f, delimiter='|', quoting=csv.QUOTE_MINIMAL)
    #
    # print "CSV Name: " + csv_name
    #
    # # write information into CSVs
    # header = ['id', 'user_id', 'user_name', 'text', 'contributors', 'in_reply_to_status_id',
    #           'favorite_count', 'coordinates', 'source', 'in_reply_to_screen_name',
    #           'in_reply_to_user_id', 'is_retweet', 'retweet_count', 'geo', 'created_at', 'place']
    # writer.writerow(header)
    #
    # print "Getting tweets..."
    #
    # l = StdOutListener()
    # auth = OAuthHandler(consumer_key, consumer_secret)
    # auth.set_access_token(access_token, access_secret)
    # stream = Stream(auth, l)
    #
    # # This line filter Twitter Streams to capture data by the keywords
    # stream.filter(track=keyword)


if __name__ == '__main__':
    main()
