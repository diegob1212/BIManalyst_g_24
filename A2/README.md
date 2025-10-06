# A2: Use Case — Structural + Fire Safety (R 120, EN 1992‑1‑2)

> Focus area: **Structural + Fire Safety**
> Use case theme: **Automated check of R120 fire resistance (tabulated method)** for load bearing concrete walls in Advanced Building Design model #2508.

---

## A2a — About our group

* **Members:** Diego Bruttin s251895 Jonas Alakuzay s170494
* **Roles:** **Analyst** 
* **Coding confidence (0–4 per person):** 3 and 1 → **Group total:** 4
* Our group focus area is structural including fire safety. We are an analyst group.

---

## A2b — Identify Claim

**Claim to check:**
Do the Load‑bearing concrete walls comply with **R 120** per **EN 1992‑1‑2** dimensions and concrete strength class. 
Found in D_Report_Team08_STR page 27-28 section 10 Structural Fire Safety. We select building 2508 to focus on.

This claim asserts that the concrete walls in the renovated Building 308 achieve R 120 fire resistance. According to EN 1992-1-2 (Eurocode 2, Part 1-2), a structure achieves R 120 if it can maintain its load-bearing capacity for 120 minutes under fire exposure. For the element to comply it requires specific minimums in thickness dimension and concrete strength class which is given in the euro code. If these thresholds are met, the element is considered compliant without further advanced calculation.

**Justification**

Fire resistance is directly tied to occupant life safety, structural robustness, and compliance with building regulations.

The criteria are explicit, checkable against model data (IFC geometry, materials, property sets) and can be automated in Python using ifcOpenShell.

It is a perfect candidate for a digital compliance check, validating the claim ensures that modelled structural elements are not only geometrically valid but also code-compliant under fire.

Among all potential claims in the report this one was selected because:  

It directly addresses our group’s focus area (structural including fire safety).

It is measurable and testable: IFC files provide element types, dimensions, and materials that can be compared to the Eurocode requirements.

---

## A2c — Use Case (how/when/what)

**How to check**
* We can check the claim by verifying that all primary load-bearing concrete walls, columns, beams and slabs achieve R 120 per EN 1992-1-2 (tabulated method) by comparing IFC model data to tabulated minima (dimensions, concrete class, axis distance/cover).

**When to check:**

* This claim would need to be checked at design phase at key gates (30/60/90%) and again before IFC issue. Finally, it is also needed for as‑built verification. So it will need to be chekced at the design and build phase.

**Information relied on:**

* From IFC: element class, dimensions/thickness (profile or material layers), concrete material/class (if present), any `FireRating` string.
* From team inputs: **µ_fi** by typology, **exposure sides** policy, **default concrete cover** per element type when rebar is not modeled.
 
**BIM purpose:** 
* They are several BIM purposes required. First we will need to gather information in order ton analyse it. Once it has been compared to the standards, our goal will be to communicate the result in order to say if the fire safety requirements are met or not.

**Closest BIM use case:** 
dont understand this question as to speak with manager to know

**BPMN overview**


have to do it ourselves 

**Example**
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

---

## A2e — Tool Idea (OpenBIM ifcOpenShell)

**Tool description**

r120_checker — Automated verification of R 120 fire resistance (EN 1992-1-2, tabulated method) for concrete walls, columns, beams and slabs from an IFC model.

What it does ?

The tool reads a discipline IFC (model.ifc) and identifies scope elements: IfcWall/IfcWallStandardCase, IfcColumn, IfcBeam, IfcSlab. It will then extract the data like Geometry (thickness for walls/slabs via IfcMaterialLayerSet, width/height for beams/columns via section profile or bbox) or Material/Concrete class from associated materials (e.g., C30/37), with a declared default if missing.

It will then apply the tabulated thresholds (based on requirements for R120): minimum dimensions, concrete class, and axis distance/cover.

In the end, we want our model to be able to classify each element: PASS (meets thresholds), FAIL (below threshold), UNKNOWN (data gap).

**Why this is valuable (business & societal)**

This tool could help different aspects of a project :

* Safety & compliance: Surfaces life-safety risks (insufficient thickness/cover/concrete class) early, before construction.

* Time & cost: Reduces manual checks and redesign iterations by automating a repeatable, auditable verification.

* Transparency: PASS/FAIL/UNKNOWN with explicit reasons and GlobalId traceability supports approvals and handovers.

**last part question has to be made**

---

## A2f — Information Requirements

| Requirement                  | Where in IFC                                                    | Expected? | Handling                                                  |
| ---------------------------- | --------------------------------------------------------------- | --------- | --------------------------------------------------------- |
| Element type                 | `IfcWall*`, `IfcBeam`, `IfcColumn`, `IfcSlab`                   | Yes       | Query via ifcOpenShell type filters                       |
| Thickness (walls/slabs)      | `IfcMaterialLayerSet` → `MaterialLayers[].LayerThickness` (sum) | Often     | Sum layers or fallback to solid geometry thickness        |
| Section dims (beams/columns) | `IfcProfileDef` (e.g., `IfcRectangleProfileDef`) or BRep bbox   | Often     | Use profile; fallback to bbox with sanity checks          |
| Concrete class (≥ C25/30)    | `IfcMaterial`/`Pset_ConcreteElementGeneral`/Name                | Sometimes | Parse; else default in `assumptions.yaml`                 |
| Axis distance / cover        | Rebar entities (`IfcReinforcingBar`) or Psets                   | Rare      | Use defaults in assumptions; mark **UNKNOWN** if critical |
| FireRating (declared)        | `Pset_*Common.FireRating`                                       | Sometimes | Compare “claimed” vs computed result                      |

**Learning needs:** robust ifcOpenShell queries, geometry thickness extraction, BCF generation, YAML config, reproducible reporting.

---

## A2g — Software Licence


**to change what software**
* **MIT** (simple/permissive) or **Apache‑2.0** (permissive with explicit patent grant).
* Recommended: **Apache‑2.0** for classroom collaboration and reuse.

---



