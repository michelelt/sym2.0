import sys
import os
p = os.path.abspath('..')
sys.path.append(p+"/")

import pickle
from geopy.geocoders import Nominatim
from Simulator.Classes.PlatesData import PlatesData 
import Simulator
import Simulator.Globals.SupportFunctions as sf
import Simulator.Globals.GlobalVar as gv
gv.init()
sf.assingVariables()


dict_plates={} #dictionary keys (plate), inside is a list of objects first appearance

def main():


    collection="enjoy_PermanentParkings"
    if gv.provider == "car2go":
        collection = "PermanentParkings"
        
    collection_parkings = sf.setup_mongodb(collection)
    
    parkings = collection_parkings.find({"city": gv.city, "init_time": {"$gt": gv.initDate, "$lt": gv.finalDate}})

    currentFleetSize = 0
    for val in parkings:
            coords = val['loc']['coordinates']
            lon1 = coords[0]
            lat1 = coords[1]
            #d = haversine(baselon, baselat, lon1, lat1)
            # if( checkPerimeter(lat1, lon1) or
            #    (provider == "car2go" and checkCasellePerimeter(lat1, lon1)) and
            #     currentFleetSize <= FleetSize):
            if sf.checkPerimeter(lat1, lon1):
                currentFleetSize += 1
                if val['plate'] not in dict_plates:
                    dict_plates[val['plate']] = PlatesData(val['init_time'], val["loc"]['coordinates'])
                else:
                    if dict_plates[val['plate']].timestamp >= val['init_time']: #se non erano in ordine nel dataset iniziale
                        dict_plates[val['plate']] = PlatesData(val['init_time'], val["loc"]['coordinates'])
            else:
                print("problem")

    print("CCID", "Seen cars:", len(dict_plates))

    
    with open("../input/" + gv.provider + "_plates_appeareance_obj.pkl", 'wb') as handle:
        pickle.dump(dict_plates, handle)

    print ("CCID, col:", gv.NColumns, " row:", gv.NRows)
    print ("CCID, End")

main()
