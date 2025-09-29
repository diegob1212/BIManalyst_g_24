# A2: Use Case — Structural + Fire Safety (R 120, EN 1992‑1‑2)

> Focus area: **Structural + Fire Safety**
> Use case theme: **Automated check of R120 fire resistance (tabulated method)** for concrete **walls, columns, beams, slabs** in selected Advanced Building Design models (#2501, #2506, #2508, #2516).

---

## A2a — About our group

* **Members:** *[fill]*
* **Roles:** **Analyst** (verification + evidence generation). The Manager role can later aggregate our outputs into composite insights.
* **Coding confidence (0–4 per person):** *[fill]* → **Group total:** *[fill]*

---

## A2b — Identify Claim

**Claim to check:**
*All primary load‑bearing concrete **walls, columns, beams and slabs** comply with **R 120** per **EN 1992‑1‑2** using the **tabulated method** (dimensions, concrete class, axis distances/cover, exposure assumptions).*

**Justification:**

* Life‑safety critical; highly auditable.
* Checkable from IFC geometry/materials (OpenBIM) + clearly documented Eurocode thresholds.
* Bridges the group’s **structural** and **fire** focus areas.

**Scope:** `IfcWall/IfcWallStandardCase`, `IfcColumn`, `IfcBeam`, `IfcSlab` (solid).
**Out of current scope (flag as gaps):** explicit **rebar/axis distance** (if not modeled), **µ_fi** (load level under fire), **exposure sides**.

---

## A2c — Use Case (how/when/what)

**When to check:**

* Design phase at key gates (30/60/90%); again before IFC issue; and once for as‑built verification.

**BIM purpose:** **Gather → Analyse → Communicate → Realise**.

**Information relied on:**

* From IFC: element class, dimensions/thickness (profile or material layers), concrete material/class (if present), any `FireRating` string.
* From team inputs: **µ_fi** by typology, **exposure sides** policy, **default concrete cover** per element type when rebar is not modeled.

**Closest BIM use case:** Automated **code/standard compliance** checking (OpenBIM).

**Process (BPMN overview):**

* Swimlanes: **Architect**, **Structural Engineer**, **Fire Engineer**, **IFC R120 Checker (Python)**, **BIM Manager**.
* Steps:

  1. Architect/Structural export **IFC**
  2. **Checker** ingests IFC → extracts element sets
  3. Checker loads **rules** (R120 thresholds) + **assumptions** (µ_fi, exposure, cover)
  4. Checker evaluates elements → **PASS / FAIL / UNKNOWN(data gap)**
  5. Outputs **CSV** + **BCF** issues
  6. Fire Engineer reviews fails/gaps; adjusts assumptions or design
  7. Structural updates model; re‑export IFC
  8. Iterate until **Pass**
  9. BIM Manager publishes summary dashboard

> See `A2/IMG/A2_usecase.bpmn` and `A2/IMG/A2_usecase_highlighted.bpmn` below (XML you can paste into **bpmn.io** and export as **SVG**).

---

## A2d — Scope the use case (where a new tool is needed)

**New tool task:** **Evaluate R120 compliance** (Python/ifcOpenShell).

* Reads IFC + YAML assumptions, applies tabulated thresholds, merges defaults where IFC lacks data, outputs CSV and BCF.
* In the **highlighted** BPMN, this task is clearly marked.

---

## A2e — Tool Idea (OpenBIM ifcOpenShell)

**Name:** `r120_checker`
**Inputs:** `model.ifc`, `assumptions.yaml` (defaults), `rules/r120_thresholds.yaml` (tabulated minima), optional `zones.csv` (for exposure heuristic).
**Logic:** map elements → read sizes/thickness → read/parse concrete class → apply R120 thresholds → triage **PASS/FAIL/UNKNOWN** → emit **report.csv** + **issues.bcfzip** + HTML summary.
**Outputs:** auditable artefacts for coordination and authority evidence.
**Value:** earlier risk discovery; repeatable checks; transparent assumptions.

---

## A2f — Information Requirements

| Requirement                  | Where in IFC                                                    | Expected? | Handling                                                  |
| ---------------------------- | --------------------------------------------------------------- | --------- | --------------------------------------------------------- |
| Element type                 | `IfcWall*`, `IfcBeam`, `IfcColumn`, `IfcSlab`                   | Yes       | Query via ifcOpenShell type filters                       |
| Thickness (walls/slabs)      | `IfcMaterialLayerSet` → `MaterialLayers[].LayerThickness` (sum) | Often     | Sum layers or fallback to solid geometry thickness        |
| Section dims (beams/columns) | `IfcProfileDef` (e.g., `IfcRectangleProfileDef`) or BRep bbox   | Often     | Use profile; fallback to bbox with sanity checks          |
| Concrete class (≥ C25/30)    | `IfcMaterial`/`Pset_ConcreteElementGeneral`/Name                | Sometimes | Parse; else default in `assumptions.yaml`                 |
| Axis distance / cover        | Rebar entities (`IfcReinforcingBar`) or Psets                   | Rare      | Use defaults in assumptions; mark **UNKNOWN** if critical |
| Exposure sides; µ_fi         | Not standard in IFC                                             | No        | Provide in `assumptions.yaml` (by element type/zone)      |
| FireRating (declared)        | `Pset_*Common.FireRating`                                       | Sometimes | Compare “claimed” vs computed result                      |

**Learning needs:** robust ifcOpenShell queries, geometry thickness extraction, BCF generation, YAML config, reproducible reporting.

---

## A2g — Software Licence

* **MIT** (simple/permissive) or **Apache‑2.0** (permissive with explicit patent grant).
* Recommended: **Apache‑2.0** for classroom collaboration and reuse.

---

# Files to include in your repo

Create this structure in your GitHub repo:

```
A2/
  README.md                 # paste the sections above
  IMG/
    A2_usecase.bpmn        # BPMN XML (import into bpmn.io and export as SVG)
    A2_usecase_highlighted.bpmn
r120_checker/
  main.py
  io_helpers.py
  rules/
    r120_thresholds.yaml
  samples/
    assumptions.yaml
  README.md
```

---

## `A2/IMG/A2_usecase.bpmn` (XML to paste into bpmn.io)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<bpmn:definitions xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL"
  id="Definitions_UseCase_R120" targetNamespace="http://example.com/bpmn">
  <bpmn:process id="Process_R120_Check" isExecutable="false">
    <bpmn:laneSet id="LaneSet_1">
      <bpmn:lane id="Lane_Architect" name="Architect" />
      <bpmn:lane id="Lane_Structural" name="Structural Engineer" />
      <bpmn:lane id="Lane_Fire" name="Fire Engineer" />
      <bpmn:lane id="Lane_Checker" name="IFC R120 Checker (Python)" />
      <bpmn:lane id="Lane_BIMMgr" name="BIM Manager" />
    </bpmn:laneSet>

    <bpmn:startEvent id="Start" name="Design milestone" />

    <bpmn:task id="Task_ExportIFC" name="Export IFC (Architect/Structural)" />
    <bpmn:dataObjectReference id="Data_IFC" name="model.ifc" />

    <bpmn:task id="Task_LoadRules" name="Load rules & assumptions" />
    <bpmn:dataObjectReference id="Data_Rules" name="r120_thresholds.yaml" />
    <bpmn:dataObjectReference id="Data_Assump" name="assumptions.yaml" />

    <bpmn:task id="Task_Eval" name="Evaluate R120 compliance" />
    <bpmn:dataObjectReference id="Data_Report" name="report.csv + issues.bcfzip" />

    <bpmn:exclusiveGateway id="Gateway_Result" name="All pass?" />

    <bpmn:task id="Task_FireReview" name="Review fails/gaps (Fire Engineer)" />
    <bpmn:task id="Task_ModelUpdate" name="Update model/materials (Structural)" />

    <bpmn:task id="Task_Publish" name="Publish summary (BIM Manager)" />
    <bpmn:endEvent id="End" name="Milestone deliverable" />

    <bpmn:sequenceFlow id="F1" sourceRef="Start" targetRef="Task_ExportIFC" />
    <bpmn:sequenceFlow id="F2" sourceRef="Task_ExportIFC" targetRef="Task_LoadRules" />
    <bpmn:sequenceFlow id="F3" sourceRef="Task_LoadRules" targetRef="Task_Eval" />
    <bpmn:sequenceFlow id="F4" sourceRef="Task_Eval" targetRef="Gateway_Result" />
    <bpmn:sequenceFlow id="F5" sourceRef="Gateway_Result" targetRef="Task_Publish">
      <bpmn:conditionExpression xsi:type="bpmn:tFormalExpression">${pass == true}</bpmn:conditionExpression>
    </bpmn:sequenceFlow>
    <bpmn:sequenceFlow id="F6" sourceRef="Gateway_Result" targetRef="Task_FireReview">
      <bpmn:conditionExpression xsi:type="bpmn:tFormalExpression">${pass == false}</bpmn:conditionExpression>
    </bpmn:sequenceFlow>
    <bpmn:sequenceFlow id="F7" sourceRef="Task_FireReview" targetRef="Task_ModelUpdate" />
    <bpmn:sequenceFlow id="F8" sourceRef="Task_ModelUpdate" targetRef="Task_ExportIFC" />
    <bpmn:sequenceFlow id="F9" sourceRef="Task_Publish" targetRef="End" />

    <bpmn:dataInputAssociation id="D1">
      <bpmn:sourceRef>Data_IFC</bpmn:sourceRef>
      <bpmn:targetRef>Task_Eval</bpmn:targetRef>
    </bpmn:dataInputAssociation>
    <bpmn:dataInputAssociation id="D2">
      <bpmn:sourceRef>Data_Rules</bpmn:sourceRef>
      <bpmn:targetRef>Task_LoadRules</bpmn:targetRef>
    </bpmn:dataInputAssociation>
    <bpmn:dataInputAssociation id="D3">
      <bpmn:sourceRef>Data_Assump</bpmn:sourceRef>
      <bpmn:targetRef>Task_LoadRules</bpmn:targetRef>
    </bpmn:dataInputAssociation>
    <bpmn:dataOutputAssociation id="D4">
      <bpmn:sourceRef>Task_Eval</bpmn:sourceRef>
      <bpmn:targetRef>Data_Report</bpmn:targetRef>
    </bpmn:dataOutputAssociation>
  </bpmn:process>
</bpmn:definitions>
```

---

## `A2/IMG/A2_usecase_highlighted.bpmn` (same, with the tool task clearly marked)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<bpmn:definitions xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL"
  id="Definitions_UseCase_R120_Highlight" targetNamespace="http://example.com/bpmn">
  <bpmn:process id="Process_R120_Check_HL" isExecutable="false">
    <bpmn:laneSet id="LaneSet_1">
      <bpmn:lane id="Lane_Architect" name="Architect" />
      <bpmn:lane id="Lane_Structural" name="Structural Engineer" />
      <bpmn:lane id="Lane_Fire" name="Fire Engineer" />
      <bpmn:lane id="Lane_Checker" name="IFC R120 Checker (Python)" />
      <bpmn:lane id="Lane_BIMMgr" name="BIM Manager" />
    </bpmn:laneSet>

    <bpmn:startEvent id="Start" name="Design milestone" />
    <bpmn:task id="Task_ExportIFC" name="Export IFC (Architect/Structural)" />
    <bpmn:dataObjectReference id="Data_IFC" name="model.ifc" />
    <bpmn:task id="Task_LoadRules" name="Load rules & assumptions" />
    <bpmn:dataObjectReference id="Data_Rules" name="r120_thresholds.yaml" />
    <bpmn:dataObjectReference id="Data_Assump" name="assumptions.yaml" />

    <!-- *** HIGHLIGHTED TOOL TASK *** -->
    <bpmn:task id="Task_Eval" name="Evaluate R120 compliance [TOOL]" />

    <bpmn:dataObjectReference id="Data_Report" name="report.csv + issues.bcfzip" />
    <bpmn:exclusiveGateway id="Gateway_Result" name="All pass?" />
    <bpmn:task id="Task_FireReview" name="Review fails/gaps (Fire Engineer)" />
    <bpmn:task id="Task_ModelUpdate" name="Update model/materials (Structural)" />
    <bpmn:task id="Task_Publish" name="Publish summary (BIM Manager)" />
    <bpmn:endEvent id="End" name="Milestone deliverable" />

    <bpmn:sequenceFlow id="F1" sourceRef="Start" targetRef="Task_ExportIFC" />
    <bpmn:sequenceFlow id="F2" sourceRef="Task_ExportIFC" targetRef="Task_LoadRules" />
    <bpmn:sequenceFlow id="F3" sourceRef="Task_LoadRules" targetRef="Task_Eval" />
    <bpmn:sequenceFlow id="F4" sourceRef="Task_Eval" targetRef="Gateway_Result" />
    <bpmn:sequenceFlow id="F5" sourceRef="Gateway_Result" targetRef="Task_Publish" />
    <bpmn:sequenceFlow id="F6" sourceRef="Gateway_Result" targetRef="Task_FireReview" />
    <bpmn:sequenceFlow id="F7" sourceRef="Task_FireReview" targetRef="Task_ModelUpdate" />
    <bpmn:sequenceFlow id="F8" sourceRef="Task_ModelUpdate" targetRef="Task_ExportIFC" />
    <bpmn:sequenceFlow id="F9" sourceRef="Task_Publish" targetRef="End" />

    <bpmn:dataInputAssociation id="D1">
      <bpmn:sourceRef>Data_IFC</bpmn:sourceRef>
      <bpmn:targetRef>Task_Eval</bpmn:targetRef>
    </bpmn:dataInputAssociation>
    <bpmn:dataInputAssociation id="D2">
      <bpmn:sourceRef>Data_Rules</bpmn:sourceRef>
      <bpmn:targetRef>Task_LoadRules</bpmn:targetRef>
    </bpmn:dataInputAssociation>
    <bpmn:dataInputAssociation id="D3">
      <bpmn:sourceRef>Data_Assump</bpmn:sourceRef>
      <bpmn:targetRef>Task_LoadRules</bpmn:targetRef>
    </bpmn:dataInputAssociation>
    <bpmn:dataOutputAssociation id="D4">
      <bpmn:sourceRef>Task_Eval</bpmn:sourceRef>
      <bpmn:targetRef>Data_Report</bpmn:targetRef>
    </bpmn:dataOutputAssociation>
  </bpmn:process>
</bpmn:definitions>
```

---

# `r120_checker/` — Python skeleton

## `r120_checker/README.md`

```
# r120_checker

Automated R120 (EN 1992-1-2) compliance check for concrete walls, columns, beams and slabs from IFC.

## Quick start
pip install ifcopenshell lxml pyyaml pandas numpy
python -m r120_checker.main --ifc path/to/model.ifc --assumptions r120_checker/samples/assumptions.yaml --rules r120_checker/rules/r120_thresholds.yaml --out out
```

## `r120_checker/main.py`

```python
import argparse
import sys
from pathlib import Path
import json
import pandas as pd
import yaml

try:
    import ifcopenshell
except Exception as e:
    ifcopenshell = None

from .io_helpers import (
    iter_structural_elements,
    get_element_dims,
    get_concrete_class,
    get_layered_thickness,
)

PASS, FAIL, UNKNOWN = "PASS", "FAIL", "UNKNOWN"


def load_yaml(p: Path):
    with open(p, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def decide_r120(elem_kind, dims, conc_class, rules, assumptions):
    """Return PASS/FAIL/UNKNOWN and reasons as dict."""
    reasons = []
    r = rules.get(elem_kind.lower(), {})
    if not r:
        return UNKNOWN, {"reason": f"no rules for {elem_kind}"}

    # concrete class check
    req_cc = r.get("min_concrete_class", "C25/30")
    if not conc_class:
        reasons.append("concrete class missing -> using default/assumption")
        conc_ok = assumptions.get("defaults", {}).get("concrete_class", None) is not None
        if not conc_ok:
            return UNKNOWN, {"reason": "missing concrete class and no default"}
    else:
        conc_ok = conc_class_meets(conc_class, req_cc)
    if not conc_ok:
        reasons.append(f"conc class below {req_cc}")

    # cover / axis distance
    cover_req = r.get("min_cover_mm")
    cover = assumptions.get("cover_mm", {}).get(elem_kind.lower())
    if cover_req is not None:
        if cover is None:
            return UNKNOWN, {"reason": "axis distance/cover unknown"}
        if cover < cover_req:
            reasons.append(f"cover {cover} < {cover_req} mm")

    # dims check
    dims_req = r.get("min_dims_mm", {})
    dims_ok = True
    for k, req in dims_req.items():
        val = dims.get(k)
        if val is None:
            return UNKNOWN, {"reason": f"missing dimension {k}"}
        if val < req:
            reasons.append(f"{k} {val} < {req} mm")
            dims_ok = False

    status = PASS if (conc_ok and dims_ok and not reasons) else (FAIL if any("<" in s for s in reasons) else UNKNOWN)
    return status, {"reasons": reasons, "req": r}


def conc_class_meets(found: str, required: str) -> bool:
    def parse_cc(s):
        # naive Cxx/yy parser -> returns numeric  (xx)
        try:
            s = s.upper().replace(" ", "")
            if s.startswith("C") and "/" in s:
                return int(s.split("/")[0][1:])
        except Exception:
            return None
        return None
    f = parse_cc(found)
    r = parse_cc(required)
    return f is not None and r is not None and f >= r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ifc", required=True)
    ap.add_argument("--assumptions", required=True)
    ap.add_argument("--rules", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    if ifcopenshell is None:
        print("ERROR: ifcopenshell is not installed in this environment.")
        sys.exit(2)

    model = ifcopenshell.open(args.ifc)
    rules = load_yaml(Path(args.rules))
    assumptions = load_yaml(Path(args.assumptions))

    rows = []
    for elem in iter_structural_elements(model):
        kind = elem.is_a()
        guid = elem.GlobalId
        name = getattr(elem, "Name", "")

        dims = get_element_dims(elem)
        if dims is None and kind.lower() in ("ifcwall", "ifcwallstandardcase", "ifcslab"):
            t = get_layered_thickness(elem)
            dims = {"thickness": t} if t else None

        conc_class = get_concrete_class(elem)
        status, meta = decide_r120(kind, dims or {}, conc_class, rules, assumptions)

        rows.append({
            "GlobalId": guid,
            "Name": name,
            "Type": kind,
            "Dimensions": json.dumps(dims, ensure_ascii=False),
            "ConcreteClass": conc_class or assumptions.get("defaults", {}).get("concrete_class"),
            "Status": status,
            "Notes": json.dumps(meta, ensure_ascii=False)
        })

    df = pd.DataFrame(rows)
    df.to_csv(out / "report.csv", index=False)
    print(f"Wrote {len(df)} rows -> {out / 'report.csv'}")

if __name__ == "__main__":
    main()
```

## `r120_checker/io_helpers.py`

```python
from typing import Dict, Iterator, Optional

try:
    import ifcopenshell
    import ifcopenshell.util.element as ifc_elem
except Exception:
    ifcopenshell = None

STRUCT_TYPES = ("IfcWall", "IfcWallStandardCase", "IfcColumn", "IfcBeam", "IfcSlab")


def iter_structural_elements(model) -> Iterator["ifcopenshell.entity_instance"]:
    for t in STRUCT_TYPES:
        for e in model.by_type(t):
            yield e


def get_element_dims(elem) -> Optional[Dict[str, float]]:
    """Try to read section dimensions for columns/beams, or slab/wall thickness via profile/bbox.
    Returns a dict in mm: {width, height} OR {thickness}
    """
    # Profile based (rectangle common in structural)
    try:
        prof = getattr(elem, "Representation", None)
        # TODO: robust traversal -> here we fall back to bbox as a minimal demo
    except Exception:
        prof = None

    # naive bbox fallback (mm)
    try:
        bb = elem.get_info().get("BoundingBox", None)
        if bb:
            w = abs(bb[3] - bb[0]) * 1000
            h = abs(bb[4] - bb[1]) * 1000
            t = abs(bb[5] - bb[2]) * 1000
            # Heuristic: for beams/columns choose two largest as width/height
            vals = sorted([w, h, t], reverse=True)
            return {"width": vals[1], "height": vals[0]}
    except Exception:
        pass
    return None


def get_layered_thickness(elem) -> Optional[float]:
    try:
        rel_mats = [r for r in elem.HasAssociations or [] if r.is_a("IfcRelAssociatesMaterial")]
        for r in rel_mats:
            mat = r.RelatingMaterial
            if mat and mat.is_a("IfcMaterialLayerSetUsage"):
                return sum([layer.LayerThickness for layer in mat.ForLayerSet.MaterialLayers])
            if mat and mat.is_a("IfcMaterialLayerSet"):
                return sum([layer.LayerThickness for layer in mat.MaterialLayers])
    except Exception:
        return None
    return None


def get_concrete_class(elem) -> Optional[str]:
    # Look for material names containing Cxx/yy pattern
    try:
        rel_mats = [r for r in elem.HasAssociations or [] if r.is_a("IfcRelAssociatesMaterial")]
        for r in rel_mats:
            mat = r.RelatingMaterial
            # IfcMaterial or IfcMaterialLayer
            def extract_name(m):
                try:
                    n = getattr(m, "Name", None)
                    if n and "C" in n and "/" in n:
                        return n
                except Exception:
                    return None
                return None
            if mat is None:
                continue
            if mat.is_a("IfcMaterial"):
                n = extract_name(mat)
                if n:
                    return n
            if mat.is_a("IfcMaterialLayerSetUsage"):
                for layer in mat.ForLayerSet.MaterialLayers:
                    n = extract_name(layer.Material)
                    if n:
                        return n
            if mat.is_a("IfcMaterialLayerSet"):
                for layer in mat.MaterialLayers:
                    n = extract_name(layer.Material)
                    if n:
                        return n
    except Exception:
        return None
    return None
```

## `r120_checker/rules/r120_thresholds.yaml`

```yaml
# Minimal, adjust to your course table
wall:
  min_concrete_class: "C25/30"
  min_cover_mm: 35
  min_dims_mm:
    thickness: 220

ifcwall:
  <<: *wall

ifcwallstandardcase:
  min_concrete_class: "C25/30"
  min_cover_mm: 35
  min_dims_mm:
    thickness: 220

ifcslab:
  min_concrete_class: "C25/30"
  min_cover_mm: 35
  min_dims_mm:
    thickness: 200

ifccolumn:
  min_concrete_class: "C25/30"
  min_cover_mm: 57  # axis distance
  min_dims_mm:
    width: 350
    height: 350

ifcbeam:
  min_concrete_class: "C25/30"
  min_cover_mm: 60  # axis distance
  min_dims_mm:
    width: 240
    height: 240
```

## `r120_checker/samples/assumptions.yaml`

```yaml
# Default assumptions when data is missing in IFC
defaults:
  concrete_class: "C30/37"

# axis distance (cover to main bars), by type
cover_mm:
  ifcwall: 35
  ifcwallstandardcase: 35
  ifcslab: 35
  ifccolumn: 57
  ifcbeam: 60

# load level under fire (µ_fi) by element type or storey
mu_fi:
  default: 0.7

# exposure sides policy (used for reporting only in this skeleton)
exposure:
  beam: 3
  column: 4
  wall: 1
  slab: 1
```

---

## How to use this package

1. Open **bpmn.io**, `Import > Paste XML` → export **SVG** and save in `A2/IMG/`.
2. Copy the A2 sections above into `A2/README.md`.
3. Put the `r120_checker/` folder at repo root; install deps; run the sample command.
4. Replace table thresholds/assumptions with your course‑approved values.
5. When you run on your model, attach `report.csv` to your A3 and link in A2.

