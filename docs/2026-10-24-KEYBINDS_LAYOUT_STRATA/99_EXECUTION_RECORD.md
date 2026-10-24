# Execution record

(Written during execution: outcomes per milestone, deviations, local-tag moves, review fix rounds.)

## M1 — Upstream (2026-10-24)

- Run `wf_eb43309a-9a5`: all 23 items landed and reviewed. Three reviews asked for a fix, and each fix round
  resolved it: WS-04 (a stray period in debug-logging.md:22), LK-11 (the capture accepted a left or right
  mouse-button chord) and WS-07 (stale major counts in library-stack-§7 and open-evolutions).
- LK-90 found three functions above CCN 15 from LK-10..LK-12 and split them in a third commit (3c2bb20). The
  failing first release bundle is kept as the record.
- The local tag v1.77.0 is at 78240f7 and is not pushed. Checkpoint row in `checkpoints.tsv`.

## M2 — Addons (launched 2026-10-24)

- The owner had recorded no decisions on the preview page (`decisions` export empty). So M2 was split:
  run `wf_9c7197ff-aa6` covers only the RV and KB items (22). The 15 ZS items are held until the owner has had a
  chance to reject strata changes, and are then launched from a fresh `accepted.json`.
- Installed dev-copilot is 2.4.0. Both re-vendor commands are unchanged on dev-copilot master since 2.4.0
  (`git log 8c562da..master -- commands/wow-revendor-*.md` is empty), so the installed procedures were used.
- Run `wf_9c7197ff-aa6` finished: 22 of 22 landed and reviewed, none blocked, no library gap. The reviews of BL-KB,
  LH-KB and WG-KB each asked for a fix (a wrong test citation in a comment, stale tab counts, a stale TOC annotation),
  and each fix round landed it.
- RV deviation, every addon: the item's VERIFY `grep 2.88.0 *.toc README.md CLAUDE.md` finds nothing. The installed
  wow-revendor-standards procedure writes no standard version into a repo file, so this was intended. The reading
  version is recorded in each addon's `docs/revendor/2026-10-24-v1.77.0/05_SUMMARY.md`.
- RV: each addon's Options degradation stub gained the four new no-op members (`KeybindingsTab`, `KeybindRows`,
  `KEYBINDS_UNCHANGED`, `StrataTooltip`), as kit 42's surface-parity case requires.

## Owner decisions (2026-10-24)

- The owner accepted all six calls on the preview page (CALL-01..CALL-06) and said: "in general, go ahead with all
  changes you are confident about". `accepted.json` (1ddc875) applies the page defaults to everything else: 438
  changes land. Read as the M3 go-ahead too, at the same >= 50 bar.
- ZS (strata) launched as run `wf_bf619483-f06`. M3 design launched as run `wf_0f27c45a-4b1`.
- Issues filed for the ideas the review moved out of item 020 (XC-34) and for CALL-05 (U-13):
  QuickComms#10 (QUI-L16), QuickComms#11 (QUI-L30), PartyFrameEnhanced#16 (PAR-L17), PrettyChat#19..#22
  (PRC-L02, L06, L11, L12), WowAddonStandards#13 (U-13). All `state:untriaged`, `severity:low`.

## M2 — strata (ZS)

- Run `wf_bf619483-f06`: 15 of 15 landed and reviewed, no library gap. PC-ZS's review asked for two doc fixes,
  and its fix round made them.
- **Lead fix, WG-ZS (f664624).** The implementer took WHA-Z01 beyond the accepted text. It made the popup body
  ignore the mouse permanently, so a click on the visible popup fell through. The accepted text disables the body
  only if an in-game probe allows it, and otherwise records the residual. f664624 restores `f:EnableMouse(true)`
  and records the soft-hide residual in the ARCHITECTURE register. POPUP-10 is now the owner's in-game probe.
- Accepted deviations, recorded in each commit body:
  - KickCD and PrettyChat name the table `NS.Const.LAYERS`, their existing constants module.
  - AbsorbTracker, ConsumableMaster and AuraMaster use the standard's level bands where the analysis drafted
    other numbers.
  - DropWatcher sets the Offer panel's strata at build, not in `dock()`.
  - Unaccepted ids were left out, as specified (for example LOO-Z07, PAR-Z02, PAR-Z05, QUI-Z08).

## M3 — settings layout (020), planned

- Design run `wf_0f27c45a-4b1`: 9 agents. The adversarial review raised 11 issues; all were resolved in the fix
  round.
- U-14 was dropped from the library: every accepted change it would have served can be built on the existing
  surface, and LK-95 files an issue for it.
- 4 layout ids were vetoed for conflicts: AUR-L01, CON-L02, DPS-L14 (CALL-03 labels) and KIC-L29 (XC-33 is
  all-or-none). That leaves 326 to make.
- addendum-01: 45 items (7b60430).

## M3 — Upstream layout (2026-10-24)

- LK-95 moved the local tag v1.77.0: commit 78240f7b2d69df27b74fc9280cbfbf7b95dd4f1f (tag object
  7380d3662be0568acf9a0d224a6aef8ac6df93ce) -> afae2f75cb7ff61c57156d9a3d8a6b2b9f4c5e10 (tag object
  b2b8ee25c5f9fa26db146254bf786b366dec986b); not pushed. Release bundle 20261024-121210: lint 0/0 in
  197 files, 2749 tests 0 failed, complexity 0 over CCN 15.
- LK-95 filed the deferred-surface issue (U-14 flow-engine seams, the `note` row, the Position-block
  composer; U-08d `PageBanner{ acts }`): https://github.com/tusharsaxena/LibKa0s/issues/59
- WS-95 closed the v2.88.0 settings-layout rulings: rulings (1)-(16) contiguous, ripples match the
  897fbd3..HEAD diff, cross-surface names and the LOCK_PREVIEW_TIP sentence match LibKa0s's
  version-30.2.34.3.5.9.2.11.4.2.1.3 Options doc and OptionsCompose.lua, check-standard green.
  U-13 (CALL-05) was not filed again: the lead had filed
  https://github.com/tusharsaxena/WowAddonStandards/issues/13 (deduped by title search), and
  open-evolutions entry (b) now links it. options-ui-§16's `tooltips` bullet now names #106, so the
  anti-pattern's group clause cites a section that states it.

## M3 — settings layout, outcomes (CT-03)

- Run `wf_281e9cd3-534`: 44 of 44 landed and reviewed, none failed, no library gap. 107 agents.
- Upstream: WS-30..WS-38 and WS-95 close standard v2.88.0 (options-ui-§21, §7, §12-§16, the ripple). LK-30..LK-32
  add OptionsCompose minors 9-11. LK-31 and LK-32 each took a review fix round.
- RV2: all 15 addons re-vendored the moved tag. Fix rounds on AT, BL, PC, PG, QC and WG, all doc or alignment fixes.
- LY: all 15 landed with the stored-path/default guard test. Every accepted id was made except the four vetoes
  (AUR-L01, CON-L02, DPS-L14, KIC-L29). Ids already delivered in M2 are recorded in `exceptions.tsv`
  (BL-LY:BAN-L14, WG-LY:WHA-L14, LH-LY:LOO-L18, MM-LY:MUL-L-new4, MM-LY:MUL-L22, QC-LY:QUI-L32).
- LY fix rounds (one each, all resolved): AT, AM, BL, CM, DW, KC, LH, PC, PF, PM, QC. Mostly missed doc or smoke
  ripples. Two were code:
  - **KC-LY 213ae29:** a real regression. After a tab click, the Units band's Enable this unit and Link to Target
    checkboxes, and a linked Focus strip, stopped refreshing. Fixed, with a test.
  - **DW-LY 429d7f4:** the footer's not-tracking tooltip still pointed at the retired Settings > Situations page.
    It now reads Settings > Drops > Situations.
- LH-LY: a docs sweep (a0574aa) briefly rewrote 42 files in frozen bundles. 0f6d75b restored them byte for byte;
  `git diff 5fe49a4 HEAD -- docs/audits docs/automated-tests docs/reviews docs/revendor docs/superpowers` is empty.
- §21 location strings: AT, CM, MM and PF write "the General page > …" where the item text said "General > …",
  because §21 requires that form when an addon also has a General tab.
- Open, for the owner:
  - **AuraMaster ellipsis.** Delete container, Delete this category and Forget unreadable categories cannot carry
    §21's "…" under owner ruling T-1 (ASCII locale). The row in ARCHITECTURE.md > Documented deviations is pending
    the owner's call: either ratify it, or widen T-1.
  - **AbsorbTracker band height.** The Target/Focus band is one row taller than Player's, against §14's new MUST,
    because ABS-L11 was not accepted. This predates the run and is not registered.
  - **WhatGroup units.** §21 units are not applied to Delay after joining, Width or Height (not among WG's ids).
  - **LibKa0s docs/api/CONSUMERS.md:750** lists MultiMeters as a planned ResetAllTooltip adopter. MultiMeters'
    General Defaults is a page reset, so it does not adopt it. The next census corrects the planned row.
- Smoke handling varies. Some addons rewrote the existing checks that name old labels and reset them to pending
  (AT, BL, PC, PF, PM, CM). Others kept the owner's passes and added new LAYOUT/PANEL checks that govern where
  they differ (DW, KC, MM, QC, PG, WG; WG reset PANEL-2).

## Handover (CT-01)

- 105 of 107 items have landed: M1 23, M2 37, M3 44, plus CT-03 and this record. Only CT-02 remains, the
  finalize, which waits for the owner's merge go-ahead.
- Every run branch and `refs/notes/ka0s-review` is pushed: WowAddonStandards, LibKa0s, dev-copilot, the 15 addons
  and this repo. The v1.77.0 tag (afae2f7) is local only, and CT-02 pushes it after LibKa0s merges.
- No addon version was bumped and no release was cut.
- The owner's checks are every row in `06_SMOKE_TESTS.md`, all pending. The DC rows need dev-copilot 2.6.0
  installed (installed: 2.4.0).
- The owner's open calls are listed under "M3 — settings layout, outcomes": the AuraMaster ellipsis register row,
  the AbsorbTracker band height, the WhatGroup §21 units, and the CONSUMERS planned-adopter row.
- CT-02 order: WowAddonStandards → LibKa0s (then `git push origin v1.77.0`) → dev-copilot → the 15 addons →
  Ka0sAddonsCommonTasks. Merge `--no-ff`, then delete the branch locally and on origin. Then remove every stash
  and worktree this run created.

## Addendum-02 — one-button keybindings row (015 follow-up)

- LK-96 moved the local tag v1.77.0: commit afae2f75cb7ff61c57156d9a3d8a6b2b9f4c5e10 (tag object
  b2b8ee25c5f9fa26db146254bf786b366dec986b) -> 2f2b2e22b4c9219cd8a4101d7e894681c7aea16e (tag object
  e9b126d961c2970e5b14d0566480f7c1d8b5e5e8); not pushed. Release bundle 20261024-162023 (measured
  7790dca): lint 0/0 in 197 files, 2755 tests 0 failed, complexity 0 over CCN 15, blindFiles 0,
  crashedFiles 0.

## Pre-merge (CT-02 stage 1) and the one-key-button follow-up (addendum-02, CT-04)

- The owner gave the merge go-ahead. Stage 1 (run `wf_dba2ebab-2ce`) did a content-only doc sync and a bounded gate in
  18 repos, all green. 11 repos committed `CT-02: sync docs before the merge`; 7 were clean.
  - Declined, for the owner: dev-copilot README.md:5 still says standard v2.86.0 (bump-version rolls it).
    WhatGroup.toc:96 cites core/CoreSetup.lua:34, which is now :41 (a comment; comments were out of scope).
    LibKa0s README notes dated "as of v1.75.0" were left as dated.
- Before the merge, the owner asked for one key button and Clear per action on the in-addon Keybindings tab, with
  Options -> Keybindings left as it is. Planned as addendum-02 (f33f7f7) and run as `wf_aca45a46-8d2`: 19 of 19 landed
  and reviewed.
  - Fix rounds: LK-40 (the kit's slot-2 driver reported KEY_BOUND for ESCAPE or a lone modifier), and RV3 for AM, CM,
    KC, PC, PG, PM and QC.
  - Kit revision stays 42 because v1.77.0 has not shipped. The change is recorded in the version-42 doc.
- The owner also asked for the Options -> Keybindings sections to sort by "Ka0s <name>". This is not done, and cannot
  be done that way. Blizzard's page does not sort: `Blizzard_SettingsDefinitions_Frame/Keybindings.lua` orders sections
  by first appearance in GetBinding order, which is addon load order (folder names). Only renaming the addon folders
  would group them, and that would break saved variables and installs. Reported to the owner.

## CT-02 — finalize (owner go-ahead, 2026-10-24)

- Merged `--no-ff` into master and pushed, in this order. Each merge tree equals the gated branch tree, because master
  had not moved during the run.
  - WowAddonStandards 36da4ef, then LibKa0s 3331f63, then the v1.77.0 tag push (tag object e9b126d, commit 2f2b2e2).
  - dev-copilot 226150a.
  - AbsorbTracker afbbda3, AuraMaster 74e9b0f, BankLedger a021130, ConsumableMaster 23a93ad, DpsRace ae39e77,
    DropWatcher 5227a11, KickCD fe640c4, LootHistory c7cf49c, MultiMeters c20a105, PanelMaster 88f0c46,
    PartyFrameEnhanced 573482c, PremadeGroupsFilterExtension 278affe, PrettyChat 96b2a55, QuickComms 3b98df7,
    WhatGroup a2a9949.
  - Then this repo.
- The run branch is deleted locally and on origin in every repo. `git stash list` and `git worktree list` show nothing
  this run created. No addon version was bumped and no release was cut. The dev-copilot release (2.6.0 is in its
  manifest) and the standard's version stamps are unchanged.
- Smoke: every row in `06_SMOKE_TESTS.md` is pending, for the owner.

## The owner's four calls (addendum-03, CT-05)

- The owner answered the four open calls: "1. Widen T1  2. Accept ABS-L11  3. Ok  4. Correct it". Planned as
  addendum-03 (c1fda62) and run as `wf_5f4fb756-6ff`: 4 of 4 landed and reviewed. The run branch was recreated from
  master in the four repos and here.
  - **AM-OC1 (1797f1e):** T-1 now allows U+2026 as well as the em dash. "Delete container…", "Delete this category…"
    and "Forget unreadable categories…" carry the ellipsis. The §21 deviation row is removed. Smoke check
    SETLAYOUT-9 (SM-AM-OC1) is pending.
  - **AT-OC2 (ae944df, review fix 90bf891):** ABS-L11 is made. The unit band is one four-cell row for every unit, so
    the band height no longer depends on the unit. The fallback was not taken, because the mocks cannot measure text
    width. The owner's LOOK-19 (SM-AT-OC2) settles truncation in the client. The enable cell keeps the shipped label
    "Enable this unit" (AT-LY).
  - **WG-OC3 (8ce9b7a):** the labels are "Delay after joining (seconds)", "Width (px)" and "Height (px)".
  - **LK-OC4 (2c0396a):** CONSUMERS lists the seven real O.ResetAllTooltip adopters with file:line. MultiMeters is
    out (it uses a page reset). This is docs only; the pushed v1.77.0 tag and its CHANGELOG entry are unchanged.
- Gate: LibKa0s 0/0, 2753 passed; AuraMaster 0/0, 2150; AbsorbTracker 0/0, 906; WhatGroup 0/0, 967. No authored .lua
  file is over 1500 lines, and vendor drift is 0.

## Owner smoke (2026-10-24)

- The owner reported: "All smoke tests pass". All 83 rows in `06_SMOKE_TESTS.md` are recorded as
  `pass (owner, 2026-10-24)`, including the DC rows (dev-copilot 2.6.0), POPUP-10, SM-LK-40a, SM-AM-OC1 and SM-AT-OC2.
- The addons' own `docs/smoke-tests.md` "Pending sign-off" lists still name this run's checks; they were not
  edited by this record.
