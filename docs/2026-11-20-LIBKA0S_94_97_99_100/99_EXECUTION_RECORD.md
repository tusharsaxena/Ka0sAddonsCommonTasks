# Execution record: LibKa0s #94, #97, #99, #100 (2026-11-20 to 2026-11-21)

The run branch is `feat/2026-11-20-libka0s-94-97-99-100` in 22 repos: LibKa0s, WowAddonStandards, this
repo and the 19 addons, RangeMaster included. Progress comes from git (`plan-data/resume-state.sh`).
At CP-1 every manifest item has a commit whose subject starts with its id, and `exceptions.tsv`
needed no rows.

## What happened, in order

1. **M0, 2026-11-20 morning.**
   - The run bundle was written (SD-PLAN).
   - The skin-defaults audit for #97 was carried out: 20 tables, 820 rows, a 75-item GAP list and 31
     questions for the owner (SD-AUDIT, `docs/2026-11-20-SKIN_DEFAULTS_AUDIT/`).
   - The first session was interrupted when the PC shut down overnight. The workflow could not be
     resumed, so a continuation workflow re-checked every committed item before going on.
   - The owner took every recommendation on U-1 to U-31, and changed one: U-31 (SkillMaster#9) was
     built in this run (SD-RULE).
2. **Logos, SkillMaster#10, U-21, owner requests made during the run.**
   - SkillMaster and RangeMaster have new TGA logos, regenerated from the owner's PNG and JPG.
   - SkillMaster#10 was filed: a verification pass on all skills, stats and professions, prompted by a
     report of a missing mace row. A Hunter cannot use maces, so that row is correct, and the issue
     records this.
   - U-21 was narrowed: the dropdown skips measuring only labels and widths that read secret. The
     owner accepted this (SD_RULE.md, Later rulings).
3. **M1, the library and the standard.**
   - **LibKa0s v1.108.0** is tagged locally at `56c20b76`:
     - #94: a footer lays out only the marks it shows.
     - #99: a strip tooltip opens above the nearest readable ancestor.
     - #100: Callout passes `onClose` and `onSettings` through.
     - #97: the library skin-default gaps SD-LK-97.1 to .19.
     - The kit's skin-switch guard (kit revision 58, SD-LK-GUARD).
   - **Review fixes before the tag:**
     - Batch B: a weak test was strengthened (`fb5b1b2c`).
     - Batch C: the font row on the bind route was fixed (`7c2bbee1`).
     - GUARD: the Forever memory gate failed at 306 MB against a 256 MB budget. The cause was a
       weak-keyed pull-out pool in a test fixture that held every client (`28c679f0`). Separately,
       the scanner crashed on names ending in a digit or underscore (`f641c0ad`).
     - Release: six functions above CCN 15 (the worst at 23) were split, with no change in
       behavior.
   - **Standard v2.116.0** is tagged locally at `4bfa42c`. It adds:
     - R-2, every option default follows the skin;
     - the revision-58 guards;
     - the preview stand-in class (U-24).

     The review's two nits were fixed and the tag was moved onto the fix.
4. **M2, the 19 addons (workflow `wf_fd79a774-21b`, 47 agents, about 5.9 h).**
   - In each addon:
     - LibKa0s v1.108.0 and the standard v2.116.0 were re-vendored (SD-RV-x);
     - the audit fixes, the owner's U rulings and the R-2 one-time steps were applied, and every
       drawn surface was declared to the skin-switch guard (SD-SK-x).
   - The extras: SD-CT-100, SD-AM-99, SD-DW-94, SkillMaster#9 (built under SD-SK-SM), and MultiMeters
     dropping its in-combat client-menu fallback.
   - Each addon had an independent review:
     - **Findings, then fixed and re-reviewed clean:** AbsorbTracker (2), Combat Trail (2), Drop
       Watcher (1) and RangeMaster (2).
     - **Clean on the first review:** every other addon.
   - All 19 final reviews are clean. The low observations they leave are listed below.
5. **SD-CT-DEF, an owner request made during the run (2026-11-20 20:50).**
   - Combat Trail's race call-out takes the owner's own settings as its defaults: the glow 2 px thick
     at offset 1, 1, drawn in the black swatch with *Use the skin's color* off.
   - It is a documented deviation from skinning-§9 in Combat Trail's `docs/ARCHITECTURE.md`. It
     overrides U-1 for the glow color only (SD_RULE.md).
   - It was built on a side branch so it would not collide with the running Combat Trail agent. That
     branch was pushed at the owner's request (`4f440c1`), merged into the run branch (`93ef4fa`, one
     smoke-table conflict resolved), and then deleted, along with its worktree.
   - An independent review of the merge found four low issues: one stored key, two missing test cases,
     a note about `Set(nil)`, and six doc drifts. All four were fixed in `888d391`, a mutation check
     confirmed the new tests catch a regression, and a review note was recorded.
6. **Lead fixes before CP-1.**
   - SkillMaster: a review nit, the card tooltip comment moved back above its function (`3b04e20`).
   - An empty, untracked `media/sounds` folder left by the icon prune in the Skin Tester was removed.

## CP-1 gate (2026-11-21, about 01:30)

Each repo was tested on every client it ships for. Every run passed.

| Repo | HEAD | Retail | WoW Forever | luacheck |
|---|---|---|---|---|
| LibKa0s | `56c20b76` | 5076 passed / 0 failed | 5076 / 0 | 0 / 0 (378 files) |
| WowAddonStandards | `4bfa42c` | `scripts/check-standard.sh` exit 0 | | |
| AbsorbTracker | `d6ec520` | 1093 / 0 | 1093 / 0 | 0 / 0 |
| AuraMaster | `c4b108b` | 2570 / 0 | 2569 / 0 | 0 / 0 |
| BankLedger | `d3453ec` | 1724 / 0 | (Retail only) | 0 / 0 |
| CombatTrail | `888d391` | 1625 / 0 | 1615 / 0 | 0 / 0 |
| ConsumableMaster | `be5e0ef` | 1523 / 0 | 1523 / 0 | 0 / 0 |
| DropWatcher | `7c42f4f` | 2720 / 0 | 2608 / 0 | 0 / 0 |
| KickCD | `4dff0e8` | 1737 / 0 | (Retail only) | 0 / 0 |
| LibKa0sSkinTester | `d4bb757` | 937 / 0 | 937 / 0 | 0 / 0 |
| LootHistory | `949b406` | 2052 / 0 | (Retail only) | 0 / 0 |
| MultiMeters | `52c1c12` | 2659 / 0 | (Retail only) | 0 / 0 |
| OutfitterReborn | `1115e72` | 1613 / 0 | 1592 / 0 | 0 / 0 |
| PanelMaster | `c6ad6be` | 1211 / 0 | 1211 / 0 | 0 / 0 |
| PartyFrameEnhanced | `0805906` | 673 / 0 | 673 / 0 | 0 / 0 |
| PremadeGroupsFilterExtension | `08535eb` | 583 / 0 | (Retail only) | 0 / 0 |
| PrettyChat | `b4c0756` | 704 / 0 | 704 / 0 | 0 / 0 |
| QuickComms | `4906e2a` | 2105 / 0 | 2105 / 0 | 0 / 0 |
| RangeMaster | `c02e49f` | 793 / 0 | 793 / 0 | 0 / 0 |
| SkillMaster | `3b04e20` | (Forever only) | 817 / 0 | 0 / 0 |
| WhatGroup | `c66a3f7` | 1139 / 0 | (Retail only) | 0 / 0 |

No authored file is over the 1500-line cap. The only file over it is PrettyChat's generated
`GlobalStrings/GlobalStrings.lua`, which is exempt by `layout-§1` and unchanged by this run. Every
tree was clean.

## Low observations the final reviews left open

None of these blocks the merge. They are recorded here so they are not lost.

- **AuraMaster.** The v21 step cannot tell a v17 template write apart from a player who unticked the
  companion while keeping the default color. The two are the same on disk, and the ruling accepts
  this.
- **BankLedger.** v1.108.0's `W.OwnerWarnings` was not adopted, because the run skipped issue filing.
  The stripe and hover guard surfaces cannot catch an alpha-only regression; other tests cover it.
- **Combat Trail.** A profile that took the skin step on pre-fix commit `e1932bd` skips the R-2
  keep-pick pass. This only matters if someone loaded this unmerged branch before `c9800ea`.
- **ConsumableMaster.** The settings description surface passes on the face moving, so only
  `test_skin_settings` pins SD-SK-CM.1. SKIN-31's old Passed line predates U-16.
- **KickCD.** The charges badge draws no shadow with Ignore fonts on, which matches the countdown.
- **MultiMeters.** Under Ka0s Default the tooltip's classless bar is the gold accent while the cell
  stays slate. One OVERRIDE row cites A7 where skinning-§7 fits better. The broad skinValues
  substrings for composed swatches would let a future swatch with no companion pass.
- **OutfitterReborn.**
  - `Glyph.Tint` lets a `false` color through. This is latent, because storage turns it into nil.
  - Picking white now stores no color and draws `icon.tint` (U-22).
  - A reused item row can flash the wrong color for one tick on a skin switch.
- **PartyFrameEnhanced.** The stand-in's skinValues rows cite "SD-RULE" as the cause, not the class
  name.
- **QuickComms review (process).** A reviewer ran `rm -rf` on a shared scratchpad folder another agent
  was using. Only scratch files were affected. No repo work was lost: every repo's gate and history
  checked out.
- **SkillMaster.** The U-7 Journal header tooltip lines have no automated test; smoke check SM-SKIN-6
  covers them.
- **WhatGroup.** The degraded popup's edge test would also pass on master. The kit's
  `test_skin_values` is the check that catches the change.

## Still owed

- The owner's smoke test (`SMOKE.md`).
- At finalize:
  - correct the LibKa0s CHANGELOG [1.108.0] line that still names standard v2.115.0 instead of
    v2.116.0;
  - fetch, and renumber if another session has released a tag, then push tags v1.108.0 and v2.116.0;
  - merge `--no-ff` in dependency order;
  - close #94, #97, #99 and #100, and SkillMaster#9;
  - delete the run branches.
- No addon version is bumped in this run.
