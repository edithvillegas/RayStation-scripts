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
ptv_name = 'PTV_ICTP'
ctv_name = 'CTV_ICTP'
external_name = 'External_ICTP'

#ROIs to exclude from the comparisons
exclusion_list = [ptv_name, ctv_name, external_name]

#create empty dictionary to store results
distances = {}

#loop over all rois to calculate distance to PTV
for roi in rois:
    if roi.Name in exclusion_list : #exclude ROIs from the comparison
        continue
    else:
        distance = structures.RoiSurfaceToSurfaceDistanceBasedOnDT(
                ReferenceRoiName = ptv_name, TargetRoiName = roi.Name)
        distances[roi.Name] = distance['Min']
        
print distances
    

