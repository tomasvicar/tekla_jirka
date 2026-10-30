"""Vygeneruje malý syntetický IFC4 model ocelové haly (sloupy, příčle, vaznice, ztužidla).

Spuštění:  uv run --with ifcopenshell python make_ifc.py
Ukázka pro workshop „Claude pro stavaře“. Do modelu jsou ZÁMĚRNĚ vloženy chyby
(chybějící fáze, odlišná ocel, prvek bez profilu v názvu), aby měla kontrola co najít.
"""
import math
from pathlib import Path

import numpy as np
import ifcopenshell
import ifcopenshell.api as api
import ifcopenshell.api.project, ifcopenshell.api.root, ifcopenshell.api.unit, ifcopenshell.api.context, ifcopenshell.api.aggregate, ifcopenshell.api.material, ifcopenshell.api.geometry, ifcopenshell.api.pset, ifcopenshell.api.spatial  # noqa: E401
import ifcopenshell.guid

OUT = Path(__file__).parent / "hala_lipnik.ifc"

SPAN, BAY, NBAYS, H, PITCH = 18.0, 6.0, 5, 6.0, math.radians(5)
LEN = BAY * NBAYS
# profil: (h, b, tw, tf, r) v metrech
PROF = {
    "IPE 400": (0.400, 0.180, 0.0086, 0.0135, 0.021),
    "IPE 360": (0.360, 0.170, 0.0080, 0.0127, 0.018),
    "IPE 160": (0.160, 0.082, 0.0050, 0.0074, 0.009),
    "IPE 220": (0.220, 0.110, 0.0059, 0.0092, 0.012),
}

f = api.project.create_file(version="IFC4")
proj = api.root.create_entity(f, ifc_class="IfcProject", name="2026-031 Hala Lipník (fiktivní)")
length = api.unit.add_si_unit(f, unit_type="LENGTHUNIT")
api.unit.assign_unit(f, units=[length])
model = api.context.add_context(f, context_type="Model")
body = api.context.add_context(f, context_type="Model", context_identifier="Body", target_view="MODEL_VIEW", parent=model)
site = api.root.create_entity(f, ifc_class="IfcSite", name="Staveniště")
bldg = api.root.create_entity(f, ifc_class="IfcBuilding", name="Hala A")
storey = api.root.create_entity(f, ifc_class="IfcBuildingStorey", name="0.NP")
api.aggregate.assign_object(f, products=[site], relating_object=proj)
api.aggregate.assign_object(f, products=[bldg], relating_object=site)
api.aggregate.assign_object(f, products=[storey], relating_object=bldg)

materials = {g: api.material.add_material(f, name=g, category="steel") for g in ("S355J2", "S235JR")}
profiles = {}
for name, (h, b, tw, tf, r) in PROF.items():
    profiles[name] = f.create_entity("IfcIShapeProfileDef", ProfileType="AREA", ProfileName=name,
                                     OverallWidth=b, OverallDepth=h, WebThickness=tw, FlangeThickness=tf, FilletRadius=r)
rod = f.create_entity("IfcCircleProfileDef", ProfileType="AREA", ProfileName="D20", Radius=0.010)
profiles["D20"] = rod

elements = []
counter = {"n": 0}


def placement_matrix(p1, p2, up_hint):
    p1, p2 = np.array(p1, float), np.array(p2, float)
    z = p2 - p1
    length = float(np.linalg.norm(z))
    z /= length
    x = np.cross(np.array(up_hint, float), z)
    if np.linalg.norm(x) < 1e-6:
        x = np.cross([1.0, 0, 0], z)
    x /= np.linalg.norm(x)
    y = np.cross(z, x)
    m = np.eye(4)
    m[:3, 0], m[:3, 1], m[:3, 2], m[:3, 3] = x, y, z, p1
    return m, length


def member(cls, name, prof, p1, p2, phase=1, grade="S355J2", up=(0, 0, 1), assembly_prefix=None):
    counter["n"] += 1
    el = api.root.create_entity(f, ifc_class=cls, name=name)
    m, L = placement_matrix(p1, p2, up)
    api.geometry.edit_object_placement(f, product=el, matrix=m)
    rep = api.geometry.add_profile_representation(f, context=body, profile=profiles[prof], depth=L)
    api.geometry.assign_representation(f, product=el, representation=rep)
    api.material.assign_material(f, products=[el], type="IfcMaterial", material=materials[grade])
    ps = api.pset.add_pset(f, product=el, name="Workshop_Common")
    props = {"Profile": prof, "AssemblyMark": f"{assembly_prefix or name[:1]}{counter['n']}", "Length_mm": round(L * 1000)}
    if phase is not None:
        props["Phase"] = phase
    api.pset.edit_pset(f, pset=ps, properties=props)
    elements.append(el)
    return el


# osy: X podél haly, Y napříč, Z nahoru
ridge = H + SPAN / 2 * math.tan(PITCH)
for i in range(NBAYS + 1):
    x = i * BAY
    phase = 1 if i <= 2 else 2
    member("IfcColumn", "SLOUP", "IPE 400", (x, -SPAN / 2, 0), (x, -SPAN / 2, H), phase, up=(0, 1, 0), assembly_prefix="C")
    # záměrná chyba: jeden sloup z jiné oceli
    member("IfcColumn", "SLOUP", "IPE 400", (x, SPAN / 2, 0), (x, SPAN / 2, H), phase,
           grade="S235JR" if i == 3 else "S355J2", up=(0, 1, 0), assembly_prefix="C")
    member("IfcBeam", "PŘÍČEL", "IPE 360", (x, -SPAN / 2, H), (x, 0, ridge), phase, assembly_prefix="B")
    member("IfcBeam", "PŘÍČEL", "IPE 360", (x, SPAN / 2, H), (x, 0, ridge), phase, assembly_prefix="B")

# vaznice po polích (prosté nosníky)
n_seg = 4
for side in (-1, 1):
    for k in range(n_seg + (0 if side == 1 else 1)):
        t = k / n_seg
        y = side * SPAN / 2 * (1 - t)
        z = H + t * SPAN / 2 * math.tan(PITCH) + 0.28
        for i in range(NBAYS):
            ph = 1 if i < 2 else 2
            # záměrná chyba: tři vaznice bez fáze
            missing = side == 1 and k == 1 and i in (1, 2, 3)
            member("IfcBeam", "VAZNICE", "IPE 160", (i * BAY, y, z), ((i + 1) * BAY, y, z),
                   None if missing else ph, assembly_prefix="P")

# štítové sloupky
for x in (0.0, LEN):
    for yy in (-SPAN / 6, SPAN / 6):
        top = H + (SPAN / 2 - abs(yy)) * math.tan(PITCH) - 0.2
        member("IfcColumn", "ŠTÍTOVÝ SLOUPEK", "IPE 220", (x, yy, 0), (x, yy, top), 1 if x == 0 else 2,
               up=(0, 1, 0), assembly_prefix="W")

# ztužidla v krajních polích (střecha + stěny)
for bi in (0, NBAYS - 1):
    x0, x1 = bi * BAY, (bi + 1) * BAY
    ph = 1 if bi == 0 else 2
    for side in (-1, 1):
        ye, z_e = side * SPAN / 2, H + 0.05
        member("IfcMember", "ZTUŽIDLO", "D20", (x0, ye, z_e), (x1, 0, ridge + 0.05), ph, assembly_prefix="X")
        member("IfcMember", "ZTUŽIDLO", "D20", (x0, 0, ridge + 0.05), (x1, ye, z_e), ph, assembly_prefix="X")
        member("IfcMember", "ZTUŽIDLO", "D20", (x0, ye, 0.2), (x1, ye, H), ph, assembly_prefix="X")
        member("IfcMember", "ZTUŽIDLO", "D20", (x0, ye, H), (x1, ye, 0.2), ph, assembly_prefix="X")

# záměrná chyba: prvek s obecným názvem a bez fáze
member("IfcMember", "Member", "IPE 160", (LEN / 2, -SPAN / 2 - 0.3, 3.0), (LEN / 2 + BAY, -SPAN / 2 - 0.3, 3.0), None, assembly_prefix="M")

api.spatial.assign_container(f, products=elements, relating_structure=storey)
f.write(str(OUT))
print(f"{OUT.name}: {len(elements)} prvků")
