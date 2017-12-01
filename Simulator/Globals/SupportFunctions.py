


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


from Simulator.Globals.GlobalVar import *
from Simulator.Classes.Zone import *

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




def setup_mongodb(CollectionName):   
    """Setup mongodb session """    
    try:        
        client = pymongo.MongoClient('bigdatadb.polito.it', 27017,ssl=True,ssl_cert_reqs=ssl.CERT_NONE) # server.local_bind_port is assigned local port                #client = pymongo.MongoClient()        
        client.server_info()        
        db = client['carsharing'] #Choose the DB to use     
        db.authenticate('carsharing', 'carSharingDB@polito')#, mechanism='MONGODB-CR') #authentication         #car2go_debug_info = db['DebugInfo'] #Collection for Car2Go watch
        Collection = db[CollectionName] #Collection for Enjoy watch   
    except pymongo.errors.ServerSelectionTimeoutError as err:        
        print(err)    
    return Collection

###############################################################################


def coordinates_to_index(coords):
    
    lon = coords[0]
    lat = coords[1]
    
    ind = int((lat - minLat)/ShiftLat)*NColumns + int((lon - minLon)/ShiftLon)
    if(ind<=MaxIndex): return int(ind)
    
    if(checkCasellePerimeter(lat,lon)): 
        print("Caselle!!!")
        return MaxIndex+1

    return -1

###############################################################################

def checkPerimeter(lat,lon):
    

    if(lon > minLon  and  lon< MaxLon and lat > minLat  and  lat< MaxLat): return True
    
    
    return False

def checkCasellePerimeter(lat,lon):
    
        if(lon > CaselleminLon  and  lon< CaselleMaxLon and lat > CaselleminLat  and  lat< CaselleMaxLat): return True
    
        return False
    
    
def zoneIDtoCoordinates(ID):
    
    Xi = ID%NColumns
    Yi = int(ID/NColumns)
    

    CentalLoni = (Xi+0.5)*ShiftLon+minLon
    CentalLati = (Yi+0.5)*ShiftLat+minLat


    return [CentalLoni, CentalLati]

def MatrixCoordinatesToID(Xi,Yi):

    
    ID = Yi*NColumns + Xi
    
    return ID

def zoneIDtoMatrixCoordinates(ID):
    
    Xi = ID%NColumns
    Yi = int(ID/NColumns)

    CentalLoni = (Xi+0.5)*ShiftLon+minLon
    CentalLati = (Yi+0.5)*ShiftLat+minLat
    
    return (ID, Xi, Yi, CentalLoni, CentalLati)


def ReloadZonesCars(ZoneCars, ZoneID_Zone, AvaiableChargingStations):
    
    for ZoneI_ID in ZoneCars:       
        ZoneI = Zone(ZoneI_ID,AvaiableChargingStations) 
        ZoneID_Zone[ZoneI_ID] = ZoneI 
        ZoneI.setCars(ZoneCars[ZoneI.ID])    
            
    return 


def loadRecharing(method, numberOfStations):
    Stations = []
    csvfilePath = p+"/input/"+provider+"_"+method+"500.csv"
    if (method == "rnd"):

        zones = pd.read_csv("../input/"+provider+"_ValidZones.txt", sep=" ", header=0)
        zones_list = list(zones.index)
        # while len(Stations)<=numberOfStations:
            # rn = np.random.randint(NColumns*Nrows, size = 1)
            # if(rn not in Stations): Stations.append(rn)
        Stations2 = random.sample(zones_list, numberOfStations)
        for i in range(0,len(Stations2)):
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

        fileid =  provider+"_"+policy +"_"+algorithm+"_"+str(AvaiableChargingStations)+"_"+str(numberOfStations)+"_"+str(tankThreshold) +"_"+str(walkingTreshold)
        
    return policy, fileid,fileid+".txt"

