from getAllPlaces import getAllPlaces
from getSpecificPlace import getSpecificPlace


CATEGORIES = ["à domicile",
              "esthéticien/esthéticienne",
              "Salon de manucure",
              "Coach"]

# SET QUERY PARAMETERS
lookFor = CATEGORIES[3]
locationZipCode = 'Abjat-sur-Bandiat'
howManyRequests = 5


# EXECUTE THE FUNCTIONS TO RUN THE PROGRAM
mainRequest = getAllPlaces(lookFor, locationZipCode, howManyRequests)
getSpecificPlace(mainRequest)
