# About the tool
## The problem that the tool solves

The tool verifies whether load-bearing concrete walls comply with the R120 fire-resistance requirement according to EN 1992-1-2.
It checks if the wall elements meet the minimum thickness and concrete strength class needed to achieve 120 minutes of load-bearing capacity under fire exposure.


## The problem is found at...
This claim originates from D_Report_Team08_STR, pp. 27–28, Section 10 “Structural Fire Safety”, where the R120 fire-resistance check was performed manually.
We found that this process could be automated for better consistency and faster validation during design.

## Description of the tool
The developed Python script, r120_wall_checker, automates the verification of fire-resistance (R120) requirements for load-bearing interior concrete walls in IFC building models.
It uses the IfcOpenShell library to parse and analyze Building Information Models (BIM) following the IFC standard.

Workflow Overview
1. IFC Model Import

The script reads both the architectural (25-08-D-ARCH.ifc) and structural (25-08-D-STR.ifc) models.

2. Wall Selection

From all IfcWall and IfcWallStandardCase elements, the tool automatically selects:

Walls explicitly marked as load-bearing in the IFC attributes or names, and

Walls identified as interior (e.g. names containing “Interior Wall (Load Bearing)”).

Note : The walls selection should be more advanced. In our case we trust what says the model but we should not. We cannot really trust the model. So to developp further our tool the idea would be to implemented some techniques and functions in order to check the validity of the model in terms of if the walls are really load bearing or not. This could be done in another project in order to implement it in ours.

3. Material and Geometry Extraction

For each selected wall, the tool extracts:

- The concrete thickness (it isn't the full thickness of the wall, it is only summing layers that contain concrete)

- The concrete strength class (e.g., C25/30) from the associated IFC materials.

If no concrete layer is found, the wall is treated as non-concrete.
If concrete is present but no class is specified, it is labeled “UNKNOWN concrete class.”

4. Fire-Resistance Evaluation (R120)

Each wall is checked against Eurocode 2 (EN 1992-1-2) tabulated requirements:

Minimum wall thickness → 220 mm

Minimum concrete class → C25/30

5. Automated Classification

Based on these parameters, the script assigns one of the different results:

- PASS	Thickness and concrete class both meet R120 criteria
- FAIL	Does not meet one or more requirements
- UNKNOWN	Concrete class not defined but thickness is satisfactory

  
6. Output and Summary

The tool prints a detailed wall-by-wall summary in the terminal, listing:

Wall name

Thickness (mm)

Concrete class or “NOT CONCRETE”

Compliance status (PASS / FAIL / UNKNOWN)

Reason for classification

At the end, it provides a summary table of:

Total number of checked walls

Number of passing walls

Number of failing walls

Number of walls with unknown results

Assumptions for wind calculation: doesn't apply to our project

Assumptions regarding the model (IFC-file): 

Our code assumes that the walls information is detailed. The model needs to find the information about load bearing and interior or not. If it is not specifiy the code will simply class the walls as unknowns. 


INPUT: The function takes an IFC-file as the input.

OUTPUT: The script outputs a detailed fire-resistance compliance report for all load-bearing interior concrete walls found in the IFC model.
Specifically, it provides:

A terminal summary listing, for each wall:

Wall name (e.g. Basic Wall:Interior Wall (Load Bearing))

Wall thickness (mm)

Concrete class (e.g. C25/30 or UNKNOWN concrete class)

Compliance status: PASS, FAIL, or UNKNOWN

Explanation of the result (e.g. "Insufficient thickness", "Concrete class not defined in IFC")

A final summary table displaying:

Number of walls meeting R120 criteria

Number of walls failing the requirements

Number of walls with incomplete data

Optionally, the results can be exported to a CSV file for documentation and further analysis.
### Overview of the function


![Picture1](https://github.com/FrederikJM/BIManalyst_g_28/blob/main/A3/BPMN.svg)<br>  (change this to an updated - version of ours) 


## Instructions to run the tool
To run the tool please follow the steps below:
1. Prepare your IFC models
Place both IFC files (the architectural and structural models) in the same directory as the script:
25-08-D-ARCH.ifc  
25-08-D-STR.ifc

2. Run the script
Open a terminal in that directory and execute:

python main.py

3. View the results
The script will:

Automatically identify load-bearing interior walls from the IFC model
Extract their thickness and concrete class
Evaluate each wall’s compliance with R120 fire-resistance requirements (EN 1992-1-2)

4. Check the output
Results are printed directly in the terminal, including:
- Wall name and ID
- Measured thickness (mm)
- Concrete class or “UNKNOWN concrete class”
- Compliance status (PASS, FAIL, or UNKNOWN)
- Explanation of the classification

# Advanced Building Design
## What Advanced Building Design Stage (A, B, C or D) would your tool be useful?
The tool is primarily used during Stage B (Design) and Stage C (Validation) of the Advanced Building Design process,
where model coordination and verification take place before issuing final IFCs.

## What subjects might use it?
The subjects that might use it could be: 
- Structural Engineering – to ensure fire resistance of load-bearing walls meets EN 1992-1-2.
- Fire Safety Engineering – to confirm the required R120 fire performance level.
- Digital BIM Coordination – to automate model verification and reduce manual checking time.

## What information is required in the model for your tool to work? (CHECK THIS=??????)
Below are stated what criteria should be fulfilled to use the tool
successfully.
- Element type: IfcWall, IfcWallStandardCase
- Load-bearing property: IsLoadBearing = TRUE
- Wall thickness: IfcMaterialLayerSet → LayerThickness
- Material name / concrete class: IfcRelAssociatesMaterial → IfcMaterial.Name
- Units and GlobalId for traceability (IfcProject.UnitsInContext, GlobalId)

# IDS – Information Delivery Specification

| Attribute                 | IFC Location                                  | Required | Example | Purpose                                 |
| ------------------------- | --------------------------------------------- | -------- | ------- | --------------------------------------- |
| Element type              | `IfcWall` / `IfcWallStandardCase`             | Yes      | –       | Defines scope                           |
| Load-bearing flag         | `IsLoadBearing`                               | Yes      | TRUE    | Filters walls                           |
| Wall thickness            | `IfcMaterialLayerSet → LayerThickness`        | Yes      | 200 mm  | Input for R120 check                    |
| Material / concrete class | `IfcRelAssociatesMaterial → IfcMaterial.Name` | Yes      | C30/37  | Input for R120 check                    |
| Units                     | `IfcProject.UnitsInContext`                   | Yes      | mm      | Ensures consistent thickness comparison |


# 1. As is BPMN diagram
<img width="2028" height="1040" alt="image" src="https://github.com/user-attachments/assets/85f2e0a4-6c96-435d-9f79-30bcb18a7e27" />

# 2. Aim
To automate the fire-resistance verification of load-bearing concrete walls (R120 per EN 1992-1-2) using IFC data, reducing manual effort and ensuring compliance early in the design stage.

# 3. To be BPMN diagram (UPDATE)

# 4. Your tool

The r120_wall_checker script is built in Python 3.12 using ifcOpenShell.
It follows the defined A2 workflow but limits its scope to load-bearing concrete walls only.
The script queries wall elements, retrieves thickness and concrete strength, and evaluates them
against tabulated Eurocode values for R120 fire resistance.

In this implementation, only walls are considered to focus on a single element type,
making the check more consistent and easier to debug during testing

# 5. Output

The tool outputs:
- A console summary showing number of PASS / FAIL / UNKNOWN walls.
- A detailed CSV file r120_results.csv listing:

  - Wall name / GlobalId
  - Thickness (mm)
  - Concrete class
  - Check result (PASS / FAIL / UNKNOWN)






















