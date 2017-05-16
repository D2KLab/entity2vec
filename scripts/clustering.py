
# coding: utf-8

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

#importing data
data = pd.read_csv('c10_p1_q4/user_vectors.csv', header=None)

X = data.values[:,1:] #skip first row

k_means = KMeans(n_clusters = 10)

result = k_means.fit(X)

np.savetxt('c10_p1_q4/labels_10.csv',result.labels_, fmt='%d')




