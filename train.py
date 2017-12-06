import numpy as np
import pandas as pd
import matplotlib
import preprocessing

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

dfStore = pd.read_csv(storeFileDir, dtype={'Store': str, 'StoreType': str, 'Assortment': str, 'PromoInterval': str})
dfTrain = pd.read_csv(trainFileDir, dtype={'Store': str})

# storeReader = pd.read_csv(storeFileDir, sep=',', iterator=True)
# trainReader = pd.read_csv(trainFileDir, sep=',', iterator=True)
# dfStore = storeReader.get_chunk(1000)
# dfStore = trainReader.get_chunk(1000)

storeColumns = list(dfStore.columns.values)
trainColumns = list(dfTrain.columns.values)

print("Store columns: " + str(storeColumns))
print("Store sample data: \n\n")
dfStore.info()
print(dfStore.describe())
print(dfStore.head(10))
# print(storeSampleData)
print("\n\nTrain columns: " + str(trainColumns))
print("Train sample data: \n\n")
# print(trainSampleData)
dfTrain.info()
print(dfTrain.describe())
print(dfTrain.head(10))


dfMerged = pd.merge(dfTrain, dfStore, how='left', left_on=['Store'], right_on=['Store'])
print("\n\nMerged sample data: ")
# print(mergedSampleData)
print(dfMerged.info())
print(dfMerged.describe())



#split date into day, month and year
# dfMerged = dfMerged.iloc[:1000]
dfMerged.info()
dfMerged['Date_year'] = ''
dfMerged['Date_month'] = ''
dfMerged['Date_date'] = ''
# dfMerged[['Date_year', 'Date_month', 'Date_date']] = ''

print(dfMerged)
# dfMerged[['year', 'month', 'date']] = dfMerged['Date'].apply(lambda column: preprocessing.SplitDateIntoDayMonthYear2(column, 'Date', 'YYYY-MM-DD'), axis = 1)
# dfMerged['Date'].apply(lambda row: preprocessing.SplitDateIntoDayMonthYear2(row, 'Date', 'YYYY-MM-DD'), axis = 1)
preprocessing.SplitDateIntoDayMonthYear(dfMerged, 'Date', 'YYYY-MM-DD')

categoricalColumns = ['DayOfWeek', 'Assortment', 'StoreType', 'StateHoliday', 'Date_year', 'Date_month', 'Date_date'];
print("One hot encoding categorical variables: ")
for categories in categoricalColumns:
	dfMerged = preprocessing.OneHotEncodeColumn(dfMerged, categories)
print(dfMerged)

Y_train = dfMerged.loc[:, 'Sales']
print("y_train: ")
print(Y_train)

del dfMerged['Sales']
del dfMerged['Customers']
del dfMerged['Store']

X_train = dfMerged
print("\n\nx_train: ")
print(X_train)

