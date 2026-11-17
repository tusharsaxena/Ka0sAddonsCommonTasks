# Wave B smoke sheet (#86 header buttons)

The owner runs these in game and records **PASS**, **FAIL** (with a note) or **N/A**. The run never marks a check
passed by itself. Each id is written out in full in that addon's `docs/smoke-tests.md`. Run each check on Retail,
and on WoW Forever too where the addon ships there (**R·F**). Skill Master ships on Forever only.

**What to look for everywhere:**
- **Order:** every window the addon builds reads, left to right, its own marks, then a **settings gear**, then the
  **X**. The marks are one size, evenly spaced and right-aligned in the corner.
- **Hover:** each mark is gray at rest and turns the link color on hover; the X turns red. Each has a tooltip
  above it.
- **The gear:** it opens this addon's settings. A window that would cover the settings panel closes first.
- **A drag strip:** it shows the gear left of its X. Clicking the gear opens the settings and changes no setting.
  Dragging by it still moves the frame.

| Addon | Checks | What changed | Result |
|---|---|---|---|
| Absorb Tracker (R·F) | BAR-23, BAR-21 | The gear on each bar's drag strip; it stays clickable after raising an overlapped bar (LibKa0s#96 watch) | |
| Aura Master (R·F) | CONT-29, PRESETS-45 | Preset picker: settings · close; container drag strips get the gear | |
| Bank Ledger | LEDG-66, LEDG-67, SESS-17 | Ledger, session and export windows: settings · close | |
| Combat Trail (R·F) | SM-CT-H17, SM-CT-R27, SM-CT-T12, SM-CT-T13, SM-CT-T14, SM-CT-RM95, SM-CT-RM49, SM-CT-RM67 | All six windows; the HUD reads Results, Race, Lock, Settings, Close | |
| Consumable Master (R·F) | BAR-40, BAR-10, BAR-38, SKIN-4 | The gear on the macro bar's drag strip | |
| Dps Race | SM-DR-AD86HUD, SM-DR-AD86RES, SM-DR-AD86TL, SM-DR-AD86GV, SM-DR-AD86SK, H6 | All four windows; the HUD reads Results, lock, settings, close | |
| Drop Watcher (R·F) | FEED-108 | Every window's marks with settings | |
| Kick CD | GRID-23, CAST-20, SKIN-46, SKIN-47 | The gear on the icon grid and cast bar drag strips | |
| Skin Tester (R·F) | SHOW-54, SHOW-50 | Showroom: settings · close | |
| Loot History | HIST-47, HIST-48, HIST-22 | History and export windows: settings · close | |
| Multi Meters | WIN-60, EXPORT-57, WIN-1 | Meter header: export, reset, segment, lock, minimize, settings, close (the gear moved next to the X); export modal | |
| Outfitter Reborn (R·F) | HB1, HB2, HB3, SK7 | Outfit window: gear, X; outfit bar: lock, gear, X; dialogs: X only | |
| PGF Extension | SKIN-57, SKIN-38, SKIN-40, SKIN-55 | The panel reads chevron, gear (no X) | |
| Quick Comms (R·F) | PREVIEW-13, PAD-18, PAD-19, EDIT-35 | Preview window, Comms Pad header and the edit modal on the strip | |
| Skill Master (F) | SM-TEST-8, SM-TEST-9, SM-TEST-10, SM-TEST-11, SM-DISP-12 | Main window, Journal, trainer popup and detached bands | |
| What Group | POPUP-13 | The group popup gains a gear and an X on its title bar (it had only the footer Close) | |

Panel Master, Party Frame Enhanced and Pretty Chat own no window with title marks and no drag strip (not
applicable; see `plan-data/exceptions.tsv`).
