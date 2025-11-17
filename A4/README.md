#  R120 Wall Checker – Automating Fire-Resistance Verification in IFC Models
### *A BIM-based Python Tutorial using IfcOpenShell*

---

##  Summary  

**Short description :**  
This tutorial teaches how to use Python and the IfcOpenShell library to automatically verify fire-resistance (R120) compliance of load-bearing concrete walls from IFC models, according to Eurocode 2 (EN 1992-1-2).  

**Learning Level:** Level 2 — *Analyst / BIM Data Automation*  
**Focus Area:** BIM Use for Structural & Fire Safety Checking  

---

##  Learning Objectives  

After completing this tutorial, you will be able to:  
1. Understand how to **extract and filter IFC wall data** using IfcOpenShell.  
2. Automatically **identify load-bearing interior walls** from IFC attributes.  
3. Retrieve **concrete layer thickness and class** information from `IfcMaterialLayerSet`.  
4. Apply **Eurocode 2 R120 fire-resistance criteria** in Python.  
5. Interpret and document the **PASS / FAIL / UNKNOWN** results of a wall-by-wall check.  

---

##  Background & Motivation  

Fire-resistance checking of walls in BIM models is typically manual and time-consuming.  
By leveraging **IfcOpenShell**, we can automate this process and ensure consistent verification across models.  
This tool responds to a learning need for *BIM analysts* to connect **model information (IFC)** with **regulatory performance requirements** (Eurocode 2).  

---

##  Prerequisites  

Before starting, make sure you have:  
- **Python ≥ 3.9**  
- Installed the `ifcopenshell` package:  
  ```bash
  pip install ifcopenshell
- IFC file in your working directory : 25-08-D-ARCH.ifc

---

## How does the code run ?

### Step 0 - Import packages

```bash
import ifcopenshell
import re
from pathlib import Path
from get_walls import get_loadbearing_interior_walls
```

Our code works in two different python files. The first file is get_walls.py. From this one, we have to import the function get_loadbearing_interior_walls in order to select the walls that we want to analyse. We separate our tool in two part because the first function get_loadbearing_interior_walls can be improved without impacting the main project.

### Step 1 - Fix the R120 requirements 

```bash
MIN_THICKNESS_R120_MM = 220        # min wall thickness for R120
MIN_CONCRETE_CLASS = "C25/30"      # min concrete class for R120
```
Based on the report we find the requirements that have to be met. This can be easily changed for the requirements of your own project.

### Step 2 - Extract properties

These two functions just extract the concrete class and the thickness of the concrete layer. For get_concrete_class if the class is not defined it returns "UNKNOWN" and if it is not concrete it returns None. For get_thickness, based on the list of load bearing walls, it will find the thickness of the concrete layer. It is tricky because lot of walls have different materials and for fire safety requirements we only want to select the thickness of concrete.

```bash
def get_concrete_class(wall):
  found_concrete = False
    try:
        for rel in getattr(wall, "HasAssociations", []) or []:
            if not rel.is_a("IfcRelAssociatesMaterial"):
                continue
        ...

             if found_concrete:
                    return "UNKNOWN"
    except Exception:
        pass

    # No concrete detected
    return None

def get_wall_thickness(elem):
  try:
        for rel in getattr(elem, "HasAssociations", []) or []:
            if not rel.is_a("IfcRelAssociatesMaterial"):
                continue
            mat = rel.RelatingMaterial
            if mat and mat.is_a("IfcMaterialLayerSet"):
                concrete_thickness = 0.0
                found = False
                for layer in getattr(mat, "MaterialLayers", []) or []:
                    m = getattr(layer, "Material", None)
                    if not m or not m.Name:
                        continue
                    lname = m.Name.lower()
                    if "concrete" in lname or "béton" in lname:
                        val = getattr(layer, "LayerThickness", None)
                        if val not in (None, "null", "NULL"):
                            try:
                                concrete_thickness += float(val)
                                found = True
                            except Exception:
                                continue
                if found:
                    return concrete_thickness
                else:
                    return None  # no concrete so thickness is None
    except Exception:
        pass

    # No info usable
    return None
```

Note : The function meets_concrete_requirement helps us to have all the information in the good format for the final function main. It already checks the concrete class requirements and returns a bool. Based on this function we can know if the concrete class requirement is met or not. 

```bash
def meets_concrete_requirement(material_flag):
    if material_flag is None:
        return False  # not concrete
    if material_flag == "UNKNOWN":
        return None   # Concrete but class unknown

    try:
        v = int(material_flag.upper().split("C")[1].split("/")[0])
        req = int(MIN_CONCRETE_CLASS.upper().split("C")[1].split("/")[0])
        return v >= req
    except Exception:
        # if format not good
        return None
```

### Step 3 - Full evaluation and output

Finally, we use the previous functions in our final main function in order to check every requirements and create an output.

```bash
def main():
    walls = get_loadbearing_interior_walls(model_arch)
    results = []

    for w in walls:
        gid = w.GlobalId
        t = get_wall_thickness(w)
        mat_class = get_concrete_class(w)
        pass_t = t and t >= MIN_THICKNESS_R120_MM
        pass_c = meets_concrete_requirement(mat_class)

        if pass_t and pass_c:
            status, reason = "PASS", "Meets R120 thickness and material class"
        elif pass_t and pass_c is None:
            status, reason = "UNKNOWN", "Concrete class not defined but thickness OK"
        elif pass_t and pass_c is False:
            status, reason = "FAIL", "Concrete class below R120 requirement"
        elif not pass_t and pass_c:
            status, reason = "FAIL", "Insufficient thickness"
        elif not pass_t and pass_c is None:
            status, reason = "FAIL", "Insufficient thickness and unknown concrete class"
        else:
            status, reason = "FAIL", "Not concrete or missing data"

        results.append((w.Name, status, t, mat_class, reason))

    print("\n===  R120 Fire Resistance Results ===")
    for r in results:
        print(f"{r[0]:<35} | {r[1]:<8} | t={r[2]} mm | {r[3]} | {r[4]}")
'''

This code automated the check of thickness and concrete class and give us as an output the list of walls with their properties and the result of the analysis.

Example of the output :

```bash
Found 53 interior load-bearing walls out of 275 total.

===  R120 Fire Resistance Results ===
Basic Wall:Interior Wall (Load Bearing):505000 | PASS    | t=230 mm | C30/37 | Meets R120 thickness and material class
Basic Wall:Interior Wall (Load Bearing):505132 | FAIL    | t=180 mm | UNKNOWN concrete class | Insufficient thickness and unknown concrete class
Basic Wall:Interior Wall (Load Bearing):505850 | UNKNOWN | t=240 mm | UNKNOWN concrete class | Concrete class not defined but thickness OK
```
---

## Conclusion

This tutorial demonstrates how **openBIM** data can be programmatically analyzed to verify fire-resistance requirements at scale. It shows as easy it is to check really fast the fire safety requirements. This project can easily be modified to increase the precision of the analysis. It adapts really good to other projects with only modifiying a few lines.
This project can also be used in different projects as checking slabs and columns for fire safety requirements. The main part will be the same just the selection of the IfcElements will be different.


--- 

## Suggested Extensions

- Export results automatically to .csv for documentation
- Integrate the tool into a **BIM execution plan**
- Adapt to other standards
- Extend to other elements such as IfcSlab or IfcColumn


























