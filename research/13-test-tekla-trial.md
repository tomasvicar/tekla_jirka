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
| MCP tempalg1n přes „řekni agentovi“ | ⏳ | |
| Makra 01–03 | ⏳ | |

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
- Agent v odpovědi chtěl, ať uživatel **zkopíruje text chybového okna** – zbytečné: agent si má chyby přečíst **sám z logu Tekly** (do CLAUDE.md/skillu dát pravidlo „chyby čti z logu, uživatele žádej až když tam nejsou“).

