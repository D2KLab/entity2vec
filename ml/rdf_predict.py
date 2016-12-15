import pandas as pd
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression, Perceptron
from sklearn import cross_validation
from sklearn import grid_search
import sklearn.metrics
import numpy as np
import optparse
import csv

def get_embeddings(ID, embeddings):

    try:

        embds = embeddings[embeddings[0] == ID].values[0]

    except IndexError:
        print ID

    return embds[1:] #the first is the id

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

    #training_set = pd.read_table('../datasets/%s/trainingSet.tsv' %dataset)

    #test_set = pd.read_table('../datasets/%s/testSet.tsv' %dataset)

    complete_set  = pd.read_table('../datasets/%s/completeDataset.tsv' %dataset)

    embeddings = pd.read_table(embedding, skiprows = 1, header = None, sep = ' ')

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


    '''train_ids = np.array([int(i) for i in training_set['id']])

    y_train = np.array([convert_labels_to_int(i, dataset) for i in training_set[y_label]])

    N_train = len(train_ids)

    test_ids = np.array([int(i) for i in test_set['id']])

    y_test = np.array([convert_labels_to_int(i,dataset) for i in test_set[y_label]])

    N_test = len(test_ids)

    X_train = np.zeros((N_train,dimension))'''

    complete_ids = np.array([int(i) for i in complete_set['id']])

    y_complete = np.array([convert_labels_to_int(i, dataset) for i in complete_set[y_label]])

    N_complete = len(complete_ids)

    X_complete = np.zeros((N_complete,dimension))

    for i in range(N_complete):

        emb = get_embeddings(complete_ids[i], embeddings)

        emb = emb.reshape((1,dimension))

        X_complete[i] =  emb

    '''for i in range(N_train):

        emb = get_embeddings(train_ids[i], embeddings)

        emb = emb.reshape((1,dimension))

        X_train[i] =  emb


    X_test = np.zeros((N_test,dimension))


    for i in range(N_test):

        emb = get_embeddings(test_ids[i], embeddings)

        emb = emb.reshape((1,dimension))

        X_test[i] = emb

    #y_test = np.reshape(y_test,(len(X_test),1))
    #y_train = np.reshape(y_train,(len(X_train),1))

    #X_train_label = np.concatenate((X_train, y_train), axis = 1)

    #np.savetxt("train.csv", X_train_label, delimiter=",", fmt = '%10.5f')

    #X_test_label = np.concatenate((X_test, y_test), axis = 1)

    #np.savetxt("test.csv", X_test_label, delimiter=",", fmt = '%10.5f')'''

    #clf = SVC( kernel = 'rbf')

    #parameters = {'gamma' : np.logspace(-9,3,30),'C': [10**-3 , 10**-2 , 0.1, 1, 10, 10**2 , 10**3 ]}

    #gs_rbf = grid_search.GridSearchCV(clf,param_grid=parameters,cv = 10, n_jobs = -1) #grid search hyper parameter optimization
    '''gs_rbf.fit(X_train,y_train)

    #choose the best estimator 
    clf = gs_rbf.best_estimator_

    output_svm = np.reshape(clf.predict(X_test),(len(X_test),1))

    a_svm = sklearn.metrics.accuracy_score(y_test, output_svm)'''

    #print 'SVM rbf score:\n'

    #print "%.3f\n" %(a_svm )

    #gs_rbf.fit(X_complete,y_complete)

    #print "%.3f\n" %gs_rbf.best_score_

    clf_3 = KNeighborsClassifier()

    parameters_3 = {'n_neighbors' : range(1,15)}

    gs_rbf = grid_search.GridSearchCV(clf_3,param_grid=parameters_3,cv = 10, n_jobs = -1) #grid search hyper parameter optimization

    '''gs_rbf.fit(X_train,y_train)

    clf_3 = gs_rbf.best_estimator_

    clf_3.fit(X_train,y_train)

    output_k_neigh = np.reshape(clf_3.predict(X_test),(len(X_test),1))

    a_k_neigh = sklearn.metrics.accuracy_score(y_test,output_k_neigh)'''

    print 'K-nearest neighbors score:\n'

    #print "%.3f\n" %(a_k_neigh)

    gs_rbf.fit(X_complete,y_complete)

    print "%.3f\n" % (gs_rbf.best_score_)



    clf_2 = DecisionTreeClassifier(random_state = 0)

    parameters_2 = {'min_samples_split' : np.arange(0.01,0.2,0.01)}

    gs_rbf = grid_search.GridSearchCV(clf_2,param_grid=parameters_2,cv = 10, n_jobs = -1) #grid search hyper parameter optimization

    '''gs_rbf.fit(X_train,y_train)

    #clf_2 = gs_rbf.best_estimator_

    output_tree = np.reshape(gs_rbf.predict(X_test),(len(X_test),1))

    a_tree = sklearn.metrics.accuracy_score(y_test,output_tree)'''

    print 'Decision Tree score:\n'

    #print "%.3f\n" %(a_tree)

    gs_rbf.fit(X_complete,y_complete)

    print "%.3f\n" %(gs_rbf.best_score_)


    clf_4 = SVC(kernel = 'linear')

    parameters_4 = {'C' : [10**-3 , 10**-2 , 0.1, 1, 10, 10**2 , 10**3 ]}

    gs_rbf = grid_search.GridSearchCV(clf_4,param_grid=parameters_4,cv = 10, n_jobs = -1) #grid search hyper parameter optimization

    '''gs_rbf.fit(X_train,y_train)

    clf_4 = gs_rbf.best_estimator_

    clf_4.fit(X_train,y_train)

    output_svm_lin = np.reshape(clf_4.predict(X_test),(len(X_test),1))

    a_svm_lin = sklearn.metrics.accuracy_score(y_test,output_svm_lin)'''

    print 'SVM lin score:\n'

    #print "%.3f\n" %(a_svm_lin)

    gs_rbf.fit(X_complete,y_complete)

    print "%.3f\n" %gs_rbf.best_score_
