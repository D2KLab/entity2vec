import numpy as np
import pandas as pd
import json
from SPARQLWrapper import SPARQLWrapper, JSON
from collections import defaultdict
from operator import itemgetter
from sklearn.metrics.pairwise import cosine_similarity  
import optparse
from ranking import ndcg_at_k, mean_average_precision 


def scorer(embeddings, gold_standard,N):

    gold_standard = pd.read_table(gold_standard, header = None)

    candidate_scores = defaultdict(list)

    for i in gold_standard.values:

        print i[2]

        query_wiki_id = i[2]

        candidate_wiki_id = i[4]

        truth_value = i[5]

        e2v_embeddings = get_e2v_embedding(embeddings)

        query_e2v = e2v_embeddings[e2v_embeddings[0] == query_wiki_id].values

        candidate_e2v = e2v_embeddings[e2v_embeddings[0] == candidate_wiki_id].values

        print query_e2v, candidate_e2v

        candidate_scores[query_wiki_id].append((similarity(query_e2v,candidate_e2v),truth_value))


    sorted_candidate_scores = sorted(candidate_scores.values(), key = itemgetter(0), reverse = True)

    relevance = []

    for score, rel in storted_candidate_scores:

        relevance.append(rel)

        
    print ndcg_at_k(relevance,N), mean_average_precision(relevance)



def similarity(vec1,vec2):
    
    #compute cosine similarity or other similarities

    v1 = np.array(vec1)

    v1 = v1.reshape(1,-1)

    v2 = np.array(vec2)

    v2 = v2.reshape(1,-1)

    return cosine_similarity(v1,v2)


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

    (options, args) = parser.parse_args()

    if options.file_name is None:
       options.file_name = raw_input('Enter file name:')

    if options.gold_standard_name is None:
        options.gold_standard_name = raw_input('Enter gold standard name:')

    if options.N is None:
        options.N = 10

    file_name = options.file_name

    gold_standard_name = options.gold_standard_name

    N = options.N

    scorer(file_name, gold_standard_name,N)

