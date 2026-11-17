# R9-critic: completeness check over R1..R8 for LibKa0s #75..#92

Read-only. LibKa0s `master` 9bc9cc51 (v1.104.0 + its merge), WowAddonStandards 3dfb951 (v2.112.2). Every claim
marked **verified** was re-checked against code in this pass. Open issue set re-listed with `gh issue list`:
#75, 76, 78-92 are open, #77 is closed, so the notes cover the full set.

---

## 1. Corrections: notes that are wrong or overstated

| # | Note | Claim | What the code says | Effect |
|---|---|---|---|---|
| C1 | R2 §2 row 21, Q-list | `OptionsSkinPicker.lua:487` (`ANCHOR_TOP`) is a Settings-canvas widget and out of scope | **Wrong, verified.** The picker is a standalone frame on `UIParent` at DIALOG strata (`OptionsSkinPicker.lua:1260,1264`), with its own close and `S.Header` (R4 §1.1). `attachTip` (`:483-499`) is used at `:1072`, `:1089` (the gear and eye buttons on the dropdown row) and `:1169` (the dropdown button). Those are toolbar controls, so top chrome: the rule wants them attached and centered **below**, and `ANCHOR_TOP` puts them above. Its own dropdown list (`:1100-1131`) is a library-drawn menu. | #92's library-move list gains the skin picker (PICKER_MINOR 11 -> 12). It is the same file #86 edits, and it is at 1493 lines (see M1). |
| C2 | R4 Q5 | Add a one-line tooltip on every header mark, the console's too | Conflicts with a documented design decision, **verified** at `DebugLogWindow.lua:192-197`: "NO TOOLTIP ... Minor 9 took a label and showed it under the control, which put it on top of the first line of the log". The chrome rule places a title-bar tooltip **directly below** the title bar, which is exactly that failure. | Owner decision (D5 below). My recommendation: header-mark tooltips on every library window except the console, or none in this run. |
| C3 | R2 §4.1 | Tooltip would be "one more major (twenty)" | **Verified:** `tests/majors.lua` lists **24** majors. Tooltip is the **25th**. | Doc counts. PanelMaster CLAUDE.md:46 and PrettyChat ARCHITECTURE.md:487 (R8) already go stale at 24 and go staler. |
| C4 | R3 §1, §7 | Adding `Report`/`Serialize` turns parity red in "every addon" | **Verified by grep of every repo's tests:** a by-name DebugLog parity case exists in **14 of 19**: AT, AM, BL, KC, ST, LH, PM, PFE, PGFE, PC, QC, SM, WG, DW. CT, CM (projected seam), DR, MM and OR have none. | Fix count is 14 stub edits, not 19. |
| C5 | R5 §5 | "No host fallback copies `icon.hot`" | **Wrong, verified:** LootHistory `core/SkinSetup.lua:169` and DropWatcher `:189` copy `icon.hot = {1,1,1,1}`. | Harmless, because R5 leaves Ka0s Default's `icon.hot` white. It would bite only if the owner moved Ka0s Default's hot. |
| C6 | R8 §1 (DW), §4 | DW's re-vendor is "copy only, expected green" | True for v1.104.0 only. At the run's new tag, DW also takes the DebugLog stub members (C4), its `SKIN_FALLBACK` `list.stripe` (R5: `core/SkinSetup.lua:185`), and DW's own skin tests may pin per-skin `icon.hot`. | DW is a real re-vendor, and another session holds its checkout (§4). |
| C7 | R1 #90 vs R3 vs R4 | Three different DebugLog keys: R1 `22.10.1.5`, R3 `23.11.1.5`, R4 only "Window 4->5" | All three issues edit `DebugLogWindow.lua`. #79 also bumps the shell and Diagnostics. | **One key: `23.11.1.5`**, with one doc and one members JSON. R1's "shell stays at 22" no longer holds once #79 lands. |
| C8 | R4 §1.2 | "Every library window gets a working settings mark from the re-vendor alone, zero addon edits" | It works only if the Launcher's registry key (`d.owner or d.name`, `Launcher.lua:373`) equals the window descriptor's `addonName`. DebugLog itself warns "Do NOT pass `d.name` blindly" (`DebugLog.lua:221`). In 8 addons I confirmed `name = addonName`, and the rest were not caught by my grep window. | Add a library test that the lookup goes through `addonName`, and check each host at re-vendor. If a host's Launcher name differs, the settings mark silently does nothing. |
| C9 | R7/R8 inventories | The predicted red list | Measured against **v1.104.0**, not the tag this run cuts. | §3 below adds the new-tag fallout. |

Verified as stated: #75 half 1 is done (`367a9f10`, `testkit/mock_ace.lua:110-128` guarded). `frameSet` is weak (`mock_base.lua:259`). The console has no GameTooltip anywhere in `DebugLog*.lua`. `Kit.VERSION = 56`. LibDBIcon MINOR 52 has `lib:GetMinimapButton` (`:456`) and `getAnchors` (`:51`). SkillMaster and CombatTrail default to `main`. `assertSurfaceParity` by name fails on any public live member the stub lacks (`testkit/asserts.lua:288-330`). Every addon has a Launcher with `openSettings`. Every addon declares the `settings` and `copy` icons.

## 2. Things no note covered

- **M1: `OptionsSkinPicker.lua` is already past its own peel trigger.** It is at 1493 lines. LibKa0s `CLAUDE.md:80` (row `FX-LK-SIZE`) sets its trigger at **1400**, with the seam "the queue, to a file of its own". #86 (gear into the header) and #92 (C1) both edit it. **The peel has to come first.** It is a payload peel, so it rides this run's release.
- **M2: `tests/test_launcher.lua` is at 1235, past its 1200 trigger** (CLAUDE.md:267, seam "the tooltip follows the skin" section). #81, #86 (registry) and #92 (launcher placer) all add launcher cases. Peel it first. It is a suite, so the peel is no release.
- **M3: `tests/test_debuglog.lua`** (1002; trigger "the next console case added", R1). #79, #86 and #90 all add console cases. **One peel, before any of the three.**
- **M4: `WidgetsDragHandle.lua` is at 1022, with a 1100 trigger and the named seam "its tooltip half"** (CLAUDE.md:286). #92 rewrites exactly that half, so the natural move is to peel it (into the new Tooltip major's helpers, or a `WidgetsDragHandleTip.lua`) as part of #92, and not to grow the file. `Skin.lua` is at 1121, past its 1100 trigger. No issue here needs Skin.lua, so keep #82/#84 to `SkinDefs*.lua`. `IconBrowser.lua` is at 958 and `OptionsWidgets.lua` at 1164, and R2's Q7 `AttachTooltip` opts would grow the latter.
- **M5: library-stack-§7 bar 1 for #80 and #81.** Both have one consumer (SkillMaster). The standard (`library-stack.md:318-334`) says a one-consumer promotion SHOULD wait for a second consumer, unless **the owner rules it a suite-wide component**, and that ruling MUST be recorded in the API doc and the CHANGELOG with who, when, where and the consumer. R4 does not mention this. Possible second consumers: DW (a launcher extra for its rolls panel?), and the AT, MM and DR bar rows for #80.
- **M6: new payload files reach three hand-written loader lists.** PGFE `tests/loader.lua`, WG `tests/loader.lua` and SkinTester `tests/loader.lua:24` are pinned to `LibKa0s.xml` (R7, R8). Besides the v1.95-v1.99 files, they now also need `Tooltip.lua`, `WidgetsHeader.lua` and `WidgetsBar.lua`, plus any peel file (M1, M4), in XML order.
- **M7: Launcher parity is checked by name in 9 addons** (AT, AM, ST, PM, PGFE, QC, SM, WG, DW), against the Launcher **instance**. #81, #86 and #92 must stay member-neutral on the instance (descriptor fields and internal hooks only), or budget 9 stub edits. **Sim parity is by name in 5** (BL, KC, LH, SM, DW): any Sim lib member (#87's `SAMPLE` data, or a new SimPanel export) costs 5 stub edits. R6 missed this. **Options helpers are parity-checked in all 19**, so no new Options helper in this run (keep #92's Q7 to an extra argument). **Core is checked by no one**, so R4's registry is safe there.
- **M8: the re-vendor skill vs. "no adoption".** `/dev-copilot:wow-revendor-libka0s` goes on to interview for adoption candidates and **files each decline as a GitHub issue**. Workflow agents cannot write to GitHub in auto mode (memory `subagent-push-refused`), and the owner deferred adoption. The plan must run only the copy, gate and bundle half, and record the candidates as "deferred, tracked by #79/#86/#88/#89/#92".
- **M9: a compliance cliff at re-vendor.** standalone-windows *Tooltip placement* says (verified): "From an addon's re-vendor of the tag that ships the surface, every placement it makes goes through the placers". So re-vendoring 19 addons this run makes every one of them non-compliant (#47/#119) until the deferred adoption lands. R4's proposed #86 rule ("MUST once the addon vendors v1.105.0") and the existing v2.110.0 strip and footer MUSTs (R8) do the same. The standard edit in this run should say what an addon owes between re-vendor and adoption: either the open issue is the record (R8's Q5), or the trigger is the addon's next feature change.
- **M10: help icon.** 12 addons do not declare `help` (BL, CT, DR, ST, LH, MM, PM, PFE, PGFE, PC, SM, WG). If any `W.HeaderButtons` default or library window uses a `help` extra, it draws blank (`Media.Icon` never checks the file). Keep the library windows to `settings`, `close`, `copy` and `clear`, or add the icon-declaration edit to every re-vendor.
- **M11: concurrent sessions.** DW's live branch `feat/2026-11-16-loose-ends` changes `modules/RowTooltip.lua` and `tests/test_row_tooltip.lua` ("RX-28 ... row tooltip group"). That is the prior art R2 designs from, and it is in flux. Re-read it after that branch merges, before #92's API is fixed. WowAddonStandards has another session's worktree on `feat/2026-11-10-per-client-quirks`. Expect a version collision on the standard (memory `standard-version-collisions`): fetch and renumber at finalize.
- **M12: visible changes reach players at re-vendor, with no adoption.** These are: seven skins' `icon.hot`, Ka0s Default's rows, the console footer, the settings marks on library windows, beside-the-menu dropdown tips, the 2 px minimap gap, icon browser and sim panel tips, and DragHandle tips on hosts with no `tooltipPlace` hook. If owner smoke rejects any of them after 19 re-vendors, the tag is re-cut and the re-vendor is redone 19 times (the v1.78.0 re-cut precedent). **Run a smoke gate through one or two hosts (SkinTester plus one HUD host such as AbsorbTracker) before the sweep.**
- **M13: the tag stays local until the owner says go.** The re-vendor copies from the tag, and the vendor-sync gate reads `../LibKa0s` at it. So cut the tag locally, re-vendor against it, and push only on the owner's go-ahead. A re-cut means moving a local tag and redoing each re-vendor commit.
- **M14: #78's dev-copilot nits.** A dev-copilot release does nothing for this run until the owner updates the installed plugin (memory `use-installed-plugin`). Keep it a leaf item, off the critical path.

## 3. New-tag fallout to add to the R7/R8 re-vendor tables

Each item goes into the re-vendor commit so the gate holds:

| Cause (issue) | Repos | Fix |
|---|---|---|
| DebugLog instance gains `Report`, `Serialize` (#79) | AT AM BL KC ST LH PM PFE PGFE PC QC SM WG DW (14) | two stub members (R3 §2.4) |
| Ka0s Default `list.stripe`/`list.hover` move (#84) | LH (`core/SkinSetup.lua:137-138`), BL (`:172-173`), DW (`:185`) | re-copy the fallback values |
| Per-skin `icon.hot` pins (#82) | possibly SM `tests/test_round2_icons.lua`, `test_round8.lua`; DW `tests/test_skin_chrome.lua`; OR `tests/test_skinsetup.lua` | re-pin where red |
| OR `of.bar.worn` follows `icon.hot` (#82) | OR `core/SkinSetup.lua:139` | turns white under WoW, Midnight and Forever. Repoint to `text.accent` (R5 D-7). This is a meaning change, not a red test |
| New payload files (#92, #86, #80, peels) | PGFE, WG, ST hand loaders | XML-order lines (M6) |
| Kit rev 57 (#75 hold-while-registered) | all | a full-suite run. A suite that relied on GC dropping a frame turns red (R1 risk) |
| Footer/strip/tooltip/header MUSTs now owed | all | named in each re-vendor report (M9) |
| Already known from R7/R8 at v1.104.0 | `SideTabs` (15 hosts), Compat members (MM PGFE WG), MM settings pin, sound prune, span bundles | unchanged |

## 4. Cross-issue interactions

- **`DebugLogWindow.lua` is touched three times:** #79 (`rebuildLog` reads `__view`), #90 (body and footer) and #86 (title bar through `W.HeaderButtons`). Build them in one milestone after the M3 peel, with one WINDOW_MINOR bump (4 -> 5) and one console smoke. #90's minimum height (TITLE_H + lines + 24 + 4) and #86's header height share one derivation.
- **#86 depends on #92** if header marks have tooltips. Chrome-rule placement comes from #92's attached placer, so build #92 first and have `WidgetsHeader` call `Tip.PlaceAttached`. Without tooltips, #86 is independent.
- **#82 before #86:** the header marks tint from `icon.tint` and `icon.hot`, which #82 changes. Smoke them together.
- **#86 + #92 + the M1 peel all hit `OptionsSkinPicker.lua`:** peel first, then #92's three `attachTip` sites, then #86's gear move (`anchorDropdown` re-anchor). Bump PICKER_MINOR once.
- **#92 and #86 both may touch `WidgetsDragHandle.lua`:** #92 changes the default placement, and #86 makes the settings mark opt-in. Bump DRAG_MINOR 13 -> 14 once, together with the M4 tooltip-half peel.
- **The Launcher is touched three times:** #81 (`extraEntries`), #86 (registers the opener) and #92 (`drawTooltip` re-places). Bump Launcher 10 -> 11 once, after the M2 peel, and keep the instance member-neutral (M7).
- **SimPanel is touched three times:** #78 (`PANEL_TITLE` in `lib.STRINGS`) and #92 (`showTip`) in `SimPanel.lua`, and #86 in `SimPanelRender.lua` (`S.Header` and settings). One Sim key move. Confirm the key's segment order in `tests/majors.lua` before writing the doc name. R1's `2.3.11.3` plus R4's render 3 -> 4 is probably `2.3.11.4`.
- **The kit moves twice:** #75 (hold-while-registered) and #92 (R2's `mock_screen.lua`). One revision, **57**, one `version-57-docs.md`.
- **#90 and #92:** the footer grip is bottom chrome, and the console footer has no marks, so nothing to place. #92 Q9 (`spec.tooltip` on Footer marks) is the only thing that would move the Widgets shell to 28. Leave it out, because #86's two new Widgets files can pair on shell 27 (check `tests/majors.lua` pairing; R4 says 27 or 28).
- **#88 and #86:** a `dock="title"` strip sits under the title bar that `W.HeaderButtons` lays out. They do not conflict in library windows, because none draws a test strip. They matter for addon adoption only.
- **#79 and #90:** `Report` writes many lines, so the footer counter's `N / 3000` is exercised, which helps smoke. There is no code coupling.
- **#84 and #82:** both are SkinDefs-only, with one Skin key move (DEFS 27 -> 28, OTHERS 9 -> 10) and one red-first test pass in `tests/test_skin_defs.lua`.
- **#80 and #92:** the Bar's `tooltip` preset draws on GameTooltip, but SkillMaster's RowTooltip places it, so placement is the host's at adoption. No coupling in the library.
- **Standard sequencing:** #79's issue says the rule "lands first". That means before the rollout audit, so landing it with this run's standard release is enough. #92's "future surface" text can only name the major, file and minor **after** the tag exists. #81 amends launcher-§2. #86 is a new standalone-windows bullet. #82/#84 add an optional skinning bullet. #90 changes debug-logging-§11's wording. #78 is M-2 and M-4. That makes **one standard minor (v2.113.0)** after the local tag and before the re-vendor, so each re-vendor report can cite it. Renumber at finalize.

## 5. Combined LibStub moves for one tag (v1.105.0)

| Major / file | Now | After | Issues |
|---|---|---|---|
| **LibKa0s-Tooltip-1.0** `Tooltip.lua` (new) | — | 1 | #92 |
| Core | 17 | 18 | #86 (registry) |
| Launcher | 10 | 11 | #81 + #86 + #92 |
| DebugLog shell / Diagnostics / Gates / Window | 22 / 10 / 1 / 4 | **23 / 11 / 1 / 5** (key `23.11.1.5`) | #79 + #90 + #86 |
| Sim: SimPanel / SimPanelRender | 10 / 3 | 11 / 4 | #78 + #92 / #86 |
| Widgets: WidgetsDropdown, WidgetsReorder, WidgetsDragHandle, WidgetsCopyWindow | 1, 6, 13, 5 | 2, 7, 14, 6 | #92, #92, #92 (+#86 opt-in), #86 |
| Widgets: WidgetsHeader, WidgetsBar (new) | — | 1, 1 | #86, #80 |
| Widgets shell | 27 | 27 (28 only if a shell helper is needed) | — |
| IconBrowser / IconBrowserWindow | 1 / 1 | 2 / 2 | #92 / #86 |
| Charts / ChartsRender | 1 / 1 | 2 / 2 | #92 |
| Options: OptionsSkinPicker (+ peel file) | 11 | 12 | M1 + #92 + #86 |
| Perf: PerfPanel | 13 | 14 | #86 |
| Skin: SkinDefs / SkinDefsOthers | 27 / 9 | 28 / 10 | #84 / #82 |
| Kit | 56 | 57 | #75 + #92 |

## 6. Proposed build order (one branch, one local tag, checkpoints)

1. **M0 hygiene** (no behavior change): suite peels `test_debuglog` (M3) and `test_launcher` (M2), and the payload peel of `OptionsSkinPicker` on its queue seam (M1). Gate green after each.
2. **M1 cheap fixes:** #75 kit rev 57 (hold while registered, R1 option A); #78 SimPanel `PANEL_TITLE` "SIM"; #82 and #84 skin values, red first in `test_skin_defs.lua`. These are independent, low risk and easy to smoke.
3. **M2 DebugLog:** #79 (plain Copy plus `__view`, `D:Report`, `Serialize`), then #90 (footer). Both bump the shell, Diagnostics and Window once.
4. **M3 Tooltip major #92:** first re-read DW's merged RowTooltip (M11). Then `Tooltip.lua` plus the solvers, the kit `mock_screen`, and the library moves: IconBrowser, Dropdown, Reorder, SimPanel `showTip`, DragHandle (with the tooltip-half peel, M4), Charts (additive ctx seam), Launcher `drawTooltip`, and the skin picker's three sites (C1). Finish with the grep-guard test.
5. **M4 header buttons:** #86 (`WidgetsHeader`, Core registry, the six window migrations), then #81 (`extraEntries`, same Launcher minor).
6. **M5 (optional, the first thing to drop if tokens run short):** #80 `W.Bar`, dead code until SkillMaster adopts. It needs the bar-1 ruling (M5 in §2).
7. **M6 release record:** docs/api for every moved key, CONSUMERS, CHANGELOG, automated-tests bundle, **local** tag v1.105.0. Standard v2.113.0 on its own branch (§4 standard sequencing).
8. **M7 smoke gate before the sweep (M12):** re-vendor SkinTester plus one HUD host. The owner smokes both clients. Fixes re-cut the local tag here, cheaply.
9. **M8 re-vendor sweep:** 18 repos (DW last, after the other session merges; R8 Q1). Copy, gate and bundle only (M8 in §2), each with the §3 fixes.
10. **M9 finalize** on the owner's go-ahead: push the tag, merge `--no-ff`, push, delete branches.

Not built this run: #76 (upstream blocked), #83 (needs its own brainstorm), #85 (adoption evaluation), #91 (close it, file follow-ups), #87 (unless ruled "both", and then budget the 5 Sim stubs), #88/#89 (adoption only).

## 7. Owner decisions that change what gets built, ranked

1. **Library scope for this run.** Build #80 and #81 under a recorded "suite-wide component" ruling (library-stack-§7 bar 1), or defer them until a second consumer exists? *Recommend: #81 yes (small, ruled one-consumer), #80 deferred or last (M–L effort, dead code, token budget).* Also confirm #83 and #87's library half are out.
2. **What an addon owes between re-vendor and adoption (M9).** The standard already makes tooltip placement through the placers due at re-vendor, and R4 proposes the same for header buttons. *Recommend: the standard edit says adoption is owed by the addon's next change, tracked by #88/#89/#92/#86, and re-vendor reports name it. No deviation rows.*
3. **#82 scope:** change `icon.hot` in all seven failing skins plus the hot-vs-heading invariant (a visible redesign of signed-off skins), or Forever only? *Recommend all failing skins with the suite floors (R5), plus the High Contrast exemption.*
4. **#86 shape:** order `[extras][settings][close]`; settings from a Core registry filled by the Launcher; icon browser opts out; DragHandle opt-in; **no tooltip on the console's marks** (C2). *Recommend as stated.* If the owner wants tooltips everywhere, #86 must wait for #92 and the console's documented rationale has to be overruled.
5. **#92 HUD strips are top chrome** (standard reading), and DragHandle's `tooltipOwner="cursor"` and `tooltipAnchor` are retired to the attached placer. *Recommend confirm.* This changes visible behavior at re-vendor on any host without a `tooltipPlace` hook.
6. **#79 detail:** keep view colors across a skin switch through a private `__view` (yes), and put `Serialize` on the instance (yes: two stub members in 14 repos).
7. **#90:** footer, not deviation; counter in `text.muted`, mono, 4-line minimum. *Recommend as R1.*
8. **One tag with a pre-sweep smoke gate**, or two tags (fixes, then surfaces)? *Recommend one local tag with the M7 gate. It is cheaper than two release records, and the gate removes the re-cut risk.*
9. **CombatTrail in the sweep** (yes) and **DW timing** (last, after the other session merges).
10. **Move each addon's standard pointer to v2.113.0 in this run?** *Recommend no.* It is `/dev-copilot:wow-revendor-standards`'s job, and it would turn every deferred MUST into an audit deviation now.
