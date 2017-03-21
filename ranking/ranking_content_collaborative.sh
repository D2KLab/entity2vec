#!/bin/bash

for metric in P@1 P@5 P@10 NDCG@10;
	do
	for model in lambda_mart ada_rank;
		do
		for feature in all collab content;
			do
				echo $model;
				file_model=models/global_p1_q1/$model"_"$feature"_"$metric.mdl;
				feature_file=$feature.txt;

				if [ $model = ada_rank ]; then
					ranker=3;
				else
					ranker=6;
				fi

				echo "java -jar RankLib-2.1-patched.jar -train ../features/movielens_1m/global_p1_q1/train/training_global_p1_q1.svm -ranker $ranker -metric2t $metric -tvs 0.9 -test ../features/movielens_1m/global_p1_q1/val/val_global_p1_q1.svm -save $file_model -feature $feature_file > results/global_p1_q1/val/$model"_"$feature"_"$metric.out"
				
				java -jar RankLib-2.1-patched.jar -train ../features/movielens_1m/global_p1_q1/train/training_global_p1_q1.svm -ranker $ranker -metric2t $metric -tvs 0.9 -test ../features/movielens_1m/global_p1_q1/val/val_global_p1_q1.svm -save $file_model -feature $feature_file > results/global_p1_q1/val/$model"_"$feature"_"$metric.out;
			done
		done
	done