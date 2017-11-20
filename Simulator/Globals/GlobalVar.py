'''
Created on 13/nov/2017

@author: dgiordan
'''

import sys
import os
p = os.path.abspath('..')
sys.path.append(p+"/")


minLon = 7.598078
MaxLon = 7.731860
minLat = 45.007341
MaxLat = 45.109600

CaselleCentralLat = 45.18843
CaselleCentralLon = 7.6435


CorrectiveFactor = 1#.88
    


shiftLat500m = 0.0045
shiftLon500m = 0.00637

shiftLat250m = shiftLat500m/2
shiftLon250m = shiftLon500m/2


NColumns = int((MaxLon-minLon)/shiftLon250m)
Nrows = int((MaxLat-minLat)/shiftLat250m)
MaxIndex = Nrows*NColumns-1


ShiftLon = (MaxLon-minLon)/NColumns
ShiftLat = (MaxLat-minLat)/Nrows



CaselleMaxLat = CaselleCentralLat + shiftLat250m/2
CaselleMaxLon = CaselleCentralLon + shiftLon250m/2
CaselleminLat = CaselleCentralLat - shiftLat250m/2
CaselleminLon = CaselleCentralLon + shiftLon250m/2

provider="enjoy"

initDataSet = "###initDataSet###"



