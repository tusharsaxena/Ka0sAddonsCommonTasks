# R8-consumers-b: re-vendor inventory, part B

Scope: MultiMeters (MM), OutfitterReborn (OR), PanelMaster (PM), PartyFrameEnhanced (PFE),
PremadeGroupsFilterExtension (PGFE), PrettyChat (PC), QuickComms (QC), SkillMaster (SM), WhatGroup (WG),
DropWatcher (DW, read-only through `master`). Target: LibKa0s **v1.104.0** (tag; LibKa0s `master` is
`9bc9cc51`, one merge past the tag), kit revision **56**, 24 majors.

Method. Repo state came from `git status/branch/stash/worktree`. The vendored tag came from the CLAUDE.md
provenance line, and I **verified it byte for byte**: `git ls-tree -r <branch>:libs/LibKa0s`, minus
`media/icons/` and `media/sounds/callout/`, matches `LibKa0s <tag>:LibKa0s` with 0 differing lines for every
addon. The kit revision is `Kit.VERSION` in `tests/_kit/framework.lua`. I ran the green gates on the real
checkouts, which are read-only and were confirmed clean afterwards. Then I ran a **simulated re-vendor**: a
`git archive` copy of each default branch went into the scratchpad, I copied in v1.104.0's `LibKa0s/` and
`testkit/`, rolled the provenance line, ran the tag's `tools/prune-icons.lua`, `git init`-ed the copy (the
vendor gate reads the index) and put a symlink to the real `../LibKa0s` for the sibling gate. Then I ran the
same gates. DW was not run. No real repo was edited.

Correction to the brief: **PGFE is at v1.93.0, not v1.75.0.** Its CLAUDE.md:52 reads `Bundles [LibKa0s](…)
v1.93.0 (MIT).` and the tree matches v1.93.0 exactly. CLAUDE.md:28-29 ("landed at LibKa0s v1.75.0, kit 41,
closing #25") is history text. PGFE's jump is the same as MM's and WG's, v1.93.0 to v1.104.0, kit 53 to 56.

## 1. The inventory table

| Addon | Default branch | Clean? | Unmerged / stashes / worktrees | Vendored tag (CLAUDE.md line) | Kit | Gate (from CLAUDE.md) | Master green today | Simulated v1.104.0 re-vendor | Fixes the re-vendor owes |
|---|---|---|---|---|---|---|---|---|---|
| MM | master (`d6dd163` = origin) | yes | none / none / none | v1.93.0 (CLAUDE.md:62) | 53 | `lua tests/run.lua` + `ka0s-bounded luacheck .` (:57-58); Retail-only, no forever run | 2589 pass / 0 fail / 1 skip; luacheck 0/0 (190 files) | **3 FAIL**: Settings pin (`window.columnHeader.font` choices gain Bebas Neue + Russo One); Options stub parity (`SideTabs` missing); Compat parity (`CharacterKey`, `RealmKey`, `RegionalNames`, `UnitCharacterName` missing) | re-pin `tests/test_settings_pin.lua`; add `SideTabs` to the `settings/OptionsSetup.lua` stub (or ignore it with a reason); add the 4 Compat members to `NS.Compat` (or ignore them with a reason) |
| OR | master (`6fea14a`) | yes | none | v1.94.0 (:44) | 53 | retail + `KA0S_KIT_CLIENT=forever` + luacheck (:38-40) | R 1563/0/31; F 1542/0/52; 0/0 (204) | **1 FAIL** (both clients): Options stub parity, `SideTabs` | Options stub `SideTabs` |
| PM | master (`c2244af`) | yes | none | v1.94.0 (:59) | 53 | retail + forever + luacheck (:37-39) | R 1201/0/1; F 1201/0/1; 0/0 (86) | **1 FAIL** (both): "Options seam's degraded surface", `SideTabs` | Options stub `SideTabs`; CLAUDE.md:46 says "Twelve of the twenty-one majors in the vendored v1.94.0 payload", which goes stale (24 majors) |
| PFE | master (`a725418`) | yes | none | v1.94.0 (:42) | 53 | retail + forever + luacheck (:36-38) | R 657/0/1; F 657/0/1; 0/0 (92) | **1 FAIL** (both): Options stub, `SideTabs` | Options stub `SideTabs` |
| PGFE | master (`9dcaa4b`) | yes | none | **v1.93.0** (:52) | 53 | retail + luacheck (:46-47); Retail-only | 548/0/1; 0/0 (73) | **3 FAIL**: harness "explicit LibKa0s list matches LibKa0s.xml" (expected 77, got 72); Options stub `SideTabs`; Compat arm (4 members) | add 5 lines to `tests/loader.lua` (Role after Compat; Callout, CalloutSettings, WaypointArrow, WaypointArrowSettings after Toast); `SideTabs`; the 4 Compat members |
| PC | master (`dca5ec2`) | yes | none | v1.94.0 (:45) | 53 | retail + forever + luacheck (:39-41) | R 694/0/1; F 694/0/1; 0/0 (70) | **1 FAIL** (both): Options stub `SideTabs` | `SideTabs`; `docs/ARCHITECTURE.md:487` says "Ten of LibKa0s's twenty-one majors", which goes stale |
| QC | master (`8b5bdc7`) | yes | none | v1.95.0 (:45) | 54 | retail + forever + luacheck (:38-40) | R 2030/0/1 (16 shards); F same; 0/0 (180) | **1 FAIL** (both): Options helpers stub `SideTabs` | `SideTabs` |
| SM | **main** (`19ed391`) | yes | none | v1.101.0 (:40); has `LibKa0s sounds: none.` (:42) | 56 | `KA0S_KIT_CLIENT=forever lua tests/run.lua` + luacheck (:35-36); Forever-only, pinned by `tests/client_pin.lua` | 739/0/1; 0/0 (147) | **GREEN** (739/0/1 both runs; 0/0) | none for green. Owes the v1.102.0 Callout notes (not consumed) and the v1.103.0 Widgets notes (4 undocked strips, a footer) as adoption |
| WG | master (`ce354d2`) | yes | none | v1.93.0 (:48) | 53 | retail + luacheck (:42-43); Retail-only | 1103/0/1; 0/0 (77) | **3 FAIL**: harness "same number of library files" (77 vs 72); Options stub `SideTabs`; Compat reader arm (4 members) | same as PGFE: `tests/loader.lua` gets 5 lines, plus `SideTabs` and the Compat members |
| DW | master (`cd43355` = origin) | **no: the checkout is on `feat/2026-11-16-loose-ends`, with 22 modified files** (another session is live; the last commit was "RX-27…" about 30 min before this read) | `feat/2026-11-16-loose-ends` (local and origin, 3 commits ahead, unmerged) | v1.103.0 (:46), no sounds line | 56 | retail + forever + luacheck (:39-41) | not run (brief) | not run. Delta is only `Callout.lua` and `CalloutSettings.lua` (4.5); DW does not consume Callout and has no sounds line, so the copy is byte-trivial; expected green | none expected; it is the reference consumer of Footer and docking (`core/WidgetsSetup.lua:88-134`) |

Every simulated run kept luacheck at 0/0, and the vendor-sync gate passed in every simulated copy once the
provenance line was rolled and `prune-icons.lua` had run. `prune-icons.lua` reports
`sounds none (no LibKa0s sounds: line); kept 0, removed 362` for each addon.

## 2. What the jump brings, per span (LibKa0s CHANGELOG + `docs/releasing.md` step 8, lines 284-374)

Payload code files that differ (`git diff --name-status <tag> v1.104.0 -- LibKa0s`, `media/` excluded):

- **v1.93.0 → v1.104.0 (MM, PGFE, WG):** A `Role.lua`, `Callout.lua`, `CalloutSettings.lua`,
  `WaypointArrow.lua`, `WaypointArrowSettings.lua`; M `Compat.lua` (4), `DebugLogDiagnostics.lua`,
  `Launcher.lua` (10), `LibKa0s.xml`, `Media.lua` (13), `OptionsNav.lua` (7), `OptionsWidgets.lua` (46),
  `Skin.lua` (18), `SkinDefsOthers.lua` (9), `Widgets.lua` (27).
- **v1.94.0 → (OR, PM, PFE, PC):** the same set without `Compat.lua` and `Skin.lua`.
- **v1.95.0 → (QC):** also without `Role.lua` and `Launcher.lua`.
- **v1.101.0 → (SM):** `Callout.lua`, `CalloutSettings.lua`, `Widgets.lua`.
- **v1.103.0 → (DW):** `Callout.lua`, `CalloutSettings.lua`.
- Kit: 53 → 56 (MM, OR, PM, PFE, PGFE, PC, WG); 54 → 56 (QC); SM and DW are already at 56. The kit trees match
  v1.93/v1.94 (53), v1.95 (54) and v1.97+ (56).

Consumer-owes items, and whether each one bites this group:

1. **v1.94.0 Compat minor 4:** four new members. This **bites MM, PGFE and WG**, through the Compat
   parity suites (simulated FAIL). OR, PFE and QC already wire `UnitCharacterName`/`CharacterKey`.
2. **v1.94.0 Skin minor 18, `DefaultSkin()`.** The standard says "An adopted addon's profile defaults MUST
   name that answer" (skinning.md:36, a MUST). MM, PGFE and WG have **0 `DefaultSkin` references**, so they
   are non-conformant after the jump. On Retail-only addons the answer is still `"ka0s"`, so behaviour does
   not change; this is a doc/audit item, not a red test.
3. **v1.95.0 Role.lua, v1.96.0 Callout pair, v1.99.0 WaypointArrow pair.** These are new payload files, so
   a consumer whose tests load library files by name must add loader lines. This **bites PGFE and WG**
   (`tests/loader.lua` hand list, checked by `tests/test_harness.lua:74` / `:51`). MM, OR, PM, PFE, PC and SM
   read `LibKa0s.xml`, so they need nothing. QC's harness reads the xml and passed.
4. **v1.96.0 kit 55, sound subset.** No line means none. Nobody here adopts Callout, so no addon needs a
   `LibKa0s sounds:` line (NEW_ADDON_CONTEXT.md:1832 says "No `LibKa0s sounds:` line, unless the addon adopts
   Callout"). SM's explicit `LibKa0s sounds: none.` is harmless but is not the canonical form. Someone
   should ask whether the audit counts it as a deviation.
5. **v1.97.0 Media minor 13:** +2 faces (35). This **bites MM's settings pin** (one font row's choice list).
   The other suites that snapshot font lists passed.
6. **v1.99.0 `media/waypoint/` ships whole:** +456 KB per addon, plus 2 fonts (+100 KB plus their OFL texts).
   That is not pruneable today. It is a size note for the owner, not a failure.
7. **v1.100.0 OptionsNav minor 7:** the Options instance gains `SideTabs`. This **bites every addon here
   whose Options stub has a parity suite**, which is everyone below v1.100 (MM, OR, PM, PFE, PGFE, PC, QC,
   WG): 8 of 10. It is the one fix the whole group shares.
8. **v1.101.0 OptionsWidgets minor 46:** slider-box junk text is reverted on Enter and on focus loss. This
   changes behaviour on every number row, but no test failed. Add a smoke line: type junk into a slider box.
9. **v1.102.0 Callout look defaults:** nobody in this group consumes Callout (0 `LibKa0s-Callout-1.0`
   refs), so it is a no-op.
10. **v1.103.0 Widgets minor 27, Footer and docking.** Nothing breaks: an undocked strip is minor 26's. But
    WowAddonStandards v2.110.0 turns "strip docked" and "window footer = `W.Footer`" into **MUSTs from this
    re-vendor**, and releasing.md:362-367 says "Each affected host's re-vendor report names the move".
    Those are LibKa0s#88 and #89, which the owner has deferred. The re-vendor reports must therefore name
    them as owed, and each affected addon (MM, OR, SM, plus any window footer) carries a known
    non-conformance until #88/#89 adoption lands. The "Preview and simulation re-look" line in v1.103.0's
    entry also asks every strip host to re-look at placement at re-vendor; that goes in the smoke sheet.
11. **Unrecorded tags.** OR, PM, PFE and PC vendor v1.94.0 but their latest `docs/revendor/` bundle is
    `2026-11-07-v1.93.0`. `/dev-copilot:wow-revendor-libka0s` will therefore want a consolidated span
    bundle (`…-v1.94.0-v1.104.0`) plus the per-tag one. MM, PGFE, WG, QC, SM and DW have their last tag
    recorded.

## 3. Adoption-site counts (addon source only: `*.lua` minus `libs/`, `tests/`, `tools/`, `docs/`, comment lines excluded)

| Addon | `SetOwner(` sites (anchors) | Files | DevTools_Dump | Report-verb candidates (multi-line; `list` stays in chat by the 2026-11-08 ruling) | Own footer / status line | TestStrip calls (docked?) | Own window title-bar buttons |
|---|---|---|---|---|---|---|---|
| MM | 2 (ANCHOR_TOP via `ANCHOR_TOKENS`, ANCHOR_RIGHT), plus a player-chosen anchor table | `modules/Tooltip.lua:610`, `settings/ColumnBlocks.lua:177` | 0 | `export`, `profile`, `window` (verify) | meter window header/status via `modules/Window_Header.lua`; no `Footer` | 2 (`modules/Window_Frame.lua:215,388`), **undocked**, placed by its own `PlaceTestStrip` (`Window_Header.lua:865`) | yes: `modules/HeaderControls.lua:124` (close/lock/... set), `modules/Export_Modal.lua:212-218` |
| OR | 10 (RIGHT 7, LEFT 1, TOP 1, NONE 1) | Bar_Buttons, Bar_Chrome, Dock, OutfitTooltip, Tooltips_Compare, Window_Rows | 0 | `missing`, `iteminfo`, `zone` (verify) | hand-built footers: `modules/Dialog_Outfit.lua:226`, `Dialog_Trigger.lua:232`, `Window.lua:60` (`selectedFooter`) | 2 via `NS.MakeTestStrip` (`Bar_Chrome.lua:244`, `Window.lua:132`), **undocked** | yes: `Bar_Chrome.lua:219` close, `Window.lua:224` close + `:241` gear, `UIDialogs.lua:150` |
| PM | 0 | none | 0 | `panels` (verify) | none | 0 | none of its own (the settings panel only) |
| PFE | 0 (1 `ANCHOR_` value, not a SetOwner) | none | 0 | `status`, `current` (verify) | none | 0 | none |
| PGFE | 2 (RIGHT) | `settings/Panel.lua` | 0 | none obvious | none | 0 | the attached panel only (no close beyond CoreSetup's seam) |
| PC | 1 (RIGHT) | `settings/Panel.lua` | 0 | none obvious | none | 0 | none |
| QC | 8 (TOP 5, RIGHT 2, NONE 1), 1 cursor ref | Dial_Render, Pad, Pad_Render, PreviewWindow, CalloutPopup, Groups_When | 0 | `check`, `probe`, `why` (verify) | none | 0 (preview window has no strip) | `modules/PreviewWindow.lua`, `settings/ModalWindow.lua` (own close) |
| SM | 8 (RIGHT 3, TOP 2, NONE 2, BOTTOM 1), 1 cursor ref | Bonuses, Broker, Chrome, Journal, RowTooltip, TrainerPopup, WaypointArrow | 0 | `probe`, `journal` (verify) | hand-built: `modules/BrokerPanel.lua:275-354` (`frame.footer` FontString) | 4 (`BrokerPanel.lua:263`, `Journal.lua:865`, `MainWindow.lua:255,262`), **undocked** | yes: `Journal.lua`, `MainWindow.lua`, `TrainerPopup.lua` |
| WG | 1 (RIGHT) | `modules/Frame.lua` | 0 | none obvious | none | 0 | the popup's own title bar: `modules/FrameLayout.lua` (12 refs) |
| DW | 3 (NONE 3; BOTTOM 1 more) | RollsPanel, Window, WindowGroup | 0 | `history`, `insights`, `scan`, `situation`, `rolls` (verify) | **already `W.Footer`** (`core/WidgetsSetup.lua:116-121`, `modules/Window.lua:536-558`, `OfferPanel.lua:216`) | 9, **docked** (`MakeTestStrip(..., dock)`; RollPopup and Toast use `{ target = f }`) | yes: `modules/WindowTitleBar.lua`, DetailCard, OfferPanel, RollsPanel (the #86 example) |

Notes on the counts. **No addon in this group calls `DevTools_Dump`**, so for these ten the #79 rollout is only
the report verbs moving onto the seam. The report-verb candidates are inferred from verb names and need
confirming against each handler. For #92 (tooltip placement), the cursor and corner anchors to remove are
OR's 7 `ANCHOR_RIGHT`, SM's 3, QC's 2 and MM's 1, plus each addon's 1-2 elsewhere. MM's `modules/Tooltip.lua`
anchor is player-configured (Schema_Vocab `ANCHOR_VALUES`), which v2.112.0 may forbid outright. That is an
owner decision.

## 4. Proposed re-vendor procedure for this group (plan input)

One commit per addon on the run branch, subject `<ID>: Re-vendor LibKa0s v1.104.0 (kit 56)`. It holds the
whole-folder copy of both payloads, the provenance line roll and the prune, plus the test fixes the copy
forces, in the same commit, so the green gate holds at every commit:

- **All 8 below v1.100 (MM OR PM PFE PGFE PC QC WG):** add `SideTabs` to the degraded Options stub. Recommended
  stub: a no-op that draws nothing, mirroring the stub's other page-drawing members. The alternative is an
  ignore row with the reason "no page calls it". The stub is the safer route, because the parity suite
  exists so that a future page call does not fall through.
- **MM, PGFE, WG:** the four Compat members. These three addons are Retail-only, so wiring them through to
  the library or answering the `UnitName` fallback both work. Recommendation: wire them on `NS.Compat` like
  PFE and QC do (one line each). An ignore row would be wrong, because the identity readers are what any
  future SavedVariables key should use.
- **PGFE, WG:** 5 loader lines in `tests/loader.lua`, in xml order.
- **MM:** re-pin `tests/test_settings_pin.lua` for `window.columnHeader.font` (+ Bebas Neue, Russo One).
- **Docs ripple, in the same commit or a sync-docs follow-up:** the CLAUDE.md provenance line (the tool
  does this); PM CLAUDE.md:46 and PC docs/ARCHITECTURE.md:487 major counts (21 → 24); the revendor bundle
  `docs/revendor/<date>-v1.104.0/` (plus the span bundle for OR, PM, PFE, PC); `docs/test-cases.md` if the
  repo generates it. There are no new icon or sound credits, because no new icons are declared and sounds
  are none.
- **SM:** copy only, already green. **DW:** copy only (Callout pair), but see risk R1.

Expected effort: about 15-30 min per addon for the eight, about 5 min for SM and DW.

## 5. Standard / doc ripple

- The standard pointer in each addon (X-Standard / badge / CLAUDE.md) is `/dev-copilot:wow-revendor-standards`'s
  job, not this re-vendor's. If the run also bumps the standard pointer to v2.112.x, v2.110.0's MUSTs (#88/#89)
  and v2.112.0's tooltip MUSTs (#92) become audit deviations in every addon until adoption.
- skinning-§2 `DefaultSkin` MUST: MM, PGFE and WG are non-conformant (0 references). This predates this run
  (it arrived with v1.94.0, which they never vendored) and should land with the adoption leg or as a small
  re-vendor fix.

## 6. Risks

- **R1, DW is occupied.** Another session has `feat/2026-11-16-loose-ends` checked out with 22 uncommitted
  files, including `DropWatcher.toc` and `tests/test_harness.lua`. Its commits touch no `libs/`,
  `tests/_kit/` or `CLAUDE.md`, so the re-vendor cannot conflict textually. But switching branches in that
  checkout would destroy the other session's state.
- **R2, SM's default branch is `main`, not `master`.** Its CLAUDE.md, the collection CLAUDE.md ("every
  collection repo's default branch is master") and any executor script that hard-codes `master` will
  misfire. Detect it per repo.
- **R3, payload growth.** Every addon gains `media/waypoint/` (456 KB) and two fonts whether or not it
  uses them (a whole-folder rule). `libs/LibKa0s` goes from 13M to 14M on disk in MM.
- **R4, the v2.110.0 MUSTs.** They take effect at this re-vendor but are deferred by the owner, so audits
  run between the re-vendor and the adoption leg will flag MM, OR and SM (undocked strips) and OR and SM
  (hand-built footers).
- **R5, slider behaviour (OptionsWidgets 46).** No test covers each addon's own number rows against it. A
  smoke check is needed.

## 7. Test plan

- Per addon, the CLAUDE.md gate: retail run, a forever run where listed, and `ka0s-bounded luacheck .` at
  0/0. The expected totals are the simulated ones above with 0 fail: MM 2590 total, OR 1594, PM 1202, PFE
  658, PGFE 549, PC 695, QC 2031, SM 740, WG 1104.
- The vendor-sync gate runs inside each suite and needs `../LibKa0s` at the v1.104.0 tag reachable. It
  passed in simulation.
- Owner smoke, per addon with a strip (MM, OR, SM, DW): strip placement re-look (v1.103.0's re-look line).
  Per addon with number rows (all): type junk into a slider box, press Enter and tab away, and the value
  must revert. Per addon: `/x diagnostics` reports `LibKa0s running:` with Role, Callout and WaypointArrow
  listed (DebugLogDiagnostics 10).

## 8. Open questions for the owner (decisions, with recommendations)

1. **DW while another session holds it.** Options: (a) re-vendor DW last, after that session merges
   `feat/2026-11-16-loose-ends`; (b) re-vendor it in a separate `git worktree` off `master` now; (c) skip
   DW, since its delta is the Callout pair it does not use. **Recommend (a)**, with (c) as the fallback if
   the other session has not merged by the time the run reaches its finalize.
2. **The `SideTabs` stub shape.** A no-op stub member, or an ignore row with a reason? **Recommend the
   no-op stub**, one line per addon.
3. **Compat identity members in MM, PGFE and WG (Retail-only).** Wire them, or ignore them with a reason?
   **Recommend wiring them**, which matches PFE and QC.
4. **`DefaultSkin` in MM, PGFE and WG.** Fix it in the re-vendor leg (small, MUST since v1.94.0), or defer
   it to adoption? **Recommend fixing it in the re-vendor leg**: it is a standing MUST violation the
   re-vendor exposes, and it takes a few lines per addon.
5. **v2.110.0 strip and footer MUSTs between re-vendor and adoption.** Should the re-vendor report record
   them as owed, under #88 and #89? **Recommend yes**, with no per-addon deviation rows: the open issues
   are the record.
6. **SM's `LibKa0s sounds: none.` line.** Keep it, or drop it to the canonical "no line" form?
   **Recommend keeping it**: the kit parses it and it is explicit. If the audit objects, record a ruling
   in the standard.
7. **Span bundles for OR, PM, PFE and PC (v1.94.0 unrecorded).** Accept the revendor command's
   consolidated span bundle? **Recommend yes** (the command's default).
