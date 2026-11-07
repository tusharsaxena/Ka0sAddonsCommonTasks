# Wave 2 smoke: the owner's checks

The checks live in each addon's own `docs/smoke-tests.md`, in its new **WoW Forever** section, and their results go
on those `Result:` lines. This file is the run sheet. Claude marks nothing passed.

## Setup (once)

Link the three checkouts into the Forever client from an elevated Windows prompt, then fully restart it:

```
mklink /d "G:\Games\Blizzard\World of Warcraft\_forever_\Interface\AddOns\PanelMaster" "D:\Profile\Users\Tushar\Documents\GIT\PanelMaster"
mklink /d "G:\Games\Blizzard\World of Warcraft\_forever_\Interface\AddOns\PrettyChat" "D:\Profile\Users\Tushar\Documents\GIT\PrettyChat"
mklink /d "G:\Games\Blizzard\World of Warcraft\_forever_\Interface\AddOns\PartyFrameEnhanced" "D:\Profile\Users\Tushar\Documents\GIT\PartyFrameEnhanced"
```

All three checkouts are on `feat/2026-11-08-forever-port-wave2`, so the Retail client loads the same branch.

## Checks, in the owner's order

| Addon | Checks | What is new to watch |
|---|---|---|
| PanelMaster | FOREVER-1..12 | FOREVER-7: unlocking panels at every strata, BACKGROUND to TOOLTIP, and the Delete popup over a FULLSCREEN panel (the strata guard) |
| PrettyChat | FOREVER-1..14 | FOREVER-3: a group member's two-word name shown whole; FOREVER-9: `/pc test` lists all 79 strings with no "(original not available)" (a miss reopens the one-list decision) |
| PartyFrameEnhanced | FOREVER-1..16 | FOREVER-5..7: both party layouts and Edit Mode on Forever; FOREVER-8 and -10: two-word names, full or cut with an ellipsis, the stand-in's "(test)" mark on the narrow raid-style look |
| All three | A Retail sanity pass: log in, open each panel, no Lua error, and a fresh Retail profile wears Ka0s Default | |

## Results

**Passed**, by the owner on 2026-11-08: "all the checks are done, and all have passed, working beuatifully in
forever". PanelMaster FOREVER-1..12, PrettyChat FOREVER-1..14 and PartyFrameEnhanced FOREVER-1..16 are recorded as
passed on the addons' `Result:` lines (each addon's `W2-SMOKE` commit).

On the way, two Forever-only incidents, neither a defect:

- **PrettyChat's first-run skin picker did not show** on the first Forever login, while PanelMaster's and
  PartyFrameEnhanced's did. Its profile had recorded the picker as seen. The likeliest cause is the library's
  "Apply to all Ka0s addons" button, which by design dismisses every picker still queued behind the one on screen
  and runs its close. PrettyChat loads after the other two, so its picker was queued. `/pc resetall` showed it
  normally, so the picker itself works on Forever.
- **The owner's Retail PanelMaster Default profile was copied to Forever** at the owner's request: 9 panels, all on
  UIParent, LibKa0s media only, neither client setting a custom UI scale. Forever's character key and global
  settings were kept, and the old file was backed up beside it.
