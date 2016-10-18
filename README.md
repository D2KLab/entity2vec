# entity2vec
entity2vec computes embeddings of entities in a Knowledge Graph by using the Word2Vec model on the neighboring entities. 

1) Compute embeddings, e.g.:

python -u src/main.py --input graph/page_links_en_wikipedia_id_reduced_largeq_1_out.edgelist --output emb/dbpedia_2015_p0.3_q1_reduced_1_equal_out.emd --directed --workers 48 --p 0.3 --q 1

2) Obtain scores, e.g.:

python lib/scorer.py -i emb/dbpedia_2015_p0.3_q1_reduced_1_equal_out.emd -g datasets/relatedness-assessment.tsv -s cosine 
