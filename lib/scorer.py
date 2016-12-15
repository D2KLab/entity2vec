import numpy as np
import pandas as pd
import json
#from SPARQLWrapper import SPARQLWrapper, JSON
from collections import defaultdict
from operator import itemgetter
from sklearn.metrics.pairwise import cosine_similarity, linear_kernel
import optparse
from ranking import ndcg_at_k, average_precision 
import time

def scorer(embeddings, gold_standard,N, similarity):

    similarity = similarity
    gold_standard = pd.read_table(gold_standard, header = None)

    candidate_scores = defaultdict(list)

    sorted_candidate_scores = defaultdict(list)

    e2v_embeddings = get_e2v_embedding(embeddings)

    ndcg = {}

    AP = {}

    queries_id_list = []

    doc_id_list = []

    c = 0

    for i in gold_standard.values:

    	doc_id = int(i[0])

        query_wiki_id = int(i[2])

        e2v_embeddings = get_e2v_embedding(embeddings)

        query_e2v = e2v_embeddings[e2v_embeddings[0] == query_wiki_id].values

    	queries_id_list.append(query_wiki_id) #to check when the query entity is changing

    	doc_id_list.append(doc_id) #check when the document is changing

        candidate_wiki_id = int(i[4])

        truth_value = int(i[5])

        print query_wiki_id, candidate_wiki_id, truth_value

        query_e2v = e2v_embeddings[e2v_embeddings[0] == query_wiki_id].values #query vector = [0.2,-0.3,0.1,0.7 ...]

        candidate_e2v = e2v_embeddings[e2v_embeddings[0] == candidate_wiki_id].values

        print query_e2v, candidate_e2v

        candidate_scores[(doc_id,query_wiki_id)].append((similarity_function(query_e2v,candidate_e2v, similarity),truth_value))


        if c == 0:

        	pass

        else:

	    	if queries_id_list[c - 1] != queries_id_list[c] or doc_id_list[c - 1] != doc_id_list[c]: #new query entity or new document, we can sort them and score

		        sorted_candidate_scores[(doc_id,query_wiki_id)] = sorted(candidate_scores[(doc_id,query_wiki_id)], key = itemgetter(0), reverse = True)

		        relevance = []

		        for score, rel in sorted_candidate_scores[(doc_id,query_wiki_id)]:

		            relevance.append(rel)
		        
		        ndcg[(doc_id,query_wiki_id)] = ndcg_at_k(relevance,N)

		        AP[(doc_id,query_wiki_id)] = average_precision(relevance)

		        #print sorted_candidate_scores

  		c += 1

  	print sorted_candidate_scores[(doc_id,query_wiki_id)] #see an example
	
    print np.mean(ndcg.values()), np.mean(AP.values())


def similarity_function(vec1,vec2, similarity):
    
    #compute cosine similarity or other similarities

    v1 = np.array(vec1)

    v2 = np.array(vec2)

    if len(v1)*len(v2) == 0: #any of the two is 0
        global count
        count +=1

        return 0

    else:

        if similarity == 'cosine':

            return cosine_similarity(v1,v2)[0][0] #returns an double array [[sim]]

        elif similarity == 'L1':
            return  0

        elif similarity == 'L2':
            return 0

        elif similarity == 'linear_kernel':
            return linear_kernel(v1,v2)[0][0]

        else:
            raise NameError('Choose a valid similarity function')

def get_e2v_embedding(embeddings):

    #read the embedding file into a dictionary

    emb = pd.read_table(embeddings, skiprows = 1, header = None, sep = ' ')

    return emb


def wiki_to_local(wiki_id):

    url = get_url_from_id(wiki_id)

    url = '<'+url+'>'

    json_open = open('dictionaries/dictionary_dbpedia2015.json')

    json_string = json_open.read()

    json_open.close()

    json_dict = json.loads(json_string)

    local_id = json_dict[url]

    return local_id



def get_url_from_id(wiki_id):

    sparql = SPARQLWrapper("http://dbpedia.org/sparql")

    sparql.setQuery("""
    PREFIX db: <http://dbpedia.org/resource/>
    SELECT *
    WHERE { ?s dbo:wikiPageID %d }
    """ %wiki_id)

    sparql.setReturnFormat(JSON)

    return str(sparql.query().convert()['results']['bindings'][0]['s']['value'])



if __name__ == '__main__':

    parser = optparse.OptionParser()
    parser.add_option('-i','--input', dest = 'file_name', help = 'file_name')
    parser.add_option('-g','--gold', dest = 'gold_standard_name', help = 'gold_standard_name')
    parser.add_option('-N','--number', dest = 'N', help = 'cutting threshold scorers',type = int)
    parser.add_option('-s','--similarity', dest = 'similarity', help = 'similarity measure')

    (options, args) = parser.parse_args()

    if options.file_name is None:
       options.file_name = raw_input('Enter file name:')

    if options.gold_standard_name is None:
        options.gold_standard_name = raw_input('Enter gold standard name:')

    if options.N is None:
        options.N = 10

    if options.similarity is None:
        options.similarity = 'cosine'

    file_name = options.file_name

    gold_standard_name = options.gold_standard_name

    N = options.N

    similarity = options.similarity

    count = 0

    start_time = time.time()

    scorer(file_name, gold_standard_name,N, similarity)

    print 'number of entities not found is %d' %count

    print 'elapsed time is:\n'

    print("--- %s seconds ---" % (time.time() - start_time))
