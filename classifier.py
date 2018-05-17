# -*- coding: utf-8 -*-
"""
Created on Mon May 14 12:47:43 2018
@author: mloz
"""

from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np
from sklearn.model_selection import KFold, cross_val_score, cross_val_predict
from sklearn.neural_network import MLPClassifier
import csv

def readTestData():
    # Read data
    data = []
    ifile = open("testDataset.csv","r")
    read = csv.reader(ifile)
    
    for row in read:
        data.append(row)
    data = np.array(data, dtype=np.float64)
    
    return data

trainSet= pd.read_csv('trainDataset.csv')
testSet = readTestData()

trainSet = np.array(trainSet)
testSet = np.array(testSet)

X = trainSet[:,:12]
Y = trainSet[:,12:13]

clf = RandomForestClassifier(random_state=0)

mlp = MLPClassifier(hidden_layer_sizes=(20,50), activation='relu', solver='adam', alpha=0.0001,
                    batch_size='auto', learning_rate='constant', learning_rate_init=0.001, power_t=0.5,
                    max_iter=200, shuffle=True, random_state=None, tol=0.0001, verbose=False, warm_start=False,
                    momentum=0.9, nesterovs_momentum=True, early_stopping=False, validation_fraction=0.1, beta_1=0.9,
                    beta_2=0.999, epsilon=1e-08)

classifier = mlp.fit(X, Y)

testX = testSet[:,:12]

predicts = classifier.predict_proba(testX)

results = np.zeros((50078,2))

for i in range(len(results)):
        results[i,0] = str(i+1)
        results[i,1] = predicts[i,1]
        
results = np.array(results,str)

for i in range(len(results)):
        results[i,0] = results[i,0].split(".")[0]
        
np.savetxt("results.csv", results, delimiter=",", fmt="%s")

'''
kf = KFold(n_splits=3, random_state=None, shuffle=True)
randomforest = RandomForestClassifier(n_estimators=200)
score = cross_val_score(randomforest,X,Y,cv=kf,scoring='accuracy')
'''

