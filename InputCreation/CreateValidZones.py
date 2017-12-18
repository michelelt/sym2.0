import sys
import os

p = os.path.abspath('..')
sys.path.append(p+"/")

from Simulator.Globals.SupportFunctions import *
from Simulator.Globals.GlobalVar import *

import pandas as pd

import pickle
import collections
from geopy.geocoders import Nominatim

import datetime
#import tzlocal  # $ pip install tzlocal

dataset_bookings=[]
dict_bookings={} #dictionary keys (timestamp), inside is a list of objects events. (events without timestamp)_
dict_bookings_short = {}
id_events = {}


def main():
    # d = ReloadZonesCars()
    readConfigFile()

    collection="enjoy_PermanentBookings"
    if provider == "car2go":
        collection = "PermanentBookings"
    enjoy_bookings = setup_mongodb(collection)
    bookings = enjoy_bookings.find({"city": city,
                                    "init_time" :{"$gt": initDate , "$lt": finalDate}})

    print (bookings.count())
    
    #geolocator = Nominatim()    
    #location = geolocator.geocode("Torino")
    #baselon = location.longitude
    #baselat = location.latitude

   
    matrix = {}
    Discarded=0
    for booking in bookings:

        #if(i>1000): break
        initt =  booking['init_time'] 
        finalt= booking['final_time']
        duration = finalt - initt
        coords = booking['origin_destination']['coordinates']
        lon1 = coords[0][0]
        lat1 = coords[0][1]
        lon2 = coords[1][0]
        lat2 = coords[1][1]

        d2 = haversine(lon1, lat1, lon2, lat2)

        if duration > 120 and duration < 3600 and d2 > 500:
            if checkPerimeter(lat1, lon1) and checkPerimeter(lat2, lon2):
                ind = coordinates_to_index(coords[1])
                matrix_coords = zoneIDtoMatrixCoordinates(ind)
                if (matrix_coords not in matrix):
                    matrix[matrix_coords] = [0, 0, 0]
                matrix[matrix_coords][0] += 1
                matrix[matrix_coords][1] += int(finalt) - int(initt)
            else:
                Discarded += 1

    validzones = open("../input/"+provider+"_ValidZones.txt", "w")
    validzones.write("Lon; Lat; NParkings; SumTime; AvgTime\n")

    for val in matrix:
        c0 = val[0]
        c3 = val[3]
        c4 = val[4]

        coords2 = "%d %.4f %.4f"%(c0,c3,c4)

        avgpark = float(matrix[val][1])/float(matrix[val][0])

        validzones.write(coords2+ " %d %d %d\n" %(matrix[val][0], matrix[val][1], avgpark))

    print ("discarded:", Discarded)
    print("End")
        
main()