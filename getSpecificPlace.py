#  IMPORTS
import json
import os
import time
from pprint import pprint

import requests
from dotenv import load_dotenv
from getAllPlaces import getAllPlaces
from getMunicipalities import allMunicipalities
# LOAD ENVIRONMENT VARIABLES FROM .env
load_dotenv()


def getSpecificPlace(placesArray):

    # VARIABLES
    baseURL = "https://maps.googleapis.com/maps/api/place/details/json"
    API_KEY = os.getenv("API_KEY")
    allPlacesArray = placesArray
    counter = 0
    noWebsiteResultsCount = 0
    MUNICIPALITIES = allMunicipalities()

    # QUERY PARAMS
    placeId = ''

    # REQUEST TIME
    requestTime = time.perf_counter()

    placeDetailData = {}
    placesDetailsArray = []

    # GET PLACE ID FROM THE PLACES IN THE IMPORTED ARRAY
    with open('NoWebsiteUrlResults.txt', 'a+') as f:
        detailsArrayCopy = placesDetailsArray.copy()
        for place in allPlacesArray:
            counter += 1
            placeId = place["ID"]

            # GET THE PLACE DETAIL
            placeDetail = requests.get(f"{baseURL}?place_id={placeId}&key={API_KEY}")
            placeDetailResult = placeDetail.json()["result"]
            placeName = placeDetailResult["name"]
            addressComponents = placeDetailResult["address_components"]
            placeHasWebsite = placeDetailResult.get("website", False)
            if placeHasWebsite:
                print(
                    f"✅ --> {placeName} has a website at: {placeHasWebsite}.")
                print()

            else:
                print(f"❌ --> {placeName} has no website.")
                print()
                noWebsiteResultsCount += 1

                for component in addressComponents:
                    firstComponentType = component["types"][0]
                    if firstComponentType == "locality":
                        placeDetailData['City'] = component["long_name"]
                        cityName = component["long_name"]

                placeDetailData['Name'] = placeDetailResult["name"]
                placeDetailData['Address'] = placeDetailResult.get(
                    "formatted_address", "")
                placeDetailData['Phone_Number'] = placeDetailResult.get(
                    "formatted_phone_number", "")
                placeDetailData['International_Phone_Number'] = placeDetailResult.get(
                    "international_phone_number", "")
                placeDetailData['Website_Url'] = ""
                placeDetailData['Average_Rating'] = placeDetailResult.get(
                    "rating", "Not Available")
                placeDetailData['Number_of_Reviews'] = len(
                    placeDetailResult.get("reviews", ""))
                placeDetailData['Business_Category(ies)'] = placeDetailResult["types"]
                for item in MUNICIPALITIES:
                    # print(cityName)
                    if cityName == item.get("name"):
                        placeDetailData["Zip_Code"] = item["zip_code"]

                detailsArrayCopy.append(placeDetailData)
                placeDetailData = {}
        placesDetailsArray = detailsArrayCopy
        f.write(str(placesDetailsArray))

    # print()
    # print(f"The loop ran {counter} times")
    # print(f"there are {str(len(allPlacesArray))} places in the array")
    # RESPONSE TIME
    responseTime = time.perf_counter()

    print(f"{noWebsiteResultsCount} results don't have a website.")

    return print(f"✅ Done! Finished Getting Place Details in {responseTime - requestTime:.2f}s")
