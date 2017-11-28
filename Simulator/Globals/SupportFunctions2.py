'''
Created on 13/nov/2017

@author: dgiordan
'''

import pymongo
import ssl
from math import *
import sys
import os
p = os.path.abspath('..')
sys.path.append(p+"/")
import pandas as pd
import numpy as np
import random
import csv


from Simulator.Globals.GlobalVar import *
from Simulator.Classes.Zone import *

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    km = 6367 * c
    
    return int(km*1000)


