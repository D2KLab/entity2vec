# -*- encoding: utf8 -*-

import networkx as nx
import numpy as np
import math
from entity2rel import entity2rel

class MW(entity2rel):

	def __init__(self,edgelist):

		entity2rel.__init__(self)

		self.edgelist = edgelist

		self._read_graph()

	def _read_graph(self):

		self.graph = nx.read_edgelist(self.edgelist,  data=(('weight',float),), create_using=nx.DiGraph(), edgetype = str)

		self.N = len(self.graph.nodes())

	#overriding of the parent function
	def relatedness_scores(self, node1, node2):

		G = self.graph

		A_in_edges = G.in_edges(node1)
		
		A = [i for i,j in A_in_edges]

		n_A = len(A)

		B_in_edges = G.in_edges(node2)
		
		B = [i for i,j in B_in_edges]

		n_B = len(B)

		n_A_B = len([i for i in A if i in B])


		if n_A*n_B == 0:
			return [0.]

		else:

			m_w = 1 - (np.log(max(n_A,n_B)) - np.log(n_A_B))/(np.log(self.N) - np.log(min(n_A,n_B))) 

			return [m_w]


	def run(self, data):

		mw = self.MW()

		mw.feature_generator(data)


if __name__ == '__main__':

	print('test relatedness:')

	mw = MW('tests/test_mw.edgelist')

	s = mw.relatedness_scores(u'<http://dbpedia.org/resource/Copenhagen>', u'<http://dbpedia.org/resource/Denmark>')

	print(s)

	print('test feature generation:')

	mw.feature_generator('datasets/ceccarelli/training.svm')