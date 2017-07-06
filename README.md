# entity2vec
entity2vec computes vector representations of Knowledge Graph entities that preserve semantic similarities and are suitable for classification tasks. It generates a set of property-specific entity embeddings by running node2vec on property specific subgraphs, i.e. K(p) = (s,p,o) where p is a given property. The repository includes:

- A reimplementation of _node2vec_, which introduces the possibility of avoiding the preprocessing of the transition probabilities, which has the effect of reducing memory effort, but slowing down the computation

- **_entity2vec_**, which generates a set of entity embeddings from Knowledge Graphs corresponding to different properties. Entity2vec can work with a set of pre-downloaded dumps or download them from a SPARQL endpoint.

- **_entity2rec_**, which generates a set of recommended entities combining property-specific similarity scores obtained using entity2vec embeddings.

## Requirements

- Python 2.7 or above
- numpy
- gensim
- networkx
- pandas
- SPARQL Wrapper

If you are using `pip`:


        pip install gensim networkx pandas SPARQLWrapper

## Property-specific entity embeddings

The set of properties can be defined in the configuration file `config/properties.json`, otherwise the software will run on each file that is located in `datasets/your_dataset/graphs` or if a SPARQL endpoint is provided, it will download all the graphs for all properties in `datasets/your_dataset/graphs`.


        python src/entity2vec.py --dataset dataset --config_file config_file --entities entities --sparql sparql --default_graph default_graph

|option          | default                |description|
|----------------|------------------------|-----------|
|`dataset`       | null **(Required)**    | name of the dataset. It will be used to create folders and retrieve properties from config file|
|`config_file`   | config/properties.json | path of the configuration file
|`entities`      | all                    | a list of entities for which the embeddings have to be computed. By default, it will use them all.|
|`sparql`        | null                   | endpoint from which property-specific graphs are obtained. If not provided, it assumes that the graphs are already stored in `datasets/your_dataset/graphs` |
|`default_graph` | null                   | whether using a default_graph in the SPARQL endpoint |
|`num_walks`     | 500                    | number of random walks per entity |
|`feedback_file` | null                   | Path to a DAT file that contains all the couples user-item. If not defined, it assumes that is the file `datasets/<my_dataset>/graphs/feedback.edgelist` |


## Entity classification

Generate unique vector representation for an entity, without considering the role of semantic properties, to use in classification tasks.

0. Create empty directory called emb

1. Run node2vec on the whole graph to create a single global embedding of the entity

        python src/node2vec.py --input datasets/aifb/aifb.edgelist --output emb/aifb_p1_q4.emd  --p 1 --q 4

2. Obtain scores, e.g.:

        cd ml

        python rdf_predict.py --dataset aifb --emb ../emb/aifb_p1_q4.emd --dimension 500
