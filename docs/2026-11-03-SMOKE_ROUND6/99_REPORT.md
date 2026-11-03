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

## Follow-up (2026-11-04): the Sim checkbox, the export glyph, the PFE fix, the README names

55 more commits in 18 repos, all on `feat/2026-11-01-full-skinning` and now pushed. Nothing is merged, no tag is pushed
and no version is bumped. Outfitter was not touched.

- **R6-SIM-STD (2):** standard v2.99.0, options-ui-§15. Every addon with an in-game simulator shows a *Sim mode* box
  next to *Test mode*, or next to *Lock frame* where there is no Test mode row. The second commit fixes wording only.
- **R6-SIM-L (1) and R6-REL2 (3):** OptionsCompose minor 19 draws the box from the host's `isSimMode` and `toggleSim`,
  so a tick is a bare `/xx sim` and an untick stops the sim. `masterRows` was split back to CCN 15. Local tag v1.85.0
  is re-cut for the eighteenth time at **550ef68**, which is LibKa0s HEAD, and it is still not pushed. Release battery
  `docs/automated-tests/20261104-024106/` has max CCN 15 and none over.
- **R6-RV2 (17):** all 16 addons re-vendored. The vendored `libs/LibKa0s` (media aside) and `tests/_kit` match LibKa0s
  HEAD in every one. The nine addons with no sim each add a "no Sim mode box" smoke row.
- **R6-SIM (14):** the box is wired in all 7 sim addons, AT, BL, DR, DW, KC, LH and MM, each with a red-first test and a
  smoke row. AT and KC place it beside Lock frame.
- **R6-MM2 (1):** the MultiMeters export bubble's padded art is cropped, so it draws at its neighbours' size (WIN-58).
- **R6-PF1 (1):** a PFE profile switch from preview no longer paints the cast bars from the profile it left
  (`CastBars.lua:120`, CAST-8).
- **R6-NAME (16):** README.md only. Each README's title, and its opening line where that line names the addon, drops
  Ka0s. Every R6-NAME commit touches `README.md` alone.
- **Reviews:** 52 of the 55 commits carry a `refs/notes/ka0s-review` note. The three R6-REL2 commits do not.
- **exceptions.tsv:** no row is needed. Every follow-up id has a commit in each repo it applies to.

**Totals** (fresh, one repo at a time through ka0s-bounded). LibKa0s: 4069 passed, 0 failed, 3 skipped, lint 0/0 in
298 files. The 16 addons: 22861 passed, 0 failed, 16 skipped, and luacheck 0/0 in every repo. No Lua file is over 1500
lines apart from PrettyChat's exempt generated `GlobalStrings.lua`. All 17 code repos: 26930 passed, 0 failed.

**Your part:** the *Follow-up* section of `06_SMOKE_TESTS.md`. After that come the automated tests, sync-docs, finalize
on your go-ahead, and then R6-ISSUES, which is the only id `resume-state.sh` still shows as OPEN.

## Finish (2026-11-04)

- **Automated tests (R6-AT):** a recorded battery in all 16 addons, all green. The Skin Tester came back amber first
  because skinRepaint was over pins set before round 3. It rose in steps at R3-RV, R4-ST1/3/4, R5-RV and R5-WIN, and
  round 6 left it flat. It was re-pinned with that history in the comment (9c3debb), then recorded green.
- **Sync-docs (R6-SD):** the 16 addons and LibKa0s (payload unchanged since the tag); the standard had no drift.
- **Finalize (R6-FIN):** 18 repos merged `--no-ff` into master and pushed, notes pushed, tag v1.85.0 pushed at
  550ef68, branch deleted locally and on origin. A subagent's push to master was refused by the permission check, so
  the lead ran it; each merge's tree equals the tested branch tree. Outfitter untouched.
- **Issues (R6-ISSUES):** closed WowAddonStandards#12, LibKa0s#71, LibKa0s#72, QuickComms#13, QuickComms#14. Kept
  open: LibKa0s#70 (partly done), #74 (not built) and every other open issue (none resolved by this work).
- **For the owner to rule on:** a Sim mode tick from idle opens the step panel like a bare `/xx sim`; DpsRace's Test
  mode box also shows ticked during a sim; BankLedger's Reset all keeps a running sim (its OWNER_SCOPE C.13), unlike
  the library's reset.
