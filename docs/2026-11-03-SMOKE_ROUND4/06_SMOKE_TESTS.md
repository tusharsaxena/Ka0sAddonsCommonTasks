# Smoke tests: the owner's fourth smoke round (2026-11-03)

**Fully exit and restart the client before you start. A `/reload` is not enough.** This round ships no new font or texture file, but all 16 addons carry a re-vendored LibKa0s, and a full restart guarantees that every addon loads that copy fresh, with no window or AceGUI widget left over from the last session. Every check below assumes the local re-cut LibKa0s v1.85.0 at **2a78817** (R4-REL3, the fifteenth re-cut), re-vendored into all 16 addons. Turn Lua errors on with `/console scriptErrors 1`. Any Lua error or taint warning fails the check.

Nothing here has passed. Every Result is blank for you to fill in. An ID is the check's ID in that addon's `docs/smoke-tests.md`, where the full steps are; the short form is here. IDs starting `SR4-` are only on this list and have no addon file. They are cross-addon checks of a library item. Addon prefixes: ST Skin Tester, AT AbsorbTracker, AM AuraMaster, BL BankLedger, CM ConsumableMaster, DR DpsRace, DW DropWatcher, KC KickCD, LH LootHistory, MM MultiMeters, PM PanelMaster, PF PartyFrameEnhanced, PG PremadeGroupsFilterExtension, PC PrettyChat, QC QuickComms, WG WhatGroup.

Order: A dropdowns, B Skin Tester, C DpsRace, D MultiMeters sim, E Ka0s Default header, F icon outlines and HUD edges, G no header separator, H clean loads.

## A. Dropdown lists close on an outside press (R4-L1, LibKa0s OptionsCombat minor 4)

Lead's call 1: only dropdowns on Ka0s surfaces close (a Ka0s settings page, its Profiles page, a Ka0s window). Escape was not added.

| ID | Do | Pass | Result |
|---|---|---|---|
| ST PANEL-17 (new) | Settings > AddOns > Ka0s Skin Tester > Sample controls: open the AceGUI dropdown, A font picker and A bar texture picker in turn and click empty page space; open one, click another dropdown; click inside a list, scroll it, drag its scrollbar, click its own dropdown; Profiles > Existing Profiles, click outside; `/st show` > Controls, open each of the five dropdowns and click the showroom body; repeat one in combat | Each list closes on the outside press and the press does nothing else; clicking another dropdown closes the first and opens the second; presses inside the list, its scrollbar or its own dropdown never close it without a pick; a pick applies and closes as before; Profiles' list closes; the showroom's five close; the same in combat, no `ADDON_ACTION_BLOCKED` | |
| BL SKIN-41 (new) | BankLedger settings > Skin tab: open the Font picker, click beside it; open it, click another dropdown; open Texture, click in its list, its scrollbar, the dropdown | Closes on the outside click; the second opens; the inside presses keep it open or toggle as before | |
| MM PANEL-59 (new) | MultiMeters Frame > Quick style > Font (all surfaces) open, click empty page; open it, click another dropdown; open Border style, scroll it and click its scrollbar, then pick; once in combat | Closes, nothing else happens; second opens; stays open while scrolling, closes on the pick; the same in combat, no error | |
| WG SKIN-35 (new) | `/wg config` > Skin: open the Font list, click empty space; open it, click another dropdown; pick a row; scroll; Profiles > Existing Profiles, click outside; once in combat | Closes and nothing under the click changes; the other opens; the pick applies and closes; scrolling keeps it open; the Profiles list closes; no `ADDON_ACTION_BLOCKED` | |
| SR4-1 | AuraMaster's settings: open any of its own dropdowns (AuraMaster's AuraMasterDropdown widget), click empty page space | Closes like the AceGUI ones (it shares the stock pullout) | |
| ST PANEL-18 (new) | With a non-Ka0s Ace3 addon installed, open one of its AceConfig dropdown lists and click outside it; then a Ka0s dropdown (PANEL-17) and click outside | The other author's list behaves as before this round (it stays open until toggled, picked or its page hides); the Ka0s one closes. No Lua error naming LibKa0s | |

## B. Skin Tester (R4-ST1 to R4-ST4)

| ID | Do | Pass | Result |
|---|---|---|---|
| ST PANEL-16 (new, R4-ST1) | On a fresh profile, `/reload`, General > Skin; `/st show` > Controls in Ka0s Default, Obsidian, Glass; tick Ignore settings panel, untick it; open another Ka0s addon's Skin tab on a new profile | Ignore settings panel starts unticked here; AceGUI Dropdown, Ka0sMedia_Font, Ka0sMedia_Statusbar and the Addon surfaces TreeGroup wear the skin; ticking puts them and the pages to the client look live, unticking brings the skin back; the other addon still defaults the box ticked | |
| ST PANEL-6 (re-opened, R4-ST1) | As its file says | Its new starting state: the box unticked | |
| ST SHOW-42 (new, R4-ST2) | `/st show` > Addon surfaces, the "TreeGroup via PaintAce (Scope: panel)" cell, in each skin with the box unticked, then ticked | Both boxes the full 120 tall side by side; General, Skin, Strings, About in the left box; the right box reads "The General page". No thin strip, no hanging row, no empty pane | |
| ST SHOW-43 (new, R4-ST3) | `/st show` in Ka0s Default, then Obsidian | One "IconBorder, fromSkin" sample in Overlays and SquareIcon (crop) + IconBorder in Controls; in Addon surfaces nothing beside the "Waiting for the pull" box | |
| ST SHOW-44 (new, R4-ST4) | `/st show` in Glass, Ka0s Default, Obsidian; compare its title band with Drop Watcher's or Loot History's window in the same skin | The same band strength in all; Glass's band a faint white wash, not a brighter strip | |

## C. DpsRace (R4-DR1 to R4-DR7)

| ID | Do | Pass | Result |
|---|---|---|---|
| DR SM-DR-R4DR1 (new) | `/dr sim`, watch the race, stop and wait; `/dr test result`; Results, a top run then another; resize the window | Every figure box (running Damage and DPS · Live, the Stop! and waiting tiles, the result card, the Results detail's Damage, DPS, Meter DPS, Delta) has its caption and figure centred; Delta and New best are a centred pair under the three boxes, Delta alone under the middle box with no badge; nothing clips at minimum width | |
| DR SM-DR-R4DR2 (new) | Arm Race screen with a dummy targeted; clear target; a non-dummy NPC; the dummy; minimum size | Equal gaps between Race Length, Target and Your best, a little more above Arm Race; with the amber warning the blocks step down and come back; no clip or overlap | |
| DR SM-DR-R4DR3 (new) | A dummy you have a best on; 0:30, 1:00; switch spec; hover the card | The label reads just *Your best*; the hover's first line under it names *<spec> · <type> · <length>* and follows each change | |
| DR SM-DR-R4DR4 (new) | A best that used a potion twice and Well Fed (or `/dr sim`); a best that used nothing | The card's second line is *date · ilvl ·* then one small icon per consumable, *x2* after one used twice, no top ability; augment runes and Healthstones show, on-use trinkets do not; nothing after *ilvl* when none was used | |
| DR SM-DR-R4DR7 (new, supersedes the hover part of R4DR4) | Hover the Your best card for a best with a potion and a flask; then one with none | Your best, the board, the date, Length, Damage, DPS, a line per consumable (icon and name), *Click to open this run in Results.*; no numbered top 3 abilities; with nothing used it goes from DPS to the click hint; the click still opens the run | |
| DR SM-DR-R4DR5 (new) | Arm Race screen with a best; a board with no race; no target | The button reads just *Arm Race*, never *· beat <DPS>*; it arms as before | |
| DR SM-DR-R4DR6 (new) | `/dr sim` > Run at the default delay; `/dr sim died` > Run; `/dr sim`, click Race starts, Racing, at once Buzzer | Steps *Armed*, *Race starts*, *Racing (30 s of damage in 10 s)*, *Buzzer*, *Result card*, *Results window* (*Racing (12 s of damage in 10 s)* and *Combat ends* for died); during Racing, about 10 s, the clock runs about 3x fast, damage climbs steadily, spell rows and chart fill with no gaps; the buzzer comes by itself; a Buzzer click mid-race waits with *The race is still running.* | |

## D. MultiMeters sim (R4-MM1)

| ID | Do | Pass | Result |
|---|---|---|---|
| MM SIM-14 (new) | Step delay at the default 1 s, `/mm sim start dungeon`; then `raid`, `wipe`, `zone` | Rows read *Pull Trash (10 s)* and *Pull Speaker Shadowcrown (10 s)*; each fight runs about 10 s, bars grow about twice a second, a damage dealer dies about two thirds into the boss; every *Pull ...* row in the other scenarios reads *(10 s)* and plays about 10 s | |

## E. Ka0s Default header (R4-L2: option E, swatch 2 is the header)

| ID | Do | Pass | Result |
|---|---|---|---|
| ST SHOW-45 (new) | `/st show` in Ka0s Default | The title band is a dark gold gradient, #3A2F0A top to #1F1905 bottom, no line under it; the Ka0s Default card's second swatch is #2C2408, not black | |
| SR4-2 | Under Ka0s Default open any skin picker (`/lh skin`, `/dr` General > Skin, `/pm skin`) and one window of each kind: an addon window (`/lh show`), a debug console (`/bl debug`), a copy window | Every band is the same dark gold gradient; every picker's Ka0s Default second swatch is the header color | |
| Per-addon header checks (new) | As each file says: BL SKIN-42, MM SKIN-44 (with *Use the skin's background*, the meter strip a flat #2C2408, also with LibKa0s absent), PM SKIN-37, WG SKIN-36, DR SM-DR-R4RV2, AM SKIN-47 | A dark gold band in each, never near-black | |
| Re-opened (R4-SEP / R4-L2 moved the expected result) | AT DIAG-1, CM DIAG-9, KC DIAG-20, PM DIAG-1, BL SKIN-1 and DIAG-7, WG SKIN-1, SKIN-32 | As each file now says: a dark gold band, no line under the title | |

## F. Icon outlines in windows, HUD edges unchanged (R4-L3, R4-L4, R4-HUD, R4-ZOOM)

Under Ka0s Default a window's icon outline (`icon.outline`) is now gray #4D4D57; a HUD icon's edge (`icon.border`) stays black. The other outline colors: Glass white 0.35, WoW Forever #5A5048, Ember #8A3C1C, WoW Midnight #7A6532; Obsidian, Azeroth, High Contrast and WoW Default look as before.

| ID | Do | Pass | Result |
|---|---|---|---|
| ST SHOW-46 (new) | `/st show`, Overlays' "IconBorder, fromSkin" and Controls' SquareIcon (crop) + IconBorder, in each skin | The 1 px outline in each skin's color above; never black in Ka0s Default, never thicker than 1 px, no art edge inside | |
| ST SHOW-47 (new) | The same two samples in Ka0s Default, Glass, Ember | Still the window outline of SHOW-46 (gray in Ka0s Default) | |
| ST SHOW-39 (amended) | As its file says | The outline names icon.outline's color | |
| DR SM-DR-R4HUD (new) | Ka0s Default, `/dr test running` with spell rows and chart on; then `/dr results`: a run's detail, its chart icons, Timeline, Compare; then Glass and Ember | The HUD's spell icons and the HUD chart's cooldown icons have a **black** 1 px edge; every Results icon (detail rows and chart icons, compare, timeline casts) keeps the gray outline; under Glass and Ember the HUD edges are those skins' HUD border, not the outline | |
| DR SM-DR-R4L3, SM-DR-R4RV3, SM-DR-FS11 (amended) | As their rows say | The same split: HUD black, windows gray; no Lua error on load | |
| MM SKIN-46 (new) | Ka0s Default, Bars > Icons > Show icons and *Use the skin's icon border*, `/mm test`; Glass, Ember, WoW Midnight, WoW Forever; back | Every row's unit icon has a **black** 1 px edge under Ka0s Default; in the others each skin's HUD border, never its outline; black again on return | |
| PF SKIN-40 (new) | Ka0s Default, `/pfe unlock` or a party cast; Glass, Ember, WoW Midnight, WoW Forever; back | The cast bar's spell icon has a **black** 1 px edge, then each skin's HUD color, black again | |
| PF SKIN-36 (amended) | As its file says | It now names the HUD's black `icon.border` edge | |
| AM SKIN-48 (new) | Ka0s Default, an icons and a bars container with Show border on; Obsidian, Azeroth, WoW Midnight; tick *Use the skin's color*; back | Every icon edge black under Ka0s Default; with the skin's color ticked each skin's `icon.border`, never the outline | |
| WG SKIN-38 (new) | With DpsRace, MultiMeters or PFE loaded, Ka0s Default, `/wg test`; Obsidian; back | The teleport icon keeps the gray window outline while those HUD icons stay black | |
| BL SKIN-44, LH SKIN-50, PM SKIN-39, PC RV-86 (new) | As each file says | The R4-L4 re-cut changes nothing these addons draw; clean load | |
| SR4-3 (no native edge) | Ka0s Default, then Obsidian: every HUD icon with its own edge — DpsRace HUD rows and chart, MultiMeters rows, the PFE cast icon, AuraMaster icons and bars, KickCD's icon grid and castbar, DropWatcher, QuickComms pads and dials, ConsumableMaster's buttons, AbsorbTracker | Each icon's art is cropped inside its edge; no rounded or beveled Blizzard native edge shows anywhere | |
| DR SM-DR-R4ZOOM, MM SKIN-45, QC ICONS-6 (new, R4-ZOOM) | As each file says | The crop is at least 0.07 per side at each site those checks name; QC at Zoom 0 still shows no native rim, glyphs and raid markers uncut | |

## G. No line under any window's title (R4-SEP)

The Skin Tester's showroom is the reference (image 27). Check each window under Ka0s Default, then one or two other skins as the addon's check says. Row dividers, footer rules, tab-strip rules and settings pages' header rule stay.

| ID | Addon: windows | Pass | Result |
|---|---|---|---|
| ST DIAG-4 | Skin Tester: debug console, its copy window (the showroom is the reference) | No line under either title | |
| AT DIAG-54 | AbsorbTracker: debug console, Copy window, perf step panel | No line under any of the three | |
| AM SKIN-47 | AuraMaster: debug console, its copy window; also the skin picker (`/am skin`) | No line under any title | |
| BL SKIN-43 | BankLedger: ledger window, session window, Export modal and its copy window, debug console and Copy box, sim panel, skin picker | No line; the ledger's tabs and their rule unmoved | |
| CM DIAG-43 | ConsumableMaster: debug console, copy window, perf panel, skin picker | No line under any of the four | |
| DR SM-DR-R4SEP | DpsRace: race HUD, Results, ability timeline, gear view, debug console, simulation window, copy window, skin picker | No line under any; footer, tab and legend rules stay | |
| DW SKIN-46 | DropWatcher: main window (full, compact, minimized), debug console, its Copy window, skin selector, `/dw sim` Steps panel | No line under any; the bottom-strip rules stay | |
| KC DIAG-46 | KickCD: debug console, copy window, perf step panel, skin picker | No line under any of the four | |
| LH SKIN-49 | LootHistory: History window, Export modal and its copy window, debug console and its copy window, skin picker | No line; tabs unmoved | |
| MM WIN-56 | MultiMeters: every meter window (also on a profile that had Show divider on), Export modal, debug console and copy window, first-run skin picker | No line; the Header > Title bar divider rows are gone; schemaVersion 26 | |
| PM SKIN-38 | PanelMaster: debug console, copy window, skin picker | No line under any | |
| SR4-4 | PartyFrameEnhanced: debug console (`/pfe debug`), its copy window, skin picker (`/pfe skin`) | No line under any | |
| SR4-5 | PremadeGroupsFilterExtension: debug console (`/pgfe debug`), its copy window, skin picker (`/pgfe skin`) | No line under any | |
| PC SKIN-33 | PrettyChat: debug console, copy window, skin selector | No line; the console's status rule stays | |
| QC SKIN-31 | QuickComms: Preview window, debug console and Copy, perf, a callout popup, its Choose icon browser and the Wowhead address window, skin picker | No line under any title; the page header rule inside the popup and browser stays | |
| WG SKIN-37, SKIN-36 | WhatGroup: the popup (`/wg test`), debug console, its Copy window | No line under any; rows 8 px under the band | |

## H. Clean load

| ID | Do | Pass | Result |
|---|---|---|---|
| SR4-6 | After the full restart, log in with all 16 addons enabled; `/reload` once | No Lua error and no taint warning from any addon; every addon's settings page opens | |
