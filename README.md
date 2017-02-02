# entity2vec
entity2vec computes vector representations of Knowledge Graph entities that preserve semantic similarities and are suitable for classification tasks.

0) Create empty directory called emb and one called walks

1) Compute random walks over the KG using node2vec walks

python src/e2v_walks.py --input datasets/aifb/aifb.edgelist --output aifb --p 1 --q 4

1) Learn embeddings through Word2vec, e.g.:

python src/learn_embeddings.py --input walks/walks_aifb_params.txt.gz --output emb/aifb_p1_q4.emd 

2) Obtain scores, e.g.:

cd ml

python rdf_predict.py --dataset aifb --emb ../emb/aifb_p1_q4.emd --dimension 500
