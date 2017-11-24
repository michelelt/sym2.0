#!/usr/bin/env python3

import numpy as np
import pickle
import sys
import os
p = os.path.abspath('..')
sys.path.append(p+"/")

from Simulator.Globals.GlobalVar import *
from Simulator.Globals.SupportFunctions import *
import datetime
import click
import csv
import sys

path = p + "/Simulator/"




zones =  list(range(10,85,5))
zones.append(120)
zones.append(160)
tt = [0,5,10,15,20, 25,30, 35,40,45,50]

alg = sys.argv[1]

def command_str(z, tt, alg):
	return path + "RunSim.py " + str(z) +" "+ alg + " " + str(t) + " 5000 & "
	
myStr=""
i=0
for z in zones:
	for t in tt :
			myStr += command_str(z, tt, alg)
			i=i+1

os.system(myStr)
