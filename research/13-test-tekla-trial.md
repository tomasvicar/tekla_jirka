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
| Claude Desktop – přihlášení, Code tab | ⏳ | |
| MCP tempalg1n přes „řekni agentovi“ | ⏳ | |
| Makra 01–03 | ⏳ | |
| Vymodelovat jednoduchou halu | ⏳ | |

## Zjištění

(doplňuje se během testu)
