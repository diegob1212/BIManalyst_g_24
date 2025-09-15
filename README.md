# OPENBIM_group24

# Assignment 1 - OpenBIM Rule Checker

- **Group number**: 24
- **Focus area**: Structure
- **Claim being checked**: "DTU building 115 is a four-story structure that includes a basement
and has a flat roof upon which is a terrace"
- **Report reference**: Structural Report, p. 1, section 1.1.1

## Description of script
The script opens the IFC structural model (`25-06-D-STR.ifc`) and counts the number of `IfcBuildingStorey` elements. It checks 
It prints the total number of columns and their IDs to validate the claim.

### Analyst notes
- The script searches for all `IfcColumn` entities in the IFC model.  
- It prints the number of columns and lists the first 10 as a sample.  

### Manager notes
- Script used: [`check_columns.py`](./check_columns.py)  
- This script validates the reported number of columns in the structural model.
