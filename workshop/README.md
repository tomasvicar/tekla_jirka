# Claude pro stavaře

**Web: <https://tomasvicar.github.io/tekla_jirka/>**

Individuální workshop (~2,5–3 h) o AI agentovi Claude pro projektanta / detailera
v Tekla Structures, který neprogramuje: co je agent a čím se liší od chatbota,
instalace Claude Desktop (záložka Code) na Windows, kancelářské úlohy, zpracování
exportů z Tekly, makra a MCP pro živou Teklu, praktické info (cena, soukromí, NDA,
zálohy, licence).

- Plán a rozhodnutí: [`PLAN.md`](PLAN.md)
- Podklady z průzkumu: [`../research/`](../research/00-souhrn.md)
- Vzor: `AI_agents_workshop` (workshop pro biology)

## Struktura

| Soubor | Obsah |
| --- | --- |
| `index.qmd`, `priprava.qmd`, `instalace.qmd`, `prakticke.qmd` | úvod, příprava, instalace, praktické info |
| `kancelar.qmd` | kancelářská cvičení (složky, PDF, Excel) |
| `cviceni.qmd` | data z Tekly: report → Excel, hmotnosti, revize |
| `tekla.qmd` | živá Tekla: C# makra a MCP |
| `ukazky.qmd`, `ukazky/*.qmd` | galerie ukázek |
| `slides/index.qmd` | prezentace (reveal.js); obrázky v `slides/figures/` |
| `files/CLAUDE.md` | pravidla pro Clauda, která si účastník stáhne do pracovní složky |
| `files/CLAUDE_tekla.md`, `files/makra/`, `files/skills/` | pravidla, makra a skills pro práci s Teklou |
| `data/` | syntetická cvičná data (generují skripty v `tools/`, semínko 2026) |
| `demos/` | vzorová řešení a výstupy |
| `assets/` | obrázky a snímky rozhraní |

## Lokálně

```bash
uv run quarto preview      # náhled webu
uv run quarto render       # celý web do _site/
```

Všechna data jsou smyšlená; žádná skutečná data klientů do repozitáře nepatří.
