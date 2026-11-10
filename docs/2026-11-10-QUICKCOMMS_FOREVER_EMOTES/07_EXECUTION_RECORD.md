# Execution record

What happened during the run that the frozen plan does not say. Newest last.

- **2026-11-10, ruling R9 (mid-run):** DpsRace is Retail-only. Done as `QFE-DPS` (see `inputs/owner-rulings.md`).
- **v1.95.0 and complexity.** The first release run (at `e4493aa`) found four functions over CCN 15 from
  v1.92.0 / v1.93.0, which were tagged without a release run: Launcher `lib.New` and the kit's `CG.strip`,
  `CG.scan`, `CG.judge`. The lead split them inside v1.95.0 (`ad603eb`: Launcher minor 10, kit revision 54)
  rather than tag over them. The release record is `docs/automated-tests/20261110-090851/` (green, max CCN 15)
  and the local tag was re-cut at `9645d18`. It is still unpushed.
- **Call C7 (the lead's):** Forever seeds the generic Dungeon set with a dungeon-only When (no Mythic+, no
  key level), because otherwise a fresh Forever profile has no dungeon group. `{key}` is hidden on Forever
  along with `{dungeon}`. QuickComms `e0fc176`.
- **Review (`QFE-REV`):** three lenses (client APIs, send path and emotes, quality and docs), 10 findings, all
  confirmed, all fixed. Notable: a Forever dual-spec swap now re-reads the role. Emote commands that the chat
  parser claims first are skipped, so *Shout* sends `/holler`, not the `/shout` alias of `/yell`. Finding 2
  contradicted call C1, and the lead amended C1: an override is never written to `store.last`
  (LibKa0s `97b8ccf`). Notes are on `refs/notes/ka0s-review`, pushed.
- **Owed rulings before the next LibKa0s tag (not this run's):** `LibKa0s/Skin.lua` at 1121 lines is past
  its 1100-line trigger, and `tests/test_launcher.lua` at 1235 is past its 1200-line trigger.
- **For the owner at smoke:** QuickComms Forever profiles that ran schema step 19 before `e0fc176` lack the
  Dungeon set; *Restore built-in groups* brings it back. Skin Tester profiles that never touched *Ignore
  settings panel* now show it ticked.
- `resume-state.sh` counts `QFE-SMOKE` done once the sheet is committed. The smoke itself is owed until
  the owner's results are in `06_SMOKE_TESTS.md`.
- **Finalize, 2026-11-10, on the owner's "merge all changes", before any smoke result was recorded.**
  The owner's smoke in `06_SMOKE_TESTS.md` is still owed. Merged `--no-ff` into master and pushed:
  LibKa0s `4d3e6c3` (tag `v1.95.0` pushed, at `9645d18`), LibKa0sSkinTester `6ac344a`, QuickComms `a9fcab6`,
  DpsRace `1ff5057`, WowAddonStandards `a96a7db`, then this repo. The finalize doc sync added `QFE-FIN`
  commits in LibKa0s (README counts and versions), QuickComms (vendored-version mentions, the
  `char.role.last` line, a stale emote test name) and DpsRace (the test badge).
- **The standard's version moved.** While the run was open, another session released standard v2.105.0
  (single-client addons, the `Forever` Clients value) and v2.106.0 (the suite pins *Ignore settings panel*
  on). The owner chose to renumber: this run's standard release is **v2.107.0**, merged over both.
  Everything above that says "standard v2.105.0" means v2.107.0.
- **Slip, recovered:** during the finalize a mis-chained command deleted this repo's remote feature branch.
  It was pushed back at the same commit (`5ddc3a2`) within the minute. Nothing was lost.
- **Open after the run:** v2.105.0's clients-§7 asks a single-client addon to record its reason in its
  README **and** `docs/ARCHITECTURE.md`. DpsRace recorded it in README, DEPENDENCIES and `docs/scope.md`,
  so its ARCHITECTURE line is owed. QuickComms#15 is left open until the owner's smoke.
