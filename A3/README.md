# About the tool
## The problem that the tool solves

The tool verifies whether load-bearing concrete walls comply with the R120 fire-resistance requirement according to EN 1992-1-2.
It checks if the wall elements meet the minimum thickness and concrete strength class needed to achieve 120 minutes of load-bearing capacity under fire exposure.


## The problem is found at...
This claim originates from D_Report_Team08_STR, pp. 27–28, Section 10 “Structural Fire Safety”, where the R120 fire-resistance check was performed manually.
We found that this process could be automated for better consistency and faster validation during design.

Reference from report:
<img width="919" height="424" alt="image" src="https://github.com/user-attachments/assets/c655f00a-d655-4194-8bfc-75a8fb1873d1" />

Detailed reference from Eurocode: 
<img width="932" height="846" alt="image" src="https://github.com/user-attachments/assets/3ef2b5c6-cb49-458a-9c7e-b10d097211a0" />

## Description of the tool
The developed Python script, r120_wall_checker, automates the verification of fire-resistance (R120) requirements for load-bearing interior concrete walls in IFC building models. It is important to add that, based on the two pictures above, the thickness of the walls only applies for the concrete part so if there is other materials in the wall we will just remove them and take into account only the concrete thickness.
It uses the IfcOpenShell library to parse and analyze Building Information Models (BIM) following the IFC standard.

**Workflow Overview**

**1. IFC Model Import**

The script reads both the architectural (25-08-D-ARCH.ifc) and structural (25-08-D-STR.ifc) models. We don't really use the structural model but we load it in case load bearing walls are defined in this one and not in the architectural model.

**2. Wall Selection**

From all IfcWall and IfcWallStandardCase elements, the tool automatically selects:

- Walls explicitly marked as load-bearing in the IFC attributes or names, and

- Walls identified as interior (e.g. names containing “Interior Wall (Load Bearing)”).

**Important Note** : The walls selection should be more advanced. In our case we trust what says the model but we should not. We cannot really trust the model. So to developp further our tool the idea would be to implemented some techniques and functions in order to check the validity of the model in terms of if the walls are really load bearing or not. This could be done in another project in order to implement it in ours.

**3. Material and Geometry Extraction**

For each selected wall, the tool extracts:

- The concrete thickness (it isn't the full thickness of the wall, it is only summing layers that contain concrete)

- The concrete strength class (e.g., C25/30) from the associated IFC materials.

If no concrete layer is found, the wall is treated as non-concrete.
If concrete is present but no class is specified, it is labeled “UNKNOWN concrete class.”

**4. Fire-Resistance Evaluation (R120)**

Each wall is checked against Eurocode 2 (EN 1992-1-2) tabulated requirements:

- Minimum wall thickness → 220 mm

- Minimum concrete class → C25/30

**5. Automated Classification**

Based on these parameters, the script assigns one of the different results:

- PASS	Thickness and concrete class both meet R120 criteria
- FAIL	Does not meet one or more requirements
- UNKNOWN	Concrete class not defined but thickness is satisfactory

  
**6. Output and Summary**

The tool prints a detailed wall-by-wall summary in the terminal, listing:

- Wall name

- Thickness (mm)

- Concrete class or “NOT CONCRETE”

- Compliance status (PASS / FAIL / UNKNOWN)

- Reason for classification

- At the end, it provides a summary table of:

- Total number of checked walls

- Number of passing walls

- Number of failing walls

- Number of walls with unknown results


**Assumptions regarding the model (IFC-file)**: 

Our code assumes that the walls information is detailed. The code needs to find the information about load bearing walls and interior or not. If it is not specifiy the code will simply class the walls as unknowns. 

Also, as we couldn't implement the load bearing walls checker tool, we trust the veracity of the model in terms of list of loadbearing walls.


**INPUT**: The function takes an IFC-file as the input.

**OUTPUT**: The script outputs a detailed fire-resistance compliance report for all load-bearing interior concrete walls found in the IFC model.
Specifically, it provides:

- A terminal summary listing, for each wall:

- Wall name (e.g. Basic Wall:Interior Wall (Load Bearing))

- Wall thickness (mm)

- Concrete class (e.g. C25/30 or UNKNOWN concrete class)

- Compliance status: PASS, FAIL, or UNKNOWN

- Explanation of the result (e.g. "Insufficient thickness", "Concrete class not defined in IFC")

A final summary table displaying:

- Number of walls meeting R120 criteria

- Number of walls failing the requirements

- Number of walls with incomplete data

Optionally, the results can be exported to a CSV file for documentation and further analysis.
### Overview of the function


![Picture1](https://github.com/diegob1212/BIManalyst_g_24/blob/main/A3/Updated%20BPMN%20scope%20highlighted.svg)<br>

There is a quick remminder of our tool. We can see that our tool could be improve by using an exterior tool that checks that load bearing walls really are what the model says. The step "Load bearing checker on the element" isn't performed by our code but is done by an exterior tool that could be implemented.

## Instructions to run the tool
To run the tool please follow the steps below:
0. Save both script python files in a direcory in your computer

1. Prepare your IFC models
Place both IFC files (the architectural and structural models) in the same directory as the script:
- 25-08-D-ARCH.ifc  
- 25-08-D-STR.ifc

2. Run the script
Open a terminal in that directory and execute:

python main.py

3. View the results
The script will:

Automatically identify load-bearing interior walls from the IFC model and extract their thickness and concrete class.
Automatically evaluate each wall’s compliance with R120 fire-resistance requirements (EN 1992-1-2)

4. Check the output

Results are printed directly in the terminal, including:
- Wall name and ID
- Measured thickness (mm)
- Concrete class or “UNKNOWN concrete class”
- Compliance status (PASS, FAIL, or UNKNOWN)
- Explanation of the classification

5. Optional : we can add csv file to have all the information
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
- Load-bearing property: Load Bearing or Not-Load Bearing
- Wall thickness: IfcMaterialLayerSet → LayerThickness
- Material name / concrete class: IfcRelAssociatesMaterial → IfcMaterial.Name or in the wall named in the wall description


# IDS – Information Delivery Specification

To ensure that the R120 wall checker can run successfully, an Information Delivery Specification (IDS) has been produced.
The IDS defines the minimum IFC data requirements that the model must fulfill for the tool to extract all necessary information about walls, materials, and fire-resistance properties.

| Attribute                      | IFC Location                                         | Required | Example                            | Purpose                                                |
| ------------------------------ | ---------------------------------------------------- | -------- | ---------------------------------- | ------------------------------------------------------ |
| Element type                   | `IfcWall` / `IfcWallStandardCase`                    | ✅ Yes   | –                                  | Defines the scope of the elements to analyze           |
| Load-bearing flag              | `Pset_WallCommon.LoadBearing`                        | ✅ Yes   | TRUE                               | Filters only load-bearing walls                        |
| Interior wall identification   | `Name` or `ObjectType` attribute                     | ✅ Yes   | Basic Wall:Interior Wall (Load Bearing) | Ensures only interior walls are checked (exposed both sides) |
| Material association            | `IfcRelAssociatesMaterial`                           | ✅ Yes   | –                                  | Required to access construction material layers        |
| Wall thickness (concrete only) | `IfcMaterialLayerSet → IfcMaterialLayer.LayerThickness` | ✅ Yes   | 220 mm                             | Used for R120 minimum thickness verification           |
| Material / concrete class      | `IfcMaterial.Name` or layer name                     | ⚠️ Optional | C25/30                            | Used for R120 concrete class check; if missing → UNKNOWN |
| Units                          | `IfcProject.UnitsInContext`                          | ✅ Yes   | mm                                 | Ensures consistent unit conversion (e.g., mm vs m)     |



A simplified version of the IDS file tailored to this project is:

```xml
<ids:InformationDeliverySpecification xmlns:ids="http://buildingSMART.org/ids">
  <ids:Specification name="R120 Wall Check Input Requirements">
    <ids:Entity name="IfcWallStandardCase">
      <ids:Requirement property="Pset_WallCommon.LoadBearing" mustExist="true"/>
      <ids:Requirement property="Name" pattern="Interior Wall"/>
      <ids:Requirement property="IfcRelAssociatesMaterial" mustExist="true"/>
      <ids:Requirement property="IfcMaterialLayer.LayerThickness" mustExist="true"/>
      <ids:Requirement property="IfcMaterial.Name" pattern="(Concrete|Béton|C\d{2,3}/\d{2,3})"/>
    </ids:Entity>
  </ids:Specification>
</ids:InformationDeliverySpecification>




















