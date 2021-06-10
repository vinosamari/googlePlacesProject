from getAllPlaces import getAllPlaces
from getSpecificPlace import getSpecificPlace
import json

CATEGORIES = ["à domicile",
              "esthéticien/esthéticienne",
              "Salon de manucure",
              "Coach"]


# SET QUERY PARAMETERS
lookFor = CATEGORIES[0]
locationZipCode = 'Agonac'
howManyRequests = 2


# EXECUTE THE FUNCTIONS TO RUN THE PROGRAM
mainRequest = getAllPlaces(lookFor, locationZipCode, howManyRequests)
getSpecificPlace(mainRequest)
