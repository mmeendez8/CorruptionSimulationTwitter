# -*- coding: utf-8 -*-
import json
import igraph
import numpy as np
from random import randint, random


bagofwords = ["pp","alcalde","nngg", "partido", "popular", "populares", "derecha", "nuevas generaciones","concejal","parlamento"]


def checkbio (bio):
    bio = bio.lower()
    for w in bagofwords:
        if w in bio: return True
    return False

def checklocation(location, location_bow):
    location = location.lower().encode('utf-8')
    for valid_location in location_bow:
        if valid_location in location:
            return True
    return False

def load_locations(filename):
    with open(filename, 'r') as locationsfile:
        location_bow = locationsfile.readlines()

    location_bow = [strip_accents(location.strip().lower()) for location in location_bow]

    return location_bow

def strip_accents(s):
    """Since we are analyzing only Spanish we will tackle this problem
    by replacing vowels with accents"""
    subs_accents = {u'á':u'a', u'é':u'e', u'í':u'i',
                    u'ó':u'o', u'ú':u'u'}
    s = s.decode('utf-8')
    s
    for c in s:
        if c in subs_accents.keys():
            s = s.replace(c, subs_accents[c])
    return s.encode('utf-8')


def _plot(g, membership,filename):
    if membership is not None:
        gcopy = g.copy()
        edges = []
        edges_colors = []
        for edge in g.es():
            if membership[edge.tuple[0]] != membership[edge.tuple[1]]:
                edges.append(edge)
                edges_colors.append("gray")
            else:
                edges_colors.append("black")
        gcopy.delete_edges(edges)
        layout = gcopy.layout("kk")
        g.es["color"] = edges_colors
    else:
        layout = g.layout("kk")
        g.es["color"] = "gray"
    visual_style = {}
    visual_style["vertex_label_dist"] = 0
    visual_style["vertex_shape"] = "circle"
    visual_style["edge_color"] = g.es["color"]
    # visual_style["bbox"] = (4000, 2500)
    visual_style["vertex_size"] = 30
    visual_style["layout"] = layout
    visual_style["bbox"] = (1024, 768)
    visual_style["margin"] = 40
    for vertex in g.vs():
        vertex["label"] = vertex.index
    if membership is not None:
        colors = []
        for i in range(0, max(membership)+1):
            colors.append('%06X' % randint(0, 0xFFFFFF))
        for vertex in g.vs():
            vertex["color"] = str('#') + colors[membership[vertex.index]]
        visual_style["vertex_color"] = g.vs["color"]
    igraph.plot(g,filename, **visual_style)



def create_graph(data,plot=0):
    # Read json file
    # with open(filename, 'r') as data_file:
    #     data = json.load(data_file)
    n = len(data)
    g = igraph.Graph()
    g.add_vertices(n)
    # Create graph vertices
    for user in data:
        node = data[user]["node"]
        # Set attributes to the node
        g.vs[node-1]["id"] = user
        # Get neighbours
        neighbours = data[user]["neighbours"]
        # Create string with all edges of one user
        edges_list = [(node-1,data[str(neigh)]["node"]-1) for neigh in neighbours]
        # Add edges
        g.add_edges(edges_list)
    if plot:
        _plot(g,None,'Figures/original_graph.png')
    return g

def export_pajek(output_filename, partition):
    # Export partition to a clu file
    with open(output_filename, 'w') as pajek_file:
        partition.insert(0,"*Vertices " + str(len(partition)))
        for line in partition:
            pajek_file.write(str(line) + "\n")

def find_comm(graph,plot=0):
    dendogram = graph.community_edge_betweenness(directed=False,clusters=3)
    # convert it into a flat clustering
    partition = dendogram.as_clustering()
    export_pajek("Partitions/test.clu",partition.membership)
    modularity = graph.modularity(partition)
    if plot:
        _plot(graph,partition.membership,"Figures/partition_graph.png")
    return partition

def get_hubs(graph, nhubs):
    matrix = graph.get_adjacency()
    matrix = np.array(matrix.data)
    connections = np.sum(matrix,axis=0)
    # Get index of most connected novedades
    ind = np.argpartition(connections,  -nhubs)[-nhubs:]
    return ind

def get_twitter_info(graph, ind, filename):
    # Read json file
    with open(filename, 'r') as data_file:
        data = json.load(data_file)
    with open("hubusers.txt",'w') as f:
        for node in ind:
            user = graph.vs[node]["id"]
            f.write(data[user]["name"].encode('utf-8')+'\n')
            f.write(data[user]["bio"].encode('utf-8')+'\n')
            f.write("\n")

def get_cluster_nodes(graph, partition, filename,number):
    ind = []
    with open(filename, 'r') as data_file:
        data = json.load(data_file)
    with open("partition" +str(number)+".txt",'w') as f:
        for node in partition:
            user = graph.vs[node]["id"]
            print node
            f.write(data[user]["bio"].encode('utf-8')+'\n')
            f.write("\n")

def check_same_loc(graph, node1, node2, users):
    locations = load_locations('municipios_madrid.txt')
    for location in locations:
        if location in users[graph.vs[node1]["id"]]["location"]:
            loc1 = locations.index[location]
            break

    for location in locations:
        if location in users[graph.vs[node2]["id"]]["location"]:
            loc2 = locations.index[location]
            break

    if loc1 == loc2:
        return 1
    else:
        return 0

def degree_dist(graph):
    """ Compute the histogram corresponding to the degree distribution
    of the given network"""
    deg_histogram = graph.degree_distribution()
    return deg_histogram


def get_verified(data):
    """Return verified users"""
    verified = [user for key,user in data.items() if user['verified']]
    return verified

def remove_root(data, root_id):
    """ Nada, de momento no lo hacemos ya que entonces hay
    nodos que quedan totalmente huerfanos sin ningun vecino y peta"""
    del(data[root_id])
    for user in data.itervalues():
        try:
            user['neighbours'].remove(int(root_id))
        except ValueError:
            pass
    return data

def simulation (graph, users, mu, beta, infected, Nrep ):
    state = [0] * len(graph.vs)
    state[infected] = 1
    new_state = state
    for step in range(Nsteps):
        new_infected = []
        # Iterate over previously infected nodes
        for infected_node in infected:
            neighbors = graph.neighbors(infected_node)
            susceptible = []
            for n in neighbors:
                # Get only non corrupted nodes
                if state[n]==0:
                    susceptible.append(n)
            # Iterate susceptible neighbors
            for s in susceptible:
                if random() < beta + check_same_loc(graph,s,infected_node,users)*10*beta:
                    # Infected
                    new_infected.append(s)
        # Set corrupted to not take them into acount in future
        state[infected] = -1
        # Set new infected
        state[new_infected] = 1
