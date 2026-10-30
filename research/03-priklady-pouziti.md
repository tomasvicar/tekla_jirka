# LLMs + Tekla Structures: real-world use examples (research as of 2026-10-30)

## Summary

There are few public, detailed first-hand accounts of practitioners using LLMs with Tekla. Most of the real activity sits in three places:

1. **Trimble's own AI tools** (Developer Assistant, Tekla Model Assistant), which are now the mainstream route.
2. **Community MCP servers** on GitHub, at least 8 of them, that let Claude, Codex or Cursor drive a live model.
3. **A handful of detailer write-ups and demos.**

Searches of Reddit, forum.tekla.com and Czech/Slovak (.cz/.sk) sources returned no relevant threads. The Tekla forum requires a login and is poorly indexed, so it was not searched directly. No Czech-language material was found. The nearest local contact is Construsoft CZ, the Tekla reseller.

Reliability tags used below: **[Official]**, **[Verified]** (I read the primary page), **[Weak]** (only a title or snippet, or a self-promotional claim).

## 1. Official Trimble AI tools

**Developer Assistant (in the Trimble Assistant for Tekla side pane)** [Official]
- You prompt it, and it generates C# Open API code. You can run the code directly with "Execute code" or save it as a macro.
- Example prompt from the docs: "Generate a macro that lists all profiles used in the model and then displays them in a dialog."
- Pitfalls Trimble itself states:
  - Generated code can fail. A "Run error log" button appears, and you edit and re-run until it works.
  - Use the *Default* environment, because the assistant takes profiles from it.
  - Always check the code and the results in the model or drawings.
- Availability: needs a Diamond or Partners licence, or Trimble Labs. It is bundled by default from TS 2025 SP5; up to SP4 you install it as an extension.
- https://support.tekla.com/doc/tekla-structures/not-version-specific/developer_assistant
- https://support.tekla.com/de/doc/tekla-structures/not-version-specific/developer_assistant

**Tekla Model Assistant (Preview, TS 2025 SP9 / 2026)** [Official]
- An agentic, natural-language tool that works on the live model and drawings. It reads the current selection and view, creates and modifies objects, sets UDAs, creates GA drawings, runs reports and clash checks, and adds marks.
- Example prompts from the docs:
  - "Create a 3x3 grid with pad footings at every intersection"
  - "Set class 5 on all HEA300 beams"
  - "Add part marks to all columns in the current drawing"
- It writes C# macros when no built-in tool fits, or when more than 500 objects are involved. Working macros are saved under `...\Environments\common\macros\ModelingAssistant\Generated Macros`.
- Limitations stated by Trimble:
  - It can only undo the last action.
  - It cannot modify bolt groups or open IFC/DWG files.
  - It cannot create single-part or assembly drawings, change layouts or add text.
  - It does not keep memory between sessions.
- Licence: Diamond, Graphite or Carbon subscription.
- https://support.tekla.com/doc/tekla-structures/2026/mod_tekla_model_assistant
- https://support.tekla.com/doc/tekla-structures/2025/rel_2025_sp9_new_features_and_improvements

**AI Cloud Fabrication Drawings** (preview in 2025, human-in-the-loop in 2026) generates fabrication drawings from your own drawing libraries. [Official, press]
- https://constructionmanagement.co.uk/trimble-announces-tekla-2026-updates

## 2. Practitioner examples

**Jordan Folkard (former steel detailer, now at BuildingPoint) used ChatGPT and Claude to build several Tekla plugins while still detailing full-time.** [Verified]
- His workflow: Idea → AI → Code → Build → Test in Tekla → Refine.
- Pitfall he stresses: AI code "looks convincing" but may not compile or may behave differently in Tekla, so "AI-generated code should never simply be assumed to be correct."
- His tips:
  - Start small and add features in stages.
  - Ask about small sub-problems (selecting objects, reading properties, dimensions).
  - Check method names against the Tekla Developer Center and the forum.
- The article names no specific plugins.
- https://buildingpoint.co.nz/ai-for-tekla/ (c. Oct 2026)

**Ilya Binus built TeklaAIBridge, a chat plugin that edits the model through the Open API.** [Verified post; commercial; no results data]
- Examples:
  - "Replace all HEA200 columns on grid C with HEA240"
  - "Find and select all RHS* profiles"
  - "Set class 3 and prefix B for all beams in phase 2"
- It also reads column schedules and grids from images. Larger changes show a preview before "Run".
- The LLM used is not stated.
- https://discourse.mcneel.com/t/i-built-a-ai-chat-that-lets-me-talk-to-my-tekla-model/223635 (Oct 2026)

**László Keresztesi built TekAssistant AI (2023), an early ChatGPT-based hobby bot.** [Verified; old]
- It has three skills: General Q&A, "Developer" (writes Open API code) and "Colleague" (turns requests into API code and runs it).
- The author admits it answers "sometimes in a somewhat silly way", and that complex tasks need more agents and tuning. It was not released.
- https://www.linkedin.com/pulse/tekassistant-ai-design-weapon-across-open-api-bim-data-keresztesi

**YouTube demos** [Weak: only the titles could be read]
- "Tekla Structures API: Optimizing C# Method with GitHub Copilot vs Claude Coding Showdown". https://www.youtube.com/watch?v=_P3zbVkfRIQ
- "I Let AI Design My Tekla Model… It Actually Worked" (generating a steel frame). https://www.youtube.com/watch?v=p5QUCEmuHKU

**Vitali Mezen's live workshop, "AI in Tekla Structures. Build your own MCP and automate your work"** (22 Apr 2026). [Weak: event listing only]
- https://addcal.co/e/e2dx35ha75hg

## 3. Community MCP servers (chat control of a live model)

| Project | What it does | Tekla versions | Safety / notes |
|---|---|---|---|
| tempalg1n/tekla-mcp-server [Verified] | About 120 tools covering queries, weights grouped by profile/UDA, QA checks, IFC objects, part export, UDA import from file, model edits, drawings (experimental), screenshots, API-doc search, and "policy-checked" C# scripts. Works with Claude, Codex and Cursor. | 2021/2023 tested on live models; 2025/26 used in the field | Writes are preview-only by default (`apply=false`). Changed objects are tagged with an MCP_ORIGIN UDA. There is a read-only mode, and mutating scripts must be approved by hash. Pitfalls: about 60 s client timeout on whole-model scans (use paging); drawing edits are lost unless saved. https://github.com/tempalg1n/tekla-mcp-server |
| teknovizier/tekla_mcp_server [Verified] | Selection, components (e.g. lifting anchors placed from weight and centre of gravity), UDAs, views, drawings. Maps plain terms like "concrete cover" to component properties. | 2022, 2026 | Read-only mode. GPL-3. https://github.com/teknovizier/tekla_mcp_server |
| SherinWorin/sherin-tekla-mcp [Verified] | BOQ/CSV quantity reports, validation, creating beams and columns | 2025 | The AI "never writes or runs code inside Tekla"; it only calls typed C# tools. Read-only by default, with preview plus confirmation token, catalog check of profiles and materials, read-back after writes, and an audit log. v0.1, not yet tested live. https://github.com/SherinWorin/sherin-tekla-mcp |
| YuriyKirillov/TeklaMCPServer [Verified] | 14 tools: filter selection, setting and getting UDAs, labels, inserting components | 2023 only | Its tests modify the real model. Python/pythonnet clr naming conflict. https://glama.ai/mcp/servers/YuriyKirillov/TeklaMCPServer |
| osc-bouw/TeklaMCP, HuVelasco/tekla-mcp [Weak] | PlaceBeam, FilterModel, drawing "management" | 2023+ | Very new and thin; HuVelasco's repo has a single commit. https://github.com/osc-bouw/TeklaMCP, https://github.com/HuVelasco/tekla-mcp |
| pawellisowski tekla-api-mcp (npm) [Verified] | Gives Claude Desktop or Claude Code searchable Tekla Open API docs and examples. Directly targets the hallucinated-method problem. | n/a | https://libraries.io/npm/tekla-api-mcp |
| Vinayak19112003/TeklaMCP [Weak, prototype] | Text, PDF or image → Claude 3.5 / GPT-4 → C# Open API code → model | n/a | Claims 75–90 % accuracy with no data. States that connections and curved geometry need manual review. https://github.com/Vinayak19112003/TeklaMCP/blob/claude/ai-tekla-model-generator-01N46iAnJG1QzeZTZLd8ZbR2/README.md |

## 4. Pitfalls reported across sources

- **Code compiles in the chat but fails in Tekla** (Folkard; the Developer Assistant docs). The fix is an iterate-and-test loop.
- **Invented or wrong API methods.** Nobody documents this with examples, but the existence of doc-grounding tools (tekla-api-mcp, API search in tempalg1n, the Developer Assistant's doc knowledge base) shows it is a real problem. Generic chat models also mix up Tekla versions; pin the target version and check the Open API release notes (https://developer.tekla.com/documentation/tekla-structures-2025-open-api-release-notes).
- **Environment and catalog mismatch.** Profiles that do not exist in your environment cause failures (Developer Assistant docs; Sherin's catalog checks).
- **Destructive edits.** Every serious tool adds preview-and-confirm or read-only modes. Model Assistant can undo only one step.
- **Drawings are the weakest area.** Both Trimble and the MCP projects label drawing edits as limited or experimental.
- **Recorded macros do not capture everything.** https://support.tekla.com/article/not-all-tekla-structures-functionalities-can-be-recorded-as-a-macro-script

## 5. Doporučené postupy / Recommended practices

1. **Work on a copy of the model and start read-only.** Turn on writes only after the queries look right. (Sherin README; tempalg1n README)
2. **Be specific, and select first.** Pre-select objects or name them precisely ("column at C4"), use the correct view or drawing mode, and say what must NOT change. (Model Assistant docs)
3. **Ask for the plan before execution**, e.g. "What exactly are you going to do?". Then approve the preview. (Model Assistant docs; TeklaAIBridge)
4. **Split big jobs into small steps.** For code, build one small function at a time: select, then read, then modify. (Model Assistant docs; Folkard)
5. **Encode company standards once** as rules (`rules.md`: naming, default materials) and skills (`skills.md`: multi-step workflows), so you do not repeat them in every prompt. If the AI repeats an error, add a rule. (Model Assistant docs)
6. **Ground code in the official API.** Name your Tekla version, point the LLM to developer.tekla.com or a docs MCP, and paste in the exact compiler error. Prefer the Default environment. (Developer Assistant docs; tekla-api-mcp)
7. **Use the safety net.** Press Ctrl+Z before retrying, start a new chat if the assistant gets confused, and close open dialogs, since Tekla handles one task at a time. (Model Assistant troubleshooting)
8. **Keep generated macros that work in a shared folder** and reuse them. Model Assistant already checks for an existing macro before writing a new one.

## 6. Starter automation ideas for a non-programmer Tekla user

1. **Model quantity and weight report.** "Group all parts by profile/material/UDA X and sum weight", exported to CSV or Excel. Read-only, so there is zero risk.
2. **Bulk property edits.** Set class, prefix, name or finish on a filtered set ("all HEA300 in phase 2"). The Model Assistant example covers exactly this.
3. **Fill UDAs from Excel.** Have the AI write a short macro, or prepare a tab-delimited file for Tekla's built-in UDA import keyed on GUID or ASSEMBLY_POS (https://support.tekla.com/fi/doc/tekla-structures/2021/int_attributes_importing).
4. **QA checks.** Find parts with no material, wrong class, duplicate positions or default profiles, then select or highlight them for review.
5. **Find and replace profiles** ("HEA200 on grid C → HEA240"), with a preview first.
6. **List and status-check drawings,** e.g. "list issued drawings modified since issue". Read-only.
7. **Small utility macros via the Developer Assistant,** e.g. "list all profiles used in a dialog", or select by name pattern (RHS*). Save the ones that work to the macro catalogue.
8. **Grids and simple layouts from a description or sketch image** (grid plus pad footings, canopy layout), which an engineer then checks.

The safest first step is ideas 1, 4 and 6, which are purely read-only.
