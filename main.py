from utils import *
import json
import matplotlib.pyplot as plt
from subprocess import call
import numpy as np


# Load information from JSON file
with open('second_round/query_output3150.json', 'r') as jsonfile:
    users = json.load(jsonfile)


# Create graph from file
print "Creating graph . . ."
graph = create_graph(users,1)


# Obtain degree distribution
print 'Obtaining histogram...'
deg_dist = degree_dist(graph)
# #
bins = [tup[0] for tup in list(deg_dist.bins())[:-1]]
vals = [tup[2] for tup in list(deg_dist.bins())[:-1]]

hist, bin_edges = np.histogram(vals, bins = range(len(bins)))
plt.bar(bin_edges[:-1], hist, width = 1)
plt.xlim(min(bin_edges), 60)
plt.ylabel('# of Nodes')
plt.xlabel('# of connections')
plt.show()

print 'Obtaining indicted politicians...'
busted = get_indicted('indicted_madrid.txt', users)

# From busted we see how juse carlos boza is 270469565
print 'Performing simulation...'

beta = 0.001
infected = [users['270469565']['node']-1]
Nrep = 500
Nsteps = 3
path = simulation(graph, users, beta, infected, Nrep, Nsteps)


# # Verified users from dataset
verified = get_verified(users)

# Obtain communities

print "Finding communities . . . "
partition = find_comm(graph,1)

for i in range(3):
    get_cluster_nodes(graph, partition[i], filename,i)


# print "Looking for most popular users . . ."
# #Get user who are hubs of the network
# ind = get_hubs(graph, 10)
#
# get_twitter_info(graph, ind, filename)
#
# print "Writing graph in pajek format"
# graph.write_pajek("1000.net")
