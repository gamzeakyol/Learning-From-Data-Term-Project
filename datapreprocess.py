# -*- coding: utf-8 -*-
"""
Created on Mon May  7 17:23:36 2018
@author: mloz & gam
"""

import numpy as np
import pandas as pd
from scipy import stats
from collections import Counter
from sklearn.preprocessing import OneHotEncoder


trainDataset = pd.read_csv('minitrain.txt')
trainDataset['age'] = -1
trainDataset['deliveryDuration'] = -1
trainDataset['closenessToValentine'] = -1
trainDataset['closenessToNewYearsEve'] = -1

trainDataset = np.array(trainDataset, dtype = str)

year = []
month = []
day = []
difference = []

cnt = Counter(trainDataset[:, 10])
mostCommon = cnt.most_common(3)

for i in range(len(trainDataset)):
        trainDataset[i][4] = trainDataset[i][4].lower()
        
        #fix colors
        if trainDataset[i][5] == 'blau':
                trainDataset[i][5] = 'blue'
                
        elif trainDataset[i][5] == 'brwon':
                trainDataset[i][5] = 'brown'
                
        elif trainDataset[i][5] == 'ol' or trainDataset[i][5] == 'oliv':
                trainDataset[i][5] = 'olive'
                
        # no country for old men
        if trainDataset[i][10].split("-")[0] == "1900":
                trainDataset[i][10] = mostCommon[2][0]

        if trainDataset[i][2] != '?' and trainDataset[i][1] != '?' and trainDataset[i][10] != '?': 
                year.append((int(trainDataset[i][2].split("-")[0]) - int(trainDataset[i][1].split("-")[0]))*365)
                month.append((int(trainDataset[i][2].split("-")[1]) - int(trainDataset[i][1].split("-")[1]))*30)
                day.append((int(trainDataset[i][2].split("-")[2]) - int(trainDataset[i][1].split("-")[2])))
                difference.append(year[-1] + month[-1] + day[-1])
                trainDataset[i][14] = int(trainDataset[i][1].split("-")[0]) - int(trainDataset[i][10].split("-")[0])
                trainDataset[i][15] = difference[i]
                
                if difference[i] < 0:
                        difference[i] = "Time error"
        else:
                year.append('error')
                month.append('error')
                day.append('error')
                difference.append('error')
                trainDataset[i][14] = 'error'
                trainDataset[i][15] = 'error'
        
        if trainDataset[i][2] != '?':
                tempMonthNewYear = abs(int(trainDataset[i][2].split("-")[1]) - 12)*30
                trainDataset[i][17] = tempMonthNewYear + abs(int(trainDataset[i][2].split("-")[2]) - 31)
                
                tempMonthValentine = abs(int(trainDataset[i][2].split("-")[1]) - 2)*30
                trainDataset[i][16] = tempMonthValentine + abs(int(trainDataset[i][2].split("-")[2]) - 14)

items = np.array(trainDataset[:,3],int)
colors = np.array(trainDataset[:,5],str)

#item_color = np.zeros((2945, 84),int)
unique_colors = set(colors)
uniqueColors = []
for i in unique_colors:
        uniqueColors.append(i)

uniqueColors = np.array(uniqueColors)

'''for i in range(len(dataset)):
        color = dataset[i][5]
        for j in range(84):
                if uniqueColors[j] == color:
                        break

"      item_color[int(dataset[i][3])-1,j] += 1'''
'''for i in range(len(dataset)):
        if dataset[i][5] == '?':
                dataset[i][5] = uniqueColors[np.argmax(item_color[int(dataset[i][3])])]
'''
sizes = np.array(trainDataset[:,4],str)
unique_sizes = set(sizes)
uniqueSizes = []
for i in unique_sizes:
        uniqueSizes.append(i)

uniqueSizes = np.array(uniqueSizes)
     
genders = np.array(trainDataset[:,9],str)
unique_genders = set(genders)
uniqueGenders = []
for i in unique_genders:
        uniqueGenders.append(i)

uniqueGenders = np.array(uniqueGenders)

states = np.array(trainDataset[:,11],str)
unique_states = set(states)
uniqueStates = []
for i in unique_states:
        uniqueStates.append(i)

uniqueStates = np.array(uniqueStates)

for i in range(len(trainDataset)):
        for j in range(len(uniqueGenders)):
                if trainDataset[i][9] == uniqueGenders[j]:
                        trainDataset[i][9] = j
                        break
        for j in range(len(uniqueSizes)):
                if trainDataset[i][4] == uniqueSizes[j]:
                        trainDataset[i][4] = j
                        break
        for j in range(len(uniqueColors)):
                if trainDataset[i][5] == uniqueColors[j]:
                        trainDataset[i][5] = j
                        break
        for j in range(len(uniqueStates)):
                if trainDataset[i][11] == uniqueStates[j]:
                        trainDataset[i][11] = j
                        break

noErrorDataset = []

for i in range(len(trainDataset)):
        if trainDataset[i][2] != '?' and trainDataset[i][5] != '?' and trainDataset[i][10] != '?' and difference[i] != 'Time error':
                noErrorDataset.append(trainDataset[i])
        
noErrorDataset = np.array(noErrorDataset)
noErrorDataset = np.delete(noErrorDataset, 12, 1)
noErrorDataset = np.delete(noErrorDataset, 10, 1)
noErrorDataset = np.delete(noErrorDataset, 2, 1)
noErrorDataset = np.delete(noErrorDataset, 1, 1)
noErrorDataset = np.delete(noErrorDataset, 0, 1)
noErrorDataset = np.array(noErrorDataset,float) 

noErrorDataset[:,[8, 12]] = noErrorDataset[:,[12, 8]]

'''
sizesOneHot = np.zeros((len(noErrorDataset),len(uniqueSizes)))
sizesOneHot[np.arange(len(noErrorDataset)), noErrorDataset[:,1]] = 1
'''

noErrorDataset[:, :12] = stats.zscore(noErrorDataset[:, :12],axis=0)

np.savetxt("trainDataset.csv", noErrorDataset, delimiter=",", fmt="%s")


a = np.array([1, 0, 3])
b = np.zeros((3, 4))
b[np.arange(3), a] = 1
print(b)
