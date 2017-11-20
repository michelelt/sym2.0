'''
Created on 13/nov/2017

@author: dgiordan
'''
import sys
import os
p = os.path.abspath('..')
sys.path.append(p+"/")

from Simulator.Classes.Car import Car

class Zone(object):
      
    def __init__(self, ID, cars):
        
        self.AvaiableChargingStations = 6
        self.ID = ID
        self.Cars = cars
        self.RechargedCars = []
        self.NoOfRech = 0
        return
    
    '''
    RETURN THE MOST CHARGED CAR BETWEEN THE CHARGING ONES 
    '''
    def getBestRechargedCars(self,stamp):
        
        BestCar = ""

        for CarI in self.RechargedCars:
            if(BestCar == ""):
                BestCar = CarI    
            else:
                if(CarI.getBatteryLvl(stamp) > BestCar.getBatteryLvl(stamp)): BestCar = CarI  
    
        if(BestCar != ""): del self.RechargedCars[self.RechargedCars.index(BestCar)]
        
        return BestCar


    '''
    RETURN THE MOST CHARGED CAR among the NOT charing ones 
    '''
    def getBestCars(self):
        
        BestCar = ""

        for CarI in self.Cars:
            if(BestCar == ""):
                BestCar = CarI    
            else:
                if(CarI.getBatteryLvl() > BestCar.getBatteryLvl()): BestCar = CarI  
        
        if(BestCar != ""): del self.Cars[self.Cars.index(BestCar)]
        return BestCar
    
    '''
    Park the car somewhere
    '''
    def getAnyParking(self,CarToPark):
        
        self.Cars.append(CarToPark)
        
        return
    
    '''
    If it is possible, park the car in the rechargnig station, else do nothing
    '''
    def getParkingAtRechargingStations(self,CarToPark):
        
        if(len(self.RechargedCars) < self.AvaiableChargingStations):
            self.RechargedCars.append(CarToPark)
            return True
        
        return False

    def getNumRecCar(self):
        
        return len(self.RechargedCars)
        
    def getNumCar(self):
        
        return len(self.Cars)

    def incrNoOfRecharging(self):
        self.NoOfRech +=1

    def toString(self):
        return str(self.ID)+";"+str(self.NoOfRecharing)
