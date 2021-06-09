import requests
import os
from dotenv import load_dotenv
from pprint import pprint
import json

# LOAD ENVIRONMENT VARIABLES
load_dotenv()

# VARIABLES
baseURL = "https://maps.googleapis.com/maps/api/place/textsearch/json"
API_KEY = os.getenv("API_KEY")
city = "Périgueux"
business = "hotels"
resp = requests.get(f"{baseURL}?query={business}+in+{city}&key={API_KEY}")
results = resp.json()["results"]
resultsArray = []
counter = 0

for result in results:
    resultsArray.append(result)
    counter += 1


# WRITE TO JSON FILE
with open('results.json', 'a+') as res:
    # res.write(str(resultsArray))
    json.dump(resultsArray, res)

print(f'{counter} items in the results')
print("DONE! ✅")
