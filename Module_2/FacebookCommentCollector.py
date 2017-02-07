# Beatrice Garcia
# January 31, 2017
# Module 2 HW

import facebook
import requests

#This script retrieves an access token and comments from a Taylor Swift posts and writes it to a file

app_id = "102756836858371"
app_secret = "dcac52372190742139bba6843068aad7"

#gets access token
oauth_url = 'https://graph.facebook.com/oauth/access_token?client_id=' + app_id + '&client_secret=' + app_secret + '&grant_type=client_credentials'
r = requests.get(oauth_url)
access_token = r.text
access_token = access_token.split("access_token=")[1]

graph = facebook.GraphAPI(access_token=access_token, version='2.7')

#get comments from a Taylor Swift post
posts = graph.get_connections(id="19614945368_10154387193250369", connection_name="comments")
comments = posts.get("data")

#write to a file
f = open('taylor_swift_comments.txt', 'w')
for x in range(len(comments)):
    f.write(comments[x].get("message").encode("UTF-8") + "\n")

f.close()
