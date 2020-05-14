# -*- coding: utf-8 -*-
"""
IronPython 2.7
Created on Tue May 12 22:58:45 2020
@author: EV

Creates a point of interest from the center of the target ROI
"""

from connect import *
import sys

#get current case, patient and examination
case = get_current("Case")
patient = get_current("Patient")
examination = get_current("Examination")

ptv_name = 'PTV_ICTP' #name of the target ROI
poi_name = "isocenter"

# Get ROI geometries 
roi_geometries = case.PatientModel.StructureSets[examination.Name].RoiGeometries

#get the center of the PTV ROI
try:
    ptv_center = roi_geometries[ptv_name].GetCenterOfRoi()
except:
    print 'Cannot access center of ROI {0}. Exiting script.'.format(ptv_name)
    sys.exit()
    
#save the coordinates in a dictionary
isocenter_coordinates = {'x':ptv_center.x, 'y':ptv_center.y, 'z':ptv_center.z}

#delete POI if it already exists
pois = case.PatientModel.PointsOfInterest
try:
    pois[poi_name].DeleteRoi()
    print 'deleted previous POI'
except:
    print 'creating POI'
    
#Create a POI from the coordinates 
with CompositeAction('Create isocenter POI'):
    isocenter_poi = case.PatientModel.CreatePoi(Examination=examination, 
    Point=isocenter_coordinates, 
    Volume=0, Name=poi_name, Color="Red", VisualizationDiameter=1, 
    Type="Isocenter")

patient.Save() #save changes (created POI)