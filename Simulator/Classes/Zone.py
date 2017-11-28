'''
Created on 13/nov/2017

@author: dgiordan
'''
import sys
import os
p = os.path.abspath('..')
sys.path.append(p+"/")

from Simulator.Classes.Car import Car
from Simulator.Globals.GlobalVar import *

class Zone(object):
      
    def __init__(self, ID, cars):
        
        self.AvaiableChargingStations = 6
        self.ID = ID
        self.Cars = cars
        self.RechargedCars = []        
        return
        
    def getBestRechargedCars(self,Stamp):
        
        if(len(self.RechargedCars)==0): return ""
        
        BestCar = ""
        BestLvl = -1

        for CarI in self.RechargedCars:
            if(BestCar == ""):
                BestCar = CarI    
            else:
                CarILvl = CarI.getBatteryLvl(Stamp)
                if(CarILvl > BestLvl): 
                    BestCar = CarI
                    BestLvl = CarILvl
    
        if(BestCar != ""): del self.RechargedCars[self.RechargedCars.index(BestCar)]
        
        
        
        return BestCar
    
    def getBestCars(self):

        if(len(self.Cars)==0): return ""
        
        BestCar = ""

        for CarI in self.Cars:
            if(BestCar == ""):
                BestCar = CarI    
            else:
                if(CarI.getBatteryLvl() > BestCar.getBatteryLvl()): BestCar = CarI  
        
        if(BestCar != ""): del self.Cars[self.Cars.index(BestCar)]
        return BestCar
    
    def getAnyParking(self,CarToPark):
        
        self.Cars.append(CarToPark)
        
        return
    
    def getParkingAtRechargingStations(self,CarToPark):
        
        if(len(self.RechargedCars) < self.AvaiableChargingStations):
            self.RechargedCars.append(CarToPark)
            return True
        
        return False

    def getNumRecCar(self):
        
        return len(self.RechargedCars)
        
    def getNumCar(self):
        
        return len(self.Cars)
    
    
    def setCars(self,cars):

        self.RechargedCars = []        
        
        CarVector = []
        for CarI in cars:
            CarVector.append(Car(provider,CarI.ID))        
        
        self.Cars = CarVector

        
        return

    def setAvaiableChargingStations(self, n):
        self.AvaiableChargingStations = n
        return

    def getAvaiableChargingStations(self):
        return self.AvaiableChargingStations