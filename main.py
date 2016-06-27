from utils import *
from subprocess import call


filename = "query_output1000.json"
# Create graph from file
print "Creating graph . . ."
graph = create_graph(filename,1)

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
