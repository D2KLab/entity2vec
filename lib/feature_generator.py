from scorer import get_e2v_embeddings
from scorer import similarity_function
import optparse
import sys
import codecs
import collection

def get_e2v_embedding_vector(embedding_file,ID):

	a = get_e2v_embedding(embeddings+'/'+prop)

	vec = a[a[0] == ID]

	del a

	try:
	
		return vec[0][1:]

	except IndexError:

		return []


def get_items_rated_by_user(training, user):

	with codecs.open(training,'r', encoding='utf-8') as train:

		items_rated_by_user = collection.defaultdict(list)

		for line in train:

				line = line.split('::')

				u = line[0]

				item = line[1]

				items_rated_by_user[u].append(item)


		return items_rated_by_user[user]



def feature_generator(embeddings, training, feature_file):

feature_property = {}

	with codecs.open(feature_file,'w', encoding='utf-8') as file_write:

		with codecs.open(training,'r', encoding='utf-8') as train:

			for line in train:

				line = line.split('::')

				user = line[0]

				item = line[1]

				########################
				## collaborative term ##
				########################

				prop = 'feedback'

				user_vec = get_e2v_embedding_vector(os.listdir(embeddings+'/'+prop)[0], user)

				item_vec = get_e2v_embedding_vector(os.listdir(embeddings+'/'+prop)[0], item)

				feature_property[prop] = similarity_function(user_vec,item_vec,cosine)

        		########################
        		## content-based term ##
        		########################

				items_rated_by_user = get_items_rated_by_user(training, user)

				num_of_items_rated = len(items_rated_by_user)

				for prop in os.listdir(embeddings): #for each property

					for past_item in items_rated_by_user:

						past_item_vec = get_e2v_embedding_vector(os.listdir(embeddings+'/'+prop)[0], item)



        				feature_property[prop] = 


						













































if __name__ == '__main__':

    parser = optparse.OptionParser()
    parser.add_option('-e','--embeddings', dest = 'embeddings_folder', help = 'embeddings_folder')
    parser.add_option('-o','--output', dest = 'feature_file', help = 'feature_file')
    parser.add_option('-t','--training', dest = 'training_set', help = 'cutting threshold scorers')


    (options, args) = parser.parse_args()

    feature_generator(options.embeddings_folder,options.feature_file,options.training_set)