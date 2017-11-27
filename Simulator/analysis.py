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

def compose_path(provider, alg, z, tt):
	return p + "/output/"+provider+"_"+str(alg)+"_"+str(z)+"_"+str(tt)+".txt"


def load_data(provider, algorithms, zones, tt ):
    settings = []
    myData = pd.DataFrame(columns=["algorithm", "zones", "deaths"])
    i=0
    
    for algorithm in algorithms:
        for z in zones:
            for t in tt:
                path = compose_path(provider, algorithm, z, t)
                try:
                    f = open(path)
                    d = {}
                    for j in range(5):
                        line=f.readline()
                        line = line.split(":")
                        d[line[0]] = line[1]
                    settings.append(d)
#                    print ("*", d)
                    
                    
                    
                    df = pd.read_csv(path, skiprows=[0,1,2,3,4,5], header=0, sep=";")

                    
                    if len(d)>0:
                        s= pd.Series()
                        s["typeE"] = len(df[df["Type"]=='e'])
                        s["typeS"] = len(df[df["Type"]=='s'])
                        
                        s["provider"] = provider
                        s["tankThreshold"] = t
                        s["zones"] = z
                        s["algorithm"] = algorithm
                        
                        s["avgWalkedDistance"] = df[
                                (df["Type"]=='e') & 
                                (df["Distance"]>0)].Distance.mean()
                        
                        s["medianWalkedDistance"] = df[
                                (df["Type"]=='e') & 
                                (df["Distance"]>0)].Distance.median()
                        
                        s["medianSOC"] = df.Lvl.median()
                        s["meanSOC"] = df.Lvl.mean()
                        
                        s["amountRecharge"] = len(df[df["Recharged"]==True])
                        s["amountRechargePerc"] = s["amountRecharge"]*100 / s["typeE"]
                        
                        
                        s["deaths"] = len(df[df["Lvl"]< 0])                                                


                        s["tot"] = len(df)
                        
                        s["reroute"] = len(df[
                                (df["Type"]=='e') & 
                                (df["Distance"]>0)])
                        
                        s["reroutePerc"] = s["reroute"]*100/s["typeE"]
                        
                        
                        
                        myData = myData.append(s, ignore_index=True)
                        
                        
                        
                except:
                    print(path)
    return settings, myData


zones =  list(range(10,85,5))
zones.append(120)
zones.append(160)
tt = [0,5,10,15,20, 25,30, 35,40,45,50]
#settings, myData = load_data("enjoy", ["max_time"], zones, tt )


def heatmap(df, provider, algorithm, metric):
    insideDF = df[(df["provider"] == provider) & (df["algorithm"]== algorithm) ]
    insideDF = insideDF[["zones", "tankThreshold", metric]]
#    return insideDF
    fontsize = 28
    
#    div_factor={
#            "reroutePerc":0.01,
#            "avgWalkedDistance": 1,
#            "medianWalkedDistance":1
#            }
    
    label = {
            "reroutePerc":"User re-routing [%]",
            "avgWalkedDistance": "[m]",
            "medianWalkedDistance": "[m]"
            }
    
    tt = df.tankThreshold.astype(int).unique()
    zones = df.zones.astype(int).unique()
    myVal = pd.DataFrame(index=tt, columns=zones)
    
    for t in tt:
        for z in zones:
            myVal.loc[t, z] = insideDF[ (insideDF["tankThreshold"]==t) & (insideDF["zones"]==z)].values[0][2] 
    
    myVal = myVal.astype(np.float64)
#    return myVal
        
    
                    
#    return myVal
                        
    fig, ax = plt.subplots(1,1, figsize=(20,10))
    heatmap = ax.pcolor(myVal, alpha=0.8)

    
    # turn off the frame
    ax.set_frame_on(False)
    
    # put the major ticks at the middle of each cell
    ax.set_yticks(np.arange(myVal.shape[0]) + 0.5, minor=False)
    ax.set_xticks(np.arange(myVal.shape[1]) + 0.5, minor=False)
    ax.set_xlabel("Zones", fontsize=fontsize)
    ax.set_ylabel("Tank Threshold", fontsize=fontsize)
    
    # want a more natural, table-like display
#    ax.invert_yaxis()
#    ax.xaxis.tick_top()
    
    # Set the labels
    ax.set_xticklabels(myVal.columns, minor=False)
    ax.set_yticklabels(myVal.index, minor=False)
    
    ax.grid(False)
    
    # Turn off all the ticks
    ax = plt.gca()
    
    for t in ax.xaxis.get_major_ticks():
        t.tick1On = False
        t.tick2On = False
    for t in ax.yaxis.get_major_ticks():
        t.tick1On = False
        t.tick2On = False
        
    cbar = fig.colorbar(heatmap)
    
    for y in range(myVal.shape[0]):
        for x in range(myVal.shape[1]):
            plt.text(x + 0.5, y + 0.5, '%.2f' % myVal.iloc[y][zones[x]],
                     horizontalalignment='center',
                     verticalalignment='center',
                 )
#    cbar.ax.set_xticklabels()  # horizontal colorbar
            
    savingPath = "/home/mc/paper/figures/heatmaps/"+\
            provider +"_"+\
            algorithm +"_"+\
            metric
            
    plt.savefig(savingPath, bbox_inches='tight')
            

    
    return myVal



zzz = heatmap(myData, "enjoy", "max_time", "avgWalkedDistance")
zzz = heatmap(myData, "enjoy", "max_time", "reroutePerc")
zzz = heatmap(myData, "enjoy", "max_time", "medianWalkedDistance")
    

#init_id =  [292, 47, 448, 57, 243, 280, 261, 452, 52, 311, 377, 5, 387, 153, 374, 339, 310, 240, 176, 215]
#final_id = [292, 47, 447, 58, 244, 301, 261, 431, 73, 310, 376, 6, 387, 132, 393, 298, 307, 200, 176, 216]
#
#def standardize(myCoords):
#    return str(myCoords[0])+","+str(myCoords[1])+"\n"
#
#f = open("/home/mc/init_id.txt", "w")
#f.write("icon,long_init,lat_init\n")
#for myId in init_id:
#    f.write("1," + standardize(zoneIDtoCoordinates(myId)))
#f.close()
#
#f = open("/home/mc/final_id.txt", "w")
#f.write("icon,long_final, lat_final\n")
#for myId in final_id:
#    f.write("2," + standardize(zoneIDtoCoordinates(myId)))
#f.close()
#
#
##df = pd.read_csv("/home/mc/init_id.txt", header=0)
##df2 = pd.read_csv("/home/mc/final_id.txt", header=0)
##df[["long_final", "lat_final"]] = df2
###df[[""] = df2 ["lat_final"]
#df.to_csv("/home/mc/coords_txt")









