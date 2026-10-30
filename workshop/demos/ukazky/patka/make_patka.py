"""Parametrický výkres patní desky sloupu (DXF + SVG + PDF).

Spuštění:  uv run --with ezdxf --with pillow python make_patka.py
Ukázka pro workshop „Claude pro stavaře“. Rozměry jsou ilustrativní,
NEJDE o posouzený detail – kotvení a desku musí navrhnout statik.
"""
from pathlib import Path

import ezdxf
from ezdxf.addons.drawing import Frontend, RenderContext, layout, svg
from ezdxf.addons.drawing.config import BackgroundPolicy, ColorPolicy, Configuration
from ezdxf.enums import TextEntityAlignment

OUT = Path(__file__).parent

# --- parametry (mm)
P = dict(
    sloup="HEA 240", h=230, b=240, tw=7.5, tf=12,
    deska_a=440, deska_b=400, t=25,          # půdorys desky (ve směru h × ve směru b), tloušťka
    rozteč_a=330, rozteč_b=290,              # osové vzdálenosti kotev
    kotva="M24", otvor=30, podlozka=60, podlití=40, kotva_delka=500,
    svar_pasnice=6, svar_stojina=4,
    zakazka="2026-031 Hala Lipník (fiktivní)", vykres="D-101", revize="A",
)

doc = ezdxf.new("R2018", setup=True)
doc.units = ezdxf.units.MM
msp = doc.modelspace()
for name, color, lt in [
    ("DESKA", 7, "CONTINUOUS"), ("SLOUP", 5, "CONTINUOUS"), ("OSY", 1, "DASHDOT"),
    ("OTVORY", 3, "CONTINUOUS"), ("KOTVY", 6, "CONTINUOUS"), ("BETON", 8, "CONTINUOUS"),
    ("KOTY", 2, "CONTINUOUS"), ("TEXT", 7, "CONTINUOUS"), ("RAZITKO", 7, "CONTINUOUS"),
    ("SKRYTE", 8, "DASHED"),
]:
    doc.layers.add(name, color=color, linetype=lt)

dim_style = doc.dimstyles.new("KOTY_10")
dim_style.dxf.dimtxt = 10
dim_style.dxf.dimasz = 7
dim_style.dxf.dimexe = 4
dim_style.dxf.dimexo = 3
dim_style.dxf.dimgap = 2
dim_style.dxf.dimdec = 0


def rect(x0, y0, w, h, layer):
    msp.add_lwpolyline([(x0, y0), (x0 + w, y0), (x0 + w, y0 + h), (x0, y0 + h)], close=True, dxfattribs={"layer": layer})


def text(s, x, y, h=10, layer="TEXT", align=TextEntityAlignment.LEFT):
    msp.add_text(s, height=h, dxfattribs={"layer": layer, "style": "OpenSans"}).set_placement((x, y), align=align)


def hdim(x1, x2, y, base_y):
    msp.add_linear_dim(base=(x1, base_y), p1=(x1, y), p2=(x2, y), dimstyle="KOTY_10", dxfattribs={"layer": "KOTY"}).render()


def vdim(y1, y2, x, base_x):
    msp.add_linear_dim(base=(base_x, y1), p1=(x, y1), p2=(x, y2), angle=90, dimstyle="KOTY_10", dxfattribs={"layer": "KOTY"}).render()


A, B, t = P["deska_a"], P["deska_b"], P["t"]
h, b, tw, tf = P["h"], P["b"], P["tw"], P["tf"]

# ===== PŮDORYS (střed desky v 0,0); osa x = směr výšky profilu h
rect(-A / 2, -B / 2, A, B, "DESKA")
# HEA: pásnice jsou rovnoběžné s osou y (profil natočený stojinou ve směru x)
I = [(-h / 2, -b / 2), (-h / 2 + tf, -b / 2), (-h / 2 + tf, -tw / 2), (h / 2 - tf, -tw / 2), (h / 2 - tf, -b / 2),
     (h / 2, -b / 2), (h / 2, b / 2), (h / 2 - tf, b / 2), (h / 2 - tf, tw / 2), (-h / 2 + tf, tw / 2),
     (-h / 2 + tf, b / 2), (-h / 2, b / 2)]
msp.add_lwpolyline(I, close=True, dxfattribs={"layer": "SLOUP"})
hatch = msp.add_hatch(color=5, dxfattribs={"layer": "SLOUP"})
hatch.set_pattern_fill("ANSI31", scale=0.6)
hatch.paths.add_polyline_path(I, is_closed=True)
ra, rb = P["rozteč_a"] / 2, P["rozteč_b"] / 2
for sx in (-1, 1):
    for sy in (-1, 1):
        cx, cy = sx * ra, sy * rb
        msp.add_circle((cx, cy), P["otvor"] / 2, dxfattribs={"layer": "OTVORY"})
        msp.add_circle((cx, cy), P["podlozka"] / 2, dxfattribs={"layer": "SKRYTE"})
        msp.add_line((cx - 25, cy), (cx + 25, cy), dxfattribs={"layer": "OSY"})
        msp.add_line((cx, cy - 25), (cx, cy + 25), dxfattribs={"layer": "OSY"})
msp.add_line((-A / 2 - 30, 0), (A / 2 + 30, 0), dxfattribs={"layer": "OSY"})
for sx in (-1, 1):  # značka řezu A–A
    msp.add_lwpolyline([(sx * (A / 2 + 30), 0), (sx * (A / 2 + 30), -30)], dxfattribs={"layer": "TEXT", "const_width": 3})
    text("A", sx * (A / 2 + 45) - 6, -45, 14)
msp.add_line((0, -B / 2 - 30), (0, B / 2 + 30), dxfattribs={"layer": "OSY"})
hdim(-A / 2, A / 2, -B / 2, -B / 2 - 70)
hdim(-ra, ra, -rb, -B / 2 - 40)
vdim(-B / 2, B / 2, A / 2, A / 2 + 70)
vdim(-rb, rb, ra, A / 2 + 40)
text(f"4× otvor Ø{P['otvor']}", ra + 20, rb + 35, 10)
text("PŮDORYS 1:10", -A / 2, B / 2 + 50, 16)
text(f"P{t} – {A}×{B} – S355J2", -A / 2, B / 2 + 25, 11)

# ===== ŘEZ (pod půdorysem); y0 = horní líc betonu
y0 = -B / 2 - 540
g = P["podlití"]
# beton
msp.add_lwpolyline([(-A / 2 - 120, y0), (A / 2 + 120, y0)], dxfattribs={"layer": "BETON"})
for i in range(-4, 5):
    msp.add_line((i * 70 - 10, y0), (i * 70 - 40, y0 - 30), dxfattribs={"layer": "BETON"})
text("BETON C30/37 – patka", A / 2 + 30, y0 - 25, 9)
# podlití
rect(-A / 2 - 10, y0, A + 20, g, "BETON")
text(f"podlití {g} mm – nesmršťující malta", A / 2 + 30, y0 + 12, 9)
# deska
rect(-A / 2, y0 + g, A, t, "DESKA")
# sloup (pohled na stojinu, řez ve směru h)
yc = y0 + g + t
rect(-h / 2, yc, tf, 200, "SLOUP")
rect(h / 2 - tf, yc, tf, 200, "SLOUP")
zz = [(-h / 2 - 20, yc + 200)] + [(-h / 2 + i * (h + 40) / 8 - 20, yc + 200 + (12 if i % 2 else -12)) for i in range(1, 8)] + [(h / 2 + 20, yc + 200)]
msp.add_lwpolyline(zz, dxfattribs={"layer": "SLOUP"})  # čára přerušení
text(P["sloup"], h / 2 + 15, yc + 150, 11)
# kotvy
for sx in (-1, 1):
    x = sx * ra
    d = 24
    rect(x - d / 2, y0 - P["kotva_delka"] + 80, d, P["kotva_delka"] - 80 + g + t + 45, "KOTVY")
    rect(x - P["podlozka"] / 2, yc, P["podlozka"], 6, "KOTVY")  # podložka
    rect(x - 22, yc + 6, 44, 20, "KOTVY")  # matice
    msp.add_line((x, y0 - P["kotva_delka"] + 60), (x, yc + 60), dxfattribs={"layer": "OSY"})
text(f"2+2× kotva {P['kotva']} – 8.8, délka {P['kotva_delka']}", ra + 40, y0 - 200, 9)
# svary (popis)
text(f"koutové svary: pásnice a{P['svar_pasnice']}, stojina a{P['svar_stojina']} – oboustranně", -A / 2, y0 + 380, 10)
vdim(y0, y0 + g, -A / 2 - 10, -A / 2 - 50)
vdim(y0 + g, y0 + g + t, -A / 2, -A / 2 - 50)
hdim(-ra, ra, y0 - P["kotva_delka"] + 80, y0 - P["kotva_delka"] + 40)
text("ŘEZ A–A 1:10", -A / 2, y0 + 410, 16)

# ===== RAZÍTKO (vpravo dole)
bx, by, bw, bh = 330, y0 - 470, 360, 130
rect(bx, by, bw, bh, "RAZITKO")
for yy in (by + 40, by + 70, by + 100):
    msp.add_line((bx, yy), (bx + bw, yy), dxfattribs={"layer": "RAZITKO"})
msp.add_line((bx + 280, by), (bx + 280, by + 70), dxfattribs={"layer": "RAZITKO"})
text("Zakázka: " + P["zakazka"], bx + 8, by + 110, 10)
text(f"Patní deska sloupu {P['sloup']} – kotvení {P['kotva']}", bx + 8, by + 80, 10)
text("Výkres: " + P["vykres"], bx + 8, by + 50, 10)
text("Rev.: " + P["revize"], bx + 288, by + 50, 10)
text("ILUSTRATIVNÍ – NEPOSOUZENO", bx + 8, by + 15, 10)
text("1:10", bx + 288, by + 15, 10)

dxf_path = OUT / "patka_HEA240.dxf"
doc.saveas(dxf_path)

# --- SVG náhled pro web (černé čáry na bílém)
ctx = RenderContext(doc)
backend = svg.SVGBackend()
cfg = Configuration(background_policy=BackgroundPolicy.WHITE, color_policy=ColorPolicy.BLACK, lineweight_scaling=1.5)
Frontend(ctx, backend, config=cfg).draw_layout(msp)
page = layout.Page(297, 420, layout.Units.mm, margins=layout.Margins.all(10))
(OUT / "patka_HEA240.svg").write_text(backend.get_string(page), encoding="utf-8")
print("hotovo:", dxf_path.name, "a SVG")
