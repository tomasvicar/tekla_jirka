# 09 – Security, client data and backups (Claude + Tekla Structures)

*Research date: 2026-10-30. Every claim has a source URL. Anything marked **[unverified]** could not be confirmed on a primary source page.*

## 1. What goes to Anthropic

- **Everything Claude reads is sent to Anthropic.** That covers prompts, model outputs, file contents Claude opens and MCP tool results, because they all become part of the conversation. Claude Code "sends data over the network. This data includes all user prompts and model outputs", encrypted with TLS 1.2+. https://code.claude.com/docs/en/data-usage
- **Large MCP results are still sent.** Claude Code warns above 10,000 tokens of MCP output and caps it at 25,000 tokens by default. A query that dumps the whole model therefore still sends a lot of data. https://code.claude.com/docs/en/mcp
- **Local transcripts.** Session transcripts are stored in plaintext under `~/.claude/projects/` for 30 days (setting: `cleanupPeriodDays`). Sessions from Claude Desktop/Cowork are exempt from that limit by default. https://code.claude.com/docs/en/data-usage

### Consumer plans (Free/Pro/Max) vs commercial plans (Team/Enterprise/API)

| | Pro / Max (consumer) | Team / Enterprise / API (commercial) |
|---|---|---|
| Training | Used for training only if "Model improvement" is on. You choose this in settings: https://code.claude.com/docs/en/data-usage | "Anthropic may not train models on Customer Content" (Commercial Terms, eff. 17 Jun 2025): https://www.anthropic.com/legal/commercial-terms |
| Retention | 30 days with improvement off. Up to 5 years with it on. https://code.claude.com/docs/en/data-usage | 30 days standard. Zero Data Retention only for qualified Enterprise orgs, enabled per org: https://code.claude.com/docs/en/data-usage |
| Exceptions | Flagged content kept up to 2 years (scores up to 7). Feedback (thumbs, `/feedback`) kept 5 years. https://privacy.claude.com/en/articles/10023548-how-long-do-you-store-my-data | `/feedback` transcripts kept 5 years on any plan: https://code.claude.com/docs/en/data-usage |
| GDPR / DPA | The DPA article covers commercial products only: https://privacy.claude.com/en/articles/7996862-how-do-i-view-and-sign-your-data-processing-addendum-dpa | DPA with SCCs is built into the Commercial Terms: same URL. "Customer Content is Customer's Confidential Information": https://www.anthropic.com/legal/commercial-terms |

- **Connectors and MCP content.** "Raw content from connectors… including MCP servers, is not included in training data", but content you paste into a chat can be. https://privacy.claude.com/en/articles/10023580-is-my-data-used-for-model-training
- **EEA consumer terms.** As fetched (effective 8 Oct 2025), these include Section 11 "Non-commercial use only": "You agree that you will not use our Services for any commercial or business purposes". They also exclude liability for business losses. https://www.anthropic.com/legal/consumer-terms
  - For a Czech detailer billing clients, this means a Pro/Max plan is a poor contractual fit for client work. A commercial plan (Team, or an API key under the Commercial Terms) is the safer basis. The exact interpretation should be checked with a lawyer **[legal interpretation unverified]**.
- **EEA controller.** For consumer users in the EEA, the data controller is Anthropic Ireland, Limited. Transfers rely on adequacy decisions and SCCs (privacy policy eff. 10 Sep 2026). https://www.anthropic.com/legal/privacy
- **Personal data in Tekla models.** Model data is mostly technical, not personal. Title blocks, user names and model history can still contain personal data **[reasoned, not sourced]**.

## 2. Client confidentiality and NDAs

- **RICS (surveyors).** Firms "must refrain from uploading" private and confidential client data to an AI system unless they have "express written consent in advance from the client". They must also be satisfied that the risk is acceptable. https://www.rics.org/profession-standards/rics-standards-and-guidance/conduct-competence/responsible-use-of-ai/client-information-note
- **RIBA (architects).** RIBA lists data security, confidentiality, professional indemnity insurance and IP as significant issues, and notes that few practices have formal AI policies. https://www.riba.org/work/insights-and-resources/ai-report/ribas-adrian-malleson-responds-to-the-2026-ai-report/
  - It advises agreeing with legal and digital advisers which data must not go into generative AI tools. https://riba.org/work/insights-and-resources/professional-features/ai-professional-features/what-are-the-risks-to-architects-and-practices-who-use-ai **[seen via search snippet only]**
- **ICAEW (accountants).** Entering client data into AI tools is "very likely" to breach confidentiality. https://www.icaew.com/regulation/regulatory-news/regulatory-news-2024-02/dont-let-ai-tools-land-you-in-hot-water
- **IStructE.** Its AI guidance reportedly recommends giving clients a copy of the firm's AI policy. https://www.istructe.org/resources/technology-digital/artificial-intelligence-guidance/ **[page returned 403; unverified]**
- **ICE, ČKAIT.** No specific guidance found **[not found]**.
- **Practical conclusion.** Typical construction NDAs and subcontracts forbid disclosing project information to third parties. Sending model data to an AI provider may count as such a disclosure. Read each NDA, and get written client consent where in doubt (following the RICS approach) **[reasoned]**.

## 3. Trimble/Tekla licence terms (EULA 2024)

Source for all of section 3 unless noted: https://tekla.com/assets/documents/TrimbleTeklaEULA2024%20(eng-us).pdf. A newer EULA version may apply to your subscription **[check]**.

- **"Application" (Open API).** Defined as any component that interacts with the software through its Interface or Open API (cl. 1, 15.2).
- **Building for yourself is allowed.** Clause 4.11(f) forbids using the software to develop other software "except the Applications". You may develop for your own use.
- **Building for others is not.** Clause 4.11(g) forbids developing Applications for third parties without the Partner Program and a Partner License.
  - Developer policy: "you can develop … applications for your own use", but distributing or selling them requires the Tekla Partners Program. https://developer.tekla.com/policy
  - A freelancer who sells or hands over macros/MCP tools to clients needs to keep this in mind.
- **Your risk.** Clause 4.12: "You shall assume all risk and liability regarding the development and/or use of any Applications."
- **Results must be checked.** Clause 9.2: results must be "verified as correct by an appropriately qualified person". This applies directly to AI-generated changes.
- **Virtual machines.** Clause 4.11(e) forbids virtualization only "in a manner that would exceed the number of Licenses purchased".
  - Tekla documents virtualized use. Each `TeklaStructures.exe` instance needs a valid licence, and models should be kept on a file server, not the VM's local disk. https://support.tekla.com/doc/tekla-structures/2026/ins_using_tekla_structures_in_a_virtual_environment
- **No AI clause found.** The 2024 EULA has no clause about AI or LLM tools **[searched text; none found]**.

## 4. Technical safety (Claude Code / Desktop)

- **Permission rules.** Rules are evaluated "deny, then ask, then allow". MCP tools can be targeted as `mcp__<server>__<tool>` or `mcp__<server>__*`. https://code.claude.com/docs/en/permissions
  - Example: put write tools such as `mcp__tekla__modify_*` in `ask`, and read tools in `allow`.
- **Permission modes.** The modes are default/manual, `acceptEdits`, `plan` (read-only exploration), `auto` (a classifier decides), `dontAsk` and `bypassPermissions`. https://code.claude.com/docs/en/permissions
  - `bypassPermissions` should be used only "in isolated environments like containers or VMs".
  - It can be disabled with `permissions.disableBypassPermissionsMode: "disable"`. Auto mode can be disabled the same way.
- **Sandboxing is not available on native Windows.** The sandbox runs on macOS, Linux and WSL2. "On native Windows, Claude Code runs commands unsandboxed." It also "covers shell commands only… MCP servers… run outside it". https://code.claude.com/docs/en/sandboxing
  - Tekla runs on Windows, so permission rules and human review are the main controls.
- **Prompt injection.** No system "is completely immune". Anthropic recommends reviewing commands, verifying changes to critical files and using VMs. https://code.claude.com/docs/en/security
  - Text inside a model (part names, UDAs, IFC from other parties, imported reference models) is untrusted input. Instructions hidden there could steer Claude **[reasoned]**.
- **MCP servers.** "Verify you trust each server before connecting it." Anthropic "does not security-audit or manage any MCP server". https://code.claude.com/docs/en/mcp , https://code.claude.com/docs/en/security
- **Your responsibility.** "You're responsible for reviewing proposed code and commands for safety before approval." https://code.claude.com/docs/en/security

## 5. Backups and Undo in Tekla

- **Undo after API changes.** Each `Model.CommitChanges()` call is one step the user can reverse with Undo: "One commit is something that a user can later on undo with the undo command." https://developer.tekla.com/doc/tekla-structures/2026/commit-changes-method-71945
  - A script that commits many times creates many undo steps. Commit once per logical operation.
  - Undo through the API itself was not documented **[not found]**. Undo is not a backup.
- **Autosave.** Default interval is 15 minutes, written to `C:\TeklaStructuresModels\autosave` as `.db1_<user>` (option `XS_AUTOSAVE_DIRECTORY`). https://support.tekla.com/doc/tekla-structures/2026/mod_saving_model_with_different_name_or_location
- **Backup copy.** *File > Save as > Save and create backup copy* writes to `..\TeklaStructuresModels\backup\<model>\<date-time>` (option `XS_MODEL_BACKUP_DIRECTORY`) and keeps the GUIDs.
  - Plain *Save as* creates new GUIDs and "cannot be used as backup".
  - To restore, copy the dated backup into the model folder or rename it.
  - Same source.
- **Model folder files.** `.db1` is the model database and `.db2` the numbering database. https://support.tekla.com/doc/tekla-structures/2026/sys_files_and_file_extensions
- **Model Sharing.** Back up shared models, including the whole folder with drawings. Keep local copies on a local disk. Have the owner create baselines regularly, for example weekly. You can recover from any user's local copy or a backup. https://support.tekla.com/doc/tekla-structures/2022/ms_best_practises
- **Experiments on a copy.** For experiments, *Save as* a copy is fine, but GUIDs change, so changes cannot be merged back by GUID (same Tekla source).

## Doporučené postupy / Recommended practices

1. **Use a commercial plan for client work.** Use Team/Enterprise or an API key under the Commercial Terms: no training, DPA with SCCs, content treated as confidential. On Pro/Max, at minimum turn off "Model improvement" (claude.ai/settings/data-privacy-controls) and do not send feedback on client sessions.
2. **Check the NDA, then get consent.** Read each project's NDA or contract. If unclear, get the client's written consent. Keep a one-page AI policy (tools used, data sent, retention) to give to clients.
3. **Send as little as possible.** Use MCP tools that return filtered, aggregated data, not whole-model dumps. Do not paste drawings, client names or contract documents into chats.
4. **Read first, write later.** Allow read tools freely, keep write and modify tools on `ask`, and start with plan mode. Disable `bypassPermissions`.
5. **Only reviewed MCP servers.** Use servers you wrote or reviewed yourself, pinned to a version. Treat model text from other parties as untrusted.
6. **Back up before every AI session.** Use *Save and create backup copy*, or work on a test copy. Commit once per logical change. Verify the results yourself, as EULA clause 9.2 requires.
7. **Keep macros and MCP code in git.** Use a private repo and review diffs before running anything. Do not distribute tools to clients without considering the Partner Program terms.

## Checklist

- [ ] Plan: Team/API (commercial), or Pro/Max with Model improvement **off**
- [ ] NDA checked / client consent on file for this project
- [ ] Backup copy created (Save and create backup copy) and time noted
- [ ] Only trusted MCP servers enabled; write tools set to `ask`
- [ ] Script/macro diff reviewed and committed to git before running
- [ ] Changes checked in Tekla (Undo available per commit); numbering and drawings checked
- [ ] Old local transcripts in `~/.claude/projects/` cleaned up when the project ends
