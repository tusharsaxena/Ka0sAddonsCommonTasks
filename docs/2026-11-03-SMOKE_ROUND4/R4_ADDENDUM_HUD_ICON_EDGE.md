# Addendum: HUD icons drawn through S.IconBorder keep icon.border (lead, 2026-11-03)

M2 (wf_9dce3497-b7b) stopped before the gate. The independent reviews of DpsRace and PartyFrameEnhanced found that
R4-L3 breaks the owner's scope answer ("I prefer the HUD icons to keep black edges", R4_SIGNOFF.md). `drawIconEdge`
reads `icon.outline` first for every `S.IconBorder` caller, and some HUD icons are edged through `S.IconBorder`. So
under Ka0s Default those edges turn grey #4D4D57 instead of staying black, and they change in Glass, Ember, WoW Midnight
and WoW Forever as well.

Lead's call (follows the sign-off, needs no new owner decision):

- **R4-L4 (LibKa0s):** `S.IconBorder(frame, { hud = true, ... })` draws the edge in `icon.border` (the HUD token,
  unchanged by R4-L3) and never reads `icon.outline`. Without `hud`, behaviour is unchanged (window outline). Pin both
  with tests, plus a test that `hud` survives replay and skin flips. Document it in docs/api and in releasing.md's
  hosts-owe note.
- **R4-REL3:** re-cut local v1.85.0 (never pushed).
- **R4-RV3:** re-vendor all 16 addons (never Outfitter).
- **R4-HUD (hosts):** pass `hud = true` at the HUD sites. Window sites keep the outline:
  - DpsRace: the race HUD's spell rows (`Hud_Breakdown.lua:81` through `Style.IconEdge`, which gains a hud flag) and
    the HUD chart's cooldown icons (`Hud_Chart.lua:698`). The Results, Compare and Timeline windows keep the outline.
  - MultiMeters: the meter row unit icons (`Row_NameCell.lua:139`), since the meter is the in-combat HUD
    (INVESTIGATION.md).
  - PartyFrameEnhanced: the party cast bar's spell icon (`Element.lua:78`).
  - WhatGroup's teleport icon is in a window and keeps the outline.

  Each host's docs and smoke rows name black under Ka0s Default for those edges, with a test that fails on the outline
  colour.
