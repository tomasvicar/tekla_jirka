---
name: souhrn-z-reportu
description: Zpracuje exportovaný report z Tekla Structures (seznam dílů / sestav v CSV nebo XLSX) – kontrola chyb, souhrn hmotností podle fáze, profilu a materiálu, grafy, Excel a HTML souhrn; volitelně porovnání dvou revizí a návrh cenové nabídky podle ceníku. Použij, když uživatel přinese nový report z Tekly nebo napíše „udělej souhrn z reportu“.
---

# Souhrn z reportu Tekla

Uživatel je konstruktér, neprogramuje. Mluv česky a stručně. Pravidla složek jsou v `CLAUDE.md`
(originály v `podklady/` jen čti, výsledky do `vystupy/`).

## Postup

1. **Najdi vstupy** v `podklady/`: seznam dílů (`*part_list*`), seznam sestav (`*assembly_list*`),
   případně starší revizi a `cenik.xlsx`. Když si nejsi jistý, který soubor je který, zeptej se.
2. **Načti report správně:** nad tabulkou je hlavička reportu, pod ní řádek `CELKEM` (nezapočítávat).
   Oddělovač `;`, desetinná čárka, UTF-8. `WEIGHT` a `AREA` jsou **na 1 kus** → vždy násobit `QTY`.
3. **Spusť skript** `vystupy/skripty/souhrn_z_reportu.py` (vytvořený v cvičení). Použití:
   `uv run --with pandas --with openpyxl --with matplotlib python vystupy/skripty/souhrn_z_reportu.py <part_list> [<starsi_part_list>] [--cenik podklady/cenik.xlsx]`
   Když skript chybí nebo na novém reportu spadne, oprav ho a vysvětli, co bylo jinak.
4. **Kontrola dat** (vždy, i když o ni uživatel nežádá): chybějící materiál, „?“ v pozicích,
   prázdné UDA, stejná značka s různou délkou/profilem, profil mimo katalogový tvar, nulová hmotnost,
   nesoulad součtu dílů a sestav. Nic neopravuj sám – vypiš a zeptej se.
5. **Výstupy** do `vystupy/<datum>_<nazev_reportu>/`: `souhrn.xlsx` (listy Přehled, Podle fáze,
   Podle profilu, Podle materiálu, Problémy), `hmotnosti.png`, `souhrn.html` (obrázky vložené).
6. **Ověření:** porovnej svou celkovou hmotnost s řádkem `CELKEM` v reportu a napiš obě čísla.
   Na konci vypiš cesty k souborům a 3–5 hlavních zjištění.

## Nedělej

- Neměň originální reporty ani model Tekly.
- Nevydávej cenu za závaznou – je to návrh k ruční kontrole; uveď předpoklady (např. jak jsi
  nacenil díl bez materiálu).
- Neuváděj nic o statice a normách jako ověřené.
