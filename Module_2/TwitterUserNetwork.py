# Beatrice Garcia
# January 31, 2017
# Module 2 HW

# This script get the Taylor Swift Twitter page, gets the first 10 followers, and collects the followers of those 10 collected followers.
# Repeated twice.

import twitter

consumer_key = "lWwcZksOC8MhoesnaZw6gLXrh"
consumer_secret = "jZSHcmzZJc1po9Af77SauPAIEoC1HxQfAZlLVPwSKTvzn8EJGD"
access_token = "755868887300780032-f7yUJ4uJ7Fl6nsChQQrmpIXdDjMkUKy"
access_secret = "x5E7C1v8maJ5XB31mU3T4B8EeRdM5TyEUhEyFWtSDY9I2"

f = open('twitter_user_network.csv', 'w')
f.write("from, to" + "\n")

#set up access and get tweets
api = twitter.Api(consumer_key=consumer_key, consumer_secret=consumer_secret, access_token_key=access_token, access_token_secret=access_secret, sleep_on_rate_limit=True)

taylor_swift_followers = api.GetFollowers(screen_name="taylorswift13", total_count="10")
for x in range(len(taylor_swift_followers)):
    level_2 = api.GetFollowers(screen_name=taylor_swift_followers[x].screen_name, total_count="10")
    for y in range(len(level_2)):
        level_3 = api.GetFollowers(screen_name=level_2[y].screen_name, total_count="10")
        for z in range(len(level_3)):
            f.write(level_2[y].screen_name + ", " + level_3[z].screen_name + "\n")



