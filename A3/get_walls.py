# -*- coding: utf-8 -*-
"""
CLAIM : check R120 requirements. 220 mm of thickness and concrete class
get_walls.py — Select walls that are both 'Interior Wall' and 'Load Bearing'

"""

import ifcopenshell


def get_loadbearing_interior_walls(model):
    """
    input : IFC model 
    Select all walls whose name/type includes BOTH:
      - 'Interior Wall'
      - 'Load Bearing'
    
    """
    all_walls = model.by_type("IfcWall") + model.by_type("IfcWallStandardCase")
    selected = []

    for wall in all_walls:
        name = (getattr(wall, "N me", "") or "").lower()
        obj_type = (getattr(wall, "ObjectType", "") or "").lower()
        desc = (getattr(wall, "Description", "") or "").lower()

        combined = f"{name} {obj_type} {desc}"

        if "interior wall" in combined and "load bearing" in combined and "non-load bearing" not in combined:
            selected.append(wall)

    print(f" Found {len(selected)} interior load-bearing walls (excluding 'Non-Load Bearing') out of {len(all_walls)} total.")
    return selected

"""
THis function can be develop in another project. This is a basic selsction who trusts the model who says which walls are load-beearing.
Other functions can be implemented that checks if the walls are really load bearing or not. So it doesn't check the validity of the project
but trut it

"""
