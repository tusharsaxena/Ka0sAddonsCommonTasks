# Adoption feedback run (2026-11-19)

This run addresses the owner's feedback on the LibKa0s v1.105 adoption smoke (`inputs/OWNER_FEEDBACK.md`, which
holds the verbatim feedback, the screenshots and every ruling). Branch: `feat/2026-11-19-adoption-feedback` in every
repo it touches. The manifest is `plan-data/items.tsv` (50 items). Progress comes from git through
`plan-data/resume-state.sh`, and `RESUME.md` says how to pick up.

## Milestones

**M1. Upstreams.**
- **LibKa0s**
  - AF-LK-01: the drag strip's marks read [?][settings][close] from left to right (today [settings][close][?]). The
    settings and close marks are on by default, and a strip opts out. The marks sit closer together. Their tint at
    rest and on hover is the window header's: the header marks' normal tint and gold hover, red hover for close.
  - AF-LK-02: the strip's tooltip always attaches above the strip, below only without room. A host's
    `tooltipPlace` no longer moves the strip's own tooltip.
  - AF-DR-LK: DpsRace leaves CONSUMERS and the live docs.
  - AF-LK-03: release v1.107.0 with an automated-tests record. The tag stays local until the owner's go-ahead.
- **WowAddonStandards**
  - AF-STD-01: the HUD header rule. A primary window's title-bar header carries close, settings and lock. A
    secondary window carries close. Window controls never go in a footer, which holds actions only. Waivers go in
    the addon's Documented deviations. The rule also states the strip mark order.
  - AF-STD-02: DpsRace off `ADDONS.md` and every live mention.
  - AF-STD-03: the release record.
- **dev-copilot** (AF-DR-DC) and **CommonTasks** (AF-DR-CT): DpsRace's live mentions.

**M2. Addons.** One workflow agent per addon, with an independent review of each.
- Every addon re-vendors v1.107.0 and refreshes its standard reference (AF-RV-*). DpsRace is retired and gets
  neither.
- Strip wiring (AF-STRIP-*, in AT, AM, CM, KC, QC and RM): every strip passes settings and close handlers, and the
  strip `tooltipPlace` hooks go.
- Header fixes (AF-HDR-*):
  - BankLedger and LootHistory get a header lock plus `/bl lock` and `/lh lock`.
  - Quick Comms pads get settings, lock and close in the pad header. Close hides that pad, which can be restored.
  - WhatGroup gets a header lock plus `/wg lock`, keeping its bottom Close as a deviation.
- Waiver rows (AF-WVR-*):
  - Skin Tester showroom (no lock)
  - Outfitter Reborn outfit window (no lock)
  - Skill Master detached and group windows (no close)
  - PGF Extension filter panel (no close)
- Combat Trail (AF-CT-TEX): every bar takes the active skin's statusbar texture by default.
- Skill Master:
  - AF-SM-RESIZE: a resize grip on the main window, gated by `locked`. The LDB tooltip never resizes.
  - AF-SM-TOMTOM: Set waypoint places a TomTom waypoint when the real TomTom is loaded, and the native pin and
    Skill Master's arrow otherwise.
- Drop Watcher:
  - AF-DW-TIP: tooltips sit flush to the main window, and beside the Rolls companion only when flush would overlap
    it.
  - AF-DW-ROLLHDR: the roll popup companion gets a small "Drop Watcher" header in the main window's header style,
    with no controls.

**M3. Checkpoint CP-1 (AF-SMOKE).** The lead re-gates every touched repo under each client it ships and pushes the
run branches. It also writes `SMOKE.md` and the execution record `99_EXECUTION_RECORD.md`.

**M4. On the owner's go-ahead.**
- `/dev-copilot:finalize`: merge, push the LibKa0s and standard tags, and delete the branches.
- Archive the DpsRace repo (AF-DR-ARCH).
- Rename CombatTrail's and SkillMaster's default branch from `main` to `master` (AF-DEFBR).
- Clean up every branch, stash and worktree the run made.

## Rules for every agent

- Follow the repo's own CLAUDE.md and green gate under each client it ships. Never edit `libs/` or `tests/_kit/`
  except through the re-vendor.
- Commit subjects start with the item id. A test comes first where the behavior is testable headlessly.
- A mid-run question from the owner is the lead's to answer. Note it and carry on.
- No version bumps, no merges, no pushes to master. Subagents never push. The lead pushes run branches at CP-1.
