import pandas as pd
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn import cross_validation
from sklearn import grid_search
import sklearn.metrics
import numpy as np

def get_embeddings(ID, embeddings):

    return embeddings[embeddings[0] == ID].values[0]

training_set = pd.read_table('../datasets/BGS/trainingSet(lith).tsv')

test_set = pd.read_table('../datasets/BGS/testSet(lith).tsv')

embeddings = pd.read_table('../emb/BGS/bgs_lith_p_0.3_q_1.emd', skiprows = 1, header = None, sep = ' ')

possible_labels = []

for i in set(training_set['label_lithogenesis']):
    possible_labels.append(i)

labels_to_int = {}

for i in range(len(possible_labels)):

    labels_to_int[possible_labels[i]] = i

train_ids = np.array([int(i) for i in training_set['id']])

y_train = np.array([labels_to_int[label] for label in training_set['label_lithogenesis']])

N_train = len(train_ids)

test_ids = np.array([int(i) for i in test_set['id']])

y_test = np.array([labels_to_int[label] for label in test_set['label_lithogenesis']])

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


clf_3 = SVC(kernel = 'linear')

parameters_3 = {'C' : [10**-3 , 10**-2 , 0.1, 1, 10, 10**2 , 10**3 ]}

gs_rbf = grid_search.GridSearchCV(clf_3,param_grid=parameters_3,cv = 10, n_jobs = -1) #grid search hyper parameter optimization

gs_rbf.fit(X_train,y_train)

clf_3 = gs_rbf.best_estimator_

output_svm_lin = np.reshape(clf_3.predict(X_test),(len(X_test),1))

a_svm_lin = sklearn.metrics.accuracy_score(y_test,output_svm_lin)

print 'SVM lin scores:\n'

print "%.3f\n" %(a_svm_lin)