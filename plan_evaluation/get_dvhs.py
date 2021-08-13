# -*- coding: utf-8 -*-
"""
IronPython 2.7
Created on Fri May 15 00:29:11 2020
@author: Edith Villegas

Get DVHs from ROIs
"""

from connect import *
import pickle

#get current patient, case, plan and beam set
patient = get_current("Patient")
case = get_current("Case")
examination = get_current("Examination")
plan = get_current("Plan")
beam_set = get_current("BeamSet")

#dose parameters
prescribed_dose = beam_set.Prescription.PrimaryDosePrescription.DoseValue

#DVH dose range
start_dose = int(prescribed_dose*0)
stop_dose = int(prescribed_dose*1.10)
step_size = int(prescribed_dose*0.01)

#plan dose
totaldose =  plan.TreatmentCourse.TotalDose

#case ROIs
rois = case.PatientModel.RegionsOfInterest 
roi_geometry = case.PatientModel.StructureSets[examination.Name].RoiGeometries

#dose axis for DVH 
dose_levels = [x for x in range(start_dose, stop_dose+step_size, step_size)]

#calculate volumes at dose
dvh_set = {}

for roi in rois:
    roiname = roi.Name
    volumes = totaldose.GetRelativeVolumeAtDoseValues(RoiName=roiname, 
                                                  DoseValues=dose_levels)
    dvh_set[roiname] = {'volume levels' : list(volumes), 
           'absolute volume': roi_geometry[roiname].GetRoiVolume(),
           'ROI type': roi.Type}

#save the data
file_name = patient.Name+ 'DVH' + '.pickle'
with open(file_name, 'wb') as f:
    pickle.dump(dvh_set, f)