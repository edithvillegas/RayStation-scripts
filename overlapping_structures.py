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
margin = 0.5 #cm

selected_rois = []

for roi in roi_distances:
    if roi_distances[roi]<margin :
        selected_rois.append(roi)

#Check that selected rois are organs
for roi in selected_rois:
    pass

#------------------------------------------------------------------------------
#Create boolean ROIs for the selected organs      
original_name = r"Bladder_ICTP"
ptv_name = 'PTV_ICTP'

#Create an empty ROI to start
#ROI parameters
ename = original_name+ "_mPTV"
ecolor = '#FFFF00FF' #ARGB value, purple
etype = 'Control'
#create ROI
boolean_roi = case.PatientModel.CreateRoi(Name=ename, Color=ecolor, Type=etype)

#Create ROI algebra to fill the empty ROI
#margin settings
margin_expand = {'Type': "Expand", 'Superior': margin, 'Inferior': margin, 
                 'Anterior': margin, 'Posterior': margin, 'Right': margin, 
                 'Left': margin}
margin_same = {'Type': "Expand", 'Superior': 0, 'Inferior': 0, 
                 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0}
#expressions (organ and PTV+margin)
expressiona = {'Operation': "Union", 'SourceRoiNames': [original_name], 
               'MarginSettings': margin_same }
expressionb = {'Operation': "Union", 'SourceRoiNames': [ptv_name], 
               'MarginSettings': margin_expand}

#do ROI algebra 
with CompositeAction('ROI Algebra'):
  expression = boolean_roi.SetAlgebraExpression(ExpressionA=expressiona, 
                                                ExpressionB=expressionb, 
                                                ResultOperation="Subtraction", 
                                                ResultMarginSettings=margin_same)

  expression.UpdateDerivedGeometry(Examination=examination, Algorithm="Auto")
  # CompositeAction ends 


