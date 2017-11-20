#!/usr/bin/env python3

import numpy as np
import pickle
import sys
import os
import csv
p = os.path.abspath('..')
sys.path.append(p+"/")
from Simulator.Globals.GlobalVar import *
from Simulator.Globals.SupportFunctions import *
import pandas as pd

import matplotlib.pyplot as plt

parametersDict = {}
csvfilePath = p+"/output/walk2.txt"

data = pd.read_csv(csvfilePath, skiprows=[0,1,2,3,4,5], header=0, sep=";")


### plot the distance missmatch in start and end ###
start_df = data[data["Type"]=='s']
end_df = data[data["Type"]=='e']

#fig, ax = plt.subplots(1,2, figsize=(30,10))
##
#ax[0].set_title("Distance on leaving", fontsize=28)
#ax[0].set_xlabel("Distances [km]")
#ax[0].set_ylabel("ECDF")
#ax[0].hist(data["Distance"].div(1000), bins=100, cumulative=True, normed=True)
#
#ax[1].set_title("Distance on arrival", fontsize=28)
#ax[1].set_xlabel("Distances [km]")
#ax[1].set_ylabel("ECDF")
#ax[1].hist(end_df["Distance"].div(1000), bins=100, cumulative=True, normed=True)


'''
### trip dist wen WT exceeds ###
'''
#fig, ax = plt.subplots(1,1, figsize=(20,10))
#wt_excedeed = data[(data["ToRecharge"]== True)]
#def f(a,b):
#    if (a == True and b == True):
#        return 1
#    elif (a == True and b == False):
#        return 0
#    else:
#        -1
#wt_excedeed["info"] = wt_excedeed.apply(lambda x : f(x["ToRecharge"], x["Recharged"]) , axis=1)
#ax.scatter(range(0, len(wt_excedeed["info"])), wt_excedeed["info"])


fig, ax = plt.subplots(1,1, figsize=(20,10))
wt_excedeed= data[data["WT_exceed"]==True]
ax.set_title("Trip dist when WT exceeds", fontsize=28)
ax.set_xlabel("Distances [km]")
ax.set_ylabel("ECDF")
ax.hist(wt_excedeed["TripDistance"].div(1000), bins=100, cumulative=True, normed=True)

#
#
#### cdf SoC `###
#fig, ax = plt.subplots(1,1, figsize=(20,10))
#ax.set_title("Average SoC", fontsize=28)
#ax.set_xlabel("SoC [%]")
#ax.set_ylabel("ECDF")
#ax.hist(data["Lvl"].div(1), bins=200, cumulative=True, normed=True)














