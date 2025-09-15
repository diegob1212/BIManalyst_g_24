# -*- coding: utf-8 -*-
"""
Created on Mon Sep 15 14:13:22 2025

@author: Diego
"""

import ifcopenshell
import ifcopenshell.util.classification

model = ifcopenshell.open("25-06-D-STR.ifc")

print('The report claims that DTU building 115 is a four-story structure that includes a basement and has a flat roof upon which is a terrace.\n')

report_storey = 6



# Find all storeys
storeys = model.by_type("IfcBuildingStorey")


print("Number of storeys (IfcBuildingStorey):", len(storeys),'\n')

# Print names and elevations in meters
for s in storeys:
    elevation_mm = getattr(s, "Elevation", 0)   
    elevation_m = elevation_mm / 1000           
    print(f" - Storey: {s.Name} | Elevation: {elevation_m} m \n")


if report_storey is len(storeys):
    print('Claim is correct ! DTU Building 115 has 6 storeys including terrace and basement.')
    
else:
    print('Claim is incorrect ! In the report we have',report_storey,'storeys and the IFC model has', len(storeys))