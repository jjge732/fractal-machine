from aws import API

print(API.retrieveMostRecentImages(5))
API.retrieveImage("fractal-3x3.svg")
API.storeImage("fractal-3x3.svg")