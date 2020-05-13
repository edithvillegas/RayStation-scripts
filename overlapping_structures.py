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

#Create an empty ROI
ename = 'empty'
ecolor = '#FFFF00FF' #ARGB value
etype = 'Control'
#etissuename = None
#erbecelltype = None
#eroimaterial = None 
#
#boolean_roi = case.PatientModel.CreateRoi(
#        Name=ename, Color=ecolor, Type=etype,
#        TissueName=etissuename, RbeCellTypeName=erbecelltype,
#        RoiMaterial=eroimaterial)

boolean_roi = case.PatientModel.CreateRoi(Name=ename, Color=ecolor, Type=etype)

#now create an algebra roi from this
#margin settings
margin_expand = {'Type': "Expand", 'Superior': 0.5, 'Inferior': 0.5, 
                 'Anterior': 0.5, 'Posterior': 0.5, 'Right': 0.5, 'Left': 0.5}
margin_same = {'Type': "Expand", 'Superior': 0, 'Inferior': 0, 
                 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0}

expressiona = {'Operation': "Union", 'SourceRoiNames': [r"Bladder_ICTP"], 
               'MarginSettings': margin_same }
    
expressionb = {'Operation': "Union", 'SourceRoiNames': [r"PTV_ICTP"], 
               'MarginSettings': margin_expand}

#boolean_roi.CreateAlgebraGeometry(
#    Examination=examination, Algorithm='Auto', 
#    )


###copied from script
with CompositeAction('ROI Algebra (empty)'):

  expression = boolean_roi.SetAlgebraExpression(ExpressionA=expressiona, 
                                                ExpressionB=expressionb, 
                                                ResultOperation="Subtraction", 
                                                ResultMarginSettings=margin_same)

  expression.UpdateDerivedGeometry(Examination=examination, Algorithm="Auto")

  # CompositeAction ends 





