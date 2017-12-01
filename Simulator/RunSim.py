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


def SearchAvailableCar(RechargingStation_Zones,ZoneI,Stamp):

    SelectedCar = "" 
    if(ZoneI.ID in RechargingStation_Zones):
        SelectedCar = ZoneI.getBestRechargedCars(Stamp)
    if(SelectedCar == ""):
        SelectedCar = ZoneI.getBestCars()
    
    
    return SelectedCar

def SearchNearestBestCar(RechargingStation_Zones,DistancesFrom_Zone_Ordered,ZoneID_Zone,BookingStarting_Position,Stamp):
       
    SelectedCar = ""
    Distance = -1
    Iter = 0
    for DistanceI in DistancesFrom_Zone_Ordered[BookingStarting_Position]:        
        Iter +=1
        RandomZones = DistanceI[1].getZones()
        for ZoneI_ID in RandomZones:
            ZoneI = ZoneID_Zone[ZoneI_ID]                    
            SelectedCar = SearchAvailableCar(RechargingStation_Zones,ZoneI,Stamp)
            if(SelectedCar != ""):
                Distance = DistanceI[1].getDistance()
                return SelectedCar, Distance, ZoneI.ID, Iter
    
    print("erroreeeee")
    return -1, -1

def ParkCar(RechargingStation_Zones, DistancesFrom_Zone_Ordered, ZoneID_Zone, BookingEndPosition, BookedCar, tankThreshold, walkingTreshold, BestEffort):
    
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
            for ZoneI_ID in RandomZones:     
                ZoneI = ZoneID_Zone[ZoneI_ID]
                if(ZoneI.ID in RechargingStation_Zones):               
                    Found = ZoneI.getParkingAtRechargingStations(BookedCar)
                    if(Found): 
                        Recharged = True
                        BookedCar.setInStation()
                        return Lvl, ToRecharge, Recharged, Distance, ZoneI.ID        

    if(BestEffort and BookingEndPosition in RechargingStation_Zones):

        DistanceI = DistancesFrom_Zone_Ordered[BookingEndPosition][0]        
        ZoneI_ID = DistanceI[1].getZones()[0]
        ZoneI = ZoneID_Zone[ZoneI_ID]        
        Found = ZoneI.getParkingAtRechargingStations(BookedCar)
        if(Found): 
            Recharged = True
            BookedCar.setInStation()
            return Lvl, ToRecharge, Recharged, Distance, ZoneI.ID        

    for DistanceI in DistancesFrom_Zone_Ordered[BookingEndPosition]:        
        RandomZones = DistanceI[1].getZones()
        for ZoneI_ID in RandomZones:       
            ZoneI = ZoneID_Zone[ZoneI_ID]             
            ZoneI.getAnyParking(BookedCar)
            return Lvl, ToRecharge, Recharged, 0, ZoneI.ID




def WriteOutHeader(file, parametersDict):
    for key in parametersDict.keys():
        file.write(key + ":" + str(parametersDict[key])+"\n")
    file.write(initDataSet+"\n")

    return

def dict_to_string(myDict):
    
    mykeys = ["Type", "ToRecharge", "Recharged","ID","Lvl","Distance",
    "Iter","Recharge", "StartRecharge", "Stamp","EventCoords",
    "ZoneC", "Discharge", "TripDistance","FileID"]
    
    
    outputString =""
    for k in mykeys:
        if(type(myDict[k]) is int):
            outputString +="%d;"%myDict[k]
        elif(type(myDict[k]) is str):
            outputString +="%s;"%myDict[k]
        elif(type(myDict[k]) is float):
            outputString +="%.6f;"%myDict[k]
        else:
            outputString +=str(myDict[k]).replace(" ", "")+";"
        
    outputString = outputString[:-1]
    outputString+="\n"

    return outputString


def RunSim(BestEffort,
    algorithm,
    AvaiableChargingStations,
    tankThreshold,
    walkingTreshold,
    ZoneCars,
    RechargingStation_Zones,
    Stamps_Events,
    DistancesFrom_Zone_Ordered,
    return_dict,
    p):

    numberOfStations = len(RechargingStation_Zones)
    
    policy, fileID, fname = foutname(BestEffort,algorithm,AvaiableChargingStations,numberOfStations,tankThreshold,walkingTreshold)
    
    
    NRecharge = 0
    NStart = 0
    NEnd = 0
    MeterRerouteStart = []
    MeterRerouteEnd = []
    NDeath = 0
    
    ActualBooking = 0

    BookingID_Car = {}

    ZoneID_Zone = {}
    
    ReloadZonesCars(ZoneCars, ZoneID_Zone, AvaiableChargingStations)

    
    fout = open("../output/"+fname,"w")
                
    fout2 = open("../output/debugproblem.txt","w")
    a = datetime.datetime.now()
    WriteOutHeader(fout, {
    "provider": provider,
    "policy": policy,                          
    "algorithm": algorithm,
    "ChargingStations":numberOfStations,
    "AvaiableChargingStations":AvaiableChargingStations, 
    "tankThreshold":tankThreshold,
    "walkingTreshold":  walkingTreshold})
    
    
    fout.write("Type;ToRecharge;Recharged;ID;Lvl;Distance;Iter;Recharge;StartRecharge;Stamp;EventCoords;ZoneC;Discharge;TripDistance;FileID\n")
 
    '''print ("Dataset from",
        datetime.datetime.fromtimestamp(int(list(Stamps_Events.keys())[0])).strftime('%Y-%m-%d %H:%M:%S'),
        "to",
        datetime.datetime.fromtimestamp(int(list(Stamps_Events.keys())[len(Stamps_Events)-1])).strftime('%Y-%m-%d %H:%M:%S'))  

    '''
        
    i=0
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
                    NearestCar, Distance, ZoneID, Iter  = SearchNearestBestCar(RechargingStation_Zones,DistancesFrom_Zone_Ordered,ZoneID_Zone,\
                                                                               BookingStarting_Position, Stamp)
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
                    "TripDistance":np.NaN,
                    "FileID": fileID}


                    #print(d)
                    fout.write(dict_to_string(d))

                    if(Distance> 0):
                        MeterRerouteStart.append(Distance)
                    NStart+=1
                else:
                    BookingEndPosition = coordinates_to_index(Event.coordinates) 
                    if(BookingEndPosition<0): print(Event.coordinates) 
                    ActualBooking -=1
                    BookedCar = BookingID_Car[Event.id_booking]
                    Discarge, TripDistance = BookedCar.Discharge(Event.coordinates)            
                    Lvl, ToRecharge, Recharged, Distance, ZoneID = ParkCar(RechargingStation_Zones,DistancesFrom_Zone_Ordered,ZoneID_Zone,\
                                                                           BookingEndPosition, BookedCar, tankThreshold, walkingTreshold, BestEffort)
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
                    "ZoneC":ZoneC,
                    "Discharge":Discarge,
                    "TripDistance":TripDistance,
                    "FileID": fileID}
                    
                    fout.write(dict_to_string(d))

                    if(Distance > 0):
                        MeterRerouteEnd.append(Distance)
                    
                    if(Recharged == True):
                        NRecharge +=1
                    
                    if(BookedCar.getBatterCurrentCapacity()<0):
                        NDeath +=1
                    
                    NEnd+=1


    b = datetime.datetime.now()    
    c = (b - a).total_seconds()
    #print("End Simulation: "+str(int(c)))

    if(return_dict != None):
    
        PercRerouteEnd = len(MeterRerouteEnd)/NEnd*100
        PercRerouteStart = len(MeterRerouteStart)/NStart*100
        PercRecharge = NRecharge/NEnd*100
        PercDeath = NDeath/NEnd*100
        
        MedianMeterEnd = np.median(np.array(MeterRerouteEnd))
        MeanMeterEnd = np.mean(np.array(MeterRerouteEnd))
    
        MedianMeterStart = np.median(np.array(MeterRerouteStart))
        MeanMeterStart = np.mean(np.array(MeterRerouteStart))
    
        RetValues = {}
        RetValues["ProcessID"] = p
        RetValues["PercRerouteEnd"] = PercRerouteEnd
        RetValues["PercRerouteStart"] = PercRerouteStart
        RetValues["PercRecharge"] = PercRecharge
        RetValues["PercDeath"] = PercDeath
        RetValues["MedianMeterEnd"] = MedianMeterEnd
        RetValues["MeanMeterEnd"] = MeanMeterEnd
        RetValues["MedianMeterStart"] = MedianMeterStart
        RetValues["MeanMeterStart"] = MeanMeterStart
        RetValues["NEnd"] = NEnd
        RetValues["NStart"] = NStart
    
        return_dict[p] = RetValues
    
    fout.close()
    fout2.close()

    current_folder = os.getcwd().split("/")
    output_folder = ""
    for i in range(0,len(current_folder)-1):
        output_folder += current_folder[i]+"/"
    output_folder+="output/"    
    os.system('cat %s | ssh bigdatadb hdfs dfs -put -f - Simulator/output/%s' %(output_folder+fname,fname))
    
    return