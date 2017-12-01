import sys
import os
p = os.path.abspath('..')
sys.path.append(p+"/")

from Simulator.RunSim import *
from Simulator.Globals.GlobalVar import * 
import datetime as datetime
import pickle

import multiprocessing
from multiprocessing import Process

#import subprocess


def main():
    

    ##TO AVOID: "OSError: [Errno 24] Too many open files"     
    #bashCommand = "ulimit -n 2048"
    #process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    #process.communicate()
    ###
    


    walkingTreshold = 1000000#int(sys.argv[4]) # in [m]

    zoneEnjoy = 220

    aglobal = datetime.datetime.now()
    nsimulations = 0
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
    
    ZoneCars = pickle.load( open( "../input/"+provider+"_ZoneCars.p", "rb" ) )



    
    zones = [i for i in range(60,61,5)]
    for i in range(120,121,20):
        zones.append(i)
    tt = []#-5
    for i in range(50,61,10):
        tt.append(i)
    
    
    
    for BestEffort in [True]:#,False]:
        for AvaiableChargingStations in [6]: #2,4,
            for algorithm in ["max_time"]:#, "max_parking", "rnd"]:
                jobs=[]
                for numberOfStations in zones:
                    for tankThreshold in tt:
                        if(tankThreshold<0 and BestEffort==False): continue
                        
                        RechargingStation_Zones = loadRecharing(algorithm, numberOfStations)
                        p = Process(target=RunSim,args = (BestEffort,
                                                          algorithm,
                                                          AvaiableChargingStations,
                                                          tankThreshold,
                                                          walkingTreshold,
                                                          ZoneCars,
                                                          RechargingStation_Zones,
                                                          Stamps_Events,
                                                          DistancesFrom_Zone_Ordered,
                                                          None,
                                                          -1))
                        nsimulations +=1

                        jobs.append(p)
                        p.start()
                
                for proc in jobs:
                    proc.join()
                
    

    b = datetime.datetime.now()    
    c = (b - aglobal).total_seconds()                
    
    print("Run %d Simulations took %d seconds"%(nsimulations,c))
    return 
        
main()

