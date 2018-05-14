# -*- coding: utf-8 -*-
"""
Created on Mon May  7 17:23:36 2018

@author: mloz & gam
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats


dataset = pd.read_csv('train.txt')
'''returns = dataset['returnShipment']
del dataset['returnShipment']'''
dataset['age'] = -1
dataset['deliveryDuration'] = -1
#dataset['returnShipment'] = returns
dataset = np.array(dataset, dtype = str)

hayda = 0
year = []
month = []
day = []
difference = []
for i in range(len(dataset)):
        dataset[i][4] = dataset[i][4].lower()
        '''if dataset[i][9] == "Mr":
                dataset[i][9] = "1"
        else: 
                dataset[i][9] = "0"'''
                        
        if dataset[i][2] != '?' and dataset[i][1] != '?' and dataset[i][10] != '?': 
                year.append((int(dataset[i][2].split("-")[0]) - int(dataset[i][1].split("-")[0]))*365)
                month.append((int(dataset[i][2].split("-")[1]) - int(dataset[i][1].split("-")[1]))*30)
                day.append((int(dataset[i][2].split("-")[2]) - int(dataset[i][1].split("-")[2])))
                difference.append(year[-1] + month[-1] + day[-1])
                dataset[i][14] = int(dataset[i][1].split("-")[0]) - int(dataset[i][10].split("-")[0])
                dataset[i][15] = difference[i]
                
                if difference[i] < 0:
                        difference[i] = "Time error"
        else:
                year.append('error')
                month.append('error')
                day.append('error')
                difference.append('error')
                dataset[i][14] = 'error'
                dataset[i][15] = 'error'

items = np.array(dataset[:,3],int)
colors = np.array(dataset[:,5],str)

item_color = np.zeros((2943, 84),int)

unique_colors = set(colors)
uniqueColors = []
for i in unique_colors:
        uniqueColors.append(i)

uniqueColors = np.array(uniqueColors)

for i in range(len(dataset)):
        color = dataset[i][5]
        for j in range(84):
                if uniqueColors[j] == color:
                        break

        item_color[int(dataset[i][3])-1,j] += 1
hayda = 0
for i in range(len(dataset)):
        if dataset[i][5] == '?':
                dataset[i][5] = uniqueColors[np.argmax(item_color[int(dataset[i][3])])]

sizes = np.array(dataset[:,4],str)
unique_sizes = set(sizes)
uniqueSizes = []
for i in unique_sizes:
        uniqueSizes.append(i)

uniqueSizes = np.array(uniqueSizes)
     
genders = np.array(dataset[:,9],str)
unique_genders = set(genders)
uniqueGenders = []
for i in unique_genders:
        uniqueGenders.append(i)

uniqueGenders = np.array(uniqueGenders)

states = np.array(dataset[:,11],str)
unique_states = set(states)
uniqueStates = []
for i in unique_states:
        uniqueStates.append(i)

uniqueStates = np.array(uniqueStates)

for i in range(len(dataset)):
        for j in range(len(uniqueGenders)):
                if dataset[i][9] == uniqueGenders[j]:
                        dataset[i][9] = j
                        break
        for j in range(len(uniqueSizes)):
                if dataset[i][4] == uniqueSizes[j]:
                        dataset[i][4] = j
                        break
        for j in range(len(uniqueColors)):
                if dataset[i][5] == uniqueColors[j]:
                        dataset[i][5] = j
                        break
        for j in range(len(uniqueStates)):
                if dataset[i][11] == uniqueStates[j]:
                        dataset[i][11] = j
                        break

noErrorDataset = []

for i in range(len(dataset)):
        if dataset[i][2] != '?' and dataset[i][5] != '?' and dataset[i][10] != '?' and difference[i] != 'Time error':
                noErrorDataset.append(dataset[i])
        
noErrorDataset = np.array(noErrorDataset)
noErrorDataset = np.delete(noErrorDataset, 12, 1)
noErrorDataset = np.delete(noErrorDataset, 10, 1)
noErrorDataset = np.delete(noErrorDataset, 2, 1)
noErrorDataset = np.delete(noErrorDataset, 1, 1)
noErrorDataset = np.delete(noErrorDataset, 0, 1)
noErrorDataset = np.array(noErrorDataset,float) 

#dataset = pd.read_csv('gamah.csv')
#dataset = np.array(dataset)
'''temp = noErrorDataset[:,8]
noErrorDataset[:,8] = noErrorDataset[:,10]
noErrorDataset[:,10] = temp
'''
noErrorDataset[:,[8, 10]] = noErrorDataset[:,[10, 8]]


noErrorDataset[:, :10] = stats.zscore(noErrorDataset[:, :10],axis=0)


np.savetxt("gamah.csv", noErrorDataset, delimiter=",", fmt="%s")

