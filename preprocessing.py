import pandas as pd

def OneHotEncodeColumn(df, columnName, useLabelNameForColumn=False, removeCategories=None):
	#find unique categories in data
	# print(df[columnName])
	print("Starting OneHotEncodeColumn for column: " + columnName)
	categories = set(df[columnName])
	print("Categories in column {0}: {1}".format(columnName, str(categories)))
	if removeCategories is not None:
		for key in removeCategories:
			print("remove category: {0} from column: {1}".format(removeCategories[key], columnName))
			if removeCategories[key] in categories:
				print("Found category to be removed before one hot encoding: " + str(removeCategories[key]))
				categories.remove(removeCategories[key])
			else:
				print('Category: [' + key + '] could not be removed. It does not exist in column: ' + columnName)

	
	return OneHotEncodeHelper(df, columnName, useLabelNameForColumn, categories)		
	#print(categories)

	

def OneHotEncodeHelper(df, columnName, useLabelNameForColumn, categories):
	print("Starting OneHotEncodeHelper for column: " + columnName)
	labels = {}
	name = ""
	if useLabelNameForColumn == True:
		for i, category in enumerate(categories):
			name = columnName + "_" + str(category)
			df[name] = 0
			labels[category] = name
	else:
		for i, category in enumerate(categories):
			name = columnName + "_" + str(i)
			df[name] = 0
			labels[category] = name

	for label in labels:
		df[labels[label]] = (df[columnName]==label).astype(int)
	#df[labels[df[columnName]]] = 1
	# d = df.copy()
	# d[columnName].map(lambda x: df[labels[x]] = 1)
	# print("version map")
	# print(d)
	# d = df.copy()
	# d[columnName].apply(lambda x: x[labels[x[columnName]]] = 1)
	# print("version apply 1")
	# print(d)
	# # d = df.copy()
	# df[columnName].apply(lambda x: x[labels[x]] = 1)
	# print("version apply 2")
	# print(df)
	# for i, row in df.T.iteritems():
	# 	#print(df.iloc[i][columnName])
	# 	#print(str(labels[df.iloc[i][columnName]]))
	# 	# print(i)
	# 	df.set_value(i, str(labels[df.loc[i][columnName]]), 1)

	#print(df)
	return df

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

# @ReceiveArgsInArray(1)
def SplitDateIntoDayMonthYear2(date, dateFormat):
	try:
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
			df = dateFormat.upper().split(split)
			# print(dateFormat)
			# print(df)
			year = df.index('YYYY')
			month = df.index('MM')
			dateNumber = df.index('DD')
			# print(str(year) + ',' + str(month) + ',' + str(dateNumber))

			d = date.split(split)
			assert len(d) == 3

			# columns = pandas.Series({columnName + "_year": d[0], columnName + "_month": d[1], columnName + "_date": d[2] })
			# print(columns)
			# return columns
			return [d[year], d[month], d[dateNumber]]

	except AssertionError:
		print("Test failed in SplitDateIntoDayMonthYear2. d: ")
		print(d)
		print("split: " + split)

	except ValueError:
		print('Unable to parse date in SplitDateIntoDayMonthYear2. Date format given not supported.')

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
						# print(func)
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
