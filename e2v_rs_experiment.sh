#!/bin/bash

################
## parameters ##
################

#dataset = $1

#property = $2

#walk_length = $3

#num_walks = $4

#p = $5

#q = $6

#d = $7

#win_size = $8

#iter = $9

#workers = $10

##########
## code ##
##########

#run the walks

input="datasets/$1/graphs/$2.ttl"

walksfile="$1/$2/num$4_p$5_q$6_l$3.txt.gz"

embeddingsfile="emb/$1/$2/num$4_p$5_q$6_l$3_d$7_iter$9_winsize$8.emd"

python -u src/e2v_walks.py --input "$input" --output "$walksfile" --walk-length "$3" --num-walks "$4" --p "$5" --q "$6"

#learn the embeddings

python -u src/learn_embeddings.py --input "walks/$walksfile" --output "emb/$1/$2/num$4_p$5_q$6_l$3_d$7.emd" --dimension "$7" --window-size "$8" --iter "$9" --workers "${10}"

