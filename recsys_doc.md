#######################
### Recommendations ###
#######################

1) Get the property-specific graphs, through a SPARQL query (select all edges with property p)

python sparql_query_get_graphs.py  -f inputs_folder -e entities_file -p property_file -o output_folder

2) Generate property-specific entity embeddings through node2vec

for property in property_file:
	./e2v_rs_experiment.sh dataset property walk_length num_walks p q d win_size iter workers

3) Generate features

python feature_generator.py -d dataset -e embedding_file -o output --training training_set --test test_set

4) Generate recommendations with RankLib

cd ranking

java -jar RankLib-2.1-patched.jar -train training_feature_file -test test_feature_file -metric2t metric -ranker rank_model -norm sum