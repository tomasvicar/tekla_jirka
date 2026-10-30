# Tekla Open API: what can be controlled programmatically?

Research date: 2026-10-30. Web research only; nothing was installed or run.

## TL;DR

**No, the API does not control absolutely everything, but it covers most of what matters.** The Tekla Open API (.NET) covers most model work: creating, reading, changing and deleting parts, bolts, welds, components and UDAs, plus selection, reports, IFC4 export and clash checks. It also covers a large and growing part of drawings. What the API cannot reach (some dialog settings, some exports, some drawing editing) can usually be scripted through recorded **Akit macros**. Those are plain `.cs` files that Tekla runs itself, which makes them the easiest path for Claude to write.

Hard constraints:
- Windows only.
- A licensed Tekla Structures instance must be running with a model open.
- The API version must match the Tekla version.
- x64 only.

## 1. Namespaces / assemblies and their scope

The official assembly list is at https://developer.tekla.com/documentation/tekla-open-api-assemblies. That page is dated 2019 but still matches the structure.

- **Tekla.Structures.Model.** Model objects such as Beam, ContourPlate, BoltArray, Load and Component. Operations such as copy, move, combine and split. Enumeration, picking and view selection, analysis results, and **clash checking**. The `Model.UI` namespace (selection, model views, temporary graphics) ships in the same DLL.
- **Tekla.Structures.Model.Operations.** The `Operation` class provides:
  - `RunMacro` (https://developer.tekla.com/doc/tekla-structures/2026/run-macro-method-73267)
  - `CreateReportFromAll` (https://developer.tekla.com/doc/tekla-structures/2026/create-report-all-method-73239)
  - `CreateIFC4ExportFromAll` (https://developer.tekla.com/doc/tekla-structures/2026/create-ifc4-export-all-method-string-operation-ifc-export-view-type-enum-operation-ifc-export-version-enum-i-enumerable-string-i-enumerable-string-73224)
  - Numbering checks such as `IsNumberingUpToDate` and `GetSimilarNumberedObjects`, plus MIS export enums and a progress bar (https://developer.tekla.com/doc/tekla-structures/2026/tekla-structures-model-operations-73185).
  - Searches did not confirm a dedicated "run full numbering" method. Numbering is commonly triggered through a macro.
  - `CreateNCFilesFromSelected` exists. Since 2026 it returns false when numbering is out of date (https://developer.tekla.com/documentation/tekla-structures-2026-open-api-release-notes).
- **Tekla.Structures.Drawing.** Drawing, View, Part, Text and Line objects, with enumeration, modification and selection in drawing views. It grows every release: 2025 added part and neighbour line properties, and 2026 added text resize behaviour, rich-text detection, cloud arcs and `RectangularCloud`. Since 2026, "Modifying text using Tekla Open API now works in the same way as … the user interface." Sources: https://developer.tekla.com/documentation/tekla-structures-2025-open-api-release-notes and https://developer.tekla.com/documentation/tekla-structures-2026-open-api-release-notes.
- **Catalogs.** Profiles, bolts, materials, rebars, meshes and printers.
- **Dialog / Plugins.** Plug-in UIs and components (`PluginBase`, `ConnectionBase`, `DrawingPluginBase`).
- **Analysis.** Analysis and design data.
- **Datatype.** Unit types.
- **CustomPropertyPlugin.** Custom template properties for reports and drawings.
- **Geometry3d / Solid.** Shipped in `Tekla.Structures.dll` and Model. Not separately documented on the assembly page.

The official C# examples are at https://github.com/TrimbleSolutionsCorporation/TSOpenAPIExamples (one branch per Tekla version) and https://developer.tekla.com/tekla-structures/documentation/model-code-examples. Trimble's GitHub also has **HeadlessTeklaStructuresExample**, which works with a model without the UI (https://github.com/TrimbleSolutionsCorporation).

## 2. Can do / partially / cannot

| Area | Status | Notes / source |
|---|---|---|
| Create, modify, delete parts, plates, bolts, welds, rebars, loads | **Can do** | Assemblies page; model code examples |
| Insert system or custom components and set their attributes | **Can do** | `Component` class; community MCP servers do this (https://github.com/teknovizier/tekla_mcp_server) |
| Read and write UDAs and report properties | **Can do** | Used widely; sherin and tempalg1n MCP servers |
| Selection, highlighting, temporary graphics, model views | **Can do** | Model.UI (assemblies page) |
| Clash check | **Can do** | Assemblies page |
| Reports from templates | **Can do** | `CreateReportFromAll` (the template must exist) |
| IFC4 export | **Can do** | `CreateIFC4ExportFromAll` (signature changed in 2026) |
| NC/DSTV files | **Can do** | `CreateNCFilesFromSelected` (needs numbering up to date) |
| Numbering | **Partially** | Status queries via the API; running numbering is typically done with a macro |
| Drawings: create, open, enumerate, modify views, marks, dimensions, texts | **Partially** | Large API, but some items such as main-part centre lines needed workarounds (https://support.tekla.com/article/not-all-tekla-structures-functionalities-can-be-recorded-as-a-macro-script). Community MCP servers call their drawing layer "experimental" (https://github.com/tempalg1n/tekla-mcp-server/blob/main/README.md) |
| Drawing printing / PDF | **Partially** | Possible via API or macro. Disabled on Trial licences (https://support.tekla.com/doc/tekla-structures/2026/ts_configurations) |
| Settings dialogs, options, and features without API classes | **Via macro only** | Akit macros replay UI commands (dialog value changes, button presses). Not every action can be recorded (support article above) |
| Arbitrary UI actions, new Tekla Model Assistant / AI features | **Cannot / unclear** | No API mentioned in the 2026 Open API release notes |
| Running without Tekla open | **Cannot** (except the special headless service) | https://developer.tekla.com/documentation/check-connection-between-application-and-tekla-structures |
| Reconnecting after Tekla restarts | **Cannot** in-process | "Currently, there's no way to re-establish the connection" (https://developer.tekla.com/doc/tekla-structures/2026/get-connection-status-method-71952) |

## 3. Technical requirements

- **Running instance.** Tekla must be running with a model open. Apps "cannot expect to have Tekla Structures running upon execution" and should check `GetConnectionStatus()`. Source: https://developer.tekla.com/documentation/check-connection-between-application-and-tekla-structures
- **Version matching.** "Tekla Open API 2024 applications will connect with the Tekla Structures 2024 process." Since 2024 the assemblies are no longer in the GAC. External exe files need a correct `exe.config`, created with the `TSAppConfigPatcherTask` NuGet package and `Directory.Build.Props`, or apps can be placed in the version-specific Extensions folder (same source).
- **.NET by version:**
  - **2023 and older:** .NET Framework (with COM and GAC).
  - **2024:** "built using .NET Framework 4.8", .NET Standard 2.0 compatible, COM removed, and ".NET 6, 7, and 8 are not yet supported to compile tools" (https://developer.tekla.com/documentation/tekla-structures-2024-open-api-release-notes).
  - **2025:** The release notes say nothing about .NET 8. The binary-compatibility break is in the RPC layer, and source compatibility is kept.
  - **2026:** NuGet `Tekla.Structures.CommonObjects` 2026.0.3 explicitly targets **net48 and net8.0-windows** (https://packages.nuget.org/packages/Tekla.Structures.CommonObjects/). `Tekla.Structures.Model` ships only **netstandard2.0** (https://www.nuget.org/packages/Tekla.Structures.Model). Tekla 2026 moved some assemblies into a `Net48Runtime/` subfolder (https://github.com/Modeling13Steel/Tekla-Nest).
  - **Conclusion:** .NET Framework 4.8 is the safe target for 2024–2026. Treat .NET 8 as emerging and not officially documented. Community MCP servers still target net48 x64 (https://github.com/SherinWorin/sherin-tekla-mcp).
- **x64.** "Extensions that use Tekla Open API now support only 64-bit platforms" (2026 release notes).
- **NuGet.** Official packages are owned by `buildmaster_Tekla` and Trimble, with versions 2021 through 2026.0.3. Avoid the third-party `Tekla.Structures.All` package (https://www.nuget.org/packages/tekla.structures.all).

## 4. The macro system (best path for a non-programmer)

- Macros are C# `.cs` files. Recorded or newly created macros go to `<model>\macros\modeling` or `<model>\macros\drawings`. Shared macros go to the folder named by `XS_MACRO_DIRECTORY`, by default `..\ProgramData\Trimble\Tekla Structures\<version>\environments\common\macros`, and up to two folders can be listed separated by `;`. Sources: https://support.tekla.com/doc/tekla-structures/2026/det_recording_editing_and_running_macros and https://support.tekla.com/doc/tekla-structures/2026/xs_macro_directory
- **To run a macro,** open Applications & components, expand Applications and double-click the macro. Macros can also be recorded there and edited in any text editor (same page). From code, use `Operation.RunMacro("name.cs")`, or `..\drawings\X.cs` for a drawing macro. It throws an exception if the file is missing (RunMacro page).
- **Structure.** A macro is `namespace Tekla.Technology.Akit.UserScript { public class Script { public static void Run(Tekla.Technology.Akit.IScript akit) {...} } }`. It can mix recorded `akit` UI commands with full Open API calls, for example `DrawingHandler`, modifying parts and `CommitChanges()` (https://support.tekla.com/article/not-all-tekla-structures-functionalities-can-be-recorded-as-a-macro-script).
- **Why it matters.** No Visual Studio, no build step and no version-matched exe are needed. Claude writes the `.cs` file into the macros folder and the user double-clicks it. The trade-off is weak error feedback.

## 5. Python via pythonnet

It works in principle, because the Open API is plain .NET and Python can load .NET assemblies. There is no official Tekla Python support or example.
- **pyTekla** is a "thin wrapper around the Tekla Open API" used by VIKTOR. It needs Windows, Python ≤ 3.11, and an open model, and it is configured with `set_tekla_path("C:/Program Files/Tekla Structures/2023.0/bin")` (https://docs.viktor.ai/docs/create-apps/software-integrations/tekla/).
- **Tekla-Nest** has a pythonnet/CLR bridge "tested with Tekla 2021–2026" and handles the 2026 `Net48Runtime` folder (https://github.com/Modeling13Steel/Tekla-Nest).
- **HuVelasco/tekla-mcp** uses a Python FastMCP server with a C# bridge (https://github.com/HuVelasco/tekla-mcp).
- **Note (my inference, not from Tekla docs):** pythonnet 3.x has to load the .NET Framework runtime (`netfx`) to match Tekla's net48 assemblies, and the 2024+ app.config/assembly-binding requirement makes this fragile.

## 6. Licensing

- "You need a Tekla Structures license to develop with the Tekla Open API". The routes are a Partners Program Suite licence, Tekla Campus (free for students), or a 30-day trial (https://developer.tekla.com/documentation/get-started-tekla-structures-open-api).
- In the 2026 subscription tiers, **Open API capabilities are ✔ in Diamond, Graphite, Carbon and Trial**. The tier still limits which features exist. Graphite has no steel or precast assembly numbering. Carbon and Trial have no production drawings. Trial cannot print or export drawings (https://support.tekla.com/doc/tekla-structures/2026/ts_configurations).
- The **Partner** configuration is for development only and may not be used commercially for modeling or detailing. Selling apps requires the Tekla Partners Program (https://www.tekla.com/in/solutions/design-interoperability/open-api).
- No statement was found that restricts Open API use on educational licences. Older "Primary/LT" configurations no longer exist under the 2026 tier names, and this was not verified for perpetual licences.

## 7. Doporučené postupy / Recommended practices

- **Start read-only, then allow writes behind preview and confirm.** Both active MCP projects default to read-only. sherin uses a `confirmToken`. tempalg1n uses `apply=false` plans, and mutating scripts run only if their SHA-256 matches the user-approved source (https://github.com/SherinWorin/sherin-tekla-mcp, https://github.com/tempalg1n/tekla-mcp-server/blob/main/README.md).
- **Work on a copy of the model.** Log every change. Tag created objects with a UDA, for example `MCP_ORIGIN`, so they can be traced and undone with Ctrl+Z (same sources).
- **Read back after every write.** tempalg1n found "part edits accepted by Tekla but never stored", and numeric UDAs read as blank on 2021 (tempalg1n README).
- **Always call `CommitChanges()`, and save drawings explicitly.** Tekla drops unsaved drawing edits when the model is reopened (tempalg1n README).
- **Check the connection and the model path first.** Use `GetConnectionStatus()` and pass the expected model path, because several running Tekla instances can confuse the target. Page large model scans to stay under the MCP client's ~60 s timeout (tempalg1n README).
- **Pin the Tekla version.** Use NuGet packages of the exact Tekla major version, net48 and x64, and the Extensions folder or `TSAppConfigPatcherTask` (connection page). Expect signature changes between versions, such as the IFC4 export in 2026.
- **Give Claude documentation.** The `tekla-api-mcp` npm package exposes Open API docs to Claude Code and Claude Desktop (https://libraries.io/npm/tekla-api-mcp). Point Claude to the version-specific API reference and the TSOpenAPIExamples branch.
- **Use recorded macros as templates.** For UI-only features, record the action in Tekla, then have Claude generalise the recorded `.cs` file.
- **Existing MCP servers to evaluate before building your own:**
  - https://github.com/tempalg1n/tekla-mcp-server (120 tools, 2021–2026, most mature)
  - https://github.com/teknovizier/tekla_mcp_server (2022 and 2026, GPLv3)
  - https://github.com/osc-bouw/TeklaMCP (2023+)
  - https://github.com/SherinWorin/sherin-tekla-mcp (2025, v0.1, live Tekla not yet tested)
