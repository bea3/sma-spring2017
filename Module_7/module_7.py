"""Extract a structured data set from a social media of your choice.  For example, you might have user_ID associated
with forum_ID.  Use relational algebra to extract a social network (or forum network) from your structured data.
Create a visualization of your extracted network.  What observations do you have in regards to the network structure of
your data?
"""

# Beatrice Garcia
# March 12, 2017
# Module 7
# Homework, Part 2


import praw
import csv


def get_data():
    client_id = "kPDOhCZFMTgJEw"
    client_secret = "nXHOnn76HS1DsSJ_CrHI-C-k2RU"
    user_agent ="webapp:philbert:v.1.0.0"
    username = "turtlephilbert"

    reddit = praw.Reddit(client_id=client_id,
                         client_secret=client_secret,
                         user_agent=user_agent, username=username)

    # get JHU subreddit and its comments
    subreddit = reddit.subreddit('climbing')

    with open('data.csv', 'wb') as csvfile:
        writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['forum_id', 'submission_id', 'comment_id', 'user_id', 'user'])

        submissions = subreddit.submissions()
        for submission in submissions:
            for comment in submission.comments:
                info = [subreddit.id, submission.id, comment.id, comment.author.id, comment.author]
                writer.writerow(info)


def main():
    get_data()

if __name__ == "__main__": main()

