# Smoke tests: the owner's fifth smoke round (2026-11-03)

**Fully exit and restart the client before you start. A `/reload` is not enough.** This round ships no new font or
texture file, but all 16 addons carry a re-vendored LibKa0s, and a full restart makes every addon load that copy fresh,
with no window, band or AceGUI widget left over from the last session. Every check below assumes the local re-cut
LibKa0s v1.85.0 at **17d18aa** (R5-REL, the sixteenth re-cut), re-vendored into all 16 addons. Turn Lua errors on with
`/console scriptErrors 1`. Any Lua error or taint warning fails the check.

Nothing here has passed. Every Result is blank for you to fill in. An ID is the check's ID in that addon's
`docs/smoke-tests.md`, where the full steps are; the short form is here. Addon prefixes: ST Skin Tester, AT
AbsorbTracker, AM AuraMaster, BL BankLedger, CM ConsumableMaster, DR DpsRace, DW DropWatcher, KC KickCD, LH LootHistory,
MM MultiMeters, PM PanelMaster, PF PartyFrameEnhanced, PG PremadeGroupsFilterExtension, PC PrettyChat, QC QuickComms,
WG WhatGroup. LibKa0s has no smoke file, so its in-game checks are the Skin Tester's and the hosts'.

Order follows your feedback: 1 header shade, 2 window geometry, 3 DpsRace header (3a title left), 4 Quick Comms pad, 5
header centring, 6 dropdowns (6b `/dr sim`), 7 icons. Many host checks cover several items at once; each is listed once,
under the item it mostly checks, and named again where it also counts.

## 1. Ka0s Default's header is darker: option C (R5-L1)

Option C is `#262006` at the top to `#141103` at the bottom, flat `#1D1805`, and it is also the picker's second swatch.
Ka0s Default only: every other skin's band is unchanged.

| ID | Do | Pass | Result |
|---|---|---|---|
| LH SKIN-51 (first part) | Ka0s Default, `/lh show` | The History band is darker than round 4, still a gold gradient with the gold title readable; nothing else moved | |
| BL SKIN-45 (first part) | Ka0s Default, `/bl show`, `/bl session`, Export and its copy window, `/bl debug`, `/bl sim`, `/bl skin` | Every band is the same gold gradient, a little darker than round 4, one band per window (SKIN-42 no longer quotes the round 4 hexes) | |
| DW SKIN-47 (first part) | Ka0s Default, `/dw show` | The band is darker than round 4's, the same olive-gold gradient with its gold title | |
| WG SKIN-39 (first part) | Ka0s Default, `/wg test` | The popup's band is a step darker than round 4, the gold title still clear (SKIN-36 no longer quotes the hexes) | |
| ST SHOW-48 | `/st show` in Ka0s Default beside Loot History's or Drop Watcher's window | The showroom band matches theirs, darker than round 4; the Ka0s Default card's second swatch is that darker gold, not black; other skins' bands unchanged | |
| PM SKIN-40 (swatch part) | `/pm skin` | The Ka0s Default card's second swatch is the new, darker header color | |
| MM SKIN-44 (re-opened) | Ka0s Default, Header > Title bar > Use the skin's background ticked | The meter's band is the darker gold and now a gradient (R5-MM1), no line under the console title | |
| DR SM-DR-R4RV2 (amended) | As its file says | The window bands are the darker gold (the hexes are no longer quoted); the icon edges as round 4 | |

## 2. Every window like Loot History's: band flush inside the edge, no strip (R5-L2, R5-WIN, R5-MM1)

Pass in every row: the band starts right inside the window edge with no strip of body color (the "inner border" of image
33) above it or at its ends; one band per window; content keeps its inset under the band; under WoW Midnight (2 px edge)
the band and its header sit 1 px lower, still flush. Keep Loot History's window open beside each for reference.

| ID | Do | Pass | Result |
|---|---|---|---|
| LH SKIN-52 | `/lh show` and Export in Ka0s Default, WoW Midnight, Glass, EllesmereUI if installed | The reference look: band flush, title and close level on its middle, the tab strip just under the band and moving with it, filter bar and Data Set dropdown in place, windows still drag | |
| MM WIN-57 | `/mm test` beside Loot History; WoW Midnight; Obsidian; Header > Title bar: untick Use the skin's background, pick a color; Frame: Custom border 3 px; collapse, expand | The meter's bar runs flush inside the edge (top, left, right) in the title gradient like Loot History's; rows keep their 6 px inset; a custom color draws flat at the same size with no gradient left; it sits inside a 3 px custom edge; **collapsed, the meter is exactly the bar and its edge, no strip of body under it**; header row on the bar's middle | |
| MM EXPORT-56 | The Export modal under Ka0s Default, WoW Midnight, WoW Default | Its bar flush inside the edge, *Export* and close on the bar's middle | |
| MM SKIN-48 | `/mm debug` and copy, `/mm perf`, `/mm sim`, `/mm skin`; then WoW Midnight | Each library window wears the band flush inside its edge, children on its middle | |
| BL SKIN-46 | `/bl show`, `/bl session`, Export; test mode; WoW Midnight; back to Ka0s Default | Each band flush; title, close and the TEST MODE badge on the band's middle; the tab strip, filter bar and export form unmoved under Ka0s Default | |
| DW SKIN-48 | `/dw test`, `/dw show`; compact and minimized; your drop's Offer panel and Edit message box; WoW Midnight, Obsidian, EllesmereUI | Flush band; title, TEST MODE, minimize, layout and close centred; minimized is the band and its edges alone; the Offer panel and the Edit message box have the full band, content below it | |
| WG SKIN-40 | `/wg test` beside Loot History; WoW Midnight, Obsidian, WoW Default, Ka0s Default | One band (no darker double band) flush inside the edge; title on its middle; the first row 8 px under the band; the popup still drags | |
| QC SKIN-33 | `/qc preview`, a callout popup, its Choose icon browser and its Wowhead window, `/qc debug` and Copy, `/qc perf`, `/qc skin`; WoW Midnight, Azeroth | One band each, flush; title and close on its middle; the popup's and browser's page starts under the band; the Preview dropdown row a small gap under it | |
| ST SHOW-49 | `/st show` in Ka0s Default, WoW Midnight, Glass, WoW Default, EllesmereUI's source | The title bar fills the band flush; title and close centred within 1 px; the title follows the skin's alignment | |
| ST SHOW-50 | `/st show` in Ka0s Default, WoW Midnight, Glass, beside Loot History | The body starts 6 px inside the title bar and footer; the SettingsFrameTemplate sample's title and close centred on its band; the Confirm popup sample has one band with its question centred on it | |
| ST DIAG-5 | `/st debug`, Copy, `/st perf` step panel; Ka0s Default, WoW Midnight | One band per window, title and close centred | |
| AT DIAG-55 | `/at debug`, Copy, `/at perf`, `/at skin` | Library windows: darker band flush inside the 1 px edge, children centred | |
| AM SKIN-49 | `/am debug`, Copy, `/am perf`, `/am skin`; Obsidian, WoW Midnight | The same; the title centred across the band | |
| CM DIAG-44 | `/cm debug`, Copy, `/cm perf`, `/cm skin`; Azeroth, WoW Midnight | The same | |
| KC DIAG-47 | `/kcd debug window`, Copy, `/kcd perf start`, `/kcd sim`, `/kcd skin`; Obsidian, EllesmereUI | The same, all five windows | |
| PM SKIN-40 | `/pm debug`, Copy, `/pm skin`; Obsidian, WoW Default, Glass | No load error; the same | |
| PF SKIN-42 | `/pfe debug`, Copy, `/pfe perf`, `/pfe skin`; Glass, WoW Midnight, WoW Default | The same | |
| PC RV-87 | `/reload`; `/pc debug`, its copy window, `/pc skin` | No Lua error; the same | |
| PF INSTALL-4 (re-opened) | As its file says | Its existing pass condition on the re-vendored build | |
| DR SM-DR-R5DR1, SM-DR-R5RV | See item 3 | | |
| PG collapsed strip (R5-PG2, **not yet built**) | Collapse the PGFE panel in Ka0s Default, Ember and WoW Midnight (images 59 to 61) | The collapsed panel is exactly the header band and its edge, with no black or body-color strip below the bottom border. R5-PG2 had not landed at this gate: run it once its commit and its PG smoke row exist | |

## 3. DpsRace has its header band (R5-L2, R5-DR1); 3a the HUD title is left

| ID | Do | Pass | Result |
|---|---|---|---|
| DR SM-DR-R5DR1 | Ka0s Default, WoW Midnight, Ember, WoW Default: `/dr hud show`; `/dr results`, a run, its Timeline, then Gear view; drag each by its title; `/dr test` (images 34 to 37, 45) | All four windows show the skin's band, flush, no strip. **3a: the HUD title sits LEFT in every skin**; Results, Timeline and Gear titles follow the skin. Title, close, the HUD's lock, settings and Results controls and the Results view chevron centred within 1 px, none overlapping. Runs/Insights tabs flush under the band, never over its last row; the test strip under the band (HUD) or the tabs (Results); dragging works | |
| DR SM-DR-R5RV | `/reload` under Ka0s Default; `/dr hud show`, `/dr results`, Timeline, Gear view; `/dr debug`; `/dr sim`; copy a talent loadout; General > Skin list presses | No Lua error; the darker band; the debug console, simulation window, copy window and skin picker show the band too with title and close centred; the skin list closes on each outside press, the last opening Font | |

## 4. Quick Comms: the pad's header band (R5-QC1)

| ID | Do | Pass | Result |
|---|---|---|---|
| QC PLOOK-12 | A Comms Pad with a section ("Solo"), Ka0s Default; then Obsidian, Azeroth, Ember, WoW Midnight, WoW Default; collapse with "-"; Pad > Layout growth up; Pad > Header custom background, class color, Border thickness 2 (images 40, 41) | The header row wears the skin's title band with its gradient, inside the pad's edge and rule with no strip; header text left, "-" right, both on the band's middle; **section titles draw no band in any skin**; no edge or box of its own in any skin; under WoW Default inside the dialog art; collapsed is exactly the band and its edge; **growing up, the band is the bottom row with the same gradient direction (lighter at the top)**; a picked color or class color replaces the band; a 2 px border draws around the band only under Ka0s Default | |
| QC PLOOK-1 to PLOOK-9 (re-opened) | Each skin as its file says | The amended look: the header is the skin's title band with no edge; section titles draw no band | |
| QC ANIM-22, FSKIN-12, LOOK-3, FSKIN-1, FSKIN-2 (re-opened) | As each file entry says | Their amended expected result against the header band | |

## 5. Every header child centred on the band (R5-L3, R5-WIN, R5-PG1)

Lead's call 6: title, close, header buttons, chevrons and badges sit on the band's geometric middle, in every skin. The
item 2 rows above also check this per window; these rows are the focused ones.

| ID | Do | Pass | Result |
|---|---|---|---|
| PG SKIN-50 | PGFE on Dungeons under each of the nine skins: Ember and High Contrast first, then Ka0s Default, Obsidian, Azeroth, Glass, WoW Default, WoW Midnight, WoW Forever; collapse and expand; EllesmereUI painting the panel; `/dump PremadeGroupsFilterExtensionPanel.TitleContainer.TitleText:GetPoint(1)` | The title's letters (ignore descenders) and the arrow's chevron on the same line, the band's middle, within 1 px, in every skin and both states; on EllesmereUI's bar too; the dump reads `CENTER`, a frame, `CENTER`, 0, 0 (images 42, 43) | |
| ST PICKER-25 | `/st skin` in Ka0s Default, WoW Midnight | "Choose a skin" and the close mark centred on the band | |
| SR5-1 | With EllesmereUI installed and its source on, open Loot History (`/lh show`) and `/st show` | Each header child centres on EllesmereUI's 25 px bar, flush at the top | |
| Also counted here | LH SKIN-52, MM WIN-57, BL SKIN-46, DW SKIN-48, WG SKIN-40, QC SKIN-33 and PLOOK-12, ST SHOW-49, DR SM-DR-R5DR1 | | |

## 6. Dropdown lists close on an outside press (R5-L4, R5-DD)

The skin picker window that `/<addon> skin` opens is the same window as the one-time skin notice (`O.SkinNotice`), so
the `/<addon> skin` rows cover the notice too. Escape still closes the whole window everywhere.

| ID | Do | Pass | Result |
|---|---|---|---|
| ST PICKER-24 | `/st skin`: open the list, press the body; the game world; the title, the eye, the gear; General > Skin: open the settings page's list, press Font; both pickers up, open the picker's list, press the settings page's list button (images 46, 47) | Every press closes the list; the eye and gear still do their own thing; Font opens; the two lists close independently; Escape closes the window | |
| AT SKIN-44, AM SKIN-50, BL SKIN-45 (second part), CM SKIN-43, DW SKIN-47 (second part), KC SKIN-44, LH SKIN-51 (picker part), MM SKIN-47, PM SKIN-41, PF SKIN-41, PG SKIN-49, PC RV-87 (picker part), QC SKIN-32, WG SKIN-39 (second part) | In each addon: `/<slash> skin`, open the skin list, press the window body, then the game world, then the Font dropdown; repeat from that addon's settings Skin tab picker where its row says so | Each press closes the list; the last opens Font; a row still picks; the list's own button still toggles; Escape closes the window | |
| DW COMPACT-10 | `/dw compact`, `/dw test`, Filters ▾; press the rows, the game world, the View dropdown; reopen, pick in its Quality dropdown; press the panel background; Filters ▾ again | Each outside press closes the panel, the last opening View; a pick in its own dropdown applies and keeps it open; its own background keeps it open; Filters ▾ toggles | |

Only Drop Watcher landed an R5-DD commit. The other 15 addons committed nothing under R5-DD (the run lands no commit for an id
with nothing to change in a repo). If you meet any other Ka0s list that stays open after an outside press,
note it here.

## 6b. `/dr sim` starts idle; a 15 s race in real time (R5-DR2)

| ID | Do | Pass | Result |
|---|---|---|---|
| DR SM-DR-R5DR2 | Out of combat, bare `/dr sim` (images 49, 50); pick *Behind the best*, back to *New best*, *Start*; time *Race starts* to the Results window with a stopwatch; *Stop*; `/dr sim died`; `/dr sim sticky`; the launcher's *Sim mode* twice; `/dr sim sideways` | Bare `/dr sim` starts nothing: the window is idle with the scenario dropdown and *Start* (no *Resume*), the steps previewed and locked. After *Start*, the HUD runs 0:15 to 0:00 at real speed, the final countdown one number a second, the buzzer about 15 s after *Race starts*; Stop!, the wait and the card at real speed; the card holds about 4 s before Results; the chart, pace bar and chip compare against a 0:15 best and *New best* shows the toast. *Stop* leaves the window idle; `died` starts at once; `sticky` waits for the drop-combat hint; *Sim mode* opens idle, then stops; `sideways` prints the usage. `/mm sim` unchanged | |
| DR SM-DR-BL14, SM-DR-BL15, SM-DR-PT11 (amended) | As their rows say, now with `/dr sim newbest` | *first* is a 0:15 board; *incomplete* 9 s and *died* 6 s; PT11 reads *Combat Ended 0:09 into the race*; BL15 prints the sim usage, then a line per scenario | |
| DR rows now naming `/dr sim newbest` | R8e, P5, P11, SM-DR-CH8, CH9, BL8, BL16, RC7, RC8, RC10, UT6, SK4, FP9, PT7, PT9, PT10, PT13, PT14, FS6, R4DR1, R4DR4, R4ZOOM, R4DR7 | Their expected results are unchanged; only the command moved, because bare `/dr sim` no longer starts a race. SM-DR-R4DR6 is superseded by SM-DR-R5DR2 | |

## 7. Icons: cropped and edged by site (R5-L5, R5-ICON)

The rule (LibKa0s `docs/api`): Blizzard icon art cropped at least 0.07 a side; in a window or on a settings page a 1 px
edge in `icon.outline` (mid gray `#4D4D57` under Ka0s Default); on the HUD and on toasts a 1 px edge in `icon.border`
(black under Ka0s Default); inline `|T` icons in tooltips and chat cropped only; atlas glyphs, Ka0s marks and round art
exempt.

| ID | Do | Pass | Result |
|---|---|---|---|
| DR SM-DR-R5ICON | Ka0s Default, WoW Forever, Ember: Results' Used and Class columns, a run's class and spec icons, its Usage list, Compare's lines; hover a Used cell and the HUD's Your best card; the new-best toast (images 51, 52) | Every icon cropped inside a 1 px edge: gray in the Results window, black around the toast's class and spec icons; the class emblem whole; tooltip icons cropped with no edge; a hidden icon leaves no empty edge | |
| DW SKIN-49 | `/dw test`, `/dw compact`; full layout's Drops rows and Me/Them gear icons, the detail card, History, the Offer panel; a toast; WoW Forever; change UI scale, window scale, toast scale; Color by item quality; untick Use the skin's color (images 53 to 56) | Window icons edged in mid gray, one screen pixel on all four sides, art cropped; the toast's edge black; WoW Forever a warm gray-brown edge; the edge stays one pixel at once after a scale change; quality colors still win; your swatch when the box is unticked | |
| MM TIP-37 | Hover a damage cell, a Deaths cell and a name with Show targets on | Every tooltip icon cropped, no native corner, still in one column, no border | |
| KC SKIN-45 | `/kcd config` > Spells, Ignore settings panel unticked; Obsidian; ticked; the Class and specialization dropdown | Spell icons cropped with a 1 px outline that follows the skin; cropped with no outline when ticked; the spec list's icons cropped | |
| CM SKIN-44 | Ignore settings panel unticked; a Macros tab; Stat Priority's spec dropdown; Add by ID or name suggestions; WoW Forever; ticked again | Item and drag icons and suggestions cropped with a gray outline; spec icons cropped; ticked keeps the crop and drops the outline; marks and the macro bar unchanged | |
| QC ICONS-7 | Ignore settings panel unticked; Choose icon… > Game icons; the footer preview; the popup chooser; the Groups row and Preview table; Markers and Glyphs; switch skins; tick the box | Game icons cropped inside a 1 px outline; markers, glyphs and the speech bubble whole with no outline; the outline follows the skin; ticked keeps the crop only | |
| LH SKIN-51 (id list part) | Ignore settings panel off; General > Filters > Blacklist and Currency blacklist with entries; type in the add box; turn the box on | Entries and suggestions cropped with a 1 px gray outline; cropped only when the box is on | |
| AM SKIN-51 | General > Spell categories, a container's Filters aura id list, and their add boxes; switch skins; scroll and remove a row | Spell icons cropped and edged in the window outline, following the skin; no stray edge left on another row or a suggestion with no icon | |

## 8. Follow-up after the gate: the PGFE collapsed strip (R5-PG2) and the DpsRace EllesmereUI pane height (R5-DR1)

These rows landed after R5-GATE (PremadeGroupsFilterExtension 2d3ca07, DpsRace fc3f3e6). They supersede the
"not yet built" PG row in item 2.

| ID | Do | Pass | Result |
|---|---|---|---|
| PG SKIN-51 | Open PGF on Dungeons and collapse the panel. Under each of the nine skins: Ka0s Default, Ember and WoW Midnight first (images 59 to 61), then Obsidian, Azeroth, Glass, High Contrast, WoW Default, WoW Forever; expand and collapse again; EllesmereUI painting the panel; `/dump PremadeGroupsFilterExtensionPanel:GetHeight()` collapsed under Ka0s Default | The bottom border is the panel's last line: no strip of black, body or band color below it, and the band fills the space between the top and bottom borders, in every skin and after re-collapsing. Under EllesmereUI the collapsed panel is its 25 px bar, nothing below it. The dump reads 32. Fail: any strip below the bottom border, or a Lua error | |
| DR SM-DR-R5DR1B | With EllesmereUI loaded, its third-party skinning on and DPS Race in its list, set General > *Skin* > *Skin source* to *EllesmereUI*; `/dr results` with a few runs; look at the foot of the *Runs* list and its detail pane, then *Insights*; drag the bottom edge taller and shorter; then *Ka0s skins* under Ka0s Default and WoW Midnight (its 2 px edge) and look again | Under EllesmereUI's 25 px bar the *Runs* list, the detail pane and the *Insights* charts reach the footer rule, with no empty strip of body color (about 5 px) between the last row and the rule; the same under the Ka0s skins and on every resize | |
