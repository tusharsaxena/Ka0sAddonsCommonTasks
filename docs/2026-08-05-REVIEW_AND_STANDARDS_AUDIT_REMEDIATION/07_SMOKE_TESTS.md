# 07 — Smoke Tests

**The minimal in-game pass for the work on `feat/2026-08-05-audit-review-remediation`.**

Nothing in this session was verified against a client. Everything below is unperformed. Out-of-game suites
(lint, harness, perf, complexity) are green in all nine repos and are not repeated here — these steps cover
only what a suite structurally cannot reach: rendering, taint, the Blizzard options list, SavedVariables
migration on a real profile, and chat output.

**Budget: about 25 minutes for the whole collection.** Section A is the highest-value half — if you stop
after it, you will have covered every changed data path and every changed options lifecycle.

---

## A — Do these first. They cover the two riskiest changes in the session.

### A1 · SavedVariables migration (AbsorbTracker, PanelMaster)

Two `schemaVersion` defaults changed so that a migration ladder that was previously unreachable now runs.
This is the only work in the session that can touch existing user data.

1. **Back up your `WTF/` folder.** Not optional — this is the one step here that can lose settings.
2. Log in with your **existing** AbsorbTracker and PanelMaster settings.
3. Confirm your bars, panels, positions, colors and profile selection are exactly as you left them.
4. `/reload`, confirm again.

**Red flags:** settings reset to defaults, a panel back at its default position, a profile switched.

### A2 · Degraded install (all 8)

Five items changed what happens when `libs/LibKa0s/` is absent. This path is invisible in normal play and
is where the session's High-severity fixes live.

1. Rename `Interface/AddOns/<Addon>/libs/LibKa0s` to `libs/LibKa0s.bak` for **one** addon at a time.
2. `/reload`.
3. The addon must **load without a Lua error**, and its slash help must print.
4. Spot-check the verbs below, then restore the folder.

| Addon | Command | Expected |
|---|---|---|
| ConsumableMaster | `/cm config`, `/cm version`, `/cm bar`, `/cm list` | every host verb dispatches; only `/cm list` prints the unavailable line |
| PanelMaster | `/pm panel audit`, `/pm debug` | audit returns a result, not an error; `/pm debug` prints an acknowledgment |
| KickCD | `/kcd debug` | prints an acknowledgment |
| the rest | `/at`, `/bl`, `/lh`, `/pc`, `/wg` | help prints, no error |

**Red flags:** `attempt to call field` or `attempt to index` in chat; a verb silently doing nothing;
`/cm` falling back to help for a host-owned verb.

### A3 · Options list and settings pages (all 8)

The options lifecycle was rewired in four addons and the shared Options seam was re-vendored into all eight.

1. Open Blizzard Settings → AddOns.
2. Each of the eight appears **once**. **KickCD's six pages appear once each** — not duplicated.
3. Open every page of every addon. Each renders; no page is blank; no Lua error.
4. Change one setting per addon, `/reload`, confirm it stuck.

**Red flags:** a duplicated entry, a blank page, a page that errors on second open.

---

## B — Per addon. One to three steps each.

### AbsorbTracker · `/at`
1. **Preview honors its duration** — `/at test`, wait past the announced seconds. The bar restores on its
   own, with **no** `/at update`.
2. **Unlock shows a placeholder fill; re-lock returns to live data.**
3. **Per-unit repaint** — disable the player bar, enable the target bar, toggle show-only-in-combat.
   The **target** bar repaints.

### BankLedger · `/bl`
1. **Tagged output** — save a view, then reset it. Both chat lines carry the **`[BL]`** prefix.
2. **Window edge unchanged** — open the ledger and the session window. Border, background, inner border and
   title color look exactly as before.
3. **Defaults tooltip is honest** — hover the Defaults button; the tooltip says it also resets both windows'
   geometry, and pressing it does that.

### ConsumableMaster · `/cm`
1. **No panel moved a pixel** — open each settings page and compare against a screenshot from before the
   branch, or against your memory of it. Header, divider and button-pair positions are unchanged.
2. **`/cm bar` updates live** — with the settings page open, run `/cm bar`. The checkbox updates **without
   the page rebuilding**.

### KickCD · `/kcd`
1. **Spell-name color** — set Spell-name color to red. The cast bar's spell name renders **red**.
   (It read a keyed color by index before, so any non-white value was wrong.)
2. **Six pages, once each** — covered by A3; confirm here if you skipped it.
3. Cast something interruptible and confirm the icon grid and cast bar behave normally — the perf brackets
   and the profile defaults both moved.

### LootHistory · `/lh`
1. **Filters see a live blacklist** — with the settings window **closed**, blacklist an item from the History
   right-click menu. Then open Filters. The new entry is **present without a `/reload`**.
2. **Price cascade** — `/lh set` a non-default price key, then do a price lookup. You get that provider's
   value **without opening the AH Price page**.
3. **Reset All is honest** — the Panel button's label matches what it actually resets.

### PanelMaster · `/pm`
1. **`/pm config` answers repeatedly** — run it three times in a row. It opens the panel every time, not
   just the first.
2. **Canvas behaves** — unlock, move a panel, re-lock, `/reload`. Position holds.
3. Covered by A1 — confirm the v1→v2 migration left your panels intact.

### prettychat · `/pc`
1. **Reputation lines render clean** — lose reputation with any faction. The line shows the faction name with
   **no stray number and no `%d` artifact**.
2. **Guardian XP line** — gain guardian experience (any pet/guardian kill credit). The line shows the **name
   followed by the amount**, not the amount alone.
3. **Original box matches source** — open the settings panel; for a few rows, the Original box matches what
   `/pc test` prints.
4. **Load time** — the `GlobalStrings` dump was reduced or lazy-loaded. Confirm login is not slower and every
   panel row still displays its text.

### WhatGroup · `/wg`
1. **Disabled means silent** — disable via `/wg`, then accept an invite from a group-finder application.
   **No notify, no popup.**
2. **Options list after combat** — `/reload` while in combat, then open Settings. WhatGroup is in the list.
3. **Teleport button fires once** — press it once; it teleports once, with **no chat error**.

---

## If a step fails

Note the addon, the step, and the exact chat text. The out-of-game suites are green, so a failure here is
almost certainly one of:

- **A rendering or lifecycle regression** from the options rewiring (`M4-01`, `M3-04`, `M3-13`) — most likely
  in ConsumableMaster, KickCD, PanelMaster or WhatGroup.
- **A defaults relocation** (`M4-02`, moved `defaults/Profile.lua` in ConsumableMaster, KickCD, LootHistory)
  showing up as a setting that will not persist.
- **A migration** (`M4-18`, `M4-22`) showing up as a reset. This is why A1 says back up `WTF/` first.

Each of those maps to a single commit on the branch; `git log --oneline` in the addon's repo, matched on the
`[ITEM-ID]` in the commit subject, isolates it.
