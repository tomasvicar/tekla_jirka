# 11 – Automation ideas for a Tekla Structures user (steel / precast / concrete)

*Research date: 2026-10-30. Web research only, nothing installed. Claims marked **[unverified]** were not confirmed by a primary source.*

## 1. What detailers lose time on

There is no public time study per task. Practitioner and vendor sources point to the same few pain points:

- **Many small repeated actions, not one big bottleneck.** These include repeated drawing operations, retyping data that already exists in the model, recreating objects, and predictable checks ([FabIntelTech](https://fabinteltech.com/blog/tekla-workflow-productivity)).
- **Drawing quality.** Common problems are overlapping dimensions and marks, outdated templates and missing views. Practitioners advise checking drawings before every issue ([LinkedIn advice thread](https://www.linkedin.com/advice/0/what-most-common-challenges-errors-you-encounter)). One forum estimate says over 80% of manual input goes into GA and erection drawings, but it is one person's opinion and it is about Advance Steel, not Tekla **[unverified]** ([Autodesk forum](https://forums.autodesk.com/t5/advance-steel-forum/moving-from-tekla-to-advance-steel/td-p/6228244/page/3)).
- **Numbering discipline.** Tekla warns about overlapping position numbers, and objects in an overlapping series are not numbered at all. Out-of-date numbers show as "?" ([Tekla numbering tips](https://support.tekla.com/doc/tekla-structures/2025/mod_numbering_tips), [what is numbering](https://support.tekla.com/doc/tekla-structures/2023/mod_what_is_numbering)).
- **Filter and report glitches.** Floating-point values (150.000 vs 150.000000345) break filters. Default values in square brackets leave report fields empty ([LinkedIn](https://www.linkedin.com/advice/0/what-most-common-challenges-errors-you-encounter)).
- **Revisions, title blocks and PDF names.** These run through advanced options and template workarounds rather than a simple UI ([print file names](https://support.tekla.com/doc/tekla-structures/2026/dra_printing_to_pdf), [drawing number in title block](https://support.tekla.com/article/drawing-number-in-titleblock)).

I could not get a ranking of the most-downloaded Tekla Warehouse items. The Warehouse can be sorted by review count ([Warehouse search](https://warehouse.tekla.com/#!/search/?resultSet=TCC&sortBy=-reviewCount)), but I did not get numbers from it. Check this by hand.

## 2. What already exists (don't reinvent)

| Need | Existing tool | Source |
|---|---|---|
| Batch PDF print, one combined PDF, file-name rules | Built-in Document manager print + `XS_DRAWING_PLOT_FILE_NAME_*` | [Print to PDF](https://support.tekla.com/doc/tekla-structures/2026/dra_printing_to_pdf), [print improvements](https://support.tekla.com/cs/doc/tekla-structures/2023/rel_printing_improvements) |
| Same revision on many drawings | Built-in Document manager > Revision | [Revise drawings](https://support.tekla.com/doc/tekla-structures/2025/dra_creating_revisions) |
| Drawing creation at scale | Cloning templates, Master drawing catalog | [Clone drawings](https://support.tekla.com/doc/tekla-structures/2025/dra_cloning_drawings) |
| Mark and dimension checking | Built-in Drawing content manager, change symbols | [DCM](https://support.tekla.com/doc/tekla-structures/2025/dra_drawing_content_manager), [change symbols](https://support.tekla.com/doc/tekla-structures/2026/dra_change_symbols) |
| UDA fill from Excel/CSV | *SetnGet UDA by List* (Warehouse, source code public; price not stated) | [Developer awards](https://developer.tekla.com/documentation/tekla-developer-awards-2019-setnget-uda-list) |
| Excel tables in drawings | *Excel to drawing* (Warehouse) | [Tekla help](https://teklastructures.support.tekla.com/not-version-specific/en/ext_excel_to_drawing) |
| Grid save/load, grid from parts | *Save Grid To File* (XML), *Grid From Parts* | [Save Grid](https://support.tekla.com/help/tekla-structures/not-version-specific/save_grid_to_file), [Grid From Parts](https://support.tekla.com/help/tekla-structures/not-version-specific/grid_from_parts) |
| Quantity takeoff to Excel | Organizer export; new .xlsx reports in TS 2026 | [Organizer export](https://support.tekla.com/doc/tekla-structures/2026/mod_exporting_object_properties_from_object_browser), [XLSX reports](https://support.tekla.com/doc/tekla-structures/2026/rep_create_excel_xlsx_report) |
| NC/DSTV, MIS lists | Built-in File > Export > NC files; MIS export (DSTV, KISS, EPC, Steel 2000) | [NC files](https://support.tekla.com/doc/tekla-structures/2026/int_create_nc_files), [MIS list](https://support.tekla.com/doc/tekla-structures/2024/int_exporting_mis_list) |
| Clash check | Built-in Clash Check Manager (sessions saved as XML in `<model>\Clashes`) | [Find clashes](https://support.tekla.com/doc/tekla-structures/2025/mod_finding_clashes_using_ccm) |
| Comparing model versions | IFC change detection, Compare parts/assemblies | [Change detection](https://support.tekla.com/doc/tekla-structures/2026/int_detecting_changes_in_reference_model), [Compare](https://support.tekla.com/zh-hans/doc/tekla-structures/2026/mod_comparing_parts_or_assemblies) |
| Drawing numbering, rebar mark merge, lifting inserts | Warehouse: Drawing Numbering Tool, Trimble Drawing Extensions, Lifting Inserts | [rendair blog **[unverified, vendor-adjacent]**](https://rendair.ai/blog/top-plugins-and-extensions-for-tekla-structures), [Lifting Inserts](https://support.tekla.com/help/tekla-structures/not-version-specific/lifting_inserts) |
| Paid steel bundle | Construsoft Steel Solutions (67 extensions, subscription) | [Construsoft](https://shop.construsoft.com/products/steel-solutions) |
| Model dump to JSON; report/template generator | LetsConstructIT *TeklaDump*, *tekla-templates* (MIT, open source) | [GitHub](https://github.com/LetsConstructIT) |

**Note:** I found no Tekla tool that compares two BOM revisions ([Tekla compare docs](https://support.tekla.com/help/tekla-structures/not-version-specific/ifc_change_management)). Tekla's own comparison works on IFC and model objects, not on exported lists. That gap is a good fit for file-based scripts.

## 3. Where Claude works well without the Tekla API (files only)

- **Exported reports (CSV/XSR/XLSX).** Reports come from the model database and do not update themselves; you must run them again after model changes ([Reports](https://support.tekla.com/doc/tekla-structures/2026/rep_reports)). Python/pandas can turn them into summaries, weight per phase and price offers.
- **DSTV/NC1 files.** Open-source parsers exist: `dstvparser` (Python, NC1 support "maturing"), the Rust `dstv` crate (draws SVG) and DSTV.Net ([PyPI](https://pypi.org/project/dstvparser/), [docs.rs](https://docs.rs/crate/dstv/0.5.0), [NuGet](https://www.nuget.org/packages/DSTV.Net/1.2.0)). Tekla also writes `dstv_nc.log`, which lists exported and skipped parts ([NC files](https://support.tekla.com/doc/tekla-structures/2026/int_create_nc_files)).
- **IFC.** `ifcopenshell` reads the property sets. `ifctester` checks a model against an IDS file and writes HTML, JSON or BCF reports ([IfcTester docs](https://docs.ifcopenshell.org/ifctester.html), [tutorial](https://thinkmoult.com/using-ifcopenshell-parse-ifc-files-python.html)). Tekla's own advice is to check exported IFC by counting objects and reading the export log ([Check exported IFC](https://support.tekla.com/doc/tekla-structures/2025/int_checking_exported_ifc_model)).
- **PDF drawings.** Batch renaming, merging and transmittal lists can be done with standard Python PDF libraries.
- **Trimble Connect.** There is a REST API with files, folders, ToDos and topics ([Connect Core docs](https://developer.trimble.com/docs/connect/core)). I found no official Python SDK **[unverified]**.

## 4. Live Tekla API: what it needs

The Open API is .NET ([Tekla Open API](https://support.tekla.com/doc/tekla-structures/2026/sys_tekla_open_api)). Recorded or hand-written C# macros (`.cs`) are compiled when they run, sit in `XS_MACRO_DIRECTORY`, and can create drawings or reports ([Macros](https://developer.tekla.com/documentation/macros-cs), [Record macro](https://support.tekla.com/doc/tekla-structures/2026/det_recording_editing_and_running_macros)).

Python can use the API through pythonnet or pyTekla ([VIKTOR docs](https://docs.viktor.ai/docs/create-apps/software-integrations/tekla/)). Scripts need a running Tekla Structures with the model open on Windows. VIKTOR lists "an active model" as a requirement; the general rule is widely known but **[unverified]** in Tekla's docs.

## 5. Ranked ideas (value vs. difficulty for a non-programmer)

| # | Idea | Needs | Value | Difficulty |
|---|---|---|---|---|
| 1 | BOM/assembly list revision diff (Rev A vs Rev B → added, removed and changed parts in Excel) | Files | High | Low |
| 2 | Report export → price offer / weight summary per phase, profile and grade, with a price table | Files | High | Low |
| 3 | PDF drawing batch: rename by title-block/list, merge per assembly, make a transmittal (Excel/PDF) | Files | High | Low |
| 4 | Report "sanity checker": empty UDAs, missing grade/finish, `?` numbering, duplicate marks | Files (report) | High | Low |
| 5 | NC1 checker: compare the DSTV folder against the assembly list, flag missing or skipped parts (from `dstv_nc.log`) and summarize holes and lengths | Files | Med–High | Low–Med |
| 6 | Cutting list / stock-length nesting from a part list (1D bin packing) | Files | Med–High | Med |
| 7 | IFC check with an IDS (required psets, phases, names) before sending to the client | Files | Med–High | Med |
| 8 | Clash session XML → readable Excel/HTML summary per responsible party | Files | Med | Low–Med |
| 9 | Excel → UDA bulk fill (or prepare the CSV for SetnGet UDA) | Existing tool + file prep | High | Low |
| 10 | Report/drawing template (.rpt/.tpl) generation and editing with Claude (see *tekla-templates*) | Files in environment | Med | Med |
| 11 | Excel → grids / member import macro | Live API | Med | Med–High |
| 12 | Batch drawing-property / revision / title UDA setter macro | Live API | High | Med–High |
| 13 | Trimble Connect sync: download the latest IFC/PDF, list open topics | REST API | Med | Med |
| 14 | Automatic mark/dimension cleanup in drawings | Live Drawing API | High | High (prefer templates and DCM) |

Start with ideas 1–5. They need only exported files, can be tested on copies, and carry no risk to the model.

## 6. Doporučené postupy / Recommended practices

1. **Measure before automating.** Value = time per action × frequency × users × projects. Skip tasks that are rare, highly variable or need judgment, and fix a bad process before automating it ([FabIntelTech](https://fabinteltech.com/blog/tekla-workflow-productivity)).
2. **Ask your best detailers** which tasks they repeat without thinking. Their existing workarounds and macros show where the real problems are ([FabIntelTech](https://fabinteltech.com/blog/tekla-workflow-productivity)).
3. **Settings before scripts.** Careful drawing properties and cloning templates cut manual editing more than after-the-fact fixes do ([Clone drawings](https://support.tekla.com/doc/tekla-structures/2025/dra_cloning_drawings)).
4. **Numbering routine.** Number the model at the start or end of each day. Set the numbering series in the default properties before modeling. Use UDAs, Organizer or colours for classification, not numbering ([Numbering tips](https://support.tekla.com/doc/tekla-structures/2025/mod_numbering_tips)).
5. **Regenerate reports after every change**, because reports do not update themselves ([Reports](https://support.tekla.com/doc/tekla-structures/2026/rep_reports)).
6. **Check outputs.** Read the NC log, compare IFC object counts, and use the drawing check and revision tools before you issue anything ([NC files](https://support.tekla.com/doc/tekla-structures/2026/int_create_nc_files), [IFC check](https://support.tekla.com/doc/tekla-structures/2025/int_checking_exported_ifc_model), [LinkedIn](https://www.linkedin.com/advice/0/what-most-common-challenges-errors-you-encounter)).
7. **Model hygiene.** Back up and repair the model regularly, and use filters and work areas on large models ([LinkedIn](https://www.linkedin.com/advice/0/what-most-common-challenges-errors-you-encounter)).
8. **Look in the Warehouse first.** Only build what is missing. Keep firm macros in a shared `XS_MACRO_DIRECTORY` ([Record macro](https://support.tekla.com/doc/tekla-structures/2026/det_recording_editing_and_running_macros)).
9. **For AI-built scripts:** have them work on exported copies, keep inputs read-only, and test on one small model before using them on a live project. This is my own recommendation, not from a source.
