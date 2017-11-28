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
from RunSim import loadRecharing, RunSim

import pandas as pd

path = p + "/Simulator/"




# zones =  list(range(10,85,5))
# zones.append(120)
# zones.append(160)
# tt = [0,5,10,15,20, 25,30, 35,40,45,50]

# alg = sys.argv[1]

# def command_str(z, tt, alg):
# 	return path + "RunSim.py " + str(z) +" "+ alg + " " + str(t) + " 5000; "
	
# myStr=""
# i=0
# for z in zones:
# 	for t in tt :
# 			myStr += command_str(z, tt, alg)
# 			i=i+1

# os.system(myStr)

def main():


    walkingTreshold = 1000000#int(sys.argv[4]) # in [m]

    zoneEnjoy = 222


    numberOfStations =int(sys.argv[1])
    algorithm =  str(sys.argv[2])
    tankThreshold = int(sys.argv[3]) # in [%]
    AvaiableChargingStations = int(sys.argv[4])



    # countNoRech = {}

    #BookingID_Car = load()
    a = datetime.datetime.now()
    Stamps_Events = pickle.load( open( "../events/"+provider+"_sorted_dict_events_obj.pkl", "rb" ) )
    b = datetime.datetime.now()    
    c = (b - a).total_seconds()
    print("End Load Events: "+str(int(c)))


    a = datetime.datetime.now()    
    global DistancesFrom_Zone_Ordered 
    DistancesFrom_Zone_Ordered = pickle.load( open( "../input/"+provider+"_ZoneDistances.p", "rb" ) )
    b = datetime.datetime.now()    
    c = (b - a).total_seconds()
    print("End Load Zones: "+str(int(c)))
    i=0
    
    ZoneCars = pickle.load( open( "../input/"+provider+"_ZoneCars.p", "rb" ) )


    
    # a = datetime.datetime.now()    
    # global RechargingStation_Zones
    # RechargingStation_Zones = loadRecharing(algorithm, provider, numberOfStations)
    # b = datetime.datetime.now()    
    # c = (b - a).total_seconds()
    # print("End Load Recharging: "+str(int(c)))


    simulations_parameters = [1]
    
    
    #simulation 1
    


    jobs = []

    # manager = multiprocessing.Manager()
    # return_dict = manager.dict()
    return_dict = {}
    k=0

    # RechargingStation_Zones = []
    # while len(RechargingStation_Zones)<numberOfStations:
    #     rn = np.random.randint(NColumns*Nrows, size = 1)[0]
    #     if(rn not in RechargingStation_Zones): RechargingStation_Zones.append(rn)

    zones =  list(range(10,85,5))
    zones.append(120)
    zones.append(160)
    global RechargingStation_Zones

    tt = [0,5,10,15,20, 25,30, 35,40,45,50]
    for algorithm in ["max_time", "max_parking", "rnd"]:
        for AvaiableChargingStations in [2,4]:
            for numberOfStations in zones:
                for tankThreshold in tt:

                    a = datetime.datetime.now()    
                    RechargingStation_Zones = loadRecharing(algorithm, provider, numberOfStations)
                    b = datetime.datetime.now()    
                    c = (b - a).total_seconds()
                    print("End Load Recharging: "+str(int(c)))

                    RunSim(algorithm,numberOfStations,tankThreshold,walkingTreshold,ZoneCars,Stamps_Events,\
                    RechargingStation_Zones,DistancesFrom_Zone_Ordered,return_dict,k, AvaiableChargingStations)

main()

