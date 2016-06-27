from utils import *

filename = "query_output1000.json"
# Create graph from file
graph = create_graph(filename,1)

# Obtain communities
find_comm(graph,1)

# Get user who are hubs of the network
ind = get_hubs(graph, 10)

get_twitter_info(graph, ind, filename)

graph.write_pajek("1000.net")
