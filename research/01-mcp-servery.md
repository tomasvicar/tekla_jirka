# MCP servers for Tekla Structures (state as of 2026-10-30)

Method: GitHub search (`gh search repos` for "tekla mcp", "teklamcp", "tekla-mcp", "tekla model context protocol", "tekla claude"), READMEs and docs read through the GitHub API, plus npm, PyPI, NuGet, LobeHub, mcpmarket, Glama, Trimble support pages and LinkedIn snippets from web search.
Legend: **[V]** = verified in the README, docs or API metadata. **[I]** = inferred or not verified. Star counts and dates come from the GitHub API on 2026-10-30.

## TL;DR
- **There is no official Trimble MCP server.** Trimble's own route is the built-in **Tekla Model Assistant (Preview)** in TS 2026 SP2. It is agentic, but it runs in a Tekla side pane and needs a Diamond, Graphite or Carbon subscription. Its documentation says nothing about MCP or external clients. [V] https://support.tekla.com/doc/tekla-structures/2026/mod_tekla_model_assistant , https://support.tekla.com/trimble-assistant-for-tekla
- Every server listed here connects to a **running Tekla instance (Windows only) through the Tekla Open API** (.NET Framework 4.8). The C# servers load the DLLs directly. The Python servers use pythonnet. [V]
- **Serious candidates:** (1) **tempalg1n/tekla-mcp-server**: C#, MIT, 120 tools, best on drawings and safety. (2) **teknovizier/tekla_mcp_server**: Python, GPL-3, most stars, about 60 tools. (3) **martin9020 Tekla-MCP-Server**: C#, about 115 tools, but proprietary ("All Rights Reserved") and the original repo is gone. Everything else is a small MVP or demo.

## 1. tempalg1n/tekla-mcp-server [V]
- URL: https://github.com/tempalg1n/tekla-mcp-server . Author "ivan", Moscow. **C# / .NET 4.8**, stdio. Released as one exe per Tekla version. **MIT.** 7 stars, 4 forks. v0.9.0 released 2026-10-19 (v0.8.0 on 2026-09-30). 9 open issues and roughly 20 closed, actively maintained. README states "v0.9.0 — early development".
- Tekla versions: maintainers ran it on live **2021 and 2023** models. **2025 and 2026** are used in the field (issues #15, #17). 2022 and 2024 are compiled but not run. On 2024+ (Trimble.Remoting) it does not yet reconnect after a Tekla restart.
- Tools: **120 in 7 toolsets.**
  - `core` (4): connection info, model summary, `tekla_get_numbering_status`, `tekla_report_gap`.
  - `model` (42): find, list and get objects, properties, solid, bounding box, curve geometry, grids, control lines, IFC reference geometry, assemblies, catalogs, advanced options, UDA read/write, create/modify beam, column, plate, connection, component, copy connection, delete, generate frame, columns on a grid, save and open model.
  - `analytics` (10): count, sum weight, group weight by field or UDA, distinct values, modeling QA, selection.
  - `files` (3): export parts and IFC reference objects to jsonl/csv, import UDAs from a file.
  - `drawings` (54, *experimental*): list, check, create, update, issue and unissue, delete, PDF export, views (GA, section, detail), dimensions, marks, texts, clouds, `tekla_capture_drawing`.
  - `visual` (2): `tekla_capture_view` (screenshot of the model view) and a schematic.
  - `scripting` (5): Open API documentation search, check and run C# (a mutating script needs the SHA-256 of the source the user approved).
  - There is **no IFC model export tool** (issue #48 asks for one). Numbering is read only.
  - Sources: https://github.com/tempalg1n/tekla-mcp-server/blob/main/docs/tools.md , https://github.com/tempalg1n/tekla-mcp-server/issues/48
- Safety: writes run with `apply=false` (preview) by default, `TEKLA_MCP_READ_ONLY=1` is available, changed objects get the `MCP_ORIGIN` UDA, Ctrl+Z works, and `expectedModelPath` stops writes to the wrong model.
- Install: download `TeklaMcp.Server-v0.9.0-teklaXXXX.zip`, unzip it, and add `{"command":"...\\TeklaMcp.Server.exe"}` to the MCP config. A mock build exists for running without Tekla.
- Limitations: one Tekla per version, about a 60 s client timeout (needs paging with `maxObjects`/`cursor`), and a committed drawing write is not saved until you call `tekla_save_drawing`.

## 2. teknovizier/tekla_mcp_server [V]
- URL: https://github.com/teknovizier/tekla_mcp_server . **Python 3.11–3.13 + pythonnet 3.1 + FastMCP 3.4.** **GPL-3.0.** 58 stars, 21 forks, about 413 commits. Created 2025-06, last push 2026-10-24. 0 open issues and no releases.
- Tested with **Tekla 2022 and 2026** (2026 loads from `bin\Net48Runtime`). Verified clients are Claude Desktop, DeepChat and Goose. Verified models include Claude Sonnet 4.6, Haiku 4.5 and GPT-4o. https://github.com/teknovizier/tekla_mcp_server/blob/main/docs/compatibility.md
- Tools (about 62, full list in https://github.com/teknovizier/tekla_mcp_server/blob/main/docs/reference.md ):
  - **Selection**: by filter (type, class, profile, material, phase, prefix, UDA, AND/OR), by saved filter, by GUID, switch to assembly or main part.
  - **Components**: put, get, modify, remove (lifting-anchor plugin with center-of-gravity logic).
  - **Properties**: get and set (name, profile, material, class, finish, numbering prefix/start, phase, UDA), cut parts, clear UDAs, coordinates, bounding box, compare elements, copy IFC properties to UDAs.
  - **View**: labels, zoom, hide, color, view filter.
  - **Operations**: boolean cuts, orphan check, attach assemblies and rebars, invalid objects, `clash_check`, `create_report` (.rpt templates), `run_macro`.
  - **Drawings**: list, read and set properties, issue, update, collision check (via DXF), unattached-dimension check, PDF print, DWG/DXF export, open and close, views, annotations, unmarked objects, move and align views.
  - **Modeling**: place beams, columns, panels, slabs, grid, phase, move, copy, delete.
  - Resources: catalogs, macros, reports, filters, phases, grids, reference models, `project://context` (your own markdown conventions).
  - Not covered: no IFC export tool, no numbering run (only via `run_macro` [I]).
- Read-only mode and `excluded_tags` in `settings.json`.
- Install: `uv pip install -r requirements.txt`, copy five `config/*.sample.json` files, set `tekla_path`, then use `"command":"python","args":["...mcp_server.py"]`. https://github.com/teknovizier/tekla_mcp_server/blob/main/docs/quickstart.md
- Limitations: a conflict with the PyPI package `clr` (delete it), and configuration is read only at startup. Semantic attribute mapping (MiniLM, about 120 MB) is opt-in.
- [I] The LinkedIn posts by Pasi Aromäki about a "Tekla MCP server + sentence-transformers" probably refer to this project. https://fi.linkedin.com/in/pasiarom%C3%A4ki

## 3. martin9020 "Tekla-MCP-Server" (mirror iflow-mcp/martin9020-tekla-mcp-server) [V]
- Mirror: https://github.com/iflow-mcp/martin9020-tekla-mcp-server . The original `github.com/martin9020/Tekla-MCP-Server` returns 404 (deleted or private). Listing: https://mcpmarket.com/server/tekla . **C# .NET 4.8**, stdio. Optional Python subprocess for semantic search (MiniLM + ChromaDB). **License: "Copyright Martin Velichkov. All Rights Reserved"** (not open source).
- Live-validated on TS **2023.0 and 2026.0**. 2024 and 2025 are compile targets only.
- Tools (about 115):
  - Connection: CheckConnection, CommitChanges.
  - Selection and query: SelectElementsByFilter, ProjectQuery, Get/SetElementsProperties, ClearElementsUDAs, CompareElements.
  - Catalog: profiles, materials, bolts.
  - Spatial: extents, statistics, grid, bounding box, distance.
  - Creation: beam, column, plate, polybeam, curved beam, grid, pad footing, cut, Modify/Move/Copy/Delete.
  - Components: Put/Remove/List, attributes, RunMacro, advanced options.
  - View: labels, temporary graphics, color.
  - Connections: CreateBoltGroup, CreateWeld, CreateFitting.
  - Phases and assemblies.
  - Drawings (about 33): create A/W/GA drawings, views and sections, dimensions, marks, texts, print, issue, drawing UDAs.
  - Export: **ExportIFC, ExportNCFiles, GenerateReport, RunClashCheck**.
- Install: clone, run `build-project.ps1`, then point the config to `TeklaMcpServer.exe`.
- Practical risk: the license and the missing upstream repo.

## 4. Smaller or experimental servers [V unless marked]
| Repo | Stack / license | Tekla | Notes |
|---|---|---|---|
| https://github.com/osc-bouw/TeklaMCP (Develoh, NL) | C# WPF app, **HTTP** `127.0.0.1:51234`, GPL-3 | 2023+ | 10 tools: PlaceBeam(s), PlaceColumn, ModifyBeam, FilterModel, GetUserSelection, UserSelectedBeam, DeleteObject(s), OverlappingNumbering. Audit log. 2 stars |
| https://github.com/nguyenthanguth/MCP-TeklaStructures-Csharp | C# net481, MIT | 2025 only | 68 tools: query, create (beams, plates, bolts, rebar), modify, UDA, MTO, geometry, work plane, drawings (create A/W/GA/cast unit, views, dimensions, marks). One commit (2026-07), 0 stars |
| https://github.com/40ushek/svMCP (PL) | C# net8 + net48 bridge, no license | 2021, 2025 | Focused on **drawings**: arrange_dimensions/marks, resolve_mark_overlaps, export PDF, create A/W/GA. 1 star, README in Russian |
| https://github.com/SherinWorin/sherin-tekla-mcp | C# (official MCP C# SDK), MIT | 2025 | 16 tools: query, quantity report/CSV, validate, create beams/columns, modify, delete. Read-only by default, confirm tokens. v0.1 **not yet tested on live Tekla** |
| https://github.com/HuVelasco/tekla-mcp | Python FastMCP + C# bridge; README says "All rights reserved" but the badge says MIT | unspecified | about 20 tools incl. `tekla_execute_code` (arbitrary code), UBIM import/export, review/apply changes. 0 stars |
| https://github.com/Tinivanser/Tekla_My_Mcp | .NET 9 host + net48 worker | 2024 | MVP: model info, selected objects, beam, modify/delete, API documentation search |
| https://github.com/YuriyKirillov/TeklaMCPServer | Python pythonnet | 2023 | 14 tools; a **copy of an older version of teknovizier** (same text, one commit 2026-02-18) [I] |
| https://github.com/zekeriyakaraca-pixel/teklamcp | Python, GPL-3 | 2019–2025 claimed | Turkish **derivative of teknovizier** [I] |
| HuskyBIM https://huskybim.com/products/tekla | commercial `.mcpb` extension for Claude Desktop | 2026 | "199 tools", free account + token; closed source, not checked in detail [I] |
| mmwarsztat/TeklaMCP, igel1989/Tekla-MCP-dist, ktpl-mohits/TeklaMcpBridge | private source or empty | – | binaries or installers only, cannot be verified |

## 5. Documentation-only MCP servers (do not touch the model)
- **tekla-api-mcp** (npm 1.3.1, MIT, Paweł Lisowski): https://github.com/pawellisowski/tekla-api-mcp , https://www.npmjs.com/package/tekla-api-mcp . Tools: `search_api`, `search_examples`, `get_example_details`, `get_class_details`, `get_method_details`, `get_statistics` (Open API docs + TSOpenAPIExamples). Install with `npx tekla-api-mcp setup`. Last publish 2025-09. [V]
- Out of scope: **tsd-mcp** is for Tekla *Structural Designer*, not Structures. https://github.com/vibhanshu-mishra/tsd-mcp
- Registries: PyPI has no tekla*-mcp package. NuGet has none either. npm has only tekla-api-mcp. Glama lists teknovizier and YuriyKirillov. LobeHub lists Mohitsharmaraina/tekla-mcp (repo returns 404). [V]

## 6. Recommended practices
Taken from READMEs, docs and real-use issues:
1. **Start in read-only mode and on a copy of the model.** Switch writes on only later. tempalg1n uses `TEKLA_MCP_READ_ONLY=1`, teknovizier uses `"read_only": true`, Sherin is read-only by default. Sources: tempalg1n README, teknovizier quickstart, Sherin README.
2. **Preview, then confirm.** Have the agent show the plan and approve `apply=true` only after that. Check the outcome (`committed`, `partial`, `unknown`). Run CommitChanges after each batch (martin9020). Save drawings explicitly with `tekla_save_drawing`. Sources: tempalg1n README, martin9020 README.
3. **Match the server build to the exact Tekla version.** On TS2024+ the transport is Trimble.Remoting. Run only one Tekla per version, or set `expectedModelPath`, `TEKLA_VERSION` or `TEKLA_BIN_DIR`. svMCP on TS2025 needs a bridge in the extensions folder with `exe.config` codeBase entries. Sources: tempalg1n README, svMCP README, martin9020 README.
4. **Large models.** The client times out after about 60 s. Page with `maxObjects`/`cursor`, and send bulk data through files (jsonl/csv) rather than through context. Source: tempalg1n docs/tools.md.
5. **Context budget.** Two servers in one client cost about 2×177k characters of tool descriptions. Limit them with `TEKLA_MCP_TOOLSETS` or `excluded_tags`. Source: issue #48.
6. **Concurrency.** Several chats against one Tekla instance cause timeouts and dropped connections. Work in one chat. `Operation.CopyObject` copies bolts and welds unreliably, and IFC export marks the model as "unsaved". Source: issue #48.
7. **Select first, then operate.** Follow Tekla's UX of selecting by filter or GUID and then modifying. Verify profiles and materials in the catalog before creating anything. Store project conventions (classes, prefixes, naming) as markdown context, for example `project://context`. Sources: martin9020 README, teknovizier reference.md.
8. **Python pitfalls.** Delete the PyPI `clr` package that conflicts with pythonnet, and use Python ≤3.13 because pythonnet does not support 3.14. Sources: teknovizier quickstart, zekeriyakaraca README.
9. **Prompts.** Write concrete, step-by-step instructions with profiles, materials, coordinates and component numbers, and say "CommitChanges after each step". The martin9020 README has a portal-frame example. A workshop, "AI in Tekla Structures. Build your own MCP…" (2026-04-22), also covered mistakes to avoid: https://addcal.io/e/e2dx35ha75hg [I, content not checked]

I found no relevant threads on Reddit or forum.tekla.com. LinkedIn content is visible only as search snippets (Yury Kulikou: https://ua.linkedin.com/in/kuliouyury). [I]
