# -*- coding: utf-8 -*-
"""
IronPython 2.7
Created on Wed May 13 21:27:33 2020
@author: EV
"""

from connect import *
import sys

#get current case and examination
case = get_current("Case")
examination = get_current("Examination")

#structures in the current examination 
structures = case.PatientModel.StructureSets[examination.Name]
#ROIs in the current case
rois = case.PatientModel.RegionsOfInterest 

#ROI names
organ_name = 'Bladder_ICTP'
ptv_name = 'PTV_ICTP'
external_name = 'External_ICTP'

##comparison distance
#distance = structures.RoiSurfaceToSurfaceDistanceBasedOnDT(ReferenceRoiName = ptv_name,
#                                                           TargetRoiName = organ_name)

#create empty dictionary to store results
distances = {}

#loop over all rois to calculate distance to PTV
for roi in rois:
    if roi.Name == ptv_name : #exclude comparison of PTV to itself
        continue
    elif roi.Name== external_name: #exclude comparison to external ROI
        continue
    else:
        distance = structures.RoiSurfaceToSurfaceDistanceBasedOnDT(
                ReferenceRoiName = ptv_name, TargetRoiName = roi.Name)
        distances[roi.Name] = distance['Min']
        
print distances
    

