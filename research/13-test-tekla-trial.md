# 13 – Test: Tekla trial + Claude ve Windows VM na `ada`

Průběžný zápis testu (začato 30. 10. 2026). Cíl: ověřit na reálné Tekle postupy z webu
(instalace, „řekni agentovi“, makra, MCP) a zkusit něco vymodelovat.

## Prostředí

- Hostitel **`ada`** (Bluefin, 62 GB RAM, 28 vláken, RTX 4070 Ti SUPER), univerzální Windows VM
  podle `reprodukovatelny-linux/21-windows-vm-na-ada.md` (flatpak GNOME Boxes, SPICE/QXL, Tailscale SSH `ssh windows`).
- **Záloha před úpravami:** `~/VMs/backup-2026-10-30/` (qcow2 + VARS + XML, SHA256 ověřeno).
- Úpravy VM 30. 10.: RAM 8 → **24 GB**, vCPU 6 → **10**, disk 64 → **200 GB**
  (`qemu-img resize`; obnovovací oddíl za C: smazán, WinRE přesunuto na C: přes `reagentc`, C: roztaženo na 199 GB).
- Grafika VM: **QXL bez GPU** → Tekla poběží na softwarovém vykreslování (sledovat použitelnost; případně *legacy rendering*).
- Ve VM už bylo: Windows 11 Pro 25H2 (neaktivované), **Claude Desktop 4.4212**, Git 2.55, uv, Codex CLI, Edge/WebView2.

## Průběh

| Krok | Stav | Poznámky |
| --- | --- | --- |
| Záloha a úprava VM | ✅ | viz výše |
| Trimble ID + stažení | ✅ | uživatel; banner „Are you a student or an educator?“ je jen obecná nabídka, ne blokace. Stahuje se **Tekla Launcher** (14 MB, Squirrel, podepsán Trimble Inc.) |
| Instalace Tekla 2026 + prostředí | ✅ | přes Launcher (~15 min); verze **2026 SP1 (226.1.58695)**, nainstalované jen prostředí *Default* (+ blank_project). Záloha VM před aktivací: `~/VMs/backup-2026-10-30-pred-aktivaci-tekly/` (SHA256 OK) |
| Aktivace trialu | ✅ 30. 10. 10:49 | Launcher → *Activate trial* otevře web `download.trimble.com/...?page=activate` → tlačítko *Activate trial* (= souhlas s T&C) → „Trial - Single User 2026“; platí 30 dní (~do 29. 11. 2026) |
| Nový model | ✅ | Launcher → New → *New blank model*, název `KOPIE_test`, bez Trimble Connect, prostředí Classic → *Default*, role *Steel Detailer* → `C:\TeklaStructuresModels\KOPIE_test`. 3D pohled na softwarovém vykreslování (QXL, bez GPU) **funguje**, start ~1 min |
| Claude Desktop – přihlášení, Code tab | ✅ | Desktop 4.4212 už přihlášený (Max). Výběr složky → dialog **„Trust this workspace?“** → *Trust workspace* |
| A1 – příprava projektu (řekni agentovi) | ✅ ~6 min | rozbalil balíček, přejmenoval CLAUDE.md, našel verzi, model, logy, `XS_MACRO_DIRECTORY`, offline CHM; **17 XML dokumentací API** v `C:\Program Files\Tekla Structures\2026.0\bin\` zkopírováno do `reference/`; v novém modelu chyběla `macros\modeling` → zeptal se a založil |
| Vymodelovat jednoduchou halu (makro 04) | ✅ | agent napsal, ověřil API v XML a nasadil makro; v Tekle po *Reload catalog* nalezeno, dvojklik → potvrzovací dialog → **51 z 51 dílů** (20× HEA200, 31× IPE300) |
| MCP B1 – instalace (řekni agentovi) | ✅ ~3 min | agent stáhl `TeklaMcp.Server` v0.9.0 pro Teklu 2026, **ověřil SHA256**, rozbalil do `C:\Nastroje\TeklaMcp`, zazálohoval `claude_desktop_config.json`, ukázal diff a počkal na souhlas; sám vysvětlil úplné ukončení Claude (ikona u hodin → Quit) |
| MCP – spojení | ✅ | po restartu Claude: `tekla_get_connection_info` → model `KOPIE_test`, `serverReadOnly: true`, server sestavený pro 2026.0, DLL z `...\2026.0\bin` → **funguje s Teklou 2026 SP1** (autor testoval jen 2021/2023) |
| MCP B2 – dotazy | ✅ | souhrn modelu: 51 dílů, **12 926,1 kg** (ruční kontrola 20×253,5 + 31×253,4 ≈ 12 926), rozpad podle profilu, materiálu i fáze (`tekla_group_weight_by`, `attr:PHASE` funguje) |
| MCP B3 – zápis s náhledem | ✅ | agent odebral READ_ONLY, vytvořil `.claude/settings.json` s `ask: mcp__tekla__*`; po restartu: náhled `apply=false` (20 sloupů třída 1→5, model beze změny) → souhlas → zápis → agent zpětně ověřil; **jedno Ctrl+Z vrátilo změnu** (ověřeno makrem 01) |
| Cvičení 1 – výpis (makro 01) | ✅ | agent makro před nasazením sám **přeložil proti DLL Tekly** a nasadil; nabídl tlačítko „Doběhlo“. CSV 51 řádků, `;` + desetinná čárka; HEA200 42,26 kg/m, IPE300 42,23 kg/m (sedí s tabulkami). Agent sám upozornil, že nosníky nejsou zkrácené na sloupech |
| Cvičení 2 – kontrola modelu | ⏭ přeskočeno | pro začátečníka zbytečně složité (zjišťovat výchozí profil přes Inquire) → zjednodušit/vypustit |
| Cvičení 3 – změna třídy (makro 03) | ✅ | dialog „Změním 51 vybraných dílů… Pokračovat?“ → 51 z 51; **jedno Ctrl+Z vrátilo třídu i UDA u všech dílů** (ověřeno makrem 01 před/po) |
| Chyba v makru | ✅ ověřeno | úmyslně rozbité makro → Tekla ukáže okno **CompileError** se souborem, řádkem a textem (CS1061…); **do logů se nezapisuje** (log má jen „Macro Run Requested“) |

## Zjištění

### Claude Desktop
- **Výchozí režim oprávnění je Auto**, ne Manual (Desktop 4.4212). Menu: Auto („Claude handles permission decisions“), Manual, Accept edits, Plan, Bypass permissions (šedé, „Enable in Claude Code settings“).
- **Manual je pro neprogramátora únavný:** ptá se na každý příkaz, i na čtení složek (A1 = ~6 dotazů s dlouhými PowerShell příkazy, kterým laik nerozumí). Tlačítka: *Deny*, *Allow once* (Ctrl+Enter), rozbalovací *Always allow* / *Allow and switch to Auto*.
- **I v Auto** se ptá na čtení souborů **mimo projektovou složku** (např. složka modelu `C:\TeklaStructuresModels\...`) → nabídka *Always allow – applies to this session only*.
- Při výběru složky se objeví **„Trust this workspace?“** – na webu zmínit.
- Desktop ukazuje i relace z jiných počítačů stejného účtu (synchronizace) – nevadí, jen to plete.

### Tekla 2026 SP1
- Prostředí po instalaci přes Launcher: jen *Default* (+ blank_project). Nový model: Launcher → **New** → *New blank model* → název → (odškrtnout Trimble Connect) → Environment: *Classic → Default* → **Role** (např. *Steel Detailer*).
- **XML dokumentace API je přímo v instalaci**: `C:\Program Files\Tekla Structures\2026.0\bin\Tekla.Structures*.xml` (17 souborů); offline CHM: `C:\ProgramData\Trimble\Tekla Structures\2026.0\Help\TeklaOpenAPI_Reference.chm`.
- Výchozí `XS_MACRO_DIRECTORY`: `C:\ProgramData\Trimble\Tekla Structures\2026.0\Environments\common\macros\` (modeling/, drawings/).
- Nový model **nemá** `macros\modeling` – je třeba ji založit.
- Logy: `%LOCALAPPDATA%\Trimble\Tekla Structures\2026.0\logs\TeklaStructures-<pid>.log/.err`, model: `<model>\logs\`.
- **Reload catalog:** panel *Applications & components* (ikona vpravo) → **≡** (vpravo nahoře v panelu) → *Catalog management* → *Reload catalog*. Pak makro najde vyhledávání (název souboru bez .cs).
- **Makro se spouští dvojklikem** na ikonu ozubených kol v panelu Applications & components.
- **Windows Forms dialogy v makrech fungují** (MessageBox s diakritikou OK) – dřívější „NEOVĚŘENO“ vyřešeno.
- Ovládání pohledu: Ctrl+šipky otáčí 3D pohled.

### Postup / web – co upravit
- **MCP pravidlo `ask: mcp__tekla__*` je moc upovídané:** ptá se i na čistě čtecí nástroje (connection info, souhrn). Okno povolení u zápisu ukazuje celý seznam změn a tlačítko *Allow once* je aktivní až po **dorolování na konec** („Scroll to the end to allow this“). Pro začátečníka: stačí server s náhledem (`apply=false` → agent se zeptá česky) a pravidlo `ask` dát jen na zapisovací nástroje, nebo ho vynechat.
- Po zápisu přes MCP agent model **neuloží** – upozorní „uložte Ctrl+S, nebo vraťte Ctrl+Z“. Dobré, na webu zmínit.
- MCP i makra fungují s Teklou 2026 SP1 → varování „netestováno na živé Tekle“ na webu nahradit „ověřeno 30. 10. 2026 na Tekle 2026 SP1 (trial)“.
- **Chyby maker:** kompilační chyba je jen v okně CompileError, ne v logu → (1) agent má makro vždy předem přeložit proti DLL Tekly (dělá to sám), (2) makra mají chyby za běhu zapisovat do `vystupy\makro_chyby.txt`, který si agent přečte, (3) když se okno přece objeví: **Win+Shift+S a vložit obrázek Claudovi (Ctrl+V)** – jednodušší než kopírovat text.
- **Ctrl+Z po makru 03 funguje** (jeden krok vrátí celou změnu) – „NEOVĚŘENO“ z webu odstranit.
- Cvičení 2 (kontrola výchozích profilů) je pro začátečníky moc složité.
- Při testu bylo vybráno vše (Ctrl+A, 52 objektů vč. osnovy) – makra správně zpracovala jen díly (51).
- Agent v odpovědi chtěl, ať uživatel **zkopíruje text chybového okna** – zbytečné: agent si má chyby přečíst **sám z logu Tekly** (do CLAUDE.md/skillu dát pravidlo „chyby čti z logu, uživatele žádej až když tam nejsou“).

