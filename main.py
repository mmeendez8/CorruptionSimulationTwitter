from utils import *
<<<<<<< HEAD
import json
import matplotlib.pyplot as plt

# Load information from JSON file
with open('query_output1000.json', 'r') as jsonfile:
    users = json.load(jsonfile)
=======
from subprocess import call
>>>>>>> retry-fix


filename = "query_output1000.json"
# Create graph from file
print "Creating graph . . ."
graph = create_graph(filename,1)

# Obtain degree distribution
deg_dist = degree_dist(graph)

bins = [tup[0] for tup in list(deg_dist.bins())]
vals = [tup[2] for tup in list(deg_dist.bins())]

# Esperamos a tener mas nodos...de momento es muy pobre con todo
plt.hist(vals[0:50], bins[0:50])

# Obtain communities

print "Finding communities . . . "
partition = find_comm(graph,1)

for i in range(3):
    get_cluster_nodes(graph, partition[i], filename,i)


#print "Looking for most popular users . . ."
# Get user who are hubs of the network
#ind = get_hubs(graph, 10)

#get_twitter_info(graph, ind, filename)

#print "Writing graph in pajek format"
#graph.write_pajek("1000.net")
