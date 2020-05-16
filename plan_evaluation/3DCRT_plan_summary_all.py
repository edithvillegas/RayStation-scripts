# -*- coding: utf-8 -*-
"""
IronPython 2.7
Created on Fri May 15 23:18:49 2020
@author: EV
"""

from connect import *
import pickle

patient = get_current('Patient')
case = get_current('Case')
examination = get_current('Examination')
plan = get_current('Plan')
beam_set = get_current('BeamSet')

#store plan data in a dictionary
def get_plan_data(plan):
    plan_data = {}
    plan_data['name'] = plan.Name
    plan_data['planner'] = plan.PlannedBy
    plan_data['comments'] = plan.Comments
    plan_data['beamsets'] = [beamset.DicomPlanLabel for beamset in plan.BeamSets] 
    return plan_data

#store beam set data in a dictionary
def get_beamset_summary(beam_set):
    beamset_data = {}
    beamset_data['name'] = beam_set.DicomPlanLabel 
    beamset_data['modality'] = beam_set.Modality 
    beamset_data['patient position'] = beam_set.PatientPosition
    beamset_data['technique'] = beam_set.PlanGenerationTechnique
    beamset_data['treatment machine'] = beam_set.MachineReference.MachineName
    beamset_data['beams'] = {}
    
    #get data for each individual beam
    for beam in beam_set.Beams:
        beamset_data['beams'][beam.Name] = {'gantry angle': beam.GantryAngle,
                    'collimator angle': beam.InitialCollimatorAngle,
                    'initial jaw positions': list(beam.InitialJawPositions),
                    'beam energy': beam.BeamQualityId,
                    'isocenter': [beam.Isocenter.Position.x, 
                                  beam.Isocenter.Position.y,
                                  beam.Isocenter.Position.z]}
        
        if beam.Wedge == None:
            continue
        
        beamset_data['beams'][beam.Name]['wedge'] = {'angle': beam.Wedge.Angle,
                              'orientation': beam.Wedge.Orientation,
                              'type': beam.Wedge.Type}
    
    #return dictionary
    return beamset_data

#GET THE DATA FOR THE PATIENT PLANS 
#get data for all plans in the patient
treatment_plans_summary = []
for treatment_plan in case.TreatmentPlans:
    treatment_plans_summary.append(get_plan_data(treatment_plan))

#get data for all beamsets in all plans
beamsets_summary = {}
for treatment_plan in case.TreatmentPlans:
    beamsets_summary[treatment_plan.Name] = []
    #conformal= [beamset for beamset in treatment_plan.BeamSets if beamset.PlanGenerationTechnique is 'Conformal'] 
    
    for beamset in treatment_plan.BeamSets:
        if beamset.PlanGenerationTechnique != 'Conformal':
            continue
        else:
            beamsets_summary[treatment_plan.Name].append(get_beamset_summary(beamset))

#save data
file = patient.Name + '_treatment_plans.pickle'
with open(file, 'wb') as f:
    pickle.dump(treatment_plans_summary, f)

file = patient.Name + '_beam_sets_s.pickle'
with open(file, 'wb') as f:
    pickle.dump(beamsets_summary, f)

