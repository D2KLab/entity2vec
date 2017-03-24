#!/bin/bash

p=4;
q=1;

for metric in P@1 P@5 P@10 MAP;
	do
	for model in lambda_mart ada_rank;
		do
		for feature in `ls feature_selection`;
			do
				echo $model;

				feature=`echo $feature | sed 's/.txt//g'`;

				echo $feature;

				file_model=models/global_p$p"_"q$q/$model"_"$feature"_"$metric.mdl;
				feature_file=feature_selection/$feature.txt;
				if [ $model = ada_rank ]; then
					ranker=3;
				else
					ranker=6;
				fi

				echo "java -jar RankLib-2.1-patched.jar -train ../features/movielens_1m/global_p$p"_"q$q/train/training_global_p$p"_"q$q.svm -ranker $ranker -metric2t $metric -tvs 0.9 -test ../features/movielens_1m/global_p$p"_"q$q/val/val_global_p$p"_"q$q.svm -save $file_model -feature $feature_file > results/global_p$p"_"q$q/val/$model"_"$feature"_"$metric.out";
				
				java -jar RankLib-2.1-patched.jar -train ../features/movielens_1m/global_p$p"_"q$q/train/training_global_p$p"_"q$q.svm -ranker $ranker -metric2t $metric -tvs 0.9 -test ../features/movielens_1m/global_p$p"_"q$q/val/val_global_p$p"_"q$q.svm -save $file_model -feature $feature_file > results/global_p$p"_"q$q/val/$model"_"$feature"_"$metric.out;
			

				score=`tail results/global_p$p"_"q$q/val/$model"_"$feature"_"$metric.out | grep "on test data" | sed 's/$metric on test data: //g'`;

				model_and_score=$model"_"$feature"_"$metric" $score";

				rm results/global_p$p"_"q$q/val/summary_results.txt;

				echo $model_and_score >> results/global_p$p"_"q$q/val/summary_results.txt;

			done
		done
	done