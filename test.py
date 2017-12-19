import sklearn

# testArr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# shuffled = sklearn.utils.shuffle(testArr)

# print(testArr)
# print(shuffled)

def shuffleDf(df):
	result = None
	try: 
		if df is not None:
			result = sklearn.utils.shuffle(df)
		
		return result
	except:
		print("Shuffling failed for variable: ")
		print(df)
		return None