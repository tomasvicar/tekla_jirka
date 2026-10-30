# Workshop „Claude pro stavaře“ — plán a rozhodnutí

Vzor: `/var/home/tom/code/AI_agents_workshop` (workshop AI agentů pro biology, Quarto web + reveal.js slajdy).
Tato verze je upravená pro **stavaře / detailera, který v Tekla Structures navrhuje různé konstrukce
(ocel, prefabrikáty, beton)** a neprogramuje. Průzkum k tématu: `../research/` (začni `00-souhrn.md`).

## Cíl a publikum

- Jeden člověk (případně malá kancelář), **neprogramátor**, Windows, Tekla Structures.
- Ukázat, co je AI agent a čím se liší od chatbota, a naučit ho prakticky:
  1. **běžné kancelářské věci** – složkové struktury zakázek, třídění a přejmenování souborů,
     PDF výkresy, Excel, e-maily/dopisy, přehledy,
  2. **data z Tekly bez rizika** – exportované reporty → Excel, souhrny hmotností, nabídky, porovnání revizí,
  3. **živá Tekla** – C# makra, která napíše Claude, a MCP server (read-only nejdřív).
- Délka cca **2,5–3 h** (jde o individuální/malé sezení, ne velký workshop).

## Prostředí (závazné)

- **Placený Claude v aplikaci Claude Desktop na Windows, záložka Code.** Firma o 2 lidech: na zkoušku Pro, ostře Team se 2 místy Standard (min. 2 místa, Claude Code v ceně, firemní podmínky; ověřeno 30. 10. 2026).
  Žádný Codex, žádné CERIT. Terminál jen zmínit.
- Git for Windows doporučen. Python skripty přes `uv` (Claude si je spustí sám).
- Projektová pravidla: `CLAUDE.md` (ne AGENTS.md).
- Tekla Structures 2025/2026; MCP server favorit `tempalg1n/tekla-mcp-server` (read-only režim),
  viz `../research/01-mcp-servery.md`.

## Osnova (návrh)

| Čas | Blok |
| --- | --- |
| 15 min | Co je AI agent, chatbot vs. agent, smyčka |
| 20 min | Instalace Claude Desktop, první spuštění, CLAUDE.md, oprávnění |
| 40 min | Kancelář: složky zakázky, třídění a přejmenování souborů, PDF, Excel |
| 40 min | Data z Tekly: report → Excel, hmotnosti, nabídka, porovnání revizí, kontrola |
| 30 min | Živá Tekla: makro (read-only → změna na kopii), MCP |
| 15 min | Ukázky (co dalšího jde) |
| 10 min | Praktické: cena, soukromí, NDA, zálohy, licence Tekly |

## Data

- Vše **syntetické** a reprodukovatelné (generátory v `tools/`, pevné semínko 2026).
- Žádná reálná data klientů.

## Rozdělení práce (subagenti)

| Soubory | Obsah |
| --- | --- |
| `index.qmd`, `priprava.qmd`, `instalace.qmd`, `prakticke.qmd`, `files/CLAUDE.md`, `README.md` | úvod, instalace, praktické info, pravidla |
| `kancelar.qmd`, `tools/make_office_data.py`, `data/kancelar/`, `demos/kancelar/` | kancelářská cvičení |
| `cviceni.qmd`, `tools/make_tekla_data.py`, `data/tekla/`, `demos/tekla_data/` | data z Tekly |
| `tekla.qmd`, `files/makra/`, `files/CLAUDE_tekla.md`, `files/skills/` | živá Tekla |
| `ukazky.qmd`, `ukazky/*.qmd`, `demos/ukazky/` | galerie ukázek |
| `slides/index.qmd`, `slides/figures/`, `tools/make_figures.py` | prezentace |

## Otevřené body

- Verze a licence Tekly u kamaráda (Diamond/Graphite/Carbon → má i Tekla Model Assistant?).
- ~~Makra a MCP neotestované~~ → **vyzkoušeno 30. 10. 2026** na Tekle 2026 SP1 (trial ve VM na `ada`):
  příprava projektu agentem, makra 01/03/04/05 (hala, výpis, změna + Ctrl+Z, export PDF do vlastní struktury),
  MCP čtení i zápis s náhledem. Podrobně `../research/13-test-tekla-trial.md`.
- Web je na GitHub Pages: <https://tomasvicar.github.io/tekla_jirka/> (veřejně dostupný na URL).
- Zbývá: vyzkoušet u kamaráda na jeho PC a plné licenci (hlavně tisk PDF a jeho skutečné výkresy).
- Trial Tekly vyprší ~29. 11. 2026 (jen jednou na verzi, vázaný na VM).

## Stav webu (30. 10. 2026)

- 3 kola zjednodušení + 3 recenze (technická, začátečník, „detailer doma sám“); ~9–10 tis. slov.
- Stránky: Úvod, Příprava, Instalace, Kancelář, Data z Tekly, Živá Tekla, Ukázky (8 vč. Export do PDF),
  Nápady (≈40 nápadů), Praktické info, Prezentace (27 slajdů), Postup, Průzkum.
- Rozhodnutí: režim **Auto** (Manual je pro začátečníky moc upovídaný), MCP jen pro čtení a volitelně,
  změny modelu makry; chyby → výřez obrazovky (Win+Shift+S) do chatu; upravené makro nasazovat pod
  novým názvem (`_v2`), Tekla si pamatuje starou verzi.
