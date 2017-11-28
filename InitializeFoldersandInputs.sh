#!/bin/bash

mkdir input
mkdir output
mkdir events

python3 InputCreation/CreateCarInitDataset.py
python3 InputCreation/CreatePickleEventi.py 
python3 InputCreation/CreatePickleZoneDistance.py
python3 InputCreation/CreateValidZones.py

