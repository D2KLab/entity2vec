c=0;
for file in `ls datasets/movielens_1m/ratings_dbpedia_train_chunks`;
	
	do

	 echo datasets/movielens_1m/ratings_dbpedia_train_chunks/$file;
	 
	 python -u lib/feature_generator.py -d movielens_1m -e num500_p1_q4_l10_d500.emd --output features/movielens_1m/global_p1_q4/train/training_chunk_$c.svm --training datasets/movielens_1m/ratings_dbpedia_train_chunks/$file &
	
	((c=c+1))
	done

