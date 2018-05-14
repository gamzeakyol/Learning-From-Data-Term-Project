# -*- coding: utf-8 -*-
"""
Created on Mon May 14 12:47:43 2018

@author: mloz
"""

from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np

noErrorDataset = pd.read_csv('gamah.csv')

noErrorDataset = np.array(noErrorDataset)

X = noErrorDataset[:,:10]
Y = noErrorDataset[:,10:11]

clf = RandomForestClassifier(max_depth=2, random_state=0)
clf.fit(X, Y)

