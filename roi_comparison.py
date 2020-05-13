# -*- coding: utf-8 -*-
"""
IronPython 2.7
Created on Wed May 13 19:33:22 2020
@author: EV

Compare 2 ROIs and check if they overlap.
Calculates dice similarity coefficient, prevision, sensitivity, specificity,
maximum and mean distance to agreement.
"""

from connect import *
import sys

#get current case and examination
case = get_current("Case")
examination = get_current("Examination")

#access roi geometries, structures
structures = case.PatientModel.StructureSets[examination.Name]
roi_geometries = structures.RoiGeometries

#ROIs
ptv_name = 'PTV_ICTP' 
organ = 'Bladder_ICTP'

#Compute overlap measures
overlap_measures = structures.ComparisonOfRoiGeometries(RoiA=ptv_name, 
                                RoiB=organ, ComputeDistanceToAgreementMeasures = True )


#decide if ROIs overlap
if overlap_measures['DiceSimilarityCoefficient']==0 :
    overlaping = False
else:
    overlaping = True
    print "ROIs overlap"

#save comparison results to a text file
file = open(r"ROI_comparison.txt", 'a')
file.write("##### ROI comparison ##### \r\n")
file.write(ptv_name)
file.write("\n")
file.write(organ)
file.write("\n")
file.write(str(overlap_measures))
file.write("\n")
file.close()










