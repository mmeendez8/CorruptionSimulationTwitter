from utils import *
import json
import matplotlib.pyplot as plt
from subprocess import call


# Load information from JSON file
with open('query_output1000.json', 'r') as jsonfile:
    users = json.load(jsonfile)


filename = "query_output1000.json"
# Create graph from file
print "Creating graph . . ."
graph = create_graph(users,1)

id_mamon = []
for elem in users.iteritems():
    if 'boza' in strip_accents(elem[1]['real_name'].encode('utf-8').lower()):
        id_mamon.append(elem[0])

print id_mamon
print users[id_mamon[0]]['real_name']
# https://twitter.com/josecarlosboza
print users[id_mamon[0]]['neighbours']

beta = 0.001
infected = [users[id_mamon[0]]['node']-1]
Nrep = 500
Nsteps = 3
simulation(graph, users, beta, infected, Nrep, Nsteps)
# Obtain degree distribution
# deg_dist = degree_dist(graph)
#
# bins = [tup[0] for tup in list(deg_dist.bins())]
# vals = [tup[2] for tup in list(deg_dist.bins())]
#
# # Esperamos a tener mas nodos...de momento es muy pobre con todo
# plt.hist(vals[0:50], bins[0:50])
# plt.show()
#
# # Verified users from dataset
# verified = get_verified(users)
# # Obtain communities
#
# print "Finding communities . . . "
# partition = find_comm(graph,1)
#
# for i in range(3):
#     get_cluster_nodes(graph, partition[i], filename,i)
#
#
# print "Looking for most popular users . . ."
# #Get user who are hubs of the network
# ind = get_hubs(graph, 10)
#
# get_twitter_info(graph, ind, filename)
#
# print "Writing graph in pajek format"
# graph.write_pajek("1000.net")
