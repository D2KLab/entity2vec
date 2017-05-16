import codecs
import optparse
import random

def shuffle_query_features(feature_file, shuffled_feature_file):

	with codecs.open(feature_file, 'r', encoding = 'utf-8') as features:

		with codecs.open(shuffled_feature_file, 'w', encoding='utf-8') as shuffled_features:

			query_id = 'user1'

			feature_query = []

			for line in features:

				print(line)

				line_split = line.split(' ')

				new_query_id = line_split[0]

				if new_query_id == query_id:

					feature_query.append(line)

				else: #new query, shuffle and write

					random.shuffle(feature_query)

					for i in feature_query:
						shuffled_features.write(i)

					feature_query = []

					feature_query.append(line)

				query_id = new_query_id


			for i in feature_query: #writes the last query
				shuffled_features.write(i)			



if __name__ == '__main__':

    parser = optparse.OptionParser()
    parser.add_option('-o','--output', dest = 'shuffled_feature_file', help = 'feature_file')
    parser.add_option('-i','--input', dest = 'feature_file', help = 'training set')

    (options, args) = parser.parse_args()

    shuffle_query_features(options.feature_file, options.shuffled_feature_file)