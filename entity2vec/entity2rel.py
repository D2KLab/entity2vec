from __future__ import print_function

import argparse
import codecs
import time

from gensim.models.keyedvectors import KeyedVectors
from entity2vec.sparql import Sparql


###################################################################
# Computes a set of relatedness scores between a pair of entities #
# from a set of property-specific Knowledge Graph embeddings      #
###################################################################


class Entity2Rel(object):
    def __init__(self, binary=True):

        self.binary = binary
        self.embedding_files = []

    # add embedding file
    def add_embedding(self, embedding_file):

        self.embedding_files.append(KeyedVectors.load_word2vec_format(embedding_file, binary=self.binary))

    # access a particular embedding file and get the relatedness score
    def relatedness_score_by_position(self, uri1, uri2, pos):

        try:

            score = self.embedding_files[pos].similarity(uri1, uri2)

        except KeyError:

            score = 0.

        return score

    # get all the relatedness scores
    def relatedness_scores(self, uri1, uri2, skip=False):

        scores = []

        if skip:
            ind = skip
        else:
            ind = len(self.embedding_files)  # unless provided with a skip index, take them all

        if uri1 is None or uri2 is None:
            scores = [0.]

        for embedding in self.embedding_files[0:ind]:

            try:

                scores.append(embedding.similarity(uri1, uri2))

            except KeyError:

                scores.append(0.)

        return scores

    # parse ceccarelli benchmark line
    @staticmethod
    def parse_ceccarelli_line(line):

        line = line.split(' ')

        relevance = int(line[0])

        query_id = int((line[1].split(':'))[1])

        doc_id = line[-1]

        ids = line[-2].split('-')

        wiki_id_query = int(ids[0])

        wiki_id_candidate = int(ids[1])

        return wiki_id_query, query_id, wiki_id_candidate, relevance, doc_id

    # write line in the svm format
    def write_line(self, query_uri, qid, candidate_uri, relevance, file, doc_id):

        scores = self.relatedness_scores(query_uri, candidate_uri)

        file.write('%d qid:%d' % (relevance, qid))

        count = 1

        l = len(scores)

        for score in scores:

            if count == l:  # last score, end of line

                file.write(' %d:%f # %s-%s %d\n' % (count, score, query_uri, candidate_uri, int(doc_id)))

            else:

                file.write(' %d:%f' % (count, score))

                count += 1

    def feature_generator(self, data):

        data_name = (data.split('/')[-1]).split('.')[0]

        with codecs.open('features/ceccarelli/%s.svm' % data_name, 'w', encoding='utf-8') as data_write:
            with codecs.open(data, 'r', encoding='utf-8') as data_read:
                for i, line in enumerate(data_read):
                    wiki_id_query, qid, wiki_id_candidate, relevance, doc_id = self.parse_ceccarelli_line(line)

                    print(wiki_id_query)

                    uri_query = Sparql.get_uri_from_wiki_id(wiki_id_query)

                    uri_candidate = Sparql.get_uri_from_wiki_id(wiki_id_candidate)

                    self.write_line(uri_query, qid, uri_candidate, relevance, data_write, doc_id)

        print('finished writing features')

        print("--- %s seconds ---" % (time.time() - start_time))

    def run(self, data):

        e2r = self.entity2rel()

        e2r.feature_generator(data)

    def test(self):

        uri1 = "http://dbpedia.org/resource/Pulp_Fiction"

        uri2 = "http://dbpedia.org/resource/Jackie_Brown_(film)"

        uri3 = "http://dbpedia.org/resource/Romeo_and_Juliet_(1996_movie)"

        embedding1 = "emb/movielens_1m_no_overwrite/feedback/num500_p1_q4_l10_d500.emd"

        embedding2 = "emb/movielens_1m_no_overwrite/dbo:director/num500_p1_q4_l10_d500.emd"

        args = Entity2Rel.parse_args()

        rel = Entity2Rel()

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
        parser.add_argument('--ground_truth', help='data from which features are generated')

        return parser.parse_args()


if __name__ == '__main__':
    # test

    start_time = time.time()

    args = Entity2Rel.parse_args()

    e2r = Entity2Rel(args.ground_truth)

    e2r.add_embedding(args.embedding)

    e2r.run()

    print("--- %s seconds ---" % (time.time() - start_time))
