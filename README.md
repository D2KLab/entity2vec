# entity2vec

Learning entity vectors from Knowledge Graphs

page_links_to_edge_list.py : converts the dbpedia links dump into an edge list of integers.

-i = input file (dbpedia dump)
-o = output file (dbpedia.edgelist)
-n = name of the dataset

python lib/page_links_to_edge_list.py -i graph/page_links_en.ttl -o graph/page_links_en.edgelist -n dbpedia2015

it serializes the dictionary that converts the id of dbpedia entities into unique integers

launch entity2vec on dbpedia data:

python src/main.py --input graph/page_links_en.edgelist --output emb/dbpedia_2015.emd
