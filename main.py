#  IMPORTS
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
city = "Lagos"
business = "schools"

# GET THE FIRST PAGE (20 RESULTS)
pageOne = requests.get(
    f"{baseURL}?query={business}+in+{city}&key={API_KEY}")
pageOneResults = pageOne.json()["results"]

# GET THE NEXT PAGE'S TOKEN
nextPageToken = pageOne.json()["next_page_token"]

resultsArray = []
counter = 0

# ADD RESULTS TO ARRAY
for result in pageOneResults:
    resultsArray.append(result)
    counter += 1

# RECURSIVELY CHECK FOR THE NEXT PAGE


def getNextPage(pageToken):
    # check if the page has a next_page_token
    # fetch the next page results with the token
    # add it to the json file
    # increment the counter
    # else do nothing. i guess.
    pass


if nextPageToken:
    print()
    print("Next Page")
    print()
    nextPage = requests.get(
        f"{baseURL}?query={business}+in+{city}&pagetoken={nextPageToken}&key={API_KEY}")
    nextPageResults = nextPage.json()["results"]
    # pprint(nextPage.json())
    for result in pageOneResults:
        resultsArray.append(result)
        counter += 1


# WRITE TO JSON FILE
with open('results.json', 'a+') as res:
    json.dump(resultsArray, res)

print(f'{counter} items in the results')
print("DONE! ✅")
