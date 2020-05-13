# -*- coding: utf-8 -*-
"""
IronPython 2.7
Created on Wed May 13 18:28:39 2020
@author: EV

Get a summary of data on all the ROIs: center coordinates, volumes, types, 
materials, and biological parameters.
"""

from connect import *
import sys

#get current case
case = get_current("Case")
examination = get_current("Examination")

#access roi geometries
roi_geometries = case.PatientModel.StructureSets[examination.Name].RoiGeometries

#create empty dictionary for geometrical parametres
roi_centers = {}
roi_volumes = {}
#create empty dictionaries for other parameters
roi_types = {} 
roi_materials= {}
roi_biological = {}

#iterate over all rois
for roi in roi_geometries:
    #volumes and centers
    center = roi.GetCenterOfRoi() #center of ROI coordinates
    roi_centers[roi.OfRoi.Name] = [center.x, center.y, center.z] 
    roi_volumes[roi.OfRoi.Name] = roi.GetRoiVolume() #in cm^3
    
    #other parameteres
    roi_types[roi.OfRoi.Name] = roi.OfRoi.Type #Organ, Target, etc.
    roi_materials[roi.OfRoi.Name] = roi.OfRoi.RoiMaterial
    roi_biological[roi.OfRoi.Name] = [roi.OfRoi.OrganData.OrganType, 
                                  roi.OfRoi.OrganData.RbeCellTypeName, 
                                  roi.OfRoi.OrganData.ResponseFunctionTissueName]
    

#print or save the information   
print roi_centers
print roi_volumes
print roi_types
print roi_materials
print roi_biological

    