c=0;

experiment='movielens_1m';
dataset='ratings_dbpedia_userplusn_test_chunks';
folder='datasets/'$experiment'/'$dataset'/';
data='test';
p=1;
q=4;


for file in `ls $folder`;
	
	do

	echo $folder$file;
	#echo $c;
	#echo "python -u lib/feature_generator.py -d $experiment -e num500"_"p$p"_"q$q"_"l10_d500.emd --output features/$experiment/global"_"p$p"_"q$q/$data/$data_chunk_$c.svm --training 'datasets/'$experiment'/ratings_dbpedia_train.dat'  --test $folder$file &";
	python -u lib/feature_generator.py -d $experiment -e num500"_"p$p"_"q$q"_"l10_d500.emd --output features/$experiment/global"_"p$p"_"q$q/$data/$data_chunk_$c.svm --training 'datasets/'$experiment'/ratings_dbpedia_train.dat'  --test $folder$file &
	c=$((c+1));

	done

wait

cat features/$experiment/global"_"p$p"_"q$q/$data/$data_chunk* > features/$experiment/global"_"p$p"_"q$q/$data/$data"_"global"_"p$p"_"q$q_no_shuf.svm;

python lib/shuffle_query_features.py --input features/$experiment/global"_"p$p"_"q$q/$data/$data"_"global"_"p$p"_"q$q_no_shuf.svm --output features/$experiment/global"_"p$p"_"q$q/$data/$data"_"global"_"p$p"_"q$q.svm;