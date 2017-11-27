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
    

    ##TO AVOID: "OSError: [Errno 24] Too many open files"     
    bashCommand = "ulimit -n 32768"
    import subprocess
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    process.communicate()
    ###
    
    walkingTreshold = 1000000#int(sys.argv[4]) # in [m]

    zoneEnjoy = 220

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


    
    a = datetime.datetime.now()    
    global RechargingStation_Zones
    #RechargingStation_Zones = loadRecharing(algorithm, provider, numberOfStations)
    b = datetime.datetime.now()    
    c = (b - a).total_seconds()
    print("End Load Recharging: "+str(int(c)))


    simulations_parameters = [1]
    
    
    #simulation 1
    
    numberOfStations =20#len(RechargingStation_Zones)#int(sys.argv[1])
    algorithm = "custom"#str(sys.argv[2])
    tankThreshold = 20#int(sys.argv[3]) # in [%]

    jobs = []


    RechargingStation_Zones = []
    
    while len(RechargingStation_Zones)<numberOfStations:
        rn = np.random.randint(NColumns*Nrows, size = 1)[0]
        if(rn not in RechargingStation_Zones): RechargingStation_Zones.append(rn)
    
    '''
    for k in range(0,1):    
        
        RechargingStation_Zones = [i for i in range(0,40)]
        
        p = Process(target=RunSim,args = (algorithm,numberOfStations,tankThreshold,walkingTreshold,ZoneCars,Stamps_Events,\
                                           RechargingStation_Zones,DistancesFrom_Zone_Ordered,return_dict,k))
    
        jobs.append(p)
        p.start()
        
    for proc in jobs:
        proc.join()'''
    
    
    results = ""
    k=0
    step=0
    manager = multiprocessing.Manager()

    while 1:
        
        return_dict = manager.dict()
               
        myindex=np.random.randint(len(RechargingStation_Zones), size = 1)[0]
        #print("myind "+str(myindex))
        ID=RechargingStation_Zones[myindex]
        #print("pollo "+str(ID))
        #print("rz")
        #print(RechargingStation_Zones)
        retv = zoneIDtoMatrixCoordinates(ID) 
        xy= [retv[1],retv[2]]
        IDn=-1

        xynew = {}
        xynew[0]=[xy[0]-1,xy[1]]
        xynew[1]=[xy[0],xy[1]-1]
        xynew[2]=[xy[0]+1,xy[1]]
        xynew[3]=[xy[0],xy[1]+1]

        RechargingStation_Zones_new = {}
        for i in range(0,len(xynew)):
            IDn=MatrixCoordinatesToID(xynew[i][0],xynew[i][1])
            if(IDn>0 and IDn not in RechargingStation_Zones):
                RechargingStation_Zones_new[i]=RechargingStation_Zones.copy()
                RechargingStation_Zones_new[i][myindex]=IDn
        
        #print("Number of threads: "+str(len(RechargingStation_Zones_new)))
        for i in RechargingStation_Zones_new:
            
            p = Process(target=RunSim,args = (algorithm,numberOfStations,tankThreshold,walkingTreshold,ZoneCars,Stamps_Events,\
                                           RechargingStation_Zones_new[i],DistancesFrom_Zone_Ordered,return_dict,i))
            k+=1
            jobs.append(p)
            p.start()
        
        
        for proc in jobs:
            proc.join()


        
        for val in return_dict.values():
            new_results = val
            print("\nNEW STEP")
            print(RechargingStation_Zones_new[int(new_results["ProcessID"])])
            print(new_results)
            if results == "" or (new_results["PercDeath"] <=results["PercDeath"] and new_results["MeanMeterEnd"]< results["MeanMeterEnd"]):

                fout = open("../output/best_solutions.txt","a")
                RechargingStation_Zones=RechargingStation_Zones_new[int(new_results["ProcessID"])].copy()
                print("\nNEW BEST SOLUTION FOUND")
                print("**********************************************************************")
                if(results!=""):
                    print("Old: %.2f %.2f"%(results["PercDeath"],results["MeanMeterEnd"]))
                print("New: %.2f %.2f"%(new_results["PercDeath"],new_results["MeanMeterEnd"]))
                print("**********************************************************************")
                
                fout.write("\nNEW BEST SOLUTION FOUND\n")
                fout.write("**********************************************************************\n")
                fout.write("Nsteps: %d"%step+"\n")
                if(results!=""):
                    fout.write("Old: %.2f %.2f\n"%(results["PercDeath"],results["MeanMeterEnd"]))
                fout.write("New: %.2f %.2f\n"%(new_results["PercDeath"],new_results["MeanMeterEnd"]))
                fout.write(str(RechargingStation_Zones)+"\n")
                fout.write(str(results)+"\n")
                fout.write("**********************************************************************\n")
                fout.close()

                results=new_results.copy()
                print(RechargingStation_Zones)
                print(results)

        step+=1



    #PercRerouteEnd, PercRerouteStart, PercRecharge,PercDeath, MedianMeterEnd, MeanMeterEnd, MedianMeterStart, MeanMeterStart, NEnd, NStart = \
    #        RunSim(algorithm,numberOfStations,tankThreshold,walkingTreshold,ZoneCars,Stamps_Events,RechargingStation_Zones,DistancesFrom_Zone_Ordered)

    #print("PercRerouteEnd, PercRerouteStart, PercRecharge, PercDeath, MedianMeterEnd, MeanMeterEnd, MedianMeterStart, MeanMeterStart, NEnd, NStart")
    #print(PercRerouteEnd, PercRerouteStart, PercRecharge,PercDeath, MedianMeterEnd, MeanMeterEnd, MedianMeterStart, MeanMeterStart, NEnd, NStart)
    
    #PercRerouteEnd, PercRerouteStart, PercRecharge,PercDeath, MedianMeterEnd, MeanMeterEnd, MedianMeterStart, MeanMeterStart, NEnd, NStart = \
    #        RunSim(algorithm,numberOfStations,tankThreshold,walkingTreshold,ZoneCars,Stamps_Events,RechargingStation_Zones,DistancesFrom_Zone_Ordered)

    #print("PercRerouteEnd, PercRerouteStart, PercRecharge, PercDeath, MedianMeterEnd, MeanMeterEnd, MedianMeterStart, MeanMeterStart, NEnd, NStart")
    #print(PercRerouteEnd, PercRerouteStart, PercRecharge,PercDeath, MedianMeterEnd, MeanMeterEnd, MedianMeterStart, MeanMeterStart, NEnd, NStart)

main()

