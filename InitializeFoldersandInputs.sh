#!/bin/bash

mkdir input
mkdir output
mkdir events

cd InputCreation

python3 CreateValidZones.py
python3 CreateCarInitDataset.py
python3 CreatePickleEventi.py 
python3 CreatePickleZoneDistance.py

