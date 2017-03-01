import codecs
from collections import defaultdict
import random


user_films = defaultdict(list)

with codecs.open('movielens_1m/ratings_dbpedia.dat','r', encoding = 'utf-8') as f:
	for line in f:

		line = line.split('::')
		user = line[0]

		user_films[user].append((line[1],line[2],line[3]))

with codecs.open('movielens_1m/ratings_dbpedia_train.dat','w', encoding = 'utf-8') as train:
	with codecs.open('movielens_1m/ratings_dbpedia_test.dat','w', encoding = 'utf-8') as test:

		for user in sorted(user_films.keys()):

			values = user_films[user]

			random.shuffle(values)

			test_values = values[0:10]

			print test_values

			for film, rating, timestamp in test_values:

				test.write('%s::%s::%s::%s' %(user,film, rating, timestamp))

			train_values = values[11:-1]

			for film, rating, timestamp in train_values:

				train.write('%s::%s::%s::%s' %(user,film, rating, timestamp))







