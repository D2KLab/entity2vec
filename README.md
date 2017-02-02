# entity2vec
entity2vec computes vector representations of Knowledge Graph entities that preserve semantic similarities and are suitable for classification tasks.

0) Create empty directory called emb

1) Compute embeddings, e.g.:

python src/main.py --input datasets/aifb/aifb.edgelist --output emb/aifb_p1_q4.emd --p 1 --q 4

2) Obtain scores, e.g.:

cd ml

python rdf_predict.py --dataset aifb --emb ../emb/aifb_p1_q4.emd --dimension 500
