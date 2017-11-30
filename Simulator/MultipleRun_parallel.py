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


def foutname(BestEffort,algorithm,AvaiableChargingStations,numberOfStations,tankThreshold):
    
    foutname = ""
    policy = "Forced"
    if(BestEffort == True):
        if(tankThreshold<0):
            policy="Best"
        else:
            policy="Hybrid"
        
        foutname =  policy+ "_"+provider+"_"+algorithm+"_"+str(AvaiableChargingStations)+"_"+str(numberOfStations)+"_"+str(tankThreshold) + ".txt","w"
            
    return policy, foutname

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



    
    zones = [i for i in range(10,61,5)]
    for i in range(80,121,20):
        zones.append(i)
    tt = [-5]
    for i in range(0,61,10):
        tt.append(i)
    
    
    
    for BestEffort in [True,False]:
        for AvaiableChargingStations in [2,4,6]:
            for algorithm in ["max_time", "max_parking", "rnd"]:
                jobs=[]
                for numberOfStations in zones:
                    for tankThreshold in tt:
                        if(tankThreshold<0 and BestEffort==False): continue
                        nsimulations +=1
                        
                        policy, foutname = foutname(BestEffort,algorithm,AvaiableChargingStations,numberOfStations,tankThreshold)
                        
                        RechargingStation_Zones = loadRecharing(algorithm, numberOfStations)
                        p = Process(target=RunSim,args = (algorithm,policy,numberOfStations,AvaiableChargingStations,
                                                          tankThreshold,walkingTreshold,ZoneCars,RechargingStation_Zones,          
                                                          Stamps_Events,DistancesFrom_Zone_Ordered,None,-1,foutname))
                        jobs.append(p)
                        p.start()
                for proc in jobs:
                    proc.join()
                
    

    b = datetime.datetime.now()    
    c = (b - aglobal).total_seconds()                
    
    print("Run %d Simulations took %d seconds"%(nsimulations,c))
    return 
        
main()

