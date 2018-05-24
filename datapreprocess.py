# -*- coding: utf-8 -*-
"""
Created on Mon May  7 17:23:36 2018
@author: mloz & gam & pelo
"""

import numpy as np
import pandas as pd
from scipy import stats
from collections import Counter


def getCategoricalArray(unique, array):
    sizesArrayOneHot = np.array(array,int)
    sizesOneHot = np.zeros((len(noErrorDataset),len(unique)))
    sizesOneHot[np.arange(len(noErrorDataset)), sizesArrayOneHot] = 1
    return sizesOneHot

trainDataset = pd.read_csv('train.txt')
testDataset = pd.read_csv('test.txt')
trainDataset['age'] = -1
trainDataset['deliveryDuration'] = -1
trainDataset['closenessToValentine'] = -1
trainDataset['closenessToNewYearsEve'] = -1
trainDataset['risk'] = -1
trainDataset['averageSpentMoney'] = -1
trainDataset['shoppingFrequency'] = -1
trainDataset['manufacturerRisk'] = -1
trainDataset = np.array(trainDataset, dtype = str)
testDataset = np.array(testDataset, dtype = str)

year = []
month = []
day = []
difference = []

cnt = Counter(trainDataset[:, 10])
mostCommon = cnt.most_common(3)
customerID = 0


trainItems = np.array(trainDataset[:,3],str)
testItems = np.array(testDataset[:,3],str)
items = np.concatenate((trainItems, testItems), axis=0)
uniqueItems = np.array(list(set(items)))

trainCustomers = np.array(trainDataset[:,8],int)
testCustomers = np.array(testDataset[:,8],int)
customers = np.concatenate((trainCustomers, testCustomers), axis=0)
uniqueCustomers = list(set(customers))

trainMans = np.array(trainDataset[:,6],int)
testMans = np.array(testDataset[:,6],int)
manufacturer = np.concatenate((trainMans, testMans), axis=0)
uniqueMans = np.array(list(set(manufacturer)))

r = np.zeros((len(uniqueItems),2))
risk = np.zeros((len(uniqueItems), 1))

m = np.zeros((len(uniqueMans),2))
man_risk = np.zeros((len(uniqueMans), 1))

# 0th column total spent money, 1st column is purchase count
customerInfo = np.zeros((len(uniqueCustomers),3))
customerInfo[:,0] = uniqueCustomers

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
        
        # closness to special days
        if trainDataset[i][2] != '?':
            orderMonth = int(trainDataset[i][2].split("-")[1])
            orderDay = int(trainDataset[i][2].split("-")[2])
            if orderMonth > 6:
                tempMonthNewYear = (12-orderMonth)*30
                trainDataset[i][17] = tempMonthNewYear + 31 - orderDay
            else: 
                tempMonthNewYear = orderMonth*30
                trainDataset[i][17] = tempMonthNewYear + orderDay
                
            if 2 < orderMonth < 8:
                if orderDay > 14:
                    temp = orderDay - 14
                    temp += (orderMonth-2)*30
                    trainDataset[i][16] = temp
                else:
                    temp = 30 - (14-orderDay)
                    temp += (orderMonth - 2 -1) * 30
                    trainDataset[i][16] = temp
                    
            elif orderMonth == 2:
                    trainDataset[i][16] = abs(orderDay - 14)
            else:
                if orderDay > 14: 
                    temp = 30 - (orderDay - 14)
                    temp += (12 - orderMonth -1 + 2) * 30
                    trainDataset[i][16] = temp
                else:
                    temp = 14 - orderDay
                    temp += (12 - orderMonth + 2)*30
                    trainDataset[i][16] = temp
                    
        # Gam
        for j in range(len(uniqueItems)):
                if uniqueItems[j] == trainDataset[i][3]:
                    if trainDataset[i][13] == "0.0":
                        r[j][0] += 1
                    else:
                        r[j][1] += 1
                        
        index_of_ID_in_unique = uniqueCustomers.index(int(trainDataset[i][8]))
        customerInfo[index_of_ID_in_unique][1] += float(trainDataset[i][7])
        customerInfo[index_of_ID_in_unique][2] += 1
       
        # Gam
        for j in range(len(uniqueMans)):
                if uniqueMans[j] == trainDataset[i][6]:
                    if trainDataset[i][13] == "0.0":
                        m[j][0] += 1
                    else:
                        m[j][1] += 1

#Gam                
for i in range(len(r)):
    risk[i] = float(5 + r[i][1]) / float(10 + r[i][0] + r[i][1])

risk = np.ravel(risk)
    
for i in range(len(m)):
    man_risk[i] = float(5 + m[i][1]) / float(10 + m[i][0] + m[i][1])

man_risk = np.ravel(man_risk)

# Update rows 
for i in range(len(trainDataset)):
    for j in range(len(risk)):
        if uniqueItems[j] == trainDataset[i][3]:
            trainDataset[i,18] = risk[j]
            
    index_of_ID_in_unique = uniqueCustomers.index(int(trainDataset[i][8]))
    trainDataset[i,19] = str(customerInfo[index_of_ID_in_unique][1]/customerInfo[index_of_ID_in_unique][2])
    trainDataset[i,20] = customerInfo[index_of_ID_in_unique][2]
            
    for j in range(len(man_risk)):
        if uniqueMans[j] == trainDataset[i][6]:
            trainDataset[i,21] = man_risk[j]
            
            
for i in range(len(testDataset)):
        testDataset[i][4] = testDataset[i][4].lower()
        
        #fix colors
        if testDataset[i][5] == 'blau':
            testDataset[i][5] = 'blue'
                
        elif testDataset[i][5] == 'brwon':
            testDataset[i][5] = 'brown'
                
        elif testDataset[i][5] == 'ol' or testDataset[i][5] == 'oliv':
            testDataset[i][5] = 'olive'

trainColors = np.array(trainDataset[:,5],str)
testColors = np.array(testDataset[:,5],str)
colors = np.concatenate((trainColors, testColors), axis=0)
uniqueColors = np.array(list(set(colors)))

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
trainSizes = np.array(trainDataset[:,4],str)
testSizes = np.array(testDataset[:,4],str)
sizes = np.concatenate((trainSizes, testSizes), axis=0)
uniqueSizes = np.array(list(set(sizes)))
     
trainGenders = np.array(trainDataset[:,9],str)
testGenders = np.array(testDataset[:,9],str)
genders = np.concatenate((trainGenders, testGenders), axis=0)
uniqueGenders = np.array(list(set(genders)))

trainStates = np.array(trainDataset[:,11],str)
testStates = np.array(testDataset[:,11],str)
states = np.concatenate((trainStates, testStates), axis=0)
uniqueStates = np.array(list(set(states)))

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

onehotGenders = getCategoricalArray(uniqueGenders, noErrorDataset[:,9])
onehotSizes = getCategoricalArray(uniqueSizes, noErrorDataset[:,4])
onehotColors = getCategoricalArray(uniqueColors, noErrorDataset[:,5])
onehotStates = getCategoricalArray(uniqueStates, noErrorDataset[:,11])


noErrorDataset = np.delete(noErrorDataset, 20, 1)
noErrorDataset = np.delete(noErrorDataset, 19, 1)
noErrorDataset = np.delete(noErrorDataset, 12, 1)
noErrorDataset = np.delete(noErrorDataset, 11, 1) # states
noErrorDataset = np.delete(noErrorDataset, 10, 1)
noErrorDataset = np.delete(noErrorDataset, 9, 1)  # genders
noErrorDataset = np.delete(noErrorDataset, 8, 1)  # customer id
noErrorDataset = np.delete(noErrorDataset, 6, 1)  # manufacturer id
noErrorDataset = np.delete(noErrorDataset, 5, 1)  # colors
noErrorDataset = np.delete(noErrorDataset, 4, 1)  # sizes
noErrorDataset = np.delete(noErrorDataset, 3, 1)  # item id
noErrorDataset = np.delete(noErrorDataset, 2, 1)
noErrorDataset = np.delete(noErrorDataset, 1, 1)
noErrorDataset = np.delete(noErrorDataset, 0, 1)
noErrorDataset = np.array(noErrorDataset,float) 

noErrorDataset[:,[1, 7]] = noErrorDataset[:,[7, 1]]

oneHotNoErrorDataset = np.zeros((len(noErrorDataset),8+5+265+320+16),float)
oneHotNoErrorDataset[:,:7] = noErrorDataset[:,:7]
oneHotNoErrorDataset[:,7:12] = onehotGenders
oneHotNoErrorDataset[:,12:277] = onehotColors
oneHotNoErrorDataset[:,277:597] = onehotSizes
oneHotNoErrorDataset[:,597:613] = onehotStates
oneHotNoErrorDataset[:,-1] = noErrorDataset[:,-1]

'''
sizesOneHot = np.zeros((len(noErrorDataset),len(uniqueSizes)))
sizesOneHot[np.arange(len(noErrorDataset)), noErrorDataset[:,1]] = 1
'''
'''
for i in range(len(noErrorDataset)):
    r[i][0] = noErrorDataset[i][12]
    if noErrorDataset[i][12] == 0:
        r[i][1] += 1
    else:
        r[i][2] += 1
'''    

oneHotNoErrorDataset[:, :7] = stats.zscore(oneHotNoErrorDataset[:, :7],axis=0)   #normalize ediliyor

np.savetxt("trainDataset.csv", oneHotNoErrorDataset, delimiter=",", fmt="%s")
