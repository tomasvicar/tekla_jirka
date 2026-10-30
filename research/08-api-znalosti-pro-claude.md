# 08 – Giving Claude accurate Tekla Open API knowledge

*Research date: 2026-10-30. Claims are sourced. Items marked **[unverified]** were not confirmed against a primary source.*

## 1. Where the API reference lives

- **Online reference (versioned, public, can be fetched):** class pages follow the pattern `developer.tekla.com/doc/tekla-structures/<year>/<slug>-<id>`, e.g. the [Beam class 2025](https://developer.tekla.com/doc/tekla-structures/2025/beam-class-51968) and [Beam class 2024](https://developer.tekla.com/doc/tekla-structures/2024/beam-class-26874). The 2026 root is `/doc/tekla-structures/2026/tekla-structures-64304`. WebFetch read the Beam page without problems, including constructors, members and an example. The IDs in the URLs are opaque, so Claude has to search for a page (or follow links to it) rather than guess its URL.
- **Older versions:** the reference page links to a [Tekla Warehouse item with older API references](https://warehouse.tekla.com/#/catalog/details/u97eeed98-e862-467b-a6f7-9b60588fadae). The format (CHM or another) is **[unverified]**.
- **Guides:** [How Tekla Open API works](https://developer.tekla.com/documentation/how-tekla-open-api-works) explains the common Select/Insert/Modify/Delete pattern. [Macros (.cs)](https://developer.tekla.com/documentation/macros-cs) says macros are .cs files in `XS_MACRO_DIRECTORY` that Tekla compiles at run time. [Update macros for WPF dialogs](https://developer.tekla.com/documentation/update-macros-work-wpf-based-dialogs) shows the old macro form (`Tekla.Technology.Akit.UserScript.Script.Run(IScript akit)`) and the new one (`#pragma reference "Tekla.Macros.Runtime"`, `[MacroEntryPointAttribute]`, `Run(IMacroRuntime runtime)`).
- **llms.txt:** `developer.tekla.com/llms.txt` returned HTTP 403 when fetched. No llms.txt was found.
- **XML doc files in NuGet (best offline source):** I downloaded `Tekla.Structures.Model` 2026.0.3 and confirmed that it ships `lib/netstandard2.0/Tekla.Structures.Model.xml` (2.8 MB, about 9,160 documented members) next to the DLL. `Tekla.Structures` ships XML docs for both net48 and netstandard2.0 ([NuGet package](https://www.nuget.org/packages/Tekla.Structures.Model/)). The current version is 2026.0.3. Other packages from the same publisher: Drawing, Dialog, Plugins, Catalogs, Datatype, Analysis and `Tekla.Structures.All`. Older releases (2025.0.0 and 2024.0.x) are also listed on the [NuGet versions list](https://www.nuget.org/packages/Tekla.Structures.Model/).
- **Context7 (MCP docs index):** two Tekla libraries exist. [`/websites/developer_tekla_doc_tekla-structures_2025`](https://context7.com/websites/developer_tekla_doc_tekla-structures_2025) has about 30,856 snippets and 4M tokens and covers the Model, Drawing, Geometry3d and Catalogs namespaces. [The 2026 entry](https://context7.com/websites/developer_tekla_doc_tekla-structures_2026_tekla-structures-64304) has only 22 snippets, so it is close to useless. The examples repo is indexed as [`/trimblesolutionscorporation/tsopenapiexamples`](https://context7.com/trimblesolutionscorporation/tsopenapiexamples) (305 snippets).
- **DeepWiki:** the page for TSOpenAPIExamples returned HTTP 429 when fetched, so whether it exists is **[unverified]**.
- **Tekla's own AI:** the [Developer Assistant](https://support.tekla.com/doc/tekla-structures/not-version-specific/developer_assistant) runs in the Trimble Assistant side pane and generates and runs Open API macros. It requires a Diamond or Partners named-user license and is a preview in 2025. If Jirka has access, it is useful for cross-checking Claude's output.

## 2. Sample code and community

- **Official examples:** [TSOpenAPIExamples](https://github.com/TrimbleSolutionsCorporation/TSOpenAPIExamples) (BSD-3) has **one branch per version, 2016 to 2026**, and was last pushed on 2026-10-05. The 2026 branch holds Model and Drawing applications and plug-ins (BeamApplication, Rebar, CNC, ClashCheck, DimensionCreator, and others). Its csprojs are SDK-style, `net48`, `x64`, with `PackageReference Tekla.Structures.* 2026.0.3` ([BeamApplication.csproj](https://github.com/TrimbleSolutionsCorporation/TSOpenAPIExamples/blob/2026/Model/Applications/BeamApplication/BeamApplication.csproj)).
- **Other repos in the [same GitHub organization](https://github.com/TrimbleSolutionsCorporation):** TSOpenAPISelfLearningExercises, TeklaApplicationLibrary (helper classes), HeadlessTeklaStructuresExample, TSDirectManipulationPluginsExample and StructuresDeveloperKitExamples.
- **Community:** [Tekla Developer Forums, Open API section](https://forum.tekla.com/forum/268-tekla-structures-developer-forums/), monitored by Tekla support ([developer community](https://developer.tekla.com/tekla-developer-community)). Also [Dynamic-Tekla-Structures-API](https://github.com/dawiddyrcz/Dynamic-Tekla-Structures-API) and the `TeklaOpenApiExtensionMethods` NuGet package (quality **[unverified]**).
- **MCP servers that drive Tekla directly (not docs):** [teknovizier/tekla_mcp_server](https://github.com/teknovizier/tekla_mcp_server) (Python, GPL-3, tested with 2022 and 2026), [tempalg1n/tekla-mcp-server](https://github.com/tempalg1n/tekla-mcp-server/releases/tag/v0.1.1) (early, 2023) and [YuriyKirillov/TeklaMCPServer](https://glama.ai/mcp/servers/YuriyKirillov/TeklaMCPServer/tree) (pythonnet).

## 3. Existing Claude/AI configurations

- I found **no public CLAUDE.md, Claude skill, Cursor rules or Copilot instructions specific to Tekla** (searches returned nothing). Treat this as a gap the project has to fill.
- Generic .NET skills: [Aaronontheweb/dotnet-skills](https://github.com/Aaronontheweb/dotnet-skills) (1.2k stars, active) includes an `ilspy-decompile` skill. Similar skills are listed on [nikiforovall's ilspy-decompile page](https://nikiforovall.blog/claude-code-rules/component-reference/skills/ilspy-decompile) and [Smithery's csharp-decompile page](https://smithery.ai/skills/j-r-beckett/csharp-decompile).

## 4. Verification techniques

1. **Ground truth from the XML docs.** Restore the NuGet package for the user's exact Tekla version, then have Claude `grep` the `.xml` for `M:Tekla.Structures.Model.Beam.` before using a member. This is cheap and offline.
2. **DLL inspection:** `ilspycmd -l c <dll>` and `ilspycmd -t <Type> <dll>` give the real signatures ([skill write-up](https://nikiforovall.blog/claude-code-rules/component-reference/skills/ilspy-decompile)). Flags differ between sources, so check them with `ilspycmd -h`. Alternatively, a small PowerShell reflection script that runs `[Reflection.Assembly]::LoadFrom(...).GetTypes()` against the DLLs in the Tekla install folder **[unverified for Tekla]**.
3. **Compile loop:** a template SDK-style project (`net48`, `x64`, `Tekla.Structures.Model` at the version matching the installed Tekla), then `dotnet build` after every change and feed the errors back to Claude. This catches every invented method. Pattern from the [official csproj](https://github.com/TrimbleSolutionsCorporation/TSOpenAPIExamples/blob/2026/Model/Applications/BeamApplication/BeamApplication.csproj).
4. **Macros:** they are compiled by Tekla at run time ([source](https://developer.tekla.com/documentation/macros-cs)), so `dotnet build` does not cover them directly. Workaround: keep the macro body in a class that also compiles in the test project **[my suggestion]**.
5. **Run safely:** test on a copy of the model, check `new Model().GetConnectionStatus()` first, and call `CommitChanges()` only at the end **[common practice, unverified source]**.

## 5. Proposed setup

```
tekla-projekty/
  CLAUDE.md
  .mcp.json                      # context7 (optional)
  .claude/skills/
    tekla-api/SKILL.md           # how to look up and verify the API
    tekla-macro/SKILL.md         # macro template + deployment to XS_MACRO_DIRECTORY
    tekla-app/SKILL.md           # standalone .exe template + build
  templates/MacroTemplate.cs, AppTemplate/AppTemplate.csproj
  reference/                     # restored Tekla.*.xml, examples clone (branch = version)
  scripts/find-api.ps1           # grep XML docs for a member
```

**CLAUDE.md outline:**
1. User profile: not a programmer. Explain things in Czech, give step-by-step instructions to run the result, and never assume Visual Studio knowledge.
2. Environment: Tekla Structures **version X**, NuGet version `X.0.n`, net48 x64, macro folder path.
3. Hard rules: never use an API member that was not verified in `reference/*.xml`, the examples or the developer.tekla.com page for the matching version. Say "not verified" when unsure. Run `dotnet build` before handing over code. No destructive operations without confirmation.
4. Lookup order: local XML docs → examples branch → Context7 2025 library → WebFetch of developer.tekla.com (`/doc/tekla-structures/<year>/`) → forum.
5. Code conventions: `Model.GetConnectionStatus()`, `ModelObjectSelector` / `Picker`, `CommitChanges()`, try/catch with a message to the user, and units in mm.
6. Testing protocol: copy of the model, a small selection first, then the full run.

**Skill `tekla-api`:** verification procedure (grep XML, ilspy, build), common pitfalls (version mismatch, `Insert()` without `CommitChanges()`, `Select()` without an Identifier).
**Skill `tekla-macro`:** both entry-point skeletons, where to copy the file, how to run it from the Applications & components catalog.

## Recommended practices

- **Pin the version everywhere.** The API reference, the examples and NuGet are all per version, so mixing versions is the main source of wrong code ([examples branches](https://github.com/TrimbleSolutionsCorporation/TSOpenAPIExamples), [NuGet](https://www.nuget.org/packages/Tekla.Structures.Model/)).
- **Start from an official example** close to the task instead of writing from scratch ([get code examples](https://developer.tekla.com/documentation/get-code-examples)).
- **Use the shipped XML docs as the source of truth.** Use Context7 only for the 2025 library, since the 2026 index is nearly empty.
- **Compile before you run.** Treat a clean `dotnet build` as the minimum bar for handing code over **[my recommendation]**.
- **Test on a model copy.** Use the Default environment when comparing with the Developer Assistant ([Tekla docs](https://support.tekla.com/doc/tekla-structures/not-version-specific/developer_assistant)).
- **Ask on the forum** when the API behaves unexpectedly. Tekla support monitors it ([developer community](https://developer.tekla.com/tekla-developer-community)).
