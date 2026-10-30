# 00 – Souhrn: Claude Code + Tekla Structures pro neprogramátora

*Stav k 30. 10. 2026. Syntéza zpráv 01–12 v této složce; zdroje a podrobnosti jsou v jednotlivých zprávách.*

## Výsledek testu (30. 10. 2026)

Vše podstatné **vyzkoušeno na Tekle 2026 SP1** (trial, Windows VM na `ada`, Claude Desktop, záložka Code) –
podrobně [13 – test](13-test-tekla-trial.md):

- Agent sám připraví projekt: najde verzi Tekly, cesty, složku maker a XML dokumentaci API (je v instalaci).
- Makra napsaná agentem fungují: hala 51 dílů, výpis do CSV, změna třídy (jedno **Ctrl+Z** vrátí vše),
  **export všech výkresů do PDF do vlastní složkové struktury** (i v trialu přes API).
- MCP server tempalg1n v0.9.0 funguje s Teklou 2026: dotazy na model, zápis s náhledem + Ctrl+Z.
- Úskalí: Manual režim se ptá na vše → doporučujeme Auto; chyba kompilace makra je jen v okně
  (→ výřez obrazovky do chatu); Tekla si pamatuje přeložená makra (→ upravené nasazovat jako `_v2`).
- Web s workshopem: <https://tomasvicar.github.io/tekla_jirka/>

## TL;DR

- **Jde to, ale ne „úplně všechno“.** Tekla Open API pokryje většinu práce s modelem (díly, šrouby, svary, komponenty, UDA, výběr, reporty, IFC/NC export, kolize). Výkresy jen částečně, číslování přes makro, některé dialogy vůbec. → [02](02-open-api-moznosti.md)
- **Oficiální MCP od Trimble pro Teklu neexistuje.** Je ~18 komunitních MCP serverů; reálně použitelné jsou 2–3. → [01](01-mcp-servery.md)
- **Trimble má vlastní AI v Tekle** (Tekla Model Assistant – preview, Developer Assistant), ale jen pro dražší licence (Diamond/Graphite/Carbon). → [06](06-trimble-ai-a-aec-mcp.md)
- **Nejlepší start pro neprogramátora není MCP, ale práce se soubory** (exporty reportů → Excel) a pak **C# makra**, která Claude napíše do složky maker. → [05](05-automatizace-bez-mcp.md), [11](11-napady-na-automatizace.md)
- **Právní stránka:** EU spotřebitelské podmínky Pro/Max obsahují v článku o odpovědnosti „non-commercial use only“ – spíš omezení ručení než jasný zákaz; Pro se v práci běžně používá, ale nemá DPA (GDPR). Pro firmu o 2 lidech je řešením **Team se 2 místy Standard** (min. 2 místa, ~25 USD/místo/měs., Claude Code v ceně, firemní podmínky, netrénuje se na datech). Hlídat NDA. → [09](09-bezpecnost-data-zalohy.md)

## Tři cesty, jak Claude s Teklou propojit

| Cesta | Co to je | Pro | Proti | Kdy |
|---|---|---|---|---|
| **A. Soubory** | Export reportu/IFC/PDF/NC z Tekly, Claude napíše Python skript → Excel/PDF | Nulové riziko pro model, Claude vidí chyby sám | Nečte živý model | **Hned od začátku** |
| **B. C# makra** | Claude zapíše `.cs` do `macros\modeling`, kamarád spustí z *Applications & components* | Bez Visual Studia, plná síla Open API | Chyby kompilace musí kamarád kopírovat zpět | **Druhý krok** |
| **C. MCP server** | Claude „mluví“ s otevřenou Teklou přímo z chatu | Nejpohodlnější, chat nad živým modelem | Komunitní software, změny jdou přímo do modelu, `/rewind` je nevrátí | **Po otestování, read-only** |

Další okrajové cesty (samostatné C# aplikace přes `dotnet build`, Python/pythonnet, Grasshopper Live Link, ovládání obrazovky) – viz [05](05-automatizace-bez-mcp.md).

## Doporučené MCP servery (z [01](01-mcp-servery.md))

1. **[tempalg1n/tekla-mcp-server](https://github.com/tempalg1n/tekla-mcp-server)** – C#, MIT, ~120 nástrojů, zápisy jen přes náhled+potvrzení, read-only režim, instalace = zip + `.exe`, má **mock režim** (běží bez Tekly). **Favorit.**
2. **[teknovizier/tekla_mcp_server](https://github.com/teknovizier/tekla_mcp_server)** – Python, GPL-3, nejpopulárnější, ~62 nástrojů vč. PDF/DWG exportu výkresů; složitější instalace.
3. **tekla-api-mcp** (npm) – neovládá model, ale dává Claudovi **dokumentaci Tekla API** → méně vymyšlených metod.

## Instalace u kamaráda (z [04](04-instalace-claude-windows.md))

1. Tarif: **Claude Pro** na zkoušku (Free nemá Claude Code); pro ostrou práci **Team se 2 místy Standard** (2 lidi ve firmě = minimum Teamu) ([09](09-bezpecnost-data-zalohy.md)). V nastavení vypnout *Model improvement*.
2. **Claude Desktop** z claude.com/download (ne Microsoft Store) → záložka **Code** (žádný terminál, Node ani WSL).
3. **Git for Windows** (doporučeno – Claude pak umí vracet změny souborů).
4. MCP: `%APPDATA%\Claude\claude_desktop_config.json` (Settings → Developer → Edit Config), absolutní cesty se zdvojenými `\\`, po změně Claude úplně ukončit a spustit. Logy: `%APPDATA%\Claude\logs\mcp*.log`.
5. Projektová složka s `CLAUDE.md` (viz níže), zpočátku režim **Manual**/Plan, zápisové MCP nástroje na `ask`, `bypassPermissions` zakázat.

## Kostra projektu a CLAUDE.md (z [05](05-automatizace-bez-mcp.md), [08](08-api-znalosti-pro-claude.md))

```
tekla-projekty/
  CLAUDE.md
  .claude/skills/  tekla-api/ tekla-macro/ tekla-app/
  macros/modeling/  macros/drawings/
  python/  reports/templates/  samples/ (anonymizované exporty)
  reference/  (XML dokumentace z NuGet + TSOpenAPIExamples pro danou verzi)
```

CLAUDE.md má obsahovat: verzi Tekly (+SP) a prostředí (CZ env), cesty (model, makra, logy), **„uživatel neprogramuje – vysvětluj česky a krok za krokem“**, **„nepoužívej API metodu, kterou jsi neověřil v reference/*.xml nebo v příkladech pro tuto verzi“**, „model měň jen v testovací kopii a jen po potvrzení“, kostru makra (`GetConnectionStatus()`, `CommitChanges()` jednou na operaci), vlastní názvy profilů/materiálů/UDA z CZ prostředí ([12](12-cz-sk-zdroje.md)).

Hotové Tekla-specifické CLAUDE.md/skills veřejně **neexistují** – vytvoříme je.

## Bezpečnost – minimum ([09](09-bezpecnost-data-zalohy.md))

- Před každou AI session: *File → Save as → **Save and create backup copy*** (zachová GUID; obyčejné Save as není záloha).
- Pracovat na kopii, nikdy na multi-user master modelu.
- Každý `CommitChanges()` = jeden Undo krok v Tekle; MCP změny `/rewind` nevrátí.
- Na Windows nefunguje sandbox → ochrana = oprávnění + kontrola člověkem.
- Text v cizích modelech/IFC je nedůvěryhodný vstup (prompt injection).
- Nástroje pro vlastní potřebu OK; předávat/prodávat klientům jen přes Tekla Partners Program.
- Výsledky musí ověřit kvalifikovaná osoba (EULA 9.2; a AI nezná ČSN/EN – [12](12-cz-sk-zdroje.md)).

## Nápady na první automatizace ([11](11-napady-na-automatizace.md), [03](03-priklady-pouziti.md))

Bez rizika (jen soubory):
1. Porovnání dvou revizí kusovníku → Excel (přibylo/ubylo/změněno) – Tekla to sama neumí.
2. Report → přehled hmotností podle fází/profilů → cenová nabídka.
3. Hromadné přejmenování/slučování PDF výkresů + transmittal.
4. Kontrola reportu: prázdné UDA, chybějící materiál, „?“ v číslování.
5. Kontrola NC/DSTV složky proti kusovníku.

S živým modelem (až potom, na kopii):
6. Read-only makro: vypiš vybrané díly a jejich atributy.
7. Hromadná změna class/prefixu/UDA na vybraných dílech s náhledem.
8. Excel → osnovy/pruty.

Nejdřív projít **Tekla Warehouse** – hodně věcí už existuje (SetnGet UDA, Excel to drawing, hromadný tisk PDF…).

## Plán výuky ([10](10-vyuka-neprogramatora.md))

První sezení ~2,5 h: proč → instalace → bezpečnost → cvičení 1–2 (soubory) → CLAUDE.md a git → cvičení 3 (skill) → ukázka plan mode na makrech (cvičení 4–5).
Principy: Claude jako parťák, konkrétní zadání + jak ověřit výsledek, plan mode u větších úkolů, po 2 neúspěšných opravách `/clear` a lepší zadání, git jako „undo“. Kurz zdarma: ccforeveryone.com; Anthropic Academy.

## Testovací prostředí u nás ([07](07-trial-a-testovaci-prostredi.md))

1. **Hned na Fedoře:** mock build `tempalg1n/tekla-mcp-server` → ověřit Claude ↔ MCP bez Windows.
2. Windows 11 Enterprise evaluation (90 dní) ve virt-manager/KVM (Q35, OVMF Secure Boot, swtpm, virtio-win), 6–8 vCPU, 16 GB RAM, ~150 GB. Snapshot.
3. Tekla 2026 trial (30 dní, Open API funguje, neprodlužitelný, vázaný na počítač) – snapshot **před** aktivací, aktivovat až na finální VM. Bez GPU zkusit *legacy rendering* (OpenGL).
4. Claude Desktop → MCP read-only (`TEKLA_MCP_READ_ONLY=1`) → náhled zápisu → jedna reálná změna na kopii.
5. Test C# makra napsaného Claude Code.
6. Zapisovat každý ruční krok pro instalaci u kamaráda.

Riziko: použitelnost Tekly ve VM bez GPU je neověřená → záloha: krátký read-only test přímo u kamaráda na kopii modelu.
Alternativa licence: demo licence přes Construsoft CZ ([12](12-cz-sk-zdroje.md)).

## Otevřené otázky ke kamarádovi

- Jakou má verzi Tekly a jakou licenci (Diamond/Graphite/Carbon)? → rozhoduje, jestli má i Tekla Model Assistant / Developer Assistant.
- Pracuje sám, nebo ve firmě (Model Sharing, IT pravidla)? Jaké NDA mají klienti?
- Které úkoly ho nejvíc otravují (zeptat se konkrétně – [11](11-napady-na-automatizace.md) bod 1–2 doporučených postupů)?

## Místní zdroje ([12](12-cz-sk-zdroje.md))

- **Construsoft CZ** (Přerov) – distributor, školení; webinář **19. 11. 2026 „Výkresy na pár kliknutí? Automatizace a AI v Tekla Structures“**, záznam z 25. 6. 2026 o AI v modelování.
- Kurz Open API česky nenalezen (polský Construsoft ho má).
