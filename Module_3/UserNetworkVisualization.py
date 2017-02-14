import networkx as nx
import matplotlib.pyplot as plt
import csv
import operator

"""
Beatrice Garcia
February 9, 2017
Module 3 Homework

The blue nodes are the 5 most central nodes.
"""

G = nx.Graph()

# read csv and add edges
with open('twitter_user_network.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in reader:
        G.add_edge(row[0].strip(), row[1].strip())

# calculate betweenness centraliy
betweenness = nx.betweenness_centrality(G, endpoints=True)

# sort by greatest score to least
sorted_betweenness = sorted(betweenness.items(), key=operator.itemgetter(1))

labels = {}
other_nodes = {}
central_nodes = {}
count = 0

# separate nodes from the top 5 most central nodes and the rest and get the labels
for x in range(G.number_of_nodes()-1,-1,-1):
    node = sorted_betweenness[x]
    node_name = node[0]
    node_score = node[1]
    if count <= 4:
        print node_name
        labels[node_name] = node_name
        central_nodes[node_name] = node_score
    else:
        labels[node_name] = " "
        other_nodes[node_name] = node_score
    count += 1

# positions for all nodes
pos = nx.spring_layout(G)

# draw labels
nx.draw_networkx_labels(G, pos, labels, font_size=14, font_family='sans-serif')

# draw the most central nodes, the rest of the nodes, and the edges
nx.draw_networkx_nodes(G, pos, nodelist=central_nodes.keys(), node_color='b', node_size=[v * 1000 for v in central_nodes.values()])
nx.draw_networkx_nodes(G, pos, nodelist=other_nodes.keys(), node_size=[v * 1000 for v in other_nodes.values()])
nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)

# save and display graph
plt.axis('off')
plt.savefig("garcia_hw3.png")
plt.show()
