from SPARQLWrapper import SPARQLWrapper, JSON
import json



def local_to_wiki(local, json_dict, wiki_dict):

    json_dict = json_dict

    wiki_dict = wiki_dict

    url = json_dict[local]

    print url

    #return get_wiki_id_from_url(url)
    return wiki_dict[url]

def get_wiki_id_from_url(url):

    sparql = SPARQLWrapper("http://3cixty.eurecom.fr/dbpedia")

    sparql.setQuery("""select ?id where {?uri <http://dbpedia.org/ontology/wikiPageID> ?id. 
        FILTER (?uri = %s) 
       }""" %url)

    sparql.setReturnFormat(JSON)

    return int(sparql.query().convert()['results']['bindings'][0]['id']['value'])

#def get_wiki_id_from_url_local(url, wiki_dict):

 #   return wiki_dict[url]



if __name__ == '__main__':

    #open the dictionary url:local_id and define the inverse local_id:url

    json_open = open('dictionaries/dictionary_dbpedia2015.json')

    json_string = json_open.read()

    json_open.close()

    json_dict = json.loads(json_string)

    json_dict = dict((v,k) for k,v in json_dict.iteritems()) #exchange key and value

    #define the dictionary url:wiki_id

    wiki_from_url_dict = {}

    with open('datasets/page_ids_en.ttl','r') as f:

        for line in f:

            line = line.split(' ')

            if line[0] == '#':
                continue

            url = line[0] 

            wiki_id_list = line[2].split('\"')

            print wiki_id_list

            wiki_id = wiki_id_list[1]

            wiki_from_url_dict[url] = int(wiki_id)


    print wiki_from_url_dict.items()[1:20]


    edge_list_local = open('graph/page_links_en_reduced_5.edgelist','rU')

    edge_list_wiki = open('graph/page_links_en_reduced_5_wiki.edgelist','w')

    #turn the local_id edgelist into a wiki_id edgelist through the afore defined dictionaries
    # local_id -> url -> wiki_id 

    for line in edge_list_local:

        line = line.split(' ')

        if line[0] == '#': #skip comments
            continue

        local_id1 = int(line[0])
        local_id2 = int(line[1])

        #skip edges where at least one entity has no wiki id

        try:

            wiki_id1 = local_to_wiki(local_id1,json_dict,wiki_from_url_dict)

            wiki_id2 = local_to_wiki(local_id2,json_dict,wiki_from_url_dict)

        except (KeyError,IndexError):
            continue

        edge_list_wiki.write('%s,%s\n'%(wiki_id1,wiki_id2))

    edge_list_wiki.close()

    edge_list_local.close()
