#!/bin/bash

if [ ! -d ./input ]; then
    mkdir input
fi

if [ ! -d ./output ]; then
    mkdir output
fi

if [ ! -d ./events ]; then
    mkdir events
fi

cd InputCreation
python3 DowloadCitiesBorders.py
#cd ../Simulator/Globals/
#python3 GlobalVar.py
#cd ../../InputCreation
python3 CreateValidZones.py
python3 CreateCarInitDataset.py
#python3 CreatePickleEventi.py
#python3 CreatePickleZoneDistance.py