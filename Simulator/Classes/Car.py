'''
Created on 13/nov/2017

@author: dgiordan
'''
import sys
import os
from Simulator.Globals.GlobalVar import CorrectiveFactor
p = os.path.abspath('..')
sys.path.append(p+"/")

from  Simulator.Globals.SupportFunctions import haversine

class Car(object):
    
    def __init__(self, provider,ID):

        self.ID = ID

        self.BatteryMaxCapacity = 25.2
        self.kwh_km = 0.188
        if provider == 'car2go':
            self.BatteryMaxCapacity = 17.6
            self.kwh_km = 0.13

        self.BatteryCurrentCapacity = self.BatteryMaxCapacity 
        self.NumRentals = 0
        self.WasInRecharge = False
        self.StartRecharge = 0 #stamp
        self.StartBookingPosition = 0 #posizione
        self.FirstRental = 0
    
    def setInStation(self):
        
        self.WasInRecharge = True
        
        return
    
    def setStartPosition(self,BookingStarting_Position):
        
        self.StartBookingPosition = BookingStarting_Position
        
        return

    def setStartRecharge(self,StartRecharge):
        
        self.StartRecharge = StartRecharge
        
        return
    
    def Recharge(self,EndRecharge):

        kw = 2.0
        delta_c = -1 
        if(self.WasInRecharge):

            duration = EndRecharge-self.StartRecharge/60.0/60.0 #in hour
            delta_c = duration * kw
            if (self.BatteryCurrentCapacity + delta_c <= self.BatteryMaxCapacity):
                self.BatteryCurrentCapacity += delta_c
            else:
                self.BatteryCurrentCapacity  = self.BatteryMaxCapacity

        self.WasInRecharge = False
        return delta_c,self.StartRecharge
    
    def Discharge(self,BookingEndPosition):
        
        s = self.StartBookingPosition
        d = BookingEndPosition
        distance = haversine(s[0],s[1],d[0],d[1])*CorrectiveFactor
        
        dist_km = distance/1000
        dc = dist_km * self.kwh_km

        self.BatteryCurrentCapacity = self.BatteryCurrentCapacity - dc

        return dc, distance
    

    def getBatteryLvl(self):
        
        return self.BatteryCurrentCapacity/self.BatteryMaxCapacity*100
    
    def getID(self):
        
        return self.ID
    
    def IsFirstBooking(self):
        
        self.FirstRental+=1
        if(self.FirstRental==1): return True
        
        return False
