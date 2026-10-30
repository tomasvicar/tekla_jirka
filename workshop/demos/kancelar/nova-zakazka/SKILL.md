---
name: nova-zakazka
description: Založí složku nové zakázky podle firemní šablony (01_Podklady … 99_Archiv) a zapíše ji do seznamu zakázek. Použij, když uživatel chce založit novou zakázku nebo projekt.
---

# Nová zakázka

1. Zeptej se na chybějící údaje: **číslo zakázky** (tvar `Z2026-015`), **název akce**, **klient**.
   Nic si nevymýšlej.
2. Podívej se do `podklady/seznam_zakazek.csv`, jestli číslo už neexistuje. Pokud ano, zastav se a zeptej se.
3. Ukaž, co vznikne (název složky a podsložky), a počkej na souhlas.
4. Spusť skript ze složky tohoto skillu:

   ```
   uv run python .claude/skills/nova-zakazka/nova_zakazka.py <číslo> "<název>" "<klient>" --koren vystupy/zakazky --seznam vystupy/seznam_zakazek.csv
   ```

   Originální `podklady/seznam_zakazek.csv` neměň. Doplněný seznam vede `vystupy/seznam_zakazek.csv`
   (při prvním použití ho zkopíruj z `podklady/`).
5. Skript nikdy nepřepíše existující složku. Když skončí chybou, chybu ukaž a nic neobcházej.
6. Na konci vypiš strom vytvořené složky a cestu k `README.txt`.

Konvence názvů souborů je v `README.txt` každé zakázky:
`<zakázka>_<TYP>_<číslo>[_<revize>].<přípona>`, např. `Z2026-014_VYK_V-102_C.pdf`.
