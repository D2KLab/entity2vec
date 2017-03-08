for prop in `cat datasets/movielens_1m/useful_properties.txt`;
do
	echo $prop;
	./e2v_rs_experiment.sh movielens_1m $prop 10 500 4 1 500 10 5 48;
done