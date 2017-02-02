import argparse
import numpy as np
import networkx as nx
import node2vec
from gensim.models import Word2Vec
import os
import pickle
import time
import gzip


def parse_args():
	'''
	Parses the node2vec arguments.
	'''
	parser = argparse.ArgumentParser(description="Run learn embeddings.")

	parser.add_argument('--input', nargs='?', default=' ',
	                    help='Input walks path')

	parser.add_argument('--output', nargs='?', default='emb/karate.emb',
	                    help='Embeddings path')

	parser.add_argument('--dimensions', type=int, default=500,
	                    help='Number of dimensions. Default is 128.')

	parser.add_argument('--window-size', type=int, default=10,
                    	help='Context size for optimization. Default is 10.')

	parser.add_argument('--iter', default=5, type=int,
                      help='Number of epochs in SGD')

	parser.add_argument('--workers', type=int, default=8,
	                    help='Number of parallel workers. Default is 8.')

	return parser.parse_args()


class Sentences(object):
    def __init__(self, fname):
        self.fname = fname
 
    def __iter__(self):
    
		try:
			file_loc = self.fname		
			for line in gzip.open(file_loc, mode='rt'):
				line = line.rstrip('\n')
				words = line.split(" ")
				yield words
		except Exception:
			print("Failed reading file:")
			print(self.fname)


def learn_embeddings(walks):
	'''
	Learn embeddings by optimizing the Skipgram objective using SGD.
	'''

	sentences = Sentences(walks)

	model = Word2Vec(sentences, size=args.dimensions, window=args.window_size, min_count=0, 
		workers=args.workers, iter=args.iter, negative = 25, sg = 1)
	print "defined model using w2v"
	model.save_word2vec_format(args.output)
	print "saved model in word2vec format"

	return

def main(args):
	'''
	Pipeline for representational learning for all nodes in a graph.
	'''	

	start_time = time.time()

	print 'Parameters:\n'

	print 'iterations = %d\n' %args.iter

	print 'window size = %d\n' %args.window_size

	print 'dimensions = %d\n' %args.dimensions


	learn_embeddings(args.input)
	print 'learned embeddings'

	print("--- %s seconds ---" % (time.time() - start_time))

args = parse_args()

main(args)


