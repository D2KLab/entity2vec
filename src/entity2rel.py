from __future__ import print_function
from gensim.models import Word2Vec
import argparse
from gensim.models.keyedvectors import KeyedVectors

#return a set of similarity scores from a set of property-specific embeddings

class entity2rel(object):


	def __init__(self, load_embeddings, binary = True):

		self.binary = binary
		self.embedding_files = []


	def add_embedding(self, embedding_file):

		#a list of embedding names

		self.embedding_files.append(KeyedVectors.load_word2vec_format(embedding_file, binary=self.binary))

	def relatedness_score_by_position(self,uri1,uri2,pos):

		try:

			score = self.embedding_files[pos].similarity(uri1,uri2)

		except KeyError:

			score = 0.

		return score

	def relatedness_scores(self, uri1, uri2, skip = False):

		scores = []

		if skip:
			ind = skip
		else:
			ind = len(self.embedding_files) #unless provided with a skip index, take them all

		for embedding in self.embedding_files[0:ind]:

			try:

				scores.append(embedding.similarity(uri1,uri2))

			except KeyError:

				scores.append(0.)

		return scores


	@staticmethod
	def parse_args():

		parser = argparse.ArgumentParser(description="Measure entity relatedness.")

		parser.add_argument('--embedding', help='File with embeddings')

		parser.add_argument('--binary', help='Whether the embeddings are stored in binary format')


if __name__ == '__main__':

	#test

	uri1 = "http://dbpedia.org/resource/Pulp_Fiction"

	uri2 = "http://dbpedia.org/resource/Jackie_Brown_(film)"

	uri3 = "http://dbpedia.org/resource/Romeo_and_Juliet_(1996_movie)"

	embedding1 = "emb/movielens_1m_no_overwrite/feedback/num500_p1_q4_l10_d500.emd"

	embedding2 = "emb/movielens_1m_no_overwrite/dbo:director/num500_p1_q4_l10_d500.emd"

	args = entity2rel.parse_args()

	rel = entity2rel()

	rel.add_embedding(embedding1)
	rel.add_embedding(embedding2)

	print('\n')
	print("Relatedness between Pulp Fiction and Jackie Brown is:\n")
	scores = rel.relatedness_scores(uri1, uri2)
	for s in scores:
		print(s)
		print('\n')

	print("Relatedness between Pulp Fiction and Romeo and Juliet is:\n")
	scores = rel.relatedness_scores(uri1, uri3)

	for s in scores:
		print(s)
		print('\n')
