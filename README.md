# entity2vec
entity2vec computes vector representations of Knowledge Graph entities that preserve semantic similarities and are suitable for classification tasks. It generates a set of property-specific entity embeddings by running node2vec on property specific subgraphs, i.e. K(p) = (s,p,o) where p is a given property. The repository includes:

- A reimplementation of node2vec as an iterator, which reduces the memory overhead. It also introduces the possibility of avoiding the preprocessing of the transition probabilities, which has the effect of reducing memory effort, but slowing down the computation

- The implementation of entity2vec, which generates a set of entity embeddings from Knowledge Graphs corresponding to different properties. Entity2vec can work with a set of pre-dowloaded dumps or download them from a SPARQL endpoint. 

## Requirements

- Python 2.7 or above
- numpy
- gensim
- networkx
- pandas
- SPARQL Wrapper

## Property-specific entity embeddings

The set of properties can be defined in the configuration file config/properties.json, otherwise the software will run on each file that is located in datasets/your_dataset/graphs or if a SPARQL endpoint is provided, it will download all the graphs for all properties in datasets/your_dataset/graphs.

```
  python src/entity2vec.py --dataset dataset --config_file config_file --entities entities --sparql sparql --default_graph default_graph
```
dataset: mandatory, name of the dataset (defaultmovielens_1m, will be used to create folders, retrieve properties from config file)

config_file: mandatory, by default config/config.properties.

entities: optional, a list of entities for which the embeddings have to be computed. By default, it will use them all.

sparql: optional, endpoint from which property-specific graphs are obtained. If not provided, it assumes that the graphs are already stored in datasets/your_dataset/graphs

default_graph: optional, whether using a default_graph in the SPARQL endpoint

## Entity Recommendation

Compute user and item embeddings from a Knowledge Graph encompassing both user feedback information (movielens_1m/graphs/feedback.edgelist) and Linked Open Data information (movielens_1m/graphs/dbpedia_property.edgelist) on the Movielens 1M dataset. It is based on property-specific entity embeddings, which can be already computed or can be computed by calling entity2vec using the command line argument --run_all. It adopts by default the AllItems candidate generation for testing, which means that features are computed for each user-item pair that is not appearing in the training set. Thus, for each user, all items in the database can be ranked to obtain top-N item recommandation.

```
python src/entity2rec.py --dataset my_dataset --train training_set.dat --test test_set.dat 
```

where it is assumed that the training and test set have the format:

```
user_id item_id rating timestamp

```
if the argument --run_all is provided, entity2vec will be called and generate property specific embeddings and all its command line arguments can be used. Otherwise, the embeddings will be loaded from the emb/ folder.

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
