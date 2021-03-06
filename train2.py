import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import preprocessing
import math
import os 
import tensorflow as tf
import sklearn as sk
import swagML as sml

# data files available for training
# train.csv, store.csv

# locations of data files
pd.set_option('display.max_columns', 999)
root = os.path.dirname(os.path.realpath(__file__))
storeFileDir = os.path.join(root, "data", "store.csv")
trainFileDir = os.path.join(root, "data", "train.csv")
testFileDir = os.path.join(root, "data", "test.csv")

print ("root directory: " + root)
print ("file location (store): " + storeFileDir)
print ("file location (train): " + trainFileDir)
print ("file location (test): " + testFileDir)

dfStore = pd.read_csv(storeFileDir, dtype={'Store': str, 'StoreType': str, 'Assortment': str, 'PromoInterval': str})
dfTrain = pd.read_csv(trainFileDir, dtype={'Store': str, 'Date': str})
dfTest = pd.read_csv(testFileDir)

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

print("Train sample data: \n\n")
dfTest.info()
print(dfTest.describe())
print(dfTest.head(10))

print("Analysing train df: ")
print(preprocessing.AnalyseDfForNaN(dfTrain))

print("Analysing store df: ")
print(preprocessing.AnalyseDfForNaN(dfStore))

print("Analysing test df: ")
print(preprocessing.AnalyseDfForNaN(dfTest))

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
	categoricalVariables.append(categories)
# print(dfDateOHE)

categoricalColumns = ['Assortment', 'StoreType'];
print("One hot encoding categorical variables: " + str(categoricalColumns))
for categories in categoricalColumns:
	dfStore = preprocessing.OneHotEncodeColumn(dfStore, categories)
	categoricalVariables.append(categories)
# print(dfStore)

print("One hot encoding categorical variables: PromoInterval")
dfStore = preprocessing.OneHotEncodeColumn(dfStore, 'PromoInterval')
categoricalVariables.append('PromoInterval')
# print(dfStore)

print("One hot encoding categorical variables: DayOfWeek, StateHoliday")
for categories in ['DayOfWeek', 'StateHoliday']:
	dfTrain = preprocessing.OneHotEncodeColumn(dfTrain, categories)
	categoricalVariables.append(categories)
# print(dfTrain)

dfMerged = pd.merge(dfTrain, dfStore, how='left', left_on=['Store'], right_on=['Store'])
dfMerged = pd.merge(dfMerged, dfDate, how='left', left_on=['Date'], right_index=True)
# print("\n\nMerged sample data: ")
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

dfMerged['CompetitionOpenDuration'] = ((dfMerged['year'].astype(int) >= dfMerged['CompetitionOpenSinceYear']).astype(int) * (dfMerged['year'].astype(int) - dfMerged['CompetitionOpenSinceYear'])).astype(int)
dfCheck = dfMerged[['Date', 'year', 'month', 'Store', 'Promo2', 'Promo2SinceWeek', 'Promo2SinceYear', 'Promo2StartMonth', 'Promo2Running', 
'CompetitionOpenSinceYear', 'CompetitionOpenSinceMonth', 'CompetitionOpenDuration']]
# print(dfCheck)
# print(dfMerged)
# print("Analysing merged df: ")
# print(preprocessing.AnalyseDfForNaN(dfMerged))

# print(dfMerged['Store'])

# training code
seed = 128
epochs = 5
batchSize = 1000
trainingSampleSize = int(0.8*dfMerged.shape[0])
numberOfBatches = math.ceil(trainingSampleSize / batchSize)
dfTrain = dfMerged[:trainingSampleSize]
batch_inteval = math.ceil(0.2 * numberOfBatches)

dfValidation_X = dfMerged[trainingSampleSize:]
dfValidation_Y = dfValidation_X['Sales']

for i in categoricalVariables:
	del dfTrain[i]
	del dfValidation_X[i]

del dfTrain['Date']
del dfTrain['Customers']
del dfValidation_X['Sales']
del dfValidation_X['Date']
del dfValidation_X['Customers']

validation_x_matrix = dfValidation_X.as_matrix()
validation_y_matrix = dfValidation_Y.as_matrix().reshape((dfValidation_Y.shape[0], 1))

# print("dfTrain_x shape: " + str(dfTrain.shape))
print("training sample size: " + str(trainingSampleSize))
print("validation x shape: {0}".format(validation_x_matrix.shape))
print("validation y shape: {0}".format(validation_y_matrix.shape))
# SetupModel()

print("Setting up model")
# setup tensorflow
input_units = dfTrain.shape[1] - 1
print("input dimension: " + str(input_units))
output_units = 1
number_of_hidden_layers = 4
output_layer_number = number_of_hidden_layers + 1
input_batch_size = 500
layer_units_size = [input_units, 50, 40, 30, 20, output_units]
learning_rate = 0.005

# define input and required output
# x = tf.placeholder(tf.float32, [input_batch_size, layer_units_size[0]])
# y = tf.placeholder(tf.float32, [input_batch_size])

x = tf.placeholder(tf.float32, [None, layer_units_size[0]], name='x')
y = tf.placeholder(tf.float32, [None], name='y')

# weights and biases for hidden layers
weights = {}
biases = {}
for i in range(len(layer_units_size) - 1):
	weights[i] = tf.Variable(tf.random_normal([layer_units_size[i], layer_units_size[i + 1]], seed=seed), name='w_' + str(i) + '_' + str(i + 1))
	biases[i] = tf.Variable(tf.random_normal([layer_units_size[i + 1]], seed=seed), name='b_' + str(i) + '_' + str(i + 1))
	print("weights[{0}]- name: {1} shape: {2}".format(i, weights[i].name, tf.shape(weights[i])))
	print("biases[{0}]- name: {1} shape: {2}".format(i, biases[i].name, tf.shape(biases[i])))

# create operation to calculate each hidden layer
layers = {}
# layer 2 (hidden layer 1): input to hidden layer 1
layers[0] = x
# layers[1] = tf.nn.relu(tf.add(tf.matmul(x, weights[1])))
for i in range(len(layer_units_size) - 2):
	layers[i + 1] = tf.nn.relu(tf.add(tf.matmul(layers[i], weights[i]), biases[i]), name='layer' + str(i+1))

# output layer
layers[output_layer_number] = tf.add(tf.matmul(layers[number_of_hidden_layers], weights[number_of_hidden_layers]), biases[number_of_hidden_layers], 
	name='layer' + str(output_layer_number) + '_output')

# loss function - for regression this should be squared loss function
loss = tf.reduce_mean(tf.square(layers[output_layer_number] - y), name='mean_cost')
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(loss)

print("Model setup completed")

# train model
init = tf.global_variables_initializer()
sess = tf.Session()
sess.run(init)

loss_plot = []
validation_result = []
saver = tf.train.Saver()
total_loss = 0
grid = gridspec.GridSpec(epochs + 1, 1)

min_loss = 0
min_epoch = 0
# model_parameters = {}
#plt.plot(range(epochs * trainingSampleSize), loss_plot, label='loss')

# go through the epochs to train model
for i in range(epochs):
	print("------------------------------------------------")
	print("Starting epoch number: " + str(i + 1))

	print("Shuffling data set")
	dfShuffled = sml.Shuffle(dfTrain)
	print("Shuffling completed")

	index = 0
	end = 0
	total_loss = 0
	for j in range(numberOfBatches - 1):

		#print("Creating test and validation sets")
		dfTrain_X = dfShuffled[:trainingSampleSize]
		#print("dfTrain_x shape: " + str(dfShuffled.shape))
		dfTrain_Y = dfTrain_X['Sales']
		del dfTrain_X['Sales']

		# create batch
		# if j == (numberOfBatches - 1):
		# 	end = trainingSampleSize
		# 	print("fetching last batch for this epoch. index = " + str(i))
			
		# else:
			# end = batchSize * (j + 1)
			# print("slice detail: {0}:{1}".format(index, end))
		
		end = batchSize * (j + 1)	
		train_matrix_x = dfTrain_X[index:end].as_matrix()
		train_matrix_y = dfTrain_Y[index:end].as_matrix()
		index = end
		cost_func, l = sess.run([optimizer, loss], feed_dict={x: train_matrix_x, y: train_matrix_y})
		# l = sess.run(loss, feed_dict={x: train_matrix_x, y: train_matrix_y})
		l_sqrt = math.sqrt(l)
		
		total_loss = l_sqrt + total_loss

		if j % batch_inteval == 0:
			print("Progress: {0}\% Completed batch number: {1}".format(str(math.ceil(j/numberOfBatches * 100)), str(i)))
			
		
		if j % 20 == 0:
			print("epoch {0} batch number: {1} loss_sqrt: {2:.2f} avg loss_sqrt: {3:.2f}".format(i + 1, j, l_sqrt, total_loss/(j + 1)))
			loss_plot.append(l_sqrt)
			#plt.plot(range(index), loss_plot, label='loss')

	# test model on validation set
	print("\n\nTesting model on validation set")	
	predicted_validation = sml.Predict(x, validation_x_matrix, sess, layers[output_layer_number])

	print("Shape of actual data structure: {0}".format(validation_y_matrix.shape))
	print("Shape of prediction data structure: {0}".format(predicted_validation.shape))
	rms = sml.EvaluateOutput_Rms(validation_y_matrix, predicted_validation)
	mean1 = sml.EvaluateOutput_Deviation(validation_y_matrix, predicted_validation)

	result = "end of epoch: {0} rms: {1:.2f}".format(i + 1, rms)
	validation_result.append(result)
	result = "end of epoch: {0} mean1: {1:.2f}".format(i + 1, mean1)
	validation_result.append(result)


	# save weights and biases of this epoch
	if rms < min_loss:
		min_loss = rms
		min_epoch = i + 1


	print("\n\nPrinting validation set summary: ")
	for k in range(len(validation_result)):
		print(validation_result[k])

	# save model to disk
	if i > 0:
		# model saved before so do not need meta file
		#saver.save(sess, 'model_dump/rossman-model', global_step=(i + 1), write_meta_graph=False)
		saver.save(sess, 'model_dump/rossman-model', global_step=(i + 1))
	else:
		# saving model for the first time
		saver.save(sess, 'model_dump/rossman-model', global_step=(i + 1))

	# add lines to plot
	# plot losses first
	# plt.subplot(2, epochs, [1 epochs])
	plt.subplot(grid[0, 0])
	plt.plot(range(len(loss_plot)), loss_plot, label='loss')
	plt.legend()
	# plot actuals vs prediction
	# plt.subplot(2, epochs, 2 * epochs - (epochs - i))
	plt.subplot(grid[i + 1, 0])
	# plt.plot(range(validation_y_matrix.shape[0]), validation_y_matrix[:,0], label='actual epoch: ' + str(i + 1))
	# plt.plot(range(validation_y_matrix.shape[0]), predicted_validation[:,0], label='predicted epoch: ' + str(i + 1))
	plt.plot(range(1000), validation_y_matrix[:1000,0], label='actual epoch: ' + str(i + 1))
	plt.plot(range(1000), predicted_validation[:1000,0], label='predicted epoch: ' + str(i + 1))
	plt.legend()

	print("\n\nPrinting weights and biases for this epoch: ")
	for i in weights:
		print("weight name: " + weights[i].name)
		print(sess.run(weights[i]))

	for i in biases:
		print("weight name: " + biases[i].name)
		print(sess.run(biases[i]))

print("Training completed!")
print("Best weights to use was found at the end of epoch: " + min_epoch)
sess.close()

# restore best weights
sess = tf.Session()
sess.run(init)
new_saver = tf.train.import_meta_graph('/model_dump/rossman-model-{0}.meta'.format(min_epoch))
print("Restoring weights and biases from epoch: " + str(min_epoch))
new_saver.restore(sess, 'model_dump/rossman-model-' + min_epoch)
print("Model restored")

graph = tf.get_default_graph()
output_op = graph.get_tensor_by_name('layer' + str(output_layer_number) + '_output:0')
x_pred = graph.get_tensor_by_name('x:0')
# y_pred = graph.get_tensor_by_name('y:0')

print("\n\nTesting model on validation set")	
pred = sml.Predict(x_pred, validation_x_matrix, sess, output_op)

print("Shape of actual data structure: {0}".format(validation_y_matrix.shape))
print("Shape of prediction data structure: {0}".format(pred.shape))
rms = sml.EvaluateOutput_Rms(validation_y_matrix, pred)
mean1 = sml.EvaluateOutput_Deviation(validation_y_matrix, pred)

result = "end of epoch: {0} rms: {1:.2f}".format(i + 1, rms)
print(result)
result = "end of epoch: {0} mean1: {1:.2f}".format(i + 1, mean1)
print(result)


print("------------------------------------------------")
# plt.show()



def SetupModel():
	print("Setting up model")
	# setup tensorflow
	input_units = dfTrain_X.shape[1] 
	output_units = 1
	number_of_hidden_layers = 4
	output_layer_number = number_of_hidden_layers + 1
	input_batch_size = 500
	layer_units_size = [input_units, 50, 40, 30, 20, output_units]
	learning_rate = 0.01

	# define input and required output
	x = tf.placeholder(tf.float32, [input_batch_size, layer_units_size[0]])
	y = tf.placeholder(tf.float32, [input_batch_size])
	
	# weights and biases for hidden layers
	weights = {}
	biases = {}
	for i in range(len(layer_units_size)):
		weights[i] = tf.Variable(tf.random_normal([layer_units_size[i], layer_units_size[i + 1]], seed=seed), name='w_' + str(i) + '_' + str(i + 1))
		biases[i] = tf.Variable(tf.random_normal(layer_units_size[i], seed=seed), name='b_' + str(i) + '_' + str(i + 1))

	# create operation to calculate each hidden layer
	layers = {}
	# layer 2 (hidden layer 1): input to hidden layer 1
	layers[0] = x
	# layers[1] = tf.nn.relu(tf.add(tf.matmul(x, weights[1])))
	for i in range(len(layer_units_size) - 1):
		layers[i + 1] = tf.nn.relu(tf.add(tf.matmul(layers[i], weights[i]), biases[i]))

	# output layer
	layers[output_layer_number] = tf.add(tf.matmul(layers[number_of_hidden_layers], weights[number_of_hidden_layers]), biases[number_of_hidden_layers])

	# loss function - for regression this should be squared loss function
	loss = tf.reduce_mean(tf.square(layers[output_layer_number] - y), name='mean_cost')
	optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(loss)

	print("Model setup completed")




