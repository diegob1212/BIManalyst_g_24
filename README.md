# OPENBIM_group24

# Assignment 1 - OpenBIM Rule Checker

- **Group number**: 24
- **Focus area**: Structure
- **Claim being checked**: "The building is supported by 24 structural columns."
- **Report reference**: Structural Report, p. 7, section 3.2

## Description of script
The script opens the IFC structural model (`25-06-D-STR.ifc`) and counts the number of `IfcColumn` elements.  
It prints the total number of columns and their IDs to validate the claim.

### Analyst notes
- The script searches for all `IfcColumn` entities in the IFC model.  
- It prints the number of columns and lists the first 10 as a sample.  

### Manager notes
- Script used: [`check_columns.py`](./check_columns.py)  
- This script validates the reported number of columns in the structural model.
