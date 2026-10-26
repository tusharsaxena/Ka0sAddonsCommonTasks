# Bounded lint: execution record (2026-10-26)

All four items landed on `feat/2026-10-26-bounded-lint`. Every repo branched from its `master`, and
none of them is merged.

## Heads

| Repo | Item | Head |
|---|---|---|
| dev-copilot | BL-01 | `02a7d4f` |
| WowAddonStandards | BL-02 | `d31c270` |
| AbsorbTracker | BL-03 | `616b511` |
| AuraMaster | BL-03 | `899aca1` |
| BankLedger | BL-03 | `e271901` |
| ConsumableMaster | BL-03 | `7ad457a` |
| DpsRace | BL-03 | `861ef57` |
| DropWatcher | BL-03 | `02ab02c` |
| KickCD | BL-03 | `31ec0e4` |
| LootHistory | BL-03 | `6a61359` |
| MultiMeters | BL-03 | `a881191` |
| PanelMaster | BL-03 | `881c324` |
| PartyFrameEnhanced | BL-03 | `659fe76` |
| PremadeGroupsFilterExtension | BL-03 | `9d31ffc` |
| PrettyChat | BL-03 | `83dd40f` |
| QuickComms | BL-03 | `ef9adec` |
| WhatGroup | BL-03 | `79f1d6d` |
| LibKa0s | BL-03 | `0b25de9` |
| Ka0sAddonsCommonTasks | BL-04 | the commit that adds this file |

## Evidence

- **dev-copilot:** `python3 scripts/test_bounded_runs.py` passes 27 of 27, `check_overlays.py` reports
  `OK: 13 overlays`, and both manifests parse. Replaying the owner's command
  (`cd …/QuickComms; lua tests/run.lua 2>&1 | tail -3; luacheck . 2>&1 | tail -1`) through the matcher is
  still refused, and the refusal now reads
  ``Run it through the bounded runner instead: `/home/tushar/.claude/dev-copilot/bin/ka0s-bounded luacheck .` ``.
- **Every addon and LibKa0s:** the gate ran in each worktree as the new `CLAUDE.md` states it, through
  the runner. Lint was 0 warnings and 0 errors in all 16 repos. The suite was green in 15. LootHistory
  has 1 failure, `TestData: the sample rollup books a holder move's loss and gain on each holder`, and it
  also fails on an untouched `master` worktree (1725 passed, 1 failed, 3 skipped). It is not this change.
- **The first gate run failed the kit's `eol` case in all 16 repos.** The edit rewrote `CLAUDE.md` with bare
  LF in repos that pin it CRLF. Checking each file out from the index again (`rm CLAUDE.md && git checkout --
  CLAUDE.md`) fixed it before the commit, and the rerun above is the one that counts.

## Merge notes

- **The plugin change takes effect only after a merge.** The installed copy is
  `~/.claude/plugins/cache/dev-copilot/dev-copilot/2.6.0`, so after dev-copilot merges, run
  `/plugin marketplace update` and then `/reload-plugins`.
- **The gate-line change works today.** It uses the runner that 2.6.0 already installs, so it does not wait
  on the plugin.
- **WowAddonStandards, LibKa0s, LootHistory and this repo also carry `feat/2026-10-25-skinning`.** None of
  BL-02, BL-03 or BL-04 overlaps the skinning diff's hunks. BL-02 deliberately leaves the version alone, so
  it does not collide with skinning's v2.89.0 changelog move.
