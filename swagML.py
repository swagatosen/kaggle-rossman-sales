import sklearn as sk
from sklearn import metrics
import numpy as np

def Shuffle(df):
	result = None
	try: 
		if df is not None:
			result = sk.utils.shuffle(df)
		
		return result
	except:
		print("Shuffling failed for variable: ")
		print(df)
		return None

def TestShuffle(input):
	print("\n\nprinting original df input: ")
	print(input)
	input = input.as_matrix()
	print("\n\nprinting numpy matrix form: ")
	print(input)
	print("\n\nprinting shuffled numpy matrix: ")
	print(Shuffle(input))

def Predict(tf_input, input_data, sess, operation):
	output = sess.run(operation, feed_dict={tf_input: input_data})
	return output

def EvaluateOutput_Rms(y_actual, y_pred):
	mse = metrics.mean_squared_error(y_actual, y_pred)
	rms = np.sqrt(mse)
	return rms

def EvaluateOutput_Deviation(y_actual, y_pred):

	percent_diff = ((y_pred - y_actual) / y_actual) * 100
	print(percent_diff)
	mean_percent_diff1 = (percent_diff.sum(0))/percent_diff.shape[0]
	mean_percent_diff2 = np.mean(percent_diff, axis=0)

	return mean_percent_diff1, mean_percent_diff2