# Setting up Claude on Windows for a Tekla Structures user (non-programmer)

Research date: 2026-10-30. Sources are mostly official docs (code.claude.com, support.claude.com, claude.com, modelcontextprotocol.io). Items marked **[UNSURE]** come from third-party sources or are likely to change.

---

## 1. Plan and pricing

- **Free plan does not include Claude Code.** You need Pro, Max, Team or Enterprise. https://code.claude.com/docs/en/setup (section "Authenticate")
- Prices from https://claude.com/pricing (USD, may vary by region/VAT):
  - **Pro**: $20/month billed monthly, or $17/month billed annually ($200/year).
  - **Max 5x**: $100/month. **Max 20x**: $200/month. https://support.claude.com/en/articles/11049744-how-much-does-the-max-plan-cost
  - **Team**: Standard seat $25 monthly / $20 annual; Premium seat $125 monthly / $100 annual.
- **Computer use** (Claude clicking around in desktop apps) **needs Pro or Max**. It is a research preview and **not available on Team/Enterprise**. https://code.claude.com/docs/en/desktop
- **Recommendation:** start with **Pro**. Move to Max 5x only if he keeps hitting usage limits.

## 2. Which interface: Desktop app (Code tab) is the friendliest

| Option | For a non-programmer | Notes |
|---|---|---|
| **Claude Desktop, Code tab** | **Best** | Graphical interface. Has diffs, approve buttons, a mode selector and a folder picker. "The desktop app includes Claude Code, so you don't need to install Node.js or the CLI." https://code.claude.com/docs/en/desktop-quickstart |
| CLI in PowerShell | Possible, less friendly | `irm https://claude.ai/install.ps1 \| iex`. No admin rights needed. https://code.claude.com/docs/en/setup |
| VS Code extension | Only if he already uses VS Code | Same engine. Mode indicator sits in the prompt box. https://code.claude.com/docs/en/permission-modes |

The Desktop app also has a normal **Chat** tab and **Cowork** for non-coding work.

**Windows requirements** (https://code.claude.com/docs/en/setup):
- Windows 10 1809+ and 4 GB+ RAM. x64 or ARM64 installer: https://claude.com/download
- **WSL is not needed.** Run it natively, since Tekla is a Windows app.
- **Git for Windows is optional** but recommended. Without it, Claude uses PowerShell as its shell. With it, Claude uses Git Bash, and Git also lets you undo changes to scripts and files. Desktop versions before 1.49585.0 required Git. https://code.claude.com/docs/en/desktop
- **Node.js** is not needed for Claude Code itself. It is needed only for MCP servers started with `npx`. Python or `uv` is needed only for Python servers.
- Desktop does **not read PowerShell profiles**. Set PATH in the Windows environment variables, then fully quit and reopen Desktop. https://code.claude.com/docs/en/desktop

### Step by step
1. Buy Pro on claude.ai.
2. Download and install Claude Desktop (Windows x64). Sign in.
3. Open the **Code** tab. Choose environment **Local**, then **Open folder…** and pick a dedicated working folder (for example `C:\TeklaAI\`). Don't pick the live model folder. https://code.claude.com/docs/en/desktop-quickstart
4. Optional: install Git for Windows (https://git-scm.com/downloads/win) and run `git init` in that working folder.
5. Set the permission mode to **Manual** for the first weeks (see section 5).

## 3. MCP (connecting Claude to Tekla or other tools)

### 3a. Claude Desktop config file
- Open it via **Settings > Developer > Edit Config** (older layout) or the **Extensions page > Local MCP servers** (newer layout). https://support.claude.com/en/articles/10949351
- File location: `%APPDATA%\Claude\claude_desktop_config.json`. https://modelcontextprotocol.io/docs/develop/connect-local-servers
- Example (backslashes must be doubled in JSON):
```json
{
  "mcpServers": {
    "tekla": {
      "command": "C:\\Tools\\TeklaMcp\\TeklaMcp.Server.exe",
      "args": [],
      "env": { "SOME_VAR": "value" }
    }
  }
}
```
  For Python use `"command": "python", "args": ["C:\\path\\server.py"]`. For .NET use `"command": "dotnet", "args": ["C:\\path\\Server.dll"]`. Always use **absolute paths**.
- After editing, **fully quit Claude** (including the tray icon) and restart it.
- Logs: `%APPDATA%\Claude\logs\mcp.log` and `mcp-server-NAME.log`. https://modelcontextprotocol.io/docs/develop/connect-local-servers
- If you see an `${APPDATA}` ENOENT error, add `"APPDATA": "C:\\Users\\<user>\\AppData\\Roaming\\"` to `env`. If `npx` fails, run `npm install -g npm` (same source).
- Servers in `claude_desktop_config.json` are available **both in Chat and in local Code-tab sessions**. The standalone CLI does **not** read this file. `claude mcp add-from-claude-desktop` works only on macOS/WSL. https://code.claude.com/docs/en/desktop
- Windows troubleshooting: restart the app, check that the server process is running in Task Manager, and read the logs. https://code.claude.com/docs/en/desktop

### 3b. Desktop Extensions (.mcpb), the easiest path
- **One-click install:** Settings > Extensions > **Browse extensions** > Install. These are Anthropic-reviewed extensions.
- **Custom .mcpb file:** Extensions > Advanced settings > **Install Extension…**. You can also double-click the file or drag it into the window. Secrets are stored in Windows Credential Manager. https://support.claude.com/en/articles/10949351 and https://www.anthropic.com/news/desktop-extensions
- Node.js ships with the app, so Node-based extensions don't need a separate Node install.
- **[UNSURE]** There is a reported bug in the Microsoft Store/MSIX build 1.12603.1.0 where Install Extension closes silently; "Install Unpacked Extension" works as a workaround. https://github.com/modelcontextprotocol/mcpb/issues/281 . Prefer the installer from claude.com/download over the Microsoft Store build.

### 3c. Claude Code (CLI) `claude mcp add`
- Syntax: `claude mcp add [--scope user|project|local] [--env K=V] --transport stdio <name> -- <command> [args]`. https://code.claude.com/docs/en/mcp
- Scopes:
  - **local** (default): this project only, stored in `~/.claude.json`.
  - **project**: shared through a `.mcp.json` file in the project root. It asks for approval on first use.
  - **user**: all projects, stored in `~/.claude.json`.
- Check servers with `/mcp`, `claude mcp list` or `claude mcp get <name>`. Set the startup timeout with `MCP_TIMEOUT`. Large outputs can be allowed with `MAX_MCP_OUTPUT_TOKENS`.
- **npx on native Windows:** `npx` is a `.cmd` shim, so wrap it: `claude mcp add myserver -- cmd /c npx -y some-package`. In JSON: `"command":"cmd","args":["/c","npx","-y","..."]`. **[UNSURE]** This comes from community guides; the current official MCP page did not show this note. https://mcpcat.io/guides/adding-an-mcp-server-to-claude-code , https://github.com/BunPrinceton/claude-mcp-windows-guide . A `.exe` server needs no wrapper.

### 3d. Existing Tekla MCP servers (community, unofficial) **[UNSURE: maturity]**
- https://github.com/teknovizier/tekla_mcp_server has a **read-only mode** and is tested with Tekla 2022 and 2026.
- https://github.com/tempalg1n/tekla-mcp-server is an .exe for Tekla 2023. UDA writes are preview-only unless an apply flag is set, and it has a mock backend.
- https://glama.ai/mcp/servers/YuriyKirillov/TeklaMCPServer uses Python 3.11+ and pythonnet, for Tekla 2023.

No official Trimble server was found. Check each one's Tekla version and start in read-only mode.

## 4. Useful features for a non-developer

- **CLAUDE.md**: project memory loaded every session. Put the Tekla version, folder layout, naming conventions and "never do X" rules here. Keep it short. The Desktop app and the CLI share it. https://code.claude.com/docs/en/memory , https://code.claude.com/docs/en/best-practices
- **Skills**: reusable procedures in `~/.claude/skills/`, started with `/` in the prompt box. Example: "export report", "check profiles". https://code.claude.com/docs/en/skills
- **Plugins**: bundles of skills, agents and MCP servers. Desktop has a plugin manager UI. https://code.claude.com/docs/en/desktop
- **Permission modes**: Manual, Accept edits, Plan, Auto, and Bypass (off by default; must be enabled in Settings). https://code.claude.com/docs/en/permission-modes
- **Slash commands**: `/rewind` (undo), `/clear` (fresh start), `/mcp`, `/chrome`. Checkpoints undo only Claude's own file edits. https://code.claude.com/docs/en/checkpointing
- **Computer use on Windows**: works in the **Desktop app only** (Settings > This computer > System > Enable computer use). Requires Pro/Max and is a research preview. The CLI version is macOS-only. It is the slowest fallback: Claude tries MCP, the shell and Chrome first. https://code.claude.com/docs/en/computer-use , https://code.claude.com/docs/en/desktop . **[UNSURE]** How well it drives the Tekla GUI is untested. Expect it to be slow and error-prone. Treat it as an experiment, not a workflow.
- **Claude in Chrome**: works with Chrome or Edge and needs a paid plan. It uses his logged-in browser sessions (for example Trimble/Tekla Warehouse). https://code.claude.com/docs/en/chrome
- **File access**: local sessions read and edit files in the chosen folder. Use `@filename` to add files to the conversation. https://code.claude.com/docs/en/desktop-quickstart

## 5. Safety

- **Sandboxing is NOT supported on native Windows.** It works only in WSL 2. https://code.claude.com/docs/en/setup . That means commands run with his full user rights, so permission prompts and backups are the main protection.
- Use **Manual** mode at first: Claude asks before every edit or command. Avoid Bypass. Even in Bypass, deny rules still block. Writes to `.claude`, `.mcp.json` and `.git` are protected. https://code.claude.com/docs/en/permission-modes
- Add **deny rules** in `.claude/settings.json` for the model folders, for example `Edit(C:/TeklaStructuresModels/**)`. Check the exact path syntax in https://code.claude.com/docs/en/permissions **[UNSURE: syntax]**.
- **`/rewind` cannot undo** changes made by shell commands, external programs, or **MCP calls into Tekla**. Those changes go straight into the model. https://code.claude.com/docs/en/checkpointing
- **Back up the Tekla model before every AI session.** Use **File > Save as > Save and create backup copy**. This keeps the GUIDs and saves a dated copy (location set by `XS_MODEL_BACKUP_DIRECTORY`). A plain "Save as" creates an unrelated model and is not a real backup. https://support.tekla.com/doc/tekla-structures/2025/mod_saving_model_with_different_name_or_location , https://support.tekla.com/fi/doc/tekla-structures/2021/xs_model_backup_directory
- Never point AI at a **multi-user master model**. Work on a local copy. https://support.tekla.com/doc/tekla-structures/2020/sys_multiuser_master_model_plan_model_autosave
- Prefer MCP servers in read-only or preview mode. Review every write action before approving it.
- Computer use runs on the real desktop. Press **Esc** to stop it. https://support.claude.com/en/articles/14128542

## 6. Recommended practices

Official, from https://code.claude.com/docs/en/best-practices:
- **Be specific.** Name the file or element, describe the symptom, and say what "done" looks like. This saves rounds of corrections.
- **Keep CLAUDE.md short.** Write only what Claude can't work out itself, plus anything you've had to correct twice.
- **Make hard rules into deny rules or hooks**, not CLAUDE.md lines. CLAUDE.md is guidance that Claude may decide doesn't apply.
- **Give Claude a check.** For example: "after the export, count the rows and compare with the Tekla report."
- **Use Plan mode** for anything bigger: Claude proposes an approach first and edits nothing.
- **Watch the first minute.** Press Esc as soon as Claude drifts. After two failed corrections, run `/clear` and write a better prompt instead of a third correction.
- **Run `/clear` between unrelated tasks.**

Tekla-specific (own synthesis):
- Start read-only: "list all beams with profile X", "summarise UDAs", "generate a report". Move to write operations only after he trusts the setup.
- Have Claude write repeatable things (macros, scripts, CSV transforms) as files, then test them on a backup copy of the model.

Community advice **[UNSURE: third-party blogs]**:
- Don't treat Claude like a vending machine. Iterate with it. https://www.adventureppc.com/blog/the-real-learning-curve-of-claude-code-what-beginners-get-wrong-in-the-first-30-days
- Vague prompts, a missing project instruction file, and sessions that mix topics are the top beginner mistakes. https://claudcod.com/blog/claude-code-beginner-mistakes/
- Always work inside one project folder. https://claudhq.com/claude-code-tips-for-absolute-beginners-2026/
- Expect a few weeks of learning. https://adventuremedia.ai/blog/how-long-does-it-take-to-learn-claude-code-by-skill-level

## Flags / uncertain
- Prices and plan features change often. Recheck https://claude.com/pricing before buying.
- The Desktop settings layout has changed recently (Developer vs. Extensions page). Menu names may differ from what is written here.
- The `cmd /c npx` advice and the community Tekla MCP servers are not official.
- Computer use on Windows is a research preview. Third-party sources disagree on its rollout dates.
