from utils import *
import igraph

graph = igraph.Graph(5)

graph.add_edges([(0,1),(1,2),(1,3),(2,3),(2,4),(3,4)])

path = simulation (graph, None, 0.7, [1], 2, 2 )

print path
