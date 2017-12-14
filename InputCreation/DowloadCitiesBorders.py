import sys
import os
p = os.path.abspath('..')
sys.path.append(p+"/")
## p = /home/michele/Scrivania/MySym ##

import requests
import json
import pprint
import codecs


def downloadCityBoarders():
    r = requests.get("http://www.car2go.com/api/v2.1/locations?oauth_consumer_key=polito&format=json")

    citiedBorders = json.loads(r.content)
    citiedBorders = citiedBorders["location"]

    d = {}

    for i in range(0, len(citiedBorders)):
        coordsDict ={"lowerRight":
                        { "lat": citiedBorders[i]["mapSection"]["lowerRight"]["latitude"],
                          "lon": citiedBorders[i]["mapSection"]["lowerRight"]["longitude"]
                        },
                     "upperLeft":
                         { "lat": citiedBorders[i]["mapSection"]["upperLeft"]["latitude"],
                           "lon": citiedBorders[i]["mapSection"]["upperLeft"]["longitude"]
                         }
                     }

        d[citiedBorders[i]["locationName"]] = coordsDict
    return d

def downloadCityBoardersFromOperationAreas():
    cities = downloadCityBoarders()

    operativeAreasExtremes = {}
    f = codecs.open(p+"/input/car2go_oper_areas_limits.csv", "w", "utf-8")
    f.write("city,maxLat,maxLon,minLat,minLon\n")

    for k in cities.keys():
        # k = "torino"
        r = requests.get("http://www.car2go.com/api/v2.1/operationareas?oauth_consumer_key=polito&loc="+k+"&format=json")
        zonesDict = json.loads(r.content)
        zonesList = zonesDict ["placemarks"]

        maxLat = None
        maxLon = None
        minLat = 2000
        minLon = 2000
        for i in range(len(zonesList)):
            coordinates = zonesList[i]["coordinates"]
            lonList = []
            latList = []
            for j in range(0, len(coordinates), 3):
                lonList.append(coordinates[j])

                latList.append(coordinates[j+1])

            if maxLat < max(latList):
                maxLat = max(latList)

            if minLat > min(latList):
                minLat = min(latList)

            if maxLon < max(lonList):
                maxLon = max(lonList)

            if minLon > min(lonList):
                minLon = min(lonList)

        operativeAreasExtremes[k] = {"maxLat":maxLat, "maxLon":maxLon, "minLat":minLat, "minLon":minLon}
        # myStr =  k + "," + str(maxLat) + "," + str(maxLon)  + "," + str(minLat) + "," + str(minLon)+ "\n"
        # myStr = myStr.encode("utf-8")
        f.write(k + "," + str(maxLat) + "," + str(maxLon)  + "," + str(minLat) + "," + str(minLon)+ "\n")



    return operativeAreasExtremes