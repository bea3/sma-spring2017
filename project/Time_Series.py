import plotly.plotly as py
import plotly.graph_objs as go

import pandas as pd
import json
import datetime
import re
import csv


keyword = ['RBoKNShF4R',
               'SEO4CUuzjq',
               'O0xVQdZDkw',
               'ENPlJ9KnZc',
               'dhMehoWjdi',
               'BIgjUQMqYu',
               'MDsxTHHA1V',
               'C8HrSJjeFw',
               'd7OGHbmu71',
               '6kE6GvulfI',
               '5BjokX7HQ5']


def add_dates(url_dict):
    all_dates = []

    start_date = datetime.datetime.strptime('Apr 22 2017 18:00', '%b %d %Y %H:%M')
    end_date = datetime.datetime.strptime('Apr 26 2017 00:00', '%b %d %Y %H:%M')
    delta = datetime.timedelta(hours=1)
    while start_date <= end_date:
        url_dict[start_date.strftime("%Y-%m-%d %H:%M")] = 0
        all_dates.append(start_date.strftime("%Y-%m-%d %H:%M"))
        start_date += delta

    return all_dates


def count_matches():
    global keyword

    all_url_dicts = []
    for x in keyword:
        url_dict = {}
        url_dict['id'] = x
        add_dates(url_dict)
        all_url_dicts.append(url_dict)


    with open('tweets.json') as data_file:
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
                        try:
                            url_dict = (item for item in all_url_dicts if item["id"] == url).next()
                            if url_dict is not None:
                                # get created at and turn it into "%Y-%m-%d %H:%M"
                                created_date = data['created_at']
                                created_date = datetime.datetime.strptime(created_date, '%a %b %d %H:%M:%S +0000 %Y')
                                created_date = created_date.replace(minute=00)
                                created_date = created_date.strftime("%Y-%m-%d %H:%M")
                                # add to appropriate slot
                                if created_date not in url_dict:
                                    url_dict[created_date] = 0
                                tally = url_dict[created_date]
                                url_dict[created_date] = tally + 1
                        except StopIteration:
                            pass
            else:
                print text

    return all_url_dicts


if __name__ == '__main__':
    print "Counting number of times URL appears..."
    all_url_dicts = count_matches()

    hello = {}
    all_dates = add_dates(hello)

    print "Writing to CSV..."
    with open('timeseries.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['date',
                         'RBoKNShF4R',
                         'SEO4CUuzjq',
                         'O0xVQdZDkw',
                         'ENPlJ9KnZc',
                         'dhMehoWjdi',
                         'BIgjUQMqYu',
                         'MDsxTHHA1V',
                         'C8HrSJjeFw',
                         'd7OGHbmu71',
                         '6kE6GvulfI',
                         '5BjokX7HQ5'])
        for d in all_dates:
            row = [str(d)]
            for k in keyword:
                # get the dict
                try:
                    url_dict = (item for item in all_url_dicts if item["id"] == k).next()
                    # get the tally for the date
                    count = url_dict[d]
                    row.append(count)
                except:
                    pass

            writer.writerow(row)

    print "Prepping for Plotly..."
    df = pd.read_csv("timeseries.csv")

    all_datas = []
    for k in keyword:
        data = go.Scatter(x=df['date'], y=df[k], name = k)
        all_datas.append(data)

    py.plot(all_datas)




