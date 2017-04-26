from __future__ import print_function
import numpy as np
import networkx as nx
import random
import node2vec
from pandas import read_json
from os.path import isfile, join
from os import mkdir
import argparse
import sparql
from node2vec import node2vec
import time

#Generates property-speficic entity embeddings from a Knowledge Graph

class entity2vec(node2vec):

	def __init__(self, is_directed, preprocessing, is_weighted, p, q, walk_length, num_walks, dimensions, window_size, workers, iterations, config, sparql, dataset):

		node2vec.__init__(self, is_directed, preprocessing, is_weighted, p, q, walk_length, num_walks, dimensions, window_size, workers, iterations)

		self.config_file = config

		self.sparql = sparql

		self.dataset = dataset

		self._define_properties()


	def _define_properties(self):

		property_file = read_json(self.config_file)

		try:

			self.properties = [i for i in property_file[self.dataset]]


		except KeyError: #if no list of properties is specified, take them all

			if self.sparql: #get all the properties from the sparql endpoint

				#TODO				
				pass

			else:
			
				onlyfiles = [f for f in listdir('datasets/%s/graphs/%s') if isfile(join(mypath, f))]

				self.properties = [file.strip('.edgelist') for file in onlyfiles]


	def e2v_walks_learn(self):

		n = self.num_walks

		p = int(self.p)

		q = int(self.q)

		l = self.walk_length

		d = self.dimensions

		it = self.iter

		win = self.window_size

		try:

			mkdir('emb/%s' %(self.dataset))

		except:
			pass

		#iterate through properties

		for prop_name in self.properties:

			graph = "datasets/%s/graphs/%s.edgelist" %(self.dataset, prop_name)

			try:

				mkdir('emb/%s/%s' %(self.dataset,prop_name))

			except:
				pass

			emb_output = "emb/%s/%s/num%d_p%d_q%d_l%d_d%d_iter%d_winsize%d.emd" %(self.dataset, prop_name, n, p, q, l, d, it, win)

			super(entity2vec, self).run(graph,emb_output) #call the run function defined in parent class node2vec


	#generate node2vec walks and learn embeddings for each property
	def run(self):

		if self.sparql:
			#TODO: add query to sparql endpoint 

			pass

		self.e2v_walks_learn() #run node2vec for each property-specific graph


	@staticmethod
	def parse_args():

		'''
		Parses the entity2vec arguments.
		'''

		parser = argparse.ArgumentParser(description="Run entity2vec.")


		parser.add_argument('--walk_length', type=int, default=10,
		                    help='Length of walk per source. Default is 10.')

		parser.add_argument('--num_walks', type=int, default=500,
		                    help='Number of walks per source. Default is 40.')

		parser.add_argument('--p', type=float, default=1,
		                    help='Return hyperparameter. Default is 1.')

		parser.add_argument('--q', type=float, default=1,
		                    help='Inout hyperparameter. Default is 1.')

		parser.add_argument('--weighted', dest='weighted', action='store_true',
		                    help='Boolean specifying (un)weighted. Default is unweighted.')
		parser.add_argument('--unweighted', dest='unweighted', action='store_false')
		parser.set_defaults(weighted=False)

		parser.add_argument('--directed', dest='directed', action='store_true',
		                    help='Graph is (un)directed. Default is directed.')
		parser.set_defaults(directed=False)

		parser.add_argument('--no_preprocessing', dest = 'preprocessing', action='store_false',
		                    help='Whether preprocess all transition probabilities or compute on the fly')
		parser.set_defaults(preprocessing=True)

		parser.add_argument('--dimensions', type=int, default=500,
		                    help='Number of dimensions. Default is 128.')

		parser.add_argument('--window-size', type=int, default=10,
	                    	help='Context size for optimization. Default is 10.')

		parser.add_argument('--iter', default=5, type=int,
	                      help='Number of epochs in SGD')

		parser.add_argument('--workers', type=int, default=8,
		                    help='Number of parallel workers. Default is 8.')

		parser.add_argument('--config_file', nargs='?', default='config/properties.json',
		                    help='Path to configuration file')

		parser.add_argument('--dataset', nargs='?', default='movielens_1m',
		                    help='Dataset')

		parser.add_argument('--sparql', dest = 'sparql', action='store_true',
		                    help='Whether downloading the graphs from a sparql endpoint')
		parser.set_defaults(sparql=False)		

		return parser.parse_args()


if __name__ == '__main__':

	start_time = time.time()

	args = entity2vec.parse_args()

	print('Parameters:\n')	

	print('walk length = %d\n' %args.walk_length)

	print('number of walks per entity = %d\n' %args.num_walks)

	print('p = %s\n' %args.p)

	print('q = %s\n' %args.q)

	print('weighted = %s\n' %args.weighted)

	print('directed = %s\n' %args.directed)

	print('no_preprocessing = %s\n' %args.preprocessing)

	print('dimensions = %s\n' %args.dimensions)

	print('iterations = %s\n' %args.iter)

	print('window size = %s\n' %args.window_size)

	print('workers = %s\n' %args.workers)

	print('config_file = %s\n' %args.config_file)

	print('sparql endpoint = %s\n' %args.sparql)

	print('dataset = %s\n' %args.dataset)

	e2v = entity2vec(args.directed, args.preprocessing, args.weighted, args.p, args.q, args.walk_length, args.num_walks, args.dimensions, args.window_size, args.workers, args.iter, args.config_file, args.sparql, args.dataset)

	e2v.run()

	print("--- %s seconds ---" % (time.time() - start_time))