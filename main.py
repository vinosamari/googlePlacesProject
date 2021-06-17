#  IMPORTS
import json
import os
import time
from pprint import pprint

import requests
from dotenv import load_dotenv
from tqdm import tqdm

# LOAD ENVIRONMENT VARIABLES FROM .env
load_dotenv()

CATEGORIES = ["à domicile",
              "esthéticien/esthéticienne",
              "Salon de manucure",
              "Coach"]

# GET ALL THE MUNICIPALITIES FROM THE JSON FILE & STORE IN AN ARRAY
def getAllMunicipalities():
    ALL_MUNICIPALITIES = []

    with open("municipalities.json") as f:
        allMunicipalities = json.load(f)["list_of_municipalities"]
        arrayCopy = ALL_MUNICIPALITIES.copy()
        for item in allMunicipalities:
            arrayCopy.append(item)
        ALL_MUNICIPALITIES = arrayCopy
    return ALL_MUNICIPALITIES
MUNICIPALITIES = getAllMunicipalities()

#  MAIN FUNCTION 
def main(queryCategory, queryLocation, queryLimit):
    # VARIABLES
    baseURL = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    API_KEY = os.getenv("API_KEY")
    resultsArray = []
    page = 0
    counter = 0
    noWebsiteResultsCount = 0

    # QUERY PARAMS
    category = queryCategory
    location = queryLocation
    numberOfQueries = queryLimit

    # GET ALL PAGE RESULTS FROM THE SEARCH QUERY (MUNICIPALITIES)

    # GET THE FIRST PAGE (~20 RESULTS)
    currentPage = requests.get(f"{baseURL}?query={category}+in+{location}&key={API_KEY}")
    currentPageResults = currentPage.json()["results"]
    print("✈️  Fetching First Page")
    page += 1
    for result in tqdm(currentPageResults):
        resultsArray.append(result)
        counter += 1
    print("✅  Done Fetching First Page")

    #  GET SUBSEQUENT PAGES BASED ON NUMBER OF QUERIES(2 QUERIES WILL GIVE YOU 3 PAGES OF RESULT i.e Page 1 + Next 2 Pages )
    for i in tqdm(range(numberOfQueries)):
        page += 1
        # print(f"✈️ Fetching Page: {page}")
        # TRY TO GET THE PAGE TOKEN IF IT IS AVAILABLE
        try:
            if currentPage.json()["next_page_token"]:
                nextPageToken = currentPage.json()["next_page_token"]
            nextPage = requests.get(f"{baseURL}?query={category}+in+{location}&pagetoken={nextPageToken}&key={API_KEY}")
            nextPageResults = nextPage.json()["results"]

            # ADD RESULTS TO ARRAY
            for result in nextPageResults:
                resultsArray.append(result)
                counter += 1
        except Exception:
            print("❌ No Other Pages Available")
            break
    print(f"✅ Done Fetching All {page} Pages")

    #  GET ALL THE PLACES IN THE LOCATION (PLACES FROM ALL PAGES)
    print("✈️ Fetching All Places From Page Results")
    placeData = {}
    placeDataArray = []
    with open('AllPlacesResults.json', 'a') as f:
        # MAKE A COPY OF newPlaceDataArray
        newPlaceDataArray = placeDataArray.copy()
        for place in tqdm(resultsArray):
            placeData["Name"] = place.get("name")
            placeData["ID"] = place.get("place_id")
            placeData["Address"] = place.get("formatted_address")
            placeData["Rating"] = place.get("rating")
            placeData["Types"] = place.get("types")
            newPlaceDataArray.append(placeData)
            placeData = {}
        # OVERWIRTE THE DETAILS OF THE ORIGINAL ARRAY WITH THE COPY
        placeDataArray = newPlaceDataArray
        # WRITE TO THE JSON FILE
        json.dump(placeDataArray, f, indent=2)

    # print(f"✅ Done Stacking All {len(resultsArray)} Places in Search.json")

    print(f"finished Getting All Places")
    # print("✅ Done!")

    # VARIABLES FOR PLACE
    allPlacesArray = placeDataArray
    placeId = ''
    placeDetailData = {}
    placesDetailsArray = []

    # GET PLACE ID FROM THE PLACES IN allPlacesArray
    with open('NoWebsiteUrlResults.json', 'a+', "utf-8") as f:
        detailsArrayCopy = placesDetailsArray.copy()
        for place in tqdm(allPlacesArray):
            counter += 1
            placeId = place["ID"]
            baseURL2 = "https://maps.googleapis.com/maps/api/place/details/json"

            # GET THE PLACE DETAIL
            placeDetail = requests.get(f"{baseURL2}?place_id={placeId}&key={API_KEY}")
            # print(placeDetail.status_code)
            placeDetailResult = placeDetail.json()["result"]
            placeName = placeDetailResult["name"]
            addressComponents = placeDetailResult["address_components"]
            placeHasWebsite = placeDetailResult.get("website", False)
            if placeHasWebsite:
                # print(f"✅ --> {placeName} has a website at: {placeHasWebsite}.")
                # print()
                pass

            else:
                # print(f"❌ --> {placeName} has no website.")
                # print()
                noWebsiteResultsCount += 1
                # GET THE CITY NAME
                for component in addressComponents:
                    firstComponentType = component["types"][0]
                    if firstComponentType == "locality":
                        placeDetailData['City'] = component["long_name"]
                        cityName = component["long_name"]

                # POPULATE THE PLACE DETAIL DICTIONARY
                placeDetailData['Name'] = placeDetailResult["name"]
                placeDetailData['Address'] = placeDetailResult.get("formatted_address", "")
                placeDetailData['Phone_Number'] = placeDetailResult.get("formatted_phone_number", "")
                placeDetailData['International_Phone_Number'] = placeDetailResult.get("international_phone_number", "")
                placeDetailData['Website_Url'] = ""
                placeDetailData['Average_Rating'] = placeDetailResult.get("rating", "Not Available")
                placeDetailData['Number_of_Reviews'] = len(placeDetailResult.get("reviews", ""))
                placeDetailData['Business_Category(ies)'] = placeDetailResult["types"]
                for item in MUNICIPALITIES:
                    if cityName == item.get("name"):
                        placeDetailData["Zip_Code"] = item["zip_code"]

                detailsArrayCopy.append(placeDetailData)
                placeDetailData = {}
        placesDetailsArray = detailsArrayCopy
        json.dump(placesDetailsArray, f)

        print(f"{noWebsiteResultsCount} results don't have a website.")
    return print(f"✅ Done! Finished Getting Place Details. Check the NoWebsiteUrlResults.json file")

# RUN THE FUNCTION FOR ALL MUNICIPALITIES AND CATEGORIES
for municipality in tqdm(MUNICIPALITIES):
    # print()
    print(f"➡️ ➡️ ➡️ Fetching results for {municipality}")
    # print()
    for category in tqdm(CATEGORIES):
        # print()
        print(f"➡️ ➡️ ➡️ Fetching category {category}")
        # print()
        # SET QUERY PARAMETERS
        lookFor = CATEGORIES[0]
        location = municipality["name"]
        howManyRequests = 19
        main(lookFor, location, howManyRequests)
    


