import optparse
import os
import codecs
import collections
import numpy as np
from gensim.models import Word2Vec
from pandas import read_json
from entity2vec import entity2vec
from entity2rel import entity2rel
import argparse
import time

class entity2rec(entity2vec, entity2rel):


	def __init__(self, is_directed, preprocessing, is_weighted, p, q, walk_length, num_walks, dimensions, window_size, workers, iterations, config, sparql, dataset, entities, default_graph, training, test, binary=True):

		entity2vec.__init__(self, is_directed, preprocessing, is_weighted, p, q, walk_length, num_walks, dimensions, window_size, workers, iterations, config, sparql, dataset, entities, default_graph)

		entity2rel.__init__(self, binary)

		self.training = training

		self.test = test

		self._get_embedding_files()

		self._get_items_liked_by_user() #defines the dictionary of items liked by each user in the training set


	def _get_embedding_files(self):

		for prop in self.properties:

			self.add_embedding('emb/%s/%s/num%s_p%s_q%s_l%s_d%s.emd' %(self.dataset, prop, self.num_walks, self.p, self.q, self.walk_length,self.dimensions))


	def _get_items_liked_by_user(self):

		self.all_train_items = []

		self.items_liked_by_user_dict = collections.defaultdict(list)

		with codecs.open(self.training,'r', encoding='utf-8') as train:

			for line in train:

				line = line.split(' ')

				u = line[0]

				item = line[1]

				relevance = int(line[2])

				if relevance > 4: #only relevant items are used to compute the similarity

					self.items_liked_by_user_dict[u].append(item)

				self.all_train_items.append(item)



	def collab_similarity(self, user, item):

		#feedback embedding is always the last of the list

		return self.relatedness_score_by_position(user, item, -1)


	def content_similarities(self, user, item):
		
		#all other properties

		items_liked_by_user = self.items_liked_by_user_dict[user]

		sims = []
		
		for past_item in items_liked_by_user:

			sims.append(self.relatedness_scores(past_item,item, -1)) #append a list of property-specific scores, skip feedback

		return np.mean(sims, axis = 0) #return a list of averages of property-specific scores


	@staticmethod
	def parse_user_id(user):

		return int(user.strip('user')) #29


	@staticmethod
	def parse_users_items_rel(line):

		line = line.split(' ')

		user = line[0] #user29

		user_id = entity2rec.parse_user_id(user) #29

		item = line[1] #http://dbpedia.org/resource/The_Golden_Child

		relevance = int(line[2]) #5

		#binarization of the relevance values
		relevance = 1 if relevance >= 4 else 0		

		return (user, user_id, item, relevance)


	def write_line(self,user, user_id, item, relevance, file):

		file.write('%d qid:%d' %(relevance,user_id))

		count = 1

		collab_score = self.collab_similarity(user, item)

		file.write(' %d:%f' %(count,collab_score))

		content_scores = self.content_similarities(user, item)

		l = len(content_scores)

		for content_score in content_scores:

			if count == l: #last score, end of line

				file.write(' %d:%f # %s\n' %(count,content_score,item))

			else:

				file.write(' %d:%f' %(count,content_score))

				count += 1		


	def get_candidates(self,user):

		#get candidates according to the all unrated items protocol

		return


	def feature_generator(self):

		#write training set
		with codecs.open('features/%s/train.svm' %self.dataset,'w', encoding='utf-8') as train_write:

			with codecs.open(self.training,'r', encoding='utf-8') as training:

				for i, line in enumerate(training):

					user, user_id, item, relevance = entity2rec.parse_users_items_rel(line)

					print(user,item)

					self.write_line(user, user_id, item, relevance, train_write)

			print('finished written training')

			'''
		with codecs.open('features/%s/test.svm','w', encoding='utf-8') as test_write:

			with codecs.open(self.test,'r', encoding='utf-8') as test:

				for i, line in enumerate(test):

					#write some candidate items

					user, user_id, item, relevance = parse_users_items_rel(line)

					write_line(user, user_id, item, relevance, test_write)

					if i > 0: #skip first iteration

						if user == prev_user:

							continue

						else:

							candidate_items = self.get_candidate_items(user)

							for item in candidate_items:

								write_line(user, user_id, item, relevance)

					prev_user = user


			print('finished written test')
	'''

	def shuffle_features(self):

		return


	def run(self, run_all):

		if run_all:
			self.entity2vec.run()

		else:
			self.feature_generator()


	@staticmethod
	def parse_args():

		'''
		Parses the entity2vec arguments.
		'''

		parser = argparse.ArgumentParser(description="Run entity2rec.")


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

		parser.add_argument('--sparql', dest = 'sparql',
		                    help='Whether downloading the graphs from a sparql endpoint')
		parser.set_defaults(sparql=False)		

		parser.add_argument('--entities', dest = 'entities', default = "all",
		                    help='A specific list of entities for which the embeddings have to be computed')


		parser.add_argument('--default_graph', dest = 'default_graph', default = False,
		                    help='Default graph to query when using a Sparql endpoint')

		parser.add_argument('--train', dest='train', help='train')

		parser.add_argument('--test', dest='test', help='test')

		parser.add_argument('--run_all', dest='run_all', default = False, help='If computing also the embeddings')

		return parser.parse_args()


if __name__ == '__main__':


	start_time = time.time()

	args = entity2rec.parse_args()

	rec = entity2rec(args.directed, args.preprocessing, args.weighted, args.p, args.q, args.walk_length, args.num_walks, args.dimensions, args.window_size, args.workers, args.iter, args.config_file, args.sparql, args.dataset, args.entities, args.default_graph, args.train, args.test)

	rec.run(args.run_all)

	print("--- %s seconds ---" % (time.time() - start_time))