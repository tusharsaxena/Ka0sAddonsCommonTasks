# Report: the owner's fifth smoke round

Branch `feat/2026-11-01-full-skinning` in 18 repos: LibKa0s, the 16 addons and this one. Outfitter was not touched.
The branches and `refs/notes/ka0s-review` are pushed. Nothing is merged, no tag is pushed and no version is bumped.
The smoke list is `06_SMOKE_TESTS.md`, and nothing on it is marked passed.

## What shipped (52 R5 commits in 17 code repos)

- **M1, LibKa0s (8 commits):** R5-L1 option C and swatch 2; R5-L2 Shell's band above a backdrop window's fill,
  toasts opt out (`noTopBar`), every library window banded; R5-L3 `S.Band` and `S.Header`, header children on the
  band's middle; R5-L4 the picker list's own outside-press listener; R5-L5 library icons cropped 0.07 and edged in
  `icon.outline`, the icon rule in `docs/api`; R5-REL the CCN split of S.Shell and S.Header, then the re-cut.
- **M2, the 16 addons:**
  - R5-RV in all 16; R5-WIN in Skin Tester, BankLedger, DpsRace, DropWatcher, LootHistory, MultiMeters, QuickComms and WhatGroup.
  - R5-DD in DropWatcher only, for its compact Filters panel.
  - R5-ICON in ConsumableMaster, DpsRace, DropWatcher, KickCD, MultiMeters and QuickComms.
  - R5-MM1 (meter band flush in the gradient, collapsed = the band), R5-DR1 (a band on all four DpsRace windows, HUD
    title left), R5-DR2 (bare `/dr sim` idle, 15 s in real time), R5-QC1 (pad header band, no section bands), R5-PG1.
- **M3:** R5-GATE (this commit). It also fixes `resume-state.sh`, which did not count a combined subject such as
  `R5-MM1 + R5-WIN: `, even though CLAUDE.md allows one.

## The lead's calls (00_PLAN.md, binding)

1. Shade C applies to Ka0s Default only; MultiMeters' `SKIN_FALLBACK["title.bg"]` moves with it.
2. The band sits at Shell's inset (`win.borderSize`, else 1), 30 px tall; content keeps 6 px; a custom meter colour is flat.
3. The band is fixed in the library (BACKGROUND above the backdrop Center); toasts opt out; popovers get the full band.
4. The DpsRace HUD title is LEFT; its other windows follow `title.align`.
5. QuickComms: the pad, not the dial; text left, borderless band, at the bottom when the pad grows upward.
6. Header children sit on the band's geometric middle, no per-font nudges; on EllesmereUI its 25 px bar.
7. The picker list has its own outside-press listener, and its body, title, eye and gear close it; Escape unchanged.
8. `/dr sim` opens idle, `/dr sim <scenario>` starts at once; 15 s in real time; the card holds 4 s.
9. Icons: crop 0.07 a side; `icon.outline` in windows and settings, `icon.border` (hud) on HUD and toasts; inline crop only.

## Totals (fresh at this gate, one repo at a time through ka0s-bounded)

- **LibKa0s:** 4030 passed, 0 failed, 3 skipped (4033); lint 0/0 in 296 files. Release battery
  `docs/automated-tests/20261103-200402/`: max CCN 15, none over, perf not measured.
- **16 addons:** 22638 passed, 0 failed, 16 skipped; luacheck 0/0 in every repo; no Lua file over 1500 lines bar
  PrettyChat's exempt generated `GlobalStrings/GlobalStrings.lua`.
- **All 17 code repos:** 26668 passed, 0 failed.

## Tag

The local v1.85.0 is at **17d18aa** (R5-REL, the sixteenth re-cut). That is LibKa0s HEAD, the tree is clean, and the
tag is not pushed.

## Open items

- **R5-PG2** (PGFE collapsed strip, `R5_ADDENDUM_PGFE_COLLAPSED.md`) has not landed. It runs as the follow-up step after
  this gate and before your smoke, with its own commit, push and PG smoke row. `06_SMOKE_TESTS.md` has a
  placeholder row for it.
- **Reviews:** this round's independent reviews ran as workflow agents. None of them wrote a `refs/notes/ka0s-review`
  note on an R5 commit; the notes refs are unchanged and pushed as they were.
- **SkinPaintExtras.lua (1228 lines):** both halves of its re-check trigger fired. It is carried unpeeled, and the R5-REL
  commit leaves the peel to you and the lead.
- **exceptions.tsv:** no row is needed. Every R5 id except R5-PG2 landed a commit.
- **Your part:** the smoke run in `06_SMOKE_TESTS.md`, then the go-ahead. After that come `/dev-copilot:finalize`, the
  v1.85.0 tag push, LibKa0s #71 and #72 closed spaced apart (#70 stays open), and the cleanup of branches, stashes and
  worktrees.
