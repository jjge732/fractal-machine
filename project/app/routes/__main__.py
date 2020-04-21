from aws import API

print(API.retrieveListOfImageNames())
API.retrieveImage("fractal-3x3.svg")
API.storeImage("fractal-3x3.svg")