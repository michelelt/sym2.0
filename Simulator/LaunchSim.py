from Simulator.RunSim import *
from Simulator.Globals.GlobalVar import * 
import datetime as datetime
import sys
import pickle

def main():


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
    
    ZoneCars = pickle.load( open( "../input/"+provider+"_ZoneCars.p", "rb" ) )


    simulations_parameters = [1]
    
    for i in simulations_parameters:
     
        PercRerouteEnd, PercRerouteStart, PercRecharge, MedianMeterEnd, MeanMeterEnd, MedianMeterStart, MeanMeterStart, NEnd, NStart = \
            RunSim(algorithm,numberOfStations,tankThreshold,walkingTreshold,ZoneCars,Stamps_Events,RechargingStation_Zones,DistancesFrom_Zone_Ordered)

    return

main()

