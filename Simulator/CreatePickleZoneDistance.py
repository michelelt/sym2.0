import sys
import os
p = os.path.abspath('..')
sys.path.append(p+"/")

import pickle
import operator
from Simulator.Classes.Distance import Distance
from Simulator.Classes.Car import Car
from Simulator.Classes.Zone import Zone
from Simulator.Globals.GlobalVar import *
from Simulator.Globals.SupportFunctions import *
from geopy.geocoders import Nominatim



def EvalDistance(i,j):
    Xi = i%NColumns
    Yi = int(i/NColumns)
    
    Xj = j%NColumns
    Yj = int(j/NColumns)
    


    CentalLoni = (Xi+0.5)*ShiftLon+minLon
    CentalLati = (Yi+0.5)*ShiftLat+minLat
    CentalLonj = (Xj+0.5)*ShiftLon+minLon
    CentalLatj = (Yj+0.5)*ShiftLat+minLat
        
    dh = haversine(CentalLoni, CentalLati, CentalLonj, CentalLatj)

    de = sqrt(pow((Xi-Xj),2)+pow((Yi-Yj),2)) 

    return de,dh

def AppendCaselle(i,ZoneDistances,ZoneID_Zone):


    Xi = i%NColumns
    Yi = int(i/NColumns)
    CentalLon = (Xi+0.5)*ShiftLon+minLon
    CentalLat = (Yi+0.5)*ShiftLat+minLat
    Caselle=NColumns*Nrows
    de, dh = EvalDistance(i, Caselle*3)
    dh = haversine(CentalLon, CentalLat, CaselleCentralLon, CaselleCentralLat)
    RealDistance = dh
    if(de not in ZoneDistances[i]):
        ZoneDistances[i][de] = Distance(RealDistance) 
    ZoneDistances[i][de].appendZone(ZoneID_Zone[Caselle])
    if(i!=Caselle):
        if(de not in ZoneDistances[Caselle]):
            ZoneDistances[Caselle][de] = Distance(RealDistance) 
        ZoneDistances[Caselle][de].appendZone(ZoneID_Zone[i])

    return

def main():

    ZoneID_Zone = {}   
    ZoneDistances = {}
    ZoneNumCars = [0 for i in range(0,NColumns*Nrows+1)]  
    
    
    #geolocator = Nominatim()    
    #location = geolocator.geocode("Torino")
    #baselon = location.longitude
    #baselat = location.latitude


    

    DictPlates = pickle.load( open( "../input/"+provider+"_plates_appeareance_obj.pkl", "rb" ) )
    for plate in DictPlates:
        CellIndex = coordinates_to_index(DictPlates[plate].coordinates)
        ZoneNumCars[CellIndex]+=1
       

    k = 0   
    ZoneCars = {} 
    for i in range(0,NColumns*Nrows+1):
        #if(ZoneNumCars[i]>0): print(i,ZoneNumCars[i])
        ZoneDistances[i]={}
        
        CarVector = []
        for j in range(0,ZoneNumCars[i]):
            
            CarVector.append(Car(provider,k))
            k+=1        
        ZoneCars[i] = CarVector
        ZoneID_Zone[i]= Zone(i,CarVector)
        
    pickle.dump( ZoneCars, open( "../input/"+provider+"_ZoneCars.p", "wb" ) )

    print(NColumns,Nrows)

    return 0
    for i in range(0,NColumns*Nrows+1):
        for j in range(i,NColumns*Nrows):
            de, dh = EvalDistance(i, j)
            RealDistance = dh
            if(de not in ZoneDistances[i]):
                ZoneDistances[i][de] = Distance(RealDistance) 
            ZoneDistances[i][de].appendZone(ZoneID_Zone[j])
            if(i!=j):
                if(de not in ZoneDistances[j]):
                    ZoneDistances[j][de] = Distance(RealDistance) 
                ZoneDistances[j][de].appendZone(ZoneID_Zone[i])
        
        AppendCaselle(i,ZoneDistances,ZoneID_Zone)
            
    
    for i in range(0,len(ZoneDistances)):
        
        ZoneDistances[i] = sorted(ZoneDistances[i].items(), key=operator.itemgetter(0))
        
    
    
    pickle.dump( ZoneDistances, open( "../input/"+provider+"_ZoneDistances.p", "wb" ) )
    
    return
main()