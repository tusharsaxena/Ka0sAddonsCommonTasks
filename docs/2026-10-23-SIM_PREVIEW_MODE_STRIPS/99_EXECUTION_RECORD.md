# 99 — Execution record

## M1 (2026-10-23, 14:22–15:20)

- 13/13 items landed and reviewed (`plan-data/m1-results.json`). One fix round: LK-90 (CLAUDE.md 1000–1500 band
  prose), commit 9949368.
- **Local tag move:** v1.76.0 was created by LK-90 at `82d76f6`; the review fix landed after it, outside the
  payload (`git diff v1.76.0 HEAD -- LibKa0s testkit` empty). The lead moved the tag to `9949368` (the branch head).
- Deviations worth knowing:
  - dev-copilot has no CHANGELOG.md; its 2.5.0 history lives in CLAUDE.md "Current version" (DC-00).
  - The standard's current entry lives in STANDARDS.md ## Changelog, and v2.86.0 moved to standards/CHANGELOG.md
    (WS-00).
  - LK-90 landed as two commits (`LK-90 (1/2):`, then `LK-90:`), per releasing.md step 7. Its CONSUMERS rows for
    MM/KC are planned; the census is re-run after M3.
- Pushed: WowAddonStandards a72d35a, LibKa0s 9949368, dev-copilot 6d45079, plus review notes. Tag not pushed.

## Addendum 01 (2026-10-23, during M2)

- **QC-05**, from an owner bug report (`inputs/qc-05-groups-preview.png`). The owner first said DropWatcher, then
  corrected it to QuickComms. In the Groups page's edit preview, the icons look faded and a dark circle sits over
  the dial icons; the preview should look exactly like live mode plus the PREVIEW tag.
- Queued as the last item of M3's QuickComms chain, debug-first. Smoke check SM-QC-8.
- **QC-06**, from an owner bug report (`inputs/qc-06-callout-strata.png`): the preview dial's hub dot and pointer
  draw over the New callout dialog. Probable cause, from reading the code: the dial header and the popup share the
  DIALOG strata, and the hub's front frame sits at header level + 20. Queued after QC-05. Smoke check SM-QC-9.

## M2 (2026-10-23)

- 21/21 items landed and reviewed (`plan-data/m2-results.json`). Fix rounds:
  - PC-RV: the working tree was restored from the index, with no new commit.
  - MM-01: the test was made to really pin the minimized title.
  - BL-10: smoke checks whose procedure changed were reset to pending.
- **Standard reference.** The installed wow-revendor-standards contract forbids writing the standard's version into
  an addon. So the RV items' `grep v2.87.0` verify finds nothing by design. The three-place references were
  confirmed current against the local v2.87.0.
- **Span bundles.** Several RV items also wrote span bundles, `docs/revendor/2026-10-23-v1.75.1-v1.75.2/`, for the
  earlier unrecorded patch re-vendors.
- The lead re-ran the gates; all green. Pushed all 14 addon branches with their notes.

## Owner smoke, M2 (2026-10-23)

- **Passed:** every M2 check the owner ran, apart from the two findings below. The rows in `06_SMOKE_TESTS.md` are
  updated at CT-01, once the per-addon Result lines are filled in.
- **KickCD "Error loading modules/Sim.lua"** is not a defect. KC-05 created the file while the client was running,
  and WoW loads only files that existed at launch. A full client restart is needed once `/kcd sim` lands.

## Addendum 02 (2026-10-23, during M3)

- **LK-91**, from an owner report (`inputs/addendum-02-simpanel-overlap.png`): a long step label runs under the
  command column, because the label has a LEFT anchor only. The fix is in SimPanel and in PerfPanel's twin renderer.
  The local tag then moves (old and new sha recorded below by LK-91), and every addon re-vendors it as
  `<PFX>-RV2`. KC, MM and QC do so after their M3 chains.
- **BL-11**, from an owner report: `/bl sim` stalls a few seconds on step 4 (the flask deposit). Debug-first.
- **LK-91 landed** (LibKa0s `7e81ff7`): the step label is bounded LEFT at 26 and RIGHT 8 short of the command, word
  wrap off, in SimPanel (minor 5 kept) and PerfPanel (7 → 8, Perf key 15.1.1.8). Gates: luacheck 0/0 in 181 files,
  2578 passed / 0 failed / 2 skipped. **Local tag v1.76.0 moved** `9949368df8db12e51c9c51e403738989c87709a5` →
  `7e81ff7e989aacef8063bfd56e4fcc5742157667` (annotated, not pushed).
- **BL-11, cause found and fixed.** It was not the item-info load the spec led with. BankLedger settled a reconcile pass
  only when it RECORDED a movement. A movement the capture gate refused (blacklist, quality threshold, excluded store)
  held the baseline for the full 6 s SETTLE_TIMEOUT, and the sim gate stayed closed meanwhile. The owner's
  SavedVariables blacklist Hearthstone 6948, which the bank scenario moves; that link is inferred, and SIM-13 checks
  it in game. The ledger now settles once every movement found is accounted for. Pacing tests are red before the fix
  (6.50 s) and green after.
- **RV2 review flags.** AT-, PC- and PM-RV2 reviews flagged an on-disk LF/CRLF mix in a doc the agent appended to.
  The committed blobs were right, and the fix rounds restored the files. The lead re-ran all 11 RV2 addons plus
  BankLedger: clean trees, every gate green.
- **Addendum 03, LK-92 (lead).** The README's Sim row pointed at 2.2.4. It now links 2.3.5, a note from LK-91's
  review. The payload is unchanged (`git diff 7e81ff7 HEAD -- LibKa0s testkit` is empty), so no re-vendor is needed.
  **Local tag v1.76.0 moved** `7e81ff7` → `e692491`.
- **Lead slip, caught before it did damage.** Saving the run's results as `plan-data/addendum-02-results.json`
  matched the `addendum-*.json` glob that next_args.py and the executor's item lookup read. It was renamed to
  `results-addendum-02.json`.

## Owner smoke and requests (2026-10-23, evening), addendum 04

- **Passed:** BankLedger sim ("works fine"), and the QuickComms preview, which now looks right
  (`inputs/addendum-04-21.png`), so QC-05 is confirmed.
- **BL-12:** the idle sim panel shows the placeholder "item A/B" names; the run shows the real items. The idle view
  should match the run.
- **QC-07 (owner feature request):** in preview and test mode, a click prints `[QC] /p <text>` with tokens filled or
  mocked, and nothing is sent.

## Owner smoke, M3 (2026-10-23, late evening)

- **Owner: "All 4 working as expected".** That covers `/kcd sim`, `/mm sim`, the step-panel label fix (SM-LK-1) and
  BankLedger's idle panel naming the real items (SM-BL-15). It came after a full client restart.
- Pushed so far for M3: every run repo except QuickComms, which waits for QC-07. Heads: LibKa0s e692491,
  AbsorbTracker 13c0a4b, AuraMaster bcaec7e, BankLedger 4c665cf, ConsumableMaster e05733d, DropWatcher 6f69e6e,
  KickCD 58f1a9e, LootHistory 06d6a6c, MultiMeters e8771f8, PanelMaster 9c950c3, PartyFrameEnhanced a24e064,
  PGFE eccfe7b, PrettyChat e644ada, WhatGroup ec996a4.

## M3 and closeout (CT-01, 2026-10-23)

- M3: 45/45 items landed and reviewed, including addenda 01–04 (QC-05, QC-06, LK-91, LK-92, 14 × RV2, BL-11, BL-12,
  QC-07). Fix rounds: MM-10, MM-12, MM-16, MM-17, QC-02, QC-06, KC-02, KC-08, plus the eol-only RV2 rounds.
- **QC-07** finished a raw preview echo that had existed since 2026-10-20. It now fills tokens and mocks missing
  ones as bracketed names (`<target>`, `<key>`), which avoids fake player names or links that look real. It also
  echoes the nothing-sent reason and the test placeholders. The click is caught by the existing insecure OnClick hook,
  and live clicks are unchanged.
- **Owner smoke:** M2 and M3 all passed, recorded on each repo's own smoke file (the run branch commits "Record the
  owner's 2026-10-23 smoke pass…") and in `06_SMOKE_TESTS.md`. Still pending:
  - SM-QC-10 / QuickComms PREVIEW-10 (QC-07; it landed after the owner's pass).
  - SM-DC-21 and SM-DC-22: dev-copilot 2.5.0 bump-version Step 1b. They need the plugin updated after the merge.
  - BankLedger DEGRADED-13 and LootHistory DEGRADED-13: they need LibKa0s removed; the owner was told to skip them.
  - PartyFrameEnhanced FADE-5: it predates this run (2026-10-13) and was never signed off.
- The owner's merge go-ahead was given in chat on 2026-10-23: "After the current workflow completes, go ahead and
  commit, merge and push all changes".

## CT-02 — finalized (2026-10-23)

- Merged `--no-ff` and pushed, in this order:

  | Repo | Merge commit |
  |---|---|
  | WowAddonStandards | a7064a8 |
  | LibKa0s | 9df6df8 |
  | dev-copilot | bf93ff7 |
  | AbsorbTracker | 1839b80 |
  | AuraMaster | c77c7fc |
  | BankLedger | 7bb8fb0 |
  | ConsumableMaster | 80943b2 |
  | DropWatcher | 847e2ad |
  | KickCD | 367e275 |
  | LootHistory | 716859a |
  | MultiMeters | d7d6a1f |
  | PanelMaster | e0a9ee3 |
  | PartyFrameEnhanced | 32ad3d5 |
  | PGFE (main) | e5b741a |
  | PrettyChat | b08c579 |
  | QuickComms | 0487489 |
  | WhatGroup | f31794f |
  | Ka0sAddonsCommonTasks | 206131e |

- Tag `v1.76.0` was pushed: tag object 600303b, commit e692491.
- **The run branch is deleted locally and on origin in every repo.** BankLedger's needed `-D`: its last commit (the
  smoke record) was never pushed to the branch, so the branch was checked to be contained in master first.
- No stashes or extra worktrees remain anywhere. MultiMeters#60 and KickCD#38 are CLOSED.
- No addon version was bumped. dev-copilot 2.5.0 is merged; the owner updates the installed plugin.
