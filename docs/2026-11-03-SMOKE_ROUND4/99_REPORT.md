# Report: the owner's fourth smoke round

Branch `feat/2026-11-01-full-skinning` in 18 repos (LibKa0s, 16 addons, this one; Outfitter untouched). Branches and `refs/notes/ka0s-review` are pushed. Nothing is merged, no tag is pushed, no version is bumped. The smoke list is `06_SMOKE_TESTS.md`; nothing on it is marked passed.

## What shipped

- **M1:** R4-L1, a dropdown list on a Ka0s surface closes on a press outside it (OptionsCombat minor 4). Skin Tester R4-ST1 to R4-ST4: Ignore settings panel off by default here only, the TreeGroup sample keeps its height and shows a page, one IconBorder sample, the showroom band painted once. DpsRace R4-DR1 to R4-DR6: centred blocks, even spacing, *Your best* label, consumables on the card, *Arm Race*, and a sim Racing step. MultiMeters R4-MM1: 10 s sim fight steps. R4-MOCK for the sign-off, then R4-REL and R4-RV.
- **M2:** R4-L2, Ka0s Default's header is option E (#3A2F0A to #1F1905, flat #2C2408), and swatch 2 is the header. R4-L3 adds a new `icon.outline` token for window icon outlines, while `icon.border` is unchanged. R4-SEP removes the line under every window title, in the library and in AbsorbTracker, BankLedger, ConsumableMaster, DpsRace, DropWatcher, KickCD, LootHistory, MultiMeters, PanelMaster, PrettyChat, QuickComms and WhatGroup. R4-ZOOM verified every HUD icon's crop, with fixes in DpsRace, MultiMeters (class fallback icon) and QuickComms. DpsRace R4-DR7 takes the top 3 abilities out of the Your best hover. Then R4-REL2 and R4-RV2.
- **M2b** (`R4_ADDENDUM_HUD_ICON_EDGE.md`): R4-L4 adds `S.IconBorder(frame, { hud = true })`, which draws in `icon.border` and never in `icon.outline` (SkinPaintControls minor 17). R4-HUD passes `hud = true` at the DpsRace HUD spell rows and HUD chart icons, the MultiMeters row unit icons and the PartyFrameEnhanced cast icon, so under Ka0s Default they stay black and windows show the grey outline. Then R4-REL3 and R4-RV3.
- **M3:** R4-GATE. The Skin Tester also gets PANEL-17 and PANEL-18, the in-client steps for R4-L1 (commit `R4-L1:` there), because LibKa0s has no smoke file.

## The lead's calls

- From 00_PLAN.md: dropdowns close only on Ka0s surfaces, with no Escape key (1). The "item 3" element is the tester's own TreeGroup sample (2). Ignore settings panel defaults off in the tester only, with no migration (3). DpsRace block contents are centred (4). Consumables appear as 12 px icons with xN (5). The DpsRace Racing step runs about 3x fast, so about 10 s (6). MultiMeters sim steps are about 10 s each (7). The header and the icon borders went to the owner (8).
- The R4_SIGNOFF.md scope call (one token, `icon.border`) was **superseded by the owner's answer**: the HUD keeps black edges. That is mockup option 2, the new `icon.outline` for windows. The M2 review found that HUD icons edged through `S.IconBorder` had turned grey, so the lead added M2b (`hud = true`) to follow the owner's answer. No new owner decision was needed.

## Totals (this gate, fresh, one repo at a time through ka0s-bounded)

- LibKa0s: 3986 passed, 0 failed, 3 skipped (3989). Lint 0/0 in 292 files. The release battery is `docs/automated-tests/20261103-160531/`: max CCN 15, 0 over, perf not measured.
- 16 addons: 22554 passed, 0 failed, 16 skipped. luacheck reports 0 warnings / 0 errors in every repo. No Lua file is over the 1500-line cap, except PrettyChat's `GlobalStrings/GlobalStrings.lua`, which is exempt by rule (generated, non-shipping). Largest suite: MultiMeters 2550. Smallest: PremadeGroupsFilterExtension 518.
- Across the 17 code repos: 26540 passed, 0 failed.

## Tag

The local tag v1.85.0 is at **2a78817** (R4-REL3, the fifteenth re-cut). That is LibKa0s HEAD, and the tree is clean. The tag is not pushed.

## DpsRace SavedVariables cleanup (R4_ADDENDUM_DR_SV_CLEANUP.md)

**DONE 2026-11-03 15:22**, by a lead subagent, with the owner logged out and approving. The race records went from 79 to 32. The 47 dropped were 33 schema 1 records (no consumables, talents or timeline) and 14 schema 2 records (no consumables or timeline). One unused gear loadout was swept. Bests are computed at runtime, so no index needed fixing. The backup is `DpsRace.lua.bak-20261103-152208`, next to the file. Logged as `R4-SVCLEAN` in `checkpoints.tsv`.

Observed at this gate, for the lead: the SavedVariables folder also holds `DpsRace.lua.bak-20261103-164909`, and `DpsRace.lua` was last written at 16:49. This gate did not open or touch either file.

## Open items

- **Owner question:** should the 9 schema 3 records also be dropped? They have all three captures but no gear stats.
- **Owed by you:** the smoke run in `06_SMOKE_TESTS.md`, then the go-ahead. After that come `/dev-copilot:finalize`, the push of tag v1.85.0, and closing LibKa0s #71 and #72, spaced apart (#70 stays open). Then the cleanup of branches, stashes and worktrees.
- `exceptions.tsv` needs no row: every M2 and M2b id landed a commit.
