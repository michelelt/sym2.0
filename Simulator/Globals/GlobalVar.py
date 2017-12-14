'''
Created on 13/nov/2017

@author: dgiordan
'''

import sys
import os
import pandas as pd
import time
import datetime

p = os.path.abspath("..")
sys.path.append(p+"/")

def readConfigFile():
    cityAreas = pd.read_csv(p+"/input/car2go_oper_areas_limits.csv", header=0)
    availableCities = cityAreas["city"]
    with open(p+"/input/config.txt", "r") as f:
        content = f.readlines()

    d={}
    for x in content:
        if len(x) == 0 :
            pass
        else:
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


    return d

d = readConfigFile()

MaxLat = d["limits"]["maxLat"]
MaxLon = d["limits"]["maxLon"]

minLat = d["limits"]["minLat"]
minLon = d["limits"]["minLon"]

city = d["city"]

provider = d["provider"]
initDate = int(d["initdate"])
finalDate = int(d["finaldate"])
fleetSize = int(d["fleetSize"])


# CaselleCentralLat = 45.18843
# CaselleCentralLon = 7.6435

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
#
#
# '''
# add /2 in order to have a zonization 250x250
# '''
# CaselleMaxLat = CaselleCentralLat + ShiftLat
# CaselleMaxLon = CaselleCentralLon + ShiftLon
# CaselleminLat = CaselleCentralLat - ShiftLat
# CaselleminLon = CaselleCentralLon + ShiftLon

# initDataSet = "###initDataSet###"
