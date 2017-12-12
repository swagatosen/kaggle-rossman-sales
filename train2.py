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
dfTrain = pd.read_csv(trainFileDir, dtype={'Store': str, 'Date': str})

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



#split date into day, month and year
# dfMerged = dfMerged.iloc[:10000]
# dfMerged.info()
# dfMerged['Date_year'] = ''
# dfMerged['Date_month'] = ''
# dfMerged['Date_date'] = ''
# dfMerged[['Date_year', 'Date_month', 'Date_date']] = ''

# print(dfMerged)
# dfMerged[['year', 'month', 'date']] = dfMerged['Date'].apply(lambda column: preprocessing.SplitDateIntoDayMonthYear2(column, 'Date', 'YYYY-MM-DD'), axis = 1)
# dfMerged['Date'].apply(lambda row: preprocessing.SplitDateIntoDayMonthYear2(row, 'Date', 'YYYY-MM-DD'), axis = 1)
# preprocessing.SplitDateIntoDayMonthYear(dfMerged, 'Date', 'YYYY-MM-DD')

dfDateColumns = ['year', 'month', 'date']
print(dfTrain['Date'])
dfTrain['year'] = dfTrain['Date'].apply(lambda d: str(d)[:4])
dfTrain['month'] = dfTrain['Date'].apply(lambda d: str(d)[5:7])
dfTrain['date'] = dfTrain['Date'].apply(lambda d: str(d)[8:])

dfTrain = pd.merge(dfTrain, dfStore, how='left', left_on=['Store'], right_on=['Store'])

# dfTrain['hasCompetition'] = dfTrain[['year', 'month', 'CompetitionOpenSinceYear', 'CompetitionOpenSinceMonth']]
# 		.apply(lambda y, m, cy, cm: 1 if y >= cy )

print('printing train data after splitting date')
print(dfTrain)
# import timeit


# timeit.timeit("preprocessing.ProcessDimensionDf(dfMerged['Date'], 'Date', outputColumns=dfDateColumns, " + 
# 			"funcProcessColumn=preprocessing.SplitDateIntoDayMonthYear2, funcProcessColumnArgs=('YYYY/MM/DD'))", "import train2")

dfDate = preprocessing.ProcessDimensionDf(dfTrain['Date'], 'Date', outputColumns=dfDateColumns, funcProcessColumn=preprocessing.SplitDateIntoDayMonthYear2, funcProcessColumnArgs=('YYYY-MM-DD'))
dfDate.info()
print(dfDate)
dateColumns = ['year', 'month', 'date']
print("One hot encoding date: ")
for categories in dateColumns:
	dfDateOHE = preprocessing.OneHotEncodeColumn(dfDate, categories, True)
print(dfDateOHE)

# dfMerged = pd.merge(dfTrain, dfStore, how='left', left_on=['Store'], right_on=['Store'])
# print("\n\nMerged sample data: ")
# print(dfMerged)
# print(dfMerged.info())
# print(dfMerged.describe())

def CalculateCompetitionOpenDuration(y, m, cy, cm):
	if cy == 0:
		return 0
	else:
		diffY = y - cy
		diffM = m - cm

		if diffM < 0:
			if diffM >= -11:
				diffM = 12 + diffM
			else:
				print('Unable to calculate duration. Invalid month parameters- y: {0}, m: {1}, cy: {2}, cm: {3}'.format(y, m, cy, cm))
				return 0

			





