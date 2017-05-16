from sklearn.decomposition import NMF
import numpy as np
from collections import defaultdict
import codecs
from operator import itemgetter
import ranking
from surprise import NMF
from surprise import Reader
from surprise import Dataset 
import os

class Matrix_Factorization:


	def __init__(self, train, test):

		self.train = train

		self.test = test

		self.item_to_ind = {}

		self.user_to_ind = {}


	def read_data(self, explicit = False):

		item_ind = 0

		user_ind = 0

		if explicit == False:
			self.X = np.zeros((6040,3201))

		else:
			self.X = np.ones((6040,3201))*3.574 #avg rating

		with codecs.open(self.train,'r',encoding='utf-8') as read_train:


			for line in read_train:

				line = line.split(' ')


				user = line[0]

				if user not in self.user_to_ind.keys(): #new user

					self.user_to_ind[user] = user_ind

					user_ind += 1


				item = line[1]

				if item not in self.item_to_ind.keys(): #new item

					self.item_to_ind[item] = item_ind

					item_ind += 1


				rel = line[2]

				if explicit == False:
					if int(rel) >= 4:
				
						self.X[user_ind -1, item_ind -1] = 1

				else:

					self.X[user_ind -1, item_ind -1] = int(rel)


	def learn_model_surprise(self):

		file_path = os.path.expanduser(self.train)

		reader = Reader(line_format='user item rating timestamp', sep=' ')

		data = Dataset.load_from_file(file_path, reader=reader)

		data.split(n_folds=5)

		algo = NMF(n_factors = 20)

		trainset = data.build_full_trainset()

		algo.train(trainset)

		self.user_vectors = algo.pu
		self.item_vectors = algo.qi



	def learn_model(self):

		model = NMF(n_components=50, solver = 'cd', alpha = 0.015, max_iter = 500)

		self.user_vectors = model.fit(self.X).transform(self.X)

		self.item_vectors = model.fit(self.X).components_.T



	def compute_avg_score(self,user): #when there is a new item in the collection

		user_ind = self.user_to_ind[user]

		user_vec = self.user_vectors[user_ind]

		avg_score = 0

		for i in range(3201):

			item_vec = self.item_vectors[i]

			avg_score += np.dot(user_vec, item_vec)

		avg_score = avg_score/3201

		return avg_score


	def compute_score(self, user, item):


		try:

			user_ind = self.user_to_ind[user]

			user_vec = self.user_vectors[user_ind]

		except KeyError:

			user_vec = self.zeros(20)

		try:

			item_ind = self.item_to_ind[item]

			item_vec = self.item_vectors[item_ind]

		except KeyError:

			return self.compute_avg_score(user)

		return np.dot(user_vec, item_vec)


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

				ranked_items[new_user].append((self.compute_score(user,item), rel))

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

		print(prec_5)
		print(prec_10)
		print(MAP)

		print(np.mean(prec_5),np.mean(prec_10),np.mean(MAP))		


	def main(self):

		#self.read_data(explicit=True)

		#self.learn_model()

		self.read_data(explicit=True)

		self.learn_model_surprise()

		self.score_items()



if __name__ == '__main__':

	#a = Matrix_Factorization('datasets/movielens_1m/ratings_dbpedia_train_shuf.dat','datasets/movielens_1m/ratings_dbpedia_test_shuf.dat')

	a = Matrix_Factorization('datasets/movielens_1m/ratings_dbpedia_train.dat','datasets/movielens_1m/ratings_dbpedia_userplusn_test.dat')
	a.main()

