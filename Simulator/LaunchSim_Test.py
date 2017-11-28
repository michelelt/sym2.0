import sys
import os
p = os.path.abspath('..')
sys.path.append(p+"/")

from Simulator.RunSim import *
from Simulator.Globals.GlobalVar import * 
import datetime as datetime
import pickle

from multiprocessing import Process
import multiprocessing

def main():


    walkingTreshold = 1000000#int(sys.argv[4]) # in [m]

    zoneEnjoy = 220

    # countNoRech = {}

    #BookingID_Car = load()
    a = datetime.datetime.now()
    Stamps_Events = pickle.load( open( "../events/"+provider+"_sorted_dict_events_obj.pkl", "rb" ) )
    b = datetime.datetime.now()    
    c = (b - a).total_seconds()
    print("End Loading Events: "+str(int(c)))


    a = datetime.datetime.now()    
    DistancesFrom_Zone_Ordered = pickle.load( open( "../input/"+provider+"_ZoneDistances.p", "rb" ) )
    b = datetime.datetime.now()    
    c = (b - a).total_seconds()
    print("End Loading Zones: "+str(int(c)))

    a = datetime.datetime.now()    
    ZoneID_Zone = pickle.load( open( "../input/"+provider+"_ZoneID_Zone.p", "rb" ) )
    b = datetime.datetime.now()    
    c = (b - a).total_seconds()
    print("End Loading ZoneID_Zone: "+str(int(c)))
    
    ZoneCars = pickle.load( open( "../input/"+provider+"_ZoneCars.p", "rb" ) )


    numberOfStations = 160#len(RechargingStation_Zones)#int(sys.argv[1])
    algorithm = "max_"#str(sys.argv[2])
    
    a = datetime.datetime.now()    
    global RechargingStation_Zones
    
    
    algorithm= "max_parking" 
    numberOfStations = 160 
    tankThreshold = 5 
    AvaiableChargingStations = 2
    
    
    RechargingStation_Zones = loadRecharing(algorithm, provider, numberOfStations)
    b = datetime.datetime.now()    
    c = (b - a).total_seconds()
    print("End Load Recharging: "+str(int(c)))

    print(RechargingStation_Zones)
    #simulation 1
    
    #tankThreshold = 50#int(sys.argv[3]) # in [%]

    
    return_dict = {}
    
    
    RunSim(algorithm,numberOfStations,tankThreshold,walkingTreshold,ZoneCars,Stamps_Events,\
       RechargingStation_Zones,DistancesFrom_Zone_Ordered,ZoneID_Zone,return_dict,-1,AvaiableChargingStations)
                                               
    return

main()

