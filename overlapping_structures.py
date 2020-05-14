# -*- coding: utf-8 -*-
"""
IronPython 2.7
Created on Wed May 13 21:27:33 2020
@author: EV

1.Checks which ROIs overlap with the PTV (plus a margin),
2.Creates control structures that dont overlap with the PTV, for each of the
overlapping ROIs.
"""

from connect import *
import sys

#ROIs to exclude from the comparisons
ptv_name = 'PTV_ICTP'
ctv_name = 'CTV_ICTP'
external_name = 'External_ICTP'
exclusion_list = [ptv_name, ctv_name, external_name]
#margin (maximum distance to PTV)  
margin = 0.5 #cm

#get current case and examination
case = get_current("Case")
examination = get_current("Examination")

#structures in the current examination 
structures = case.PatientModel.StructureSets[examination.Name]
#ROIs in the current case
rois = case.PatientModel.RegionsOfInterest 

#1------------------------------------------------------------------------------
#create empty dictionary to store results
roi_distances = {}

#loop over all rois to calculate distance to PTV
for roi in rois:
    if roi.Name in exclusion_list : #exclude ROIs from the comparison
        continue
    else:
        distance = structures.RoiSurfaceToSurfaceDistanceBasedOnDT(
                ReferenceRoiName = ptv_name, TargetRoiName = roi.Name)
        roi_distances[roi.Name] = distance['Min'] #save just the min distance
        
#select the ROIs that are within a certain distance of the PTV
selected_rois = []

for roi in roi_distances:
    if roi_distances[roi]<margin :
        selected_rois.append(roi)

#Check that selected rois are organs
for roi in selected_rois:
    pass

#2------------------------------------------------------------------------------
#Create boolean ROIs for the selected organs  

#ROI parameters
purple = '#FFFF00FF' #ARGB value, purple

#Algebra settings
#margin settings
margin_expand = {'Type': "Expand", 'Superior': margin, 'Inferior': margin, 
                 'Anterior': margin, 'Posterior': margin, 'Right': margin, 
                 'Left': margin}
margin_same = {'Type': "Expand", 'Superior': 0, 'Inferior': 0, 
                 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0}
#expression PTV+margin
expression_ptv = {'Operation': "Union", 'SourceRoiNames': [ptv_name], 
               'MarginSettings': margin_expand}


#Loop over all selected organs, create empty ROI and fill it 
for organ_roi in selected_rois:
    algebra_name = organ_roi + "_mPTV"

    #create empty ROI
    with CompositeAction('Create ROI'):
        boolean_roi = case.PatientModel.CreateRoi(Name=algebra_name, 
                                              Color=purple, Type='Control')
    #end composite action

    #expressions (organ expression)
    expression_organ = {'Operation': "Union", 'SourceRoiNames': [organ_roi], 
               'MarginSettings': margin_same }

    #do ROI algebra to fill in ROI
    with CompositeAction('ROI Algebra'):
        expression = boolean_roi.SetAlgebraExpression(ExpressionA=expression_organ, 
                                                ExpressionB=expression_ptv, 
                                                ResultOperation="Subtraction", 
                                                ResultMarginSettings=margin_same)

        expression.UpdateDerivedGeometry(Examination=examination, Algorithm="Auto")
    # CompositeAction ends 