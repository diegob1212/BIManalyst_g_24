# A2: Use Case — Structural + Fire Safety (R 120, EN 1992‑1‑2)

> Focus area: **Structural + Fire Safety**
> Use case theme: **Automated check of R120 fire resistance for walls** for load bearing concrete walls in Advanced Building Design model #2508.

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

* It directly addresses our group’s focus area (structural including fire safety).

* It is measurable and testable: IFC files provide element types, dimensions, and materials that can be compared to the Eurocode requirements.

---

## A2c — Use Case (how/when/what)

**How to check**
* We can check the claim by firstly verifying all load-bearing concrete walls and then see if those walls achieve R 120 per EN 1992-1-2 by comparing IFC model data to the Euro code requirments (wall thickness & concrete class)
* 
**When to check:**
* This claim would need to be checked at design phase at key gates (30/60/90%) and again before IFC issue. Finally, it is also needed for as‑built verification. So it will need to be chekced at the design and build phase.

**Information relied on:**
* From IFC: element class (IfcWall), wall thickness (from IfcMaterialLayerSet → LayerThickness), concrete material/class.
 
**BIM purpose:** 
* Several BIM purposes are required. First, we need to gather the structural wall information in order to analyse it. Once it has been compared to the Eurocode requirements, our goal is to communicate whether the fire safety (R120) requirement is met or not.

**Closest BIM use case:** 
The most relevant existing BIM use case is '08 Structural Analysis'.

<img width="2037" height="1046" alt="image" src="https://github.com/user-attachments/assets/07626271-907e-4036-bbf8-9f6144e144f0" />

---

## A2d — Scope the use case (where a new tool is needed)

<img width="2029" height="1042" alt="image" src="https://github.com/user-attachments/assets/f305ea32-c755-4dc7-8cff-5fe0cb337fbb" />

---

## A2e — Tool Idea (OpenBIM ifcOpenShell)

**Tool description**

r120_checker — Automated verification of R 120 fire resistance (EN 1992-1-2) for concrete walls, columns, beams and slabs from an IFC model.

What it does ?

The tool reads a discipline IFC (model.ifc) and identifies scope elements as IfcWall/IfcWallStandardCase, IfcColumn, IfcBeam, IfcSlab. It will then extract the data like Geometry (thickness for walls  via IfcMaterialLayerSet, width/height for beams/columns via section profile or bbox) or Material/Concrete class from associated materials (e.g., C30/37), with a declared default if missing. In this case we will focus our work on walls.

It will then apply the tabulated thresholds (based on requirements for R120): minimum dimensions, concrete class.

In the end, we want our model to be able to classify each element: PASS (meets thresholds), FAIL (below threshold), UNKNOWN (data gap).

**Why this is valuable (business & societal)**

This tool could help different aspects of a project :

* Safety & compliance: Surfaces life-safety risks (insufficient thickness/cover/concrete class) early, before construction.

* Time & cost: Reduces manual checks and redesign iterations by automating a repeatable, auditable verification.

* Transparency: PASS/FAIL/UNKNOWN with explicit reasons and GlobalId traceability supports approvals and handovers.

**BMPN Diagram summarized**
<img width="2028" height="1040" alt="image" src="https://github.com/user-attachments/assets/85f2e0a4-6c96-435d-9f79-30bcb18a7e27" />

---

## A2f — Information Requirements


| Requirement | Where in IFC | In our models? | How we get it with ifcOpenShell | Notes  |
|--------------|--------------|----------------|----------------------------------|--------------------|
| **Units (mm vs m)** | `IfcProject.UnitsInContext` → `IfcSIUnit / IfcConversionBasedUnit` (Length) | Yes | Read once to build a **mm scale** factor | Needed to convert geometry to mm consistently. |
| **Element type (walls)** | `IfcWall`, `IfcWallStandardCase` | Yes | `model.by_type("IfcWall")`, etc. | Scope of the checker. |
| **GlobalId / Name** | Entity attributes | Yes | `elem.GlobalId`, `elem.Name` | Used for traceability. |
| **Wall thickness** | `IfcRelAssociatesMaterial` → `IfcMaterialLayerSet(Usage)` → `MaterialLayers[].LayerThickness` (sum) | Often | Sum layer thicknesses; else **bbox** min dimension | Primary input for **R120**. |
| **Material / Concrete detection** | `IfcRelAssociatesMaterial` → `IfcMaterial` or layer material `Name` | Often | Parse names for “concrete”, “beton”, or `Cxx/yy` pattern | None. |



**Learning needs:** robust ifcOpenShell queries, geometry thickness extraction.

---

## A2g — Software Licence


**to change what software**
* Blender, BPMN, Github, Anaconda & Python

---



