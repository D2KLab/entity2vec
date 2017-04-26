# entity2vec
entity2vec computes vector representations of Knowledge Graph entities that preserve semantic similarities and are suitable for classification tasks. It generates a set of property-specific entity embeddings by running node2vec on property specific subgraphs, i.e. K(p) = (s,p,o) where p is a given property.

## Requirements

- Python 2.7 or above
- numpy
- gensim
- networkx
- pandas
- SPARQL Wrapper

## Property-specific entity embeddings

Compute user and item embeddings from a Knowledge Graph encompassing both user feedback information (movielens_1m/graphs/feedback.edgelist) and Linked Open Data information (movielens_1m/graphs/dbpedia_property.edgelist) on the Movielens 1M dataset. The set of properties can be defined in the configuration file config/properties.json, otherwise the software will run on each file that is located in datasets/your_dataset/graphs. Using the argument --sparql it is also possible to query a sparql endpoint to download the graphs in datasets/your_dataset/graphs.

```
  python src/entity2vec.py
```

## Entity classification

Generate unique vector representation for an entity, without considering the role of semantic properties, to use in classification tasks.

0) Create empty directory called emb

1) Run node2vec on the whole graph to create a single global embedding of the entity
```
  python src/node2vec.py --input datasets/aifb/aifb.edgelist --output emb/aifb_p1_q4.emd  --p 1 --q 4
```
2) Obtain scores, e.g.:
```
  cd ml

  python rdf_predict.py --dataset aifb --emb ../emb/aifb_p1_q4.emd --dimension 500
```
