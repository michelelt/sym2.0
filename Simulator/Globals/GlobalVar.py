'''
Created on 13/nov/2017

@author: dgiordan
'''

import sys
import os
import pandas as pd
import time
import datetime

p = os.path.abspath("..")
sys.path.append(p+"/")


def init():

    global MaxLat, MaxLon, minLat, minLon, city, provider, initDate, finalDate, fleetSize
    global shiftLat500m, shiftLon500m, NColumns, NRows, MaxIndex, ShiftLon, ShiftLat

    MaxLat = 0
    MaxLon = 0
    minLat = 0
    minLon = 0
    city = 0
    provider = 0
    initDate = 0
    finalDate = 0
    fleetSize = 0
    CaselleCentralLat = 45.18843
    CaselleCentralLon = 7.6435

    CorrectiveFactor = 1#.88

    shiftLat500m = 0.0045
    shiftLon500m = 0.00637

    '''
    add /2 in order to have a zonization 250x250
    '''
    shiftLat250m = shiftLat500m
    shiftLon250m = shiftLon500m

    NColumns = 1
    NRows = 1
    MaxIndex = NRows*NColumns-1

    ShiftLon = (MaxLon-minLon)/NColumns
    ShiftLat = (MaxLat-minLat)/NRows

    return


# '''
# add /2 in order to have a zonization 250x250
# '''
# CaselleMaxLat = CaselleCentralLat + ShiftLat
# CaselleMaxLon = CaselleCentralLon + ShiftLon
# CaselleminLat = CaselleCentralLat - ShiftLat
# CaselleminLon = CaselleCentralLon + ShiftLon

# initDataSet = "###initDataSet###"






