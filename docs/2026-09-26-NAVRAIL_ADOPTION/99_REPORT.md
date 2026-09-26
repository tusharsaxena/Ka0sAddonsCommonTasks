# 99 — Execution record

NR-REC-01, written 2026-09-26. This file records what the NavRail adoption run actually did: LibKa0s
v1.61.0 into the ten addons that carried v1.60.0, the MultiMeters Windows page (MultiMeters#55) and
the KickCD Grid page (KickCD#33). The plan (`03_EXECUTION_PLAN.md`) is frozen and is not edited.
Sources are git in the ten repos (`git log master..feat/2026-09-26-navrail-adoption`, the
`refs/notes/ka0s-review` notes, local `origin/*` refs), `./resume-state.sh -v`, and the workflow's
per-item and per-checkpoint evidence. No battery was re-run for this record.

## 1. Outcome

- All sixteen build items are done. `resume-state.sh -v` reports M1 10/10, M2 6/6, and NR-REC-01 as
  the only READY item. All ten addon trees were clean (`dirty=0`) and every one carries the
  v1.61.0 payload.
- **Ten addons re-vendored.** Each has LibKa0s v1.61.0 (tag `v1.61.0`, `c6183bd`; OptionsNav minor 1,
  Options 25, OptionsTabs 5) in `libs/LibKa0s`, byte-identical to the tag's archive. `tests/_kit`
  did not change (kit revision 27) in any of them. The CLAUDE.md provenance line reads v1.61.0.
  Nine addons' library-absent stubs gained an inert `NavRail` no-op. ConsumableMaster's did not
  (02_SPEC R18); its Options inventory test names `OptionsNav` instead.
- **MultiMeters** has the one Windows page: the Active window band, the rail (General · Frame ·
  Header · Bars · Tooltip · Visibility · Columns, 120 wide), and each entry's own strip. It also has
  per-entry tab memory, deep links (`NS.OpenOptionsPage`, `Helpers.SelectSection`, the `SelectTab`
  route) and Defaults per entry for the active window. The six sub-pages are retired. The tree is
  General · Windows · Profiles.
- **KickCD** has the Grid page: the Unit band, the rail (Icons · Cast bar · Text Label) through
  `RenderUnitPanel`'s new chrome hook (linked Focus included), per-entry tab memory, Defaults for the
  unit in the band (a ratified deviation row, 02_SPEC R8), and deep links from the former page keys.
  The Icons, Cast bar and Text Label pages are retired. The tree is General · Grid · Spells ·
  Profiles.
- **Nothing was pushed, merged, tagged or version-bumped.** No repo has an
  `origin/feat/2026-09-26-navrail-adoption` ref, and every `master` equals its `origin/master`. The
  review notes are local only.
- The in-client smoke checks have **not** been run. They are the owner's (section 6).

## 2. Commits

Every branch sits directly on its current `master` (the merge base is master's head), so a later
`--no-ff` merge is clean. Each commit carries a local `refs/notes/ka0s-review` note except the three
`R` fixes, whose findings are in the note on the commit they fix.

| Id | Repo | Commit | Subject | Review |
|---|---|---|---|---|
| NR-AT-01 | AbsorbTracker | `1c27f7a` | Re-vendor LibKa0s v1.61.0 and stub NavRail | clean |
| NR-BL-01 | BankLedger | `18b7293` | Re-vendor LibKa0s v1.61.0 and stub NavRail | clean |
| NR-CM-01 | ConsumableMaster | `4a15a89` | Re-vendor LibKa0s v1.61.0; the Options inventory names OptionsNav | clean |
| NR-KC-01 | KickCD | `425a0e8` | Re-vendor LibKa0s v1.61.0 and stub NavRail | clean |
| NR-LH-01 | LootHistory | `191765a` | Re-vendor LibKa0s v1.61.0 and stub NavRail | clean |
| NR-MM-01 | MultiMeters | `5a91478` | Re-vendor LibKa0s v1.61.0 and stub NavRail | clean |
| NR-PM-01 | PanelMaster | `9357c07` | Re-vendor LibKa0s v1.61.0 and stub NavRail | clean |
| NR-PF-01 | PartyFrameEnhanced | `cb0a2fe` | Re-vendor LibKa0s v1.61.0 and stub NavRail | clean |
| NR-PC-01 | PrettyChat | `f2b0ce8` | Re-vendor LibKa0s v1.61.0 and stub NavRail | clean |
| NR-WG-01 | WhatGroup | `3e14c50` | Re-vendor LibKa0s v1.61.0, load OptionsNav, stub NavRail | clean |
| NR-MM-02 | MultiMeters | `9b9c9fc` | The Windows page draws a nav rail: one page per window | fixed |
| NR-MM-02R | MultiMeters | `2290500` | Make the committed tree green again (a British spelling in the new suite) and fix two stale docstrings | (fix) |
| NR-MM-03 | MultiMeters | `5bb1d97` | Deep links open the Windows page on an entry | clean |
| NR-MM-04 | MultiMeters | `ad3afcb` | Retire the six window sub-pages; the tree is General, Windows, Profiles | fixed |
| NR-MM-04R | MultiMeters | `81b967e` | Master visibility's tooltip no longer names the retired Visibility page | (fix) |
| NR-KC-02 | KickCD | `7f636cc` | The Grid page: Icons, Cast bar and Text Label on a nav rail | clean |
| NR-KC-03 | KickCD | `54842c7` | Grid Defaults for the unit in the band; deep links open Grid on an entry | clean |
| NR-KC-04 | KickCD | `0a5d894` | Retire the Icons, Cast bar and Text Label pages; the tree is General, Grid, Spells, Profiles | fixed |
| NR-KC-04R | KickCD | `b1d06cb` | Smoke steps and comments reach the retired pages through Grid | (fix) |

### Heads

| Repo | `master` (= `origin/master`) | Branch head | Commits ahead |
|---|---|---|---|
| AbsorbTracker | `7540ab3` | `1c27f7a` | 1 |
| BankLedger | `90b0c60` | `18b7293` | 1 |
| ConsumableMaster | `e2103f9` | `4a15a89` | 1 |
| KickCD | `604e922` | `b1d06cb` | 5 |
| LootHistory | `4f03c04` | `191765a` | 1 |
| MultiMeters | `c374876` | `81b967e` | 6 |
| PanelMaster | `5fa3da8` | `9357c07` | 1 |
| PartyFrameEnhanced | `151d467` | `cb0a2fe` | 1 |
| PrettyChat | `bfac822` | `f2b0ce8` | 1 |
| WhatGroup | `0fcfe6f` | `3e14c50` | 1 |

## 3. Gates

Every run went through `ka0s-bounded`. The same figures are in `checkpoints.tsv`. In every addon the
vendor check (`diff -r --strip-trailing-cr ../LibKa0s/LibKa0s libs/LibKa0s`) printed nothing. LibKa0s
`master` is `cf38896`, one `--no-ff` merge past the tag (`git describe`: `v1.61.0-1-gcf38896`), and
`git diff v1.61.0 master -- LibKa0s` is empty, so each copy is exactly v1.61.0. The lizard line
(`-l lua -x "./libs/*" -x "./tests/_kit/*" -C 15 -w .`) printed nothing in every addon.

**M1** (the checkpoint ran on each branch head, clean before and after):

| Addon | Head | Tests (passed / failed / skipped) | Plan expected | luacheck |
|---|---|---|---|---|
| AbsorbTracker | `1c27f7a` | 810 / 0 / 0 | 810 | 0/0 in 66 files |
| BankLedger | `18b7293` | 1104 / 0 / 0 | 1104 | 0/0 in 75 files |
| ConsumableMaster | `4a15a89` | 1112 / 0 / 0 | 1112 | 0/0 in 122 files |
| LootHistory | `191765a` | 961 / 0 / 0 | 961 | 0/0 in 70 files |
| PanelMaster | `9357c07` | 962 / 0 / 0 | 962 | 0/0 in 64 files |
| PartyFrameEnhanced | `cb0a2fe` | 383 / 0 / 0 | 383 | 0/0 in 75 files |
| PrettyChat | `f2b0ce8` | 518 / 0 / 0 | 518 | 0/0 in 51 files |
| WhatGroup | `3e14c50` | 823 / 0 / 0 | 823 | 0/0 in 54 files |
| MultiMeters (NR-MM-01) | `5a91478` | 2078 / 0 (item run; badge 2078) | 2078 | 0/0 |
| KickCD (NR-KC-01) | `425a0e8` | badge 1189 (item run) | 1189 | 0/0 in 109 files |

MultiMeters' and KickCD's checkpoint gates ran on their M2 heads (below), which contain NR-MM-01 and
NR-KC-01. File cap: the largest authored Lua files reported are ConsumableMaster
`tests/test_slash.lua` 1426, PanelMaster `settings/PanelEditor.lua` 1447, WhatGroup
`tests/test_frame.lua` 1422, LootHistory `modules/Browser.lua` 1289, PrettyChat `tests/test_panel.lua`
1125 and PartyFrameEnhanced `tests/test_launcher.lua` 578. PrettyChat's generated
`GlobalStrings/GlobalStrings.lua` (23842 lines) predates this branch and is untouched by it.
WhatGroup's only files over 1500 lines are an existing frozen `complexity.txt` and media binaries.

**M2:**

| Addon | Head | Tests | Plan expected | luacheck | lizard | Largest authored files |
|---|---|---|---|---|---|---|
| MultiMeters | `81b967e` | 2092 / 0 / 0 | 2091 | 0/0 in 141 files | clean; 4459 functions, AvgCCN 2.4 | `modules/Row.lua` 1446, `modules/Aggregator.lua` 1432 |
| KickCD | `b1d06cb` | 1201 / 0 / 0 | 1201 | 0/0 in 111 files | clean; 3089 functions, AvgCCN 2.0 | — |

Both README Tests badges match their runs (MultiMeters 2092/2092, KickCD 1201/1201).

## 4. Deviations from the plan

The plan is frozen, so each deviation is recorded here with the commit that shows it.

1. **The bundle was not committed before M1.** The plan's "Before M1 — commit the bundle" step did
   not run: `git log main -- docs/2026-09-26-NAVRAIL_ADOPTION` was empty when this record was
   written, and the whole bundle was untracked. NR-REC-01 therefore commits the whole bundle,
   including the plan files, in one commit. The plan files were not edited, but their first commit
   is this one, so `git diff --cached --stat` lists them as new files, which Step 4 said it must not
   show. `00_OVERVIEW.md` still says "DRAFT, not executed". That is its frozen planning-time text; this
   file is the record of execution.
2. **Checkpoint rows were written late.** The M1 and M2 checkpoints ran, but neither row was
   appended to `checkpoints.tsv` at the time (it held only its header). NR-REC-01 appends the M1, M2
   and M3 rows from the recorded evidence.
3. **The luacheck line in every revendor bundle.** The plan's `rv_bundle` shorthand wrote luacheck's
   colored totals line into `05_SUMMARY.md` with ANSI escapes. All ten addons departed from the
   literal command in the same cosmetic way. AbsorbTracker and LootHistory captured it with
   `luacheck --no-color`, and the other eight stripped the codes. PartyFrameEnhanced also wrote its
   intermediate diff and run files under the session scratchpad instead of `/tmp/<Addon>-*`.
4. **ConsumableMaster (`4a15a89`).** The `rv_bundle` helper's generic "stub gains NavRail" line in
   `03_DECISIONS.md` was wrong for ConsumableMaster (R18), so it was reworded. The checkpoint evidence
   records the gate as `lua tests/run.lua`, where the plan names `lua5.1` for this addon.
5. **MultiMeters NR-MM-02 was committed red (`9b9c9fc`).** A comment copied verbatim from the plan's
   Step 1 test file said "cancelling", and the kit's prose gate (localization-§5) failed on it. The
   prose scan reads only tracked files, so the suite passed while the file was untracked and failed
   once it was committed. NR-MM-02R (`2290500`) made the tree green again ("canceling") and fixed two
   stale docstrings in `settings/Windows.lua`. NR-MM-02 itself also changed "cancelled" to "canceled"
   in a Step 5 comment, pointed the plan's `#column-editing` link at the real anchor
   (`#column-editing-is-settings-panel-only-and-out-of-combat-only`), and updated two
   `docs/module-map.md` rows under the "citations move with the code" rule.
6. **NR-MM-03 (`5bb1d97`):** the degraded namespace-parity case did not fail before the fix, as Step 2
   expected, because `NS.OpenOptionsPage` was nil on both arms. It does real work now that both arms
   define it. The reviewer noted one coverage gap and no defect: removing `stashTab(ctx)` from
   `Helpers.SelectSection` leaves the suite green.
7. **NR-MM-04 (`ad3afcb`).**
   - The Columns Defaults tooltip key the plan said to delete was never in `locales/enUS.lua`. The
     orphaned shorter key, which had no caller, was removed instead.
   - The Step 8.3 deletion in `docs/settings-panel.md` stopped at the next heading of any level, so
     the sections Step 8.4 edits were kept.
   - Comments and docs beyond the named files were fixed to satisfy the plan's own greps:
     `settings/Schema_Compose.lua`, `tests/test_window.lua`, `docs/debug.md`, and the `Columns.lua`
     issue-#53 comment.
   - The review found one R15 miss: `master.visibility`'s tooltip still named "one window's own
     Visibility page". NR-MM-04R (`81b967e`) fixed it and added a test, "Options: no row's text sends
     the player to a retired window page". That is why MultiMeters ends at **2092**, not the plan's
     2091.
   - Left alone: internal comments that still say "Frame page" and similar (for example
     `settings/Schema.lua:248`). They are not player-facing, and the plan asked for no comment sweep.
8. **KickCD.**
   - NR-KC-01 (`425a0e8`): the stub comment names `settings/Grid.lua` before it exists. That is as
     planned, and NR-KC-02 created it.
   - NR-KC-02 (`7f636cc`): two more comments in `tests/test_options_panel.lua` that said "six" pages
     became count-free, beyond the two comments the plan named. The change is comment-only.
   - NR-KC-03 (`54842c7`): a cosmetic nit was left unfixed. The new sentence in
     `Helpers.OpenPageTab`'s docstring (`settings/Panel_Widgets.lua:114`) has no `---` separator
     before the `refusedInCombat` paragraph.
   - NR-KC-04 (`0a5d894`) edited `tests/test_locale.lua`'s RESIDUE list, which the plan did not name.
     The plan's new `/kcd reset` literals would otherwise have failed two locale cases, contrary to
     Step 2's expectation. It also fixed `docs/ARCHITECTURE.md:128` and stale panel mentions in
     smoke-tests #20, #22 and #23 and `settings-panel.md:223`. Smoke #36 sits after #27 in the suite
     index, because rows 28-35 were already missing.
   - The review found that 15 smoke steps outside the plan's cited lines still sent the owner to
     Settings -> Icons, Cast bar or Text Label, and that some comments still said "page". NR-KC-04R
     (`b1d06cb`) routes each step through Grid -> entry and fixes the comments.
9. **`06_SMOKE_TESTS.md` is unchanged.** No owner results for this bundle's checks have arrived
   (section 6).

## 5. Follow-ups

Nothing was filed by this task. This run had no GitHub access, and the GitHub MCP server also failed
to connect in the launching session (the Authorization header was rejected). The owner, or a session
with working GitHub access, files these. Space the writes out.

1. **AuraMaster: the clean-up issue** for leftover sub-page wording and dead code, owed from
   SETTINGS_REDESIGN (its `99_REPORT.md` section 7.1). It covers `settings/Text.lua`'s `pageDim` and
   its unreachable `ctx.__renderDisabled` read, the Aura type row's `desc` ("The Filters page
   offers..."), the possibly unreachable `EMPTY_PAGE` in `settings/OptionsSetup.lua`, and informal
   "the Filters page" / "its Text page" mentions in the README and `docs/settings-panel.md`.
   **Status: still owed.** No evidence shows it was filed. File it on AuraMaster with
   `/wow-addon:issue-add`.
2. **MultiMeters#55 and KickCD#33: the comments.** The "ready once v1.61.0 is published" notes owed
   from SETTINGS_REDESIGN are out of date: v1.61.0 is published (tag pushed at the SETTINGS_REDESIGN
   finalize). The new state is that each layout is built on `feat/2026-09-26-navrail-adoption`
   (MultiMeters `81b967e`, KickCD `b1d06cb`), reviewed, not merged, and waiting on the owner's smoke
   checks. **Status: neither issue was commented.** Post one comment on each.
3. **MultiMeters: the header gear.** `modules/HeaderControls.lua`'s `settings` action could open
   Windows on the gear's window with `NS.OpenOptionsPage("windows")` instead of the main panel
   (02_SPEC R3). File it as a MultiMeters enhancement.
4. **WowAddonStandards: options-ui-§13.** It could state the Defaults scope for a railed page whose
   band picks one of several instances, as KickCD's new `docs/ARCHITECTURE.md` deviation row asks
   (02_SPEC R8). File it on WowAddonStandards, or take it to `/wow-addon:harvest-standards`.
5. **MultiMeters: a pinning test** for `stashTab(ctx)` in `Helpers.SelectSection` (the surviving
   mutant in NR-MM-03's review). It is optional and low priority.
6. **PanelMaster#55.** The plan states it was already closed `state:will-not-do` at planning time
   (`00_OVERVIEW.md`, "A rail in any other addon"). NR-PM-01's reviewer read it as a pending write.
   Nothing is owed unless GitHub shows otherwise. This record could not check.

## 6. Owner smoke

RV-S1, MM-S1 … MM-S11 and KC-S1 … KC-S11 are in `06_SMOKE_TESTS.md`. None has been run, and none is
marked. MM-S1..MM-S11 are also MultiMeters `docs/smoke-tests.md` §36, and KC-S1..KC-S11 are KickCD
`docs/smoke-tests.md` #36, each with an empty Result column. The NR-MM-02 and NR-MM-04 reviews also
point at MultiMeters §1 (the tree check) and §4 (the sidebar combat walk), which were reworded for
the new tree.

The owner's in-client results reported alongside this run (Containers rail alignment, scroll, style
entry, tab memory, old links, combat lock, and KickCD's pages unchanged under AuraMaster's v1.61.0)
belong to SETTINGS_REDESIGN. They are recorded there (`08b1522`). They do not cover RV-S1, which
runs with AuraMaster disabled so that each addon's own v1.61.0 copy is the one loaded.

## 7. Finalize

On the owner's go-ahead, `/wow-addon:finalize` would merge `feat/2026-09-26-navrail-adoption`
`--no-ff` into `master` in all ten addons: AbsorbTracker, BankLedger, ConsumableMaster, KickCD,
LootHistory, MultiMeters, PanelMaster, PartyFrameEnhanced, PrettyChat and WhatGroup. It would re-run
each gate on the merge, push `master` and the `refs/notes/ka0s-review` notes, and delete the
branches. The ten are independent of one another, and LibKa0s and WowAddonStandards need nothing:
the tag and the standard are already published. No addon version is bumped as part of it. Until
then, all ten branches exist only locally.
