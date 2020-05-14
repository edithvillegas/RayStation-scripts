# -*- coding: utf-8 -*-
"""
IronPython 2.7
Created on Wed May 13 00:10:48 2020
@author: EV

Rounds the coordinates of a POI
"""

from connect import *
import sys

#get current case, patient and examination
case = get_current("Case")
patient = get_current("Patient")
examination = get_current("Examination")

#name of the POI
isocenter_name = 'ISO_POI'

#access the POI
poi_geometries = case.PatientModel.StructureSets[examination.Name].PoiGeometries

try:
    isocenter_poi = poi_geometries[isocenter_name]
except:
    print 'Error: POI not found' 
    sys.exit()

#save the values of the coordinates
x = isocenter_poi.Point.x
y = isocenter_poi.Point.y
z = isocenter_poi.Point.z

#round coordinates to one decimal place
x = round(x,1)
y = round(y,1)
z = round(z,1)

#change the coordinates. 
#use a Python dictionary that contains the properties of the ExpandoObjectas keys
new_coordinates = {'x': x, 'y':y, 'z':z}

#Undo group
with CompositeAction('Change POI Coordinates'):
    isocenter_poi.Point = new_coordinates

#patient.Save() #this makes undoing the last action not possible