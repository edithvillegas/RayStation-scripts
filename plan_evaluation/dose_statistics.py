# -*- coding: utf-8 -*-
"""
IronPython 2.7
Created on Thu May 14 2020
@author: EV

Summarize dose statistics in all ROIs of a plan
"""

from connect import *
import pickle

#get current patient, case, plan and beam set
patient = get_current("Patient")
case = get_current("Case")
examination = get_current("Examination")
plan = get_current("Plan")
beam_set = get_current("BeamSet")

#ROIs in the current patient model
rois = case.PatientModel.RegionsOfInterest 
roi_geometry = case.PatientModel.StructureSets[examination.Name].RoiGeometries

#dose with the current plan
totaldose =  plan.TreatmentCourse.TotalDose
fdose = beam_set.FractionDose

#make an epmty dictionary to store all ROIs
roi_dic = {}
#volume levels to calculate dose at volume statistics
volume_levels = [0, 0.01, 0.02, 0.50, 0.95, 0.98, 0.99, 1] 

for roi in rois:
    name = roi.Name
    #calculate the dose at relative volumes for each ROI
    dose_atv = list(totaldose.GetDoseAtRelativeVolumes(RoiName = name, 
                                                  RelativeVolumes=volume_levels))
    #for each ROI, store dose statistics in a dictionary
    roi_dic[name] = {'mean dose': totaldose.GetDoseStatistic(RoiName=name, DoseType='Average'), 
           'minimum dose': totaldose.GetDoseStatistic(RoiName=name, DoseType='Min'),
           'maximum dose': totaldose.GetDoseStatistic(RoiName=name, DoseType='Max'),
           'mean fraction dose': fdose.GetDoseStatistic(RoiName=name, DoseType='Average'),
           'minimum fraction dose': fdose.GetDoseStatistic(RoiName=name, DoseType='Min'),
           'maximum fraction dose': fdose.GetDoseStatistic(RoiName=name, DoseType='Max'),
           'dose at volume': dose_atv,
           'ROI volume': roi_geometry[name].GetRoiVolume() #cm^4
           }

#save the data
file_name = patient.Name + 'ROI_dose' + '.pickle'
with open(file_name, 'wb') as f:
    pickle.dump(roi_dic, f)

#