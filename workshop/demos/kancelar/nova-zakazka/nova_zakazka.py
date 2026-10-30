"""Založí složku nové zakázky podle firemní šablony. Nic existujícího nepřepisuje.

Použití (Claude ho spouští sám):
    uv run python nova_zakazka.py Z2026-015 "Sklad Kuřim" "Investor a.s." --koren Zakazky --seznam podklady/seznam_zakazek.csv

- číslo musí mít tvar Z + rok + pomlčka + tři číslice (Z2026-015),
- složka se jmenuje <číslo>_<název bez diakritiky a mezer>,
- když složka už existuje, skript skončí s chybou (nic nepřepíše),
- s --seznam připíše řádek do seznamu zakázek (CSV se středníky), pokud tam číslo ještě není.
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path

SLOZKY = [
    "01_Podklady",            # od architekta, investora, zaměření (DWG, IFC, PDF)
    "02_Vypocty",             # statické výpočty, výpočetní tabulky
    "03_Model",               # IFC exporty z Tekly (model samotný zůstává v TeklaStructuresModels)
    "04_Vykresy",             # jen PLATNÉ revize výkresů
    "05_Korespondence",       # e-maily, zápisy z KD, poznámky z telefonu
    "06_Nabidky_a_fakturace", # nabídky, smlouvy, faktury
    "07_Fotodokumentace",
    "99_Archiv/stare_revize", # nahrazené revize a verze
    "99_Archiv/duplicity",    # stejné soubory pod jiným jménem
]

KONVENCE = """Konvence názvů souborů:
  <zakázka>_<TYP>_<číslo>[_<revize>].<přípona>
  TYP: VYK výkres, VYP výpočet, MOD model/IFC, POD podklad, KOR korespondence,
       ZAP zápis, POZ poznámka, NAB nabídka, SML smlouva, FAK faktura, FOT fotka
  příklad: Z2026-014_VYK_V-102_C.pdf, Z2026-014_FAK_FA-2026-0042.pdf
  bez diakritiky a mezer; revize výkresů písmenem (A, B, C), verze výpočtů v1, v2…
"""


def bez_diakritiky(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^A-Za-z0-9-]+", "_", text).strip("_")


def zaloz(cislo: str, nazev: str, klient: str = "", koren: Path = Path("."), seznam: Path | None = None,
          dnes: date | None = None) -> Path:
    if not re.fullmatch(r"Z\d{4}-\d{3}", cislo):
        raise ValueError(f"Číslo zakázky '{cislo}' nemá tvar Z2026-015.")
    cil = Path(koren) / f"{cislo}_{bez_diakritiky(nazev)}"
    if cil.exists():
        raise FileExistsError(f"Složka {cil} už existuje – nic jsem nepřepsal.")
    for s in SLOZKY:
        (cil / s).mkdir(parents=True)
    dnes = dnes or date.today()
    (cil / "README.txt").write_text(
        f"Zakázka: {cislo}\nNázev: {nazev}\nKlient: {klient}\nZaloženo: {dnes:%d. %m. %Y}\n\n"
        "Složky:\n" + "".join(f"  {s}\n" for s in SLOZKY) + "\n" + KONVENCE, encoding="utf-8")
    if seznam:
        seznam = Path(seznam)
        radky = list(csv.reader(seznam.open(encoding="utf-8-sig"), delimiter=";")) if seznam.exists() else []
        if not any(r and r[0] == cislo for r in radky):
            hlavicka = radky[0] if radky else ["cislo_zakazky", "nazev", "slozka", "klient", "stav"]
            hodnoty = dict(cislo_zakazky=cislo, nazev=nazev, slozka=cil.name, klient=klient, stav="nová")
            with seznam.open("a", newline="", encoding="utf-8") as f:
                w = csv.writer(f, delimiter=";")
                if not radky:
                    w.writerow(hlavicka)
                w.writerow([hodnoty.get(sloupec, "") for sloupec in hlavicka])
    return cil


def main() -> None:
    p = argparse.ArgumentParser(description="Založí složku nové zakázky.")
    p.add_argument("cislo")
    p.add_argument("nazev")
    p.add_argument("klient", nargs="?", default="")
    p.add_argument("--koren", default=".", help="kam složku založit (výchozí: aktuální složka)")
    p.add_argument("--seznam", help="CSV seznam zakázek, kam se připíše nový řádek")
    a = p.parse_args()
    try:
        cil = zaloz(a.cislo, a.nazev, a.klient, Path(a.koren), Path(a.seznam) if a.seznam else None)
    except (ValueError, FileExistsError) as e:
        sys.exit(f"CHYBA: {e}")
    print(f"Založeno: {cil.resolve()}")


if __name__ == "__main__":
    main()
