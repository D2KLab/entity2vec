# entity2vec
entity2vec computes vector representations of Knowledge Graph entities that preserve semantic similarities and are suitable for classification tasks. It generates a set of property-specific entity embeddings by running node2vec on property specific subgraphs, i.e. K(p) = (s,p,o) where p is a given property.

# ##






# Entity classification

0) Create empty directory called emb

1) Run node2vec on the whole graph to create a single global embedding of the entity

python src/node2vec.py --input datasets/aifb/aifb.edgelist --output emb/aifb_p1_q4.emd  --p 1 --q 4

2) Obtain scores, e.g.:

cd ml

python rdf_predict.py --dataset aifb --emb ../emb/aifb_p1_q4.emd --dimension 500
