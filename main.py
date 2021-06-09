#  IMPORTS
import json
import os
import time
from pprint import pprint

import requests
from dotenv import load_dotenv

# LOAD ENVIRONMENT VARIABLES FROM .env
load_dotenv()

# VARIABLES
baseURL = "https://maps.googleapis.com/maps/api/place/textsearch/json"
API_KEY = os.getenv("API_KEY")
resultsArray = []
numberOfQueries = 6
counter = 0
page = 0


# QUERY PARAMS
category = "a domicile"
location = "Prigonrieux"


# REQUEST TIME
requestTime = time.perf_counter()


# GET THE FIRST PAGE (20 RESULTS)
currentPage = requests.get(
    f"{baseURL}?query={category}+in+{location}&key={API_KEY}")
currentPageResults = currentPage.json()["results"]

print("✈️ Fetching First Page")
page += 1

for result in currentPageResults:
    resultsArray.append(result)
    counter += 1
print("✅ Done Fetching First Page")

#  GET SUBSEQUENT PAGES BASED ON LIST OF QUERIES

for i in range(numberOfQueries):
    page += 1
    print(f"✈️ Fetching Page: {page}")

    if currentPage.json()["next_page_token"]:
        nextPageToken = currentPage.json()["next_page_token"]
        nextPage = requests.get(
            f"{baseURL}?query={category}+in+{location}&pagetoken={nextPageToken}&key={API_KEY}")
        nextPageResults = nextPage.json()["results"]

        # ADD RESULTS TO ARRAY
        for result in nextPageResults:
            resultsArray.append(result)
            counter += 1

    else:
        print("❌ No Other Pages Available")

print(f"✅ Done Fetching All {page} Pages")

#  GET ALL THE PLACES IN THE LOCATION (PLACES FROM ALL PAGES)
print("✈️ Fetching All Places")
placeData = {}
with open('Search.json', 'a') as f:
    for place in resultsArray:
        placeData["Name"] = place.get("name")
        placeData["ID"] = place.get("place_id")
        placeData["Address"] = place.get("formatted_address")
        placeData["Rating"] = place.get("rating")
        json.dump(placeData, f)


print(f"✅ Done Stacking All {len(resultsArray)} Places")


# RESPONSE TIME
responseTime = time.perf_counter()

print(f"finished in {responseTime - requestTime:.2f}s")
print("✅ Done!")
