"""Syntetická ukázka „výkresy vytištěné z Tekly do jedné složky“ pro ukázku PDF export.

Zakázka Z2026-021 Hala sklad Lipník (stejná jako ve cvičení Data z Tekly).
Obsah ZIPu data/pdf_export.zip:
    tisk_z_tekly/          PDF výkresy pojmenované jako při tisku z Tekly („A3 - PRICLE - A.pdf“ =
                           značka bez tečky - název výkresu - revize; bez revize „A3 - PRICLE.pdf“),
                           některé ve více revizích, jeden duplikát a dva soubory smetí
    seznam_vykresu.csv     seznam výkresů jako export ze seznamu výkresů (Document manager)
    README.txt             popis

Úmyslné „chyby“ k nalezení: výkres A.12 má v seznamu revizi A, ale vytištěný je jen bez revize;
výkres A.10 je v Tekle neaktuální; „A5 - ZTUZIDLO (1).pdf“ je kopie; Thumbs.db a plot_log.txt jsou smetí.
Výchozí název ověřen v Tekle 2026 SP1 („A2 - BEAM.pdf“); přípona s revizí je přibližná.
Vše vymyšlené, deterministické (semínko 2026, pevná data v PDF).

Spuštění (z kořene workshopu):
    uv run --with reportlab python tools/make_pdf_export_data.py
"""
from __future__ import annotations

import csv
import io
import random
import shutil
import unicodedata
import zipfile
from pathlib import Path

from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "pdf_export"
ZIP = ROOT / "data" / "pdf_export.zip"
DATE = (2026, 1, 1, 0, 0, 0)
ORDER, PROJECT = "Z2026-021", "Hala sklad Lipník"

# Písmo s češtinou; když není, píše se bez diakritiky.
FONT = "Helvetica"
for p in ["/usr/share/fonts/liberation-sans-fonts/LiberationSans-Regular.ttf",
          "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
          "/usr/share/fonts/dejavu-sans-fonts/DejaVuSans.ttf"]:
    if Path(p).exists():
        pdfmetrics.registerFont(TTFont("CZ", p))
        FONT = "CZ"
        break


def txt(s: str) -> str:
    if FONT != "Helvetica":
        return s
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()


# (typ, značka, název výkresu, fáze, revize [(značka revize, datum)], stav v Tekle)
# Jako v seznamu výkresů Tekly: typ A = sestava, W = dílec (single part, značka P.x),
# G = výkres rozmístění. Název výkresu = název sestavy/dílu, proto se opakuje.
# Revize: "" = výkres ještě bez revize, pak A, B...
DRAWINGS = [
    ("G", "G.1", "KOTEVNI PLAN", 1, [("", "2026-09-01"), ("A", "2026-09-15"), ("B", "2026-10-12")], "Aktuální"),
    ("G", "G.2", "PUDORYS SLOUPU", 1, [("", "2026-09-01"), ("A", "2026-10-12")], "Aktuální"),
    ("G", "G.3", "STRECHA", 2, [("", "2026-09-03")], "Aktuální"),
    ("G", "G.4", "REZY A POHLEDY", 2, [("", "2026-09-03")], "Aktuální"),
    ("A", "A.1", "SLOUP", 1, [("", "2026-09-05")], "Aktuální"),
    ("A", "A.2", "SLOUP", 1, [("", "2026-09-05")], "Aktuální"),
    ("A", "A.3", "PRICLE", 1, [("", "2026-09-05"), ("A", "2026-10-12")], "Aktuální"),
    ("A", "A.4", "VAZNICE", 2, [("", "2026-09-08")], "Aktuální"),
    ("A", "A.5", "ZTUZIDLO", 2, [("", "2026-09-08")], "Aktuální"),
    ("A", "A.6", "ZTUZIDLO", 2, [("", "2026-09-08")], "Aktuální"),
    ("A", "A.7", "VAZNICE", 2, [("", "2026-09-08"), ("A", "2026-10-14")], "Aktuální"),
    ("A", "A.8", "PAZDIK", 3, [("", "2026-09-10")], "Aktuální"),
    ("A", "A.9", "RAM VRAT", 3, [("", "2026-09-10")], "Aktuální"),
    ("A", "A.10", "SLOUPEK", 3, [("", "2026-09-10")], "Neaktuální"),
    ("A", "A.11", "VYMENA", 3, [("", "2026-09-10")], "Aktuální"),
    ("A", "A.12", "SLOUPEK", 3, [("", "2026-09-10"), ("A", "2026-10-20")], "Aktuální"),
    ("W", "P.1", "PATNI PLECH", 1, [("", "2026-09-05")], "Aktuální"),
    ("W", "P.2", "CELNI DESKA", 1, [("", "2026-09-05"), ("A", "2026-10-12")], "Aktuální"),
    ("W", "P.3", "VYZTUHA", 1, [("", "2026-09-05")], "Aktuální"),
    ("W", "P.4", "STYCNIKOVY PLECH", 2, [("", "2026-09-08")], "Aktuální"),
    ("W", "P.5", "ZEBRO", 2, [("", "2026-09-08")], "Aktuální"),
    ("W", "P.6", "KOTEVNI PLECH", 3, [("", "2026-09-10")], "Aktuální"),
]
# Výkres, jehož poslední revize se nevytiskla (v seznamu je, PDF chybí).
NOT_PRINTED = {("A.12", "A")}


def pdf_name(mark: str, name: str, rev: str) -> str:
    """Výchozí název při tisku z Tekly: značka bez tečky + " - " + název výkresu.
    S volbou „Include revision mark to file name“ přibude " - <revize>" (přibližně)."""
    base = f"{mark.replace('.', '')} - {name}"
    return f"{base} - {rev}.pdf" if rev else f"{base}.pdf"


TYPE_NAME = {"A": "VÝKRES SESTAVY", "W": "VÝKRES DÍLCE", "G": "VÝKRES ROZMÍSTĚNÍ"}


def make_pdf(rng: random.Random, typ, mark, name, phase, rev, date) -> bytes:
    buf = io.BytesIO()
    w, h = landscape(A4)
    c = canvas.Canvas(buf, pagesize=(w, h), invariant=1)
    c.setTitle(f"{mark} {name} rev {rev}")
    c.setAuthor("Tekla Structures (syntetická ukázka)")
    c.setLineWidth(1.2)
    c.rect(20, 20, w - 40, h - 40)
    # Jednoduchý „výkres“: obdélníky jako pohled na prvek.
    c.setLineWidth(0.8)
    x0, y0 = 70, 260
    if typ == "G":
        for i in range(rng.randint(5, 9)):
            c.line(x0 + i * 70, y0 - 150, x0 + i * 70, y0 + 230)
        for j in range(4):
            c.line(x0 - 20, y0 - 150 + j * 125, x0 + 600, y0 - 150 + j * 125)
    else:
        L = rng.randint(380, 620)
        H = rng.randint(30, 90) if typ == "A" else rng.randint(120, 220)
        c.rect(x0, y0, L, H)
        for k in range(rng.randint(2, 6)):
            c.circle(x0 + 20 + k * 30, y0 + H / 2, 6)
        c.line(x0, y0 - 30, x0 + L, y0 - 30)
        c.setFont(FONT, 9)
        c.drawCentredString(x0 + L / 2, y0 - 42, str(L * 10))
    # Razítko vpravo dole.
    bx, by, bw, bh = w - 300, 20, 280, 120
    c.setLineWidth(1)
    c.rect(bx, by, bw, bh)
    for yy in (by + 30, by + 60, by + 90):
        c.line(bx, yy, bx + bw, yy)
    c.setFont(FONT, 8)
    c.drawString(bx + 6, by + bh - 12, txt(f"Zakázka: {ORDER} {PROJECT}"))
    c.drawString(bx + 6, by + 72, txt(f"{TYPE_NAME[typ]}   Fáze: {phase}"))
    c.drawString(bx + 6, by + 42, txt(f"Název: {name}"))
    c.drawString(bx + 6, by + 12, txt(f"Revize: {rev}    Datum: {date}"))
    c.setFont(FONT, 18)
    c.drawRightString(bx + bw - 8, by + 70, mark)
    c.setFont(FONT, 7)
    c.drawString(28, 26, txt("Syntetický výkres pro workshop – není skutečný projekt."))
    c.showPage()
    c.save()
    return buf.getvalue()


def main() -> None:
    rng = random.Random(2026)
    if OUT.exists():
        shutil.rmtree(OUT)
    tisk = OUT / "tisk_z_tekly"
    tisk.mkdir(parents=True)

    files: dict[str, bytes] = {}
    for typ, mark, name, phase, revs, _ in DRAWINGS:
        for rev, date in revs:
            if (mark, rev) in NOT_PRINTED:
                continue
            files[pdf_name(mark, name, rev)] = make_pdf(rng, typ, mark, name, phase, rev or "-", date)
    # Duplikát (kopie stejného souboru) a smetí.
    files["A5 - ZTUZIDLO (1).pdf"] = files["A5 - ZTUZIDLO.pdf"]
    files["Thumbs.db"] = bytes(rng.randrange(256) for _ in range(512))
    files["plot_log.txt"] = ("Plot started 2026-10-21 14:02\r\n"
                             + "".join(f"Printed {n}\r\n" for n in sorted(files) if n.endswith(".pdf"))
                             ).encode()
    for n, data in files.items():
        (tisk / n).write_bytes(data)

    # Seznam výkresů: jen aktuální (poslední) revize, jako v seznamu výkresů Tekly.
    with open(OUT / "seznam_vykresu.csv", "w", encoding="utf-8-sig", newline="") as f:
        wr = csv.writer(f, delimiter=";", lineterminator="\r\n")
        wr.writerow(["Typ", "Znacka", "Nazev", "Revize", "Datum_revize", "Faze", "Stav"])
        for typ, mark, name, phase, revs, stav in DRAWINGS:
            rev, date = revs[-1]
            wr.writerow([typ, mark, name, rev, date, phase, stav])

    (OUT / "README.txt").write_text(
        "Ukázková zakázka Z2026-021 Hala sklad Lipník (vymyšlená).\r\n\r\n"
        "tisk_z_tekly/        PDF výkresy tak, jak je Tekla vytiskla do jedné složky.\r\n"
        "                     Název souboru: <značka bez tečky> - <název výkresu>[ - <revize>].pdf,\r\n"
        "                     např. A3 - PRICLE - A.pdf (výkres A.3, revize A).\r\n"
        "                     Značka: A = sestava, P = dílec, G = výkres rozmístění.\r\n"
        "seznam_vykresu.csv   seznam výkresů ze seznamu výkresů Tekly (Document manager).\r\n"
        "                     Oddělovač středník. Typ: A = sestava, W = dílec, G = rozmístění.\r\n"
        "                     Revize = aktuální revize výkresu (prázdná = bez revize).\r\n"
        "                     Stav = Aktuální / Neaktuální (model se od tisku změnil).\r\n",
        encoding="utf-8")

    with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(OUT.rglob("*")):
            if p.is_file():
                info = zipfile.ZipInfo(p.relative_to(OUT).as_posix(), DATE)
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o644 << 16
                z.writestr(info, p.read_bytes())
    n_pdf = sum(1 for n in files if n.endswith(".pdf"))
    print(f"{ZIP.relative_to(ROOT)}: {n_pdf} PDF + {len(files) - n_pdf} smetí, "
          f"{len(DRAWINGS)} výkresů v seznamu, {ZIP.stat().st_size // 1024} kB")


if __name__ == "__main__":
    main()
