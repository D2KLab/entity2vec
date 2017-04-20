import numpy as np
import networkx as nx
import random
import gzip



class Graph():
	
	def __init__(self, nx_G, is_directed, p, q, preprocessing):
		self.G = nx_G
		self.is_directed = is_directed
		self.p = p
		self.q = q
		self.preprocessing = preprocessing


	def node2vec_walk(self, walk_length, start_node):
		'''
		Simulate a random walk starting from start node.
		'''
		G = self.G

		walk = [start_node]

		while len(walk) < walk_length:

			cur = walk[-1]
			cur_nbrs = sorted(G.neighbors(cur))

			if len(cur_nbrs) > 0:

				if self.preprocessing:

					alias_nodes = self.alias_nodes
					alias_edges = self.alias_edges

					if len(walk) == 1: #first step of the walk, no previous node

						walk.append(cur_nbrs[alias_draw(alias_nodes[cur][0], alias_nodes[cur][1])])

					else:
						prev = walk[-2]

						next_node = cur_nbrs[alias_draw(alias_edges[(prev, cur)][0], 
							alias_edges[(prev, cur)][1])]

						walk.append(next_node)

				else:

					p = self.p
					q = self.q
					G = self.G

					unnormalized_probs = []

					if len(walk) == 1: #first step of the walk, no previous node

						for dst_nbr in cur_nbrs:

							unnormalized_probs.append(G[cur][dst_nbr]['weight'])

						norm_const = sum(unnormalized_probs)

						normalized_probs =  [float(u_prob)/norm_const for u_prob in unnormalized_probs]

						next_node = cur_nbrs[np.random.multinomial(1,normalized_probs).argmax()]

						walk.append(next_node)

					else:

						prev = walk[-2]

						for dst_nbr in cur_nbrs:

							if dst_nbr == prev:

								unnormalized_probs.append(G[cur][dst_nbr]['weight']/p)

							elif G.has_edge(dst_nbr, prev):
								unnormalized_probs.append(G[cur][dst_nbr]['weight'])
							else:
								unnormalized_probs.append(G[cur][dst_nbr]['weight']/q)

						norm_const = sum(unnormalized_probs)
						normalized_probs =  [float(u_prob)/norm_const for u_prob in unnormalized_probs]

						next_node = cur_nbrs[np.random.multinomial(1,normalized_probs).argmax()]

						walk.append(next_node)
			else:
				break

		return walk


	def simulate_walks(self, num_walks, walk_length, output, p, q):
		'''
		Repeatedly simulate random walks from each node.
		'''
		G = self.G

		nodes = G.nodes()
		print 'Walk iteration:'

		with gzip.open('walks/%s' %output,'w') as walks_file:
			for walk_iter in range(num_walks):
				print str(walk_iter+1), '/', str(num_walks)
				random.shuffle(nodes)
				for node in nodes:
					walk = self.node2vec_walk(walk_length=walk_length, start_node=node)
					
					c = 1
					length = len(walk)
					for entity in walk:

						if c == length:
							
							walks_file.write(''.join(entity.encode('utf-8')+'\n'))

						else:

							walks_file.write(''.join(entity.encode('utf-8')))
							walks_file.write(' ')
							c += 1

		return 

	def get_alias_edge(self, src, dst):
		'''
		Get the alias edge setup lists for a given edge.
		'''
		G = self.G
		p = self.p
		q = self.q

		unnormalized_probs = []
		for dst_nbr in sorted(G.neighbors(dst)):
			if dst_nbr == src:
				unnormalized_probs.append(G[dst][dst_nbr]['weight']/p)
			elif G.has_edge(dst_nbr, src):
				unnormalized_probs.append(G[dst][dst_nbr]['weight'])
			else:
				unnormalized_probs.append(G[dst][dst_nbr]['weight']/q)
		norm_const = sum(unnormalized_probs)
		normalized_probs =  [float(u_prob)/norm_const for u_prob in unnormalized_probs]

		return alias_setup(normalized_probs)

	def preprocess_transition_probs(self):
		'''
		Preprocessing of transition probabilities for guiding the random walks.
		'''
		G = self.G
		is_directed = self.is_directed

		alias_nodes = {}
		for node in G.nodes():
			unnormalized_probs = [G[node][nbr]['weight'] for nbr in sorted(G.neighbors(node))]
			norm_const = sum(unnormalized_probs)
			normalized_probs =  [float(u_prob)/norm_const for u_prob in unnormalized_probs]
			alias_nodes[node] = alias_setup(normalized_probs)

		alias_edges = {}
		triads = {}

		if is_directed:
			for edge in G.edges():
				alias_edges[edge] = self.get_alias_edge(edge[0], edge[1])
		else:
			for edge in G.edges():
				alias_edges[edge] = self.get_alias_edge(edge[0], edge[1])
				alias_edges[(edge[1], edge[0])] = self.get_alias_edge(edge[1], edge[0])

		#print alias_nodes

		#print alias_edges

		self.alias_nodes = alias_nodes
		self.alias_edges = alias_edges

		return


def alias_setup(probs):
	'''
	Compute utility lists for non-uniform sampling from discrete distributions.
	Refer to https://hips.seas.harvard.edu/blog/2013/03/03/the-alias-method-efficient-sampling-with-many-discrete-outcomes/
	for details
	'''
	K = len(probs)
	q = np.zeros(K)
	J = np.zeros(K, dtype=np.int)

	smaller = []
	larger = []
	for kk, prob in enumerate(probs):
	    q[kk] = K*prob
	    if q[kk] < 1.0:
	        smaller.append(kk)
	    else:
	        larger.append(kk)

	while len(smaller) > 0 and len(larger) > 0:
	    small = smaller.pop()
	    large = larger.pop()

	    J[small] = large
	    q[large] = q[large] + q[small] - 1.0
	    if q[large] < 1.0:
	        smaller.append(large)
	    else:
	        larger.append(large)

	return J, q

def alias_draw(J, q):
	'''
	Draw sample from a non-uniform discrete distribution using alias sampling.
	'''
	K = len(J)

	kk = int(np.floor(np.random.rand()*K))
	if np.random.rand() < q[kk]:
	    return kk
	else:
	    return J[kk]