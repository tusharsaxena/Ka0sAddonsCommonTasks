# MultiMeters — settings layout analysis

Item 020. Read-only analysis of `../MultiMeters` at `master` (2026-10-24). The current map below is not
transcribed from `docs/settings-panel.md`. It was taken from a headless load of the addon (the vendored
test kit's loader, `NS.Schema` walked in order), then checked against `settings/*.lua`. Line numbers refer
to that tree.

Notation: `[cb]` checkbox, `[dd]` dropdown, `[sl]` slider, `[sw]` color swatch, `[eb]` edit box,
`[btn]` button, `[media]` LSM dropdown. `SL` = the row starts a new line (`startsLine`). `C` = emitted by a
LibKa0s composer (`settings/Schema_Compose.lua`). `(hidden)` = schema row with no panel widget.
`(session)` = `sessionOnly`.

## Current map

**Counts.** 3 settings pages (General, Windows, Profiles) plus the landing page. The Windows page has a
nav rail with 7 entries. There are **30 tabs**: 3 on General and 27 on the Windows rail
(1 + 4 + 4 + 6 + 6 + 3 + 3). Profiles has no tabs. `NS.Schema` has **170 rows**: 159 are drawn on the
panel, and 11 are hidden (6 on Header > Controls, 4 in General's Export group, and `window.columns`).
The bespoke controls are the band picker, New, Duplicate, Delete, Source window, Settings to copy and
Copy, the Columns block editor, and the composer's Reset position / Reset all settings pair.

```
Landing (library BuildLandingPage) — logo, tagline, Slash Commands

General page                                   settings/General.lua:196 (CreatePanel), :247 (RenderTabbedSchema)
├─ Tab "Master controls"                       Schema.lua:1227 block(MASTER_ROWS) ← Schema_Compose.lua:634
│    Enable Multi Meters [cb] enabled SL C   | General visibility [dd] master.visibility C
│    Master scale [sl] master.scale SL C     | Master alpha [sl] master.alpha C
│    Lock frame [cb] master.locked (session) SL C | Debug console [cb] state.debugConsole (session) C
│    Minimap button [cb] global.minimap.shown SL C | Test mode [cb] state.testMode (session) C
│    [btn] Reset position | [btn] Reset all settings      (composer afterGroup, General.lua:215)
│    note: "Reset position moves the selected window…"     (General.lua afterMaster)
├─ Tab "Behavior"                              Schema.lua:1247-1257
│    Merge pets into their owner [cb] data.mergePets | Refresh interval [sl] data.throttle
├─ (group "Export" — all 4 hidden, never a tab) Schema.lua:1285-1316
│    export.metric, export.channel, export.whisperTo, export.lines
└─ Tab "Statistic colors"                      Schema.lua:1362 (generated loop)
     Damage [sw] statColors.DamageDone | Healing [sw] statColors.HealingDone
     Absorbs [sw] statColors.Absorbs   | Interrupts [sw] statColors.Interrupts
     Dispels [sw] statColors.Dispels   | Damage Taken [sw] statColors.DamageTaken
     Avoidable Damage [sw] statColors.AvoidableDamageTaken | Deaths [sw] statColors.Deaths
     note: "These colors are worn wherever …"             (General.lua:238)

Windows page                                   settings/Windows.lua:479 (CreatePanel), :489
├─ Band: Active window [dd]  (session pointer) settings/Windows.lua:223 (H.WindowBanner → PageBanner)
└─ Nav rail (order OptionsSetup.lua:116; drawn OptionsSetup.lua:613)
   ├─ General   (Windows.lua:493; strip Windows.lua:457)
   │  └─ Tab "General"
   │     ├─ Section "Window"                    Windows.lua:464
   │     │    Window name [eb] window.name (full width)             Windows.lua:352 / Schema.lua:178
   │     │    [btn] New window | [btn] Duplicate window             Windows.lua:415
   │     │    [btn] Delete window                                   Windows.lua:425
   │     └─ Section "Copy settings from"        Windows.lua:466
   │          Source window [dd] | Settings to copy [dd]            Windows.lua:373/396
   │          [btn] Copy                                            Windows.lua:443
   ├─ Frame     (Frame.lua:25)
   │  ├─ Tab "General"                          Schema.lua:225-300
   │  │   ├─ Sub "Window":   Lock window [cb] window.frame.locked | Keep on screen [cb] window.frame.clampToScreen
   │  │   └─ Sub "All surfaces":
   │  │        Color mode (all surfaces) [dd] window.colorMode | Bar texture (all surfaces) [media] window.barTexture
   │  │        Font (all surfaces) [media] window.font         | Font outline (all surfaces) [dd] window.fontOutline
   │  ├─ Tab "Size and position"                Schema.lua:305-340
   │  │    Width [sl] window.frame.width     | Height [sl] window.frame.height
   │  │    Scale [sl] window.frame.scale     | Opacity [sl] window.frame.alpha
   │  │    Frame strata [dd] window.frame.strata | Padding [sl] window.frame.padding
   │  ├─ Tab "Background and border"            Schema.lua:351-352 ← Schema_Compose.lua:842/865
   │  │   ├─ Sub "Background": Background color [sw] window.frame.backdropColor SL C | Background color mode [dd] window.frame.backdropColorMode
   │  │   └─ Sub "Border":     Border style [media] window.frame.borderStyle SL C | Border thickness [sl] window.frame.borderSize C
   │  │                        Border color [sw] window.frame.borderColor SL C | Border color mode [dd] window.frame.borderColorMode
   │  └─ Tab "Row"                              Schema.lua:367-424
   │       Maximum rows [sl] window.rows.maxRows | Row height [sl] window.rows.height
   │       Row spacing [sl] window.rows.spacing  | Growth direction [dd] window.rows.growthDirection
   │       Always show yourself [cb] window.rows.alwaysShowSelf | Highlight yourself [cb] window.rows.highlightSelf
   │       Highlight on mouseover [cb] window.rows.mouseoverHighlight | Alternating background [cb] window.rows.alternatingBackground
   ├─ Header    (Header.lua:33)
   │  ├─ Tab "Title bar"                        Schema.lua:464-545
   │  │   ├─ Sub "Layout":     Show title bar [cb] window.header.show | Alignment [dd] window.header.align
   │  │   │                    Header height [sl] window.header.height
   │  │   ├─ Sub "Background": Header background [sw] window.header.bgColor SL      (no companion: documented deviation)
   │  │   └─ Sub "Divider":    Show divider [cb] window.header.divider | Divider thickness [sl] window.header.dividerThickness
   │  │                        Divider color [sw] window.header.dividerColor SL | Divider color mode [dd] window.header.dividerColorMode
   │  ├─ Tab "Title text"                       Schema.lua:568 ← Schema_Compose.lua:900
   │  │    Font [media] window.header.font SL C | Font size [sl] window.header.size C
   │  │    Text color [sw] window.header.color SL C | Text color mode [dd] window.header.colorMode
   │  │    Font outline [dd] window.header.outline C | Text shadow [cb] window.header.shadow C
   │  ├─ Tab "Controls"                         Schema.lua:603-708
   │  │    Show segment [cb] window.frame.showSegmentText | ⓘShow export [cb] window.frame.showExport
   │  │    ⓘShow reset [cb] window.frame.showReset | ⓘShow segment picker [cb] window.frame.showSegment
   │  │    ⓘShow settings [cb] window.frame.showSettings | ⓘShow lock [cb] window.frame.showLock
   │  │    ⓘShow minimize [cb] window.frame.showMinimize | ⓘShow close [cb] window.frame.closeButton
   │  │    (hidden) window.frame.minimized, window.data.sessionType, .sessionID, .sortColumn, .sortMode, .sortAscending
   │  └─ Tab "Button style"                     Schema.lua:725-800
   │      ├─ Sub "Icon":    Reveal controls on hover [cb] window.frame.hoverReveal | Control size [sl] window.frame.controlSize
   │      ├─ Sub "Color":   Control color [sw] window.frame.controlColor SL | Control color mode [dd] window.frame.controlColorMode
   │      │                 Control hover color [sw] window.frame.controlHoverColor SL | Control hover color mode [dd] window.frame.controlHoverColorMode
   │      └─ Sub "Opacity": Control opacity [sl] window.frame.controlAlpha | Control hover opacity [sl] window.frame.controlHoverAlpha
   ├─ Bars      (Bars.lua:46)
   │  ├─ Tab "Bar"                              Schema.lua:820 ← Schema_Compose.lua:941
   │  │    Bar texture [media] window.bars.texture SL C | Bar opacity [sl] window.bars.alpha C
   │  │    Bar color [sw] window.bars.customColor SL C  | Bar color mode [dd] window.bars.colorMode
   │  │    Fill direction [dd] window.bars.fillDirection C | Animate bar fills [cb] window.bars.animate C
   │  ├─ Tab "Background"                       Schema.lua:822 ← Schema_Compose.lua:998
   │  │    Bar background color [sw] window.bars.bgColor SL C | Bar background color mode [dd] window.bars.bgColorMode
   │  │    Bar background opacity [sl] window.bars.bgAlpha C
   │  ├─ Tab "Border"                           Schema.lua:824 ← Schema_Compose.lua:1025
   │  │    Bar border [cb] window.bars.border SL C
   │  │    Border style [media] window.bars.borderStyle SL C | Border thickness [sl] window.bars.borderThickness C
   │  │    Border color [sw] window.bars.borderColor SL C   | Border color mode [dd] window.bars.borderColorMode
   │  ├─ Tab "Text content"                     Schema.lua:834-870
   │  │    Left text [dd] window.text.leftSlot | Right text [dd] window.text.rightSlot
   │  │    Number format [dd] window.text.numberFormat | Death timestamps [dd] window.text.deathTimeFormat
   │  │    Max name length [sl] window.text.maxNameLength
   │  ├─ Tab "Text style"                       Schema.lua:876 ← Schema_Compose.lua:1072
   │  │    Font [media] window.text.font SL C | Font size [sl] window.text.size C
   │  │    Text color [sw] window.text.color SL C | Text color mode [dd] window.text.colorMode
   │  │    Font outline [dd] window.text.outline C | Text shadow [cb] window.text.shadow C
   │  │    Text opacity [sl] window.text.alpha C
   │  └─ Tab "Icons"                            Schema.lua:881-896
   │       Show icon [cb] window.icons.showIcon | Icon position [dd] window.icons.position
   │       Icon size [sl] window.icons.size
   ├─ Tooltip   (Tooltip.lua:28)
   │  ├─ Tab "General"                          Schema.lua:910-950
   │  │    Tooltip anchor [dd] window.tooltip.anchor | Tooltip scale [sl] window.tooltip.scale
   │  │    Horizontal offset [sl] window.tooltip.offsetX | Vertical offset [sl] window.tooltip.offsetY
   │  │    Hide tooltips in combat [cb] window.tooltip.hideInCombat
   │  ├─ Tab "Bar"                              Schema.lua:964 ← Schema_Compose.lua:1119
   │  │    Bar texture [media] window.tooltip.barTexture SL C | Bar opacity [sl] window.tooltip.barAlpha C
   │  │    Bar color [sw] window.tooltip.barColor SL C | Bar color mode [dd] window.tooltip.barColorMode
   │  │    Bar spacing [sl] window.tooltip.barSpacing C
   │  ├─ Tab "Bar background"                   Schema.lua:970 ← Schema_Compose.lua:1162
   │  │    Bar background color [sw] window.tooltip.barBgColor SL C | Bar background color mode [dd] window.tooltip.barBgColorMode
   │  │    Bar background opacity [sl] window.tooltip.barBgAlpha C
   │  ├─ Tab "Bar border"                       Schema.lua:976 ← Schema_Compose.lua:1191
   │  │    Bar border style [media] window.tooltip.barBorderStyle SL C | Bar border thickness [sl] window.tooltip.barBorderSize C
   │  │    Bar border color [sw] window.tooltip.barBorderColor SL C | Bar border color mode [dd] window.tooltip.barBorderColorMode
   │  ├─ Tab "Text"                             Schema.lua:981 ← Schema_Compose.lua:1229
   │  │    Font [media] window.tooltip.font SL C | Font size [sl] window.tooltip.fontSize C
   │  │    Text color [sw] window.tooltip.textColor SL C | Text color mode [dd] window.tooltip.colorMode
   │  │    Font outline [dd] window.tooltip.fontOutline C | Text shadow [cb] window.tooltip.fontShadow C
   │  └─ Tab "Contents"                         Schema.lua:984-1054
   │       Show spell breakdown [cb] window.tooltip.showSpells | Maximum spells [sl] window.tooltip.maxSpells
   │       Show targets [cb] window.tooltip.showTargets | Maximum targets [sl] window.tooltip.maxTargets
   │       Name the killer [cb] window.tooltip.showDeathCaster | Name the killing blow [cb] window.tooltip.showDeathSpell
   │       Summarize on the name [cb] window.tooltip.showAllStatsOnName
   ├─ Visibility (Visibility.lua:47)
   │  ├─ Tab "Where to show this window"        Schema.lua:1063-1104
   │  │    Dungeons [cb] .dungeon | Raids [cb] .raid | Arenas [cb] .arena | Battlegrounds [cb] .battleground
   │  │    Delves [cb] .delve | Scenarios [cb] .scenario | Open world [cb] .world      (all window.visibility.*)
   │  ├─ Tab "When to hide this window"         Schema.lua:1108-1157
   │  │    Hide when solo .hideWhenSolo | Hide in vehicles .hideInVehicle | Hide when mounted .hideWhenMounted
   │  │    Hide when skyriding .hideWhenSkyriding | Hide on flight paths .hideOnTaxi
   │  │    Hide in player housing .hideInHousing | Hide in pet battles .hideInPetBattle | Hide while dead .hideWhenDead
   │  └─ Tab "Combat"                           Schema.lua:1163-1172
   │       Hide in combat [cb] window.visibility.hideInCombat | Hide out of combat [cb] window.visibility.hideOutOfCombat
   └─ Columns   (Columns.lua:366; strip Columns.lua:322)
      ├─ Tab "Columns"   — note text + block editor (one block per stat; tick + drag)   Columns.lua:274
      │                    backing row window.columns (hidden)                         Schema_Paths.lua:580
      ├─ Tab "Header text"                      Schema.lua:1189 ← Schema_Compose.lua:1276
      │    Font [media] window.columnHeader.font SL C | Font size [sl] window.columnHeader.size C
      │    Text color [sw] window.columnHeader.color SL C | Text color mode [dd] window.columnHeader.colorMode
      │    Font outline [dd] window.columnHeader.outline C | Text shadow [cb] window.columnHeader.shadow C
      └─ Tab "Header background"                Schema.lua:1190 ← Schema_Compose.lua:1321
           Background color [sw] window.columnHeader.bgColor SL C | Background color mode [dd] window.columnHeader.bgColorMode

Profiles page — AceDBOptions via AceConfigDialog (no strip; options-ui-§3/§13 exemption)   settings/Profiles.lua:82
```

## Problems

| id | file:line | problem |
|---|---|---|
| MUL-P01 | settings/Schema.lua:225-300 | **Frame > General mixes two unrelated subjects.** The Window pair (Lock window, Keep on screen) is about where the window may sit. The All surfaces quartet styles bars, headers, the tooltip and the column header. Placing a window means going to Frame > General for the lock and Frame > Size and position for size and strata, so one task needs two tabs. |
| MUL-P02 | settings/Schema.lua:305-340 | **Size and position holds things that are neither size nor position** (Opacity, Frame strata), and it does *not* hold the two controls that are about position (Lock window, Keep on screen; see P01). Six rows with no subgroup, in an order that does not follow the subject: Frame strata pairs with Padding. |
| MUL-P03 | settings/Schema.lua:367-424 | **Frame > Row is a mixed tab with no subsection headings.** It has four geometry controls (slider, slider, slider, dropdown) and then four highlight/visibility checkboxes. options-ui-§7 requires a mixed tab to say where one kind stops. The pairing is also off: *Maximum rows* sits beside *Row height* and *Row spacing* beside *Growth direction*, when the two pixel dials (height, spacing) belong together, and so do count and direction. |
| MUL-P04 | settings/Schema.lua:369 | **Tab label "Row" is singular** while every sibling is plural (Bars, Icons, Columns, Controls), and the Copy dropdown already calls the same group "Rows" (`settings/Windows.lua:156`). |
| MUL-P05 | settings/Schema.lua:421 (desc) | **Stale cross-reference.** The *Alternating background* tooltip says "Sits behind the bar background **above**", but the bar background is on another rail entry (Windows > Bars > Background), not above it. The text dates from when Rows lived on the Bars page. |
| MUL-P06 | settings/Bars.lua:3-13 | **Stale file header.** It says the Bars entry holds "seven groups … the row (how tall, how many …)" and that "THE ROWS, TEXT AND ICONS PAGES ALL FOLDED IN HERE". Rows are on Frame now. A reader of the code gets the wrong map. |
| MUL-P07 | settings/Schema.lua:469 | **Alignment is in the wrong tab.** Its tooltip says "Where the header text sits horizontally": it is a property of the *text*, but it sits on Title bar > Layout, away from the Title text tab where the font is set. |
| MUL-P08 | settings/Schema_Compose.lua:919 | **Wrong tooltip on Header > Title text > Font.** It reads "Font used for every number in the grid. A monospace font such as JetBrains Mono … the default matches the window header." That text is copied from the cell-text font (`:1097`) and describes a different surface. |
| MUL-P09 | settings/Schema_Compose.lua:922 | *Text color* on Title text has the tooltip "Color of the header's own lines", which is vague ("lines" means the title and session text). |
| MUL-P10 | settings/Schema.lua:603-800 | **Header controls are split over two tabs.** Controls says which buttons are shown, and Button style says how big they are, what color, and how they fade. Restyling the header buttons is one task and today needs two tabs. Each tab is short (8 toggles; 8 style rows). |
| MUL-P11 | settings/Schema.lua:603 | **"Show segment" next to "Show segment picker" is confusing.** The first shows the *name of the fight* (text) and the second shows a *button*. Only the second carries an icon, which reinforces the wrong reading that they are two versions of one control. |
| MUL-P12 | settings/Schema.lua:820-824 | **Bars has three tabs for one surface.** Bar, Background and Border are the three layers of one cell bar, and comparing the fill against its background tint (the usual tuning loop) means clicking between tabs. The entry has six tabs, the most on the page, and the strip may wrap (`docs/settings-panel.md` "The strip wraps"). Frame already shows the merged form ("Background and border", two subgroups). |
| MUL-P13 | settings/Schema.lua:834-876 | **Cell text is split into Text content and Text style.** "What the cell says" and "how it is written" are one subject, the cell text, and each tab is short. |
| MUL-P14 | settings/Schema.lua:854 | **Death timestamps is in the wrong place.** It sits on Bars > Text content, but no cell reads it: `modules/Tooltip_Builders.lua:715` (Deaths tooltip) and `modules/DrillDown.lua:230` (the window's death list) do. Its two siblings, *Name the killer* and *Name the killing blow*, are on Tooltip > Contents, another rail entry. |
| MUL-P15 | settings/Schema.lua:964-976 | **Tooltip has the same three-way bar split as Bars** (Bar, Bar background, Bar border), giving six tabs on this entry too. |
| MUL-P16 | settings/Schema.lua:964 vs :820 | **Inconsistent labels across the two bar blocks.** Bars > Border says *Border style / Border thickness / Border color / Border color mode*, while Tooltip > Bar border says *Bar border style / Bar border thickness / Bar border color / Bar border color mode*. The same composer is used for the same concept with two wordings. |
| MUL-P17 | settings/Schema_Compose.lua:1136 | **"Bar spacing" in the tooltip is really line spacing.** Its tooltip says "Gap in pixels between one tooltip line and the next". |
| MUL-P18 | settings/Schema.lua:984-1054 | **Tooltip > Contents mixes three tooltips with no headings**: the cell breakdown (spells, targets), the Deaths list (killer, killing blow) and the name tooltip (summarize). The label *Summarize on the name* does not say what it shows. |
| MUL-P19 | settings/Schema.lua:910 | **Too many tabs named "General".** The Windows page alone has the rail entry *General*, Frame's first tab *General* and Tooltip's first tab *General*, and the settings tree has a *General* page as well. "Go to General" has four meanings. The rail entry is fixed (options-ui-§14), and the two inner tabs are not. |
| MUL-P20 | settings/Schema.lua:1063-1172 | **Visibility is three tabs for one question.** "Why is my window hidden?" needs all 17 checkboxes, and the entry's own file header says so ("seventeen checkboxes to read before you can tell which one took it away", `settings/Visibility.lua:20-22`). *Combat* is a two-row tab. The tab labels are sentences ("Where to show this window") that repeat the entry's subject. |
| MUL-P21 | settings/Columns.lua:309-311 | **Column header styling is split over two tabs** (Header text, Header background), and the labels are ambiguous on a page that also has a Header rail entry. "Header text" could mean the title bar's text, which is Header > Title text. |
| MUL-P22 | settings/Windows.lua:410-433 | **"New window" sits on the General entry and not in the band.** options-ui-§14: "the band MUST carry the identity controls — the picker, and the create control where the page has one". `O.PageBanner` has an `action` slot for this (`libs/LibKa0s/OptionsTabs.lua:45`, minor 4). |
| MUL-P23 | settings/Windows.lua:388, :444 | **The Copy tooltips say "Choose which group of settings to copy below"**, but the group dropdown is *beside* the source picker and the Copy button is the thing below. The Copy button reuses the source picker's tooltip word for word. |
| MUL-P24 | settings/Windows.lua:153-164 | **The "Settings to copy" labels do not match the panel.** They name config subtrees, not the rail. *Frame* copies `window.frame.*`, which includes every header button toggle and style (edited on Header > Controls / Button style) plus lock, clamp and strata. *Header* copies only the title bar and its text. *Rows*, *Text* and *Data* name no rail entry. *Data* is the hidden sort and segment state. A player who picks "Header" to copy their header buttons gets none of them. The order (frame, header, rows, …) does not follow the rail either. |
| MUL-P25 | settings/General.lua:249 | **General page tab order with the planned Keybindings tab.** Behavior is a one-line tab (two rows). Adding Keybindings gives four tabs, and the order should be decided once for all seven windowed addons (see Cross-addon notes). |
| MUL-P26 | settings/General.lua:238 | **The Statistic colors footnote names tab paths** ("Windows > Bars", "Windows > Bars > Text style", "Windows > Columns") that any tab change will invalidate. Today they are right. |
| MUL-P27 | settings/Schema_Compose.lua (bars colorMode desc) | **No route from Per-statistic to the palette.** *Bar color mode*, *Bar background color mode*, *Text color mode* (cells) and *Text color mode* (column header) offer Per-statistic, but none of their tooltips says the palette is edited on General > Statistic colors, another page. |
| MUL-P28 | settings/Schema.lua:331-334 | *Frame strata* tooltip: "Which layer the window sits in relative to the rest of your interface" does not say what the four values mean or that Dialog covers the addon's own dialogs (see the strata analysis, MUL-S03). |
| MUL-P29 | settings/Schema.lua:1039-1048 | **"Name the killer" / "Name the killing blow" are ambiguous.** A killing blow is an event. The row adds the *spell*, and its tooltip says so. |
| MUL-P30 | docs/settings-panel.md:62-76 | The panel doc's per-entry tab tables must be rewritten with any change here. Doc drift, not a UI defect. |
| MUL-P31 | settings/Schema.lua:621 (desc) vs modules/Window.lua:640-660 | **Stale tooltip on *Show segment picker*.** It ends "The session line stays clickable either way", but the session line takes no mouse: it was a Button carrying the segment dropdown, and that click target was removed on purpose (Window.lua:646-656). The picker button is now the only way to the menu, so the tooltip promises a fallback that does not exist. |
| MUL-P32 | settings/Schema_Compose.lua:1031-1034 | **The Bars border toggle is labelled "Bar border"**, while options-ui-§16 calls a border group's leading toggle *Show border*, and every other on/off row on the page starts with "Show" (Show icon, Show title bar, Show divider). Under a "Border" subgroup heading (L10) the label would read "Border / Bar border". |
| MUL-P33 | settings/Schema.lua:870 | **"Max name length" is the only abbreviated "Maximum"**, next to *Maximum rows*, *Maximum spells* and *Maximum targets*. |
| MUL-P34 | settings/Schema.lua:725-733 | **Sub "Icon" holds *Reveal controls on hover*,** which is not about the icon. It fades the controls (its tooltip: "Fade every control except the one under the pointer"), so it belongs with *Control opacity* / *Control hover opacity*, the two values that fade uses. |
| MUL-P35 | settings/Schema.lua:465-493 | **Title bar tab mixes "title bar" and "header" for one strip:** *Show title bar* sits beside *Header height* and *Header background*. The rail entry is *Header* (it also holds the buttons), but this tab is the title bar and should use one word. |
| MUL-P36 | settings/Schema.lua:226-229; options-ui-§14 | **A per-window "unlock" is drawn off the General entry.** §14 lists "enable, unlock, copy, reset, delete" as acts on the instance whole that go in the band or on the `General` first entry, and "no page-wide control is drawn on any other tab". *Lock window* is on Frame > General. Whether a stored per-window lock is such an act is not spelled out (see Upstream 6); the header's Lock button toggles the same path. |
| MUL-P37 | settings/Schema_Compose.lua:737, :741, :757; settings/Schema.lua:228-229, :493 | **Tooltips that name panel paths** ("Windows > Frame", "the General page", "under Windows > Columns"). Any move in this file must update them, as P26 does for the Statistic colors note. |

## Proposed changes

Every change keeps `path`, `default`, value set, range and behavior. Moving a row changes only its
`group` / `subgroup` (and `page`, only in L09). A `group` is not a stored path (`docs/settings-panel.md:261`).

| id | change | reason | confidence | fixes |
|---|---|---|---|---|
| MUL-L01 | Frame: move **Lock window** (`window.frame.locked`) and **Keep on screen** (`window.frame.clampToScreen`) from Tab General > Sub "Window" to Tab "Size and position", as a new Sub **"Placement"** after a new Sub **"Geometry"**. Placement order: Lock window \| Keep on screen, then Frame strata (moved from the Geometry rows). | Everything about where the window sits and whether it can move ends up on one tab, so placing a window is one visit instead of two. | 80% | P01, P02 |
| MUL-L02 | Frame > Size and position: give the existing rows Sub **"Geometry"**, ordered Width \| Height, Scale \| Opacity, Padding. Frame strata moves to Placement (L01). | Scale \| Opacity then read like Master scale \| Master alpha on General, the same pairing in both places (options-ui-§15 order). Strata is layering, not geometry. | 70% | P02 |
| MUL-L03 | Frame: rename the first tab from **General** to **Quick style**. After L01 it holds only Sub "All surfaces" (the four broadcast rows, unchanged), and moves to the **second** position, after Size and position. | The tab now holds one subject, and the name says what it does instead of a fourth "General". It cannot be called "All surfaces": options-ui-§7 forbids a subgroup repeating its tab's name, and §16's broadcast exemption *requires* the "All surfaces" subgroup heading (see Upstream). Second, not last: the retired end-of-strip tab was undiscoverable (`settings/Schema.lua:198-203`), and second is still one click from opening. | 50% | P01, P19 |
| MUL-L04 | Frame: rename tab **Row** to **Rows**. Split it into Sub **"Grid"** (Row height \| Row spacing, Maximum rows \| Growth direction, Always show yourself) and Sub **"Highlighting"** (Highlight yourself \| Highlight on mouseover, Alternating background). | §7 headings for a mixed tab; the two pixel dials paired; plural like its siblings and like the Copy label. | 65% | P03, P04 |
| MUL-L05 | Reword the *Alternating background* tooltip: "…Sits behind each cell's bar background (Windows > Bars > Bar style), so a strong tint there will hide it." Update the `settings/Bars.lua:3-13` header comment so it no longer claims Rows. | Fixes a stale pointer and stale code comments. | 95% | P05, P06 |
| MUL-L06 | Header: move **Alignment** (`window.header.align`) from Title bar > Layout to the end of Tab **Title text**, after the composed font block (`startsLine`), and relabel it **Text alignment**. Title bar > Layout becomes Show title bar \| Header height. | It is a property of the text, placed with the font. Appending after the block is what §16 permits ("MAY append further rows of the same kind after the block"). | 75% | P07 |
| MUL-L07 | Fix tooltips: Title text **Font** → "Font for the window's title and the fight name beside it." **Text color** → "Color of the window's title and the fight name beside it." | The current text describes the grid font. "Fight name" is the term L08 gives the player for that line, so one word is used for it everywhere. | 95% | P08, P09 |
| MUL-L08 | Header: merge **Controls** and **Button style** into one tab **Controls**. Subs in order: **"Shown"** (the 8 toggles, strip order kept), **"Icon"**, **"Color"**, **"Opacity"** (existing rows and order). The 6 hidden rows stay in the group. Relabel **Show segment** → **Show fight name**. | Choosing and styling the buttons becomes one tab (16 visible rows, about 9 lines). The relabel separates the text from the picker button. Header drops from 4 tabs to 3. | 70% (merge) / 80% (relabel) | P10, P11 |
| MUL-L09 | Move **Death timestamps** (`window.text.deathTimeFormat`) from Bars > Text content to Tooltip > Contents > Sub "Deaths", first, on its own line. Append to its tooltip: "Also used by the death list in the window's breakdown." Its `page` changes `bars`→`tooltip`. Side effects: the Defaults button that resets it becomes Tooltip's, `/mm list` groups it under tooltip, and the `CONFIG_CHANGED` section changes (no reactor reads `section`; verified by grep: `modules/Window_Lifecycle.lua:134` ignores `section`, `modules/Format.lua:678` invalidates on any change). Copy "Text" still carries it, because the path is `window.text.*`, and Copy "Tooltip" does **not**. That mismatch is the cost of this move, and L19's label must say so. | All death-line display controls end up in one place, beside the two death switches. Lowered from 65%: moving a row across `page` shifts its Defaults button, its `/mm list` group and its Copy group apart, which the brief's "just the layout" tolerates but a player who copies "Tooltip" will not expect. | 55% | P14 |
| MUL-L10 | Bars: merge **Bar**, **Background** and **Border** into one tab **Bar style**, with Subs **"Fill"** (Bar texture \| Bar opacity, Bar color \| Bar color mode, Fill direction \| Animate bar fills), **"Background"** and **"Border"**. These are the three composer calls with `group`/`subgroup` changed; composed order is untouched. | One tab per surface, matching Frame's "Background and border". §16 explicitly allows several groups on one tab with a heading per group. 14 rows, about 8 lines. | 75% | P12 |
| MUL-L11 | Bars: merge **Text content** and **Text style** into one tab **Text**, Subs **"Content"** (Left text \| Right text, Number format \| Max name length) and **"Style"** (the composed font block, then Text opacity). | The cell text becomes one tab. Bars goes from 6 tabs to 3 (Bar style, Text, Icons), which ends the wrap risk. | 70% | P13 |
| MUL-L12 | Tooltip: merge **Bar**, **Bar background** and **Bar border** into **Bar style**, with Subs **"Fill"**, **"Background"** and **"Border"**, the same shape as L10. Relabel the border rows **Border style / Border thickness / Border color / Border color mode** (as on Bars) and the background rows **Background color / Background color mode / Background opacity**. Relabel *Bar spacing* → **Line spacing**. | The two places a bar is styled now read alike. The subgroup heading carries the "Bar …" prefix, so the label does not need it. | 70% (merge) / 60% (labels) | P15, P16, P17 |
| MUL-L13 | Tooltip > Contents: move it to **second** position (after General). Add Subs **"Breakdown"** (Show spell breakdown \| Maximum spells, Show targets \| Maximum targets), **"Deaths"** (Death timestamps from L09, Name the killer \| Name the killing spell) and **"Player name"** (Show all statistics on name hover). Relabels: *Name the killing blow* → **Name the killing spell**; *Summarize on the name* → **Show all statistics on name hover**. | What the tooltip shows comes before how it looks. Three tooltips, three headings. The labels say what each does. Tooltip goes from 6 tabs to 4 (General, Contents, Bar style, Text). | 65% | P18, P29 |
| MUL-L15 | Visibility: merge the three tabs into one tab **Rules**, Subs **"Show in"** (the 7 contexts, order kept), **"Hide when"** (the 8 hide rules, order kept) and **"Combat"** (the 2 combat rows). | Every rule that can hide the window is on one screen (17 checkboxes, 9 lines), which is the debugging task the entry exists for. Three tabs become one, and short headings replace the sentence-length tab labels. | 80% | P20 |
| MUL-L16 | Columns: merge **Header text** and **Header background** into one tab **Column header**, Subs **"Text"** and **"Background"**. This is a bespoke-strip code change at `settings/Columns.lua:309-344`: one tab, `RenderRows` without `noHeadings`, rows carrying `subgroup`. | The column strip becomes one tab, and its name cannot be confused with the Header rail entry. Columns goes from 3 tabs to 2. | 70% | P21 |
| MUL-L17 | Windows band: move **New window** into the band through `PageBanner{ action = {…} }`. The General entry's Window section becomes Window name (full width), then Duplicate window \| Delete window. | options-ui-§14 MUST (create control in the band). It also puts Delete on the same line as Duplicate instead of alone. | 75% | P22 |
| MUL-L18 | Copy settings from: source tooltip → "The window to copy from. Pick what to copy beside it, then press Copy." Copy button tooltip → "Copy the chosen settings from the source window onto this one." | The current wording says "below", which is wrong, and the button repeats the dropdown's tooltip. | 90% | P23 |
| MUL-L19 | "Settings to copy" labels and order (labels only; keys and `WindowManager.COPY_GROUPS` untouched). Re-order the panel list as frame, rows, header, bars, text, icons, tooltip, visibility, columns, data. Labels: **Frame and header buttons**, **Rows**, **Title bar and title text**, **Bars**, **Bar text** (**Bar text and death timestamps** if L09 lands), **Icons**, **Tooltip**, **Visibility**, **Column list**, **Sort and segment**. Tooltip: "Copy every setting, or just one group. Groups follow where a setting is stored, so header buttons copy with the frame." The panel list in `settings/Windows.lua:153-164` is a separate table from `WindowManager.COPY_GROUPS`, so the reorder touches display only. | The labels match what is actually copied. (Out of scope: see the note under the table.) Lowered from 70%: the labels get longer and still need a tooltip to explain the storage split. | 65% | P24 |
| MUL-L20 | General page tab order: **Master controls**, **Keybindings** (planned), **Behavior**, **Statistic colors**. | Keybindings is the most-asked-for addon-wide control after the master set, and in the same slot in every windowed addon (Cross-addon). Behavior stays its own tab: its two rows are neither canonical nor about turning the addon up or down (`docs/settings-panel.md:176-182`). MultiMeters' tab holds one binding today, *Toggle meter windows* (`Bindings.xml:7`, label at `core/LauncherSetup.lua:167`); its key-binding header is `BINDING_HEADER_MULTIMETERS` = "Ka0s Multi Meters" under `category="ADDONS"`, which item 015 replaces with the addon's own category. | 60% | P25 |
| MUL-L21 | Append to each Per-statistic-capable color-mode tooltip: "Per-statistic colors are set on General > Statistic colors." Update the Statistic colors footnote's paths to the new tab names (Windows > Bars > Bar style / Text; Windows > Columns > Column header). | A route from the mode to the palette on the other page, and the footnote kept true after the renames. | 85% | P26, P27 |
| MUL-L22 | *Frame strata* tooltip → "Which layer the window draws in. Low and Medium sit with most of the interface; High sits above it; Dialog sits with dialogs and can cover this addon's own export window and confirmations." | Says what the values mean. The behavior is unchanged. | 80% | P28 |
| MUL-L23 | Rewrite `docs/settings-panel.md` (the page and entry tables, the subgroup list, "four tabs here do"), the rail entry tooltips (Frame: "…size, position, quick style, background, border and rows"), the file headers that describe tabs (`settings/Frame.lua:3`, `settings/Columns.lua:296-304`, and `settings/Schema.lua:190-203`, which argues for the Frame tab order L03 changes), and every tooltip that names a panel path (P37: `Schema_Compose.lua:737/741/757`, `Schema.lua:228-229/493`). `tests/test_columns.lua` pins the three Columns tabs and must move with L16. | Keeps the docs, the tooltips and the tests true. | 95% | P30, P37 |
| MUL-L25 | Header > Title bar: relabel **Header height** → **Title bar height** and **Header background** → **Title bar background** (keys untouched). | The tab, its toggle and its rows then say one name for one strip. "Header" stays the rail entry's name for the strip plus its buttons. | 55% | P35 |
| MUL-L26 | Bars > Border: relabel the toggle **Bar border** → **Show border** (`labels.borderShow` in the composer call, `settings/Schema_Compose.lua:1034`). | options-ui-§16's own name for the group's leading toggle, and the "Show …" form every other on/off row on the page uses. | 65% | P32 |
| MUL-L27 | Bars > Text: relabel **Max name length** → **Maximum name length**. | Matches Maximum rows / spells / targets. | 75% | P33 |
| MUL-L28 | Header > Controls (after L08): move **Reveal controls on hover** from Sub "Icon" to the head of Sub "Opacity" (own line, `startsLine`), and rename Sub "Icon" → **"Size"** (Control size alone). | The fade toggle sits with the two opacities it switches between. Costs a one-row subgroup. | 50% | P34 |
| MUL-L29 | *Show segment picker* tooltip → "Choose which fight this window shows. The fight name beside the buttons is turned on and off by Show fight name." | Removes the promise of a clickable session line that no longer exists. | 90% | P31 |
| MUL-L30 | Move **Lock window** (`window.frame.locked`) from Frame to the Windows > **General** entry, Section "Window", on its own line under Window name. If taken, L01's Sub "Placement" holds Keep on screen \| Frame strata. Bespoke: the General entry is hand-drawn (`settings/Windows.lua:458-469`), so the row is rendered there with `RenderRows`, its `page` becomes `windows`, and the General entry's Defaults (today "nothing to restore", `Windows.lua:496`) would then reset it. Update the Master *Lock frame* tooltip, which points to "Windows > Frame". | options-ui-§14 lists *unlock* among the acts on the instance whole, which go in the band or on the `General` first entry and nowhere else. The page also opens on that entry. Against it: the lock is a stored per-window setting, and the standard does not say whether that makes it an act (Upstream 6). Pick L30 or L01's lock half, not both. | 45% | P36 |

**Out of scope, but found while checking L19 (behavior, not layout; file separately).** `WindowManager`'s
copy never carries `window.columnHeader.*`, not even for "Everything". `groupsToCopy`
(`modules/WindowManager.lua:460`) iterates `COPY_GROUPS` only (`:65-68`), and `columnHeader` is not in it,
so the column-header font, colors and background stay the target's. The four window-level broadcast rows
(`window.colorMode`, `.barTexture`, `.font`, `.fontOutline`) are not copied either, but that does no harm:
they store only what was last broadcast and nothing reads them (`settings/Schema.lua:262-268`). The surfaces
they wrote are copied with their own groups.

**Totals.** 30 tabs become 22 (Keybindings included), and the Windows rail goes from 27 tabs to 18. No row is
added or removed.

### Considered and rejected

| id | change | why rejected | confidence |
|---|---|---|---|
| MUL-L14 | Tooltip: rename tab **General** → **Placement**. | No name fits all five rows (*Hide tooltips in combat* is not placement). "Placement" would also collide with L01's Frame subgroup of the same name, on the same page, for a different subject. "General" as an entry's first tab is the collection's convention. The P19 overload is real but mild here. | 35% |
| MUL-L24 | Fold **Behavior** (Merge pets, Refresh interval) into Master controls through the composer's `extra` slot. | §15's `extra` is for controls that govern the addon "the way the canonical rows do", and the addon's own doc argues these do not. With Keybindings arriving, the General page has four tabs either way. | 25% |
| — | Rename the Frame first tab **All surfaces** (instead of L03's "Quick style"). | options-ui-§16 requires the broadcast rows under a subgroup whose heading names the scope, and §7 forbids a subgroup repeating its tab's name. Raised upstream (1) instead of violating either. | 20% |
| — | Merge Header > Title bar and Title text into one tab. | 16 visible rows over four subgroups, one of them a composed font block. The title bar's divider and background are a different surface from the text, and the merge would make the longest tab on the page for one fewer click. | 30% |
| — | Merge Visibility's "Combat" pair into Sub "Hide when". | They are the one pair that can contradict each other (both ticked hides always). A heading of their own keeps that visible. | 30% |

## Proposed map

```
General page
├─ Tab "Master controls"   (unchanged — options-ui-§15 canonical set + reset pair + note)
├─ Tab "Keybindings"       (planned item 015 — Toggle meter windows, synced with Blizzard Key Bindings)
├─ Tab "Behavior"          Merge pets into their owner | Refresh interval
├─ (hidden group "Export"  export.metric, .channel, .whisperTo, .lines)
└─ Tab "Statistic colors"  8 swatches (unchanged) + footnote with updated paths

Windows page
├─ Band: Active window [dd]  ·  [btn] New window (PageBanner action)            L17
└─ Rail
   ├─ General
   │  └─ Tab "General"
   │     ├─ Section "Window":  Window name [eb] (full width)   [+ Lock window on its own line, only if L30 is taken]
   │     │                     [btn] Duplicate window | [btn] Delete window
   │     └─ Section "Copy settings from": Source window [dd] | Settings to copy [dd] (relabeled, rail order)   L18 L19
   │                                      [btn] Copy
   ├─ Frame
   │  ├─ Tab "Size and position"
   │  │   ├─ Sub "Geometry":  Width | Height ; Scale | Opacity ; Padding                                   L02
   │  │   └─ Sub "Placement": Lock window | Keep on screen ; Frame strata (tooltip reworded)              L01 L22
   │  ├─ Tab "Quick style"
   │  │   └─ Sub "All surfaces": Color mode (all surfaces) | Bar texture (all surfaces) ;
   │  │                          Font (all surfaces) | Font outline (all surfaces)                         L03
   │  ├─ Tab "Background and border"   (unchanged: Sub Background, Sub Border)
   │  └─ Tab "Rows"                                                                                    L04
   │      ├─ Sub "Grid":         Row height | Row spacing ; Maximum rows | Growth direction ; Always show yourself
   │      └─ Sub "Highlighting": Highlight yourself | Highlight on mouseover ; Alternating background (tooltip fixed)  L05
   ├─ Header
   │  ├─ Tab "Title bar"
   │  │   ├─ Sub "Layout":     Show title bar | Title bar height                                      L06 L25
   │  │   ├─ Sub "Background": Title bar background                                                  L25
   │  │   └─ Sub "Divider":    Show divider | Divider thickness ; Divider color | Divider color mode
   │  ├─ Tab "Title text"      Font | Font size ; Text color | Text color mode ; Font outline | Text shadow ;
   │  │                        Text alignment (moved, SL)                                             L06 L07
   │  └─ Tab "Controls"                                                                               L08
   │      ├─ Sub "Shown":   Show fight name | Show export ; Show reset | Show segment picker (tooltip fixed, L29) ;
   │      │                 Show settings | Show lock ; Show minimize | Show close     (+6 hidden rows)
   │      ├─ Sub "Size":    Control size                                                            L28
   │      ├─ Sub "Color":   Control color | Control color mode ; Control hover color | Control hover color mode
   │      └─ Sub "Opacity": Reveal controls on hover (SL) ; Control opacity | Control hover opacity       L28
   ├─ Bars
   │  ├─ Tab "Bar style"                                                                               L10
   │  │   ├─ Sub "Fill":       Bar texture | Bar opacity ; Bar color | Bar color mode ; Fill direction | Animate bar fills
   │  │   ├─ Sub "Background": Bar background color | Bar background color mode ; Bar background opacity
   │  │   └─ Sub "Border":     Show border ; Border style | Border thickness ; Border color | Border color mode   L26
   │  ├─ Tab "Text"                                                                                    L11
   │  │   ├─ Sub "Content": Left text | Right text ; Number format | Maximum name length              L27
   │  │   └─ Sub "Style":   Font | Font size ; Text color | Text color mode ; Font outline | Text shadow ; Text opacity
   │  └─ Tab "Icons"           Show icon | Icon position ; Icon size
   ├─ Tooltip
   │  ├─ Tab "General"         Tooltip anchor | Tooltip scale ; Horizontal offset | Vertical offset ; Hide tooltips in combat   (unchanged; L14 rejected)
   │  ├─ Tab "Contents"                                                                                L13
   │  │   ├─ Sub "Breakdown":   Show spell breakdown | Maximum spells ; Show targets | Maximum targets
   │  │   ├─ Sub "Deaths":      Death timestamps (moved, SL) ; Name the killer | Name the killing spell    L09
   │  │   └─ Sub "Player name": Show all statistics on name hover
   │  ├─ Tab "Bar style"                                                                               L12
   │  │   ├─ Sub "Fill":       Bar texture | Bar opacity ; Bar color | Bar color mode ; Line spacing
   │  │   ├─ Sub "Background": Background color | Background color mode ; Background opacity
   │  │   └─ Sub "Border":     Border style | Border thickness ; Border color | Border color mode
   │  └─ Tab "Text"            Font | Font size ; Text color | Text color mode ; Font outline | Text shadow
   ├─ Visibility
   │  └─ Tab "Rules"                                                                                   L15
   │      ├─ Sub "Show in":   Dungeons | Raids ; Arenas | Battlegrounds ; Delves | Scenarios ; Open world
   │      ├─ Sub "Hide when": Hide when solo | Hide in vehicles ; Hide when mounted | Hide when skyriding ;
   │      │                   Hide on flight paths | Hide in player housing ; Hide in pet battles | Hide while dead
   │      └─ Sub "Combat":    Hide in combat | Hide out of combat
   └─ Columns
      ├─ Tab "Columns"         note + block editor (unchanged)
      └─ Tab "Column header"                                                                           L16
          ├─ Sub "Text":       Font | Font size ; Text color | Text color mode ; Font outline | Text shadow
          └─ Sub "Background": Background color | Background color mode

Profiles page — unchanged
```

Counts after: 3 pages, 7 rail entries, 22 tabs (General 4, Windows 1+4+3+3+4+1+2 = 18), 170 schema rows
(159 visible, 11 hidden), nothing added or removed.

## Cross-addon notes / Upstream suggestions

**Cross-addon notes**

- **Keybindings tab slot.** All seven windowed addons should put it in the same place on the General page.
  The recommendation is directly after *Master controls*: it is the next thing a player looks for, and a
  fixed second slot is easy to learn.
- **Tab-per-composed-group vs merged.** MultiMeters' Frame merges background and border into one tab with
  subgroups, but its Bars and Tooltip give each composed group its own tab. Pick the merged form
  collection-wide: one tab per *surface*, one subgroup per §16 group, and name the merged tab
  "Bar style" wherever a fill, background and border are styled together.
- **Font-block labels drift.** MultiMeters overrides the composer's labels to *Text color / Font outline /
  Text shadow*, where the standard's table says *Font color / Font flags / Font shadow*. Check what the
  other addons show. §16's promise ("a player who has set a font in one Ka0s addon MUST find the same rows
  in the same order in the next one") is about rows, but players read labels.
- **Opacity vs alpha.** MultiMeters says *Opacity* everywhere except the canonical *Master alpha*.
- **"General" overload.** Any addon with a nav rail (AuraMaster Containers is the pattern MultiMeters
  copied) will have the rail's *General* plus a General page. Avoid naming inner tabs *General* as well.
- **Visibility rule pages.** Addons with per-instance show/hide rules should use one tab with *Show in /
  Hide when / Combat* subgroups, so "why is it hidden" is answered on one screen.
- **Copy-settings vocabulary.** If other addons have copy-from with group filters, the labels should name
  what the player sees, not storage subtrees.
- **"Max" vs "Maximum", "Header" vs "Title bar", "Show border".** Pick one spelling per concept
  collection-wide: *Maximum …* in full, *Show border* for a border group's toggle (as §16 names it), and one
  word for a window's top strip.
- **Stale cross-reference tooltips.** MultiMeters has five tooltips that name a panel path and one that
  describes a removed click target (P31, P37). Every addon touched by item 020 should grep its tooltips
  for `>` paths and "page" after the moves.

**Upstream suggestions (WowAddonStandards)**

1. **options-ui-§16 broadcast exemption vs §7.** The exemption requires the broadcast rows under their own
   subgroup whose heading names the scope, and §7 forbids a subgroup repeating its tab's name. Together they
   stop a tab holding only broadcasts from being called "All surfaces" (hence L03's "Quick style"). Allow
   the scope to be carried by the **tab label** when the tab holds nothing but broadcast rows.
2. **options-ui-§13/§16.** Add a SHOULD: on a page whose tabs are composed groups over one surface (bar
   fill, background, border), prefer **one tab per surface with a subgroup per group** to one tab per group.
   That keeps strips from wrapping. §16's last bullet already permits it; nothing yet prefers it.
3. **options-ui-§15.** Rename the canonical *Master alpha* to *Master opacity*. Every other row in the
   collection the player meets says opacity, and the rename is a label (`group`/label), not a stored path.
   This changes the canonical set, so it is an owner decision.
4. **options-ui-§15 / new.** Write down where the Keybindings tab goes on the General page (name and slot),
   so item 015 lands identically in all seven addons.
5. **options-ui-§14.** Name the `PageBanner{ action = … }` slot as the way to satisfy "the create control
   in the band". MultiMeters missed the MUST, probably because the escape paragraph lists "rename, copy-from
   … delete" and the reader assumes create goes with them.
6. **options-ui-§14.** Say whether a **stored per-instance lock** (MultiMeters' *Lock window*, toggled by a
   header button as well) is one of the "unlock" acts that must sit in the band or on the `General` entry,
   or a frame setting that may live with size and position. Today the text lists *unlock* among the acts,
   and MultiMeters keeps the lock on Frame. L30 and L01 are the two answers.

## Review

Independent review, 2026-10-24, against `../MultiMeters` at `master` (`fd3200a`). Every row of the
current map was checked against `settings/Schema.lua`, `settings/Schema_Compose.lua`, `settings/Windows.lua`,
`settings/Columns.lua`, `settings/General.lua` and the rail entry files. The map is accurate: tab counts
(30), row counts (170, 11 hidden), groups, subgroups and labels all match. No proposed change alters a
key, default, range or behaviour. L09 changes a row's `page`, which moves its Defaults button, `/mm list`
group and CONFIG_CHANGED section, and that is now stated with its cost.

What changed:

- **New problems P31-P37 and changes L25-L30.** The *Show segment picker* tooltip promises a clickable
  session line that was removed (P31/L29). *Bar border* should be *Show border*, the §16 name (P32/L26).
  *Max name length* is the only abbreviated "Maximum" (P33/L27). *Reveal controls on hover* sits under
  "Icon" but is an opacity toggle (P34/L28). The title bar tab mixes "header" and "title bar" (P35/L25).
  *Lock window* is a per-window "unlock" drawn off the General entry, a §14 question rather than a clear
  breach, so it is raised upstream (P36/L30/Upstream 6). Five tooltips name panel paths and must move with
  the layout (P37, folded into L23 with the file headers and `tests/test_columns.lua`).
- **Recalibrated.** L09 65→55% (Copy "Tooltip" would not carry the moved row, and Copy "Text" would). L19
  70→65%, with the shorter "Frame and header buttons" label and a death-timestamps variant if L09 lands.
- **Rejected (<40%).** L14 (35%: no name fits, and "Placement" would collide with L01's subgroup) and L24
  (25%) moved to a new "Considered and rejected" section with three other options considered.
- **Wording.** L07 now says "fight name" to match L08's relabel, so the player meets one term for that line.
- **Out-of-scope note corrected.** The copy gap is `window.columnHeader.*` only. The four broadcast rows
  are uncopied but unread, so nothing is lost.
- **L20** now records the one binding MultiMeters has and its current header and category.
- **Proposed map** updated for L25-L29, the unchanged Tooltip "General" tab, and the optional L30 row.
- **Cross-addon notes and Upstream**: added the naming-spelling and stale-tooltip notes, and Upstream 6.

