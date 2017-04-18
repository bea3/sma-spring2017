#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import csv
import json
import pprint

consumer_key = "FhiyBRb0cz4zOoDfcHNVOyBDS"
consumer_secret = "Q7MsbrPbFVzrwztW2KFH5JDGVpnSMhBlztwfJrLQeIGG591LST"
access_token = "755868887300780032-FqY1RAUiznqmVMToIotldxavDEKdEe9"
access_secret = "DV3O14tD9nTR1cVThyY1wriLMarXQoNQoudbZMHnUxYBP"

# create the CSVs
f = open('trump-russia_palmerreport.csv', 'wb')
writer = csv.writer(f, delimiter='|', quoting=csv.QUOTE_MINIMAL)


class StdOutListener(StreamListener):

    def on_data(self, data):
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
            text = data['text'].encode("utf-8") if data['text'] is not None else ""
            text = text.strip()
            text = text.replace('\n', '')
            text = ''.join([i if ord(i) < 128 else ' ' for i in text])
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
            coordinates = data['coordinates'].encode("utf-8") if data['coordinates'] is not None else ""
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
            geo = data['geo'].encode("utf-8") if data['geo'] is not None else ""
        except KeyError:
            geo = ""

        try:
            time = data['created_at'] if data['created_at'] is not None else ""
        except KeyError:
            time = ""

        try:
            place = data['place']['full_name'].encode("utf-8") if data['place'] is not None else ""
        except KeyError:
            place = ""

        row = [id, user_id, user_name, contributors, text, in_reply_status_id, fave_count, coordinates, source,
               in_reply_name, in_reply_user_id, is_rt, rt_count, geo, time, place]
        writer.writerow(row)
        return True

    def on_error(self, status):
        close_csv()
        print status


def close_csv():
    f.close()


def main():
    # write information into CSVs
    header = ['id', 'user_id', 'user_name', 'contributors', 'text', 'in_reply_to_status_id',
              'favorite_count', 'coordinates', 'source', 'in_reply_to_screen_name',
              'in_reply_to_user_id', 'is_retweet', 'retweet_count', 'geo', 'created_at', 'place']
    writer.writerow(header)

    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    stream = Stream(auth, l)

    csv_titles = ['trump-russia_palmerreport', 'h1b_the-guardian', 'h1b-wsj', 'h1b-economic-times']
    keywords = [['palmerreport', 'fbi', 'trump'], ['']]

    # This line filter Twitter Streams to capture data by the keywords
    stream.filter(track=['palmerreport', 'fbi', 'trump'])


if __name__ == '__main__':main()