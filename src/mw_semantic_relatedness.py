import networkx as nx
import numpy as np
import math

class MW(object):

	def __init__(self,edgelist):

		self.edgelist = edgelist

		self._read_graph()

	def _read_graph(self):

		self.graph = nx.read_edgelist(self.edgelist,  data=(('weight',float),), create_using=nx.DiGraph(), edgetype = str)

		self.N = len(self.graph.nodes())

	def relatedness(self, node1, node2):

		G = self.graph

		A_in_edges = G.in_edges(node1)
		
		A = [i for i,j in A_in_edges]

		n_A = len(A)

		B_in_edges = G.in_edges(node2)
		
		B = [i for i,j in B_in_edges]

		n_B = len(B)

		n_A_B = len([i for i in A if i in B])

		m_w = 1 - (np.log(max(n_A,n_B)) - np.log(n_A_B))/(np.log(self.N) - np.log(min(n_A,n_B))) 

		if math.isnan(m_w) == True: #by definition if one of the two nodes has no inlinks
			m_w = 0.

		return m_w


if __name__ == '__main__':

	mw = MW('../tests/prova.edgelist')

	s = mw.similarity(u'<http://dbpedia.org/resource/Actrius>', u'<http://dbpedia.org/resource/Catalan_language>')

	print(s)
