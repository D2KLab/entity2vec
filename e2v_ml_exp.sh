#!/bin/bash

for p in 1 4;
do
    for q in 1 4;
        do
            if [ $p -eq 4 ] && [ $q -eq 4 ] ; then
            echo $p, $q;
            else
            echo $p, $q;

            input='datasets/bgstheme/bgstheme.edgelist';

            echo $input;

            prova1=`python src/main.py --input $input --output emb/bgstheme/200_skip/bgstheme\_p$p\_q$q\_skip.emd --p $p --q $q --workers 48`;
            echo $prova1;

            prova2=`python src/main.py --input $input --output emb/bgstheme/500_skip/bgstheme\_p$p\_q$q\_skip.emd --p $p --q $q --workers 48 --dimension 500`;
            echo $prova2;

            prova3=`python src/main_cbow.py --input $input --output emb/bgstheme/200_cbow/bgstheme\_p$p\_q$q\_cbow.emd --p $p --q $q --workers 48`;
            echo $prova3;

            prova4=`python src/main_cbow.py --input $input --output emb/bgstheme/500_cbow/bgstheme\_p$p\_q$q\_cbow.emd --p $p --q $q --workers 48 --dimension 500`;
            echo $prova4;            

            fi
        done
done


