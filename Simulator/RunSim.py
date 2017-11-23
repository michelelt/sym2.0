#!/usr/bin/env python3

import numpy as np
import pickle
import sys
import os
p = os.path.abspath('..')
sys.path.append(p+"/")

from Simulator.Globals.GlobalVar import *
from Simulator.Globals.SupportFunctions import *
import datetime
import click
import csv
import sys
import time


def SearchAvailableCar(ZoneI,Stamp):

    SelectedCar = "" 
    if(ZoneI.ID in RechargingStation_Zones):
        SelectedCar = ZoneI.getBestRechargedCars(Stamp)
    if(SelectedCar == ""):
        SelectedCar = ZoneI.getBestCars()
    
    
    return SelectedCar

def SearchNearestBestCar(BookingStarting_Position,Stamp):
       
    SelectedCar = ""
    Distance = -1
    Iter = 0
    for DistanceI in DistancesFrom_Zone_Ordered[BookingStarting_Position]:        
        Iter +=1
        RandomZones = DistanceI[1].getZones()
        for ZoneI in RandomZones:                    
            SelectedCar = SearchAvailableCar(ZoneI,Stamp)
            if(SelectedCar != ""):
                Distance = DistanceI[1].getDistance()
                return SelectedCar, Distance, ZoneI.ID, Iter
    
    print("erroreeeee")
    return -1, -1

def ParkCar(BookingEndPosition,BookedCar, tankThreshold, walkingTreshold):
    
    ToRecharge = False
    Recharged = False
    Distance =-1
    
    Lvl =BookedCar.getBatteryLvl()
    if(Lvl < tankThreshold):
        #print("PROBLEMA: %d"%BookedCar.getBatteryLvl())
        ToRecharge = True
        for DistanceI in DistancesFrom_Zone_Ordered[BookingEndPosition]:        
            Distance = DistanceI[1].getDistance()
            if(Distance > walkingTreshold): break            
            RandomZones = DistanceI[1].getZones()
            for ZoneI in RandomZones:     
                if(ZoneI.ID in RechargingStation_Zones):               
                    Found = ZoneI.getParkingAtRechargingStations(BookedCar)
                    if(Found): 
                        Recharged = True
                        BookedCar.setInStation()
                        return Lvl, ToRecharge, Recharged, Distance, ZoneI.ID        

    for DistanceI in DistancesFrom_Zone_Ordered[BookingEndPosition]:        
        RandomZones = DistanceI[1].getZones()
        for ZoneI in RandomZones:                    
            ZoneI.getAnyParking(BookedCar)
            return Lvl, ToRecharge, Recharged, 0, ZoneI.ID


def loadRecharing(method, provider, numberOfStations):
    Stations = []
    csvfilePath = p+"/input/"+provider+"_"+method+"500.csv"
    if (method == "rnd"):
        while len(Stations)<=numberOfStations:
            rn = np.random.randint(NColumns*Nrows, size = 1)
            if(rn not in Stations): Stations.append(rn)

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

def load_distances():
    return

RechargingStation_Zones = []

DistancesFrom_Zone_Ordered ={}

BookingID_Car = {}
Stamps_Events ={}


def getncar():
    
    TotalCar1 = 0
    TotalCar2 = 0
    
    for DistanceI in DistancesFrom_Zone_Ordered[1964]:        
        RandomZones = DistanceI[1].getZones()
        for ZoneI in RandomZones:                    
            TotalCar1 += ZoneI.getNumCar()
            TotalCar2 += ZoneI.getNumRecCar()
    
    return TotalCar1,TotalCar2

def WriteOutHeader(file, parametersDict):
    for key in parametersDict.keys():
        file.write(key + ":" + str(parametersDict[key])+"\n")
    file.write(initDataSet+"\n")

    return

def dict_to_string(myDict):
    
    mykeys = ["Type", "ToRecharge", "Recharged","ID","Lvl","Distance",
    "Iter","Recharge", "StartRecharge", "Stamp","EventCoords",
    "ZoneC", "Discharge", "TripDistance"]
    
    
    outputString =""
    for k in mykeys:
        outputString += str(myDict[k])+";"

    outputString = outputString[:-1]
    outputString+="\n"

    return outputString


def main():
    mt = time.time()
    numberOfStations = int(sys.argv[1])
    algorithm = str(sys.argv[2])
    tankThreshold = int(sys.argv[3]) # in [%]
    walkingTreshold = int(sys.argv[4]) # in [m]


    zoneEnjoy = 220

    # countNoRech = {}

    #BookingID_Car = load()
    a = datetime.datetime.now()
    Stamps_Events = pickle.load( open( "../events/"+provider+"_sorted_dict_events_obj.pkl", "rb" ) )
    b = datetime.datetime.now()    
    c = (b - a).total_seconds()
    print("End Load Events: "+str(int(c)))
    
    a = datetime.datetime.now()    
    global RechargingStation_Zones
    RechargingStation_Zones = loadRecharing(algorithm, provider, numberOfStations)



    b = datetime.datetime.now()    
    c = (b - a).total_seconds()
    print("End Load Recharging: "+str(int(c)))

    a = datetime.datetime.now()    
    global DistancesFrom_Zone_Ordered 
    DistancesFrom_Zone_Ordered = pickle.load( open( "../input/"+provider+"_ZoneDistances.p", "rb" ) )
    b = datetime.datetime.now()    
    c = (b - a).total_seconds()
    print("End Load Zones: "+str(int(c)))
    i=0
    print (time.time()-mt)
    

    #TotalCar1,TotalCar2 = getncar()
    ActualBooking = 0
    

    #print(TotalCar1,TotalCar2,ActualBooking)
    fout = open("../output/aa_"+\
        provider+"_"+\
        algorithm+"_"+
        str(numberOfStations)+"_"+\
        str(tankThreshold) + ".txt","w")
    fout.write("yuppie ye")
    fout2 = open("../output/debugproblem.txt","w")
    a = datetime.datetime.now()
    WriteOutHeader(fout, {"provider": provider,
    "algorithm ": algorithm,
    "ChargingStations":numberOfStations, 
    "tankThreshold":tankThreshold,
    "walkingTreshold":  walkingTreshold})
    
    
    # fout.write("Type;ToRecharge;Recharged;CarID;BatteryLvl;PickDistance;Re/DisCharge;StartRec/TripDistance;EndRec;C1;C2\n")
    fout.write("Type;ToRecharge;Recharged;ID;Lvl;Distance;Iter;Recharge;StartRecharge;Stamp;EventCoords;ZoneC;Discharge;TripDistance\n")
 

    print ("Dataset from",
        datetime.datetime.fromtimestamp(int(list(Stamps_Events.keys())[0])).strftime('%Y-%m-%d %H:%M:%S'),
        "to",
        datetime.datetime.fromtimestamp(int(list(Stamps_Events.keys())[len(Stamps_Events)-1])).strftime('%Y-%m-%d %H:%M:%S'))  
        
    with click.progressbar(Stamps_Events, length=len(Stamps_Events)) as bar:
        for Stamp in bar:
            for Event in Stamps_Events[Stamp]:
                i+=1
                #print(i,Event.type)
                    
                if(Event.type == "s"):
                    #TotalCar1,TotalCar2 = getncar()
                    fout2.write("%d %d \n"%(Stamp,ActualBooking))#,TotalCar1,TotalCar2))
                    ActualBooking +=1
                    BookingStarting_Position = coordinates_to_index(Event.coordinates)                
                    BookingID = Event.id_booking
                    NearestCar, Distance, ZoneID, Iter  = SearchNearestBestCar(BookingStarting_Position, Stamp)
                    Recharge,StartRecharge = NearestCar.Recharge(Stamp)
                    NearestCar.setStartPosition(Event.coordinates)
                    BookingID_Car[BookingID] = NearestCar
                    Lvl = NearestCar.getBatteryLvl()
                    ID = NearestCar.getID()
                    ZoneC = zoneIDtoCoordinates(ZoneID)

                    d={"Type":"s",
                    "ToRecharge":np.NaN,
                    "Recharged":np.NaN,
                    "ID":ID,
                    "Lvl":Lvl,
                    "Distance":Distance,
                    "Iter":Iter,
                    "Recharge":Recharge,
                    "StartRecharge":StartRecharge,
                    "Stamp":Stamp,
                    "EventCoords":str(Event.coordinates),
                    "ZoneC":str(ZoneC),
                    "Discharge":np.NaN,
                    "TripDistance":np.NaN}


                    #print(d)
                    fout.write(dict_to_string(d))

                
                
                else:
                    BookingEndPosition = coordinates_to_index(Event.coordinates) 
                    if(BookingEndPosition<0): print(Event.coordinates) 
                    ActualBooking -=1
                    BookedCar = BookingID_Car[Event.id_booking]
                    Discarge, TripDistance = BookedCar.Discharge(Event.coordinates)            
                    Lvl, ToRecharge, Recharged, Distance, ZoneID = ParkCar(BookingEndPosition,BookedCar, tankThreshold, walkingTreshold)
                    BookedCar.setStartRecharge(Stamp)
                    ID = BookedCar.getID()
                    del BookingID_Car[Event.id_booking]
                    ZoneC = zoneIDtoCoordinates(ZoneID)

                    d={"Type":"e",
                    "ToRecharge":ToRecharge,
                    "Recharged":Recharged,
                    "ID":ID,
                    "Lvl":Lvl,
                    "Distance":Distance,
                    "Iter":Iter,
                    "Recharge":np.NaN,
                    "StartRecharge":np.NaN,
                    "Stamp":Stamp,
                    "EventCoords":str(Event.coordinates),
                    "ZoneC": ZoneC,
                    "Discharge":Discarge,
                    "TripDistance":TripDistance}
                    fout.write(dict_to_string(d))

                                   

    b = datetime.datetime.now()    
    c = (b - a).total_seconds()
    print("End Simulation: "+str(int(c)))
    
                
    return

main()