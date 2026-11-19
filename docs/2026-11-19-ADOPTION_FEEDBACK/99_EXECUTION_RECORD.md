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
