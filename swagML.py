import sklearn

# testArr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# shuffled = sklearn.utils.shuffle(testArr)

# print(testArr)
# print(shuffled)

def Shuffle(df):
	result = None
	try: 
		if df is not None:
			result = sklearn.utils.shuffle(df)
		
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