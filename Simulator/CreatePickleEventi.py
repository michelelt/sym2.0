import sys
import os
p = os.path.abspath('..')
sys.path.append(p+"/")
from Simulator.Globals.SupportFunctions import *
from Simulator.Classes.EventBook import EventBook  
from Simulator.Globals.GlobalVar import *


import pickle
import collections
from geopy.geocoders import Nominatim

      
dataset_bookings=[]
dict_bookings={} #dictionary keys (timestamp), inside is a list of objects events. (events without timestamp)_
dict_bookings_short = {}
id_events = {}



def main():
    


    collection="enjoy_PermanentBookings"
    if(provider == "car2go"):
        collection = "PermanentBookings"
    enjoy_bookings = setup_mongodb(collection)
    bookings = enjoy_bookings.find({"city": "Torino"});
    geolocator = Nominatim()    
    location = geolocator.geocode("Torino")
    #baselon = location.longitude
    #baselat = location.latitude

    
    i=0 #id del booking, numero progressivo
    
    NumEvents=0
    NumEventsFiltered=0
    Discarted=0
    for booking in bookings:
            initt =  booking['init_time'] 
            finalt= booking['final_time']
            duration = finalt - initt
            coords = booking['origin_destination']['coordinates']
            lon1 = coords[0][0]
            lat1 = coords[0][1]
            lon2 = coords[1][0]
            lat2 = coords[1][1]
            #d = haversine(baselon, baselat, lon2, lat2)
            #d1 = haversine(baselon, baselat, lon1, lat1)
            d2 = haversine(lon1, lat1, lon2, lat2)

            '''
            filtering on duration and distance
            '''
            if(duration > 120 and duration<3600 and d2>500):
                '''
                if coord inside the square or
                if CSO is car2go, check if the coords inside per or from or to Caselle
                '''
                if( 
                    checkPerimeter(lat1, lon1) and checkPerimeter(lat2, lon2) or
                   (
                    provider == "car2go" and  
                    ((checkPerimeter(lat1, lon1) and checkCasellePerimeter(lat2, lon2)) or
                    (
                        checkCasellePerimeter(lat1, lon1) and checkPerimeter(lat2, lon2))))): 
                    NumEvents+=1

                    ### event cration addressed per univoque id ###
                    id_events[i] = [booking['init_time'], booking['final_time'], ### timestamps
                    EventBook(i,"s",  booking["origin_destination"]['coordinates'][0]), ### evento bookings
                    EventBook(i ,"e", booking["origin_destination"]['coordinates'][1])]

                    ### Collection of TS connecting the TS - booking ID ###
                    if booking['init_time'] not in dict_bookings:
                        dict_bookings[booking['init_time']]=[]
                    dict_bookings[booking['init_time']].append([i,"s"])
                    
                    if booking['final_time'] not in dict_bookings:
                        dict_bookings[booking['final_time']]=[]
                    dict_bookings[booking['final_time']].append([i,"e"])        
                    i=i+1
                
                    ### ####
                    if(i<1000):
                        if booking['init_time'] not in dict_bookings_short:
                            dict_bookings_short[booking['init_time']]=[]
                        dict_bookings_short[booking['init_time']].append(EventBook(i,"s",  booking["origin_destination"]['coordinates'][0]))
                        if booking['final_time'] not in dict_bookings_short:
                            dict_bookings_short[booking['final_time']]=[]
                        dict_bookings_short[booking['final_time']].append(EventBook(i ,"e", booking["origin_destination"]['coordinates'][1]))  
            else:
                Discarted+=1   
                        
                    

    with open("../events/"+provider+"_dict_bookings.pkl", 'wb') as handle:
        pickle.dump( dict_bookings,handle)
    
    with open("../events/"+provider+"_id_events.pkl", 'wb') as handle:
        pickle.dump( id_events,handle)
    
    print("End Pickles")
    '''exit(0)
    
    dict_bookings= pickle.load( open( "../events/"+operator+"_dict_bookings.pkl", "rb" ) )
    id_events= pickle.load( open( "../events/"+operator+"_id_events.pkl", "rb" ) )
    '''
    print("Start")
    to_delete = []
    EventDeleted=0

    ### prevent outliers ###
    for stamp in dict_bookings:
        startbooking = 0
        for event in dict_bookings[stamp]:
            if(event[1]=="s"): startbooking+=1
        
        if(startbooking>30):
            EventDeleted+=startbooking
            to_delete.append(stamp)
        
    ### Removing the elements which are outliers ###    
    for stamp in to_delete:
        events_to_delete = []
        for event in dict_bookings[stamp]:
            if(event[1] == "s"): events_to_delete.append(event[0])
            
        for event in events_to_delete:
            InitTime = id_events[event][0]
            FinalTime = id_events[event][1]
            InitInd = dict_bookings[InitTime].index([event,"s"])
            FinalInd = dict_bookings[FinalTime].index([event,"e"])

            del  dict_bookings[InitTime][InitInd]
            del  dict_bookings[FinalTime][FinalInd]
            
    
        if(len(dict_bookings[stamp])==0):
            del dict_bookings[stamp]
    
    
    ### cerate definitvely the dict of dict of events ###
    for stamp in dict_bookings:
        for i in range(0,len(dict_bookings[stamp])):
            NumEventsFiltered+=1
            EventT = dict_bookings[stamp][i]
            if(EventT[1] == "s"): dict_bookings[stamp][i]=id_events[EventT[0]][2]
            else: dict_bookings[stamp][i]=id_events[EventT[0]][3]
            


    print(NumEventsFiltered+EventDeleted,NumEventsFiltered,EventDeleted,Discarted)
    
    ordered_dict_booking = collections.OrderedDict(sorted(dict_bookings.items()))
    ordered_dict_booking_short = collections.OrderedDict(sorted(dict_bookings_short.items()))
   

    with open("../events/"+provider+"_sorted_dict_events_obj.pkl", 'wb') as handle:
        pickle.dump( ordered_dict_booking,handle)

    with open("../events/"+provider+"_sorted_dict_events_obj_short.pkl", 'wb') as handle:
        pickle.dump( ordered_dict_booking_short,handle)
    


main()

'''
if(d<30000 and d1<30000 and d2<30000):
    min30+=1
'''