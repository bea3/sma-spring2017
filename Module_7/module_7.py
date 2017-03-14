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
    """
    Get submissions and comments in the JHU subreddit and writes it to a CSV file.
    """
    client_id = "kPDOhCZFMTgJEw"
    client_secret = "nXHOnn76HS1DsSJ_CrHI-C-k2RU"
    user_agent = "webapp:philbert:v.1.0.0"
    username = "turtlephilbert"

    reddit = praw.Reddit(client_id=client_id,
                         client_secret=client_secret,
                         user_agent=user_agent, username=username)

    # get JHU subreddit and its comments
    subreddit = reddit.subreddit('jhu')

    # write submissions and its comments in a CSV file
    with open('data.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['forum_id', 'submission_id', 'comment_id', 'user_id', 'user'])

        submissions = subreddit.submissions()
        for submission in submissions:
            if submission is not None:
                for comment in submission.comments:
                    if comment is not None:
                        info = [subreddit.id, submission.id, comment.id, comment.author.id, comment.author]
                        writer.writerow(info)


def visualize_data():
    """
    Read the CSV and use Networkx to visualize the  graph.
    """
    G = nx.Graph()

    # read csv and add edges
    with open('data.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            G.add_edge(row[0].strip(), row[1].strip())
            G.add_edge(row[1].strip(), row[2].strip())
            G.add_edge(row[2].strip(), row[4].strip())

    # calculate degree centrality
    degree = nx.degree_centrality(G)

    # sort by greatest score to least
    sorted_degree = sorted(degree.items(), key=operator.itemgetter(1))

    labels = {}
    all_nodes = {}

    # separate nodes from the top 5 most central nodes and the rest and get the labels
    for x in range(G.number_of_nodes()):
        node = sorted_degree[x]
        node_name = node[0]
        node_score = node[1]
        labels[node_name] = node_name
        all_nodes[node_name] = node_score

    # positions for all nodes
    pos = nx.spring_layout(G)

    # draw labels
    nx.draw_networkx_labels(G, pos, labels, font_size=10, font_family='sans-serif')

    # draw the most central nodes, the rest of the nodes, and the edges
    nx.draw_networkx_nodes(G, pos, nodelist=all_nodes.keys(), node_color='b', node_size=[v * 1000 for v in all_nodes.values()])
    nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)

    # save and display graph
    plt.axis('off')
    plt.savefig("garcia_hw7.png")
    plt.show()


def main():
    # get_data()
    visualize_data()


if __name__ == "__main__": main()
