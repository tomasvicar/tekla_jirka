# Automating Tekla Structures with Claude Code without MCP: the options

*Research date: 2026-10-30. Audience: a Tekla user who does not program and wants Claude Code to write and run the automation.*

Ground rule: Tekla Structures runs only on Windows. Every route that talks to a running model (C# macros, standalone apps, pythonnet, Grasshopper) needs Claude Code on the same Windows PC as Tekla, with Tekla running and a model open ([connection check docs](https://developer.tekla.com/documentation/check-connection-between-application-and-tekla-structures)). Offline routes (reports, IFC, Excel) work on any machine.

## 1. C# macros (.cs files) — the best first route

- **What they are:** plain `.cs` text files that Tekla compiles and runs itself, so no Visual Studio or .NET SDK is needed. A modeling macro goes in `<model>\macros\modeling\` and a drawing macro in `<model>\macros\drawings\`. Tekla creates both folders automatically. Macros shared across models go in the folders set by `XS_MACRO_DIRECTORY` (default `C:\ProgramData\Trimble\Tekla Structures\<version>\environments\common\macros\modeling|drawings`). Tekla reads the model folder first ([macro docs 2026](https://support.tekla.com/doc/tekla-structures/2026/det_recording_editing_and_running_macros), [RunMacro API](https://developer.tekla.com/doc/tekla-structures/2026/run-macro-method-73267)).
- **How to run:** Applications & components → Applications → double-click. A new file may only show up after *Catalog management → Reload catalog*. Tekla's docs say a macro "can be opened in any text editor", so Claude Code can write it straight into the folder.
- **Two styles:**
  - *Recorded UI macros* (`akit.Callback(...)`, `akit.ValueChange(...)`) replay clicks in dialogs. You can record one in Tekla and then have Claude generalize it.
  - *Open API macros* use `Tekla.Structures.Model` (select objects, change UDAs, create parts). Extra DLLs are referenced with `#pragma reference "..."`. The older `XS_MACRO_REFERENCES` option is obsolete ([xs_macro_references](https://support.tekla.com/doc/tekla-structures/2022/xs_macro_references)).
- **Compile errors:** the docs do not describe how compile errors are reported. In practice Tekla shows an error message when you run the macro, and the session log is under `%LOCALAPPDATA%\Trimble\Tekla Structures\<ver>\Logs` (2026) or the model's `\logs` folder (older versions) ([log files](https://support.tekla.com/doc/tekla-structures/2026/sys_log_files)). Claude cannot see that error dialog. The user has to paste the error back, or Claude reads the log file. *Untested — check on your machine.*
- **Examples:** [TSOpenAPIExamples](https://github.com/TrimbleSolutionsCorporation/TSOpenAPIExamples) (official, one branch per Tekla version, includes macros), [Model code examples](https://developer.tekla.com/documentation/model-code-examples), [Introduction to Tekla macros API](https://developer.tekla.com/documentation/download-introduction-tekla-macros-api), [macros and WPF dialogs](https://developer.tekla.com/documentation/update-macros-work-wpf-based-dialogs), and a community example: [Show Assemblies From Assembly Drawings](https://github.com/benkoshy/TeklaPlugin---Show-Assemblies-From-Assembly-Drawings).
- **Official alternative:** Trimble's **Developer Assistant** (an AI side pane in Tekla, installed by default since 2025 SP5) generates macros, runs them and saves them. It needs a Diamond or Partners license, or the Trimble Labs program ([Developer Assistant](https://support.tekla.com/doc/tekla-structures/not-version-specific/developer_assistant)). Its loop is: prompt, run, read the error log, refine. That is the same loop to copy with Claude Code.

## 2. Standalone C# apps (console/WinForms) with NuGet

- `dotnet new console`, then `dotnet add package Tekla.Structures.Model --version <your Tekla version>`, then `dotnet build`, then run the `.exe` while Tekla is running. The NuGet package version must match the installed Tekla version (2023.0.x, 2024.0.x, 2025.0.0, 2026.0.3…). The current packages target `netstandard2.0`, and NuGet reports them as compatible with net48 and net6/8 ([NuGet Tekla.Structures.Model](https://www.nuget.org/packages/Tekla.Structures.Model/)). Tekla's own examples target .NET Framework 4.8 (`net48`). For a non-programmer, net48 is the safest target. *Check the right target framework in the [Developer Center](https://developer.tekla.com/tekla-structures) release notes for your version.*
- **Prerequisites:** .NET SDK (dotnet CLI), .NET Framework 4.8 Developer Pack, and a matching Tekla version.
- **Pros:** Claude sees compile errors directly in the terminal and can fix them on its own, and the app can have its own GUI. **Cons:** more setup, and the build has to be redone when Tekla is upgraded. The unofficial [Dynamic Tekla Structures API](https://github.com/dawiddyrcz/Dynamic-Tekla-Structures-API) avoids being tied to one version.

## 3. Python via pythonnet

- pythonnet (`import clr; clr.AddReference(r"C:\Program Files\Tekla Structures\<ver>\bin\Tekla.Structures.Model.dll")`) can load the Tekla API. **[PyTekla](https://github.com/efdiloreto/pytekla)** ([docs](https://efdiloreto.github.io/PyTekla/)) is a thin wrapper on top of it. VIKTOR uses pyTekla in production (Python ≤ 3.11, `set_tekla_path(".../bin")`) ([VIKTOR Tekla integration](https://docs.viktor.ai/docs/create-apps/software-integrations/tekla/)).
- **Viability:** it works, but there are few examples, it depends on the Python version, and PyTekla is not clearly maintained. It is attractive when the user's real goal is pandas/Excel processing. For writing to the model, a C# macro is more robust.

## 4. Grasshopper–Tekla Live Link (Rhino)

- Free Tekla Warehouse extension. It works with Rhino 6/7/8; Rhino 8 must be switched with `SetDotNetRuntime` → NETFramework. Install the link built for your exact Tekla version. Start Tekla and the model first, then Rhino ([Live Link](https://support.tekla.com/help/tekla-structures/not-version-specific/grasshopperteklalink), [FAQ](https://support.tekla.com/help/tekla-structures/not-version-specific/grasshopperteklalink-faq), [McNeel forum](https://discourse.mcneel.com/c/grasshopper/tekla/155)).
- This is the visual route for parametric geometry, renumbering and setting UDAs from Excel ([BIM Corner – 4 scripts](https://bimcorner.com/4-ready-to-use-grasshopper-scripts-to-automate-tekla-structures/)). It needs a Rhino license. Claude helps less here because .gh files are binary; it can only write C#/Python script components.

## 5. Built-in Tekla tools that need no code

- **Report templates (.rpt):** textual `.rpt` files are plain text, so Claude can draft them or modify existing ones (best by copying a system template). Since 2026 there are `.xlsx.rpt` templates paired with an `.xltx` file ([create a template](https://support.tekla.com/doc/tekla-structures/2026/rep_creating_template), [tips](https://support.tekla.com/doc/tekla-structures/2025/rep_tips_for_templates_and_reports), [2026 changes](https://support.tekla.com/pt-pt/doc/tekla-structures/2026/rel_tpl_changes_in_template_editor_and_templates)). The grammar is not formally documented, so Claude should work from real example files.
- **Organizer:** categories export to XML, and property values export to Excel through templates in `ProjectOrganizerData\ExcelTemplates` ([Organizer export](https://support.tekla.com/doc/tekla-structures/2026/mod_exporting_object_properties_from_object_browser)).
- **Tekla Warehouse extensions and custom components:** check whether a solution already exists before writing code. Custom components are built interactively in the GUI, so Claude can only advise.
- **Where Claude helps most:** Python/pandas processing of exported reports (CSV/XLSX): merging, checks, summaries, BOMs.

## 6. Offline file processing

- **IFC + [ifcopenshell](https://thinkmoult.com/using-ifcopenshell-parse-ifc-files-python.html):** checks, quantities, comparing revisions. Tekla can export assemblies and base quantities ([IFC export](https://support.tekla.com/doc/tekla-structures/2023/int_exporting_into_ifc), [property sets](https://support.tekla.com/pt-pt/doc/tekla-structures/2023/int_property_sets_in_ifc_export)).
- **CSV/XSR reports, DWG/PDF drawings:** PDF via pypdf/pdfplumber (title blocks, revision lists), DWG via ezdxf after converting to DXF.
- **[Trimble Connect API](https://developer.trimble.com/docs/connect):** REST with OAuth, file upload and download. It requires a license and technical knowledge ([help](https://help.trimble.com/en/trimble-connect/trimble-connect/welcome-to-trimble-connect/trimble-connect-api-documentation-resources)). It is a later step.
- **Pros:** zero risk to the model, works on any OS, easy to test. **Con:** read-only.

## 7. GUI automation (computer use, AutoHotkey)

- Claude computer use clicks through the screen. AutoHotkey or pywinauto run scripted clicks.
- **Pros:** works with anything, including dialogs that have no API. **Cons:** fragile (resolution, dialog layout, language version), slow, and it can click something destructive. Use it only as a last resort, and only on a copy of the model. A recorded akit macro does the same job more reliably.

## Comparison

| Route | Setup effort | Power | Risk to model | Fit for a non-programmer |
|---|---|---|---|---|
| C# macro in the macros folder | Low (text file) | High (full API + UI) | Medium | ★★★★ best start |
| Standalone C# app (NuGet) | Medium–high (SDK, versions) | Highest | Medium | ★★★ (Claude debugs alone) |
| Python + pythonnet/PyTekla | Medium | High | Medium | ★★ (few examples) |
| Grasshopper Live Link | Medium (Rhino license) | High for geometry | Medium | ★★★ visual, less help from Claude |
| Report templates / Organizer | Low | Medium (read-only) | None | ★★★★★ |
| Offline (IFC, CSV, PDF) + Python | Low | Medium (read-only) | None | ★★★★★ |
| Trimble Connect API | Medium–high (OAuth) | Medium | Low | ★★ |
| GUI automation | Low to start, high to maintain | Universal | High | ★ last resort |

## Recommended workflow

1. Start read-only: Tekla report or IFC export, then a Python script from Claude, then an Excel output.
2. Then simple macros: list or select objects, show a MessageBox. Only then macros that modify the model, always on a **copy of the model**.
3. Loop: Claude writes the `.cs`, the user runs it, the user pastes the error or Claude reads the log, Claude fixes it.
4. Once a tool proves useful, move it into a shared `XS_MACRO_DIRECTORY` or a standalone app.

**Folder structure** (git repo):
```
tekla-automation/
  CLAUDE.md
  macros/modeling/   macros/drawings/   # source; a script copies them to Tekla
  reports/templates/                     # .rpt
  python/            # report/IFC processing
  samples/           # sample exports (CSV, IFC), anonymized
  docs/api-notes.md  # API excerpts that have been verified
```

**What to put in CLAUDE.md:**
- Tekla version (e.g. 2025 SP x), language, environment, Windows paths: model, `macros\modeling`, `XS_MACRO_DIRECTORY`, Tekla `bin`, logs.
- Links: the API reference for the matching version (`developer.tekla.com/doc/tekla-structures/<ver>/...`), TSOpenAPIExamples on the matching branch.
- Rules: "the user is not a programmer, explain in plain language"; "never change the model without asking — and only in the test model"; "do not invent API methods, check them against the docs for version X"; "every macro starts by checking `GetConnectionStatus()`, reports what it did, and wraps changes in `CommitChanges()`"; "after every change, describe how to run it and what to paste back if it fails".
- The macro template that works on the user's machine (proven `using` and `#pragma reference` lines).

## Recommended practices

- **Version-pinned docs instead of memory:** LLMs invent API members. Restrict Claude to the supplied docs or examples and check every call against them ([Anthropic: reduce hallucinations](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations); developer experience with C# interop: [lemmy.world](https://lemmy.world/comment/24465058)). In the repo, keep a working example from TSOpenAPIExamples for the exact version.
- **Iterate in small steps:** describe the outcome clearly, run it, send back the error log, and refine. This is the loop Trimble's own Developer Assistant recommends ([Developer Assistant](https://support.tekla.com/doc/tekla-structures/not-version-specific/developer_assistant)). It also recommends the Default environment, because profiles from other environments trip up generated code.
- **Plan mode for unclear tasks, direct requests for small ones;** keep CLAUDE.md short and add rules to it only after real mistakes ([Claude Code best practices](https://code.claude.com/docs/en/best-practices)).
- **Git as an "undo" button:** commit after every working step so a broken version is one command away from being reverted ([OpenHands guide](https://www.openhands.dev/blog/claude-code-best-practices-agentic-coding), [DataCamp](https://www.datacamp.com/tutorial/claude-code-best-practices)).
- **Mistakes to avoid:** testing on a production model; a NuGet or DLL version that does not match Tekla; a Grasshopper link for the wrong Tekla version, or Tekla running twice ([forum](https://discourse.mcneel.com/t/ive-lost-the-tekla2025-tab-in-grasshopper/218344)); running Rhino as administrator ([forum](https://discourse.mcneel.com/t/tekla-live-link-can-t-connect/214785)); trusting generated code without a test.
- **Inspiration:** a workshop on moving from Grasshopper to Python, Tekla macros and "vibe coding" ([Tiit Bürkland, 05/2026](https://addcal.co/e/rng9338k07te)).

## Gaps in this research

- No official Tekla source describes how macro compile errors are shown.
- No up-to-date tutorial showing pythonnet alone (without PyTekla) was found.
- The exact target framework for 2026 (net48 vs net8) needs to be checked in the Developer Center release notes.
