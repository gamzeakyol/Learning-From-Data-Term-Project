# -*- coding: utf-8 -*-
"""
Created on Mon May 14 13:31:31 2018

@author: mloz & gam & pelo
"""
import numpy as np
import pandas as pd
from scipy import stats
from collections import Counter

def getCategoricalArray(unique, array):
    sizesArrayOneHot = np.array(array,int)
    sizesOneHot = np.zeros((len(dataset),len(unique)))
    sizesOneHot[np.arange(len(dataset)), sizesArrayOneHot] = 1
    return sizesOneHot

dataset = pd.read_csv('test.txt')
dataset['age'] = -1
dataset['deliveryDuration'] = -1
dataset['closenessToValentine'] = -1
dataset['closenessToNewYearsEve'] = -1
dataset['risk'] = -1
dataset['averageSpentMoney'] = -1
dataset['shoppingFrequency'] = -1
dataset['manufacturerRisk'] = -1
dataset = np.array(dataset, dtype = str)

# if test set is processed
dataset['dummyReturnShipment'] = -1
dataset = np.array(dataset, dtype = str)

year = []
month = []
day = []
difference = []

cnt = Counter(dataset[:, 10])
mostCommon = cnt.most_common(3)
customerID = 0

items = np.array(dataset[:,3],str)
uniqueItems = np.array(list(set(items)))

customers = np.array(dataset[:,8],int)
uniqueCustomers = np.array(list(set(customers)))

manufacturer = np.array(dataset[:,6],str)
uniqueMans = np.array(list(set(manufacturer)))

r = np.zeros((len(uniqueItems),2))
risk = np.zeros((len(uniqueItems), 1))

m = np.zeros((len(uniqueMans),2))
man_risk = np.zeros((len(uniqueMans), 1))

# 0th column total spent money, 1st column is purchase count
customerInfo = np.zeros((len(uniqueCustomers),2))

for i in range(len(dataset)):
        dataset[i][4] = dataset[i][4].lower()
        
        #fix colors
        if dataset[i][5] == 'blau':
                dataset[i][5] = 'blue'
                
        elif dataset[i][5] == 'brwon':
                dataset[i][5] = 'brown'
                
        elif dataset[i][5] == 'ol' or dataset[i][5] == 'oliv':
                dataset[i][5] = 'olive'
                
        # no country for old men
        if dataset[i][10].split("-")[0] == "1900":
                dataset[i][10] = mostCommon[2][0]
                        
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
                
        if dataset[i][2] != '?':
            orderMonth = int(dataset[i][2].split("-")[1])
            orderDay = int(dataset[i][2].split("-")[2])
            if orderMonth > 6:
                tempMonthNewYear = (12-orderMonth)*30
                dataset[i][17] = tempMonthNewYear + 31 - orderDay
            else: 
                tempMonthNewYear = orderMonth*30
                dataset[i][17] = tempMonthNewYear + orderDay
                
            if 2 < orderMonth < 8:
                if orderDay > 14:
                    temp = orderDay - 14
                    temp += (orderMonth-2)*30
                    dataset[i][16] = temp
                else:
                    temp = 30 - (14-orderDay)
                    temp += (orderMonth - 2 -1) * 30
                    dataset[i][16] = temp
                    
            elif orderMonth == 2:
                    dataset[i][16] = abs(orderDay - 14)
            else:
                if orderDay > 14: 
                    temp = 30 - (orderDay - 14)
                    temp += (12 - orderMonth -1 + 2) * 30
                    dataset[i][16] = temp
                else:
                    temp = 14 - orderDay
                    temp += (12 - orderMonth + 2)*30
                    dataset[i][16] = temp
                
                # Gam
        for j in range(len(uniqueItems)):
                if uniqueItems[j] == dataset[i][3]:
                    if dataset[i][13] == "0.0":
                        r[j][0] += 1
                    else:
                        r[j][1] += 1
        # Mah
        for j in range(len(uniqueCustomers)):
                if uniqueCustomers[j] == dataset[i][8]:
                    customerInfo[j][0] += float(dataset[i][7])
                    customerInfo[j][1] += 1
                    
        # Gam
        for j in range(len(uniqueMans)):
                if uniqueMans[j] == dataset[i][6]:
                    if dataset[i][13] == "0.0":
                        m[j][0] += 1
                    else:
                        m[j][1] += 1

#Gam                
for i in range(len(r)):
    risk[i] = float(5 + r[i][1]) / float(10 + r[i][0] + r[i][1])
    
for i in range(len(m)):
    man_risk[i] = float(5 + m[i][1]) / float(10 + m[i][0] + m[i][1])
    
for i in range(len(dataset)):
    for j in range(len(risk)):
        if uniqueItems[j] == dataset[i][3]:
            dataset[i,18] = risk[j]
    for j in range(len(uniqueCustomers)):
        if uniqueCustomers[j] == dataset[i][8]:
            dataset[i,19] = str(customerInfo[j,0]/customerInfo[j,1])
            dataset[i,20] = customerInfo[j,1]
    for j in range(len(man_risk)):
        if uniqueMans[j] == dataset[i][6]:
            dataset[i,21] = man_risk[j]

items = np.array(dataset[:,3],int)
colors = np.array(dataset[:,5],str)

#item_color = np.zeros((2945, 84),int)

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
sizes = np.array(dataset[:,4],str)
uniqueSizes = np.array(list(set(sizes)))
     
genders = np.array(dataset[:,9],str)
uniqueGenders = np.array(list(set(genders)))

states = np.array(dataset[:,11],str)
uniqueStates = np.array(list(set(states)))

items = np.array(dataset[:,3],str)
uniqueItems = np.array(list(set(items)))

r = np.zeros((len(uniqueItems),3))

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

cnt = Counter(dataset[:, 14])
mostCommon = cnt.most_common(2)
mostCommon14 = mostCommon[1][0]

cnt = Counter(dataset[:, 15])
mostCommon = cnt.most_common(2)
mostCommon15 = mostCommon[1][0]

for i in range(len(dataset)):
        if dataset[i][14] == 'error':
                dataset[i][14] = mostCommon14
        if dataset[i][15] == 'error':
                dataset[i][15] = mostCommon15
        if dataset[i][5] == '?':
                dataset[i][5] = 25

for i in range(len(dataset)):
        if 'error' in dataset[i]:
                print(i)
                print(dataset)
                break
        
dataset = np.delete(dataset, 12, 1)
dataset = np.delete(dataset, 10, 1)
dataset = np.delete(dataset, 2, 1)
dataset = np.delete(dataset, 1, 1)
dataset = np.delete(dataset, 0, 1)
dataset = np.array(dataset,float) 

dataset[:,[8, 12]] = dataset[:,[12, 8]]


dataset[:, :12] = stats.zscore(dataset[:, :12],axis=0)


np.savetxt("testDataset.csv", dataset, delimiter=",", fmt="%s")
