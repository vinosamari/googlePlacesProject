from getAllPlaces import getAllPlaces
from getSpecificPlace import getSpecificPlace
from getMunicipalities import allMunicipalities
import json

CATEGORIES = ["à domicile",
              "esthéticien/esthéticienne",
              "Salon de manucure",
              "Coach"]

ALL_MUNICIPALITIES = allMunicipalities()
# print(ALL_MUNICIPALITIES)
for municipality in ALL_MUNICIPALITIES:
    print()
    print(f"➡️ ➡️ ➡️ Fetching results for {municipality}")
    print()
    for category in CATEGORIES:
        print()
        print(f"➡️ ➡️ ➡️ Fetching category {category}")
        print()
        # SET QUERY PARAMETERS
        lookFor = CATEGORIES[0]
        location = municipality["name"]
        howManyRequests = 30

        # EXECUTE THE FUNCTIONS TO RUN THE PROGRAM
        mainRequest = getAllPlaces(lookFor, location, howManyRequests)
        getSpecificPlace(mainRequest)
