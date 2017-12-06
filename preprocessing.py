import pandas

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

def SplitDateIntoDayMonthYear(df, columnName, dateFormat):
	if (dateFormat.upper() == "YYYY/MM/DD" or dateFormat.upper() == "YYYY-MM-DD"):
		d = dateFormat.split('/')
		split = ''

		if (len(d) == 3):
			# date format is yyyy/mm/dd
			split = '/'
			#year = int(d[0])
			#month = int(d[1])
			#date = int(d[2])
			#validFormat = true

		else:
			d = dateFormat.split('-')
			if (len(d) == 3):
				# date format is yyyy-mm-dd
				split = '-'
				#year = int(d[0])
				#month = int(d[1])
				#date = int(d[2])
				#validFormat = true

		if (split is not ''):
			print(df.loc[0, columnName].split(split))
			df[columnName + "_year"] = (df[columnName].str.split(split))[0]
			#for i, row in df.T.iteritems():

				#df.loc[i, columnName + "_year"] = 
				#df[columnName + "_month"]

	print(df)

def SplitDateIntoDayMonthYear2(row, columnName, dateFormat):

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
			d = row[columnName].split(split)
			columns = pandas.Series({columnName + "_year": d[0], columnName + "_month": d[1], columnName + "_date": d[2] })
			return columns
			