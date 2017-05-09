from __future__ import print_function
from gensim.models import Word2Vec
import argparse
from gensim.models.keyedvectors import KeyedVectors
import sparql
#return a set of similarity scores from a set of property-specific embeddings

class entity2rel(object):


	def __init__(self, binary = True):

		self.binary = binary
		self.embedding_files = []


	def add_embedding(self, embedding_file):

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


	def parse_ceccarelli_line(self, line):

		line = line.split(' ')

		relevance = int(line[0])

		query_id = int((line[1].split(':'))[1])

		wiki_id_query = int(line[2])

		wiki_id_candidate = int(line[3])

		return (wiki_id_query, query_id, wiki_id_candidate, relevance)


	def write_line(self, query, query_id, candidate, relevance, file):

		scores = self.relatedness_scores(query, candidate_entity)

		file.write('%d qid:%d' %(relevance,query_id))

		count = 1

		l = len(scores)

		for score in scores:

			if count == l + 1: #last score, end of line

				file.write(' %d:%f # %s\n' %(count,score,candidate))

			else:

				file.write(' %d:%f' %(count,score))

				count += 1


	def feature_generator(self, data):

		data_name = (data.split('/')[-1]).split('.')[0]

		with codecs.open('features/ceccarelli/%s.svm' %(data_name),'w', encoding='utf-8') as data_write:

			with codecs.open(data,'r', encoding='utf-8') as data_read:

				for i, line in enumerate(data_read):

					wiki_id_query, query_id, wiki_id_candidate, relevance = self.parse_ceccarelli_line(line)

					print(wiki_id_query)

					try:

						uri_query = sparql.get_uri_from_wiki_id(wiki_id_query)

						uri_candidate = sparql.get_uri_from_wiki_id(wiki_id_candidate)

					except KeyError:
						continue

					self.write_line(uri_query, query_id, uri_candidate, relevance)

		print('finished writing features')

		print("--- %s seconds ---" % (time.time() - start_time))


	def run(self,data):


		e2r = self.entity2rel()

		e2r.feature_generator(data)


	def test(self):

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


	@staticmethod
	def parse_args():

		parser = argparse.ArgumentParser(description="Measure entity relatedness.")

		parser.add_argument('--embedding', help='File with embeddings')

		parser.add_argument('--binary', help='Whether the embeddings are stored in binary format')

		parser.add_argument('--ground_truth', help = 'data from which features are generated')



if __name__ == '__main__':

	#test

	start_time = time.time()

	args = entity2rel.parse_args()

	e2r = entity2rel(args.ground_truth)

	e2r.add_embedding(args.embedding)

	e2r.run()

	print("--- %s seconds ---" % (time.time() - start_time))