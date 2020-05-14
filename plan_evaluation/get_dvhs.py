# -*- coding: utf-8 -*-
"""
IronPython 2.7
Created on Fri May 15 00:29:11 2020
@author: EV

Get DVHs from ROIs
"""
from connect import *
import pickle
import numpy as np

#dose parameters
prescribed_dose = 5000 #cGy

#DVH range
start_dose = 0
stop_dose = 1.10
step_size = 0.01 

#get current patient, case, plan and beam set
patient = get_current("Patient")
case = get_current("Case")
examination = get_current("Examination")
plan = get_current("Plan")
beam_set = get_current("BeamSet")

#plan dose
totaldose =  plan.TreatmentCourse.TotalDose

#dose axis for DVH 
dose_levels = prescribed_dose*np.arange(start_dose, stop_dose+step_size, step_size)

#calculate volumes at dose
dvh_set = {}
roiname = 'PTV'
volumes = totaldose.GetRelativeVolumeAtDoseValues(RoiName=roiname, 
                                                  DoseValues=dose_levels)
dvh_set[roiname] = volumes

#save the data
file_name = patient.Name+ '1' + '.pickle'
with open(file_name, 'wb') as f:
    pickle.dump(dvh_set, f)