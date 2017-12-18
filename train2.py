import numpy as np
import pandas as pd
import matplotlib
import preprocessing
import math
import os 
import tensorflow as tf

# data files available for training
# train.csv, store.csv

# locations of data files
pd.set_option('display.max_columns', 999)
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

print("Analysing train df: ")
print(preprocessing.AnalyseDfForNaN(dfTrain))

print("Analysing store df: ")
print(preprocessing.AnalyseDfForNaN(dfStore))

dfStore['Promo2SinceWeek'] = dfStore['Promo2SinceWeek'].map(lambda x: 0 if math.isnan(x) else x)
dfStore['Promo2SinceYear'] = dfStore['Promo2SinceYear'].map(lambda x: 0 if math.isnan(x) else x)

print(dfStore['PromoInterval'])
dfStore['PromoInterval'] = dfStore['PromoInterval'].map(lambda x: 0 if x is np.nan else x)

print(dfStore['PromoInterval'])

dfStore['CompetitionOpenSinceYear'] = dfStore['CompetitionOpenSinceYear'].map(lambda x: 99999 if math.isnan(x) else x)
dfStore['CompetitionOpenSinceMonth'] = dfStore['CompetitionOpenSinceMonth'].map(lambda x: 0 if math.isnan(x) else x)
dfStore['CompetitionDistance'] = dfStore['CompetitionDistance'].map(lambda x: 9999999 if math.isnan(x) else x)

print("Analysing train df: ")
print(preprocessing.AnalyseDfForNaN(dfTrain))

print("Analysing store df: ")
print(preprocessing.AnalyseDfForNaN(dfStore))

print(dfStore['PromoInterval'].unique())
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
categoricalVariables = []
# run the next 3 lines of code for mac
# dfTrain['year'] = dfTrain['Date'].apply(lambda d: str(d)[:4])
# dfTrain['month'] = dfTrain['Date'].apply(lambda d: str(d)[5:7])
# dfTrain['date'] = dfTrain['Date'].apply(lambda d: str(d)[8:])

# run the next 3 lines of code for windows
# dfTrain['year'] = dfTrain['Date'].apply(lambda d: int(str(d)[6:]))
# dfTrain['month'] = dfTrain['Date'].apply(lambda d: int(str(d)[3:5]))
# dfTrain['date'] = dfTrain['Date'].apply(lambda d: int(str(d)[:2]))

# dfTrain = pd.merge(dfTrain, dfStore, how='left', left_on=['Store'], right_on=['Store'])

# dfTrain['hasCompetition'] = dfTrain[['year', 'month', 'CompetitionOpenSinceYear', 'CompetitionOpenSinceMonth']]
# 		.apply(lambda y, m, cy, cm: 1 if y >= cy )

# print('printing train data after splitting date')
# print(dfTrain)
# import timeit


# timeit.timeit("preprocessing.ProcessDimensionDf(dfMerged['Date'], 'Date', outputColumns=dfDateColumns, " + 
# 			"funcProcessColumn=preprocessing.SplitDateIntoDayMonthYear2, funcProcessColumnArgs=('YYYY/MM/DD'))", "import train2")
# run this on mac
dfDate = preprocessing.ProcessDimensionDf(dfTrain['Date'], 'Date', outputColumns=dfDateColumns, 
	funcProcessColumn=preprocessing.SplitDateIntoDayMonthYear2, funcProcessColumnArgs=('YYYY-MM-DD'))
#run this on windows. not sure why this happens.
# dfDate = preprocessing.ProcessDimensionDf(dfTrain['Date'], 'Date', outputColumns=dfDateColumns, 
# 	funcProcessColumn=preprocessing.SplitDateIntoDayMonthYear2, funcProcessColumnArgs=('DD/MM/YYYY'))
dfDate.info()
# print(dfDate)
dateColumns = ['year', 'month', 'date']
print("One hot encoding date: ")
for categories in dateColumns:
	dfDateOHE = preprocessing.OneHotEncodeColumn(dfDate, categories, True)
# print(dfDateOHE)

categoricalColumns = ['Assortment', 'StoreType'];
print("One hot encoding categorical variables: " + str(categoricalColumns))
for categories in categoricalColumns:
	dfStore = preprocessing.OneHotEncodeColumn(dfStore, categories)
	categoricalVariables.append(categories)
# print(dfStore)

print("One hot encoding categorical variables: PromoInterval")
dfStore = preprocessing.OneHotEncodeColumn(dfStore, 'PromoInterval')
# print(dfStore)

print("One hot encoding categorical variables: DayOfWeek, StateHoliday")
for categories in ['DayOfWeek', 'StateHoliday']:
	dfTrain = preprocessing.OneHotEncodeColumn(dfTrain, categories)
# print(dfTrain)

dfMerged = pd.merge(dfTrain, dfStore, how='left', left_on=['Store'], right_on=['Store'])
dfMerged = pd.merge(dfMerged, dfDate, how='left', left_on=['Date'], right_index=True)
print("\n\nMerged sample data: ")
# print(dfMerged)
# print(dfMerged.info())
# print(dfMerged.describe())

dfMerged['Promo2Running'] = (dfMerged['year'].astype(int) > dfMerged['Promo2SinceYear']).astype(int)
# print(dfMerged[['Date', 'year', 'month', 'Store', 'Promo2', 'Promo2SinceWeek', 'Promo2SinceYear', 'Promo2StartMonth', 'Promo2Running']])
dfMerged['HasCompetition'] = ((dfMerged['year'].astype(int) > dfMerged['CompetitionOpenSinceYear']) | 
		((dfMerged['year'].astype(int) == dfMerged['CompetitionOpenSinceYear']) & dfMerged['month'] > dfMerged['CompetitionOpenSinceMonth'])).astype(int)

weeksPerMonth = 52 / 12
dfMerged['Promo2StartMonth'] = dfMerged['Promo2SinceWeek'].map(lambda x: math.ceil(x / weeksPerMonth))
dfMerged['Promo2Running'] = (dfMerged['Promo2Running'] | (dfMerged['year'].astype(int) == dfMerged['Promo2SinceYear'].astype(int)) & 
		(dfMerged['Promo2StartMonth'] >= dfMerged['month'].astype(int))).astype(int)

dfMerged['CompetitionOpenDuration'] = (dfMerged['CompetitionOpenSinceYear'] < 99999).astype(int) * (dfMerged['year'].astype(int) - dfMerged['CompetitionOpenSinceYear'])
dfCheck = dfMerged[['Date', 'year', 'month', 'Store', 'Promo2', 'Promo2SinceWeek', 'Promo2SinceYear', 'Promo2StartMonth', 'Promo2Running', 
'CompetitionOpenSinceYear', 'CompetitionOpenSinceMonth', 'CompetitionOpenDuration']]
print(dfCheck)

print("Analysing merged df: ")
print(preprocessing.AnalyseDfForNaN(dfMerged))

# print(dfMerged['Store'])

# training code
dfTrain_Y = dfMerged['Sales']
del dfMerged['Sales']
dfTrain_X = dfMerged[:0.8*len(dfMerged)]













