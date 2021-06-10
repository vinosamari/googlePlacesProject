#  IMPORTS
import json
import os
import time
from pprint import pprint

import requests
from dotenv import load_dotenv
from getAllPlaces import getAllPlaces
# LOAD ENVIRONMENT VARIABLES FROM .env
load_dotenv()

# https://maps.googleapis.com/maps/api/place/details/json?place_id=ChIJN1t_tDeuEmsRUsoyG83frY4&fields=name,rating,formatted_phone_number&key=YOUR_API_KEY


# VARIABLES
baseURL = "https://maps.googleapis.com/maps/api/place/details/json"
API_KEY = os.getenv("API_KEY")
allPlacesArray = getAllPlaces('gym', 'Abuja', 4)
counter = 0


# QUERY PARAMS
placeId = ''


# REQUEST TIME
requestTime = time.perf_counter()

# GET PLACE ID FROM THE PLACES IN THE IMPORTED ARRAY
for place in allPlacesArray:
    placeId = place["ID"]

    # GET THE PLACE DETAIL
    placeDetail = requests.get(
        f"{baseURL}?place_id={placeId}&key={API_KEY}")
    placeDetailResult = placeDetail.json()["result"]
    placeName = placeDetailResult["name"]
    placeHasWebsite = placeDetailResult.get("website", False)
    if placeHasWebsite:
        pprint(placeName)
    else:
        print(f"{placeName} has no website")
    # pprint(placeDetailResult.get("website", ""))
# RESPONSE TIME
responseTime = time.perf_counter()

print(f"finished Getting Place Details in {responseTime - requestTime:.2f}s")
print("✅ Done!")
