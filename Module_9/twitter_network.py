# Beatrice Garcia
# April 9, 2017
# Module 9

# This script collects 500 tweets and creates an adjacency matrix with them

import twitter
import pprint
import csv


def add_lists_wo_dupes(first_list, second_list):
    in_first = set(first_list)
    in_second = set(second_list)

    in_second_but_not_in_first = in_second - in_first

    result = first_list + list(in_second_but_not_in_first)
    return result


def get_tweets():

    consumer_key = "FhiyBRb0cz4zOoDfcHNVOyBDS"
    consumer_secret = "Q7MsbrPbFVzrwztW2KFH5JDGVpnSMhBlztwfJrLQeIGG591LST"
    access_token = "755868887300780032-FqY1RAUiznqmVMToIotldxavDEKdEe9"
    access_secret = "DV3O14tD9nTR1cVThyY1wriLMarXQoNQoudbZMHnUxYBP"

    #set up access and get tweets
    api = twitter.Api(consumer_key=consumer_key, consumer_secret=consumer_secret, access_token_key=access_token, access_token_secret=access_secret)
    nascar_tweets = api.GetSearch(term="nascar", result_type="tweet", count=100)

    # create the CSVs
    f = open('nascar_tweets.csv', 'wb')
    writer = csv.writer(f, delimiter='|', quoting=csv.QUOTE_MINIMAL)

    # write information into CSVs
    header = ['id', 'user', 'created_date', 'text', 'mentions', 'type']
    writer.writerow(header)

    for x in range(len(nascar_tweets)):
        tweet = nascar_tweets[x]

        id = tweet.id
        text = tweet.text.encode("utf-8")
        text = text.replace('\n', '')
        text = text.replace(',', ' ')

        if text.startswith("RT"):
            type = "RT"
        elif text.startswith("@"):
            type = "reply"
        else:
            type = "tweet"

        mentions = []
        user_mentions = tweet.user_mentions
        for um in user_mentions:
            mentions.append(um.screen_name.encode("utf-8"))

        writer.writerow([tweet.id, tweet.user.screen_name, tweet.created_at, text, mentions, type])

    f.close()


def create_adjacency_matrix():
    # create the CSVs
    f = open('adjacency_matrix.csv', 'wb')
    writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)

    relationships = {}
    all_users = []

    count = 0
    for line in open("nascar_tweets.csv"):
        if count > 0:
            row = line.split('|')

            mentions = row[4]
            mentions = mentions.replace("[", "")
            mentions = mentions.replace("]", "")
            mentions = mentions.replace("'", "")
            mentions = mentions.split(",")
            user = row[1]

            if user not in all_users:
                all_users.append(user)

            for m in mentions:
                m = m.strip()
                if m not in all_users:
                    all_users.append(m)

            if user not in relationships:
                relationships[user] = mentions
            else:
                relationships[user] = add_lists_wo_dupes(mentions, relationships[user])

        count += 1

    writer.writerow(all_users)

    pprint.pprint(relationships)

    row = []
    for user in all_users:
        row.append(user)
        to_users = []

        if user in relationships.keys():
            to_users = relationships[user]
            for k, v in relationships.items():
                if user == v or isinstance(v, list) and user in v:
                    to_users.append(k)
        else:
            to_users = []
            for k, v in relationships.items():
                if user == v or isinstance(v, list) and user in v:
                    to_users.append(k)

        for u in all_users:
            if u in to_users:
                row.append(1)
            else:
                row.append(0)

        writer.writerow(row)
        row = []

    f.close()


def main():
    # get_tweets()

    create_adjacency_matrix()

if __name__ == "__main__": main()