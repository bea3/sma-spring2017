# Beatrice Garcia
# January 31, 2017
# Module 2 HW

import praw

client_id = "kPDOhCZFMTgJEw"
client_secret = "nXHOnn76HS1DsSJ_CrHI-C-k2RU"
user_agent ="webapp:philbert:v.1.0.0"
username = "turtlephilbert"


reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent, username=username)

#get a random subreddit and its comments
subreddit = reddit.random_subreddit(nsfw=False)
subredditComments = subreddit.comments(limit=100)

f = open('subreddit_comments.txt', 'w')
f.write('Subreddit: ' + subreddit.title.encode("UTF-8") + "\n\n")

counter = 1

for comment in subredditComments:
    f.write("COMMENT #" + str(counter) + "\n")
    f.write(comment.body.encode("UTF-8") + "\n\n")
    counter += 1

f.close()
