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
| Trimble ID + žádost o trial Tekla 2026 | ⏳ čeká na uživatele | formulář na jméno uživatele |
| Instalace Tekla 2026 + prostředí | ⏳ | |
| Claude Desktop – přihlášení, Code tab | ⏳ | |
| MCP tempalg1n přes „řekni agentovi“ | ⏳ | |
| Makra 01–03 | ⏳ | |
| Vymodelovat jednoduchou halu | ⏳ | |

## Zjištění

(doplňuje se během testu)
