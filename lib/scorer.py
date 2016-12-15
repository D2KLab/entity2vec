import numpy as np
import pandas as pd
import json
from collections import defaultdict
from operator import itemgetter, mod
from sklearn.metrics.pairwise import cosine_similarity, linear_kernel
import optparse
from ranking import ndcg_at_k, average_precision 
import time
import sys
from scipy.stats import spearmanr
from SPARQLWrapper import SPARQLWrapper, JSON
from random import shuffle

def scorer(embeddings, gold_standard,N, similarity):

    similarity = similarity
    gold_standard = pd.read_table(gold_standard, delimiter = ' ',header = None)

    candidate_scores = defaultdict(list)

    sorted_candidate_scores = defaultdict(list)

    e2v_embeddings = get_e2v_embedding(embeddings)

    ndcg = {}

    AP = {}

    queries_id_list = []

    doc_id_list = []

    similarities = []

    c = 0

    l = len(gold_standard.values)

    missing_query_entities = []

    missing_candidate_entities = []

    for i in gold_standard.values:

    	doc_id = int(i[0])

        query_id = int(i[1])

    	queries_id_list.append(query_id) #to check when the query entity is changing

    	doc_id_list.append(doc_id) #check when the document is changing

        candidate_id = int(i[2])

        truth_value = int(i[3])

        print doc_id,query_id, candidate_id, truth_value

        query_e2v = e2v_embeddings[e2v_embeddings[0] == query_id].values#query vector = [0.2,-0.3,0.1,0.7 ...]

        query_e2v = query_e2v[1:]

        candidate_e2v = e2v_embeddings[e2v_embeddings[0] == candidate_id].values

        candidate_e2v = candidate_e2v[1:]

        if len(query_e2v) == 0:
        	
        	missing_query_entities.append(query_id)
        	

        if len(candidate_e2v) == 0:

        	missing_candidate_entities.append(candidate_id)

        #print query_e2v, candidate_e2v

        candidate_scores[(doc_id,query_id)].append((similarity_function(query_e2v,candidate_e2v, similarity),truth_value))


        if queries_id_list[c - 1] != queries_id_list[c] or doc_id_list[c - 1] != doc_id_list[c]: #new query entity or new document, we can sort them and score

			#get the doc_id and wiki_id of the previous iteration

            prev_doc_id = doc_id_list[c - 1]

            prev_query_id = queries_id_list[c - 1]

            sorted_candidate_scores[(prev_doc_id,prev_query_id)] = sorted(candidate_scores[(prev_doc_id,prev_query_id)], key = itemgetter(0), reverse = True)

            relevance = []	

            for score, rel in sorted_candidate_scores[(prev_doc_id,prev_query_id)]:
                relevance.append(rel)

           #print relevance
		        
            ndcg[(prev_doc_id,prev_query_id)] = ndcg_at_k(relevance,N)

            AP[(prev_doc_id,prev_query_id)] = average_precision(relevance)

            #print AP[(prev_doc_id,prev_query_id)]


        c = c + 1

        if c == l: #end of the file, needs to add to the dictionary the current element, which is the last query

			sorted_candidate_scores[(doc_id,query_id)] = sorted(candidate_scores[(doc_id,query_id)], key = itemgetter(0), reverse = True)

			relevance = []	

			for score, rel in sorted_candidate_scores[(doc_id,query_id)]:
				relevance.append(rel)

			ndcg[(doc_id,query_id)] = ndcg_at_k(relevance,N)

			AP[(doc_id,query_id)] = average_precision(relevance)

			print AP[(doc_id,query_id)]

    print sorted_candidate_scores[(doc_id,query_id)] #see an example
	
    print np.mean(ndcg.values()), np.mean(AP.values())

    print set(missing_query_entities), set(missing_candidate_entities)


def scorer_kore(embeddings, gold_standard,N, similarity):

    similarity = similarity

    candidate_scores = defaultdict(list)

    e2v_embeddings = get_e2v_embedding(embeddings)

    gold_standard_dict = defaultdict(list)

    ndcg = {}

    AP = {}

    missing_query_entities = []

    missing_candidate_entities = []

    scores = []

    #read the gold the standard and save it as a dictionary

    gs = open(gold_standard)

    lines = gs.readlines()

    gs.close()

    c = 0

    #define the gold standard dict

    for line in lines:

        label = line.strip(' ').replace(' ','_').replace('\n','').replace('\t','') #clean the string


        if mod(c,21) == 0:

            key = label
            gold_standard_dict[key] = []

        else: 

            gold_standard_dict[key].append(label)

        c += 1


    #define the predicted ranking and scores

    c = 0

    dots = []

    for line in lines:

        label = line.strip(' ').replace(' ','_').replace('\n','').replace('\t','') #clean the string

        if c == len(lines) - 1: #reached the end of file

            print 'end of file'

            candidate_id = get_id_from_label(str(label))

            candidate_e2v = e2v_embeddings[e2v_embeddings[0] == candidate_id].values #query vector = [0.2,-0.3,0.1,0.7 ...]

            candidate_e2v = candidate_e2v[1:]

            if len(candidate_e2v) == 0:
                missing_candidate_entities.append(label)

            candidates = candidate_scores[query_id] 

            shuffle(candidates)

            candidate_scores[query_id] = candidates

            candidate_scores[query_id].append((similarity_function(query_e2v,candidate_e2v, similarity),label)) #pair (score, candidate_name)

            ranking_tuples = sorted(candidate_scores[query_id], key = itemgetter(0), reverse = True)

            ranking = [j for i,j in ranking_tuples]

            gs_ranking = gold_standard_dict[key]    

            print ranking

            scores.append(spearmanr(ranking,gs_ranking)[0])


        if mod(c,21) == 0: #every twenty lines changing the key, new query entity

            if c != 0:

                candidates = candidate_scores[query_id] 

                shuffle(candidates)

                candidate_scores[query_id] = candidates

                #sort them according to the score

                ranking_tuples = sorted(candidate_scores[query_id], key = itemgetter(0), reverse = True)

                ranking = [j for i,j in ranking_tuples]

                gs_ranking = gold_standard_dict[key]

                scores.append(spearmanr(ranking,gs_ranking)[0])

            key = label

            query_id = get_id_from_label(str(label)) 

            query_e2v = e2v_embeddings[e2v_embeddings[0] == query_id].values #query vector = [0.2,-0.3,0.1,0.7 ...]

            query_e2v = query_e2v[1:]

            if len(query_e2v) == 0:
                missing_query_entities.append(label)

        else: #candidate entity
            if len(query_e2v) == 0:
                missing_query_entities.append(label)

        else:


            candidate_id = get_id_from_label(str(label))

            candidate_e2v = e2v_embeddings[e2v_embeddings[0] == candidate_id].values #query vector = [0.2,-0.3,0.1,0.7 ...]

            candidate_e2v = candidate_e2v[1:]

            if len(candidate_e2v) == 0:
                missing_candidate_entities.append(label)

            print query_id

            if len(candidate_e2v) == 0:
                missing_candidate_entities.append(label)

            candidate_scores[query_id].append((similarity_function(query_e2v,candidate_e2v, similarity),label)) #pair (score, candidate_name)

        c += 1

    print missing_query_entities
    print missing_candidate_entities

    print candidate_scores
  
    it_companies = np.mean(scores[0:5])

    celebrities = np.mean(scores[5:10])

    video_games = np.mean(scores[10:15])

    tv_series = np.mean(scores[15:20])

    chuck_norris = scores[20]

    print 'it_companies: %f\n' %it_companies

    print 'celebrities: %f\n' %celebrities

    print 'video_games: %f\n' %video_games

    print 'tv_series: %f\n' %tv_series

    print 'chuck_norris: %f\n' %chuck_norris



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

        elif similarity == 'softmax':

            return np.exp(np.dot(v1[0],v2[0]) - 10**9   ) #normalization is useless for relative comparisons

        elif similarity == 'linear_kernel':
            return linear_kernel(v1,v2)[0][0]

        elif similarity == 'euclidean':
            return euclidean_distances(v1,v2)[0][0]
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


def get_id_from_label(label):

    #print label

    label = label.decode('utf8')

    sparql = SPARQLWrapper("http://dbpedia.org/sparql")

    url = '<http://dbpedia.org/resource/'+label+'>'

    sparql.setQuery("""
     SELECT ?uri ?id  WHERE {
     ?uri <http://dbpedia.org/ontology/wikiPageID> ?id.
     FILTER (?uri = %s) }""" %url)

    sparql.setReturnFormat(JSON)

    return int(sparql.query().convert()['results']['bindings'][0]['id']['value'])

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
    parser.add_option('-k','--kore', dest = 'kore', action = "store_true", default = False, help = 'kore dataset')

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

    kore = options.kore

    count = 0

    start_time = time.time()


    if kore == True:

        scorer_kore(file_name, gold_standard_name,N, similarity)

    else:

        scorer(file_name, gold_standard_name,N, similarity)

    print 'number of entities not found is %d' %count

    print 'elapsed time is:\n'

    print("--- %s seconds ---" % (time.time() - start_time))
