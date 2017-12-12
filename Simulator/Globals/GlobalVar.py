'''
Created on 13/nov/2017

@author: dgiordan
'''

import sys
import os
import time
import datetime
import requests
import json


p = os.path.abspath('..')
sys.path.append(p+"/")

availableCities = [
    "vienna", "calgary", "montreal", "toronto", "vancouver", "chongqing","amburgo", "berlino", "francoforte", "monaco","renania",\
    "stoccarda","firenze", "milano", "roma", "torino", "catania", "amsterdam", "madrid", "austin", "columbus", "denver", "new york",\
    "portland", "seattle", "washington"]


def readConfigFile():
    path = os.path.abspath('../../input')
    with open(path+"/config.txt") as f:
        content = f.readlines()

    d={}
    for x in content:
        if len(x) == 0 :
            pass
        else:
            x = x.rstrip()
            line = x.split("=")
            d[line[0]] = line[1]

    d["city"] = d["city"].split(",")
    for city in d["city"]:
        if city not in availableCities:
            print ("No entries for", "city")

    d["provider"] = d["provider"].split(",")

    d["initdate"] = int(time.mktime(datetime.datetime.strptime(d["initdate"], "%Y-%m-%dT%H:%M:%S").timetuple()))
    d["finaldate"] = int(time.mktime(datetime.datetime.strptime(d["finaldate"], "%Y-%m-%dT%H:%M:%S").timetuple()))


    return d

def computeOperativeArea(city):
    r = requests.get("http://www.car2go.com/api/v2.1/operationareas?oauth_consumer_key=polito&loc="+city+"&format=json")
    r = request.get("https://www.car2go.com/api/v2.1/locations?oauth_consumer_key=polito&format=json")

    return r.content


d = readConfigFile()
print (d)

city=d["city"]
provider = d["provider"]
initTimeStamp = d["initdate"]
finalTimeStamp = d["finaldate"]

myStr = computeOperativeArea(city[0])
myStr = json.loads(myStr)
myStr = myStr["placemarks"][0]["coordinates"]

lons =[]
lats =[]

for i in range(0, len(myStr), 3):
    lons.append(myStr[i])
    lats.append(myStr[i+1])

print ("minLons:", min(lons), "maxLons", max(lons))
print ("minLats:", min(lats), "maxLats", max(lats))
exit(11)


minLon = 7.598078
MaxLon = 7.731860
minLat = 45.007341
MaxLat = 45.109600

CaselleCentralLat = 45.18843
CaselleCentralLon = 7.6435


CorrectiveFactor = 1#.88


shiftLat500m = 0.0045
shiftLon500m = 0.00637

'''
add /2 in order to have a zonization 250x250
'''
shiftLat250m = shiftLat500m
shiftLon250m = shiftLon500m


NColumns = int((MaxLon-minLon)/shiftLon250m)
Nrows = int((MaxLat-minLat)/shiftLat250m)
MaxIndex = Nrows*NColumns-1


ShiftLon = (MaxLon-minLon)/NColumns
ShiftLat = (MaxLat-minLat)/Nrows


'''
add /2 in order to have a zonization 250x250
'''
CaselleMaxLat = CaselleCentralLat + ShiftLat
CaselleMaxLon = CaselleCentralLon + ShiftLon
CaselleminLat = CaselleCentralLat - ShiftLat
CaselleminLon = CaselleCentralLon + ShiftLon

provider="enjoy"

initDataSet = "###initDataSet###"

