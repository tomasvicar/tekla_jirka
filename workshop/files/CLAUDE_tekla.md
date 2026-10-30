# Pravidla pro Clauda – makra pro Tekla Structures

Patří do hlavní složky projektu jako `CLAUDE.md`. Hodnoty v `< >` doplní agent.

## Kdo jsem

- Konstruktér / detailer v Tekle. **Neprogramuji.** Odpovídej česky, stručně, bez žargonu.
- Po každé změně napiš: co jsi vytvořil (cesta), jak to v Tekle spustím a co ti poslat, když to selže.
- Normy a statiku nikdy neuváděj jako ověřený fakt.

## Prostředí

- Tekla Structures **<verze, SP>**, prostředí **<Czech / Default>**.
- Testovací model (KOPIE): `<C:\TeklaStructuresModels\Projekt_KOPIE>`
- Makra modelu: `<model>\macros\modeling\`
- Sdílená makra (XS_MACRO_DIRECTORY): `<cesta>`
- Logy Tekly: `<cesta, NEOVĚŘENO>`
- Projekt: `makra/` (hlavní kopie .cs), `knihovna/` (ověřená makra), `reference/` (XML dokumentace API
  z instalace Tekly, např. `Tekla.Structures.Model.xml`; když chybí, napiš sem „reference/ prázdná“).

## Tvrdá pravidla

1. **Nevymýšlej API.** Každý člen Tekla Open API ověř v `reference/*.xml`. Když `reference/`
   je prázdná, ověř ho na developer.tekla.com v dokumentaci **pro moji verzi Tekly** (nebo
   v příkladech TSOpenAPIExamples). Neověřené označ `// NEOVĚŘENO:`.
2. **Model měním jen na kopii a s potvrzením.** Makro, které mění model: kontrola, že **název
   složky modelu** obsahuje „KOPIE“ (velikost písmen nevadí), dialog „Změním N dílů…
   Pokračovat?“, při chybě u části dílů seznam a dotaz, na konci **jedno**
   `model.CommitChanges("popis")`.
3. **Nejdřív jen čtení.** Nové makro nejprve jen vypíše, co by změnilo.
4. Modelových souborů (`.db1`, `.db2`) se nedotýkej. Makra jen kopíruj do složky maker, spouštím je já.
5. Ve `knihovna/` nic nemaž ani nepřepisuj bez souhlasu.
6. **Před nasazením makro přelož** (zkontroluj) proti DLL Tekly z instalace
   (`<C:\Program Files\Tekla Structures\<verze>\bin>`). Nasazuj jen makro, které se přeložilo.
   Když složka `macros\modeling` v modelu chybí, zeptej se a založ ji.
7. **Chyby za běhu** si makro zapisuje do `<model>\vystupy\makro_chyby.txt`
   (`try/catch` + `File.AppendAllText`). Když řeknu, že makro selhalo, **přečti nejdřív tento
   soubor**. Chyba překladu (okno *CompileError*) se nikam nezapíše – pak mě požádej
   o **výřez obrazovky: Win+Shift+S a Ctrl+V do chatu**. Text mě ručně kopírovat nenech.
8. **Model se sám neuloží.** Po změně mi připomeň: zkontrolovat, pak **Ctrl+S** (uložit),
   nebo **Ctrl+Z** (vrátit celou změnu).

## Nastavení dělá agent

- Cesty zjisti sám čtením disku a zapiš sem. Co nenajdeš, označ „NEOVĚŘENO“ a zeptej se.
- Konfiguraci (`claude_desktop_config.json`, `.claude/settings.json`) měň takto: záloha,
  ukázat změnu, počkat na souhlas, ověřit JSON, říct mi, co restartovat.
- Já sám: záloha a kopie modelu, schvalování, restart Claude Desktop, spuštění makra.
- Jak makro spustím (piš mi to takto): **Applications & components** (panel vpravo) → **≡** →
  **Catalog management** → **Reload catalog**, vyhledat název makra, **dvojklik**.
- MCP server pro Teklu (pokud je) používej **jen pro čtení**. Změny modelu dělej makrem.

## Moje zvyklosti

- Profily: `HEA200`, `IPE300`, `L80*8`, `PL10*200` – přesný zápis ověř v mém katalogu.
- Materiály: `S235JR`, `S355J2`, `C30/37`.
- UDA: `<USER_FIELD_1 = stav kontroly>`. Třídy: `<1 = sloupy, 2 = nosníky, …>`.
- Výstupy: CSV do `<model>\vystupy\`, středník, UTF-8 s BOM, desetinná čárka.
