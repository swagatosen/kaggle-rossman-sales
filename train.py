import numpy as np
import pandas as pd
import matplotlib

import os

# data files available for training
# train.csv, store.csv

# locations of data files
root = os.path.dirname(os.path.realpath(__file__))
storeFileDir = os.path.join(root, "data", "store.csv")
trainFileDir = os.path.join(root, "data", "train.csv")

print ("root directory: " + root)
print ("file location (store): " + storeFileDir)
print ("file location (train): " + trainFileDir)


storeReader = pd.read_csv(storeFileDir, sep=',', iterator=True)
trainReader = pd.read_csv(trainFileDir, sep=',', iterator=True)

storeSampleData = storeReader.get_chunk(10)
trainSampleData = trainReader.get_chunk(10)

storeColumns = list(storeSampleData.columns.values)
trainColumns = list(trainSampleData.columns.values)

print("Store columns: " + str(storeColumns))
print("Store sample data: \n\n")
print(storeSampleData)
print("\n\nTrain columns: " + str(trainColumns))
print("Train sample data: \n\n")
print(trainSampleData)


mergedSampleData = pd.merge(trainSampleData, storeSampleData, how='left', left_on=['Store'], right_on=['Store'])
print("\n\nMerged sample data: ")
print(mergedSampleData)

Y_train = mergedSampleData.loc[:, 'Sales']
del mergedSampleData['Sales']
del mergedSampleData['Customers']
X_train = mergedSampleData

print("\n\nx_train: ")
print(X_train)
del X_train['Store']
print("\n\nx_train again: ")
print(X_train)

print("\n\nMerged sample data: ")
print(mergedSampleData)

print("y_train: ")
print(Y_train)

