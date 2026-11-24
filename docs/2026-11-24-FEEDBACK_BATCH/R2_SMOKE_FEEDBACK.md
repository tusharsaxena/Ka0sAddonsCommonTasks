# Round 2: the owner's smoke feedback and LibKa0s#104 (2026-11-24)

An addendum to `00_PLAN.md`, which stays frozen. The owner passed all 42 checks of round 1
(`06_SMOKE_TESTS.md`), gave the go-ahead to finalize, and then sent more feedback from the same session in
game. Round 2 lands on the same branch, `feat/2026-11-24-feedback-batch`, before the finalize merge.

## The owner's words (verbatim where quoted)

1. **Quick Comms.** "in test mode, for the test mode string from the toast ("Test mode: a placeholder
   that sends nothing,") --> make it shroter so it fits in one line"
2. **Drop Watcher.** "The ask button overflows in the detail view - rename it to just Ask instead without
   the character name (both compact and expanded views)"
3. **Drop Watcher, ROLLS-22.** "i dont see a roll bar in test mode at all (or sim mode ... just regular
   /dw sim with dungeon selected - there is no "/dw sim roll" command)"
4. **LibKa0s#104.** "Add a github issue in LibKa0s to adopt the predefined test mode names consistently
   across all addon's test/sim modes", then "As part of this run, lets also build
   https://github.com/tusharsaxena/LibKa0s/issues/104"
5. **Loot History, the dropdowns.** "Character dropdown - current character is not highlighted in gold.
   It uses the skin color. - in this specific case, make the current selected always be a different color
   than the other texts - e.g. gold in ka0s default, etc - Check this for all addons that have a similar
   pattern - e.g. [Drop Watcher, Combat Trail screenshots] BankLedger, etc"
6. **Sim stepper.** "When i do /lh sim start loot - it plays the simulation but doesnt show the
   simulation window - sim mode whether started from a command like /xx sim start <scenario> or from just
   plain /xx sim should always show the sim stepper window (make this an upstream standards change) - Fix
   this for loothistory and audit and fix this for all other addons which use a sim mode"

## Done in the lead session

| Id | Repo | What | Commit |
|---|---|---|---|
| FB-QC-03 | QuickComms | The sample toast's note reads "Test mode: sends nothing." (the pad tooltip keeps the long one) | `4cdb39e` |
| FB-DW-02 | DropWatcher | The detail card's Ask reads `Ask`, with no name (FEED-114) | `9b25639` |
| FB-DW-03 | DropWatcher | Test mode's sample roll runs a looping 60 s countdown (bar and time); ROLLS-22's sim steps corrected | `7ccbe42` |
| - | LibKa0s | Issue #104 filed | - |
| FB-FIN | LibKa0s, WowAddonStandards | Content-only doc sync | `298af729`, `c1e3973` |

Diagnoses behind them:
- **Item 3, sim.** `/dw sim roll` exists as one of Drop Watcher's host verbs on a running sim, and a new
  headless test shows its bar. On Retail the dungeon scenario plays no roll of its own (personal loot);
  only WoW Forever's scenarios have roll steps. The smoke step was what misled.
- **Item 6.** `LibKa0s-Sim-1.0`'s grammar (`SimTimeline.lua` `runVerb`) calls `sim:ShowPanel()` on a
  bare `/xx sim` only; `start` (`verbStart`), and any other start path, never shows it.
- **Item 5.** `WidgetsDropdown` paints a selected row `menu.textSel`: Ka0s Default's gold, and every other
  skin's accent (`SkinDefsOthers` maps `accent` onto `menu.textSel`). Where a skin's accent sits near its
  body text, a selected row reads like the rest. Combat Trail's character dropdown marks the selection
  with a highlight bar but leaves the text white.

## Decisions (the lead's calls; the owner may revisit)

- **D1, #104 option (a).** The library publishes a shared deterministic crowd (`Sim.SampleCrowd`) beside
  the five protagonists, and the convention's rule 6 ("roster pools do not converge") is retired: every
  named sample person in every addon comes from the library. Addons keep their seeded determinism by
  seeding the library's crowd, not by keeping their own lists.
- **D2, sim panel.** "Always show the stepper" is the library's job: every start of a session shows the
  step panel (the grammar's `start`, the panel's own Start row, the Master controls Sim box and a host's
  own start call), headless sessions excepted. An addon whose sim does not run on the library gets the
  same rule by hand.
- **D3, dropdown.** A selected row's text always differs from a plain row's and from any value color it
  would otherwise wear (class, quality): `menu.textSel`, with Ka0s Default's gold standing in wherever a
  skin's value is too close to `menu.text`. The rule is the library's; addons that build their own menus
  match it.
- **D4, versions.** LibKa0s **v1.113.0** (the v1.112.0 tag stays as cut, local only, and both tags go
  out at the finalize), standard **v2.120.0**.
- **D5, where the work happens.** The game loads the live checkouts, so builders work in clones under
  `~/ka0s-scratch/fb2/` and never write a live repo. The lead fast-forwards each live branch from its
  clone after the run.

## Items

| Id | Repo | What |
|---|---|---|
| FB2-LK-01 | LibKa0s | Sim: every start shows the step panel (D2) |
| FB2-LK-02 | LibKa0s | WidgetsDropdown: the selected row's distinct color (D3) |
| FB2-LK-03 | LibKa0s | Sim: `SampleCrowd` and the convention without rule 6 (D1, #104) |
| FB2-STD-01 | WowAddonStandards | v2.120.0: the three rules (sim start shows the panel; selected row distinct; one name source) |
| FB2-LK-REL | LibKa0s | v1.113.0, local tag, release run |
| FB2-<AB>-01 | every roster addon | Re-vendor v1.113.0; sim start paths audited; own dropdowns audited; sample names from the library; smoke checks; doc sync |
| FB2-<AB>-REV | every roster addon | Independent review of the addon's round-2 diff, fixes in place |
| FB2-CT-REC | Ka0sAddonsCommonTasks | Round 2's record and smoke list |

`<AB>` is the addon's code from `00_PLAN.md` (AT AM BL CTR CM DW KC ST LH MM OR PM PFE PGFE PC QC RM SM WG).

## Smoke

The checks each item adds land in the addon's own `docs/smoke-tests.md`. The lead adds them to a new
sheet, `Documents/Ka0sPendingSmoke-2026-11-24-ADDED-FB2.csv`. The owner's sheets are never overwritten.
