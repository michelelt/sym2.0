'''
Created on 13/nov/2017

@author: dgiordan
'''

import pymongo
import ssl
from math import *
import sys
import os
p = os.path.abspath('..')
sys.path.append(p+"/")
import pandas as pd
import numpy as np
import random
import csv

import Simulator.Globals.GlobalVar as GlobalVar


def readConfigFile():
    cityAreas = pd.read_csv(p+"/input/car2go_oper_areas_limits.csv", header=0)
    with open(p+"/input/config.txt", "r") as f:
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

def assingVariables():

    d = readConfigFile()

    GlobalVar.MaxLat = d["limits"]["maxLat"]
    GlobalVar.MaxLon = d["limits"]["maxLon"]
    GlobalVar.minLat = d["limits"]["minLat"]
    GlobalVar.minLon = d["limits"]["minLon"]
    GlobalVar.city = d["city"]
    GlobalVar.provider = d["provider"]
    GlobalVar.initDate = int(d["initdate"])
    GlobalVar.finalDate = int(d["finaldate"])
    GlobalVar.fleetSize = int(d["fleetSize"])

    GlobalVar.CaselleCentralLat = 45.18843
    GlobalVar.CaselleCentralLon = 7.6435

    GlobalVar.CorrectiveFactor = 1  # .88

    # GlobalVar.shiftLat500m = 0.0045
    # GlobalVar.shiftLon500m = 0.00637

    '''
    add /2 in order to have a zonization 250x250
    '''

    GlobalVar.NColumns = int((GlobalVar.MaxLon - GlobalVar.minLon) / GlobalVar.shiftLon500m)
    GlobalVar.NRows = int((GlobalVar.MaxLat - GlobalVar.minLat) / GlobalVar.shiftLat500m)
    GlobalVar.MaxIndex = GlobalVar.NRows * GlobalVar.NColumns - 1

    GlobalVar.ShiftLon = (GlobalVar.MaxLon - GlobalVar.minLon) / GlobalVar.NColumns
    GlobalVar.ShiftLat = (GlobalVar.MaxLat - GlobalVar.minLat) / GlobalVar.NRows

    return

def setup_mongodb(CollectionName):   
    """"Setup mongodb session """    
    try:        
        client = pymongo.MongoClient('bigdatadb.polito.it',
                                     27017,
                                     ssl=True,
                                     ssl_cert_reqs=ssl.CERT_NONE) # server.local_bind_port is assigned local port                #client = pymongo.MongoClient()
        client.server_info()        
        db = client['carsharing'] #Choose the DB to use     
        db.authenticate('carsharing', 'carSharingDB@polito')#, mechanism='MONGODB-CR') #authentication         #car2go_debug_info = db['DebugInfo'] #Collection for Car2Go watch
        Collection = db[CollectionName] #Collection for Enjoy watch   
    except pymongo.errors.ServerSelectionTimeoutError as err:        
        print(err)    
    return Collection

###############################################################################




def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    km = 6367 * c
    
    return int(km*1000)

###############################################################################


def coordinates_to_index(coords):
    
    lon = coords[0]
    lat = coords[1]
    
    ind = int((lat - GlobalVar.minLat) / GlobalVar.ShiftLat) * \
          GlobalVar.NColumns + \
          int((lon - GlobalVar.minLon) / GlobalVar.ShiftLon)
    if(ind<=GlobalVar.MaxIndex): return int(ind)
    
    if(checkCasellePerimeter(lat,lon)): 
        print("Caselle!!!")
        return GlobalVar.MaxIndex+1

    return -1

###############################################################################

def checkPerimeter(lat,lon):

    if(lon > GlobalVar.minLon  and  lon < GlobalVar.MaxLon and lat > GlobalVar.minLat  and  lat< GlobalVar.MaxLat): return True

    return False

def checkCasellePerimeter(lat,lon):
    
        if(lon > CaselleminLon  and  lon< CaselleMaxLon and lat > CaselleminLat  and  lat< CaselleMaxLat): return True

        return False
    
    
def zoneIDtoCoordinates(ID):
    
    Xi = ID % GlobalVar.NColumns
    Yi = int(ID / GlobalVar.NColumns)
    

    CentalLoni = (Xi + 0.5) * GlobalVar.ShiftLon + GlobalVar.minLon
    CentalLati = (Yi + 0.5) * GlobalVar.ShiftLat + GlobalVar.minLat

    return [CentalLoni, CentalLati]

def MatrixCoordinatesToID(Xi,Yi):

    
    ID = Yi * GlobalVar.NColumns + Xi
    
    return ID

def zoneIDtoMatrixCoordinates(ID):
    
    Xi = ID % GlobalVar.NColumns
    Yi = int(ID / GlobalVar.NColumns)

    CentalLoni = (Xi + 0.5) * GlobalVar.ShiftLon + GlobalVar.minLon
    CentalLati = (Yi + 0.5) * GlobalVar.ShiftLat + GlobalVar.minLat
    
    return (ID, Xi, Yi, CentalLoni, CentalLati)


def ReloadZonesCars(ZoneCars, ZoneID_Zone, AvaiableChargingStations):
    
    for ZoneI_ID in ZoneCars:       
        ZoneI = Zone(ZoneI_ID,AvaiableChargingStations) 
        ZoneID_Zone[ZoneI_ID] = ZoneI 
        ZoneI.setCars(ZoneCars[ZoneI.ID])    
            
    return 


def loadRecharing(method, numberOfStations):
    Stations = []
    csvfilePath = p+"/input/"+ GlobalVar.provider + "_" + method + "500.csv"
    if (method == "rnd"):

        zones = pd.read_csv("../input/" + GlobalVar.provider + "_ValidZones.txt", sep=" ", header=0)
        zones_list = list(zones.index)
        # while len(Stations)<=numberOfStations:
            # rn = np.random.randint(NColumns*Nrows, size = 1)
            # if(rn not in Stations): Stations.append(rn)
        Stations2 = random.sample(zones_list, numberOfStations)
        for i in range(0, len(Stations2)):
            Stations.append(np.array(Stations2[i]))


    else :
        coords = []
        with open(csvfilePath, 'rt') as csvfile:
                csvreader = csv.reader(csvfile, delimiter=',')
                next(csvreader)
                for row in csvreader:
                    coords.insert(0, float(row[2])) #lon
                    coords.insert(1, float(row[1])) #lat
                    index = np.array(coordinates_to_index(coords))
                    Stations.append(index)
                    if len(Stations) == numberOfStations+1:
                        Stations.pop(0)
                        break
        
    return Stations

def foutname(BestEffort,algorithm,AvaiableChargingStations,numberOfStations,tankThreshold,walkingTreshold):
    
    foutname = ""
    policy = "Forced"
    if(BestEffort == True):
        if(tankThreshold<0):
            policy="Best"
        else:
            policy="Hybrid"

        fileid = provider+"_"+\
                 policy +"_"+\
                 algorithm+"_"+\
                 str(numberOfStations)+"_"+\
                 str(AvaiableChargingStations)+"_"+\
                 str(tankThreshold) +"_"+\
                 str(walkingTreshold)
        
    return policy, fileid,fileid+".txt"

from Simulator.Classes.Zone import *
