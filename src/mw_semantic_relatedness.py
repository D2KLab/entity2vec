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

		if n_A*n_B == 0:
			return 0.

		else:

			m_w = 1 - (np.log(max(n_A,n_B)) - np.log(n_A_B))/(np.log(self.N) - np.log(min(n_A,n_B))) 

			return m_w


if __name__ == '__main__':

	mw = MW('tests/test_mw.edgelist')

	s = mw.relatedness(u'<http://dbpedia.org/resource/Copenhagen>', u'<http://dbpedia.org/resource/Denmark>')

	print(s)