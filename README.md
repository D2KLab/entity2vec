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
|`feedback_file` | null                   | Path to a DAT file that contains all the couples user-item. If not defined, it assumes that is the file `datasets\<my_dataset>\graphs\feedback.edgelist` |

## Entity Recommendation

Compute user and item embeddings from a Knowledge Graph encompassing both user feedback information (`movielens_1m/graphs/feedback.edgelist`) and Linked Open Data information (`movielens_1m/graphs/dbpedia_property.edgelist`) on the Movielens 1M dataset. It is based on property-specific entity embeddings, which can be already computed or can be computed by calling _entity2rec_ using the command line argument `--run_all`. It adopts by default the _AllItems_ candidate generation for testing, which means that features are computed for each user-item pair that is not appearing in the training set. Thus, for each user, all items in the database can be ranked to obtain top-N item recommendation.

    python src/entity2rec.py --dataset my_dataset --train training_set.dat --test test_set.dat

The command accepts all the params of _entity2vec_ and, in addition:

|option          | default                |description |
|----------------|------------------------|------------|
|`train`         | null **(Required)**    | Path of the train set in DAT format (see below for syntax) |
|`test`          | null **(Required)**    | Path of the test set in DAT format (see below for syntax)  |
|`run_all`       | False                  | Whether running entity2vec to compute the embeddings       |


The training and test set have the format:

    user_id item_id rating timestamp

where the `user_id` should be an integer, possibly preceded by the string `user` (i.e. `13` or `user13`).

If the argument `--run_all` is provided, _entity2vec_ will be called and generate property specific embeddings and all its command line arguments can be used. Otherwise, the embeddings will be loaded from the `emb/` folder.

## Entity classification

Generate unique vector representation for an entity, without considering the role of semantic properties, to use in classification tasks.

0. Create empty directory called emb

1. Run node2vec on the whole graph to create a single global embedding of the entity

        python src/node2vec.py --input datasets/aifb/aifb.edgelist --output emb/aifb_p1_q4.emd  --p 1 --q 4

2. Obtain scores, e.g.:

        cd ml

        python rdf_predict.py --dataset aifb --emb ../emb/aifb_p1_q4.emd --dimension 500
