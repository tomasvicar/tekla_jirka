# 10 – Onboarding a non-programmer (Tekla detailer) to Claude Code

*Research date: 2026-10-30. [UNVERIFIED] = only third-party or snippet sources, or my own inference.*

## 1. Which tool to start with

- **Claude Code in the Desktop app (Code tab)** is the best fit. It runs on Windows (x64/ARM64), has a visual diff view where you can leave comments on lines, and offers permission modes (Manual, Accept edits, Plan, Auto) without needing a terminal. https://code.claude.com/docs/en/desktop
- The CLI works natively on Windows from PowerShell/CMD. Git for Windows is optional, and without it Claude uses PowerShell. Claude Code needs a Pro, Max, Team, Enterprise or Console account; the free plan is not enough. https://code.claude.com/docs/en/setup
- **Cowork** is Anthropic's desktop agent for non-developers. It works in a sandboxed folder and suits file and document tasks, not building C# plugins. https://www.lowcode.agency/blog/claude-cowork-vs-claude-code , https://every.to/vibe-check/vibe-check-claude-cowork-is-claude-code-for-the-rest-of-us. Launch date and platform availability vary between sources [UNVERIFIED].

## 2. Learning material

**Official (Anthropic Academy)** https://anthropic.skilljar.com/
- Claude 101
- Introduction to Claude Cowork
- AI Fluency: Framework & Foundations
- Claude Code 101 (aimed at developers new to AI agents; covers explore → plan → code → commit and CLAUDE.md): https://anthropic.skilljar.com/claude-code-101
- Claude Code in Action
- Introduction to Agent Skills

**Official articles and docs**
- "How Anthropic teams use Claude Code": Legal built a "phone tree" prototype with no developers; Growth Marketing built a workflow that processes ad CSVs and a Figma plugin; Design fed Figma files in to map edge cases. The article's key line: *"treat Claude Code as a thought partner rather than a code generator."* https://claude.com/blog/how-anthropic-teams-use-claude-code
- Terminal guide for beginners: https://code.claude.com/docs/en/terminal-guide
- Best practices: https://code.claude.com/docs/en/best-practices

**Community**
- "Claude Code for Everyone" (Carl Vellotti): free, not affiliated with Anthropic, taught inside Claude Code. Module 1 takes about 3 h; requires Pro or Max. https://ccforeveryone.com/
- Overview of courses: https://theneuron.ai/explainer-articles/claude-code-complete-guide-best-tutorials-2026

**AEC-specific**
- Autodesk University class "Don't Wait: Non-Revit Developers Create Your Own Revit Add-Ins Using AI and the Revit API" (2026). The page returned 403, so this is based on the search snippet only [UNVERIFIED]. https://www.autodesk.com/autodesk-university/class/Dont-Wait-Non-Revit-Developers-Create-Your-Own-Revit-Add-Ins-Using-AI-and-the-Revit-API-2026
- **Tekla's own Developer Assistant** generates Open API macro code in a side pane, ships in TS 2025 SP5+, and requires a Diamond licence or a Partners subscription. It is worth comparing with Claude. https://support.tekla.com/doc/tekla-structures/not-version-specific/developer_assistant
- Macros are stored in `\macros\modeling` or `\macros\drawings` (model folder or XS_MACRO_DIRECTORY) and are created via Applications & components → Record/New macro. https://support.tekla.com/doc/tekla-structures/2026/xs_macro_directory

## 3. Mental models to teach

1. **Describe the task in domain language, plus what "done" looks like.** Name the file, the symptom and the expected result, or give Claude a real sample file instead of describing it. https://code.claude.com/docs/en/best-practices
2. **Plan mode (Shift+Tab / "Plan" in Desktop).** Claude explores and proposes a plan but edits nothing. This catches wrong assumptions before any code is written. https://code.claude.com/docs/en/desktop , https://builder.io/blog/claude-code-tips-best-practices
3. **Give Claude a check to run.** For example: "compare the totals with the original report". https://code.claude.com/docs/en/best-practices
4. **Steer early.** Press `Esc` the moment Claude drifts. After two failed corrections, use `/clear` and write a better prompt. https://code.claude.com/docs/en/best-practices
5. **Checkpoints and `/rewind` (Esc Esc).** Roll back the code, the conversation, or both. This only covers files Claude edited itself, not changes made by Bash commands, so git is still needed. https://code.claude.com/docs/en/best-practices
6. **Ask Claude to explain.** Ask what a line does, why it took an approach, or what could break. That is how he learns C# over time ("thought partner"). https://claude.com/blog/how-anthropic-teams-use-claude-code
7. **Review the changes** in the Desktop diff view with line comments. https://code.claude.com/docs/en/desktop
8. **CLAUDE.md memory.** Run `/init`, keep the file short, and add anything you have had to correct twice (Tekla version, paths, naming conventions). https://code.claude.com/docs/en/best-practices
9. **Skills / slash commands.** Save a repeatable procedure as a skill. Only its name and description load until Claude needs it. https://code.claude.com/docs/en/best-practices

## 4. Typical beginner mistakes

- **The "vending machine" mindset:** one prompt in, finished code out. https://www.adventureppc.com/blog/the-real-learning-curve-of-claude-code-what-beginners-get-wrong-in-the-first-30-days [UNVERIFIED blog]
- **Treating it as a chat instead of a workspace.** https://claudecodeformarketers.com/blog/what-i-got-wrong-about-claude-code/
- **Not checking the result.** Expecting a perfect first attempt. https://buildtolaunch.substack.com/p/claude-code-for-everyone-from-zero-to-your-first-project-in-30-minutes
- **Long, mixed conversations.** Use `/clear` between unrelated tasks; it is free and makes answers better and cheaper. https://code.claude.com/docs/en/best-practices
- **Unrealistic timeline.** Expect roughly 3–6 weeks to confident use. https://adventuremedia.ai/blog/how-long-does-it-take-to-learn-claude-code-by-skill-level [UNVERIFIED]
- **Running macros on a production model.** Always test on a copy of the model. This is my recommendation, not a sourced claim.

## 5. Realistic expectations: cost and limits

- **Plans:** Pro is $20/month, Max 5x is $100/month and Max 20x is $200/month. Chat and Claude Code share one usage pool, with a 5-hour rolling window plus a weekly cap. https://ai.zenken.co.jp/en/post/claude-pro-vs-max-comparison/ , https://inventivehq.com/blog/claude-code-rate-limits-explained [UNVERIFIED, third-party]
- **May 2026 change:** Anthropic reportedly doubled the 5-hour Claude Code limits. https://inventivehq.com/blog/claude-code-rate-limits-explained [UNVERIFIED]
- **Recommendation:** start on Pro. Move to Max 5x only if he regularly hits the limit. Check current terms at https://support.claude.com.

## 6. First session agenda (about 2.5 h)

| Time | Block |
|---|---|
| 0:00–0:15 | Why bother: Anthropic's examples of Legal and Marketing teams building tools without developers. Set expectations: Claude is a junior colleague who needs review. |
| 0:15–0:35 | Install the Desktop app, log in (Pro), create the folder `C:\TeklaAI\` with a `data\` subfolder holding sample exports. Install Git for Windows. |
| 0:35–0:50 | Tour: chat, Plan mode, permission modes, diff view, Esc, `/rewind`, `/clear`. |
| 0:50–1:30 | **Exercises 1 + 2**, with him at the keyboard and you only coaching. |
| 1:30–1:40 | Break. |
| 1:40–1:55 | `/init` → CLAUDE.md (Tekla version, units, column meanings). Make a first git commit with Claude's help ("save a version"). |
| 1:55–2:25 | **Exercise 3**, which saves the procedure as a skill. |
| 2:25–2:40 | Demo of exercises 4–5 in Plan mode only (on a model copy). Homework: Academy "Claude 101" + ccforeveryone Module 1. |

## 7. Five progressive exercises for a Tekla user

1. **Report → Excel summary.** "Read `data/material_list.csv` (a Tekla report export) and make an Excel file with weight by profile and by phase, with a TOTAL row." The check: the total must match the report.
2. **Check and clean the data.** "Find parts with no name, no material, or duplicate positions; write them to a 'Problems' sheet." Practise follow-up questions and asking Claude to explain its logic.
3. **Reusable tool plus a skill.** "Turn this into a script I can run on any export with one double-click (a .bat file)." Then save the procedure as a skill, `/souhrn-reportu`.
4. **Read-only Tekla macro.** In Plan mode: "Write a Tekla macro in C# that lists the selected parts (name, profile, material, class) to a file." Copy it into `\macros\modeling` and run it via Applications & components. https://support.tekla.com/doc/tekla-structures/2026/xs_macro_directory
5. **Macro that changes attributes of the selected parts** (for example, set Class/Name/UDA by profile). Requirements: work on a model copy, a summary of what will change with an "OK" confirmation before anything is changed, and `CommitChanges` only at the end. Have Claude explain every block. Optionally compare with the Tekla Developer Assistant. https://support.tekla.com/doc/tekla-structures/not-version-specific/developer_assistant

## 8. Doporučené postupy / Recommended practices

- One folder per project, with a CLAUDE.md written in his own words (Czech is fine).
- Always start with Plan mode. Let Claude ask questions first ("interview me before you start"). https://ccforeveryone.com/
- Provide a real sample file and a check for every task. https://code.claude.com/docs/en/best-practices
- Make a small step, check it, then commit to git ("save a version"). Use checkpoints/`/rewind` for quick rollbacks, but don't rely on them alone. https://code.claude.com/docs/en/best-practices
- After two failed corrections, use `/clear` and write a better prompt. https://code.claude.com/docs/en/best-practices
- Ask "explain it to me like a detailer", and read the diff before accepting.
- Test Tekla macros only on a copy of the model, starting with read-only versions. This is my recommendation.
- Save a prompt that worked as a skill or slash command, and build a personal library of them.
- Do not use bypass permissions. Manual or Accept edits mode is enough. https://code.claude.com/docs/en/desktop
