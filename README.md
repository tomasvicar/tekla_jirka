# Tekla Structures + Claude Code

**Web: <https://tomasvicar.github.io/tekla_jirka/>**: workshop, [postup nasazení](https://tomasvicar.github.io/tekla_jirka/postup.html) a [průzkum](https://tomasvicar.github.io/tekla_jirka/pruzkum.html).

Průzkum a podklady: jak pomocí Claude Code / Claude Desktop (MCP, C# makra, skripty) automatizovat práci v Tekla Structures – pro uživatele, který neprogramuje.

## Obsah

- `workshop/` – Quarto web (workshop „Claude pro stavaře“, postup, prezentace); po pushi do `main` se nasadí na GitHub Pages (`.github/workflows/publish.yml`). Lokálně: `cd workshop && uv run quarto preview`.
- `research/` – výsledky průzkumu (číslované zprávy), na webu v sekci Průzkum
  - **00 – souhrn a doporučený postup → začni tady: [research/00-souhrn.md](research/00-souhrn.md)**
  - 01 – existující MCP servery pro Teklu
  - 02 – možnosti a limity Tekla Open API
  - 03 – příklady použití z praxe
  - 04 – instalace Claude na Windows
  - 05 – automatizace bez MCP (makra, skripty, soubory)
  - 06 – AI od Trimble a MCP pro jiné AEC nástroje
  - 07 – trial Tekly a testovací prostředí
  - 08 – jak dát Claudovi přesné znalosti Tekla API
  - 09 – bezpečnost, data, zálohy
  - 10 – výuka neprogramátora
  - 11 – nápady na automatizace
  - 12 – české a slovenské zdroje

Pozor: GitHub Pages z privátního repa jsou na své URL veřejně dostupné.
