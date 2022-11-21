# importing the requests library
import requests

def IsPolice(nummerplade):
    # api-endpoint
    URL = "https://localhost:7196/api/insurance/plade/"
    
    # sending get request and saving the response as response object
    response = requests.post(url = URL+nummerplade, verify=False)
    resp_dict = response.json()

    return resp_dict.get('is_police_vehicle')