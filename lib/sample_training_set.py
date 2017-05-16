import codecs
import optparse
import random
import numpy as np

def sample_training_set(feature_file, sampled_feature_file, f):

	with codecs.open(feature_file, 'r', encoding='utf-8') as train:
		
		with codecs.open(sampled_feature_file, 'w', encoding='utf-8') as train_sample:

			query_id = 'qid:1'

			feature_query = []

			for line in train:

				print(line)

				line_split = line.split(' ')

				new_query_id = line_split[1]

				if new_query_id == query_id:

					feature_query.append(line)

				else: #new query, sample and write

					l = len(feature_query)

					k = max([1,int(np.round(f*l))]) #at least one always

					sample = random.sample(feature_query, k)

					for i in sample:
						train_sample.write(i)

					feature_query = []

					feature_query.append(line)

				query_id = new_query_id

			#last query

			l = len(feature_query)

			k = max([1,int(np.round(f*l))])

			sample = random.sample(feature_query, k)

			for i in sample: #writes the last query
				train_sample.write(i)				



if __name__ == '__main__':

    parser = optparse.OptionParser()
    parser.add_option('-o','--output', dest = 'sampled_feature_file', help = 'sampled feature_file')
    parser.add_option('-i','--input', dest = 'feature_file', help = 'training set')
    parser.add_option('-f','--fraction', dest = 'fraction', type = float, help = 'fraction of sampling')

    (options, args) = parser.parse_args()

    sample_training_set(options.feature_file, options.sampled_feature_file, options.fraction)