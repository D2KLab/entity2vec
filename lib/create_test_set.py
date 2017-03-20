import codecs
from collections import defaultdict
import random
import numpy as np

#this script creates a test set from a probe set according to the Rel plus N

items_file = 'datasets/movielens_1m/films.txt'

probe_set_file = 'datasets/movielens_1m/ratings_dbpedia_probe_test.dat'

test_set_file = 'datasets/movielens_1m/ratings_dbpedia_relplusn_test.dat'

items = []

N = 100

with codecs.open(items_file,'r', encoding='utf-8') as items_file_read:
	
	for item in items_file_read:

		items.append(item.strip('\n'))


with codecs.open(probe_set_file,'r', encoding='utf-8') as probe_set:

	with codecs.open(test_set_file,'w', encoding='utf-8') as test_set:

		count = 1

		for line in probe_set:
			
			line = line.split(' ')

			user = line[0]

			item = line[1]

			rating = int(line[2])

			timestamp = line[3].strip('\n')

			print(user)

			if rating == 5: #only select highly relevant items

				fake_user = 'user%d' %count #this is a trick to use feature generator later

				position = random.randint(0,100) #place the relevant item at a random position

				false_candidates = random.sample(items, N)

				for candidate in false_candidates[0:position]:

					test_set.write('%s %s %s %s\n' %(fake_user,candidate,3,-1))

				test_set.write('%s %s %s %s\n' %(fake_user,item,rating,timestamp))


				for candidate in false_candidates[position:]:

					test_set.write('%s %s %s %s\n' %(fake_user,candidate,3,-1))

				count += 1 #increment the counter at each relevant item
