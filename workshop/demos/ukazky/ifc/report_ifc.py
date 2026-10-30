"""Přečte IFC model a vytvoří HTML report: množství podle typu a profilu, hmotnosti a kontrola dat.

Spuštění:  uv run --with ifcopenshell python report_ifc.py [soubor.ifc]
Ukázka pro workshop „Claude pro stavaře“.
"""
import html
import math
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

import numpy as np
import ifcopenshell
import ifcopenshell.geom
import ifcopenshell.util.element as uel
import ifcopenshell.util.placement as upl

SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent / "hala_lipnik.ifc"
OUT = SRC.with_name(SRC.stem + "_report.html")
RHO = 7850.0
CLASS_CZ = {"IfcColumn": "Sloupy", "IfcBeam": "Nosníky", "IfcMember": "Pruty / ztužidla", "IfcPlate": "Plechy"}
GENERIC = {"member", "beam", "column", "part", "plate", ""}

f = ifcopenshell.open(str(SRC))
proj = f.by_type("IfcProject")[0]


def profile_area(p):
    if p.is_a("IfcIShapeProfileDef"):
        h, b, tw, tf, r = p.OverallDepth, p.OverallWidth, p.WebThickness, p.FlangeThickness, p.FilletRadius or 0
        return 2 * b * tf + (h - 2 * tf) * tw + (4 - math.pi) * r * r
    if p.is_a("IfcCircleProfileDef"):
        return math.pi * p.Radius ** 2
    if p.is_a("IfcRectangleProfileDef"):
        return p.XDim * p.YDim
    return float("nan")


rows = []
for el in f.by_type("IfcElement"):
    solid = next((it for rep in el.Representation.Representations for it in rep.Items
                  if it.is_a("IfcExtrudedAreaSolid")), None) if el.Representation else None
    prof = solid.SweptArea if solid else None
    L = solid.Depth if solid else 0.0
    m = upl.get_local_placement(el.ObjectPlacement)
    start = m[:3, 3]
    end = start + m[:3, 2] * L
    mat = uel.get_material(el)
    ps = uel.get_pset(el, "Workshop_Common") or {}
    rows.append(dict(
        guid=el.GlobalId, cls=el.is_a(), name=el.Name or "", prof=(prof.ProfileName if prof else "?"),
        L=L, kg=profile_area(prof) * L * RHO if prof else 0.0, mat=(mat.Name if mat else None),
        phase=ps.get("Phase"), mark=ps.get("AssemblyMark"), Lprop=ps.get("Length_mm"), start=start, end=end,
    ))

# --- kontrolní pravidla (obdoba IDS / „sanity check“ před odesláním)
issues = []
by_name_mat = defaultdict(Counter)
for r in rows:
    by_name_mat[r["name"]][r["mat"]] += 1
for r in rows:
    probs = []
    if r["phase"] is None:
        probs.append("chybí fáze (Phase)")
    if r["mat"] is None:
        probs.append("chybí materiál")
    else:
        common = by_name_mat[r["name"]].most_common(1)[0][0]
        if r["mat"] != common:
            probs.append(f"ocel {r['mat']} – ostatní „{r['name']}“ mají {common}")
    if r["name"].strip().lower() in GENERIC:
        probs.append(f"obecný název „{r['name']}“")
    if r["Lprop"] is not None and abs(r["Lprop"] - r["L"] * 1000) > 1:
        probs.append("délka v Psetu nesouhlasí s geometrií")
    if probs:
        issues.append((r, probs))
marks = Counter(r["mark"] for r in rows)
dups = [m for m, n in marks.items() if m and n > 1]

# geometrie: lze každý prvek skutečně vytvořit?
settings = ifcopenshell.geom.settings()
geo_ok = 0
for el in f.by_type("IfcElement"):
    try:
        ifcopenshell.geom.create_shape(settings, el)
        geo_ok += 1
    except Exception:  # noqa: BLE001
        pass

# --- souhrny
by_cls = defaultdict(lambda: [0, 0.0, 0.0])
by_prof = defaultdict(lambda: [0, 0.0, 0.0])
by_phase = defaultdict(float)
for r in rows:
    for d, k in ((by_cls, r["cls"]), (by_prof, (r["prof"], r["mat"]))):
        d[k][0] += 1
        d[k][1] += r["L"]
        d[k][2] += r["kg"]
    by_phase[r["phase"] if r["phase"] is not None else "bez fáze"] += r["kg"]
total = sum(r["kg"] for r in rows)
bad_guids = {r["guid"] for r, _ in issues}

# --- izometrický náhled (SVG)
def iso(p):
    x, y, z = p
    return (x - y) * math.cos(math.radians(30)), -(x + y) * math.sin(math.radians(30)) - z


pts = [iso(r["start"]) for r in rows] + [iso(r["end"]) for r in rows]
xs, ys = [p[0] for p in pts], [p[1] for p in pts]
pad = 2.0
minx, maxx, miny, maxy = min(xs) - pad, max(xs) + pad, min(ys) - pad, max(ys) + pad
W = 760
sc = W / (maxx - minx)
Hh = (maxy - miny) * sc
COL = {1: "#2f5d8a", 2: "#1a7f6e", "bez fáze": "#c0392b"}
lines = []
for r in sorted(rows, key=lambda r: r["guid"] in bad_guids):
    (x1, y1), (x2, y2) = iso(r["start"]), iso(r["end"])
    bad = r["guid"] in bad_guids
    c = "#d62828" if bad else COL.get(r["phase"], "#888")
    w = 4.5 if bad else (2.6 if r["cls"] != "IfcMember" else 1.2)
    lines.append(f'<line x1="{(x1-minx)*sc:.1f}" y1="{(y1-miny)*sc:.1f}" x2="{(x2-minx)*sc:.1f}" y2="{(y2-miny)*sc:.1f}" '
                 f'stroke="{c}" stroke-width="{w}" stroke-linecap="round"><title>{html.escape(r["name"])} {r["mark"]} – {r["prof"]}'
                 f'{" – " + "; ".join(p for rr, p_ in issues if rr is r for p in p_) if bad else ""}</title></line>')
svg = f'<svg viewBox="0 0 {W} {Hh:.0f}" width="100%" role="img" aria-label="Izometrický náhled os prvků">{"".join(lines)}</svg>'


def fmt(v, d=0):
    return f"{v:,.{d}f}".replace(",", " ").replace(".", ",")


cls_rows = "".join(f"<tr><td>{CLASS_CZ.get(k, k)} <small>{k}</small></td><td>{v[0]}</td><td>{fmt(v[1],1)}</td><td>{fmt(v[2])}</td></tr>"
                   for k, v in sorted(by_cls.items(), key=lambda kv: -kv[1][2]))
prof_rows = "".join(f"<tr><td>{p}</td><td>{m or '–'}</td><td>{v[0]}</td><td>{fmt(v[1],1)}</td><td>{fmt(v[2])}</td></tr>"
                    for (p, m), v in sorted(by_prof.items(), key=lambda kv: -kv[1][2]))
phase_rows = "".join(f"<tr><td>{'Fáze ' + str(k) if k != 'bez fáze' else '<b class=bad>bez fáze</b>'}</td><td>{fmt(v)}</td><td>{fmt(v/total*100,1)} %</td></tr>"
                     for k, v in sorted(by_phase.items(), key=lambda kv: str(kv[0])))
issue_rows = "".join(f"<tr><td><code>{r['mark']}</code></td><td>{html.escape(r['name'])}</td><td>{r['prof']}</td><td>{'; '.join(p)}</td><td><code>{r['guid']}</code></td></tr>"
                     for r, p in issues)
dup_text = ", ".join(dups) if dups else "žádné"

page = f"""<!doctype html><html lang="cs"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Kontrola IFC – {html.escape(proj.Name)}</title>
<style>
body{{margin:0;font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;color:#17212b;background:#f3f6f8}}
.wrap{{max-width:1000px;margin:0 auto;padding:20px 16px 40px}}
h1{{color:#12355b;font-size:1.6rem;margin:.2rem 0}} h2{{color:#12355b;font-size:1.1rem;margin:1.6rem 0 .5rem;border-bottom:2px solid #12355b;padding-bottom:.2rem}}
.meta{{color:#5b6b78;font-size:.88rem}}
.kpi{{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:1rem 0}} .kpi div{{background:#fff;border:1px solid #d7e5ea;border-radius:10px;padding:10px 12px}}
.kpi small{{display:block;color:#5b6b78;font-size:.75rem}} .kpi b{{font-size:1.4rem;color:#12355b}} .kpi .bad b{{color:#c0392b}}
table{{border-collapse:collapse;width:100%;background:#fff;font-size:.86rem;font-variant-numeric:tabular-nums}}
th,td{{padding:5px 8px;border-bottom:1px solid #e6edf0;text-align:right}} th:first-child,td:first-child,td:nth-child(2):not(.n){{text-align:left}}
th{{background:#f4f8f9;color:#5b6b78;font-weight:600}} small{{color:#8a99a4}} .bad{{color:#c0392b}}
.issues td,.issues th{{text-align:left}} .issues code{{font-size:.75rem}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:16px}} .card{{background:#fff;border:1px solid #d7e5ea;border-radius:12px;padding:12px}}
.legend span{{margin-right:14px;font-size:.8rem}} .legend i{{display:inline-block;width:18px;height:4px;vertical-align:middle;margin-right:5px}}
.note{{background:#fff6ed;border-left:4px solid #b54708;padding:8px 12px;font-size:.85rem;margin:1rem 0}}
@media(max-width:760px){{.kpi,.grid{{grid-template-columns:1fr 1fr}}.grid{{grid-template-columns:1fr}}}}
</style></head><body><div class="wrap">
<h1>Kontrola IFC před odesláním</h1>
<p class="meta">Model: <b>{html.escape(proj.Name)}</b> · soubor <code>{SRC.name}</code> · schéma {f.schema} · report vytvořen {date.today():%d. %m. %Y} skriptem <code>report_ifc.py</code> (ifcopenshell {ifcopenshell.version})</p>
<div class="kpi"><div><small>Prvků</small><b>{len(rows)}</b></div><div><small>Hmotnost oceli</small><b>{fmt(total/1000,2)} t</b></div>
<div><small>Geometrie vytvořena</small><b>{geo_ok} / {len(rows)}</b></div><div class="{'bad' if issues else ''}"><small>Prvků s nálezem</small><b>{len(issues)}</b></div></div>
<h2>Náhled modelu</h2>
<div class="card">{svg}<div class="legend"><span><i style="background:#2f5d8a"></i>fáze 1</span><span><i style="background:#1a7f6e"></i>fáze 2</span><span><i style="background:#d62828;height:6px"></i>prvek s nálezem (najeďte myší)</span></div></div>
<h2>Nálezy kontroly ({len(issues)})</h2>
<table class="issues"><thead><tr><th>Značka</th><th>Název</th><th>Profil</th><th>Problém</th><th>GUID (pro vyhledání v Tekle)</th></tr></thead><tbody>{issue_rows or '<tr><td colspan=5>Bez nálezů.</td></tr>'}</tbody></table>
<p class="meta">Pravidla: každý prvek má fázi a materiál; materiál odpovídá ostatním prvkům stejného názvu; název není obecný; délka v Psetu odpovídá geometrii. Duplicitní značky sestav: {dup_text}.</p>
<h2>Množství</h2>
<div class="grid"><div><table><thead><tr><th>Typ prvku</th><th>ks</th><th>délka [m]</th><th>kg</th></tr></thead><tbody>{cls_rows}</tbody></table></div>
<div><table><thead><tr><th>Fáze</th><th>kg</th><th>podíl</th></tr></thead><tbody>{phase_rows}</tbody></table></div></div>
<h2>Podle profilu a materiálu</h2>
<table><thead><tr><th>Profil</th><th>Materiál</th><th>ks</th><th>délka [m]</th><th>kg</th></tr></thead><tbody>{prof_rows}</tbody>
<tfoot><tr><th>Celkem</th><th></th><th>{len(rows)}</th><th>{fmt(sum(r['L'] for r in rows),1)}</th><th>{fmt(total)}</th></tr></tfoot></table>
<div class="note">Hmotnost je spočtena z plochy profilu × délka extruze × 7 850 kg/m³, bez zkrácení na přípojích, bez svarů, šroubů a plechů.
Před odesláním porovnejte s reportem z Tekly – rozdíl v jednotkách procent je normální, větší rozdíl je důvod hledat chybu.
Model je syntetický a chyby jsou do něj vloženy záměrně.</div>
</div></body></html>"""
OUT.write_text(page, encoding="utf-8")
print(f"{OUT.name}: {len(rows)} prvků, {total/1000:.2f} t, {len(issues)} nálezů, geometrie {geo_ok}/{len(rows)}")
