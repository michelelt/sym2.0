#!/usr/bin/env python3

import numpy as np
import pickle
import sys
import os
import csv
p = os.path.abspath('..')
sys.path.append(p+"/")

from Simulator.Globals.GlobalVar import *
from Simulator.Globals.SupportFunctions import *
import datetime
import click

countNoRech = {}


def SearchAvailableCar(ZoneI):

    SelectedCar = "" 
    if(ZoneI.ID in RechargingStation_Zones):
        SelectedCar = ZoneI.getBestRechargedCars()
    if(SelectedCar == ""):
        SelectedCar = ZoneI.getBestCars()
    
    
    return SelectedCar

def SearchNearestBestCar(BookingStarting_Position):
       
    SelectedCar = ""
    Distance = -1
    Iter = 0
    for DistanceI in DistancesFrom_Zone_Ordered[BookingStarting_Position]:        
        Iter +=1
        RandomZones = DistanceI[1].getZones()
        for ZoneI in RandomZones:                    
            SelectedCar = SearchAvailableCar(ZoneI)
            if(SelectedCar != ""):
                Distance = DistanceI[1].getDistance()
                return SelectedCar, Distance, ZoneI.ID, Iter
    
    print("erroreeeee")
    return -1, -1

def ParkCar(BookingEndPosition,BookedCar, tankThreshold, walkingTreshold):
    
    ToRecharge = False
    Recharged = False
    Distance =-1
    WT_exceed = False
    
    Lvl =BookedCar.getBatteryLvl()
    ''' oblige car to park in charging station '''
    if(Lvl < tankThreshold):
        #print("PROBLEMA: %d"%BookedCar.getBatteryLvl())
        ToRecharge = True
        '''Search the nearest station under the th'''
        for DistanceI in DistancesFrom_Zone_Ordered[BookingEndPosition]:        
            Distance = DistanceI[1].getDistance()
            if(Distance > walkingTreshold):
                WT_exceed = True
                break

            '''chose randomly one zone in the cs dataset '''
            RandomZones = DistanceI[1].getZones()
            for ZoneI in RandomZones:     
                if(ZoneI.ID in RechargingStation_Zones):               
                    Found = ZoneI.getParkingAtRechargingStations(BookedCar)
                    if(Found): 
                        Recharged = True
                        countNoRech[ZoneI.ID] +=1
                        return Lvl, ToRecharge, Recharged, Distance, WT_exceed       

    ''' leave the car in the first zone '''
    for DistanceI in DistancesFrom_Zone_Ordered[BookingEndPosition]:        
        RandomZones = DistanceI[1].getZones()
        for ZoneI in RandomZones:                    
            ZoneI.getAnyParking(BookedCar)
            return Lvl, ToRecharge, Recharged, 0, WT_exceed


def loadRecharing(method, provider, numberOfStations):
    Stations = []
    csvfilePath = p+"/input/"+provider+"_"+method+".csv"
    if (method == "rnd"):
        while len(Stations)<numberOfStations:
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
                    if len(Stations) == numberOfStations:
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
    outputString =""
    for k in myDict.keys():
        outputString += str(myDict[k])+";"

    outputString = outputString[:-1]
    outputString+="\n"

    return outputString


def main():
    

    tankThreshold = 50 # in [%]
    walkingTreshold = 2000 # in [m]
    algorithm = "rnd"
    tot_deaths = 0

    # countNoRech = {}

    #BookingID_Car = load()
    a = datetime.datetime.now()
    Stamps_Events = pickle.load( open( "../events/"+provider+"_sorted_dict_events_obj.pkl", "rb" ) )
    b = datetime.datetime.now()    
    c = (b - a).total_seconds()
    print("End Load Events: "+str(int(c)))
    
    a = datetime.datetime.now()    
    global RechargingStation_Zones
    numberOfStations = 60
    RechargingStation_Zones = loadRecharing(algorithm, provider, numberOfStations)
    for ZoneI in RechargingStation_Zones:
        countNoRech[int(ZoneI[0])] = 0



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
    
    

    #TotalCar1,TotalCar2 = getncar()
    ActualBooking = 0

    

    #print(TotalCar1,TotalCar2,ActualBooking)
    fout = open("../output/walk2.txt","w")
    fout2 = open("../output/debugproblem.txt","w")
    a = datetime.datetime.now()
    WriteOutHeader(fout, {"provider": provider,
    "algorithm ": algorithm,
    "ChargingStations":numberOfStations, 
    "tankThreshold":tankThreshold,
    "walkingTreshold":  walkingTreshold})

    # fout.write("Type;ToRecharge;Recharged;CarID;BatteryLvl;PickDistance;Re/DisCharge;StartRec/TripDistance;EndRec;C1;C2\n")
    fout.write("Type;ToRecharge;Recharged;ID;Lvl;Distance;Iter;Recharge;StartRecharge;Stamp;EventCoords;ZoneC;WT_exceed;Discharge;TripDistance\n")


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
                    NearestCar, Distance, ZoneID, Iter  = SearchNearestBestCar(BookingStarting_Position)
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
                    "WT_exceed": np.NaN,
                    "Discharge":np.NaN,
                    "TripDistance":np.NaN}



                    fout.write(dict_to_string(d))

                    # fout.write("s;0;0;%d;%d;%d;%d;%f;%d;%d;0;0" \
                    #     %(ID, Lvl, Distance, Iter, Recharge,StartRecharge,Stamp)+ ";" +str(Event.coordinates)+";"+str(ZoneC)+"\n")
                    #     )

                else:
                    BookingEndPosition = coordinates_to_index(Event.coordinates) 
                    if(BookingEndPosition<0): print(Event.coordinates) 
                    ActualBooking -=1
                    BookedCar = BookingID_Car[Event.id_booking]
                    Discarge, TripDistance = BookedCar.Discharge(Event.coordinates)            
                    Lvl, ToRecharge, Recharged, Distance, WT_exceed = ParkCar(BookingEndPosition,BookedCar, tankThreshold, walkingTreshold)
                    BookedCar.setStartRecharge(Stamp)
                    ID = BookedCar.getID()
                    del BookingID_Car[Event.id_booking]
                    # fout.write("e;%s;%s;%d;%d;%d;%f;%d"%(ToRecharge, Recharged, ID, Lvl,Distance, Discarge, TripDistance)+"\n")

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
                    "ZoneC":np.NaN,
                    "WT_exceed": WT_exceed,
                    "Discharge":Discarge,
                    "TripDistance":TripDistance}
                    fout.write(dict_to_string(d))

                    
            # if(i>100): break


                    

    b = datetime.datetime.now()    
    c = (b - a).total_seconds()
    print ("Tot deaths", tot_deaths)
    print("End Simulation: "+str(int(c)))
    fStationsStats = open("../output/stationsStats.txt","w")
    fStationsStats.write("ID;NoOfRecharing")
    for stationID in countNoRech.keys():
        fStationsStats.write(str(stationID)+";"+str(countNoRech[station]))
    
                
    # return

main()