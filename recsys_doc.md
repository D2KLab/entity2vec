#######################
### Recommendations ###
#######################

**************
** TRAINING **
**************

1) Generate feedback graph, converting ratings file into implicit feedback file "user item\n". Example:

$cat ratings_dbpedia_train.dat | awk -F' ' '$3 >= 4' | cut -f1,2 > feedback_graph

You can now either provide a set of property-specific graphs or a SPARQL endpoint (--sparql endpoint) from which these graphs will be downloaded as data sources. 
[OPTIONAL]: in config/config.properties, enter the name of your dataset as key and a set of properties for which you want to compute the embeddings. 
If not done, by default, it will use all the graphs stored in datasets/your_dataset/graphs or it will get all the possible properties from the SPARQL endpoint.

2) Generate property-specific entity embeddings through entity2vec

$python entity2vec.py

--dataset: mandatory, name of the dataset (defaultmovielens_1m, will be used to create folders, retrieve properties from config file)

--config_file: mandatory, by default config/config.properties.

--entities: optional, a list of entities for which the embeddings have to be computed. By default, it will use them all.


4) Generate features

$python feature_generator.py -d dataset -e embedding_file -o output --training training_set --test test_set


5) Generate recommendations with RankLib

$cd ranking

$java -jar RankLib-2.1-patched.jar -train training_feature_file -test test_feature_file -metric2t metric -ranker rank_model -norm sum


**********
** TEST **
**********

1) Generate recommendations

java -jar RankLib-2.1-patched.jar -load model -rank test_feature_file -score recommendations.txt

sort recommendations.txt

2) Evaluate recommendations

java -jar RankLib-2.1-patched.jar -load model -test test_feature_file -metric metric
