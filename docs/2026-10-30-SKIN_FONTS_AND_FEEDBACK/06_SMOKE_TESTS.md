# Smoke tests: skin fonts and feedback (LibKa0s v1.82.0)

The owner runs these checks in the client. Each repo keeps its own checks in `docs/smoke-tests.md`, listed under
Pending sign-off, and the owner records the results there. This file gives the index and the order to run them in.
The run marks nothing here as passed.

## Before you start

- The game loads every addon from its `GIT/<Addon>` checkout. All 15 addons, LibKa0sSkinTester and LibKa0s are on
  `feat/2026-10-30-skin-fonts-feedback`, so every addon carries LibKa0s v1.82.0.
- **Restart the client fully** once, not just `/reload`: new font files register only at start. Then `/reload` once
  with every addon on.
- **The Fira Sans Medium caveat.** Your SharedMedia_MyMedia registers "Ka0s Fira Sans Medium" as build 4.301;
  LibKa0s ships 4.203 under the same key, and whichever registers first is drawn. The widths were measured on 4.203.
  Before a WoW Forever width result counts, run
  `/dump LibStub("LibSharedMedia-3.0"):Fetch("font", "Ka0s Fira Sans Medium")`: the path should end in
  `libs\LibKa0s\media\fonts\FiraSans-Medium.ttf`. If it points into SharedMedia_MyMedia, disable that addon (or its
  Fira entry) for the WoW Forever checks. Ka0s Prototype and Ka0s Expressway are the same bytes as your pack copies,
  so they need no check.
- On your client `Fonts/FRIZQT__.TTF` is Prototype, so WoW Default looks like Ka0s Default. That is expected
  (LibKa0s#69).
- Start with the Skin Tester. It shows every skin's faces, the Font outline and the width ratios on one screen.

## Cross-cutting checks (run once)

| Id | Check | Ruling | Result |
|---|---|---|---|
| FX-1 | Client restart, then `/reload` with every addon on: no Lua error | LK-A2, every XX-01 | |
| FX-2 | **The three new faces, per skin.** Ka0s Default draws Prototype for body, titles and HUD. Obsidian draws Expressway for all three. WoW Forever draws Fira Sans Medium for body and Fira Sans SemiBold for titles and HUD. The other skins keep their faces. **Judge Prototype's legibility outlined on the HUD** | owner items 2-4, D-02, LK-A1 | |
| FX-3 | The removed faces are gone: no Ka0s Inter, Ka0s Inter SemiBold, Ka0s Oxanium SemiBold or Bold, or Ka0s Fira Sans (Regular) in any font dropdown, unless another addon of yours registers them | item 7, D-03 | |
| FX-4 | **Width parity.** Open one LootHistory window and switch through all nine skins (compare image-17): no skin truncates text that Ka0s Default fits. Then `/st widths`: Ka0s Default reads 1.000x on all three roles, the others close to it (the measured worst are Azeroth and Glass titles at about 0.96x and Obsidian's HUD at about 1.01x). **Judge how close is close enough** | item 5, D-08, LK-05 | |
| FX-5 | **Font outline.** General > Skin > *Font outline* reads *All text* on a new profile: window and HUD text are outlined. *HUD text only*: window text loses the outline live, HUD text keeps it. *Off*: no outline anywhere. The mono role (JetBrains Mono: debug console, race clocks) is never outlined. Tick *Ignore fonts*: the dropdown greys out and Ignore fonts wins. Choose *All text* again afterwards | item 13, D-06, LK-03 | |
| FX-6 | **From skin flags.** In an addon with font settings (AuraMaster, KickCD, MultiMeters, DpsRace, QuickComms, PFE, ConsumableMaster, AbsorbTracker, DropWatcher's Tables), *Font flags* lists *From skin* first and a block you never changed shows it. **A flag you picked by hand before the update (for example Thick outline or None) is still picked** after the upgrade and after `/reload`. A block you had on plain *Outline* now shows From skin and looks the same under All text | D-07, Addendum 01, every XX-01 | |
| FX-7 | **HUD size scale.** With a HUD block on *Use the skin's font* at size 24, switch Ka0s Default to Obsidian: it draws a little larger (26) and about as wide; Glass draws 22. `/xx get` on the size still prints 24. A block on its own face, or under Ignore fonts, keeps its stored size | item 5, D-09, LK-06 | |
| FX-8 | **Overrides reset on a skin change.** Pick a Font and a Texture override, then another skin on the Skin tab: both go back to *Skin's own*. In the picker (`/xx skin`) a preview clears them, the close mark restores them, Apply saves the cleared pair. Apply to all clears them in every addon whose skin changes. Re-picking the same skin keeps them (image-06) | item 1, D-10, LK-07 | |
| FX-9 | **Skin tab layout.** *Reset font* and *Reset texture* sit side by side under the dropdowns, each greyed while its half is the skin's own, and each clears only its half. The Scope boxes are half width and line up with the dropdowns above. *Copy to every Ka0s addon* has its own heading, *Other Ka0s addons*. The description line is in the Look section (image-29, image-30) | item 6, D-11, LK-08 | |
| FX-10 | **`/xx skin` in every addon**: `/at`, `/am`, `/bl`, `/cm`, `/dr`, `/dw`, `/kcd`, `/lh`, `/mm`, `/pm`, `/pfe`, `/pgfe`, `/pc`, `/qc`, `/st`, `/wg`. Each opens the *Choose a skin* picker even on a profile that has seen it; *help* lists `skin` right after `config`; refused with one line while the addon is disabled; one grey line per press in combat | item 12, D-16, LK-11 | |
| FX-11 | **Anchor titles not cut off.** Unlock each addon's drag strips (AbsorbTracker, AuraMaster, ConsumableMaster, KickCD, QuickComms, PFE, the Skin Tester) and switch through the skins: every title fits, with no ellipsis or clipped letter. Repeat once **right after a fresh `/reload`** in a non-default skin (KickCD's Focus and Target strips first): the OnShow re-fit was left out (LK-09 review F2). The full per-addon sweep is LibKa0s#68 | item 11, D-12, LK-09 | |
| FX-12 | **Characters.** LootHistory's footer reads `Database ~1.6 MB` (image-19) and its History panel `Database size: ~`; BankLedger the same. LootHistory's Transfer glyph is `↔`. No box where a character should be, in any skin | item 5b, D-19, LH-02, BL-02 | |
| FX-13 | **Arm Race.** DpsRace's idle *Arm Race* button reads as enabled in every skin (image-55..57), also after combat disables and re-enables it, and after a skin switch made while it was disabled. Other primary buttons and close marks look normal | item 16, LK-14, DR-02 | |
| FX-14 | **No floating sim marker.** `/kcd sim start pull`: no "Simulation: ..." strip floats over the grids (image-46); the step panel stays up as the sign. AuraMaster's test mode draws no "TEST" beside containers (image-35) | items 9, 11; D-13, D-14 | |

## Skin Tester (start here)

| Checks | What | Result |
|---|---|---|
| SLASH-5, SLASH-6 (new) | `/st skin`; `/st widths` prints nine lines of ratios against Ka0s Default | |
| PANEL-12 (new) | The Font outline dropdown and the showroom's mode line, live, surviving `/reload` | |
| SHOW-26, SHOW-27 (new) | The *Faces and widths* section (each skin's faces and width ratio); the FontFlags and HudFontSize values | |
| SHOW-13, 19, 20, 21, 23, 24 (re-opened) | Ka0s Default's face is now Prototype; every skin's HUD face (Obsidian Expressway); Ignore fonts on the HUD; library widgets; tool windows; the picker button now goes through `/st skin`'s route | |

## Per addon

The checks this run added or re-opened in each repo's `docs/smoke-tests.md`, all with an empty Result there.

| Addon | Checks added or re-opened | What to look at | Result |
|---|---|---|---|
| AbsorbTracker | New SKIN-27..32. Re-opened INSTALL-2, SLASH-3, SKIN-1..5, SKIN-9, SKIN-26, MIGRATE-2 | Outline, From skin flags, `/at skin`, strip and window widths, HUD size scale on the value text, the new faces; schema v7 | |
| AuraMaster | New SKIN-26..32. Re-opened CONT-27, SKIN-4, SKIN-25 | **Your Ka0s Kait Text containers get their own face and the old glow back, red text included (SKIN-31, v15; image-36/37)**; no TEST marker (CONT-27); stacked Text with Size to fit scales (SKIN-30); strips re-fit after a skin switch (SKIN-32). SKIN-4's Result line holds only a re-open note | |
| BankLedger | New SLASH-11, SKIN-27..31. Re-opened PANEL-8, SKIN-1, SKIN-2, SKIN-8, SKIN-9, SKIN-15 | `/bl skin`; outline; widths; the `~` footer and History readout, no ▼▲ in the Direction tooltip (SKIN-30); override reset (SKIN-31) | |
| ConsumableMaster | New SKIN-24..29. Re-opened INSTALL-4, INSTALL-5, BAR-13, SKIN-1, SKIN-3, SKIN-4, SKIN-9, SKIN-10 | Label flags From skin and the v5 step (stamps read 5); label and stack count scale; override reset | |
| DpsRace | New SM-DR-SF1..SF10 (section 28) | Outline incl. Results text under HUD text only, clocks never outlined (SF1); From skin on the five font blocks (SF2); `/dr skin`; widths; HUD scale; **Arm Race (SF6)**; **the toast 25% larger with icons (SF7)**; **full spell tooltips beside the window, mid and post race (SF8, report a mid-race name-only tooltip)**; breakdown tooltips beside the window (SF9); the two-column Difference (SF10). UT14, W5b, CP1 and CP4 were reworded to point at these | |
| DropWatcher | New SIT-6, TOAST-8, GLOW-12, GLOW-13, SKIN-25..30 | Loot rule column fits (SIT-6, image-38); toast 90 px like DpsRace's (TOAST-8); Proc defaults and colors (GLOW-12); only the picked styles' sections show, Offset stays (GLOW-13); **the Tables font block, its color on plain text only (SKIN-30)**; **the new Situations defaults, image-64 (SIT-7)**; **no Offer, no Post my tradeables while you are the only player: solo, a delve with Brann, a follower dungeon; it comes back when a player joins (ASK-13, image-66)** | |
| KickCD | New SIM-13, SKIN-30..36. Re-opened SIM-12, SKIN-1, SKIN-2, SKIN-6, SKIN-9, SKIN-11 | No strip over the grids, the step panel stays up and closes after a stop (SIM-13); the flags step keeps your picks (SKIN-32); **your own HUD fonts come back (SKIN-36)**; strip and window widths (SKIN-35). LAYER-7 is retired with the strip, no run owed | |
| LootHistory | New SLASH-10, PANEL-25, SKIN-40..42. Re-opened SLASH-2, PANEL-10, HIST-8, LED-11, LED-P2-17 | `/lh skin`; Skin tab; **width parity against image-17 (SKIN-40)**; Insights cards follow the outline live (SKIN-41); no boxes, `~` footer, `↔` Transfer (SKIN-42, HIST-8) | |
| MultiMeters | New INSTALL-17, SLASH-33, SKIN-25..27. Re-opened INSTALL-3, INSTALL-12..16, WIN-49, DEGRADED-11, SKIN-1..4, SKIN-7, SKIN-8, SKIN-24 | The v22 upgrade (INSTALL-17); `/mm skin`; outline (**does the title count as HUD text under HUD text only? SKIN-25**); From skin; meter window width parity | |
| PanelMaster | New SKIN-21..26 | Outline; no font settings of its own; `/pm skin`; the new faces; widths; override reset and the Skin tab layout | |
| PartyFrameEnhanced | New SLASH-7, SKIN-26..29. Re-opened INSTALL-4, SLASH-1, SKIN-1, SKIN-3, SKIN-4, SKIN-6, SKIN-8, SKIN-9, SKIN-24 | `/pfe skin`; outline; From skin; HUD and window widths; schema v3 | |
| PremadeGroupsFilterExtension | New SLASH-4, SKIN-34..38 | **The collapse button is a chevron on the title band in every skin, including Glass and WoW Default (SKIN-38, image-33/34, 48..51)**; outline; the new faces; panel width | |
| PrettyChat | New SKIN-19..23. Re-opened SLASH-1, SLASH-3, SKIN-16 | Outline; From skin with nothing stored; `/pc skin`; widths; the v1.82.0 Skin tab | |
| QuickComms | New ICON-5, SKIN-24..28 | **`/qc test`: numbered glyphs on the dial's first ring and the pad sections, folder and speech-bubble defaults (ICON-5, image-52/53)**; outline; From skin and step 11; HUD scale grows the cells; widths. Its Pending sign-off also asks for a re-run of LOC-1, SKIN-1, 2, 3, 5 and 10 (amended to the new faces, old results kept) | |
| WhatGroup | New SKIN-25..29. Re-opened SLASH-1, SKIN-1, SKIN-2, SKIN-6, SKIN-9, SKIN-17 | Outline (the popup is window text); no font settings; `/wg skin`; widths; picker and override reset | |

Checks reworded with their passes kept, so no run is owed: AuraMaster LAYER-2, SKIN-1, SKIN-2 and SKIN-5 (the TEST
marker dropped from the wording); DpsRace UT14, W5b, CP1 and CP4; DropWatcher FEED-66 (points at TOAST-8);
MultiMeters SLASH-19 (renumbered references); PanelMaster SKIN-1 (Oxanium to Prototype). QuickComms' amended LOC-1
and SKIN-1, 2, 3, 5 and 10 keep their passes too, but its Pending sign-off asks for a re-run (row above).
