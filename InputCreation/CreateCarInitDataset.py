import sys
import os
p = os.path.abspath('..')
sys.path.append(p+"/")

import pickle
from geopy.geocoders import Nominatim
from Simulator.Globals.SupportFunctions import * 
from Simulator.Globals.GlobalVar import * 
from Simulator.Classes.PlatesData import PlatesData 
import Simulator


dict_plates={} #dictionary keys (plate), inside is a list of objects first appearance

def main():


    collection="enjoy_PermanentParkings"
    if(provider == "car2go"):
        collection = "PermanentParkings"
        
    collection_parkings = setup_mongodb(collection)
    
    parkings = collection_parkings.find({"city": city, "init_time" : {"$gt" : initDate, "$lt": finalDate}});
    #geolocator = Nominatim()    
    #location = geolocator.geocode("Torino")
    #baselon = location.longitude
    #baselat = location.latitude
    currentFleetSize = 0
    for val in parkings:
            coords = val['loc']['coordinates']
            lon1 = coords[0]
            lat1 = coords[1]

            #d = haversine(baselon, baselat, lon1, lat1)


            
            # if( checkPerimeter(lat1, lon1) or
            #    (provider == "car2go" and checkCasellePerimeter(lat1, lon1)) and
            #     currentFleetSize <= FleetSize):
            if checkPerimeter(lat1, lon1) and currentFleetSize <= fleetSize:
                currentFleetSize += 1
                if val['plate'] not in dict_plates:
                    dict_plates[val['plate']] = PlatesData(val['init_time'], val["loc"]['coordinates'])
                else:
                    if dict_plates[val['plate']].timestamp >= val['init_time']: #se non erano in ordine nel dataset iniziale
                        dict_plates[val['plate']] = PlatesData(val['init_time'], val["loc"]['coordinates'])
            else:
                print("problem")

                
   '''
   allocare tutte le macchine poi vedi dove le piazza, magari ha senso allocarle tutte e considerare poi una flotta virtuale di sole x macchine
   '''

    print(len(dict_plates))

    
    '''fout = open("cords.csv","w")
    for plate in dict_plates:
        fout.write(plate+",%f"%dict_plates[plate].coordinates[0]+",%f"%dict_plates[plate].coordinates[1]+"\n")'''
    
    with open("../input/"+provider+"_plates_appeareance_obj.pkl", 'wb') as handle:
        pickle.dump(dict_plates,handle)



main()
