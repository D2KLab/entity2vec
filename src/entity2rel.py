from gensim.models import Word2Vec
import argparse
from gensim.models.keyedvectors import KeyedVectors

#return a set of similarity scores 

class entity2rel(object):

	def __init__(self, embedding_file, binary = True):

		self.embedding_file = embedding_file
		self.binary = binary

		self._load_embedding()

	def _load_embedding(self):

		self.embedding = KeyedVectors.load_word2vec_format(self.embedding_file, binary=self.binary) #a set of embeddings as a generator


	def similarity(self, uri1, uri2):

		return self.embedding.similarity(uri1,uri2)


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

	embedding = "../emb/movielens_1m_no_overwrite/feedback/num500_p1_q4_l10_d500.emd"

	args = entity2rel.parse_args()

	rel = entity2rel(embedding)

	print('\n')
	print("Similarity between Pulp Fiction and Jackie Brown is:\n")
	s = rel.similarity(uri1, uri2)
	print(s)
	print('\n')

	print("Similarity between Pulp Fiction and Romeo and Juliet is:\n")
	s = rel.similarity(uri1, uri3)
	print(s)
	print('\n')