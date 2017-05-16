import codecs
from collections import defaultdict
import random
import numpy as np

#this script creates a test set from a probe set according to the user plus N

items_file = 'datasets/movielens_1m/films.txt'

probe_set_file = 'datasets/movielens_1m/ratings_dbpedia_probe_val.dat'

test_set_file = 'datasets/movielens_1m/ratings_dbpedia_userplusn_val.dat'

items = []

N = 100

with codecs.open(items_file,'r', encoding='utf-8') as items_file_read:
	
	for item in items_file_read:

		items.append(item.strip('\n'))


with codecs.open(probe_set_file,'r', encoding='utf-8') as probe_set:

	with codecs.open(test_set_file,'w', encoding='utf-8') as test_set:

		count = 1

		past_user = -1

		for line in probe_set:
			
			line = line.split(' ')

			user = line[0]

			item = line[1]

			rating = int(line[2])

			timestamp = line[3].strip('\n')

			print(user)

			if rating == 5: #only select highly relevant items

				test_set.write('%s %s %s %s\n' %(user,item,rating,timestamp))

			if past_user != user: #sample and write candidates only if changing user

				false_candidates = random.sample(items, N)

				for candidate in false_candidates:

					test_set.write('%s %s %s %s\n' %(user,candidate,3,-1))

			past_user = user

