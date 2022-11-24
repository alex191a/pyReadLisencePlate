# importing the requests library
import requests

from lib import config

def IsPolice(nummerplade):

	# return object
	returnObject = {
		"success": False,
		"IsPolice": False,
		"status": ""
	}

	try:
		# api-endpoint
		URL_API = config.config["api"]["url"]
		URL_FULL = URL_API + nummerplade

		# sending get request and saving the response as response object
		response = requests.post(url = URL_FULL, verify=False, json={ "location": "Arhus", "email": "jona674j@edu.mercantec.dk" })
		resp_dict = response.json()

		# Check if success
		# Check status code
		if response.status_code != 200:
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