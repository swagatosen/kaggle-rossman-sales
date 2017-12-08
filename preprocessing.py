import pandas as pd

def OneHotEncodeColumn(df, columnName):
	#find unique categories in data
	#print(df[columnName])
	categories = list(set(df[columnName]))
	#print(categories)

	labels = {}
	for i, category in enumerate(categories):
		df[columnName + "_" + str(i)] = 0
		labels[category] = i

	#print(df)
	#print(labels)

	for i, row in df.T.iteritems():
		#print(df.iloc[i][columnName])
		#print(str(labels[df.iloc[i][columnName]]))
		df.set_value(i, columnName + "_" + str(labels[df.iloc[i][columnName]]), 1)

	#print(df)
	return df

# def SplitDateIntoDayMonthYear(args):
# 	if len(args) == 3:
# 		df = args[0]
# 		columnName = args[1]
# 		dateFormat = args[2]

# 	return SplitDateIntoDayMonthYear(df, columnName, dateFormat)

def ReceiveArgsInArray(argLength):
	def decorator(func):
		def wrapper(data, *args):
			if len(args) == argLength:
				return func(data, *args)
			else:
				return print("The number of arguments accepted by this function does not match. Function accepts {0} arguments.".format(argLength))
		return wrapper
	return decorator

@ReceiveArgsInArray(2)
def SplitDateIntoDayMonthYear(df, columnName, dateFormat):
	if df is not None:
		if (dateFormat.upper() == "YYYY/MM/DD" or dateFormat.upper() == "YYYY-MM-DD"):
			d = dateFormat.split('/')
			split = ''

			if (len(d) == 3):
				# date format is yyyy/mm/dd
				split = '/'

			else:
				d = dateFormat.split('-')
				if (len(d) == 3):
					# date format is yyyy-mm-dd
					split = '-'


			if (split != ''):
				for i, row in df.T.iteritems():
				# print(df.loc[0, columnName].split(split))
					d = df.loc[i, columnName].split(split)
					df.at[i, columnName + "_year"] = d[0]
					df.at[i, columnName + "_month"] = d[1]
					df.at[i, columnName + "_date"] = d[2]


		print(df)

ReceiveArgsInArray(1)
def SplitDateIntoDayMonthYear2(date, dateFormat):
	try:
		if (dateFormat.upper() == "YYYY/MM/DD" or dateFormat.upper() == "YYYY-MM-DD"):
			d = dateFormat.split('/')
			split = ''

			if (len(d) == 3):
				# date format is yyyy/mm/dd
				split = '/'

			else:
				d = dateFormat.split('-')
				if (len(d) == 3):
					# date format is yyyy-mm-dd
					split = '-'

			if (split != ''):
				d = date.split(split)
				assert len(d) == 3

				# columns = pandas.Series({columnName + "_year": d[0], columnName + "_month": d[1], columnName + "_date": d[2] })
				# print(columns)
				# return columns
				return [d[0], d[1], d[2]]

	except AssertionError:
		print("Test failed in SplitDateIntoDayMonthYear2. d: ")
		print(d)
		print("split: " + split)

def CreateEmptyMonthColumns(df, display="number"):
	if display == "name":
		names = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dev']
		for name in names:
			df["month_" + name] = 0
	elif display == "number":
		for num in range(1, 13):
			df["month_" + num] = 0

def CreateEmptyDayColumns(df):
	if df is not None:
		for num in range(1, 32):
			df["month_" + num] = 0

def ProcessDimensionDf(column_chunk, columnName, **kwargs):
	if column_chunk is not None:
		output = kwargs.get('output')
		if output is None:
			#create new output df
			dfColumns = kwargs.get('outputColumns')
			if (dfColumns is not None) and (len(dfColumns) > 0):
				print('Creating new df with columns: ' + str(dfColumns))
				output = CreateEmptyDf(columns=dfColumns)
			else:
				print('No output df is provided. Column names for new output is missing as well.')
				return None

		# process column of data now

		func = kwargs.get('funcProcessColumn')
		func_args = kwargs.get('funcProcessColumnArgs')
		if func is not None:
			for i, row in column_chunk.iteritems():
				# try: 
					data = row
					# print(data)
					if not output.index.contains(data):
						#create new row in df with this index
						output.loc[data] = func(data, func_args)
				# except:
				# 	print("column name: " + columnName + " does not exist in this df. Terminating processing.")
				# 	return output
		else:
			print('No function found to process column data. No additional data has been added to output df.')
		
		print(output)
		return output


def CreateEmptyDf(**kwargs):
	columns = kwargs.get('columns')
	if columns is not None:
		output = pd.DataFrame(columns=columns)
		return output
