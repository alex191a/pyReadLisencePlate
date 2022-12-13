import random

# Generate random location in Denmark
def RandomLocationDenmark():

	# Min and max X
	minX = 55.647790
	maxX = 56.844539

	# Min and max Y
	minY = 8.426107
	maxY = 10.162932

	# Random X
	x = random.uniform(minX, maxX)

	# Random Y
	y = random.uniform(minY, maxY)

	# new object with x and y coordinates
	returnObject = {
		"x": x,
		"y": y
	}

	# Return
	return returnObject


