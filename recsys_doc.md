#######################
### Recommendations ###
#######################

**************
** TRAINING **
**************

1) Generate feedback graph, converting ratings file into implicit feedback file "user item\n". Example:

cat ratings_dbpedia_train.dat | awk -F' ' '$3 >= 4' | cut -f1,2 > feedback_graph


2) Get the property-specific graphs, through a SPARQL query (select all edges with property p)

python sparql_query_get_graphs.py  -f inputs_folder -e entities_file -p property_file -o output_folder


3) Generate property-specific entity embeddings through node2vec

for property in property_file:
	./e2v_rs_experiment.sh dataset property walk_length num_walks p q d win_size iter workers


4) Generate features

python feature_generator.py -d dataset -e embedding_file -o output --training training_set --test test_set


5) Generate recommendations with RankLib

cd ranking

java -jar RankLib-2.1-patched.jar -train training_feature_file -test test_feature_file -metric2t metric -ranker rank_model -norm sum


**********
** TEST **
**********

1) Generate recommendations

java -jar RankLib-2.1-patched.jar -load model -rank test_feature_file -norm sum -score recommendations.txt

sort recommendations.txt

2) Evaluate recommendations

java -jar RankLib-2.1-patched.jar -load model -test test_feature_file -norm sum -metric metric
