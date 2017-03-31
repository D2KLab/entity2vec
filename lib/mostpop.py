import codecs
import ranking
from collections import defaultdict
import numpy as np
from operator import itemgetter

class MostPop:

	def __init__(self,train, test):

		self.train = train
		self.test = test
		self.pop_dict = defaultdict(int) #initialize all keys to 0

	def compute_popularity(self):

		with codecs.open(self.train,'r',encoding='utf-8') as read_train:

			for line in read_train:

				line = line.split(' ')

				user = line[0]

				item = line[1]

				rel = line[2]

				if int(rel) >= 4:
				
					self.pop_dict[item] += 1


	def score_items(self):

		ranked_items = defaultdict(list)

		prec_5 = []

		prec_10 = []

		MAP = []

		with codecs.open(self.test,'r',encoding='utf-8') as read_test:

			user = 'user1'

			for line in read_test:

				line = line.split(' ')

				new_user = line[0]

				item = line[1]

				rel = int(line[2])

				if rel == 5:

					rel = 1

				else:
					
					rel = 0

				ranked_items[new_user].append((self.pop_dict[item], rel))

				if new_user != user: #compute the score for the previous query user

					sorted_rank = sorted(ranked_items[user], key = itemgetter(0), reverse = True)

					relevance = []	

					for score, rel in sorted_rank:

						relevance.append(rel)

					prec_5.append(ranking.precision_at_k(relevance,5))

					prec_10.append(ranking.precision_at_k(relevance,10))

					MAP.append(ranking.average_precision(relevance))

				user = new_user	

			#last user

			sorted_rank = sorted(ranked_items[user], key = itemgetter(0), reverse = True)

			relevance = []	

			for score, rel in sorted_rank:

				relevance.append(rel)

			prec_5.append(ranking.precision_at_k(relevance,5))

			prec_10.append(ranking.precision_at_k(relevance,10))

			MAP.append(ranking.average_precision(relevance))


		print(np.mean(prec_5),np.mean(prec_10),np.mean(MAP))


	def main(self):

		self.compute_popularity()

		self.score_items()


if __name__ == '__main__':
	
	a = MostPop('datasets/movielens_1m/ratings_dbpedia_train.dat','datasets/movielens_1m/ratings_dbpedia_userplusn_test.dat')

	a.main()