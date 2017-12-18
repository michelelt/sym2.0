import sys
import os
p = os.path.abspath('..')
sys.path.append(p+"/")


import pandas as pd
import time
import datetime

def readConfigFile():
    cityAreas = pd.read_csv(p+"/../input/car2go_oper_areas_limits.csv", header=0)
    with open(p+"/../input/config.txt", "r") as f:
        content = f.readlines()

    d={}
    for x in content:
        if len(x) > 0:
            x = x.rstrip()
            line = x.split("=")
            d[line[0]] = line[1]

    # d["city"] = d["city"].
    # for city in d["city"]:
    #     if city not in availableCities:
    #         print ("No entries for", "city")
    #
    # d["provider"] = d["provider"].split(",")

    d["initdate"] = int(time.mktime(datetime.datetime.strptime(d["initdate"], "%Y-%m-%dT%H:%M:%S").timetuple()))
    d["finaldate"] = int(time.mktime(datetime.datetime.strptime(d["finaldate"], "%Y-%m-%dT%H:%M:%S").timetuple()))
    cityAreas = cityAreas.set_index("city")
    d["limits"] = cityAreas.loc[d["city"]]

    global MaxLat, MaxLon, minLat, minLon, city, provider, initDate, finalDate, fleetSize

    MaxLat = d["limits"]["maxLat"]
    MaxLon = d["limits"]["maxLon"]

    minLat = d["limits"]["minLat"]
    minLon = d["limits"]["minLon"]

    city = d["city"]

    provider = d["provider"]
    initDate = int(d["initdate"])
    finalDate = int(d["finaldate"])
    fleetSize = int(d["fleetSize"])

    return d

