# Execution record

Run 2026-09-30, one session. Branch `feat/2026-09-30-debug-logs-and-resize` in 14 repos, all pushed to
origin with `refs/notes/ka0s-review`. Nothing merged; the LibKa0s tag `v1.64.0` is local only.

## Results

| Item | Repo | Head | Gate (tests passed/failed · luacheck) | Review |
|---|---|---|---|---|
| DL-STD-01 | WowAddonStandards | 19dc25f | docs-only (no gate) | OK, round 3 |
| DL-LIB-01 | LibKa0s | 6db28eb (tag v1.64.0) | 1819/0 (1 skipped) · 0/0 in 127 | OK, round 3 |
| DL-AT-01/02 | AbsorbTracker | 7f4ed1e | 833/0 · 0/0 in 67 | OK, OK r1 |
| DL-AM-01/02 | AuraMaster | d8d52c6 | 1767/0 · 0/0 in 149 | OK, OK r2 |
| DL-BL-01/02 | BankLedger | 7ef7940 | 1167/0 · 0/0 in 82 | OK r2, OK r3 |
| DL-CM-01/02 | ConsumableMaster | a98d3bb | 1146/0 · 0/0 in 128 | OK, OK r2 |
| DL-KC-01/02 | KickCD | 0cb364d | 1228/0 · 0/0 in 113 | OK, round 3 left one moved citation: fixed by the orchestrator (0cb364d), gate re-run, noted OK |
| DL-LH-01/02 | LootHistory | cb5e5d7 | 1003/0 · 0/0 in 74 | OK, OK r3 |
| DL-MM-01/02 | MultiMeters | 75eaa37 | 2125/0 · 0/0 in 145 | OK, OK r2 |
| DL-PM-01/02 | PanelMaster | 751ac73 | 991/0 · 0/0 in 68 | OK, OK r2 |
| DL-PF-01/02 | PartyFrameEnhanced | e971f63 | 406/0 · 0/0 in 76 | OK, OK r2 |
| DL-PC-01/02 | PrettyChat | 1d7cdb5 | 552/0 · 0/0 in 56 | OK, OK r1 |
| DL-WG-01/02 | WhatGroup | 3d0f356 | 869/0 · 0/0 in 58 | OK, OK r1 |

Every addon: lizard shows no touched function above CCN 15. Per-addon detail: `coverage-maps/<Addon>.md`.

## What landed

- **Standard v2.70.0.** debug-logging §8 Diagnosis checklist (state edges, held and flushed work, refusals
  naming the guard, dependencies, caught errors); §9 quiet steady state (a repeating path logs on change
  or once per interval with a count; `(xN)` folding does not count); §1 and performance-§4 describe the
  resizable, session-only windows and forbid saving their size; anti-pattern #91.
- **LibKa0s v1.64.0.** `Core.MakeResizable` (guarded, no floor raise); the console, every CopyWindow and the
  perf panel (width only) resize from a bottom-right grip, with minimums and relayout; the size lives on
  the frame for the session; defaults unchanged. Kit revision 33 (`mock_resize.lua`).
- **Eleven addons.** Re-vendored v1.64.0, cite v2.70.0, smoke rows for resizing; each audited against the
  new §8/§9 with the gaps filled, repeating paths quieted (MultiMeters' Aggregator/Render and tooltip
  lines, ConsumableMaster's per-macro deferral lines, KickCD's list signatures among them), tests pinning
  the lines that matter plus quiet-steady-state tests, and a Coverage section in `docs/debug.md`.

## Residuals (not done; for the owner)

Library gaps several addons hit and could not fix from their side (libs/ is vendored):
1. **LibKa0s-Slash has no debug hook**: its own refusals (disabled gate, unknown verb, validation, profile
   switch in combat) reach chat only. Reported by AuraMaster, BankLedger, KickCD, PanelMaster, PrettyChat,
   WhatGroup, AbsorbTracker.
2. **LibKa0s-DebugLog has no Clear hook**: a console Clear cannot re-arm the hosts' change-gates
   (MultiMeters `NS.DebugSteadyReset`, PanelMaster `NS.DebugOnce`, KickCD's list signatures); turning
   logging off and on does.
3. **LibKa0s-Options combat lock** refuses writes/Defaults/tab switches silently, and its "register parked
   (in combat)" line has no flush line.
4. **LibKa0s-Launcher dependency lines** run at OnEnable while logging is off, so they never land.
5. **LibKa0s-Lifecycle logs no edges** (the hosts now log their own).
6. Several addons grew their own "log once / log on change" helper; whether one belongs in DebugLog is
   the same decision as 2.

Addon-level owner calls:
- MultiMeters: the per-drag `[Window] N moved to …` line is a debug-logging-§10 SHOULD NOT. Drop it, or
  record a deviation?
- AuraMaster: a refused test-mode checkbox still writes its `[Set] state.testMode = true` line after the
  refusal line. Leave, or refuse in the seam (changes the chat text)?
- WhatGroup DIAG-11 expects the console at its default position after /reload; the layout-cache check in
  `IN_GAME_CHECKS.md` decides whether that row needs rewording.
- Small pre-existing stale comment citations (AbsorbTracker tests, ConsumableMaster and PanelMaster
  `.luacheckrc`) left as found.

## To finish (owner go-ahead)

Merge `--no-ff` per repo, standard and LibKa0s first, gate on each merge, push master, push tag
`v1.64.0`, delete the feature branches. Then the in-game checks in `IN_GAME_CHECKS.md`.

## Addenda and finalize (2026-09-30, later the same day)

- **A1** orange Diagnostics link in every console title bar (LibKa0s DebugLog 16); owner saw the AuraMaster
  preview: "Looks good".
- **A2** running diagnostics turns debug logging on for the session (standard v2.71.0 reverses §14's
  flag rule on the owner's decision; LibKa0s DebugLog 17, DebugLogDiagnostics 2, kit revision 34).
- **A3** README uses bullets, never numbered lists, because CurseForge does not render them (standard
  v2.72.0); every README converted, Reporting a bug is the bulleted fixed text in all eleven.
- AuraMaster, outside the DL ids: a new user spell category starts Hide in existing containers (7dfba5a).
- **Finalized** on the owner's go-ahead, in order WowAddonStandards → (LibKa0s | wow-addon) → the eleven addons
  → this repo: doc sync (content only), gate on the branch and on the merge, `--no-ff` merge, push, review notes
  pushed, branches deleted. LibKa0s tag **v1.64.0 pushed**. Master heads: WAS 00b1bed, LibKa0s 4cdaa36,
  wow-addon 3e195b1, AT c6e5acb, AM 9751fec, BL 56a2ba1, CM b64b221, KC 34072c7, LH 15725a1, MM 7dc1cab,
  PM dbc6d82, PF c4bbf0e, PC e10a474, WG 4d53415. Every merge gate green.
- Reported by the doc syncs, not acted on: stale line numbers in some `.luacheckrc` / test comments (BL, LH, WG,
  KC), no `docs/revendor/` bundle for the v1.64.0 re-vendor (KC, PM; that bundle is `/wow-addon:revendor-libka0s`'s),
  and test-only exports (AM, MM, PM, PF).
