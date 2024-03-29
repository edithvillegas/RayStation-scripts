# RayStation-scripts
This repository contains a set of IronPython 2.7 scripts for the RayStation Treatment Planning System for External Beam Radiotherapy. The scripts provide basic functionality and serve as examples of how the scripting environment works. The scripts are divided into two sets, one for ROI (Region of Interest) and POI (Point of Interest) functions and another one for extracting information on the plans.

ROI and POI Scripts:
- **isocenter_poi.py**: Automatically creates a POI from the center of the planning target volume ROI. 
- **overlapping_structures.py**: Checks which ROIs overlap with the PTV (plus a margin) and creates control structures that don't overlap with the PTV, for each of the
overlapping ROIs.
- **roi_characteristics.py**: Gets a summary of data on all the ROIs: center coordinates, volumes, types, materials, and biological parameters.
- **roi_comparison.py**: Compares 2 ROIs and check if they overlap. Calculates dice similarity coefficient, prevision, sensitivity, specificity,
maximum and mean distance to agreement.
- **roi_poi_list.py**: Gets a list with the names of all the POIs and ROIs, checks if a ROI or POI name exists.
- **round_poi_coordinates.py**: Rounds the coordinates of the isocenter POI.

Plan information scripts:
- **3DCRT_plan_summary.py**: Exports a summary of the current beam set for a 3DCRT plan.
- **3DCRT_plan_summary_all.py**: Exports a summary of all plans for a patient.
- **dose_statistics.py**: Retrieves dose statistics of all ROIs in a plan.
- **get_dvhs.py**: Retrieves Dose Volume Histograms (DVH) from the current plan ROIs.
- **get_dvhs_all_plans.py**: Retrieves Dose Volume Histograms (DVH) from all ROIs in the current patient case.
