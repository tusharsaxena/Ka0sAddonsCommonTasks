# Skin causes: yes or no

Goal: change the skin and every addon changes with it. The 727 rows reduce to **31 causes**, the meaning-color line and 237 rows that are not gaps. Settings panel rows count only if they stay stock with the Scope cleared. Recommended Fix: 21 causes, 241 rows. Recommended Leave: 10 causes, 204 rows.

| ID | What you'd see in game | Where it reaches | Rows | Effort | Recommendation |
|---|---|---|---:|---|---|
| L1 | Minimap button tooltip text, including the green and red Yes/No words, ignores the skin | Library, every addon | 19 | S | Fix: one change, the launcher just needs the skin |
| L2 | Hover tooltips: the text lines stay Blizzard's color, on settings rows and a few windows | Library, every addon; plus AM, PC, QC | 9 | S | Fix: the standard already says lines follow the skin |
| L3 | Settings, Scope cleared: header divider, nav rail edge, id suggestion popup and tab edges keep Blizzard art or ignore the skin | Library, every addon | 5 | M | Fix: your ruling, every element supports skins |
| L4 | Settings, Scope cleared: section headings and some labels stay or snap back to the Blizzard font | Library, every addon; plus DW, MM, PM, PGFE | 5 | S | Fix: your ruling |
| L5 | Settings, Scope cleared: fixed colors remain, on slash command rows, AuraMaster dropdown values, PanelMaster hints and an id list warning | Library, every addon; plus AM, PM | 7 | S | Fix: your ruling |
| L6 | Blizzard or plain white marks (tick, cross, remove, refresh, help, hover flash) beside skinned controls, Scope cleared included | Library, every addon; plus CM, DR, KC, LH, MM, QC | 21 | M | Fix: use the Ka0s icons and tint them |
| L7 | Scroll bars: the small up and down arrow buttons stay Blizzard's | Library, every addon | 3 | M | Fix: visible in every window |
| L8 | Small misses: odd labels never painted, a resize grip with no skin, wrong color role, widget leftovers | Library plus 8 addons | 26 | S | Fix: quick, one by one |
| L9 | Title bars differ between windows: 24 to 30 high, left or centered | Library, every addon; plus BL, DR, DW, LH, MM, PGFE, WG | 12 | M | Fix: most visible on export and tool windows |
| L10 | Icon shapes and the minimap ring look the same in every skin; only icon color changes | Library, every addon | 30 | L | Leave: an icon set is not skin data |
| L11 | Text size comes from each window's layout; the skin only scales it | Library, every addon | 21 | L | Leave: your size ruling, it protects layouts |
| L12 | Debug console, copy boxes and arrow glyphs always use the fixed-width font | Library, every addon | 24 | S | Leave: fixed width is required, and no skin changes it |
| L13 | Chat lines: cyan [tag], yellow commands, gold, gray, debug ON/OFF words are fixed | Library, every addon | 65 | M | Leave: the standard fixes them; chat is not a skinned surface |
| D1 | Settings builder: 'use the skin' options start off, and new font, border and bar rows start on Blizzard picks | Library, every addon | 6 | S | Fix: every future setting then follows the skin |
| D2 | HUD text keeps its stored color: bar names, timers, labels, counts | AT, AM, CM, DR, KC, MM, PFE | 15 | L | Fix: needs a new HUD text color in every skin, and reverses the 'HUD colors are the player's' decision |
| D3 | HUD bar fill keeps its stored color | AT, AM, PFE | 3 | L | Fix: needs a new HUD fill color in every skin; class and interrupt colors stay |
| D4 | HUD backgrounds, borders and their thickness keep stored values; some borders are off so the skin's never shows | AT, AM, CM, DR, DW, KC, MM, PFE | 25 | M | Fix: skin colors exist, add 'use the skin' and start it on |
| D5 | Glow, pandemic, running-out and cooldown tint colors keep stored values | AM, DW, KC | 6 | M | Fix glow; Leave warning tints, they carry meaning |
| D6 | Text shadows: HUD text ignores the skin's shadow setting | Library; plus AT, AM, CM, DR, DW, KC, MM, PFE, QC | 10 | M | Fix: new HUD shadow setting, on the same pass as D2 |
| D7 | QuickComms pads and dials keep their own look: every fill, edge and text color, plus the shine | QC only | 28 | L | Fix: the biggest single holdout; needs 'use the skin' on each block |
| D8 | Window text has no outline even though Ka0s Default lists one | Library, every addon | 11 | S | Leave: your ruling of Oct 31, HUD text only |
| D9 | Ka0s Default keeps Blizzard's resize grip and hover art; other skins tint them | Library, every addon | 7 | S | Leave: your earlier ruling, and it does follow the skin |
| A1 | Hand-built tabs, column header bands, footers, row hover, boxes and icon edges skip the skin's versions; some icons have no border at all | BL, DR, DW, LH, MM, PFE, WG | 17 | M | Fix: changes Ka0s Default a little, but makes windows match |
| A2 | Menus that are Blizzard's although a skinned Ka0s menu exists: DpsRace row menus, MultiMeters segment picker, PGFE dropdowns | DR, MM, PGFE | 3 | M | Fix: swap to the Ka0s menu |
| A3 | Skins with gloss (Glass) show no gloss on HUD bars | AT, AM, KC, MM, PFE | 5 | M | Fix: no change under Ka0s Default |
| A4 | Delete profile confirmation stays stock under every setting | Every addon with Profiles; found in AT, PM | 2 | M | Fix with care: Ace shares this box with non-Ka0s addons |
| A5 | Skin Tester's own sample rows that are not painted, so it misreports a skin | Tester | 14 | S | Fix: the tester has to tell the truth |
| A6 | Cooldown sweep, cast spark, shield, button press and flash, proc glow, text selection stay Blizzard's | AM, CM, DW, KC, PFE, PGFE, WG | 13 | L | Leave: game feedback players know; no skin setting exists |
| A7 | Fades and dims, flat thin bars, and skin settings nothing reads: corner radius, scroll width | CM, BL, DR, DW, KC, LH, QC, WG, library | 21 | M | Leave: nothing to see today, or a stated rule |
| A8 | PanelMaster panels keep the colors and textures the player chose | PM | 5 | M | Leave: panels are the player's own content |
| A9 | DpsRace clocks, bar colors and missing tracks stay as you set them | DR | 7 | S | Leave: your own calls, Oct 25 to 31 |

L = library, D = default flip, A = addon-specific. Effort: S under a day, M a few days, L a week or more; these are my estimates.

**One thing to decide with D2 to D7.** A flip reaches new profiles only. Existing profiles keep their stored colors unless we also migrate them, which overwrites choices players made. My recommendation is new profiles plus a one-click 'use the skin for everything' button.

## What can't be skinned

- **Blizzard's Settings window** (12 rows): the frame around our pages belongs to the client, and the standard forbids restyling it.
- **Client Menu popups** (12 rows): the minimap right-click menu. The client draws it and offers no paint hook; the only route is replacing it, as A2 does inside windows.
- **Tooltip frame, confirmation popups, color picker** (19, 20 and 6 rows): Blizzard frames shared with every addon. The lines we write in a tooltip can follow the skin (L1, L2); the frame can't.
- **Chat frame font, Group Finder rows, raid warnings, party frames, big countdown** (6 rows): client frames the addons only write into or attach to.

## Meaning colors: confirm

**MC (45 rows):** class colors, item quality, dispel types, cast states, stat, category, region and data hues stay the same in every skin, because the color is the information. Yes or no?

## Not gaps

237 rows, no answer needed: follow the Scope 48, LSM30 pickers being replaced 3, can't skin 75, game art 31, addon logos 27, layout 27, previews by design 22, missing-media fallbacks 4.

Totals: 445 rows in causes + 45 MC + 237 not gaps = 727. Row numbers are the CSV's line numbers (header is line 1). The row-by-row map is `SKIN_CAUSES_map.csv` beside this file.
