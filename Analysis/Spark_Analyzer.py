from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext
import numpy as np
import pandas as pd
import os

header = ["Provider","Policy","Algorithm","TankThreshold","Zones","Acs","WalkingThreshold","TypeS", "TypeE",
          "AvgWalkedDistance","MedianWalkedDistance", "AvgWalkedDistanceGlobal", "MedianWalkedDistanceGlobal",
          "AvgSOC", "MedianSOC", "AmountRecharge","AmountRechargeForced","AmountRechargeForcedFail",
          "AmountRechargeBestEffort", "AmountRechargePerc", "AvgTimeInStation", "MedianTimeInStation",
          "Deaths","Reroute","ReroutePerc","ReroutePercofRecharge"]


def dict_to_str(s):
    
    OutStr = ""
    for val in header:
        if(type(s[val]) is int):
            OutStr +="%d "%s[val]
        elif(type(s[val]) is str):
            OutStr +="%s "%s[val]
        else:
            OutStr +="%.2f "%s[val]

    OutStr =OutStr[:-1]+"\n"
    
    
    return OutStr

def mapf(s):

    sp = s.split(";")

    if(sp[0] != 's' and sp[0] != 'e'):
        return ("DELETE",[])    
    
    key = str(sp[14])
    values=[]
    if(sp[0]=="s"):    
        values = [sp[0],"-","-",float(sp[4]),float(sp[5]),float(sp[7]),int(sp[8]),int(sp[9]),"-","-"]
    else:
        values = [sp[0],bool(sp[1]),bool(sp[2]),float(sp[4]),float(sp[5]),"-","-",int(sp[9]),float(sp[12]),int(sp[13])]    
    #Type ToRecharge Recharged ID Lvl Distance Iter Recharge StartRecharge Stamp EventCoords ZoneC Discharge  TripDistance  FileID
    #0     1            2       3 4     5       6     7        8            9        10        11    12        13            14

    return (key,values)


def mapf2(x):



    df = pd.DataFrame()
    
    key = x[0]
    keysplit=key.split("_")

    values = list(x[1])
    

    labels = ["Type", "ToRecharge", "Recharged", "Lvl", "Distance", "Recharge", "StartRecharge", "Stamp", "Discharge", "TripDistance"]

    xv = [[] for i in range(0,len(labels))]    
    for val in values:
        for i in range(0,len(labels)):
            xv[i].append(val[i])

    for i in range(0,len(labels)):
        df[labels[i]] = xv[i]
    
    s = {}
    
    s["Provider"] = keysplit[0]
    s["Policy"] = keysplit[1]
    s["Algorithm"] = keysplit[2]
    s["Zones"] = keysplit[3]
    s["Acs"] = keysplit[4]
    s["TankThreshold"] = keysplit[5]
    s["WalkingThreshold"] = keysplit[6]

    s["TypeS"] = len(df[df["Type"]=='s'])                            
    s["TypeE"] = len(df[df["Type"]=='e'])
    
    s["AvgWalkedDistance"] = df[
            (df["Type"]=='e') &
            (df["Distance"]>0)].Distance.mean()
    s["MedianWalkedDistance"] = df[
            (df["Type"]=='e')& 
            (df["Distance"]>0)].Distance.median()   
                                         
    s["AvgWalkedDistanceGlobal"] = df[
            (df["Type"]=='e')].Distance.mean()                                
    s["MedianWalkedDistanceGlobal"] = df[
            (df["Type"]=='e')].Distance.median()                                
            
    s["AvgSOC"] = df[(df["Type"]=='e')].Lvl.mean()
    s["MedianSOC"] = df[(df["Type"]=='e')].Lvl.median()
    s["AmountRecharge"] = len(df[
                               (df["Type"]=='e') &
                               (df["Recharged"]==True)])
    s["AmountRechargeForced"] = len(df[
                              (df["Type"]=='e') &
                              (df["Recharged"]==True) & 
                              (df["ToRecharge"]==True)])
    s["AmountRechargeForcedFail"] = len(df[
                              (df["Type"]=='e') &
                              (df["Recharged"]==False) & 
                              (df["ToRecharge"]==True)])
    s["AmountRechargeBestEffort"] = len(df[
                              (df["Type"]=='e') &
                              (df["Recharged"]==True) & 
                              (df["ToRecharge"]==False)])
    s["AmountRechargePerc"] = s["AmountRecharge"]*100 / s["TypeE"]

    TmpRes                    = df[
                              (df["Type"]=='s') & 
                              (df["StartRecharge"]>0)]                        

    
    s["AvgTimeInStation"]  = (TmpRes['Stamp'] - TmpRes['StartRecharge']).mean()
    
    s["MedianTimeInStation"]  = (TmpRes['Stamp'] - TmpRes['StartRecharge']).median()
            
    s["Deaths"] = len(df[df["Lvl"]< 0])                                                
    s["Reroute"] = len(df[
            (df["Type"]=='e') & 
            (df["Distance"]>0)])
    s["ReroutePerc"] = s["Reroute"]*100/s["TypeE"]
    s["ReroutePercofRecharge"] = s["Reroute"]*100/s["AmountRecharge"] 
    
    return (key,s)


def main():
    
    # establish the spark context
    conf = SparkConf().setAppName("Carsharing_BigDataAnalytics")

    sc = SparkContext(conf=conf)

    text_file = sc.textFile("hdfs:///user/giordano/Simulator/output/*")
    counts = text_file.map(mapf). \
    filter(lambda x: x[0]!="DELETE"). \
    groupByKey().map(mapf2).collectAsMap()

    HederStr = ""
    for val in header:
        HederStr+=val+" "
    
    HederStr =HederStr[:-1]+"\n"
    
    fout = open("spark_scripts/output/out_analysis.txt","w")
    
    fout.write(HederStr)
    for val in counts:
        outs = dict_to_str(counts[val])
        fout.write(outs)            
    return

main()