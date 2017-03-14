c=0;
#sleep 8h;
experiment='movielens_1m';
dataset='ratings_dbpedia_relplusn_val_chunks';
folder='datasets/'$experiment'/'$dataset'/';

for file in `ls $folder`;
	
	do

	echo $folder$file;
	#echo $c;
	python -u lib/feature_generator.py -d $experiment -e num500_p1_q1_l10_d500.emd --output features/$experiment/global_p1_q1/val/val_chunk_$c.svm --training 'datasets/'$experiment'/ratings_dbpedia_train.dat'  --test $folder$file &
	c=$((c+1));

	done

wait

cat features/$experiment/global_p1_q1/val/val_chunk* > features/$experiment/global_p1_q1/val/training_global_p1_q1.svm;
