# -*- coding: utf-8 -*-
"""
IronPython 2.7
Created on Wed May 13 01:43:42 2020
@author: EV

Get a list with the names of all the POIs and ROIs,
check if a ROI or POI name exists
"""

from connect import *
import sys

#get current case
case = get_current("Case")

pois = case.PatientModel.PointsOfInterest #access POIs
rois = case.PatientModel.RegionsOfInterest #access ROIs

#create empty lists
poi_list = []
roi_list = []

#loop over POIs
for poi in pois:
    poi_list.append(poi.Name)
    
#loop over ROIs
for roi in rois:
    roi_list.append(roi.Name)
    
#check if there is a ROI with a certain name
roi_name = 'PTV'

if (roi_name in roi_list):
    print "The ROI exists"
else:
    print "ROI was not found"
    
#check if there is a POI with a certain name
poi_name = "isocenter"

if (poi_name in poi_list):
    print "The POI exists"
else:
    print "POI was not found"
    
##ALTERNATIVE 
#poi_geometries = case.PatientModel.StructureSets[examination.Name].PoiGeometries
#
#for points in poi_geometries:
#    print points.OfPoi.Name
    