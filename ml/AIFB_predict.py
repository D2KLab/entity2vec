import pandas as pd
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn import cross_validation
from sklearn import grid_search
import sklearn.metrics
import numpy as np

def get_embeddings(ID, embeddings):

    return embeddings[embeddings[0] == ID].values[0]

def convert_labels_to_int(label):
    if label == 'http://www.aifb.uni-karlsruhe.de/Forschungsgruppen/viewForschungsgruppeOWL/id1instance':
        return 1
    elif label == 'http://www.aifb.uni-karlsruhe.de/Forschungsgruppen/viewForschungsgruppeOWL/id2instance':
        return 2
    elif label == 'http://www.aifb.uni-karlsruhe.de/Forschungsgruppen/viewForschungsgruppeOWL/id3instance':
        return 3
    else:
        return 4

training_set = pd.read_table('../datasets/AIFB/trainingSet.tsv')

test_set = pd.read_table('../datasets/AIFB/testSet.tsv')

embeddings = pd.read_table('../emb/AIFB/aifb_p_0.3_q_1.emd', skiprows = 1, header = None, sep = ' ')

train_ids = np.array([int(i) for i in training_set['id']])

y_train = np.array([convert_labels_to_int(i) for i in training_set['label_affiliation']])

N_train = len(train_ids)

test_ids = np.array([int(i) for i in test_set['id']])

y_test = np.array([convert_labels_to_int(i) for i in test_set['label_affiliation']])

N_test = len(test_ids)

X_train = np.zeros((N_train,130))

for i in range(N_train):

    emb = get_embeddings(train_ids[i], embeddings)

    emb = emb.reshape((1,129))

    X_train[i] =  np.append(emb, y_train[i])

X_test = np.zeros((N_test,130))

for i in range(N_test):

    emb = get_embeddings(test_ids[i], embeddings)

    emb = emb.reshape((1,129))

    X_test[i] =  np.append(emb, y_test[i])

y_test = np.reshape(y_test,(len(X_test),1))


clf = SVC( kernel = 'rbf')

parameters = {'gamma' : np.logspace(-9,3,5),'C': np.logspace(-2,10,5)}

gs_rbf = grid_search.GridSearchCV(clf,param_grid=parameters,cv = 10, n_jobs = -1) #grid search hyper parameter optimization
gs_rbf.fit(X_train,y_train)

#choose the best estimator 
clf = gs_rbf.best_estimator_

output_svm = np.reshape(clf.predict(X_test),(len(X_test),1))

a_svm = sklearn.metrics.accuracy_score(y_test, output_svm)

print 'SVM scores:\n'

print "%.3f\n" %(a_svm )


clf_2 = RandomForestClassifier()

parameters_2 = {'n_estimators' : range(5,50,5)}

gs_rbf = grid_search.GridSearchCV(clf_2,param_grid=parameters_2,cv = 10, n_jobs = -1) #grid search hyper parameter optimization

gs_rbf.fit(X_train,y_train)

clf_2 = gs_rbf.best_estimator_

output_forest = np.reshape(clf_2.predict(X_test),(len(X_test),1))

a_forest = sklearn.metrics.accuracy_score(y_test,output_forest)

print 'Random Forest score:\n'

print "%.3f\n" %(a_forest)


clf_3 = KNeighborsClassifier()

parameters_3 = {'n_neighbors' : range(1,15)}

gs_rbf = grid_search.GridSearchCV(clf_3,param_grid=parameters_3,cv = 10, n_jobs = -1) #grid search hyper parameter optimization

gs_rbf.fit(X_train,y_train)

clf_3 = gs_rbf.best_estimator_

clf_3.fit(X_train,y_train)

output_k_neigh = np.reshape(clf_3.predict(X_test),(len(X_test),1))

a_k_neigh = sklearn.metrics.accuracy_score(y_test,output_k_neigh)

print 'K-nearest neighbors scores:\n'

print "%.3f\n" %(a_k_neigh)



clf_4 = SVC(kernel = 'linear')

parameters_4 = {'C' : [10**-3 , 10**-2 , 0.1, 1, 10, 10**2 , 10**3 ]}

gs_rbf = grid_search.GridSearchCV(clf_4,param_grid=parameters_4,cv = 10, n_jobs = -1) #grid search hyper parameter optimization

gs_rbf.fit(X_train,y_train)

clf_4 = gs_rbf.best_estimator_

clf_4.fit(X_train,y_train)

output_svm_lin = np.reshape(clf_4.predict(X_test),(len(X_test),1))

a_svm_lin = sklearn.metrics.accuracy_score(y_test,output_svm_lin)

print 'SVM lin scores:\n'

print "%.3f\n" %(a_svm_lin)