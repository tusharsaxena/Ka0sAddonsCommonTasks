# Skin-defaults audit (LibKa0s#97), 2026-11-20

This bundle is frozen. It records what the audit found on 2026-11-20. Later rulings and fixes go in the run bundle
`docs/2026-11-20-LIBKA0S_94_97_99_100/` (its execution record, `RESUME.md` or `checkpoints.tsv`), never here.

## What was audited

LibKa0s#97 asks whether every skinnable element takes the active skin's value by default, in every consumer. The
rule: under any skin, every skinnable element draws the skin's value unless the owner has explicitly asked for an
override. The trigger was Combat Trail in the 2026-11-19 smoke review, where several bar families drew a flat fill or an
addon-local texture instead of the skin's statusbar texture.

Twenty consumers were audited: the library's own widgets (LibKa0s) and the 19 addons on
`../WowAddonStandards/standards/ADDONS.md`, RangeMaster included (owner, 2026-11-20). Each table lists the consumer's
skinnable elements by token family (backdrop and border, header, body and title fonts, statusbar texture, bar fill and
background, row floors, hover and selection washes, marks and icon tints, scrollbars, tooltips, chips, dividers, footers
and strips, plus HUD text and "other"), with the token it should read, a status, file:line evidence and the ruling or
fix. Each table also opens with a note on the consumer's headless guards (`Kit.skinValues` and `Kit.skinSwitch`) and on
what they leave uncovered.

The normative text is `../WowAddonStandards/standards/standards/skinning.md`, sections 1 (adoption and owner tokens),
3 (the Skin tab and its Scope), 4 (the shipped skins), 6 (HUD style follows the skin), 7 (what a skin never touches) and
9 (every surface follows the skin, with its Leave, Game art and Meaning colors classes). On top of that sits the owner's
ruling **R-2 of 2026-11-20** (`docs/2026-11-20-LIBKA0S_94_97_99_100/00_PLAN.md`): an addon option for a texture, font or
color whose default is the addon's own value is a GAP. Its default must follow the skin; a stored pick stays.

## Method

The audit was read-only. No file in any audited repo was changed. For each consumer:

1. One **auditor** agent read the consumer's code, defaults, settings and test guards and drafted a table.
2. One **adversarial skeptic** agent then re-opened every row, checked each cited ruling against its source,
   re-ran the greps, overturned or reclassified rows it could not stand behind, and added rows the auditor had missed.
   The skeptic wrote the final table. Reclassified rows say so in their Status cell (for example "GAP (reclassified
   from OVERRIDE)" or "OK (was UNCLEAR)").

A row is marked OVERRIDE (owner) only when it cites an owner ruling: a section of the standard that records one, or a
bundle, smoke sheet, issue or spec where the owner decided it. A lead's or agent's decision, however long it has stood,
is not an owner ruling; rows that rest on one were marked GAP or UNCLEAR.

The three front files (this README, `01_GAP_LIST.md` and `02_UNCLEAR.md`) were written from the 20 tables after they
were final. The totals below were counted from the tables' rows, not taken from the counts some tables print in their
own preamble.

## Commits audited

Each table names its commit in its first line or its opening note. QuickComms and WhatGroup do not, so their entries are
the default-branch heads read with `git rev-parse --short master` when this README was written. Neither repo has a
commit dated after 2026-11-19, so those heads are the trees the agents read.

| Consumer | Branch | Commit | Note |
|---|---|---|---|
| LibKa0s | `feat/2026-11-20-libka0s-94-97-99-100` | `140d56df` (v1.107.0) | The tree carried the uncommitted SD-LK-94 edit to Widgets.lua (+3 lines after :137). SD-LK-94 has since landed as `93633f47`, so line numbers after Widgets.lua:137 are 3 lower than the file now shows |
| AbsorbTracker | master | `030d6e9` | |
| AuraMaster | master | `178c309` | |
| BankLedger | master | `3205b7f` | |
| CombatTrail | master | `0ee871e` | |
| ConsumableMaster | master | `75f87d6` | |
| DropWatcher | master | `755157c` | |
| KickCD | master | `dd9c401` | |
| LibKa0sSkinTester | master | `d9b1ed9` | |
| LootHistory | master | `97cec5e` | |
| MultiMeters | master | `c9cba61` | |
| OutfitterReborn | master | `2755a0d` | |
| PanelMaster | master | `b1871ec` | |
| PartyFrameEnhanced | master | `9f8147c` | |
| PremadeGroupsFilterExtension | master | `64f274f` | |
| PrettyChat | master | `5103580` | |
| QuickComms | master | `0af3a12` | From `git rev-parse`; the table names no commit |
| RangeMaster | master | `77cb263` | master has since moved to `5cb0ff6`, a docs-only sync (`2c0cae6`); the audited code is unchanged |
| SkillMaster | master | `21a93dd` | |
| WhatGroup | master | `dd61034` | From `git rev-parse`; the table names no commit |

Every addon had LibKa0s v1.107.0 vendored. Addon tables cite `libs/LibKa0s/...` at that vendored copy.

## Status key

| Status | Meaning |
|---|---|
| OK | The element reads the skin's value by default: through LibKa0s-Skin, an owner token that follows a library token, or a library widget that does. A stored swatch or pick that draws only while its `FromSkin` companion is off counts as OK. |
| GAP | The element bypasses the skin by default, with no owner ruling behind it. This includes an option whose default is the addon's own value (R-2), a headless guard that cannot see a regression on a painted surface, and a missing companion the standard requires. Every GAP becomes a fix item in `01_GAP_LIST.md`. |
| OVERRIDE (owner) | The element keeps its own look on purpose, and the row cites the owner ruling that says so. |
| UNCLEAR | The audit could not tell whether the element should follow the skin, usually because two owner rulings collide or because the only basis is a lead's call. Every UNCLEAR becomes a question in `02_UNCLEAR.md`. |

A qualifier in parentheses, such as "(new)", "(latent)", "(guard)", "(widened)", "(missed)", "(at smoke)", "(ungated)"
or "(reclassified from X)", is the skeptic's note. The row counts under its leading word.

## Owner-override sources cited

The OVERRIDE (owner) rows across the tables rest on these sources. Paths without a repo are in this repo.

- **The standard**, `../WowAddonStandards/standards/standards/skinning.md`: §1 owner tokens (default is the Ka0s Default
  pixel, `follow` elsewhere); §3 the Scope toggles (Ignore settings panel on by default, Ignore fonts off) and the Font
  outline "HUD text only" default; §4 the shipped skins and their `q.*`, `sem.*` tokens, including ruling Q2 (Ka0s
  Default's selection held off its hover); §6 HUD style follows the skin (HUD sizes follow the skin's factor, D-09; class
  and meaning colors come first; a skin's None border defers to the stored values, ruling of 2026-11-01); §7 a skin never
  touches a Blizzard shared frame, and the TestStrip's amber and cyan stay the library's meaning colors; §9 the Leave
  classes (fades and dims, flat thin bars, text size, the monospace face, chat lines, icon shapes and the minimap ring,
  window text with no outline, Ka0s Default's client resize grip and hover art, PanelMaster's player-authored panels,
  Combat Trail's race clocks, bar colors and missing tracks), the Game art class and the Meaning colors class.
- **Full-skinning run, owner rulings of 2026-11-01**: `docs/2026-11-01-FULL_SKINNING/00_PLAN.md` (:7 Scope, :10 MC
  "Meaning colors stay", :11 the Leave list A6, A7, A8, A9, D8, D9, L10, L11, L12, L13, :12 D5 "leave warning tints,
  fix glow"), with `inputs/SKIN_CAUSES.md`, `inputs/SKIN_DEFAULT_GAPS.csv`, `plan-data/SKIN_CAUSES_map.csv`,
  `06_SMOKE_TESTS.md` (QuickComms PLOOK-1, -7, -10, -11, passed 2026-11-02) and `99_REPORT.md`.
- **Skin library follow-ups, 2026-10-30**: `docs/2026-10-30-SKIN_LIBRARY_FOLLOWUPS/00_PLAN.md` R-1 (Ignore fonts covers
  the HUD, :15), R-2 (Ignore settings panel stays, default on, :16), R-4 (per-skin HUD fonts, :18), R-5 (every custom
  widget obeys the Scope, :19); `DECISIONS.md`; `exceptions.tsv` (WG-01).
- **Skin overrides and picker** (LibKa0s#63, #64): `docs/2026-10-28-SKIN_OVERRIDES_AND_PICKER` (the Skin tab font and
  texture overrides default to "", the skin's own; LH-01 chart bars through BarTexture).
- **Font pickers and skin faces**: `docs/2026-10-31-FONT_PICKERS_AND_SKIN_FACES/DECISIONS.md` D-10 (outline "HUD text
  only").
- **Skinning rollout, 2026-10-29**: `docs/2026-10-29-SKINNING_ROLLOUT/OWNER_RULINGS_M3.md` (R-1 KickCD keeps an edge,
  R-3 MultiMeters window fill), `00_PLAN.md` O1 (near-miss pixels kept under Ka0s Default). Its `DECISIONS.md` X1, X2,
  D2, D3, D6 and D7 are lead decisions; rows that rest on them alone were not marked OVERRIDE.
- **Smoke feedback**: `docs/2026-11-01-SMOKE_FEEDBACK/items.tsv` (SF-AM-1, -2, -3; SF-MM-1, -2, -3);
  `docs/2026-11-03-SMOKE_ROUND4/99_REPORT.md` (R4-SEP); `docs/2026-11-03-SMOKE_ROUND5/00_PLAN.md` with
  `docs/2026-11-03-SMOKE_ROUND6/inputs/OWNER_FEEDBACK.md` (QuickComms section bands, PLOOK-12);
  `docs/2026-11-06-REVENDOR_LIBKA0S_V1_89/SF1_SMOKE_FEEDBACK.md` (SF1-CM button edge);
  `docs/2026-11-16-LIBKA0S_ISSUES_75_PLUS/SR2_SMOKE_ROUND2.md` (SR2-STP, the Skin Tester's panel default).
- **Per-addon records**: OutfitterReborn `docs/ARCHITECTURE.md:421-422` (DEV-SKIN-SHEET-BUTTON, DEV-SKIN-FLYOUT-TINT,
  owner 2026-11-05 and 2026-11-09); SkillMaster `docs/superpowers/plans/2026-11-10-feedback-1.md:114` (FB-19, border
  style companion off); AuraMaster `docs/superpowers/specs/2026-11-14-auramaster-presets-design.md` §15 to §17 (preset
  call-out look and bar background); Combat Trail `docs/superpowers/plans/2026-11-10-combat-trail-v0.2-feedback.md`
  (THIS gold, best blue, player and pet caster colors); RangeMaster `modules/Presets.lua:91-95` (band frame alpha, owner
  2026-11-19 M12).
- **Contested**: LibKa0s `docs/superpowers/plans/2026-11-13-callout.md:93` (L17, the owner's in-game Callout settings).
  The LibKa0s table holds it UNCLEAR against R-2; the Combat Trail table calls the same defaults a GAP. See U-1.

## Totals

Counted from the table rows. 820 rows in all.

| Consumer | OK | GAP | OVERRIDE | UNCLEAR | Rows | Table |
|---|---:|---:|---:|---:|---:|---|
| LibKa0s | 24 | 14 | 8 | 4 | 50 | [LibKa0s](tables/LibKa0s.md) |
| AbsorbTracker | 25 | 0 | 10 | 1 | 36 | [AbsorbTracker](tables/AbsorbTracker.md) |
| AuraMaster | 24 | 2 | 12 | 9 | 47 | [AuraMaster](tables/AuraMaster.md) |
| BankLedger | 22 | 4 | 9 | 1 | 36 | [BankLedger](tables/BankLedger.md) |
| CombatTrail | 17 | 10 | 10 | 2 | 39 | [CombatTrail](tables/CombatTrail.md) |
| ConsumableMaster | 25 | 2 | 9 | 4 | 40 | [ConsumableMaster](tables/ConsumableMaster.md) |
| DropWatcher | 40 | 1 | 16 | 2 | 59 | [DropWatcher](tables/DropWatcher.md) |
| KickCD | 15 | 2 | 13 | 0 | 30 | [KickCD](tables/KickCD.md) |
| LibKa0sSkinTester | 30 | 4 | 12 | 2 | 48 | [LibKa0sSkinTester](tables/LibKa0sSkinTester.md) |
| LootHistory | 34 | 1 | 14 | 1 | 50 | [LootHistory](tables/LootHistory.md) |
| MultiMeters | 32 | 7 | 15 | 1 | 55 | [MultiMeters](tables/MultiMeters.md) |
| OutfitterReborn | 24 | 14 | 9 | 2 | 49 | [OutfitterReborn](tables/OutfitterReborn.md) |
| PanelMaster | 15 | 0 | 15 | 1 | 31 | [PanelMaster](tables/PanelMaster.md) |
| PartyFrameEnhanced | 24 | 0 | 17 | 3 | 44 | [PartyFrameEnhanced](tables/PartyFrameEnhanced.md) |
| PremadeGroupsFilterExtension | 20 | 0 | 16 | 0 | 36 | [PremadeGroupsFilterExtension](tables/PremadeGroupsFilterExtension.md) |
| PrettyChat | 20 | 0 | 9 | 1 | 30 | [PrettyChat](tables/PrettyChat.md) |
| QuickComms | 16 | 4 | 8 | 4 | 32 | [QuickComms](tables/QuickComms.md) |
| RangeMaster | 10 | 13 | 7 | 2 | 32 | [RangeMaster](tables/RangeMaster.md) |
| SkillMaster | 30 | 5 | 9 | 2 | 46 | [SkillMaster](tables/SkillMaster.md) |
| WhatGroup | 18 | 0 | 12 | 0 | 30 | [WhatGroup](tables/WhatGroup.md) |
| **Total** | **465** | **83** | **230** | **42** | **820** | |

Two counting notes. PrettyChat's preamble says 19 OK, but the table has 20 OK rows. One PartyFrameEnhanced row (the
stand-in's name text) carries an unescaped `|` inside a color escape in its Evidence cell, so a markdown renderer splits
it into seven cells; it is one UNCLEAR row and is counted as one.

The 83 GAP rows become 19 library items and 56 addon items in `01_GAP_LIST.md`, after moving library-owned fixes up and
merging duplicates. The 42 UNCLEAR rows become 31 owner questions in `02_UNCLEAR.md`.

## Files

- [`01_GAP_LIST.md`](01_GAP_LIST.md): every GAP as a fix item, the library first (SD-LK-97.n), then per addon (`SD-SK-<abbr>.n`).
- [`02_UNCLEAR.md`](02_UNCLEAR.md): every UNCLEAR row as an owner question (U-1 to U-31).
- [`tables/`](tables/): the 20 per-consumer tables, one per consumer, as the skeptic left them.
