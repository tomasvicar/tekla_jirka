# 07 – Tekla trial and test environment (Fedora host → Windows → Tekla → Claude)

Researched 2026-10-30. Nothing was downloaded or installed. Items marked **[UNCERTAIN]** are not confirmed by a primary source.

## 1. Tekla Structures licence options

**Official 30-day trial (best fit)**
- The trial page now offers **Tekla Structures 2026**. It is free for 30 days and open to "any individual professional". Students are sent to Tekla Campus instead. https://download.trimble.com/tekla-structures/free-trial
- Workflow: create a Trimble ID → install Tekla and at least one Environment → activate through Tekla Launcher → sign in and pick the *trial configuration*. https://support.tekla.com/tekla-structures/get-started-with-trial, https://support.tekla.com/doc/tekla-structures/2026/ins_lic_tekla_structures_installation_and_licensing_workflow
- Configuration: there is one "trial configuration" with "the full functionality of Tekla Structures". You don't pick Full, Steel Detailing or Primary. Exceptions:
  - production imports and exports are disabled
  - drawings can be print-previewed but not printed or exported
  - Model Sharing is off
  - Trimble Connect integration is limited
  - **no Tekla Warehouse content**
  - the Support Tool is off
  - preview features are off

  Source: https://download.trimble.com/tekla-structures/free-trial
- **The trial cannot be extended.** You get **one trial per version**. Once activated, it is **locked to the Trimble ID and to the specific computer**. A computer that has already used a trial for that version can't get another one. The 30 days start at activation. Same source.
- **Open API in the trial: yes.** Tekla's developer site says the 30-day free trial lets you "test Tekla Structures and Tekla Open API". https://developer.tekla.com/tekla-structures, https://developer.tekla.com/tekla-structures-for-startups. I found no statement that macros or external apps are blocked. Warehouse is blocked, so get extensions from GitHub or build them yourself.
- **VM implication [UNCERTAIN, inference]:** the lock is to "a specific computer". If you rebuild or clone the VM, or change its hardware, the trial could be lost. Activate only on the final VM, and use snapshots instead of reinstalling.

**Tekla Campus / Student (Educational)**
- This is for higher-education students and educators. It runs 365 days, gives up to 2 concurrent sessions and allows 24 h offline. Drawings and reports carry a watermark. Steel and precast fabrication features are excluded. Educational models can't be opened in commercial licences, and commercial models opened in it can't go back. https://www.tekla.com/solutions/campus/student-subscription
- The Learning edition is for "educational use… production use is limited". https://support.tekla.com/pl/bulletin/do-not-save-production-model-with-tekla-structures-learning-edition
- Open API under Campus: **[UNCERTAIN]**. Tekla's Open API Fundamentals course accepts a "Tekla Campus license" as its prerequisite, which suggests it works, but nothing states it explicitly. https://credentials.tekla.com/6bed415a-0c8e-4be3-b6ff-91ab641dad43. Neither of you is likely to be eligible anyway.

**Partner / developer**
- The Tekla Partners Program costs about €3,300 per user per year. It includes the AI Developer Assistant and the right to sell apps. https://developer.tekla.com/tekla-structures-for-startups. The Developer Assistant is limited to Diamond named-user or Partners licences. https://support.tekla.com/doc/tekla-structures/not-version-specific/developer_assistant

**Friend's real subscription**
- Subscriptions are named-user and work "on one computer at a time", with up to 3 days offline reservation. https://support.tekla.com/doc/tekla-structures/2025/lic_use_online_license_offline. Technically he could also use it in a VM. Each TeklaStructures.exe running in a virtual environment needs its own valid licence. https://support.tekla.com/doc/tekla-structures/2026/ins_using_tekla_structures_in_a_virtual_environment

## 2. System requirements and virtualisation

- **Tekla 2026** officially supports **Windows 11 64-bit only**, not ARM. Recommended baseline: 16 GB RAM (32 GB for best performance), 1 TB SSD, Core i7, NVIDIA RTX 4060/4070 class. https://support.tekla.com/doc/tekla-structures/2026/ins_tekla_structures_hardware_recommendations
- **Rendering:** DirectX is the default, and legacy OpenGL is under File > Settings > Switches > "Use legacy rendering". DirectX "may not work as expected" over remote connections, for example parts missing or slow, and the fix is to switch to legacy. The docs say DirectX performs worse on "systems without a GPU", which implies it still runs there. https://support.tekla.com/doc/tekla-structures/2025/mod_change_rendering
- Virtualisation is officially supported only as Citrix or desktop virtualisation, with GPU-enabled Azure N-series as the recommended server. https://support.tekla.com/doc/tekla-structures/2026/ins_using_tekla_structures_in_a_virtual_environment, https://support.tekla.com/article/recommended-server-specifications-for-running-tekla-structures-on-citrix
- **KVM, VirtualBox or VMware without a GPU: no Tekla-specific reports found [UNCERTAIN].**
  - Inference: Windows' Basic Display/WARP software renderer plus legacy OpenGL rendering should be enough to open a small model and test the API. The 3D view will be slow. The API test doesn't depend on rendering speed.
  - VirtualBox only exposes OpenGL 2 / DirectX 9 class graphics. https://dspace.lu.lv/handle/7/39715
  - The only hypervisor report found is an old Parallels 13 redraw bug. https://forum.parallels.com/threads/version-13-tekla-structures.342847/
- **Wine, Bottles, CrossOver: no reports of Tekla working.** I found no WineHQ AppDB entry. Treat it as not viable. A .NET Framework CAD app with DirectX, Trimble Identity and licensing services is a poor candidate **[inference]**.

## 3. Windows 11 VM on Fedora 44

- **ISO:** Windows 11 Enterprise Evaluation (26H2 or LTSC 2024) from https://www.microsoft.com/en-us/evalcenter/evaluate-windows-11-enterprise. It runs 90 days, needs no product key, and requires registration. After expiry the desktop goes black and the VM shuts down every hour. The page also says a Microsoft account sign-in is required **[UNCERTAIN: Enterprise usually allows a domain-join/local account option]**. An unofficial rearm trick extends it to about 270 days. https://atmarkit.itmedia.co.jp/ait/spv/2402/28/news010.html
- **Stack:** use virt-manager (KVM/libvirt) rather than GNOME Boxes. In Boxes, TPM and UEFI need XML edits, and the Flatpak build can't emulate a TPM. https://www.ctrl.blog/entry/how-to-win11-in-gnome-boxes/
  - Packages: `edk2-ovmf swtpm swtpm-tools virt-manager`. Use firmware `OVMF_CODE.secboot.fd`, chipset Q35, and an emulated TPM 2.0. https://computingforgeeks.com/enable-tpm-on-kvm-and-install-windows/
  - virt-manager ≥4.0 adds an emulated TPM automatically when UEFI is selected. https://lists.libvirt.org/archives/list/devel@lists.libvirt.org/thread/MMMHFWCJHCOAFSUN6Q4JMSZJ7GZY3GNB
- **Drivers:** stable virtio-win ISO, then `virtio-win-gt-x64.msi` / guest tools. https://fedorapeople.org/groups/virt/virtio-win/direct-downloads/stable-virtio/virtio-win.iso, https://docs.fedoraproject.org/en-US/quick-docs/creating-windows-virtual-machines-using-virtio-drivers/
- **3D:** virgl for Windows guests is still experimental, OpenGL only, and may crash or show a black screen. https://gitlab.freedesktop.org/virgl/virglrenderer/-/merge_requests/1185, https://github.com/virtio-win/kvm-guest-drivers-windows/pull/943. In practice that leaves software rendering (QXL/VirtIO-GPU 2D) or full GPU passthrough, which needs a second GPU.
- **Sizing [recommendation]:** 6–8 vCPU, 16 GB RAM (12 GB minimum), and a 120–150 GB qcow2 disk. Tekla, Visual Studio/.NET SDK, Claude and Windows updates all need space.
- **Cloud alternatives:**
  - Azure NV12ads A10 v5 Windows costs about **$1.46/h** pay-as-you-go in East US (third-party aggregator). https://www.azurespeed.com/AzureVmPricing/Standard_NV12ads_A10_v5
  - Shadow PC costs about $30–55/month **[third-party, unverified]**. https://tech-insider.org/shadow-pc-vs-geforce-now-2026/
  - Caveat: the trial lock makes moving between machines costly.
- **Friend's PC:** the most realistic environment, with a real GPU and his licence. The risk is that you'd be experimenting on his production setup.

## 4. Concrete test plan (about 1–1.5 days total)

1. **Without Tekla, on Fedora (30 min):** run `tempalg1n/tekla-mcp-server`'s `net8.0-mock` build. It serves a synthetic model on any OS, so you can check the Claude ↔ MCP plumbing first. https://github.com/tempalg1n/tekla-mcp-server
2. **Windows VM (2–3 h):** install with TPM and Secure Boot, add virtio drivers, update Windows, take snapshot "clean".
3. **Tekla trial (1–2 h):** create a Trimble ID, install Tekla 2026 plus the Default environment. Snapshot **before** activation. Activate, open a sample model, and switch to legacy rendering if the view is broken. Snapshot again.
4. **Claude Desktop + Claude Code (30 min):**
   - Config file: `%APPDATA%\Claude\claude_desktop_config.json`. Logs: `%APPDATA%\Claude\logs\mcp*.log`. https://modelcontextprotocol.io/docs/develop/connect-local-servers
   - Claude Code: run `irm https://claude.ai/install.ps1 | iex`. Git for Windows is recommended. A Pro or Max plan is needed. https://code.claude.com/docs/en/setup
5. **MCP test (1–2 h):**
   - Use the Tekla build matching the 2026 version, with `TEKLA_MCP_READ_ONLY=1` set.
   - Call `tekla_get_connection_info`, then run read queries: list beams, profiles and weights.
   - Then try a preview write (`apply=false`), and finally one applied change on a copy of the model.
   - Alternatives: https://github.com/teknovizier/tekla_mcp_server (tested with Tekla 2026), https://glama.ai/mcp/servers/YuriyKirillov/TeklaMCPServer
6. **C# macro test (1 h):**
   - Have Claude Code write a `.cs` macro into the `modeling` subfolder of `XS_MACRO_DIRECTORY`, then run it from the Applications & components catalog.
   - Alternatively, have it build a small external .NET app that references the Tekla DLLs.
   - Sources: https://support.tekla.com/doc/tekla-structures/2023/xs_macro_directory, https://developer.tekla.com/doc/tekla-structures/2026/run-macro-method-73267
7. **Verify:**
   - connection to the running Tekla instance
   - read accuracy against the GUI
   - write and undo behaviour
   - CPU/RAM load in the VM
   - which trial limits matter (no exports or drawing printing)
   - Note down every manual step for your friend's install.

## Recommended practices

- **Run read-only first.** Use previews and make writes opt-in (`apply=false`, `TEKLA_MCP_READ_ONLY=1`). Always review the plan before applying. https://github.com/tempalg1n/tekla-mcp-server, https://github.com/teknovizier/tekla_mcp_server
- **Work on a copy of the model.** Save after milestones. A "committed" drawing change isn't saved yet. Same source.
- **Match the server build to the Tekla version.** The API DLLs are version-specific. Tekla has to be running with a model open, and only one instance per version should run. Same source.
- **Page large queries** with `maxObjects`/`cursor`, because the client times out after about 60 s. Same source.
- **Ground generated code** in the official API reference for the exact version (https://developer.tekla.com/tekla-structures). Claude can hallucinate API members. A Tekla MCP listing advertises API-doc semantic search for this reason. https://mcpmarket.com/server/tekla
- **Use the Default environment** when generating code. Tekla's own Developer Assistant recommends it. https://support.tekla.com/doc/tekla-structures/not-version-specific/developer_assistant
- **Claude Desktop:** quit the app before editing the config, use absolute paths with escaped backslashes, and check `mcp.log`. https://modelcontextprotocol.io/docs/develop/connect-local-servers
- **VM:** snapshot before Tekla activation. Never reinstall after activation, because of the per-computer trial lock.
- **Avoid:** Educational licences on production models (they're incompatible both ways), activating the trial on a throwaway VM, and Wine.

## Recommendation

Use **virt-manager + KVM on Fedora with the Windows 11 Enterprise eval** and the **Tekla 2026 30-day trial**, which covers the Open API. Accept software rendering with legacy OpenGL mode. The goal is to prove the Claude ↔ MCP/macro loop, not graphics performance.

Before activating anything, check the MCP plumbing with the mock server. Activate the trial only once the VM is final and snapshotted, and plan the full test into one or two focused weeks.

If Tekla won't start or render usably without a GPU, which is the main **[UNCERTAIN]** risk, fall back to a short session on the friend's PC. Use a model copy and read-only MCP there, rather than paying for an Azure GPU VM.
