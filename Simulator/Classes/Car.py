'''
Created on 13/nov/2017

@author: dgiordan
'''
import sys
import os

from Simulator.Globals.SupportFunctions import haversine

from Simulator.Globals.GlobalVar import *



class Car(object):
    
    def __init__(self, provider, ID):
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

    def setStartPosition(self, BookingStarting_Position):
        
        self.StartBookingPosition = BookingStarting_Position
        
        return

    def setStartRecharge(self, StartRecharge):
        
        self.StartRecharge = StartRecharge
        
        return
    
    def EvalCurrentCapacity(self, CurrentStamp):
        kw = 2.0
        starting_value = self.BatteryCurrentCapacity
        duration = (CurrentStamp-self.StartRecharge)/(60.0/60.0) #in hour
        delta_c = duration * kw
        if (self.BatteryCurrentCapacity + delta_c <= self.BatteryMaxCapacity):
            return delta_c, self.BatteryCurrentCapacity + delta_c

        return self.BatteryMaxCapacity-starting_value, self.BatteryMaxCapacity
    
    def Recharge(self, EndRecharge):

        delta_c = -1 
        start_recharge = -1

        # distance = haversine(1.1,1.2,1.2,1.3)
        if self.WasInRecharge:
            delta_c, self.BatteryCurrentCapacity = self.EvalCurrentCapacity(EndRecharge)
            start_recharge = self.StartRecharge
            
        self.WasInRecharge = False
        self.StartRecharge = -1
        
        return delta_c, start_recharge

    def Discharge(self, BookingEndPosition):
        s = self.StartBookingPosition
        d = BookingEndPosition
        distance = 1000#haversine(s[0],s[1],d[0],d[1])*CorrectiveFactor
        
        dist_km = distance/1000
        dc = dist_km * self.kwh_km

        self.BatteryCurrentCapacity = self.BatteryCurrentCapacity - dc
        if self.BatteryCurrentCapacity <=0 :
            self.BatteryCurrentCapacity = -0.001

        return dc, distance

    def getBatteryLvl(self, Stamp = False):
        #BCC = local battery current capacity
        delta_c, BCC = self.EvalCurrentCapacity(Stamp)
        
        if Stamp != False:
            return BCC/self.BatteryMaxCapacity*100
        
        return self.BatteryCurrentCapacity/self.BatteryMaxCapacity*100
    
    def getID(self):
        
        return self.ID
    
    def IsFirstBooking(self):
        
        self.FirstRental+=1
        if(self.FirstRental==1): return True
        
        return False

    def getBatterCurrentCapacity(self):
        
        return self.BatteryCurrentCapacity

    def resetFields(self):

        self.BatteryCurrentCapacity = self.BatteryMaxCapacity 
        self.NumRentals = 0
        self.WasInRecharge = False
        self.StartRecharge = 0 #stamp
        self.StartBookingPosition = 0 #posizione
        self.FirstRental = 0

        #print("Reset")
        return