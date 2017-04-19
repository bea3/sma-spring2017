from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import csv
import json
import pprint
import time
import sys
import operator

consumer_key = "FhiyBRb0cz4zOoDfcHNVOyBDS"
consumer_secret = "Q7MsbrPbFVzrwztW2KFH5JDGVpnSMhBlztwfJrLQeIGG591LST"
access_token = "755868887300780032-FqY1RAUiznqmVMToIotldxavDEKdEe9"
access_secret = "DV3O14tD9nTR1cVThyY1wriLMarXQoNQoudbZMHnUxYBP"

writer = None
f = None
count = 0
csv_name = ""

class StdOutListener(StreamListener):
    global f
    global writer

    def on_data(self, data):
        global count
        data = json.loads(data)

        try:
            id = data['id']
        except KeyError:
            id = ""

        try:
            data['user']
            user_id = data['user']['id']
            user_name = data['user']['screen_name'] if data['user']['screen_name'] is not None else ""
        except KeyError:
            user_id = ""
            user_name = ""

        try:
            contributors = data['contributors'].encode("utf-8") if data['contributors'] is not None else ""
        except KeyError:
            contributors = ""

        try:
            text = data['text'] if data['text'] is not None else ""
            text = text.strip()
            text = text.replace('\n', '')
            text = ''.join([i if ord(i) < 128 else ' ' for i in text])
            text = text.encode("utf-8")
        except KeyError:
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
        except KeyError:
            source = ""

        try:
            in_reply_name = data['in_reply_to_screen_name'].encode("utf-8") if data['in_reply_to_screen_name'] is not None else ""
        except KeyError:
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
        except KeyError:
            place = ""

        row = [id, user_id, user_name, text, contributors, in_reply_status_id, fave_count, coordinates, source,
               in_reply_name, in_reply_user_id, is_rt, rt_count, geo, time, place]
        writer.writerow(row)

        count += 1

        if count >= 50000:
            close_csv()
            get_top_urls()
            return False
        return True

    def on_error(self, status):
        close_csv()
        get_top_urls()
        print status


def close_csv():
    global f
    print "Closing CSV"
    f.close()


def get_top_urls():
    global csv_name

    print "Getting Top Urls..."

    urls = {}
    with open(csv_name, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter='|')
        for row in reader:
            text = row[3]
            text_urls = [word for word in text.split() if word.startswith('https://t.co/')]
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

    csv_name = "trump"
    keyword = ["trump"]
    date_str = time.strftime("%c")
    date_str = date_str.replace(' ', '-')
    csv_name = csv_name + "_" + date_str + ".csv"

    # get_tweets(csv_name, keyword)

    # create the CSVs
    f = open(csv_name, 'wb')
    writer = csv.writer(f, delimiter='|', quoting=csv.QUOTE_MINIMAL)

    print "CSV Name: " + csv_name

    # write information into CSVs
    header = ['id', 'user_id', 'user_name', 'text', 'contributors', 'in_reply_to_status_id',
              'favorite_count', 'coordinates', 'source', 'in_reply_to_screen_name',
              'in_reply_to_user_id', 'is_retweet', 'retweet_count', 'geo', 'created_at', 'place']
    writer.writerow(header)

    print "Getting tweets..."

    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    stream = Stream(auth, l)

    # This line filter Twitter Streams to capture data by the keywords
    stream.filter(track=keyword)


if __name__ == '__main__':main()