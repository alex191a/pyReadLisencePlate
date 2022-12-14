# importing the requests library
import requests

from lib import config
from lib import randomLocation

# check_api_status
def check_api_status():
	
	# return object
	returnObject = {
		"success": False,
		"status": ""
	}

	try:
		# api-endpoint
		URL_API = config.config["api"]["url"] + "ping"

		# sending get request and saving the response as response object
		response = requests.get(url = URL_API, verify=False)

		# Check status code
		if response.status_code != 200:
			returnObject["success"] = False
			returnObject["status"] =  f"{response.status_code} - {response.reason}"
			return returnObject

		# Decode response		
		resp_dict = response.json()

		# Update return object
		returnObject["success"] = resp_dict.get('success') or False
		returnObject["status"] = resp_dict.get('status') or ""

		# Print insurance
		# print(resp_dict['insurance']['selskab'])
	except Exception as e:

		# Print
		print(str(e))

		# Update return object
		returnObject["success"] = False
		returnObject["status"] = str(e)

		return returnObject

	except:

		# Print error
		print("Error in API call")

		# Update return object
		returnObject["success"] = False
		returnObject["status"] = "Error in API call"

		return returnObject

	return returnObject

def IsPolice(nummerplade, mail):

	# return object
	returnObject = {
		"success": False,
		"IsPolice": False,
		"status": ""
	}

	try:
		# api-endpoint
		URL_API = config.config["api"]["url"] + "insurance/plade/"
		URL_FULL = URL_API + nummerplade

		# Random coordinates
		randomLoc = randomLocation.RandomLocationDenmark()

		postData = {
			"location": {
				"x": randomLoc["x"].__str__(),
				"y": randomLoc["y"].__str__()
			},
			"email": "jona674j@edu.mercantec.dk"
		}

		print(randomLoc["x"], randomLoc["y"])

		# sending get request and saving the response as response object
		response = requests.post(url = URL_FULL, verify=False, json={ "location": { "x": randomLoc["x"].__str__(), "y": randomLoc["y"].__str__() }, "email": mail })
		resp_dict = response.json()

		# Check if success
		# Check status code
		if response.status_code != 200:
			print(resp_dict)
			returnObject["status"] = f"{response.status_code} - {response.reason} - {resp_dict.get('status')}"
			returnObject["success"] = False
			return returnObject

		# update return object
		# Update return object
		returnObject["success"] = True
		returnObject["IsPolice"] = resp_dict.get('is_police_vehicle') or False
		returnObject["status"] = resp_dict.get('status') or ""

		# Print insurance
		# print(resp_dict['insurance']['selskab'])
	except Exception as e:

		# Print
		print(str(e))

		# Update return object
		returnObject["success"] = False
		returnObject["status"] = str(e)
	except:

		# Print error
		print("Error in API call")

		# Update return object
		returnObject["success"] = False
		returnObject["IsPolice"] = False
		returnObject["status"] = "Error in API call"

	return returnObject