# A5 — Reflection: OpenBIM Fire & Structural Safety Checker

## Group Focus Area
**Focus:** Structural + Fire Safety  
**Use Case:** Verification of Load-Bearing Walls and Fire Resistance (R120) using IFC models  
**Team Members:** [Add your names here]  

---

## 1. Learning Experience and Concept Focus

At the beginning of this course, our understanding of OpenBIM workflows was mainly conceptual — we knew IFC was a data format, but we didn’t yet grasp how to use it to **automate model validation** or extract structured information. Through the assignments (A1–A4), we progressively learned how to define a use case, model a process (BPMN), and implement an actual **Python-based OpenBIM tool** with `ifcopenshell`.

Our concept — **fact-checking structural fire safety claims (R120)** — forced us to engage deeply with the **data structure of IFC models**. We learned to identify not only what data exists (geometry, material, properties) but also what is missing, and how to handle incomplete BIM data using assumptions, tolerances, and derived logic.

In practice, this meant learning:
- How to query and filter entities like `IfcWall`, `IfcSlab`, and `IfcRelAssociatesMaterial`.
- How to detect materials and thicknesses for fire verification.
- How to interpret and visualize information in an **analytical BIM context**, not just 3D geometry.

By implementing a real OpenBIM script, we understood the link between **BIM information quality** and **regulatory checking** — a key insight for future digital compliance workflows.

---

## 2. My Development During the Course

| Skill / Concept | At Start of Course | At End of Course |
|-----------------|-------------------|------------------|
| Understanding of IFC data model | Basic — only knew IFC was an open standard | Good — can navigate entities, property sets, and relations |
| Python for BIM | Limited (basic data handling) | Intermediate — capable of developing a complete IFC analysis tool |
| Fire safety design (EN 1992-1-2) | Theoretical understanding only | Practical — implemented tabulated method as code rules |
| BIM use case modelling (BPMN) | Never used before | Confident — able to map full information exchanges |
| Tool interoperability | Limited awareness | Strong — able to extract, process, and communicate results across models (STR + ARCH) |

---

## 3. What I Still Need to Learn

- **IFC geometry handling**: precise geometric operations (beyond bounding boxes) using `ifcopenshell.geom` or `IfcOpenShell.geom.create_shape`.  
- **Property standardization**: handling different naming conventions and localization (e.g., `Pset_WallCommon`, custom property sets).  
- **BCF integration**: exporting issues directly into BIM coordination tools (Solibri, BIMcollab).  
- **Automation frameworks**: connecting OpenBIM scripts with CI/CD pipelines for automated model checking.

---

## 4. How I Might Use OpenBIM in the Future

In the future, I see OpenBIM as a **core framework** for integrating analysis and design verification across disciplines:
- **Academic use (thesis):** Applying OpenBIM to validate sustainability, structural safety, or LCA metrics automatically.  
- **Professional practice:** Developing or adapting scripts to check compliance for fire resistance, accessibility, or energy performance before model submission.  
- **Collaborative work:** Using shared IFC models to bridge gaps between architects, engineers, and fire safety specialists through transparent data exchange.

---

## 5. Process of Developing the Tutorial (A3–A4)

Developing our Python tutorial (A3–A4) was one of the most valuable parts of the course. We started with a conceptual BPMN diagram (A2), then converted it into a real **fact-checking script** that identifies load-bearing walls and verifies R120 compliance.  
The process required:
- Iterative debugging with `ifcopenshell`.  
- Testing with both **architectural** and **structural** models to handle inconsistent data.  
- Learning to express results clearly (CSV, table, or visual feedback).  

This development forced us to combine **structural reasoning** with **data reasoning** — deciding what counts as a “load-bearing wall” when data is incomplete, and implementing a scoring heuristic.  

---

## 6. Reflection on the Course Design

- **Choice of use case:** The freedom to select our focus area (fire & structure) made the learning more personal. Although it added complexity, it encouraged autonomy and creativity.  
  → Would we prefer less choice? Probably not — the open format helped us explore genuine interests.

- **Number of tools:** The balance was good. BPMN.io, Markdown, GitHub, and Python (ifcopenshell) were sufficient. Adding more tools might have distracted from the main goal — understanding the **information logic** of BIM.

- **Process & outcomes:** Each assignment (A1–A4) built logically on the previous one, and A3–A4 gave us the confidence to build a functional prototype tool.

- **Relation to thesis:** Yes — this project raised new questions that could lead to thesis topics, such as **automated regulatory checking**, **fire safety verification**, and **OpenBIM for digital compliance**.

---

## 7. Feedback Summary (as a Group)

Our peers appreciated that our tool addressed a **concrete and safety-critical use case**.  
Feedback highlights:
- The **logic for detecting load-bearing walls** without relying on the `LoadBearing` flag was considered innovative and realistic.  
- Some feedback suggested visualizing the results directly in 3D (e.g., color-coded walls), which could be a good future extension.  
- The **R120 verification logic** was clear and linked to Eurocode standards — a strong point.  

### What stage does our tool work in Advanced Building Design?
Our tool supports **Stage B–C** (Design & Analysis):
- **Stage B:** Quality assurance of the model before coordination.
- **Stage C:** Early compliance checks before detailed fire design.

---

## 8. Individual Future Outlook

**Will I use OpenBIM tools in my thesis?**  
Yes — the course gave me enough confidence to apply OpenBIM workflows to a structural or sustainability topic.  

**Will I use OpenBIM tools in professional life?**  
Very likely. Over the next 10 years, automation and model-based validation will be standard in design offices. Knowing how to inspect and script IFC files gives a real advantage.

---

## 9. Wrap-Up — Journey from A1 → A5

- **A1 (Explore):** Defined our general focus on structural & fire safety in buildings.  
- **A2 (Use Case):** Designed the process in BPMN and identified the claim to check (“Walls satisfy R120 fire resistance”).  
- **A3 (Tool):** Implemented the first Python prototype using ifcopenshell.  
- **A4 (Teach):** Documented the method as a tutorial for others.  
- **A5 (Reflect):** Looked back at what we learned, built, and understood about OpenBIM as a method.

> Through A1–A5, our perspective shifted:  
> From **“BIM as 3D geometry”** → to **“BIM as structured, verifiable information.”**  
> We learned to use OpenBIM not only to visualize design but to **prove performance and compliance.**

---

*End of Reflection – Group Fire & Structure*

