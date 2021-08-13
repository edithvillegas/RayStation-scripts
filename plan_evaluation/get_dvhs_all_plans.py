# -*- coding: utf-8 -*-
"""
IronPython 2.7
Created on Fri May 15 00:29:11 2020
@author: Edith Villegas

Get DVHs of all ROIs from all plans in current patient case
"""

from connect import *
import pickle

#get current patient, case and examination
patient = get_current("Patient")
case = get_current("Case")
examination = get_current("Examination")

#get plan list
plans = case.TreatmentPlans

#case ROIs
rois = case.PatientModel.RegionsOfInterest 
roi_geometry = case.PatientModel.StructureSets[examination.Name].RoiGeometries

#empty dictionary to store DVH
dvh_set = {}

for plan in plans:

    #plan dose
    totaldose =  plan.TreatmentCourse.TotalDose
    beam_set = plan.BeamSets[0]
    
    #dose parameters
    try:
        prescribed_dose = beam_set.Prescription.PrimaryDosePrescription.DoseValue
    except:
        prescribed_dose = 8000 #if there is no dose prescription, take this
    
    #DVH dose range
    start_dose = int(prescribed_dose*0)
    stop_dose = int(prescribed_dose*1.10)
    step_size = int(prescribed_dose*0.01)
    
    #dose axis for DVH 
    dose_levels = [x for x in range(start_dose, stop_dose+step_size, step_size)]

    #calculate volumes at dose for each ROI
    dvh_set[plan.Name] = {}
    for roi in rois:
        roiname = roi.Name
        volumes = totaldose.GetRelativeVolumeAtDoseValues(RoiName=roiname, 
                                                      DoseValues=dose_levels)
        dvh_set[plan.Name][roiname] = {'volume levels' : list(volumes),
               'dose levels': dose_levels,
               'absolute volume': roi_geometry[roiname].GetRoiVolume(),
               'ROI type': roi.Type, 'prescribed dose': prescribed_dose}

#save the data
file_name = patient.Name+ 'DVH_all_plans' + '.pickle'
with open(file_name, 'wb') as f:
    pickle.dump(dvh_set, f)