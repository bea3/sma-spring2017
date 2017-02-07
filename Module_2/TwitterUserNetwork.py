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

# consumer_key = "FB7K67fqH4OTOJte8IvcbG0pF"
# consumer_secret = "DbikkVO4aryhqqvpZ1TvdVzIG3P5qs7OhOlX5TPpeFFsOPdIto"
# access_token = "755192173964857344-2iI4XySsQlTKxTCrwWDaho4H0xiRjS1"
# access_secret = "bjlNh5m5CZ6AwGHAQaJIfwnH2Nm1QnJsTatF2MkO8xhF6"

f = open('twitter_user_network.csv', 'w')
f.write("from, to" + "\n")

#set up access and get tweets
api = twitter.Api(consumer_key=consumer_key, consumer_secret=consumer_secret, access_token_key=access_token,
                  access_token_secret=access_secret)

starter_user = "LuckyDuckyQuack"

level_1 = api.GetFollowers(screen_name=starter_user, total_count="10")
level_2 = api.GetFollowers(screen_name=level_1[0].screen_name, total_count="10")
level_3 = api.GetFollowers(screen_name=level_2[0].screen_name, total_count="10")
level_4 = api.GetFollowers(screen_name=level_3[0].screen_name, total_count="10")

for w in range(len(level_1)):
    f.write(starter_user + ", " + level_1[w].screen_name.encode("UTF-8") + "\n")

for x in range(len(level_2)):
    f.write(level_1[0].screen_name.encode("UTF-8") + ", " + level_2[x].screen_name.encode("UTF-8") + "\n")

for y in range(len(level_3)):
    f.write(level_2[0].screen_name.encode("UTF-8") + ", " + level_3[y].screen_name.encode("UTF-8") + "\n")

for z in range(len(level_3)):
    f.write(level_3[0].screen_name.encode("UTF-8") + ", " + level_4[z].screen_name.encode("UTF-8") + "\n")

f.close()
