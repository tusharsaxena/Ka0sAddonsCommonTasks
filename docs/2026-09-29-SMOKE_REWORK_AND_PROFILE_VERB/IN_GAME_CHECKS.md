# In-game checks for this run (owner)

Every gameplay change made on 2026-09-29/30, mapped to the exact check in each addon's new
`docs/smoke-tests.md` (branch `feat/2026-09-29-smoke-and-profile`). Run the steps as written there; this
page only says which checks, where, and in what order. Grouped by where you have to be, so one session
per group covers every addon.

Setup once: install every addon from its feature branch. Turn debug on where a check says so
(`/<prefix> debug on`; it switches itself off on every /reload).

## A. Anywhere (city or open world), plus a target dummy for the combat steps

**0. Library version (all addons at once).** `/dump select(2, LibStub:GetLibrary("LibKa0s-Slash-1.0"))`
→ `17`. The collection shares one loaded copy, so one check covers all eleven.

**The `profile` verb.** Make the spare profiles each doc's setup asks for first (usually on the addon's
Profiles page). The combat check is the one marked *(dummy)*.

| Addon | Checks, in order |
|---|---|
| AbsorbTracker `/at` | PROFILE-9, PROFILE-3, PROFILE-4, PROFILE-5, PROFILE-6, PROFILE-7 (key: `use` no longer creates a profile), PROFILE-8, PROFILE-10, PROFILE-12, STATE-3, PROFILE-13, PROFILE-14, PROFILE-11 *(dummy)*, PROFILE-15, SLASH-3 |
| AuraMaster `/am` | PROFILE-5 – 10, PROFILE-11 *(dummy)*, SLASH-2 |
| BankLedger `/bl` | PROFILE-8 – 12, PROFILE-13 *(dummy)*, PANEL-1 |
| ConsumableMaster `/cm` | PROFILE-15 – 20, PROFILE-11, SLASH-14, PROFILE-21 *(dummy)* |
| KickCD `/kcd` | PROFILE-2 (setup), PROFILE-9 – 13, PROFILE-14 *(dummy)* |
| LootHistory `/lh` | PROFILE-7 – 11, PROFILE-13, PROFILE-12 *(dummy)*, SLASH-2 |
| MultiMeters `/mm` | PROFILE-9 – 15, PROFILE-17, STATE-1, SLASH-3, SLASH-4, PROFILE-16 *(dummy)* |
| PanelMaster `/pm` | PROFILE-11 – 15, PROFILE-17, SLASH-2, SLASH-3, PROFILE-16 *(dummy)* |
| PartyFrameEnhanced `/pfe` | PROFILE-2, PROFILE-3, PROFILE-5 – 7, PROFILE-9, PROFILE-8 *(dummy)*; PROFILE-4 in a party (a follower dungeon queue is enough) |
| PrettyChat `/pc` | PROFILE-5 – 9, SLASH-1, PANEL-1, PROFILE-10 *(dummy)* |
| WhatGroup `/wg` | PROFILE-3 – 8, SLASH-1, PANEL-1, PANEL-14, STATE-3, PROFILE-9 *(dummy)* |

**New Profiles pages and profile handling (the four addons that had none).**

| Addon | Checks |
|---|---|
| PrettyChat | PROFILE-1 – 4, PROFILE-6, PROFILE-9, PANEL-2, PANEL-3, DIAG-19 (loot an item to see a formatted chat line) |
| WhatGroup | PROFILE-1, PROFILE-2, PROFILE-4, PROFILE-8, PROFILE-11 – 13, SLASH-2, PROFILE-14 and COMBAT-2 *(dummy)*; PROFILE-10 needs two characters |
| BankLedger | PROFILE-1 – 6, PANEL-2, PANEL-27 – 29, DIAG-19, PROFILE-7 (retention stays account-wide: needs a History row older than 30 days, debug on, no `[Prune]` line) |
| LootHistory | PROFILE-1 – 6, INSTALL-2, PANEL-1, PANEL-19, DIAG-3, DIAG-14, DIAG-15, COMBAT-3 *(dummy)*, PROFILE-4 (retention stays account-wide) |

**AuraMaster `/am redraw`.** SLASH-9, SLASH-10 (debug on), SLASH-11 (the in-combat half on a dummy).

**ConsumableMaster event lines.** COMBAT-17 (debug on): swap main hand → `slot=16`; ring → nothing; spec
change → one line.

**MultiMeters event lines.** DIAG-26 (take a portal), DIAG-27 *(dummy)*, DIAG-28 (join or leave a group),
DIAG-30 (mount, shapeshift, die: no line).

## B. Fresh login (exit the game fully, not /reload)

- **AuraMaster enchant name (SP-AMX-01):** FILT-42. Apply an oil/stone/poison before logging out; after
  login the enchant bar must show the weapon's name. If it is ever blank:
  `/dump C_Item.GetItemName(ItemLocation:CreateFromEquipmentSlot(16))`.

## C. Upgrade from your current install (back up `WTF/` first)

- **BankLedger** settings migrate into the Default profile, history and retention stay account-wide:
  PROFILE-14, INSTALL-8 – 10.
- **LootHistory** the same: INSTALL-4 (before/after the update), INSTALL-5, INSTALL-3, SLASH-7, PANEL-12.

## D. A boss encounter (follower dungeon or LFR)

- **ConsumableMaster:** COMBAT-16 (debug on): `type=1 active=1 rewrite=no` at the pull, `active=0
  rewrite=yes` at the kill, then one `[Macro] … edited` line per macro.
- **AuraMaster:** DIAG-12 (debug on).
- **MultiMeters:** DIAG-29 (debug on).

## E. A Mythic+ key

- **ConsumableMaster (owed from earlier today):** COMBAT-14 and COMBAT-15. `/reload` out of combat between
  pulls, `/cm debug on`, finish the key **without typing any `/cm` command** → the action-bar macro icons
  come back by themselves at the key's end; the log shows `type=2 active=0 rewrite=yes`, `[Macro] marked
  15 macro(s) stale`, and one `[Macro] KCM_… edited` line per macro.
- **AuraMaster:** COMBAT-7 (`/reload` between pulls → every container draws at once; then `/am debug on`,
  `/am diagnostics` → `apply queue: all=false`, every `[Cont]` line `engine=yes`), and DIAG-11 (the event
  trace across pulls, a boss and the key's end).
- **AuraMaster `/am redraw`:** the in-key half of SLASH-11 (bare redraw runs light and says full has to wait).
- **MultiMeters:** DIAG-29 also passes at key start and end.

## F. Optional: library-absent install (rename `libs/LibKa0s` aside, /reload, rename back)

The `profile` verb must print its "unavailable" line and switch nothing: AbsorbTracker DEGRADED-2,
BankLedger DEGRADED-6, ConsumableMaster DEGRADED-5, KickCD DEGRADED-10 and DEGRADED-13, LootHistory
DEGRADED-10, MultiMeters DEGRADED-8, PanelMaster DEGRADED-12 and DEGRADED-14, PrettyChat DEGRADED-9,
WhatGroup DEGRADED-4.

## Known gaps (no check in the docs; quick ad-hoc steps)

- **LootHistory:** switch to a second profile and back → the History window shows the same rows.
- **PrettyChat:** switch to a second profile, `/reload` → that profile is still current and applied.
- **AuraMaster:** a full relog (not `/reload`) mid-key → containers draw at once (COMBAT-7 covers
  `/reload` only).
- **KickCD:** `/kcd help` lists the `profile` row; a `/kcd profile <name>` switch with debug on logs one
  `[Profile] switched` line.

Everything else in each doc's "Pending sign-off" section is a check that was never run or was rewritten
tonight; run those when convenient. The ones above are the ones that verify this run's changes.
