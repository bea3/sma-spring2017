import csv
import pprint
import operator

urls = {}
with open('04-18-17/trump_Tue-Apr-18-20:44:06-2017.csv', 'rb') as csvfile:
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