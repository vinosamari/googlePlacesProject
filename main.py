#  IMPORTS
import json
import os
from pprint import pprint
from googleplaces import GooglePlaces
import requests
from dotenv import load_dotenv

# LOAD ENVIRONMENT VARIABLES
load_dotenv()

# VARIABLES
API_KEY = os.getenv("API_KEY")
google_places = GooglePlaces(API_KEY)
hasNextPageToken = False
textQuery = 'studio in Abuja'
resultsArray = []
currentPageResults = google_places.text_search(query=textQuery)

#  CHECK FOR NEXT PAGE
if currentPageResults.has_next_page_token:
    nextPageResults = google_places.text_search(
        query=textQuery, pagetoken=currentPageResults.next_page_token)
# DISPLAY NEXT PAGE
pprint(currentPageResults.places)
pprint(nextPageResults.places)
