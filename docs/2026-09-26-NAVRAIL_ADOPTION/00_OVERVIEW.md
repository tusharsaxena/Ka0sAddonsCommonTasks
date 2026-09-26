# NavRail adoption: overview

**Status: DRAFT, not executed.** Nothing in this bundle has run. No repo has
`feat/2026-09-26-navrail-adoption` yet, nothing is committed or pushed, and the bundle itself is not
committed yet: the plan's first step ("Before M1") commits it on `main`. It is frozen once execution starts (`../../CLAUDE.md`, "Bundle conventions").

This is the "new bundle" that `../2026-09-26-SETTINGS_REDESIGN/00_OVERVIEW.md` ("After this bundle")
promised: AuraMaster's shipped settings redesign (#6), carried to the collection. It has two parts:

1. **Re-vendor LibKa0s v1.61.0 into the ten addons that still carry v1.60.0.** AuraMaster already
   carries v1.61.0 (SR-AM-01).
2. **Build the same layout in MultiMeters and KickCD.** MultiMeters' Windows page becomes one page per
   window (MultiMeters#55). KickCD's Icons, Cast bar and Text Label pages become one Grid page
   (KickCD#33).

The design is the owner's (2026-09-26). The owner waived spec and plan review and asked for the build
to run straight through, as with AuraMaster. `02_SPEC.md` writes the owner's text down as a short
design addendum in the AuraMaster spec's shape. `03_EXECUTION_PLAN.md` turns it into work.

## Preconditions (true at planning time, re-checked by every NR-XX-01 Step 1)

| What | State | Proof |
|---|---|---|
| LibKa0s v1.61.0 published | tag `v1.61.0` peels to `c6183bd` (tag object `7e64131`) and is on origin; `master` = `cf38896`, and its `LibKa0s/` and `testkit/` equal the tag's | `git -C ../../../LibKa0s rev-parse v1.61.0^{}`; `git -C ../../../LibKa0s diff --quiet v1.61.0 master -- LibKa0s testkit` |
| Standard v2.69.0 published | WowAddonStandards `master` = `30aa3cd`; options-ui-§13 sanctions the rail, options-ui-§14 puts the band above the rail and the strip | `grep -n "nav rail" ../../../WowAddonStandards/standards/standards/options-ui.md` |
| AuraMaster reference | `master` = `b51aee8`: `settings/OptionsSetup.lua` :184-209 (registry), :500-599 (rail page, `SelectSection`, `SelectTab` route) | the SETTINGS_REDESIGN bundle's `99_REPORT.md` |
| The ten addons | every one on a clean `master`, level with origin, vendoring v1.60.0 | `./resume-state.sh` |

## What the owner decided

| # | Decision | Spec | Where it lands |
|---|---|---|---|
| D1 | Re-vendor all ten addons except AuraMaster from the `v1.61.0` tag, exactly as SR-AM-01 did. The CLAUDE.md provenance line moves to v1.61.0. Each host's library-absent stub gains the `NavRail` no-op so `tests/test_surface_parity.lua` stays green (ConsumableMaster excepted: R18). Gate green, one commit per addon. | §4 | NR-XX-01 |
| D2 | MultiMeters' **Windows** page becomes the one page per window. The rail runs General · Frame · Header · Bars · Tooltip · Visibility · Columns, is 120 wide, and each entry's existing tabs become its strip. | §A2 | NR-MM-02 |
| D3 | MultiMeters **General** holds the Windows page's own content (new, rename, delete, duplicate, the group filter), and the "Copy settings from" tab folds into General as a new subsection (owner ruling). | §A2 | NR-MM-02 |
| D4 | MultiMeters has one pinned **Active window** band on top, full width (today's picker). `NS.State.activeWindowId` stays the one selection. | §A2 | NR-MM-02 |
| D5 | The six MultiMeters sub-pages leave the tree, which becomes General · Windows · Profiles. The D6 nesting mark (`NS.SubPageLabel`) goes. | §A3 | NR-MM-04 |
| D6 | Every MultiMeters schema row keeps its page key and window-relative path. `/mm get` and `/mm set`, defaults and profiles are untouched. | §A3 | all MM items |
| D7 | Deep links to a former MultiMeters sub-page open Windows at that entry. | §A3 | NR-MM-03 |
| D8 | MultiMeters Defaults restores the active entry's rows for the active window. | §A3 | NR-MM-02 |
| D9 | KickCD's new **Grid** page replaces Icons, Cast bar and Text Label. The rail runs Icons · Cast bar · Text Label, and each entry's tabs become its strip. | §B2 | NR-KC-02 |
| D10 | KickCD has one pinned **Unit** band across the top (today's `L["Unit"]` PageBanner), shared by all three entries. | §B2 | NR-KC-02 |
| D11 | General, Spells and Profiles are unchanged, and the tree becomes General · Grid · Spells · Profiles. | §B3 | NR-KC-04 |
| D12 | KickCD schema paths are unchanged. Deep links to icons, castbar and label open Grid at that entry. | §B3 | NR-KC-03 |
| D13 | KickCD Defaults restores the **active entry's rows for the selected unit**. | §B3 | NR-KC-03 |
| D14 | Execution order: the re-vendor first, then the two layouts. Nothing is pushed or merged, no tag is made, and no version is bumped. | — | all |

## Plan resolutions the owner may want to see

The owner waived review, so these are recorded, not asked. Each is in `02_SPEC.md` §9 with its
reasoning.

| # | Point | Resolution |
|---|---|---|
| R1 | D8 on MultiMeters' **General** entry. Its only schema row is `window.name`, so a row walk would rename the window to the shipped "Multi Meters". | Defaults on General restores **nothing** and prints one line saying so. The Windows page's own button restored nothing before (it had none). |
| R8 | D13 narrows KickCD's Defaults to one unit. The sub-pages' buttons reset **both** units, and options-ui-§13 says a railed Defaults covers "the set the folded sub-page's own button restored". | The owner's ruling is built. NR-KC-03 records it as a ratified deviation in KickCD's `docs/ARCHITECTURE.md` register, and NR-REC-01 lists a standard follow-up. MultiMeters needs no row: its rows are window-relative, so its sub-pages already reset one window. |
| R3 | MultiMeters has no deep-link caller today. Every way in is `NS.OpenOptionsPanel()`, which takes no argument. | NR-MM-03 adds the seam (`NS.OpenOptionsPage`, `Helpers.SelectSection`, the `SelectTab` route) with tests. The header gear keeps opening the main panel as it does today, and NR-REC-01 lists "gear opens Windows" as a follow-up. |
| R18 | D1 says **each** host's stub gains the `NavRail` no-op. ConsumableMaster's stub is checked against a named `OPTIONS_SEAM` list (`tests/test_surface_parity.lua:264`) of the members its code calls, which has no `NavRail` (nor `SelectTab`), and its comment refuses stubs "for a member no page reads". | NR-CM-01 adds **no** stub member, a departure from D1's letter, and keeps D1's purpose: parity stays green, and the new file is caught by `tests/test_libka0s.lua`'s Options inventory, which NR-CM-01 updates. If the owner wants the letter, the no-op is harmless and one line. |

## Scope

| Repo | What it gets | Milestone |
|---|---|---|
| AbsorbTracker, BankLedger, ConsumableMaster, KickCD, LootHistory, MultiMeters, PanelMaster, PartyFrameEnhanced, PrettyChat, WhatGroup | LibKa0s v1.61.0 from the tag (`libs/LibKa0s` only: the kit is unchanged at revision 27), the provenance line, the `NavRail` stub no-op, the hand-typed library lists four of them keep, and a `docs/revendor/<date>-v1.61.0/` bundle | M1 |
| MultiMeters | The Windows page with its rail, per-entry tabs, Defaults and deep links. The six sub-pages then retire, and the tests and docs follow. | M2 |
| KickCD | The Grid page with its rail, per-entry tabs, Defaults for the selected unit and deep links. The three pages then retire, and the tests and docs follow. | M2 |
| Ka0sAddonsCommonTasks | This bundle, committed on `main` before M1. Then `99_REPORT.md` and `checkpoints.tsv` rows. The owner's smoke results go in `06_SMOKE_TESTS.md`. | before M1, M3 |

**Out of scope:**

- **AuraMaster.** It is done: v1.61.0 was re-vendored in SR-AM-01 and the Containers page shipped at
  `b51aee8`. Nothing in AuraMaster is touched.
- **LibKa0s and WowAddonStandards.** Both are read only. The tag and the standard are published, and
  no library or standard change is needed. If a task finds a library defect, it stops and reports;
  the fix ships as `v1.61.1` under its own plan.
- **Pushes, merges, tags, version bumps and releases.** The owner has not authorized them for this
  run. `/wow-addon:finalize` runs later, on the owner's go-ahead.
- **A rail in any other addon.** PanelMaster#55 is closed `state:will-not-do`. The other eight addons
  get the library and the stub no-op only.
- **GitHub writes.** This run has no GitHub access. The follow-ups the SETTINGS_REDESIGN run could not
  file (the AuraMaster clean-up issue for leftover sub-page wording and dead code, and the
  "ready once v1.61.0 is published" notes on MultiMeters#55 and KickCD#33) belong to the session that
  launches this plan. NR-REC-01 records whether they were filed and lists the new follow-ups. It
  files nothing itself.

## Milestones

| Milestone | Repos | Content | Checkpoint |
|---|---|---|---|
| **M1** | the ten addons | NR-AT-01 … NR-WG-01: one re-vendor commit per addon, run in parallel | Each addon's full gate is green on its branch head, its `test_vendor_sync` passes, `libs/LibKa0s` equals the tag's `LibKa0s/` (`diff -r --strip-trailing-cr`), and its tree is clean. Nothing is pushed. |
| **M2** | MultiMeters, KickCD | NR-MM-02..04 and NR-KC-02..04, two chains in parallel, each in order | Full gate in both (tests 0 failed, luacheck 0/0, lizard: no new function above CCN 15, the 1500-line cap), clean trees, test-cases and badge agree with the run. Nothing is pushed. |
| **M3** | Ka0sAddonsCommonTasks | NR-REC-01 | `99_REPORT.md` and the checkpoint rows on `main` |

## Dependency order

```
NR-AT-01  NR-BL-01  NR-CM-01  NR-LH-01  NR-PM-01  NR-PF-01  NR-PC-01  NR-WG-01   (independent)
NR-MM-01 ─► NR-MM-02 rail page ─► NR-MM-03 deep links ─► NR-MM-04 retire sub-pages ─┐
NR-KC-01 ─► NR-KC-02 Grid page ─► NR-KC-03 Defaults + deep links ─► NR-KC-04 retire ─┤
                                                           (every M1 item) ──────────┴─► NR-REC-01
```

## Files in this bundle

| File | What it is |
|---|---|
| `00_OVERVIEW.md` | This file |
| `02_SPEC.md` | The design addendum: the owner's decisions for the Windows page and the Grid page, in the AuraMaster spec's shape, and the resolutions of every open point |
| `03_EXECUTION_PLAN.md` | The implementation plan: global constraints, review focus, every task with its files, interfaces, test code, implementation code, commands and commit |
| `items.tsv` | The manifest: id, milestone, repo, title, dependencies, effort, smoke checks, traces |
| `resume-state.sh` | Progress computed from git (zsh, read-only) |
| `RESUME.md` | How a fresh session picks the run up |
| `checkpoints.tsv` | One row per milestone that passed its checkpoint (header only until then) |
| `06_SMOKE_TESTS.md` | The owner's in-client checks (RV-S1, MM-S1..S11, KC-S1..S11), each with an empty Result |

There is no `01` file and no `inputs/`. The findings are the owner's design text and four read-only
surveys (the MultiMeters, KickCD, re-vendor dry-run and AuraMaster-pattern maps). Their facts are
cited inline in `03_EXECUTION_PLAN.md` with file:line. The re-vendor dry run's scratch copies were
temporary and are not part of the record.
