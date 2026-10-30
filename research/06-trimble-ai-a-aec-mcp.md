# 06: Trimble/Tekla official AI direction and sibling AEC MCP patterns

Research date: 2026-10-30. Web research only, nothing was installed. "(unverified)" means it comes from a third-party listing or search snippet, or I could not open the primary page.

---

## A) What Trimble/Tekla offers officially

### A1. AI features inside Tekla Structures

| Feature | What it does | Status / licence | Source |
|---|---|---|---|
| **Trimble Assistant for Tekla: User Assistant** | Chat Q&A over Trimble User Assistance docs (Tekla Structures, TSD, Tedds, PowerFab). In the browser, and in the Tekla Structures side pane | GA since TS 2025. Diamond/Graphite/Carbon subscription, or Partner/Evaluation licence | https://support.tekla.com/doc/tekla-structures/2025/rel_trimble_assistant_for_tekla , https://support.tekla.com/doc/tekla-structures/not-version-specific/trimble_assistant_for_tekla |
| **Trimble Assistant for Tekla: Developer Assistant** | Writes macros/Open API code (RAG over Open API docs). **Has no access to the model** | Preview in TS 2025. Diamond, Partner, or Trimble Labs | same + https://www.tekla.com/assets/documents/trimble_assistant_for_tekla_developer_assistant_-_security_white_paper_v.1.9.pdf |
| **Tekla Model Assistant** (agentic) | Side-pane agent that reads live context (selection, views) and creates/modifies beams, columns, plates, slabs, grids, UDAs, components. Also runs filters, reports, clash checks, generated macros, GA-drawing operations, PDF export, and Trimble Connect up/download. Asks for confirmation on risky ops. Customisable with **rules.md / skills.md** files in user/model/project/firm folders | **Preview** via Trimble Labs: TS 2025 SP9 and TS 2026 SP2. Diamond/Graphite/Carbon only. Install via setup option or a `.tsep` from Tekla Warehouse | https://support.tekla.com/doc/tekla-structures/2026/mod_tekla_model_assistant , https://support.tekla.com/doc/tekla-structures/2025/rel_2025_sp9_new_features_and_improvements , https://support.tekla.com/doc/tekla-structures/2026/rel_2026_sp2_new_features_and_improvements |
| AI Cloud Fabrication Drawings | Cloud-generated fabrication drawings | Preview at 2025 launch, "available now" in Nov 2025 | https://news.trimble.com/2025-03-12-Trimble-Expands-Connected-Workflows-in-Tekla-Structures-2025 , https://news.trimble.com/2025-11-10-Trimble-Highlights-AI-Strategy-and-Innovation-at-Dimensions-User-Conference |

Documented Model Assistant limits: it cannot click UI, can undo only the last action, and has no memory between sessions. It also cannot do full rebar automation, edit bolt groups, open IFC/DWG, run structural calculations, or create single-part/assembly drawings automatically. It does not monitor the model in real time (https://support.tekla.com/doc/tekla-structures/2026/mod_tekla_model_assistant). Its tool surface (create/modify/filter/report/macro/drawings) is essentially the same set a third-party Tekla MCP would expose. The rules/skills files work much like CLAUDE.md and skills.

A new "Trimble Assistant for Tekla" running on a "proprietary Trimble AI platform" is in development. The old one is kept as "Classic" (SP9/SP2 release notes above).

### A2. Trimble-wide agentic AI
- At Dimensions 2025 (Nov 10–12, 2025) Trimble announced an "open and extensible" **agentic AI platform** and **Trimble Agent Studio**, piloted with select customers and headed for Labs. The Trimble Connect Help Assistant was due in Labs in Q1 2026 (https://news.trimble.com/2025-11-10-Trimble-Highlights-AI-Strategy-and-Innovation-at-Dimensions-User-Conference , https://aecmag.com/ai/trimble-builds-ai-strategy-around-agentic-ai-platform/).
- At the same event Trimble announced its first developer conference for third-party developers, to be held inside Dimensions 2026. The developer-summit page lists sessions on Developer Console, Agent Studio, Trimble Workflows and Marketplace (https://www.trimble.com/en/our-company/events/dimensions/developersummit; date of page unverified). I found no public statement that Agent Studio supports MCP.

### A3. MCP and partnerships
- **The only official Trimble MCP server I found is for SketchUp**, not Tekla. It is a hosted remote server at `https://api.sketchup.com/mcp/v1/sketchup/mcp` with OAuth via Trimble ID. It was launched on 2026-04-28 in Anthropic's "Claude for Creative Work" connector set, and Claude is the only officially supported assistant. It generates new models only. Free users get 30 SKP/month; paid SketchUp has no limit (https://www.engineering.com/now-sketchup-has-an-mcp-server-for-claude-based-3d-modeling/ ; endpoint from https://mcpservers.org/remote-mcp-servers/sketchup, unverified).
- **No official Tekla or Trimble Connect MCP server was found** (searched Oct 2026). The Trimble Connect MCP servers that exist are community projects (see B).
- Microsoft: a long-running strategic partnership, said to have been extended to generative AI. The only source is a 2024 article (https://aimagazine.com/company-reports/navigating-new-horizons-how-trimble-is-reshaping-industries) (unverified detail). Tekla assistants run on Azure (white paper below). I found no Trimble–OpenAI deal. The only Trimble–Anthropic link is the SketchUp connector.

### A4. Terms, automation and developer program
- The AI Transparency Notice for Trimble Assistant for Tekla says verbatim: **"Automation is prohibited."** Provider is Trimble Europe B.V.; the model is not named (https://support.tekla.com/legal/transparency-notice-for-ai-system-use-in-trimble-assistant-for-tekla). This means you must not script or bot-drive Trimble's assistant. It does not restrict your own Open API use.
- Tekla developer policy: you may build Open API apps for your own use. Distributing or selling them requires the paid Tekla Partners Program. Partner-licence software may not be used for production modeling. Trimble Connect apps are "internal use only" (https://developer.tekla.com/policy). Trimble Developer Terms v1.2 (https://trimble.com/legal/developer-terms). A company running Claude plus a local Open API bridge on its own licences is therefore "own use". Sharing a tool commercially is a Partners Program matter. This is my interpretation, not legal advice.
- I found no clause in the Tekla terms that explicitly bans third-party LLMs from driving the Open API (unverified: the full EULA was not reviewed).

### A5. Data privacy
- Developer Assistant white paper v1.9: it runs on Microsoft Azure, "multiple models provisioned by the Trimble platform". New version is in **US, Virginia**; Classic is in Azure North Europe. Identity and licensing run on AWS (Ireland). Prompts are visible to limited Trimble staff "in an anonymous format". There is **no access to models, drawings or metadata** (https://www.tekla.com/assets/documents/trimble_assistant_for_tekla_developer_assistant_-_security_white_paper_v.1.9.pdf).
- User Assistant white paper: https://www.tekla.com/assets/documents/trimble_assistant_for_tekla_user_assistant_-_security_white_paper_v.1.7.pdf. Trimble's general AI notice says user data is not used to train models for other customers (https://www.trimble.com/en/our-commitment/responsible-business/data-privacy-and-security/data-privacy-center/ai-transparency-notice) (from a search snippet, unverified).
- The **Model Assistant** page does not document its data flow or LLM provider. It necessarily sends live model context to the Trimble cloud (inference). With Claude plus a local MCP, whatever the tools return (names, profiles, UDAs, coordinates) goes to Anthropic. So use read-only/minimal tool outputs and check client/NDA rules.

**Bottom line A:** With a Diamond/Graphite/Carbon subscription, **Tekla Model Assistant** is the official in-app alternative to a Claude+MCP setup. It is preview, Tekla-only, and closed, with a fixed toolset. Claude adds cross-tool work (files, Excel, Connect, code), your own tools, and model choice.

---

## B) Sibling AEC MCP servers (reference patterns)

| Tool | Project / URL | Maturity | Architecture |
|---|---|---|---|
| **Tekla** | teknovizier/tekla_mcp_server (https://github.com/teknovizier/tekla_mcp_server) | Community, GPL-3.0, ~58 stars. Tested with TS 2022 and 2026 | Python FastMCP 3.0 server with providers (Selection, View, Properties, Components, Operations, Drawings, Modeling). Read-only mode, hideable tool categories, embedding-based attribute mapping. Uses the Open API from outside the process (how it connects is not stated on the README; unverified) |
| **Revit (community)** | https://github.com/mcp-servers-for-revit (revit-mcp 475★, now archived → monorepo mcp-servers-for-revit 413★; mcp-server-for-revit-python 220★) | Most mature community ecosystem, MIT | **C# add-in inside Revit = WebSocket bridge** + TS MCP server (stdio) + pluggable "command set" running in Revit ExternalEvents. The Python variant uses pyRevit Routes HTTP and an `execute_revit_code` tool |
| **Revit (official)** | Autodesk Revit Public MCP Server (https://www.autodesk.com/blogs/aec/2026/06/17/revit-public-mcp-server/ , https://help.autodesk.com/view/ADSKMCP/ENU) | Revit 2027 add-on, tech preview; read-tools first | Add-on + stdio, any MCP client |
| **Rhino/Grasshopper** | xunliuDesign/rhino-gh-mcp (https://pypi.org/project/rhino-gh-mcp/), REER RhinoMCP, others (https://lobehub.com/mcp?q=rhino) | Community, many forks | Rhino plugin TCP socket (:9876) + GH component HTTP server (:9999) + Python MCP (unverified) |
| **SketchUp** | Official hosted (A3). Community mhyrr/sketchup-mcp (https://glama.ai/mcp/servers/@mhyrr/sketchup-mcp/tree) | Official = cloud generation only. Community = live editing | Ruby extension opens a TCP server in SketchUp + Python MCP. Fork zinin/sketchup-mcp2 has `eval_ruby` **off by default** in the Warehouse build (https://glama.ai/mcp/servers/zinin/sketchup-mcp2) |
| **Archicad** | tapir-archicad-mcp (https://pypi.org/project/tapir-archicad-mcp/), archicad-mcp (https://pypi.org/project/archicad-mcp/) | Community | Uses Archicad's JSON API + Tapir add-on. "4 MCP tools front 173 commands" (dispatcher pattern) |
| **AutoCAD** | puran-water/autocad-mcp (https://gittrend.io/repo/puran-water/autocad-mcp, ~216★), acad-cmd COM (https://lobehub.com/en/mcp/emptykot-acad-cmd) | Community | COM/pywin32, or LISP dispatcher loaded in AutoCAD, or headless DXF |
| **Navisworks** | xuantinhnbs-rgb/navisworks-mcp (https://glama.ai/mcp/servers/xuantinhnbs-rgb/navisworks-mcp), NavisCoord (https://www.typingmind.com/mcp/naviscoord-mcp) | Community, early (unverified) | Native .NET add-in + MCP server |
| **IFC** | JotaDeRodriguez/Bonsai_mcp (https://github.com/JotaDeRodriguez/Bonsai_mcp), Show2Instruct/ifc-bonsai-mcp (https://github.com/Show2Instruct/ifc-bonsai-mcp) | Community | Blender+Bonsai add-on (socket) + Python MCP using IfcOpenShell. Can query entities, spatial tree, quantities |
| **Speckle** | Daviidro/speckle-mcp (https://glama.ai/mcp/servers/Daviidro/speckle-mcp) | Community; no official Speckle MCP found | Metadata/projects/versions via Speckle API, no geometry |
| **Trimble Connect** | nhantruong96/trimble-connect-mcp (https://glama.ai/mcp/servers/nhantruong96/trimble-connect-mcp/tree), SimonTrim/trb-mcp-server-api (https://glama.ai/mcp/servers/SimonTrim/trb-mcp-server-api) | Community | stdio Python, 40 tools on Core API v2. **Writes gated behind `TC_ENABLE_WRITE=1`**, no undelete |

### Patterns that transfer to Tekla
1. **The dominant pattern is an in-host add-in + a localhost socket + an MCP server** (Revit, Rhino, SketchUp, Navisworks, Blender). Tekla is easier: its Open API is used **from outside the process** by an exe that talks to the running Tekla instance. So an MCP server can call `Tekla.Structures.Model` directly without a socket plugin (based on known Open API behaviour; see https://support.tekla.com/doc/tekla-structures/2026/sys_tekla_open_api, page not re-checked, so unverified). teknovizier does this from Python. For a C# design see the Revit "command set" split.
2. **Typed tools + an escape hatch** (Revit `execute_revit_code`, SketchUp `eval_ruby`, Tekla Model Assistant's "generate and run macro"). Keep the escape hatch off by default.
3. **Read-only by default with opt-in writes** (Autodesk official read-tools first, Trimble Connect `TC_ENABLE_WRITE`, teknovizier read-only mode).
4. **A dispatcher for large APIs** (Archicad: 4 tools → 173 commands) keeps the tool list small.
5. **A rules/skills context file** (Tekla rules.md/skills.md; CLAUDE.md in the pyRevit tutorial).

### Cross-tool paths that work with Tekla today
- **IFC:** Tekla exports IFC natively. An IfcOpenShell-based MCP (Bonsai_mcp) can then query it offline, read-only. This needs no Tekla licence on the AI side and limits data exposure.
- **Speckle:** the official Speckle Tekla connector (v3) supports **TS 2023/2024/2025, Windows**. 2026 is not listed. It "does not take care of updating existing elements" (https://docs.speckle.systems/connectors/tekla , https://www.speckle.systems/blog/speckle-next-gen-tekla-connector-upgrade-your-structural-workflows). Speckle-mcp then gives the AI metadata access.
- **Trimble Connect:** community MCPs (above) can manage files and versions, for example .ifc/.trb/PDF published from Tekla. The Model Assistant itself can also push PDFs to Connect.

---

## Doporučené postupy / Recommended practices
- **Start read-only, then gate writes.** Use explicit approval for changes. Claude proposes the targets, and the action runs only after the user confirms (https://vagon.io/blog/how-to-use-revit-with-claude-mcp-computer-use; Tekla Model Assistant does the same). Use opt-in write flags (Trimble Connect MCP above).
- **Test on a model copy.** Bulk fixes on live projects are risky. Wrap edits in transactions with rollback, and check that elements exist and are editable first (https://www.bimpure.com/blog/pyrevit-mcp-claude-code-tutorial). For Tekla, the equivalent is `Model.CommitChanges()` only after validation. Tekla Model Assistant can undo only the last step.
- **Write a CLAUDE.md / rules file** with the Tekla version, units, naming, profiles and UDA conventions, connection details and working style (bimpure; Tekla rules.md/skills.md).
- **Bind local bridges to 127.0.0.1**, not 0.0.0.0 (bimpure).
- **Prompting:** give numbered, structured requirements. Let the agent check the version and setup through MCP instead of asking you. Use a cheaper model for simple queries and a stronger one for multi-step work (bimpure).
- **Explore, then productise.** Turn a useful MCP one-off into a reusable macro or extension (bimpure). Tekla Model Assistant also saves generated macros.
- **What works:** repetitive, selection/filter-based edits, cleanup, reports, dashboards. **What doesn't (yet):** complex geometry (stairs failed in Revit), UI/dialog-driven code, replacing proper add-ins (bimpure). Tekla's own assistant cannot do rebar automation, bolt-group edits or single-part drawings either.
- **Setup pitfalls:** MCP servers often do not show up until the path is checked and Claude Desktop is fully restarted. Watch Windows backslashes in the JSON config (https://www.cadforum.cz/en/why-isn-t-revit-mcp-server-showing-up-in-my-claude-ai-tool-tip15125 ; bimpure).
- **Do not automate Trimble's own assistant** ("Automation is prohibited"). Keep model data exposure to a minimum and check client NDAs before sending model data to any cloud LLM.
- I found few independent, first-hand failure reports. Most practice notes come from vendor or tutorial blogs (unverified as general experience).
