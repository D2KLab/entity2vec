'''
Reference implementation of node2vec. 

Author: Aditya Grover

For more details, refer to the paper:
node2vec: Scalable Feature Learning for Networks
Aditya Grover and Jure Leskovec 
Knowledge Discovery and Data Mining (KDD), 2016
'''

import argparse
import numpy as np
import networkx as nx
import node2vec_uniform
from gensim.models import Word2Vec

import time


def parse_args():
	'''
	Parses the node2vec arguments.
	'''
	parser = argparse.ArgumentParser(description="Run node2vec.")

	parser.add_argument('--input', nargs='?', default='graph/karate.edgelist',
	                    help='Input graph path')

	parser.add_argument('--output', nargs='?', default='emb/karate.emb',
	                    help='Embeddings path')

	parser.add_argument('--dimensions', type=int, default=128,
	                    help='Number of dimensions. Default is 128.')

	parser.add_argument('--walk-length', type=int, default=10,
	                    help='Length of walk per source. Default is 10.')

	parser.add_argument('--num-walks', type=int, default=10,
	                    help='Number of walks per source. Default is 40.')

	parser.add_argument('--window-size', type=int, default=10,
                    	help='Context size for optimization. Default is 10.')

	parser.add_argument('--iter', default=1, type=int,
                      help='Number of epochs in SGD')

	parser.add_argument('--workers', type=int, default=8,
	                    help='Number of parallel workers. Default is 8.')

	parser.add_argument('--p', type=float, default=1,
	                    help='Return hyperparameter. Default is 1.')

	parser.add_argument('--q', type=float, default=1,
	                    help='Inout hyperparameter. Default is 1.')

	parser.add_argument('--weighted', dest='weighted', action='store_true',
	                    help='Boolean specifying (un)weighted. Default is unweighted.')
	parser.add_argument('--unweighted', dest='unweighted', action='store_false')
	parser.set_defaults(weighted=False)

	parser.add_argument('--directed', dest='directed', action='store_true',
	                    help='Graph is (un)directed. Default is undirected.')
	parser.add_argument('--undirected', dest='undirected', action='store_false')
	parser.set_defaults(directed=False)

	return parser.parse_args()

def read_graph():
	'''
	Reads the input network in networkx.
	'''
	print 'asd'
	if args.weighted:
		G = nx.read_edgelist(args.input,  nodetype = int,data=(('weight',float),), create_using=nx.DiGraph())
	else:
		G = nx.read_edgelist(args.input, nodetype = int, create_using=nx.DiGraph())
		for edge in G.edges():
			G[edge[0]][edge[1]]['weight'] = 1

	if not args.directed:
		G = G.to_undirected()

	return G

def learn_embeddings(walks):
	'''
	Learn embeddings by optimizing the Skipgram objective using SGD.
	'''
	walks = [map(str, walk) for walk in walks]


	for walk in walks:
		os.system('echo %s >> walks_p%f_q%f.txt' %(walk,args.p,args.q))

	print "defined walks inside learn embeddings"
	model = Word2Vec(walks, size=args.dimensions, window=args.window_size, min_count=0, 
		workers=args.workers, iter=args.iter, negative = 15)
	print "defined model using w2v"
	model.save_word2vec_format(args.output)
	print "saved model in word2vec format"

	return

def main(args):
	'''
	Pipeline for representational learning for all nodes in a graph.
	'''

	start_time = time.time()

	nx_G = read_graph()
	print 'read graph'
	G = node2vec_uniform.Graph(nx_G, args.directed, args.p, args.q)
	print 'defined G'
	#G.preprocess_transition_probs()
	#print 'preprocessed'
	walks = G.simulate_walks(args.num_walks, args.walk_length)
	print 'defined walk'
	learn_embeddings(walks)
	print 'learned embeddings'


	print("--- %s seconds ---" % (time.time() - start_time))

args = parse_args()
main(args)




