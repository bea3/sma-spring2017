import matplotlib.pyplot as plt
import numpy as np
import json
import re
import os
import pprint

# data to plot
n_groups = 4
# gathered manually
fave_count = (773, 223, 580, 421)

keyword = ['RBoKNShF4R',
           'C8HrSJjeFw',
           '6kE6GvulfI',
           '5BjokX7HQ5']

all_url_dicts = dict()

for x in keyword:
    all_url_dicts[x] = 0

dir = os.path.dirname(__file__)
filename = os.path.join(dir, '../data/tweets.json')
with open(filename) as data_file:
    df = json.load(data_file)
    for data in df:
        # get tweet text
        text = data['text']
        # get urls in text
        regex_pattern = re.compile('https:\/\/t.co\/.*')
        matches = re.findall(regex_pattern, text)
        if (len(matches) > 0):
            matches = matches[0].split()
            # for each url, find the appropriate dictionary
            for i in range(len(matches)):
                url = matches[i]
                if i == 0 or url.startswith("https://t.co/"):
                    url = url.replace("https://t.co/", '')
                    if url in all_url_dicts:
                        all_url_dicts[url] += 1
                    else:
                        if url == 'SEO4CUuzjq':
                            all_url_dicts['RBoKNShF4R'] += 1
                        elif url == 'd7OGHbmu71':
                            all_url_dicts['5BjokX7HQ5'] += 1
        else:
            pass

pprint.pprint(all_url_dicts)

rt_count = (all_url_dicts['RBoKNShF4R'],
           all_url_dicts['C8HrSJjeFw'],
           all_url_dicts['6kE6GvulfI'],
           all_url_dicts['5BjokX7HQ5'])

# create plot
fig, ax = plt.subplots()
index = np.arange(n_groups)
bar_width = 0.35
opacity = 0.8

rects1 = plt.bar(index, rt_count, bar_width,
                 alpha=opacity,
                 color='b',
                 label='Retweet Count')

rects2 = plt.bar(index + bar_width, fave_count, bar_width,
                 alpha=opacity,
                 color='g',
                 label='Favorite Count')

plt.xlabel('Tracked URLs')
plt.ylabel('Count')
plt.title('Retweet Count and Favorite Count by Tracked URL')
plt.xticks(index + bar_width,
           ('Jezebel',
            'Huffington Post',
            'Sarah Ferris',
            'Independent'),
           rotation='horizontal',)
plt.legend()

plt.tight_layout()
plt.show()
