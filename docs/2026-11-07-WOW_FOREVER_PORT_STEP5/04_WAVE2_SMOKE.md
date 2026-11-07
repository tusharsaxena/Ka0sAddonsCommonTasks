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

Owed. Record them here as well as on the addons' `Result:` lines once the owner has run them.
