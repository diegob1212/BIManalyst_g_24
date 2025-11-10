# -*- coding: utf-8 -*-
"""
main.py — R120 fire resistance compliance checker
"""

import ifcopenshell
import re
from pathlib import Path
from get_walls import get_loadbearing_interior_walls

# ============================================================
# --- R120 REQUIREMENTS (EN 1992-1-2 thresholds) ---
# ============================================================

MIN_THICKNESS_R120_MM = 220        # min wall thickness for R120
MIN_CONCRETE_CLASS = "C25/30"      # min concrete class for R120

# ============================================================
# --- MATERIAL + THICKNESS EXTRACTION ---
# ============================================================

def get_concrete_class(wall):
    """
    Détecte si le mur est en béton et, si oui, retourne la classe:
      - None       -> no concrete found in the different layers
      - "UNKNOWN"  -> concrete but class is not defined
      - "Cxx/yy"   -> Concrete class found (ex. "C25/30")
    Logic: IfcMaterialLayerSet and look for concrete
    """
    found_concrete = False
    try:
        for rel in getattr(wall, "HasAssociations", []) or []:
            if not rel.is_a("IfcRelAssociatesMaterial"):
                continue
            mat = rel.RelatingMaterial
            # Case IfcMaterial
            if mat and mat.is_a("IfcMaterial"):
                name = (mat.Name or "").strip()
                if name:
                    # Looking for concrete
                    if "concrete" in name.lower():
                        found_concrete = True
                        m = re.search(r"C\d{2,3}/\d{2,3}", name.upper())
                        if m:
                            return m.group(0)
                        # no concrete class
                        return "UNKNOWN"
            # Case IfcMaterialLayerSet 
            elif mat and mat.is_a("IfcMaterialLayerSet"):
                # Looking at every laer for concrete
                for layer in getattr(mat, "MaterialLayers", []) or []:
                    mat2 = getattr(layer, "Material", None)
                    if not mat2:
                        continue
                    lname = (mat2.Name or "").strip()
                    if not lname:
                        continue
                    if "concrete" in lname.lower():
                        found_concrete = True
                        m = re.search(r"C\d{2,3}/\d{2,3}", lname.upper())
                        if m:
                            return m.group(0)
                
                if found_concrete:
                    return "UNKNOWN"
    except Exception:
        pass

    # No concrete detected
    return None


def meets_concrete_requirement(material_flag):
    """
    Évalue l’exigence de classe béton en fonction de la valeur de get_concrete_class(wall):
      - None       -> pas béton  => retourne False
      - "UNKNOWN"  -> béton sans classe => retourne None (inconnu)
      - "Cxx/yy"   -> compare numériquement, retourne True/False
    """
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


def get_wall_thickness(elem):
    """
    Return wall thickness (mm) from IfcMaterialLayerSet, considering ONLY concrete layers.
    Some walls are made of different materials. For R120 requirements only the concrete thickness
    has to be checked.
    If no concrete layer found, return None.
    """
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


# ============================================================
# --- MAIN PROGRAM ---
# ============================================================

def main():
    model_path_arch = Path(r"C:\DTU\openbim\assignement_2\25-08-D-ARCH.ifc")
    model_path_str  = Path(r"C:\DTU\openbim\assignement_2\25-08-D-STR.ifc")

    print(" Opening IFC models...")
    model   = ifcopenshell.open(model_path_arch)
    model_2 = ifcopenshell.open(model_path_str)

    # 1) Selection of walls 
    print("\n Identifying load-bearing interior walls...")
    loadbearing_walls = get_loadbearing_interior_walls(model)
    if not loadbearing_walls:
        print(" Warning : No load-bearing interior walls detected.")
        return

    # 2) Checking R120 requirements
    print("\n Checking R120 fire resistance compliance...")
    results = []

    for w in loadbearing_walls:
        gid  = w.GlobalId
        wall = model.by_guid(gid) or model_2.by_guid(gid)
        if not wall:
            continue

        # Thickess of concrete
        t = get_wall_thickness(wall)  # None if not concrete
        # Concrete class (None if not concrete, "UNKNOWN" if class unknown, "Cxx/yy" if class is defined)
        mat_flag = get_concrete_class(wall)
        conc_ok  = meets_concrete_requirement(mat_flag)  # False / None / True

        # Cas demandés
        pass_thickness = (t is not None) and (t >= MIN_THICKNESS_R120_MM)

        if pass_thickness and conc_ok is True:
            status = "PASS"
            reason = "Thickness OK and concrete class OK"
        elif pass_thickness and conc_ok is None:
            status = "UNKNOWN"
            reason = "Thickness OK but concrete class not defined"
        elif pass_thickness and conc_ok is False:
            status = "FAIL"
            reason = "Thickness OK but material is not concrete or below requirement"
        elif not pass_thickness and conc_ok is True:
            status = "FAIL"
            reason = "Concrete class OK but thickness insufficient"
        elif not pass_thickness and conc_ok is False:
            status = "FAIL"
            reason = "No sufficient thickness and not concrete"
        elif not pass_thickness and conc_ok is None:
            status = "FAIL"
            reason = "Thickness insufficient and concrete class unknown"
        else:
            # Security check 
            status = "UNKNOWN"
            reason = "Incomplete data"

        # Display mat
        if mat_flag is None:
            mat_str = "NOT CONCRETE"
        else:
            mat_str = mat_flag  # "UNKNOWN" ou "Cxx/yy"

        results.append({
            "GlobalId": gid,
            "Name": w.Name,
            "Thickness_mm": t,
            "Material": mat_str,
            "Status": status,
            "Reason": reason
        })

    # 3) Results
    print("\n===  R120 Fire Resistance Check Results ===")
    for r in results:
        print(f"{r['Name']:<35} | {r['Status']:<8} | t={r['Thickness_mm']} mm | material={r['Material']} | {r['Reason']}")

    # 4) Synthèse
    total   = len(results)
    passed  = sum(1 for r in results if r["Status"] == "PASS")
    failed  = sum(1 for r in results if r["Status"] == "FAIL")
    unknown = sum(1 for r in results if r["Status"] == "UNKNOWN")

    print("\n=== Summary ===")
    print(f"  Total checked walls: {total}")
    print(f"  ✅ PASS: {passed}")
    print(f"  ❌ FAIL: {failed}")
    print(f"  ❓ UNKNOWN: {unknown}")


if __name__ == "__main__":
    main()
