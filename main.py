from utils import *

# Create graph from file
graph = create_graph("query_output1000.json",1)

# Obtain communities
find_comm(graph,1)
