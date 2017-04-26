from __future__ import print_function
import pandas as pd
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression, Perceptron
from sklearn import model_selection
import sklearn.metrics
import numpy as np
import optparse
import csv
from gensim.models import Word2Vec
from gensim.models.keyedvectors import KeyedVectors



def convert_labels_to_int(label,dataset):

    if dataset == 'aifb':

        if label == 'http://www.aifb.uni-karlsruhe.de/Forschungsgruppen/viewForschungsgruppeOWL/id1instance':
            return 0

        elif label == 'http://www.aifb.uni-karlsruhe.de/Forschungsgruppen/viewForschungsgruppeOWL/id2instance':
            return 1

        elif label == 'http://www.aifb.uni-karlsruhe.de/Forschungsgruppen/viewForschungsgruppeOWL/id3instance':
            return 2

        else:
            return 3

    elif dataset == 'mutag':
        #already binary values
        return int(label)

    else: #bgslith, bgstheme
        possible_labels = []

        for i in set(complete_set[y_label]):

            possible_labels.append(i)

        labels_to_int = {}

        for i in range(len(possible_labels)):

            labels_to_int[possible_labels[i]] = i

        return labels_to_int[label]


if __name__ == '__main__':

    parser = optparse.OptionParser()
    parser.add_option('-d','--dataset', dest = 'dataset', help = 'aifb or mutag or bgslith or bgstheme')
    parser.add_option('-e','--emb', dest = 'embedding', help = 'the embedding that you want to use')
    parser.add_option('-f','--dimension', dest = 'dimension', help = 'length of the embedding vector')

    (options, args) = parser.parse_args()

    if options.dataset is None:
       options.dataset = raw_input('Enter dataset name, aifb or mutag or bgslith or bgstheme:')

    if options.embedding is None:
       options.embedding = raw_input('Enter the embedding file that you want to use:')

    if options.dimension is None:
        options.dimension = 128

    dataset = options.dataset

    embedding = options.embedding

    dimension = int(options.dimension)

    complete_set  = pd.read_table('../datasets/%s/completeDataset.tsv' %dataset)

    embeddings = KeyedVectors.load_word2vec_format(embedding, binary=True)


    if dataset == 'aifb':
        y_label = 'label_affiliation'

    elif dataset == 'mutag':
        y_label = 'label_mutagenic'

    elif dataset == 'bgslith':
        y_label = 'label_lithogenesis'

    elif dataset == 'bgstheme':
        y_label = 'label_theme'
    
    elif dataset == 'am':
	    y_label = 'label_category'    

    else:
        raise NameError('Enter a valid dataset name. Choose among aifb or mutag or bgslith or bgstheme')


    complete_ids = np.array([str(i) for i in complete_set['id']])

    y_complete = np.array([convert_labels_to_int(i, dataset) for i in complete_set[y_label]])

    N_complete = len(complete_ids)

    X_complete = np.zeros((N_complete,dimension))

    for i in range(N_complete):

        emb = embeddings[complete_ids[i]]

        emb = emb.reshape((1,dimension))

        X_complete[i] =  emb

    clf_3 = KNeighborsClassifier()

    parameters_3 = {'n_neighbors' : range(1,15)}

    gs_rbf = model_selection.GridSearchCV(clf_3,param_grid=parameters_3,cv = 10, n_jobs = -1) #grid search hyper parameter optimization


    print('K-nearest neighbors score:\n')

    #print "%.3f\n" %(a_k_neigh)

    gs_rbf.fit(X_complete,y_complete)

    print("%.3f\n" % (gs_rbf.best_score_))



    clf_2 = DecisionTreeClassifier(random_state = 0)

    parameters_2 = {'min_samples_split' : np.arange(0.01,0.2,0.01)}

    gs_rbf = model_selection.GridSearchCV(clf_2,param_grid=parameters_2,cv = 10, n_jobs = -1) #grid search hyper parameter optimization


    print('Decision Tree score:\n')

    #print "%.3f\n" %(a_tree)

    gs_rbf.fit(X_complete,y_complete)

    print("%.3f\n" %(gs_rbf.best_score_))


    clf_4 = SVC(kernel = 'linear')

    parameters_4 = {'C' : [10**-3 , 10**-2 , 0.1, 1, 10, 10**2 , 10**3 ]}

    gs_rbf = model_selection.GridSearchCV(clf_4,param_grid=parameters_4,cv = 10, n_jobs = -1) #grid search hyper parameter optimization

    print('SVM lin score:\n')

    #print "%.3f\n" %(a_svm_lin)

    gs_rbf.fit(X_complete,y_complete)

    print("%.3f\n" %gs_rbf.best_score_)
