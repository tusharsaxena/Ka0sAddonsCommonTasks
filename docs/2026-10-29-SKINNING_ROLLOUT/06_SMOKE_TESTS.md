# Smoke tests: the skinning rollout

The owner runs these in the client. Each addon's checks live in its own `docs/smoke-tests.md` (the Skins
section, listed under Pending sign-off), and the results are recorded there. This file is the index and
the running order. Nothing here is marked passed by the run. The owner reported every check passed on 2026-10-30.

## Before you start

- The game loads every addon from its `GIT/<Addon>` checkout, so each repo is already on
  `feat/2026-10-29-skinning-rollout`, and LibKa0s is v1.80.0 everywhere.
- The first login shows each addon's first-run skin picker, on every profile (O3). That first login is
  itself the picker check.
- The O2 reset runs once per profile at that login: HUD faces and border styles go back to "From skin".
  Note your HUD faces and borders **before** you update, so you can see what moved.

## Cross-cutting checks (run once)

| Id | Check | Result |
|---|---|---|
| RO-1 | Log in: each addon's picker appears once (not in combat). Apply on one profile, then switch to a second profile: its picker appears too | Passed (owner, 2026-10-30) |
| RO-2 | Under Ka0s Default, every addon looks as before except the changes its SKIN-1..3 lists (mostly Oxanium faces and title bands; report §Owner calls 3–4) | Passed (owner, 2026-10-30) |
| RO-3 | Switch skins live in one addon's Skin tab: only that addon repaints; `/reload` keeps it | Passed (owner, 2026-10-30) |
| RO-4 | EllesmereUI on, with the source set to EllesmereUI: every addon follows it; off, they fall back to their stored skin | Passed (owner, 2026-10-30) |
| RO-5 | Ignore settings panel on (the default): the settings pages stay stock, the windows and HUD still follow the skin | Passed (owner, 2026-10-30) |
| RO-6 | Disable then re-enable an addon (stand-down): no picker, timer or frame left behind; the picker comes back on the next login if not yet seen | Passed (owner, 2026-10-30) |

## Per addon

| Addon | Checks | Owner calls to settle there (99_REPORT.md) | Result |
|---|---|---|---|
| AbsorbTracker | SKIN-1..26 | Ignore fonts on the HUD (worked around); HUD face under the other skins (SKIN-5) | Passed (owner, 2026-10-30) |
| AuraMaster | SKIN-1..24 | Ignore fonts on the HUD (SKIN-10); dropdowns now library-painted | Passed (owner, 2026-10-30) |
| BankLedger | SKIN-1..26 | Close control under Ka0s Default; Oxanium labels | Passed (owner, 2026-10-30) |
| ConsumableMaster | SKIN-1..23 | Buttons' 2 px icon-family edge (SKIN-1); KCM rows in Oxanium (SKIN-7) | Passed (owner, 2026-10-30) |
| DpsRace | SM-DR-SK1..24 | Modal title band; square checkboxes; Oxanium labels | Passed (owner, 2026-10-30) |
| DropWatcher | SKIN-1..24 | Title band D3 (SKIN-2); library scroll bars; icon border reset (SKIN-3) | Passed (owner, 2026-10-30) |
| KickCD | SKIN-1..29 | **Cast-bar border gone under every skin (SKIN-1, SKIN-6)**; icon border thickness; Ignore fonts (SKIN-14) | Passed (owner, 2026-10-30) |
| MultiMeters | SKIN-1..24 | Window chrome stays the player's (SKIN-4); export modal in Oxanium (SKIN-2) | Passed (owner, 2026-10-30) |
| PanelMaster | SKIN-1..20 | Unlock label in Oxanium; PANEL-1 amended | Passed (owner, 2026-10-30) |
| PartyFrameEnhanced | SKIN-1..25 | Holder caption face; no cast-icon edge | Passed (owner, 2026-10-30) |
| PremadeGroupsFilterExtension | SKIN-11..32 | The EllesmereUI bridge is retired: the stored EUI choice carries over; the metal panel is unchanged (SKIN-11) | Passed (owner, 2026-10-30) |
| PrettyChat | SKIN-1..17 | X11 TreeGroup flat edge; the notes follow the Scope (SKIN-6) | Passed (owner, 2026-10-30) |
| QuickComms | SKIN-1..23 | Icon border 1→2 px (SKIN-1); Preview title in Oxanium, browser texts keep Blizzard's font (SKIN-3); pad inner line per skin; popup and browser under EllesmereUI | Passed (owner, 2026-10-30) |
| WhatGroup | SKIN-1..24 | Flat Close button (D4); title band | Passed (owner, 2026-10-30) |
