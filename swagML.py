class VanillaANN:
	def __init__(self, layers):
		if layers is None:
			self.numberOfLayers = 0
		else 
			self.numberOfLayers = len(layers)


# problem specific preprocessing function
def CalculateCompetitionOpenDuration(year, month, currentYear, currentMonth):
	try:
		y = int(year)
		month = int(month)
		cy = int(currentYear)
		cmonth = int(currentMonth)

	except ValueError:
		print("Invalid non-numeric year and month encountered: " + str(year) + ", " + str(month) 
			+ ", " + str(currentYear) + ", " + str(currentMonth) )
		return None

	
