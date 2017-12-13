import sys
import os
p = os.path.abspath('..')
sys.path.append(p+"/")

import pickle
from geopy.geocoders import Nominatim
from Simulator.Globals.SupportFunctions import *
from Simulator.Globals.GlobalVar import *
from Simulator.Classes.PlatesData import PlatesData


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




