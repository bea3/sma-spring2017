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
import networkx as nx
import matplotlib.pyplot as plt
import csv
import operator


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
        writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['forum_id', 'submission_id', 'comment_id', 'user_id', 'user'])

        submissions = subreddit.submissions()
        for submission in submissions:
            for comment in submission.comments:
                info = [subreddit.id, submission.id, comment.id, comment.author.id, comment.author]
                writer.writerow(info)


def visualize_data():
    G = nx.Graph()

    # read csv and add edges
    with open('data.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            G.add_edge(row[0].strip(), row[1].strip())
            G.add_edge(row[1].strip(), row[2].strip())

    # calculate betweenness centraliy
    betweenness = nx.betweenness_centrality(G, endpoints=True)

    # sort by greatest score to least
    sorted_betweenness = sorted(betweenness.items(), key=operator.itemgetter(1))

    labels = {}
    other_nodes = {}
    central_nodes = {}
    count = 0

    # separate nodes from the top 5 most central nodes and the rest and get the labels
    for x in range(G.number_of_nodes()):
        node = sorted_betweenness[x]
        node_name = node[0]
        node_score = node[1]
        labels[node_name] = node_name
        central_nodes[node_name] = node_score
        count += 1

    # positions for all nodes
    pos = nx.spring_layout(G)

    # draw labels
    nx.draw_networkx_labels(G, pos, labels, font_size=14, font_family='sans-serif')

    # draw the most central nodes, the rest of the nodes, and the edges
    nx.draw_networkx_nodes(G, pos, nodelist=central_nodes.keys(), node_color='b',
                           node_size=[v * 1000 for v in central_nodes.values()])
    nx.draw_networkx_nodes(G, pos, nodelist=other_nodes.keys(), node_size=[v * 1000 for v in other_nodes.values()])
    nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)

    # save and display graph
    plt.axis('off')
    plt.savefig("garcia_hw7.png")
    plt.show()

def main():
    # get_data()
    visualize_data()


if __name__ == "__main__": main()

