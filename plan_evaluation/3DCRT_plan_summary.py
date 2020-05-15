# -*- coding: utf-8 -*-
"""
IronPython 2.7
Created on Fri May 15 18:24:40 2020
@author: EV

Export a summary of the current treatment plan beam set, 3DCRT
"""

from connect import *
import pickle

patient = get_current('Patient')
case = get_current('Case')
examination = get_current('Examination')
plan = get_current('Plan')

#store plan data in a dictionary
plan_data = {}
plan_data['name'] = plan.Name
plan_data['planner'] = plan.PlannedBy
plan_data['comments'] = plan.Comments
plan_data['beamsets'] = [beamset.DicomPlanLabel for beamset in plan.BeamSets]  

#get current beamset
beam_set = get_current('BeamSet')

#store beam set data in a dictionary
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


#save data
file_beamset = patient.Name + '_' + beam_set.DicomPlanLabel + '.pickle'

with open(file_beamset, 'wb') as f:
    pickle.dump([plan_data, beamset_data], f)







