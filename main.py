from utils import *
import json
import matplotlib.pyplot as plt

# Load information from JSON file
with open('query_output1000.json', 'r') as jsonfile:
    users = json.load(jsonfile)

# Create graph from file
graph = create_graph("query_output1000.json",1)

# Obtain degree distribution
deg_dist = degree_dist(graph)

bins = [tup[0] for tup in list(deg_dist.bins())]
vals = [tup[2] for tup in list(deg_dist.bins())]

# Esperamos a tener mas nodos...de momento es muy pobre con todo
plt.hist(vals[0:50], bins[0:50])

# Obtain communities
#find_comm(graph,1)
