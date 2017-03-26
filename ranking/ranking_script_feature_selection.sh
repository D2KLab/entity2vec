#!/bin/bash

p=1;
q=4;

rm results/global_p$p"_"q$q/test/summary_results.txt;

for metric in P@1 P@5 P@10 MAP;
	do
	#for model in lambda_mart ada_rank;
	for model in lambda_mart;
		do
		for feature in `ls feature_selection`;
			do
				echo $model;

				feature=`echo $feature | sed 's/.txt//g'`;

				echo $feature;

				file_model=models/global_p$p"_"q$q/test/$model"_"$feature"_"$metric.mdl;

				feature_file=feature_selection/$feature.txt;

				if [ $model = ada_rank ]; then
					ranker=3;
				else
					ranker=6;
				fi

				echo "java -jar RankLib-2.1-patched.jar -train ../features/movielens_1m/global_p$p"_"q$q/train/training_global_p$p"_"q$q.svm -ranker $ranker -metric2t $metric -tvs 0.9 -test ../features/movielens_1m/global_p$p"_"q$q/test/test_global_p$p"_"q$q.svm -save $file_model -feature $feature_file > results/global_p$p"_"q$q/test/$model"_"$feature"_"$metric.out;";
				
				java -jar RankLib-2.1-patched.jar -train ../features/movielens_1m/global_p$p"_"q$q/train/training_global_p$p"_"q$q.svm -ranker $ranker -metric2t $metric -tvs 0.9 -test ../features/movielens_1m/global_p$p"_"q$q/test/test_global_p$p"_"q$q.svm -save $file_model -feature $feature_file > results/global_p$p"_"q$q/test/$model"_"$feature"_"$metric.out;
			

				score=`tail results/global_p$p"_"q$q/val/$model"_"$feature"_"$metric.out | grep "on test data" | sed 's/$metric on test data: //g'`;

				model_and_score=$model"_"$feature"_"$metric" $score";

				echo $model_and_score >> results/global_p$p"_"q$q/test/summary_results.txt;

			done
		done
	done