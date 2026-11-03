# Report: the owner's sixth smoke round (the skin picker's preview)

Branch `feat/2026-11-01-full-skinning` in 19 repos: WowAddonStandards, LibKa0s, the 16 addons and this one. Outfitter
was not touched. The branches and `refs/notes/ka0s-review` are pushed. Nothing is merged, no tag is pushed and no
version is bumped. The smoke list is `06_SMOKE_TESTS.md`, and nothing on it is marked passed.

## What shipped (51 R6 commits in 18 code and standard repos)

- **M1, the standard (2):** R6-STD, skinning-§10 plus its follow-up that quotes the eye's words.
- **M1, LibKa0s (5):** R6-L1 adds the `spec.preview` contract and the review's tooltip fix. R6-REL brings paintEye back
  to CCN 15, writes the hosts-owe paragraph and records the re-cut battery.
- **M2, the 16 addons (44):** R6-RV in all 16. R6-PV in all 16, PGFE included, where it records the no-preview case.
  Review follow-ups landed as later R6-PV commits in 11 of them (two in MultiMeters).

## The lead's calls (00_PLAN.md, binding)

1. The contract is in the library: `spec.preview = { mode, enter, exit, isActive, isShown }`. On a fresh show with the
   surface hidden, the picker enters the mode. The eye toggles it and shows its state. `closed()` restores the opening
   state on every route (Apply, Apply to all, the gear, the close control, Escape, HideSkinPicker), before `onClose` and
   the queue's handover. A refused enter changes nothing. `onPreview` stays as a one-shot for back-compat.
2. Per-addon modes. **Test:** AM, BL, DR, DW, LH, MM, QC, WG. **Unlock:** AT, CM, KC, PM, PF. **Window:** the Skin
   Tester's showroom. **Console:** PrettyChat's debug console with the `/pc test` sample. **None:** PGFE.
3. Unlock is a stored setting, and no new persistence was added. PanelMaster's unlock is session state, so a `/reload`
   there comes back locked.
4. A new rule in the standard (below).
5. The tag v1.85.0 is re-cut locally and not pushed. The picker's minor goes to 11. Outfitter's vendored copy stays at 10.

## The standard

**v2.98.0** (2026-11-03): skinning-§10, *the skin picker's preview*. It sets the mode order (test, unlock, window,
console) and defines what "the main surface is hidden" means for each mode. The picker auto-enters on a fresh show only,
the eye toggles, and every close route restores. Enter and exit go through the addon's own write seam, and PGFE is the
documented no-preview addon. The rule adds anti-pattern #111 (an eye that only enters) and the *Skin picker preview*
column in `ADDONS.md`. The ripple covers the index, the executive summary, the context pack (hard rule 24b),
`NEW_ADDON.md` and `AUDIT.md`. `scripts/check-standard.sh` passes.

## Totals (fresh at this gate, one repo at a time through ka0s-bounded)

- **LibKa0s:** 4053 passed, 0 failed, 3 skipped (4056), lint 0/0 in 297 files. The release battery
  `docs/automated-tests/20261104-002816/` is green at 4fd5b47: max CCN 15, none over, perf not measured.
- **16 addons:** 22815 passed, 0 failed, 16 skipped. luacheck reports 0/0 in every repo. No Lua file is over 1500 lines
  apart from PrettyChat's exempt generated `GlobalStrings/GlobalStrings.lua`.
- **All 17 code repos:** 26868 passed, 0 failed.

## Tag

The local v1.85.0 is an annotated tag on **79d043d** (R6-REL, the seventeenth re-cut). That commit is LibKa0s HEAD, the
tree is clean, and the tag is not pushed.

## Open items

- **LibKa0s#74** (Ka0s skins as EllesmereUI styles) is filed and not built.
- **LibKa0s#71 and #72** close after the merge, spaced apart. **#70** (SF-DR-9, deferred) stays open.
- **Still to run in this workflow:** R6-MM2 (the MultiMeters export glyph), R6-SIM-STD, R6-SIM-L and R6-SIM (the Sim
  checkbox), R6-NAME (README only), then the automated tests, sync-docs and finalize, and R6-ISSUES after finalize.
  `resume-state.sh` lists them as OPEN.
- **Reviews:** 43 of the 51 R6 commits carry a `refs/notes/ka0s-review` note, and the notes are pushed with the branches.
- **exceptions.tsv:** no row is needed. Every M1 to M3 id has a commit in each repo it applies to, PGFE's R6-PV included.
- **Your part:** run the smoke list in `06_SMOKE_TESTS.md`, then give the go-ahead. R6-GATE (M3) is this commit.
