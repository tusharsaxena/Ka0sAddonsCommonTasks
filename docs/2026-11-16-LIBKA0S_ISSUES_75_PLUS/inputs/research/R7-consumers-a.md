# R7-consumers-a: re-vendor inventory, part A

Scope: AbsorbTracker, AuraMaster, BankLedger, CombatTrail, ConsumableMaster, DpsRace, KickCD,
LibKa0sSkinTester, LootHistory. This was a read-only pass on 2026-11-16. The gates were run through
`ka0s-bounded`, and every tree was confirmed clean after the run (`git status --porcelain` empty in all nine).
Target: LibKa0s **v1.104.0** (`9bc9cc51`, kit revision **56**).

## 1. Repo state and green gate (master today)

| Addon | Default branch | Clean | Open/unmerged branches | Vendored tag (CLAUDE.md) | Kit rev | Last revendor bundle | Clients | Gate commands (CLAUDE.md) | Master green? (tests / lint) |
|---|---|---|---|---|---|---|---|---|---|
| AbsorbTracker | master | yes | none | v1.94.0 (CLAUDE.md:47) | 53 | v1.93.0 (v1.94.0 unrecorded, so a span bundle is owed) | Retail + Forever | `lua tests/run.lua`, `KA0S_KIT_CLIENT=forever lua tests/run.lua`, `ka0s-bounded luacheck .` (CLAUDE.md:40-43) | GREEN: 1065/0/1 skip, both profiles; lint 0/0 in 85 files |
| AuraMaster | master | yes | none | v1.98.0 (CLAUDE.md:36) | 56 | v1.98.0 | Retail + Forever | same three (CLAUDE.md:34) | GREEN: 2523/0/1 retail, 2522/0/2 forever (16 shards); lint 0/0 in 228 |
| BankLedger | master | yes | none | v1.93.0 (CLAUDE.md:48) | 53 | v1.93.0 | Retail only | `lua tests/run.lua`, `ka0s-bounded luacheck .` (CLAUDE.md:41-43) | GREEN: 1660/0/1; lint 0/0 in 121 |
| CombatTrail | **main** (origin/main only, no origin/HEAD set) | yes | none | v1.102.0, commit 2748549 (CLAUDE.md:52,59) | 56 | v1.102.0 | Retail + Forever | same three (CLAUDE.md:44-47) | GREEN: 1515/0/1 retail, 1507/0/1 forever; lint 0/0 in 194 |
| ConsumableMaster | master | yes | none | v1.94.0 (CLAUDE.md:61) | 53 | v1.93.0 (span owed) | Retail + Forever | `lua5.1 tests/run.lua`, forever profile, `ka0s-bounded luacheck .` (CLAUDE.md:107-109) | GREEN: 1481/0/1, both profiles; lint 0/0 in 156 |
| DpsRace | master | yes | none | v1.93.0 (CLAUDE.md:43) | 53 | v1.93.0 | Retail only (since 2026-11-10) | two (CLAUDE.md:38-40) | GREEN: 1509/0/1; lint 0/0 in 185 |
| KickCD | master | yes | `origin/feature/glow-options` (2026-10-18, **already merged**, 0 commits ahead; stale remote branch) | v1.93.0 (CLAUDE.md:42) | 53 | v1.93.0 | Retail only | two (CLAUDE.md:40) | GREEN: 1678/0/1; lint 0/0 in 158 |
| LibKa0sSkinTester | master | yes | none | v1.94.0 (CLAUDE.md:41) | 53 | v1.93.0 (span owed) | Retail + Forever | three (CLAUDE.md:36-38) | GREEN: 890/0/1, both profiles; lint 0/0 in 83 |
| LootHistory | master | yes | none | v1.93.0 (CLAUDE.md:58) | 53 | v1.93.0 | Retail only | two (CLAUDE.md:51-52) | GREEN: 1987/0/1; lint 0/0 in 162 |

Notes:
- CombatTrail is **not in `WowAddonStandards/standards/ADDONS.md`**, and its default branch is `main`. That contradicts the
  CommonTasks CLAUDE.md line "every collection repo's default branch is master". Per-repo detection is mandatory here.
- Kit revision by tag: v1.93/v1.94 = 53, v1.95 = 54, v1.96 = 55, v1.97..v1.104 = 56. All nine repos match the kit of their tag.
- No library icon changed between v1.93.0 and v1.104.0 (`git diff --stat v1.93.0 v1.104.0 -- LibKa0s/media/icons` is empty),
  so no `LibKa0s icons:` declaration can be refused by `prune-icons.lua`.

## 2. What the jump to v1.104.0 can break (per-addon evidence)

Library Lua files that changed between v1.93.0 and v1.104.0 (`git diff --stat v1.93.0 v1.104.0 -- LibKa0s/*.lua`):
Callout*, Compat, DebugLogDiagnostics, Launcher, Media, OptionsNav, OptionsWidgets, Role (new), Skin, SkinDefsOthers,
WaypointArrow* (new), Widgets. The consumer notes come from CHANGELOG "What a consumer owes" and docs/releasing.md:278-370.

### 2a. Predicted RED at re-vendor (must be fixed in the re-vendor commit)

1. **Options instance gains `SideTabs`** (OptionsNav minor 7, v1.100.0; releasing.md "a host's Options instance stub,
   if it is checked for parity against a live instance, gains it"). Every host below has an Options `Helpers` degradation stub that
   is parity-checked by the by-name form (`T.assertSurfaceParity(stub, "LibKa0s-Options-1.0", ignore)`), and none of them lists `SideTabs`:
   - AbsorbTracker tests/test_surface_parity.lua:104, stub settings/OptionsSetup.lua:327 (`Helpers.NavRail = function() end`)
   - AuraMaster tests/test_surface_parity.lua:46, stub settings/OptionsSetup.lua:327 (name list)
   - BankLedger tests/test_surface_parity.lua:289, stub settings/OptionsSetup.lua:250
   - DpsRace tests/test_surface_parity.lua:26, stub settings/OptionsSetup.lua:185
   - KickCD tests/test_surface_parity.lua:180, stub settings/OptionsSetup.lua:410
   - LibKa0sSkinTester tests/test_surface_parity.lua:130, stub settings/OptionsSetup.lua:147
   - LootHistory tests/test_surface_parity.lua:160, stub settings/OptionsSetup.lua:128
   - ConsumableMaster is **probably safe**. Its Options case uses the reached-member form (test_surface_parity.lua:250-262, a grep of `Helpers.*` call sites).
   - Precedent fix: CombatTrail settings/OptionsSetup.lua:145 lists `"SideTabs"` in its no-op list, and DropWatcher's v1.102.0 bundle records the same fix.
   Fix: one no-op `SideTabs` in each stub. Mechanical.
2. **LibKa0sSkinTester's hand-written library load list.** tests/loader.lua:24 `LIBKA0S = { ... }` is pinned to LibKa0s.xml by
   tests/test_harness.lua:51 ("the explicit LibKa0s list matches LibKa0s.xml, in XML order"). The re-vendor must insert, in XML order, `Role.lua` after `Compat.lua` (v1.95),
   `Callout.lua` and `CalloutSettings.lua` after `Toast.lua` (v1.96), and `WaypointArrow.lua` and `WaypointArrowSettings.lua` after `CalloutSettings.lua` (v1.99).
   Every other repo in this part derives its list from the XML (`Loader.xmlFiles`), so nothing goes red from the list itself. Examples: BankLedger tests/run.lua:62,
   ConsumableMaster tests/run.lua:161, DpsRace tests/run.lua:19, KickCD tests/run.lua:53, LootHistory tests/run.lua:21 and AbsorbTracker/AuraMaster test_loadorder.
3. **Kit rev 55: the sound subset** (v1.96.0). With no `LibKa0s sounds:` line the gate reads "none", so `libs/LibKa0s/media/sounds/` must be
   empty. The v1.104.0 whole-folder copy brings eight voice packs, about 2.7 MB. The tag's `tools/prune-icons.lua` prunes them in the
   same run as the icons. If that prune is skipped, `test_vendor_sync` goes red. The eight hosts other than CombatTrail have no sounds line. CombatTrail declares all eight packs
   (CLAUDE.md:61). None of the nine passes custom `pairs` to `VendorSync.register` (all `register(T, {...root/provenance...})`),
   so the `sounds = "media/sounds"` pair edit is not owed.

### 2b. Silent or low risk (verify while running)

- **New files now load in every XML-derived harness** (Role, Callout, CalloutSettings, WaypointArrow, WaypointArrowSettings, plus the
  `media/waypoint/` folder). They register at file load under each host's mocks. A host with its own client mock (ConsumableMaster
  tests/wow_mock.lua, KickCD's shared mocks) may lack a global those files touch at load (for example C_VoiceChat or PlaySoundFile).
  Expected to be fine, because they are guarded and the kit mocks cover the LibKa0s suite, but only a run proves it.
- DebugLogDiagnostics 7 to 10 and Launcher 9 to 10: no member change. The pins found are `>=` (LootHistory test_libka0s.lua:733,
  KickCD test_compat_api.lua:1259 for Compat). No exact-minor pin was found in tests.
- Media FONTS 33 to 35 and `Skin.__FACE_SIZES`: no count pins were found (only `FONTS[name] ~= nil` checks).
- Compat minor 4 (v1.94.0) is new to BankLedger, DpsRace, KickCD and LootHistory: it adds members only. KickCD's parity case only sanity-checks the major. LootHistory, KickCD
  and DpsRace keep their own `core/Compat.lua` and do not mirror the major's full surface.
- Skin minor 18 (`DefaultSkin` per client): it changes nothing on Retail. The four Retail-only hosts are unaffected. The Forever hosts are already at v1.94 or later.
- Widgets 27 (`Footer`, `FOOTER`, `DockTestStrip`): the Widgets stubs here are reached-member parity (AbsorbTracker
  test_surface_parity.lua:295-339), so nothing goes red. Spies on `W.TestStrip` (BankLedger test_browser.lua:723, DpsRace
  test_skinsetup.lua:139/155, KickCD test_sim_marker.lua:34) keep working, because an undocked strip is still minor 26's.
- Callout contract changes (glow boolean, default voice) only touch CombatTrail. It is already at Callout 4.5 (v1.102.0).
  Its v1.102 to v1.104 delta is **Widgets 27 only**, with no kit change. That makes it the lowest-risk re-vendor of the nine.
- AuraMaster (v1.98 to v1.104) skips the kit change (already 56). It takes SideTabs (red, item 1), OptionsWidgets 46 (the slider junk fix,
  "owes nothing"), Callout 2 to 4 (not adopted, so no loader line is owed) and WaypointArrow (new). Its `libs/LibKa0s/media/sounds/` exists
  as an empty, untracked directory, so the gate is already satisfied.
- Every re-vendor rolls the CLAUDE.md provenance line in the same commit, regenerates `docs/test-cases.md`, updates the README
  `[Tests]` badge where one exists, and writes `docs/revendor/<date>-v1.104.0/`. A **span bundle** (v1.94.0 to v1.104.0) is owed for
  AbsorbTracker, ConsumableMaster and LibKa0sSkinTester, whose v1.94.0 vendoring has no bundle.

## 3. Adoption-site counts (planned features; not built in this run)

Counted over addon source, excluding `libs/`, `tests/`, `docs/`, `tools/` and comment lines. These are greps, so the numbers are
approximate and should be re-derived per addon at adoption time.

| Addon | #92 tooltips: `:SetOwner(` sites / files; cursor & corner anchors | #79 reports: `DevTools_Dump`; multi-line report verbs beyond reserved `/x list` | #89 hand-built footers / status lines | #88 strips: `TestStrip` sites (docked) / HUD needing a strip | #86 own window title bars (close + extra header buttons) |
|---|---|---|---|---|---|
| AbsorbTracker | 0 own; bar tooltips go through the library's widget at ANCHOR_NONE (modules/Bar.lua:52) | 0; `/at profile list` (settings/Slash.lua:506) | 0 (N/A) | 0 (0) / bars in `/at sim` need `dock="hud"` | 0 windows |
| AuraMaster | 0 direct; **player option `tooltipAnchor`** with 7 anchors incl. `ANCHOR_CURSOR` and corner anchors (core/Constants.lua:290-295, settings/Layout.lua:531, default `ANCHOR_BOTTOMLEFT` defaults/Profile.lua:249). This conflicts with #92 "never on the cursor or a corner" | 0; none found | 1: PresetPicker status/footer (settings/PresetPicker.lua:497-505, 593) | 0 (0) / containers in `/am test` need HUD strips; the PresetPicker opens in test mode (window) | 1 (PresetPicker close, settings/PresetPicker.lua:478) |
| BankLedger | 12 / 4 files (Browser, InsightsWidgets, LedgerTable, SessionWindow); 4 `ANCHOR_RIGHT`, 1 `ANCHOR_NONE` | 0; none (diagnostics sections are already library reports) | 1: Browser footerBar, `FOOTER_H = 18` via `NS.Skin.Footer` (modules/Browser.lua:1005-1046) plus `_dbFooter` | 2 `W.TestStrip` (0 docked): Browser strip under the filter bar (Browser.lua:741), SessionWindow strip hand-anchored under the title bar (SessionWindow.lua:486); plus the Browser.lua:125 strip | 3 title bars (Browser.lua:992, Export.lua:402, SessionWindow.lua:572) through `B:MakeCloseButton` |
| CombatTrail | 22 / 16 files (incl. core/ChartsSetup.lua:18); 4 corner (`ANCHOR_RIGHT`), 2 `ANCHOR_NONE` | 0; `/ct ignore list` (modules/LaneIgnore.lua:156) | 2 hand-built at **20 px**: Hud `buildFooter` (modules/Hud.lua:167, 511) and RaceWindow (RaceWindow.lua:352). "The reference look" is still hand-built and not 24 px, so it too must move to `W.Footer` | 2 `W.TestStrip` (0 docked): HUD strip hand-anchored (Hud.lua:622), Results `anchorStrip` test + sim (Results.lua:541-557) | 6 windows with `NS.MakeCloseButton` (Hud, RaceWindow, Results, Results_Compare, Results_Timeline, Results_Gear) + 12 `Style.ControlButton` header controls (lock/settings/race) |
| ConsumableMaster | 5 / 4 files, all `ANCHOR_RIGHT` (core/MacroDisplay.lua:155/234, modules/KCMItemRow.lua:398, settings/MacroBarSlots.lua:235, settings/StatPriority.lua:471). The settings-page ones may be Settings-canvas, which is out of scope | 0 live (the comment at core/SlashDump.lua:31); **local `DL.Report` already** (core/DebugLogSetup.lua:337, 6 call sites) for `dump`, `priority … list`, `stat list`, `aio … list`, `seed status`. It becomes a passthrough and its serializer is deleted | 0 (N/A) | 0 / none (no test/sim mode) | 0 windows |
| DpsRace | 13 / 9 files; 3 `ANCHOR_RIGHT`, 2 `ANCHOR_NONE` | 0; `/dr ignore show` (settings/Slash.lua:72) | 1 hand-built at 20 px: Hud `buildFooter` (modules/Hud.lua:61, 564) | 2 `W.TestStrip` (0 docked): Hud test + sim `anchorStrip` (Hud.lua:650-669), Results `anchorStrip` (Results.lua:469-481) | 4 windows (Hud, Results, Results_Gear, Results_Timeline) + 7 `Style.ControlButton` |
| KickCD | 3 / 2 files, all `ANCHOR_RIGHT` (modules/IconGrid_Render.lua:319 HUD; settings/Spells_Rows.lua:85/174, Settings-canvas, likely out of scope) | 0; `/kcd spells list` (core/KickCD.lua:890) and `/kcd debug spells|castbar|interrupt|window|events` dumps (DEBUG_COMMANDS, core/KickCD.lua:444) | 0 (N/A) | 0 / **icon grids in `/kcd sim` now MUST carry a HUD strip**. That reverses KC-02/D-13: tests/test_sim_marker.lua pins "no strip, step panel only", so the test must be inverted at adoption | 0 windows |
| LibKa0sSkinTester | 0 | 0; none | 1 hand-built at 22 px: Showroom footer (modules/Showroom.lua:35, 258-269, 300) | 1 per showcase cell (modules/ShowroomOverlays.lua:102). This is a specimen, so it is probably N/A or kept as a showcase | 1 (Showroom title bar + close, Showroom.lua:250-252) |
| LootHistory | 14 / 5 files, 8 of them in the `core/Compat.lua` tooltip helpers (613-724, default `ANCHOR_RIGHT`); **3 `ANCHOR_CURSOR`** (modules/AnalyticsLedger.lua:115, Timeline.lua:407, 556); 10 corner `ANCHOR_RIGHT` | 0; none | 1: Browser footer fontString, `FOOTER_H = 18` (modules/Browser.lua:130, 1054-1057) plus `_dbFooter` | 1 window, 2 anchor sites: Browser strip under the filter bar (Browser.lua:925) and under dividerBar (Browser.lua:260) | 2 (Browser.lua:1014, Export.lua:490) |

## 4. Proposed re-vendor procedure (the piece this run builds)

Run per addon on `feat/<run-date>-libka0s-v1.105` or whatever the run's tag is. If the run cuts a new LibKa0s tag, every point below still
applies and its own delta is added on top.
1. Copy `libs/LibKa0s/` and `tests/_kit/` whole from the tag. Run the tag's `tools/prune-icons.lua` (icons + sounds).
2. Roll the provenance line. Add `SideTabs` to the Options stub (the seven hosts in 2a.1). Extend the SkinTester loader list (2a.2).
3. Gate: tests under both profiles where the CLAUDE.md says so, plus lint 0/0. Regenerate test-cases.md and update the badge.
4. Write the revendor bundle (and the span bundle for AbsorbTracker, ConsumableMaster and LibKa0sSkinTester).
Expected effort: about 15 to 30 minutes per addon. CombatTrail is lowest (Widgets only), AuraMaster and the v1.93 hosts are the largest deltas.

## 5. Risks

- R1: The new modules load inside host-owned mocks (ConsumableMaster wow_mock, KickCD). Medium likelihood of a missing-global raise at file load. Fix it
  in the host mock, never in libs/.
- R2: A forgotten prune leaves 2.7 MB of voice packs, which `test_vendor_sync` catches (good). Risk is low if the skill is used.
- R3: CombatTrail on `main`. A script that hard-codes `master` fails or creates a stray branch. Detect per repo.
- R4: Another session may be releasing the standard or LibKa0s mid-run (the standard-version-collisions memory). Fetch before finalize.
- R5: The kit jump from 53 to 56 touches the glyph guard's face list (rev 56). A host that renders new face names in a test string is unaffected (the safe set
  stays at 117).

## 6. Open questions for the owner (decisions, with a recommended answer)

1. **Is CombatTrail in scope?** It is not in ADDONS.md, and its default branch is `main`. *Recommend: yes. Re-vendor it, because it is the Callout consumer and
   the footer reference. Rename `main` to `master` only if you rule it (as PGFE/DpsRace were), and add it to ADDONS.md in the
   standard as a separate change.*
2. **AuraMaster's player-chosen tooltip anchor (incl. "At the cursor") versus #92.** *Recommend: aura icons are HUD body
   elements, so migrate the setting. Either retire it and default to the beside-the-container placer, or keep only "beside, right
   first" and "beside, left first", with a schema migration mapping ANCHOR_CURSOR and the corners to the default. This is an owner ruling because it takes
   away a player option.*
3. **KickCD sim HUD strip reverses ruling D-13** (step panel only, no floating strip). v2.110.0 retires that exemption. *Recommend:
   follow v2.110.0 (`dock="hud"` per visible grid, `Place()` after a move). Invert test_sim_marker at adoption.*
4. **Stale `origin/feature/glow-options` on KickCD** (merged on 2026-10-18). *Recommend: delete the remote branch at this run's cleanup.
   It is not this run's branch, so ask first.*
5. **CombatTrail and DpsRace footers are 20 px hand-built, and the SkinTester one is 22 px.** *Recommend: all move to `W.Footer` (24 px) in the adoption
   phase, CombatTrail included despite being "the reference look".*
6. **Settings-canvas tooltips (KickCD Spells_Rows, ConsumableMaster StatPriority and MacroBarSlots).** *Recommend: treat them as out of scope under
   #92's "Settings pages in Blizzard's canvas" if they render in the Blizzard Settings canvas. Confirm per site at adoption.*
