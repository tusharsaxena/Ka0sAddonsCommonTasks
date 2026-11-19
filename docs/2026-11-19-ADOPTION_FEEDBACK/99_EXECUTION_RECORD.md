# Execution record

## M0: setup (2026-11-19)

- The owner reported every adoption wave A–D smoke check passed, and gave the go-ahead to merge. The adoption run was
  finalized before this run branched; see the adoption bundle's `07_EXECUTION_RECORD.md` → *Finalized*.
- Grilling: the owner's rulings are in `inputs/OWNER_FEEDBACK.md`. The read-only HUD header audit is in
  `inputs/HUD_HEADER_AUDIT.md`, and each deviation in it was ruled one at a time.
- Issues filed: LibKa0s#97 (skin-defaults audit) and LibKa0s#98 (show/hide fade).
- RangeMaster's session merged `feat/2026-11-19-dynamic-bands` (98ee004) and released RangeMaster to this run.
- AF-DR-CT (`0583bcc`): CommonTasks' CLAUDE.md treats DpsRace as retired. AF-DR-DC is an exception: dev-copilot names
  no addon, so there was nothing to change.

## M1: upstreams (workflow wf_ff8c9959-90a, 5 agents)

- **LibKa0s**
  - AF-LK-01 + #96 (`cbf3577f`, WidgetsDragHandle minor 15): marks read [?][settings][close]. Each mark is a 14 px
    frame, giving 6 px between arts where there were 10. The tints are the header's (`icon.tint`, `text.link`,
    `close.rest`/`close.hot`). The settings mark is on by default, and close is drawn only with `onClose`. #96 is
    fixed in code; the issue is still open.
  - AF-LK-02 (`efbed582`, Tip minor 2): the strip tooltip always opens above the strip. `tooltipPlace` is accepted
    but ignored (deprecated).
  - AF-DR-LK (`f468fe7c`): DpsRace is out of the `releasing.md` sweep. `CONSUMERS.md` only carries a note, because
    it is a stamped census and the next census re-run drops DpsRace.
  - AF-LK-03 (`24b9cea1`, `72653ecc`, `5e963659`): v1.107.0, with release gate green (lint 0/0, 4948/0/3 tests,
    0 functions over CCN 15). Tag `v1.107.0` is local only.
  - Review: clean, with two low advisories. A default gear with no resolvable opener does nothing. The mark tooltips
    fall back to the strip's description, so the M2 strip hosts pass explicit mark tooltips.
- **WowAddonStandards**
  - AF-STD-02 (`e0318a1`): DPS Race is retired from the roster and every live mention.
  - AF-STD-01 (`4c4f9d9`): the rule for which marks a window owes, and the drag strip's marks.
  - AF-STD-03 (`887b536`): v2.115.0.
  - Review fixes: `7409738`, `3668b89`. `check-standard` passes.

## M2: addons (workflow wf_e7b4fb4d-b80, 53 agents, none failed)

Each addon had a build agent, an independent review and a fix pass. Every review finding was fixed in the addon,
or is listed below as left to the lead.

- **Re-vendor (AF-RV-\*)**: all 19 addons are on LibKa0s v1.107.0 and the standard v2.115.0. Each writes a
  `docs/revendor/2026-11-19-v1.107.0/` delta report except RangeMaster, which has never kept one. The lead leaves it
  exempt rather than settle the repo's convention in one commit.
- **Strips (AF-STRIP-AT, AM, CM, KC, QC, RM)**: every strip passes settings and close handlers, and the strip
  `tooltipPlace` hooks are deleted. Absorb Tracker retired BAR-23. Aura Master marked five checks superseded.
- **Headers (AF-HDR-BL, LH, QC, WG)**: Bank Ledger, Loot History and WhatGroup gained a header lock and a
  `lock`/`unlock` verb. Quick Comms' pads carry lock, settings and close in the header row. Close hides that pad and
  stays per profile (review fix `b62f263`), and `/qc show` restores it.
- **Waivers (AF-WVR-ST, OR, SM, PGFE)**: one Documented deviations row each.
- **AF-CT-TEX**: every Combat Trail bar takes the active skin's statusbar texture. The review fix batches the Results
  redraw to one per frame.
- **AF-SM-RESIZE, AF-SM-TOMTOM**: Skill Master's main window resizes while unlocked, snapping to the step grid and
  capped by Master scale. Set waypoint uses TomTom when it is loaded. It leaves an earlier native pin alone (known
  limitation: a player's own pin cannot be told apart from Skill Master's).
- **AF-DW-TIP, AF-DW-ROLLHDR**: Drop Watcher's tooltips sit flush to the main window, and the roll companion has a
  header.

Left to the lead, and settled:

- **Aura Master**: a strip whose position reads secret shows no tooltip, because the strip's own placement hook is
  gone. Filed as LibKa0s#99 and cited in `known-limitations.md` and DRAG-20 (`5b3ada6`).
- **Combat Trail**: the race call-out's strip has no close, because the library builds it. Filed as LibKa0s#100. A
  Documented deviations row cites it until the library passes `onClose` through (`498b199`, then `d3c6c9b` to keep
  the hub under 400 lines). The owner has not reviewed this row yet.
- **Range Master**: the run branch conflicts with the other session's unmerged `fix/2026-11-19-beyond-shows-oor`
  in `README.md` and `docs/test-cases.md`. At finalize, merge one branch, re-run both suites and recompute the totals
  rather than take a side. The main checkout belongs to that session, so this run gated RangeMaster in a temporary
  worktree (removed in the clean-up).

## Owner report mid-run: a secret-number error in the HUD dock (LibKa0s#95)

The owner created a new Aura Master profile and closed the preset picker without choosing. That raised
`Widgets.lua:647: attempt to perform arithmetic on a secret number value`. Test mode ended, so the mode strip was
re-placed, and the strip's height read secret. The dock's `num()` asked only `type(v) == "number"`, which a secret
passes.

- LibKa0s `87ae35f3` (AF-LK-03 + #95): `num()` now reads an `issecretvalue` value as none. `Widgets.lua` moves to
  minor **29** (key 29.2.7.15.2.7.8.6.1.1). A new case in `tests/test_widgets_teststrip_dock.lua` fails without the
  fix. The gate is 4949/0/3 on both clients, with luacheck 0/0.
- The fix is folded into **v1.107.0**, which was never pushed. The local tag was moved to `87ae35f3`. The
  `28.2.7.15…` API documents never shipped, so they moved to the new key. The frozen automated-tests bundle
  `20261119-205557` records the gate before the fix. This record is where the re-cut is noted.
- All 19 addons re-copied `Widgets.lua`, one `AF-RV-*` commit each. Quick Comms' agent did its own (`95cdebe`).
  Loot History re-pinned minor 29 in three tests (`b9ea65e`, `d8437af`). The delta reports written earlier in this
  run name Widgets 28.
- LibKa0s#95 stays open until the owner's smoke check, then closes at finalize.

## Drop Watcher results recorded

The owner reported FEED-108 to FEED-111, SLASH-5, SLASH-10, STATE-11, SKIN-52 and COLL-10 passed. They are recorded
in Drop Watcher's `docs/smoke-tests.md` (`53e1804`).

## CP-1 (2026-11-19)

Re-gated at the pushed heads, Retail and WoW Forever under the bounded runner, plus `ka0s-bounded luacheck .`.
Every repo has 0 failures on each client it ships, luacheck 0/0, `docs/test-cases.md` matching `--list`, and no
authored file over the cap. PrettyChat's generated `GlobalStrings.lua` is carved out. The Forever failures in Bank
Ledger, Kick CD, Multi Meters, PGF Extension and WhatGroup are in Retail-only addons, whose TOCs list 120105 alone.
Skill Master ships WoW Forever only.

| Repo | Head | Retail | Forever |
|---|---|---|---|
| LibKa0s | 87ae35f3 | 4949/0/3 | 4949/0/3 |
| AbsorbTracker | 37a8638 | 1085/0/1 | 1085/0/1 |
| AuraMaster | ffeaa16 | 2553/0/1 | 2552/0/2 |
| BankLedger | 20320f7 | 1700/0/1 | not shipped |
| CombatTrail | d3c6c9b | 1589/0/1 | 1581/0/1 |
| ConsumableMaster | a4330fd | 1503/0/1 | 1503/0/1 |
| DropWatcher | 53e1804 | 2651/0/1 | 2543/0/108 |
| KickCD | 5f9d0c5 | 1733/0/1 | not shipped |
| LibKa0sSkinTester | 06f8d8a | 915/0/1 | 915/0/1 |
| LootHistory | d8437af | 2031/0/1 | not shipped |
| MultiMeters | 5ff37cf | 2642/0/1 | not shipped |
| OutfitterReborn | 7295c27 | 1600/0/31 | 1579/0/52 |
| PanelMaster | 0f4a663 | 1206/0/1 | 1206/0/1 |
| PartyFrameEnhanced | 132b941 | 660/0/1 | 660/0/1 |
| PremadeGroupsFilterExtension | ccae1e7 | 564/0/1 | not shipped |
| PrettyChat | 0085585 | 696/0/1 | 696/0/1 |
| QuickComms | b62f263 | 2093/0/1 | 2093/0/1 |
| RangeMaster | c56ef85 | 725/0/1 | 725/0/1 |
| SkillMaster | 3932243 | not shipped | 803/0/1 |
| WhatGroup | 70616c3 | 1137/0/1 | not shipped |

WowAddonStandards `3668b89` passes `check-standard`. All 21 run branches are pushed with their `ka0s-review` notes
where they exist. No tag is pushed: LibKa0s v1.107.0 is local, and the standard's v2.115.0 is cut at finalize.
The owner's smoke sheet is `SMOKE.md`.
