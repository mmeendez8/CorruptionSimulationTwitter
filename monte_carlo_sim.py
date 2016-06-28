import random
import networkx as nx
import sys


def monte_carlo_sim(network, mu, beta, Nrep, p0, Tmax, Ttran):
	"""
	mu:			Spontaneous recovery probability
	beta:		Infection of a susceptible S
	Nrep:		Number of repetitions
	p0:			Initial fraction of infected nodest
	Tmax:		Number of time steps
	Ttrans:		Number of steps in the transitory
	"""
	# Number of nodes
	num_nodes = nx.number_of_nodes(network)

	

	# Average of p_steps for each repetition
	p_rep = []

	# Start the simulation
	for repetition in range(Nrep):
		p_steps = []
		nodes_dict = dict.fromkeys(nx.nodes(network))

	# Initial infection nodes
		for node in network.nodes():
			if random.random()<p0:
				nodes_dict[node] = 'I'
			else:
				nodes_dict[node] = 'S'

		nx.set_node_attributes(network, 'state',nodes_dict)		
		for step in range(Tmax):
			
			# Compute fraction of infected p at state t

			p_steps.append(sum([state == 'I' for node,state in nx.get_node_attributes(network, 'state').iteritems()])/float(len(network)))
			#print "p_steps: "+str(p_steps)
			#sys.exit()
			# Copy of the actual state t
			nodes_dict = nx.get_node_attributes(network, 'state')

			for key,value in nx.get_node_attributes(network, 'state').iteritems():

				# For each infected, recover with probability mu
				if value == 'I':
					if random.random() < mu:
						nodes_dict[key] = 'S'
				else:
					# For each susceptible, compute infection based on neighbors
					for neighbour in nx.all_neighbors(network, key):
						if nodes_dict[key] == 'S':
							if random.random() < beta:
								nodes_dict[key] = 'I'
						else:
							break


			nx.set_node_attributes(network, 'state', nodes_dict)


		p_rep.append(float(sum(p_steps[Ttran:])) / len(p_steps[Ttran:]))
		#print "p repetitions: "+str(p_rep)


	return (sum(p_rep) / Nrep)