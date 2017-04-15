
#simulates the entity2vec walks and serialize them to a txt file

import argparse
import numpy as np
import networkx as nx
import node2vec
from gensim.models import Word2Vec
import os
import pickle
import gzip
import time


def parse_args():
	'''
	Parses the node2vec arguments.
	'''
	parser = argparse.ArgumentParser(description="Run node2vec.")

	parser.add_argument('--input', nargs='?', default='graph/karate.edgelist',
	                    help='Input graph path')

	parser.add_argument('--output', nargs='?', default='walks',
                    help='walks file name')

	parser.add_argument('--walk-length', type=int, default=10,
	                    help='Length of walk per source. Default is 10.')

	parser.add_argument('--num-walks', type=int, default=500,
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

	return parser.parse_args()


def read_graph():
	'''
	Reads the input network in networkx.
	'''
	print 'asd'
	if args.weighted:
		G = nx.read_edgelist(args.input,  data=(('weight',float),), create_using=nx.DiGraph())
	else:
		G = nx.read_edgelist(args.input, create_using=nx.DiGraph())
		for edge in G.edges():
			G[edge[0]][edge[1]]['weight'] = 1

	if not args.directed:
		G = G.to_undirected()

	return G



def main(args):
	'''
	Pipeline for representational learning for all nodes in a graph.
	'''	

	start_time = time.time()

	print('Parameters:\n')

	print('p = %f\n' %args.p)

	print('q = %f\n' %args.q)

	print('num walks = %d\n' %args.num_walks)

	nx_G = read_graph()
	print('read graph')

	#G = node2vec.Graph(nx_G, args.directed, args.p, args.q)
	#print 'defined G'

	G = node2vec.Graph(nx_G, args.directed, args.p, args.q, args.preprocessing)
	print('defined G')

	#print(G.preprocessing)

	if G.preprocessing:
		G.preprocess_transition_probs()
		print('preprocessed')

	#G.preprocess_transition_probs()
	#print 'preprocessed'
	G.simulate_walks(args.num_walks, args.walk_length, args.output, args.p, args.q)
	print('defined walk')

	print("--- %s seconds ---" % (time.time() - start_time))

args = parse_args()

main(args)
