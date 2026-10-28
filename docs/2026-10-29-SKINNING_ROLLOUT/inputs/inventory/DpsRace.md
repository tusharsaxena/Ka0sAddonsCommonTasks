# DpsRace (DR) — skinning inventory

Read-only inventory, 2026-10-29, for items DR-RV and DR-01..DR-05 of `00_PLAN.md`. Repo
`../DpsRace` (checked-out branch `feat/2026-10-29-skinning-rollout` at master's head `e2cfb9b`, clean),
vendoring LibKa0s v1.77.0 plus `libs/LibKa0s/Toast.lua` copied in on its own (the same bytes as v1.79.0's
`Toast.lua`, apart from CRLF line endings). The library was read at v1.79.0 (Skin minor 6, SkinDefs minor 14,
SkinPaintExtras minor 4, OptionsCompose minor 12). Every `file:line` below is DpsRace's unless it names
LibKa0s.

## 0. How the code is shaped, and the seams to convert

DpsRace has two windows (the Race HUD and Results), two modal windows that open over Results (the ability
timeline and the gear view), a center-screen countdown, a toast, and six settings pages. Almost all of its
styling passes through a few helpers. Converting those helpers converts most of the call sites:

| Seam | Where | What it paints today | Converts to |
|---|---|---|---|
| `Style.Text(parent, font, color, justify)` | modules/Style.lua:71-77 | every label: a Blizzard font object, then an optional `SetTextColor` | Create the FontString, then call `S.Text(fs, role)`. Roles by `Style.FONT` key (Style.lua:30-46): TITLE→`title`, HEADER/SECTION/CHART→`heading`, TEXT/HEADING/NAME/FIGURE→`body`, CAPTION/EMPTY→`disabled`. A `color` argument becomes a token name, never an rgb triple. |
| `Style.GOLD` / `REST` / `TAB_IDLE` | Style.lua:50-54 | header gold; title-bar control rest gray; idle tab gray | `text.accent`/`title.text`, `icon.tint`, `tab.text` (all exact) |
| `Style.AddToStrip` / `PaintStrip` / `ControlButton` | Style.lua:131-206 | title-bar controls, gold under the pointer | rest `icon.tint`, hot `text.accent` read through `S.Color`; close control left to `S.CloseButton` (see doubtful D-9) |
| `Style.IconMarkup(name, fallback, color)` | Style.lua:86-90 | sort arrows and chevrons as `\|T` markup tinted gold | color from `S.Color("icon.arrow")` (GOLD, exact); markup rebuilt on `OnLooksChanged` (Results_Table.lua:632-633 and 1037-1038 build it once at file load) |
| `Style.AddTipLines` | Style.lua:116-123 | lines written onto GameTooltip, default 0.9 gray | `gtip.body` (exact 0.9) |
| `States.Button(parent, label, onClick, style)` | modules/Hud_States.lua:173-194 (styles :38-42, paint :143-150) | every flat button in both windows (also used by Results_Compare:309, Detail:563, Insights:654, Loadout:288, Runs:828, Usage:361-363) | `S.Button(b)` for normal, `S.Button(b, {primary=true})` for primary or selected, danger is gap DR-G2 |
| `panel()` / `Tbl.Panel(parent, bg, edge)` | Hud_States.lua:132-141; modules/Results_Table.lua:94-102 | flat 1px box, default fill {1,1,1,.03} and edge {1,1,1,.10} | `S.Card` / `S.Panel` (D-3); the amber variant is gap DR-G3 |
| `NS.ApplySkin` | core/CoreSetup.lua:88-89 | `Core.ApplySkin(f)`, no owner | `Core.ApplySkin(f, nil, addonName)` (equals `S.Shell`) |
| `NS.MakeCloseButton` | CoreSetup.lua:101-103 | already passes `addonName` | nothing to change; once the owner is registered it paints through `S.CloseButton` (Core minor 13) |
| `NS.HudAppearance.*` | modules/Hud_Appearance.lua:68-147 | HUD faces and bar textures by LSM name, plus colors | `S.Resolve("hud.font"/"bar.texture", stored, fromSkin)` (section 3) |
| `Charts.Host()` | modules/Results_InsightsCharts.lua:810-827 (defaults :87-106) | the Insights chart host: colors, fonts, palette | build `colors` from `S.ChartStyle()` and tokens, palette from `chart.series` (the values match exactly) |

## 1. Surfaces

The tokens named are SkinDefs.lua's schema names. "Exact" means Ka0s Default's value equals the value typed
today. "Near" means it does not, and the item goes to section 6.

### 1a. Race HUD window (modules/Hud.lua)

| # | Surface | Built | Typed today | Paints with |
|---|---|---|---|---|
| H1 | HUD shell | Hud.lua:466-480 (`CreateFrame ... BackdropTemplate`, `NS.ApplySkin(f)` :480) | Core.SKIN | `S.Shell(f)` via `ApplySkin(f, nil, owner)`; `win.bg`, `win.border`, `win.inner`, `title.bg` |
| H2 | Title, divider | Hud.lua:417-423 | GameFontNormal, gold once ApplySkin tints it | Shell paints `frame.title` (`title.text`, title font) and `frame.divider` (`divider`) |
| H3 | Title-bar controls (lock, settings, results) and close | Hud.lua:424-433; Style.lua:179-206 | `Style.REST` / `GOLD` | `icon.tint` / `text.accent`; close: `close.rest` / `close.hot` |
| H4 | Footer rule and two caption lines | Hud.lua:449-459 (rule :452 `0.24,0.24,0.27,0.85`) | literal rule; GameFontDisableSmall | `S.Divider(line)` → `divider` (exact); `S.Text(fs,"disabled")` |
| H5 | Test-mode strip | Hud.lua:540 via core/WidgetsSetup.lua:51-54 | `W.TestStrip`, no owner | pass `owner` → `S.Strip` → `strip.test` |
| H6 | Resize grip | Hud.lua:486 (`NS.Sizing.MakeResizable`) → Core.MakeResizable | library art | none (library; see D-12) |

### 1b. HUD bodies (modules/Hud_States.lua): idle, armed, running, stop, waiting, result

| # | Surface | Built | Typed today | Paints with |
|---|---|---|---|---|
| B1 | HUD palette `C` | Hud_States.lua:23-31 | text .93/.93/.95, dim .62/.62/.68, gold, amber 1/.72/.29, red 1/.32/.32, green .36/.86/.46, info .56/.72/1 | text→`text.body` (near, D-1); dim→`text.muted` (near, D-1); gold→`text.accent` (exact); red→`sem.statusBad` (exact); green/amber/info → gap DR-G4 |
| B2 | Flat buttons: presets, Custom, Arm, Stop Now, Cancel, New Race, Delete, links | :173-194, presets :447-450, Arm :464-465, rows :408/:418, :839-841, :1094-1097 | BUTTON_STYLES :38-42 (normal = `btn.*` exact: bg .1/.1/.12/.9, edge .24/.24/.27/.9, white, gold hover); FLAT backdrop :34 | `S.Button`; primary → `btnPrimary.*` (near, D-2); danger → DR-G2; disabled dimming :146-149 (D-2) |
| B3 | KPI boxes (Damage, DPS, captioned pairs) | :211-241 | `panel()` defaults PANEL_BG/EDGE :35; FONT.FIGURE value | `S.Card(f, {title=label})` (near, D-3); figure `S.Text(value,"body")`, recolored with the meaning token |
| B4 | Section captions and headings (Target, Damage profile, Spell breakdown) | :244-249, :763, :1082 | FONT.HEADER / SECTION gold | `S.Text(fs,"heading")` |
| B5 | Chips (late casts, grace, time, new best, vs best, ignored) | :260-326 (pooled; paint :306-309) | border = item color at .55, fill = item color at .08 | composed from the meaning token (`sem.*` / DR-G4) with `S.Color`; the per-alpha shape is D-4 |
| B6 | Target card and its amber badge | :345-360 (badge :352-355) | badge `{1,.72,.29,.08}` / `{1,.72,.29,.6}`, amber text | card → `S.Card`; badge → DR-G3 |
| B7 | Custom-length edit box | :451-457 | BackdropTemplate, FONT.TEXT | `S.EditBox(w.customBox, {padInput=false})` → `input.*` |
| B8 | Idle warning and refusal lines | :461, :468 | `C.amber` | DR-G4 (`sem.caution`) |
| B9 | Race clocks and STOP (monospace) | `bigText` :123-130; idle :513, running :736-743, stop :865 | `SetFont(FONT_MONO, size, "")` + C.text/red/green | running pair: `HudAppearance` (section 3); the idle clock (`BIG` 40) and the stop `STOP` (48) stay mono → `S.Token("font.mono")` resolved by LSM (exact: "JetBrains Mono"), colors are meaning (text/red) |
| B10 | Notes and sub-captions | :515, :519, :746-775, :870 | FONT.CAPTION / TEXT + C.dim | `S.Text(fs,"disabled")` / `"muted"` |
| B11 | Waiting body's hint box | :943-949 | panel `{1,.72,.29,.07}` / `{1,.72,.29,.35}`, text `{.95,.85,.67}` | DR-G3 |
| B12 | Result body's lost line | :1071 | C.red | `sem.statusBad` (exact) |
| B13 | Button and chip tooltips (GameTooltip lines) | :159-168 (gold body lines :166), :278-282 | white title, GOLD lines | `gtip.value` (white, exact) for the title; `gtip.title` (GOLD, exact) for the lines |

### 1c. HUD spell rows (modules/Hud_Breakdown.lua; also drawn in the Results detail)

| # | Surface | Built | Typed today | Paints with |
|---|---|---|---|---|
| R1 | Row bar (StatusBar) | :72-99 (texture and color :98-99 from `Appearance.Bar()`) | LSM "Solid" + indigo .29/.29/.45 @ .85 | `S.Resolve("bar.texture", stored, barTextureFromSkin)`; color stays the player's setting (section 3, D-6) |
| R2 | Track behind the bar | :76-78 | `TRACK_COLOR {1,1,1,.04}` :34 | `chart.track` {1,1,1,.06} (near) or `bar.bg` {0,0,0,.5} (far): D-5 |
| R3 | Stripe | :142-147 | WHITE8x8 + alpha `list.stripe(i)` (0.025 on even rows) | `S.ListRow(row,{stripe=even})` → `list.stripe` .03 (near, D-5) |
| R4 | Name, amount, pct text | :80-82 | Style.Text TEXT/CAPTION, then `Appearance.ApplyFont` (spellText block) | HUD font via section 3 |
| R5 | Spell icon | :73, :188 | spell art | rung 4: spell icon stays; edge: D-10 |

### 1d. Damage chart and pace bar (modules/Hud_Chart.lua; the HUD, the result card, the Results detail)

| # | Surface | Built | Typed today | Paints with |
|---|---|---|---|---|
| C1 | Plot background | :490-496, restyle :470-473 | `PLOT_BACKDROP` :85 + `appearance.chart.bgColor` {0,0,0,.35} | the player's swatch; a style color with no skin companion (D-6) |
| C2 | Columns (StatusBar) | :564-571 | `Appearance.Chart()` texture + color | `S.Resolve("bar.texture", …)` (section 3) |
| C3 | Best's pace diagonal | :87, :462 | `{.9,.9,.92,.4}` | `chart.marker` {.8,.8,.8,.6} (near, D-7) |
| C4 | Cooldown icons and their +n marks | :680-698 | `ICON_CROP` :92; `MARK_BG {0,0,0,.75}` :93 | icons rung 4; `MARK_BG` → `handle.bg` {0,0,0,.75} (exact) |
| C5 | Pace bar track, ahead and behind fills, tick | :790-819, restyle :866-868 | PACE_TRACK {1,1,1,.08}, AHEAD green@.85, BEHIND red@.85, TICK {1,1,1,.85}, WHITE8x8 | track → `chart.grid` {1,1,1,.07} (near, D-7); ahead/behind are gain/loss meaning → DR-G4 green / `sem.statusBad` red (exact rgb); the fill texture comes from `Appearance.Pace()` (section 3) |
| C6 | Chart title and note | :485-488 | Style.Text SECTION / CAPTION | `S.Text` heading / disabled |

### 1e. Countdown (modules/Countdown.lua) and the buzzer

| # | Surface | Built | Typed today | Paints with |
|---|---|---|---|---|
| K1 | Center-screen digits and glow | :131-150, frame :168 | Blizzard `Interface\Timer\BigTimerNumbers(Glow)` :40-41 | exception (section 4: the client's own start-timer art) |
| K2 | Fallback number | :157-163 | `SetFont(STANDARD_TEXT_FONT,110,"THICKOUTLINE")`, GOLD :46 | stays with K1 (D-11) |
| K3 | STOP raid warning | Hud.lua:166-168 | `RaidNotice_AddMessage(RaidWarningFrame…)` | exception (Blizzard shared frame) |

### 1f. New-best toast (modules/BestToast.lua, shell LibKa0s-Toast-1.0)

| # | Surface | Built | Typed today | Paints with |
|---|---|---|---|---|
| T1 | Toast shell and close | Toast.lua (library) via core/ToastSetup.lua:36-40 | `d.owner = addonName` already passed | follows the owner once it is registered (Toast.lua:216-218: `ApplySkin(f, nil, owner)`, `MakeCloseButton(…, owner)`) |
| T2 | Trophy icon | :130-136 | `ph:trophy` tinted `Tbl.COLORS.blue` {.40,.66,1} | rung-4 data hue (Status column's "spec best" blue), see section 4 |
| T3 | Title, detail, flags lines | :138-167 | Style.Text TITLE/TEXT; detail red/green :88-90; flags amber | `S.Text`; red `sem.statusBad`, green and amber DR-G4 |

### 1g. Results window (modules/Results.lua and its tabs)

| # | Surface | Built | Typed today | Paints with |
|---|---|---|---|---|
| W1 | Shell | Results.lua:286-299 (`NS.ApplySkin(f)` :299) | Core.SKIN | `S.Shell` |
| W2 | Title (gold), divider, view toggle, close | :185-204 | `Style.Text(…, C.gold)` | Shell `frame.title`, `divider`; controls as H3 |
| W3 | Tabs Runs / Insights | :168-182 (underline :177), paint :422 | GameFontNormal; gold label and underline when on, `TAB_IDLE` when off | `S.Tab(b)` + `S.SetTabSelection(b, on)` → `tab.onText`, `tab.text`, `tab.onLine` (all exact) |
| W4 | Tab-strip rule, footer rule, footer captions | :217-231 | `0.24,0.24,0.27,0.85` twice | `S.Divider` → `divider` (exact); `S.Text(fs,"disabled")` |
| W5 | Test-mode strip | :469 | `W.TestStrip`, no owner | owner → `strip.test` |
| W6 | Dim cover under the timeline | :596-607 | `SetColorTexture(0,0,0,COVER_ALPHA=.45)` :47 | `S.Cover(c.dim)` → `cover.dim` {0,0,0,.6} (near, D-8) |
| W7 | Row context menu (MenuUtil) and its red Delete entry | :766-781 (`\|cffff5555` :779) | Blizzard menu; literal escape | menu = exception; the escape → `sem.danger` (exact ff5555) as an escape built from the token |
| W8 | Delete confirmation | :786 `DPSRACE_DELETE_RUN` | StaticPopup | exception |

### 1h. Results table (modules/Results_Table.lua; the Runs list, the detail's lists, Compare)

| # | Surface | Built | Typed today | Paints with |
|---|---|---|---|---|
| L1 | Table palette `C` | :46-58 | as B1, plus blue .40/.66/1 and violet, orange, pink, slate | text, dim, gold, red as B1; blue and the four status hues are rung-4 data hues (section 4) |
| L2 | Header buttons, labels, sort arrows | :637-660 (label gold :640; tip :649-651), arrows :632-633 | FONT.HEADER gold; markup arrows tinted gold | `S.SortHeaderBar(t.header, {texts=…})` → `list.header.text` (exact GOLD); `list.header.bg` {1,1,1,.04} is new paint (D-5); arrows `icon.arrow` |
| L3 | Header rule | :754 | `0.24,0.24,0.27,0.85` | `S.Divider` (exact) |
| L4 | Pooled rows: stripe, hover, selection | :665-673, stripe :1050, `STRIPE_ALPHA .025` :37 | sel `{1,.82,0,.10}`, hover `{1,1,1,.04}` | `S.ListRow(row, state)` → `list.stripe` .03, `list.hover` {1,.82,0,.10}, `list.sel` {1,.82,0,.18}; all near (D-5) |
| L5 | Text cells and bar cells | :287-340 (bar :291-293, tint :430) | WHITE8x8 + `resultsTable.*Bar` style | text `S.Text`; bar `S.BarTexture(cell.bar, r,g,b,a)` with the resolved setting (section 3) |
| L6 | Status and category badges | :343-361 | edge = color @ .6, fill = color @ .08 | as B5 (D-4) |
| L7 | Class and spec icons | :113-140 (`CLASS_ATLAS` :44) | Blizzard atlas | rung 4 |
| L8 | Scroll bar (Slider) | :712-725 | thumb `{1,1,1,.25}` | `S.ScrollBar(bar, {thumb=thumb})` → `scroll.thumb` {.5,.5,.55,.85}, `scroll.track` (near, D-5) |
| L9 | Group rows: chevrons and gray count | :1037-1046 (`\|cff808080` :1044) | gold markup; literal gray escape | `icon.arrow`; count escape from `text.disabled` (.5, exact) |
| L10 | Side, spell and below tips (GameTooltip lines) | :236-273 | title C.gold | `gtip.title` (exact) |

### 1i. Runs tab (modules/Results_Runs.lua) and Insights tab (modules/Results_Insights.lua, Results_InsightsCharts.lua)

| # | Surface | Built | Typed today | Paints with |
|---|---|---|---|---|
| I1 | Filter bar: checkboxes | Runs :797-806; Insights :624-633 | `UICheckButtonTemplate` | `S.Checkbox(b)` (Ka0s Default draws its square box: a look change, D-13) |
| I2 | Filter dropdowns | Runs :819; Insights :646 (via WidgetsSetup.lua:28-35) | `W.Dropdown`, no owner | pass `owner` → `S.Dropdown`, `S.MenuFrame` |
| I3 | View buttons | Runs :828; Insights :654 | States.Button | as B2 |
| I4 | Bar rules | Runs :808-813; Insights :635-640, :690 | `0.24,0.24,0.27,0.85` | `S.Divider` (exact) |
| I5 | Insights sub-tabs | Insights :388-422 | gold underline, `TAB_IDLE` | as W3 |
| I6 | Insights charts: cards, bars, list panels, legend chips, dividers, axes | InsightsCharts :237-420, :764 | host colors :817-820 (bar = C.blue), fonts :822-825, `DEFAULT_PALETTE` :99-106 | `Charts.Host()` from tokens: body `text.body` (near .93→.9), value `text.value`, muted `text.muted`, heading `text.heading`, caption `text.disabled`, rule `section.rule` (exact), bar `chart.bar` (near: .40/.66/1 vs .40/.60/.95/.9, D-7), axis `chart.axis`, track `chart.track`; palette `chart.series` (exact); panel → `S.Panel`/`S.Card`; fonts via `S.Text` roles; the shrink-to-fit `SetFont` :405 keeps the skin's face |
| I7 | Scroll frames | Insights :666-667 | no bar art | none |

### 1j. Run detail (modules/Results_Detail.lua) and its parts

| # | Surface | Built | Typed today | Paints with |
|---|---|---|---|---|
| D1 | Collapsible section headers and gold arrow | :378-398 | arrow `SetVertexColor(Style.GOLD)` | `icon.arrow` (exact); heading `S.Text(…,"heading")` |
| D2 | KPI boxes (Damage, DPS, Meter DPS, Delta) | :432-461 | `Tbl.Panel`; colors green/dim | as B3 |
| D3 | Name, meta lines, spec badge | :456-470 (badge icon blue :469) | NAME white, meta dim; blue | `S.Text`; class color rung 4 (:713); blue rung 4 |
| D4 | Race strip: two segments, marks, legend | :481-520 | segments `{.07,.07,.1,1}` / `{1,1,1,.08}` :500-501; marks amber @.45, green @.8; legend RACE/CYAN/VIOLET :99-105 | segments → `S.Inset` (`input.bg` CTL_FILL, near: D-3); marks and legend are rung-4 data hues |
| D5 | Flags box | :530-541, paint :735-748 | panel `{1,.72,.29,.06}` / `{1,.72,.29,.35}`; FLAG_MAIN/FLAG_BODY :109-110; IGNORED :98 | DR-G3 |
| D6 | Note edit box | :546-554 | bg `.1,.1,.12,.9` (= `input.bg`), edge `1,.82,0,.9` (= `input.focus`, shown at rest too) | `S.EditBox(w.noteBox)`; the gold edge at rest becomes `input.border` (D-14) |
| D7 | Scroll pane panel | :645-652 | `Tbl.Panel(parent,{0,0,0,.15},{.24,.24,.27,.85})` | `S.Panel(frame)` → `panel.bg` / `panel.border` (near) |
| D8 | Delta text and name color | :695, :713 | meaning: delta sign; class | DR-G4 / `sem.statusBad`; class rung 4 |
| D9 | Timeline ticks on the chart | :1012 | meaning colors | rung 4 |
| D10 | Compare (Results_Compare.lua) | :285 delta colors; toggle :303; boards hover :314; separators `SEP_COLOR {.5,.5,.5,.18}` :45 / :342; score rule :353; bars BAR_UP/BAR_DOWN :54-55 / :510; rows stripe :604; `MUTED \|cff9e9ead` :62 | as listed | checkbox `S.Checkbox`; rule `S.Divider` (exact); separator → `divider` (near, D-7); stripe → `S.ListRow`; BAR_UP/DOWN rung 4; MUTED escape → `text.muted` (near: 9e9ead = .62/.62/.68 is C.dim, D-1) |
| D11 | Loadout (Results_Loadout.lua) | :226-370: item cells :258-261 (amber .16 mark), quality edge :335-348, `EMPTY_BG` :42, talent link `\|cffffd100` :112 | quality and amber | quality → `q.*` tokens (`NS.QualityColor`, LootHistory's pattern); EMPTY_BG → `input.bg` (near); amber mark DR-G4; link escape = hyperlink gold (rung 4) |
| D12 | Usage (Results_Usage.lua) | rows :281-363, checkboxes :337, Save/Edit :361-363 | Blizzard food/question icons :49-50 | `S.Checkbox`, `S.Button`; icons rung 4 |

### 1k. Ability timeline (modules/Results_Timeline.lua) and gear view (modules/Results_Gear.lua), the two modal windows

| # | Surface | Built | Typed today | Paints with |
|---|---|---|---|---|
| M1 | Opaque modal shell | Timeline :745-756 (`ApplySkin(f, Timeline.SKIN)`, SKIN :179-186); Gear :350-364 (`ApplySkin(f, Gear.SKIN)`) | a copy of Core.SKIN made opaque | **DR-G1**: passing a skin table bypasses the facade (Core.lua:218-227 builds `S` only when `skin == nil`) |
| M2 | Title, rules, controls, drag | Timeline :500-516 (rule :506); Gear :267-291 (rule :272) | gold title, `0.24…` rule | as W2 / `S.Divider` |
| M3 | Timeline lanes, ticks, legend discs, corridor, grid | :489-495, :542, :845-883, :912, :1113; THIS/OTHER/CORRIDOR :158-164; TRACK/GRID :167-168; DISC art :165 | data hues; `{1,1,1,.06}`, `{1,1,1,.08}` | lanes and legend rung 4; TRACK → `chart.track` (exact), GRID → `chart.grid` (.07, near), legend rule → `divider`-family (near) |
| M4 | Timeline controls (`-`, `+`, `?`, zoom level) | :576 (`SetFont(STANDARD_TEXT_FONT,size,"")`), :615 (CONTROL_FONT), zoom color :1082, LEVEL_REST :155 | typed face and grays | the strip as H3; `SetFont` → `S.Font(fs)` (body face); LEVEL_REST → `text.disabled` (exact .5); HOT = red |
| M5 | Timeline scroll bar | :652-662 | track `{1,1,1,.10}`, thumb `{1,1,1,.35}` | `S.ScrollBar(bar,{track=,thumb=})` (near, D-5) |
| M6 | Gear cells, columns, legends | Gear :300-318, :409-550 (tint amber .16 :413, quality edge :459/:489, EMPTY_BG :77, MARK_EDGE :78, legends :291/:547-550) | quality, amber, blue | quality `q.*`; MARK_EDGE → `icon.border` {0,0,0,1} (exact); amber DR-G4; EMPTY_BG `input.bg` (near); blue rung 4 |

### 1l. Library-drawn tool surfaces (DR-04)

| # | Surface | Built | Owner today | To do |
|---|---|---|---|---|
| X1 | Debug console | core/DebugLogSetup.lua:58-60 (`addonName = addonName`) | yes, through addonName (DebugLog minor 22) | nothing beyond registering the owner |
| X2 | Perf step panel | core/PerfSetup.lua:22-24 (`addonName`) | yes (PerfPanel minor 10) | nothing |
| X3 | Copy window (talent export) | WidgetsSetup.lua:65-77 (`addonName = addonName`) | yes (`d.addonName`) | nothing |
| X4 | Test strip | WidgetsSetup.lua:51-54 | **no** | `opts.owner = addonName` |
| X5 | Dropdown and its shared menu | WidgetsSetup.lua:28-35 | **no** | `opts.owner = addonName` |
| X6 | Toast | ToastSetup.lua:36-40 | yes (`d.owner`) | nothing |
| X7 | Settings pages (General, Race, HUD, History) | settings/OptionsSetup.lua:15-57 (`addonName`) | yes (Options 33.x paints by owner) | add the Appearance tab (DR-01) |
| X8 | Profiles page: AceDBOptions in an AceGUI SimpleGroup the addon acquires itself | settings/Profiles.lua:29-38 | **no** | `Skin:PaintAceTree(owner, container)` after each `AceConfigDialog:Open`; any OnRelease of its own through `Skin:OnRelease` |
| X9 | Sim | modules/Sim.lua drives the HUD bodies; no `LibKa0s-Sim` panel and no sim strip | n/a | nothing |
| X10 | Minimap and LDB launcher | core/LauncherSetup.lua:87 | library-owned art | nothing |
| X11 | Three hidden key-binding buttons | LauncherSetup.lua:24-38 | invisible | nothing to paint |

Surface count: 66 rows across 1a-1l.

## 2. Library factories that take an owner

| Factory | Call site | Owner passed? |
|---|---|---|
| `Core.ApplySkin(frame, skin, owner)` | CoreSetup.lua:89 published as `NS.ApplySkin`; called at Hud.lua:480, Results.lua:299, Results_Timeline.lua:756, Results_Gear.lua:364 | **no**. Wrap it as LootHistory does: `NS.ApplySkin(f) → lib.ApplySkin(f, nil, addonName)`. The two modals need DR-G1. |
| `Core.MakeCloseButton(parent, onClick, addonName)` | CoreSetup.lua:101-103 | yes |
| `W.Dropdown(parent, width, opts)` | WidgetsSetup.lua:31 | **no**: add `owner = addonName` |
| `W.TestStrip(parent, opts)` | WidgetsSetup.lua:53 | **no**: add `owner = addonName` |
| `W.CopyWindow(desc)` | WidgetsSetup.lua:69 | yes (`addonName`) |
| `W.CloseMenu()` | WidgetsSetup.lua:82 | takes none |
| `DebugLog:New(d)` | DebugLogSetup.lua:58 | yes (`addonName`, no `skin`/`applySkin` passed) |
| `Perf:New(d)` | PerfSetup.lua:22 | yes (`addonName`) |
| `Toast:New(d)` | ToastSetup.lua:39 | yes (`d.owner`) |
| `Options:New(descriptor)` | OptionsSetup.lua:131 | yes (`addonName`) |
| `Core.MakeResizable` (through NS.Sizing) | modules/Sizing.lua | takes no owner in v1.79.0 |
| `Launcher:New` | LauncherSetup.lua:87 | takes no owner |
| `Skin:PaintAce` / `PaintAceTree` | none today; needed at Profiles.lua:29-38 | — |

## 3. HUD style settings (the O2 / R3 one-time reset)

All of them are composed groups (settings/Hud.lua:114-176 and settings/History.lua:86-96), with defaults
at defaults/Profile.lua:77-114 and resolution at modules/Hud_Appearance.lua:68-141. Today
`H.FontGroup`/`H.BarGroup` are called without `fromSkin = true`, so no companion rows exist.

| Schema key | Default | Kind | How it follows the skin |
|---|---|---|---|
| `appearance.figures.font` | "Friz Quadrata TT" | font | `fromSkin = true` → `appearance.figures.fontFromSkin`; `Appearance.FontAt` reads `S.Resolve("hud.font", stored, fromSkin)` → "Ka0s Oxanium SemiBold" |
| `appearance.spellText.font` | "Friz Quadrata TT" | font | same (`spellText.fontFromSkin`) |
| `appearance.elapsed.font` | "JetBrains Mono" | font | **D-15 / DR-G5**: the clock-pair layout assumes a monospace advance (Hud_States.lua:44-48). The composer's companion is hard-wired to `hud.font` (OptionsCompose.lua FROM_SKIN.font), so following the skin would put a proportional face on the clocks. |
| `appearance.left.font` | "JetBrains Mono" | font | same as elapsed |
| `appearance.bars.barTexture` | "Solid" | statusbar | `fromSkin = true` → `bars.barTextureFromSkin`; `Appearance.BarAt` reads `S.Resolve("bar.texture", stored, fromSkin)` → "Ka0s Default", then LSM fetch as today (`fetch("statusbar", …)` Hud_Appearance.lua:116) |
| `appearance.chart.barTexture` | "Solid" | statusbar | same (`chart.barTextureFromSkin`) |
| `appearance.pace.barTexture` | "Solid" | statusbar | same (`pace.barTextureFromSkin`) |
| `resultsTable.damageBar.barTexture` | "Solid" | statusbar | same; on the Results window, not the HUD (D-16) |
| `resultsTable.dpsBar.barTexture` | "Solid" | statusbar | same (D-16) |
| `resultsTable.barText.font` | "Friz Quadrata TT" | font | same (D-16) |
| `*.fontSize`, `*.fontFlags`, `*.fontShadow` (6 font blocks) | 26/26/20/10/10; ""; shadow on for figures, spellText and barText | number, string, bool | **no companion in the composer**. `hud.fontSize` 12 and `hud.outline` "OUTLINE" exist as tokens, but nothing composes them. They stay the player's (D-6). |
| `*.barColor`, `*.barAlpha` (bars, chart, pace, damageBar, dpsBar); `appearance.chart.bgColor`; `*.fontColor` (figures, spellText, barText) | indigo .29/.29/.45@.85; .36/.37/.84@.9; bg {0,0,0,.35}; text .93/.93/.95 and white | color | **no color companion in the composer, and no HUD bar-fill token** (`bar.bg` is the track, not the fill). They stay the player's (D-6). The elapsed green and left red font colors carry meaning (section 4). |
| `appearance.bars.rowHeight`, `appearance.chart.height`, `appearance.chart.columnGap` | 18, 80, 0 | geometry | not style; never reset |

**The reset.** Add migration step 5 → 6 in core/Database.lua:10-41 (`perProfile = true`; NS.SCHEMA_VERSION :6
goes to 6) that sets the companions true. **Risk:** the runner hands each step the **raw** `sv.profiles[...]`
table, with no AceDB defaults metatable (Database.lua:70-71). On a raw table `Skin.ResetToSkin`
(Skin.lua:650-670) writes the `"@skin"` sentinel into the leaf whenever the companion key is absent: a stored
`font` with no stored `fontFromSkin` gets `font = "@skin"`, and a companion path named directly gets the string
`"@skin"`, not `true`. So either seed the companion (`= false`) before calling `ResetToSkin`, or write
`<block>.fontFromSkin = true` / `barTextureFromSkin = true` directly in each block table that exists. Also add
the companions to `defaults/Profile.lua` (the composer reads `spec.defaults[leaf .. "FromSkin"]`,
OptionsCompose.lua:229-238). That makes their default `true` (D-17), so a new profile and *Restore defaults*
both follow the skin.

## 4. Exceptions

### Rung 3: frames a skin never touches (skinning-§7)

| What | Where | Reason |
|---|---|---|
| StaticPopups `DPSRACE_DELETE_RUN`, `DPSRACE_RESET_ALL`, History's popup, Share's whisper popup | Results.lua:786; settings/General.lua:25; settings/History.lua:58; modules/Share.lua:168 | Blizzard StaticPopup |
| MenuUtil context menus (row menu, late-ignore menu, share submenu) | Results.lua:766-781; LateIgnore.lua:321-330 | Blizzard's shared menu frame. Lines the addon writes on it take token colors (the Delete escape → `sem.danger`). |
| GameTooltip itself | every tip site (Style.lua:190-196, Hud_States.lua:159-168, Results_Table.lua:236-273, and others) | Blizzard shared frame. The lines' colors come from `gtip.*`. |
| RaidWarningFrame "STOP" | Hud.lua:166-168 | Blizzard shared frame |
| Countdown digits and glow | Countdown.lua:40-41, 131-150 | the client's own start-timer art (BigGold), deliberately Blizzard's look |
| SettingsPanel chrome, ColorPickerFrame (the swatches), AceGUI-3.0-SharedMediaWidgets pull-outs (the LSM font and texture pickers) | settings pages | §7 named frames |
| Hidden binding buttons | LauncherSetup.lua:24-38 | never shown |

### Rung 4: game-meaning colors and art that stay

| What | Where | Reason |
|---|---|---|
| Class colors (rows, detail name, the HUD's useClassColor companions) | Results_Table.lua:104-109; Results_Detail.lua:713; Hud_Appearance.lua:50-62 | class meaning (RAID_CLASS_COLORS) |
| Class and spec icons; spell icons (breakdown, chart cooldown icons, timeline); item icons; Compare's two Blizzard icons; the trophy fallback; the food and question-mark icons | Results_Table.lua:44, 113-140; Hud_Breakdown.lua:188; Hud_Chart.lua:680-698; Results_Compare.lua:59-60; BestToast.lua:42; Results_Usage.lua:49-50 | game art |
| Item quality (gear and loadout cell edges) | Results_Gear.lua:249-251, 459, 489; Results_Loadout.lua:153-160, 344-348 | **not an exception in an adopted addon**: read through the `q.*` tokens, as LootHistory's `NS.QualityColor` does (Ka0s Default writes the client's values out) |
| Talent hyperlink gold `\|cffffd100` | Results_Loadout.lua:112 | the client's link color |
| Race-length hues (five soft ROYGBIV plus neutral) | Results_Table.lua:68-74 | DPS Race's data encoding (owner's call 2026-10-25), distinct by design |
| Category hues (single, cleave, dungeoneer, boss, pvp, other) | Results_Table.lua:78-83 | data encoding (mockup screens 08-09) |
| Status-tag hues blue, violet, orange, pink, slate | Results_Table.lua:53-58; also BestToast.lua:134-136, Results_Detail.lua:469, Results_Gear.lua:547 | data encoding ("each status a distinct color", owner 2026-10-25) |
| Timeline THIS (gold) and OTHER (blue) runs and their corridors | Results_Timeline.lua:158-164 | per-run identity colors (the "per-player colors" the plan names) |
| Compare BAR_UP / BAR_DOWN | Results_Compare.lua:54-55 | higher and lower run |
| Detail strip legend RACE, CYAN, VIOLET, IGNORED | Results_Detail.lua:97-105 | data encoding of the strip's line types |
| The elapsed-clock green and time-left red | defaults/Profile.lua:80-83; Hud_States.lua:736-743 | elapsed against remaining (spec §6.1). Player-set swatches, never reset. |
| Chat prefix `\|cff00ffff[DR]\|r` and the disabled-line yellow | core/Namespace.lua:5; settings/Slash.lua:110 | chat text, not a frame |

## 5. Gaps (rung 2)

Strict list: only what no existing primitive or token can paint while Ka0s Default keeps today's values.

**DR-G1: an opaque modal shell (primitive option `S.Shell(f, { opaque = true })`).** The timeline and the gear
view open over the Results window and must hide it completely, in every skin. Glass, for one, is translucent by
design. Today each window passes its own skin table to `Core.ApplySkin(f, Timeline.SKIN)`, and a table argument
skips the facade (LibKa0s Core.lua:220: `S` exists only when `skin == nil`), so neither window could follow a
skin. No token is opaque: `win.bgDense` is .95. Ka0s Default must draw Results_Timeline.lua:179-186 (Gear uses
the same SKIN): the fill is `win.bg` at alpha 1, `{0.06, 0.06, 0.08, 1}`, and the inner border and divider are
blended over that fill to alpha 1 (`opaque(c, bg)`, Results_Timeline.lua:~170-178: `c*a + bg*(1-a)`, so `win.inner`
{.24,.24,.27,.85} becomes ≈ {.213,.213,.242,1}). Under every other skin: its `win.bg` at alpha 1, with its inner
and divider blended the same way.

**DR-G2: a danger button (primitive option `S.Button(b, { danger = true })`, tokens `btnDanger.bg`,
`btnDanger.border`, `btnDanger.text`, `btnDanger.hover`).** Cancel race and Delete run are red-edged buttons.
`S.Button` knows only `btn.*` and `btnPrimary.*` (SkinPaintControls.lua:93-151), and no Buttons token is red.
Ka0s Default: bg `{1, 0.32, 0.32, 0.08}`, border `{1, 0.32, 0.32, 0.6}`, text `{1, 0.32, 0.32, 1}`, hover text GOLD
`{1, 0.82, 0, 1}` (Hud_States.lua:41, 145-149). Disabled: fill alpha ×0.4, edge .25, label alpha .4
(Hud_States.lua:146-149), the same disabled rule as normal and primary (D-2).

**DR-G3: a caution callout (new primitive `S.Callout(frame, { text = fs, strong = bool })`, tokens `callout.bg`,
`callout.border`, `callout.text`, `callout.borderStrong`).** An amber-washed box with cream text appears three
times: the HUD's waiting hint, the target card's badge, and the Results detail's flags box. `S.Panel` and
`S.Card` take fixed `panel.*` / `card.*` tokens and no amber token exists. Ka0s Default, exact:
- hint: bg `{1,.72,.29,.07}`, edge `{1,.72,.29,.35}`, text `{.95,.85,.67}` (Hud_States.lua:946-949)
- flags box: bg `{1,.72,.29,.06}`, edge `{1,.72,.29,.35}`, main line `{.95,.84,.65}`, body `{.94,.84,.65}`, detail
  amber (Results_Detail.lua:109-110, 530-541, 735-748)
- badge: bg `{1,.72,.29,.08}`, edge `{1,.72,.29,.6}`, amber text (Hud_States.lua:352-355)

Recommended: one `callout.bg` .07, `callout.border` .35, `callout.borderStrong` .6 (the badge), and `callout.text`
`{.95,.85,.67}`. The flags box's .06 and its two text tints .01 off would then move to those values (D-18).

**DR-G4: DPS Race's semantic hues (tokens).** The standard says meaning colors in an adopted addon come from
the skin's semantic tokens, with Ka0s Default answering the addon's old values. These three have no token with
that value or hue:
- `sem.ahead` (gain / ahead / new best / positive delta / DPS figure): `{0.36, 0.86, 0.46, 1}`. Hud_States.lua:29;
  Results_Table.lua:51; Hud_Chart.lua:89 at .85 alpha. `sem.good` is `{.35,.80,.45}` and `sem.goodAlt` is
  `{.25,1,.25}`.
- `sem.caution` (late casts, warnings, flag details, the amber cell marks): `{1.0, 0.72, 0.29, 1}`.
  Hud_States.lua:27; Results_Table.lua:50; used at .16 on Gear :413 and Loadout :261. `sem.warn` is orange
  `{1,.5,0}`.
- `sem.infoAlt` (grace and time chips): `{0.56, 0.72, 1.0, 1}`. Hud_States.lua:30. `sem.info` is cyan
  `{.3,.8,1}`.

Red is already covered: `sem.statusBad` `{1,.32,.32}` is exact.

**DR-G5: a FontGroup `fromSkin` token choice (composer option `fromSkin = "font.mono"`).** The two clocks are
monospace by layout (Hud_States.lua:44-48: "an advance of at most 0.62 em"). OptionsCompose's font companion
always shows and resolves `hud.font` (OptionsCompose.lua FROM_SKIN.font). Ka0s Default's `font.mono` is
"JetBrains Mono", which is the clocks' default exactly (defaults/Profile.lua:80-83). This gap goes away if the
owner rules the clocks out of R3 (D-15).

No gap for: the chart host (`S.ChartStyle`, `chart.series` exact), tabs, title-bar controls, dividers, test strip,
cover, list rows, scroll bars, checkboxes, edit boxes and bar textures (`S.BarTexture`). Each of those composes
from existing primitives, sometimes at near values (section 6).

## 6. Doubtful calls (DECISIONS.md)

| # | Call | Recommendation |
|---|---|---|
| D-1 | The HUD/table body text `{.93,.93,.95}` and dim `{.62,.62,.68}` (also `\|cff9e9ead`, Results_Compare.lua:62) have no exact token. | Map to `text.body` (.9) and `text.muted` (.7/.7/.72). The shift is ≤.08 and keeps DR in line with LootHistory. Do not add tokens. |
| D-2 | Primary and selected buttons: DR's `{1,.82,0,.12}` fill and `.75` edge against `btnPrimary` `{.2,.16,.03,.95}` / `.8`. DR also dims a disabled button's fill and edge, while `S.Button` dims only the label. | Accept `btnPrimary` (the owner's "primary must differ" note). Draw a selected preset as primary. Accept the library's disabled treatment. Smoke-check the Arm button. |
| D-3 | KPI boxes, chips' base and panels: DR's faint white wash `{1,1,1,.03}`/`{1,1,1,.10}` has no token. The composite fill is ≈ `card.bg` over the window; the edge is lighter under `card.border`. The detail strip's segments `{.07,.07,.1,1}` map to `input.bg`. | `S.Card` for KPI boxes and cards, `S.Panel` for list panels, `S.Inset` for strip segments. Accept the slightly brighter edge. |
| D-4 | Chips and status badges tint a meaning color to .08 fill and .55/.6 edge. Composing them from `S.Color(token)` writes those alphas at the call site (#107 names "alpha"). | Compose. Keep the two alphas as named constants in `modules/Style.lua` and record why they are data-encoding, not chrome. Rebuild on `OnLooksChanged`. Escalate to a `S.Badge` primitive only if the reviewer reads #107 strictly. |
| D-5 | List and scroll near-values: stripe .025 against `list.stripe` .03; hover `{1,1,1,.04}` against `list.hover` gold .10; selection gold .10 against `list.sel` .18; header gets a new `list.header.bg` .04; breakdown track `{1,1,1,.04}` against `chart.track` .06; scroll thumbs white .25/.35 against `scroll.thumb`. | Accept the library tokens throughout, for one list look across the collection. Smoke-check the Runs list and the spell rows. |
| D-6 | HUD colors, sizes, outline and shadow stay the player's. The composer offers `fromSkin` only for font face, border and bar texture, and no token holds a bar fill color. | Reset only the faces and textures (R3's wording: texture, border, font). Record that the colors do not follow, and open a LibKa0s issue if the owner wants color companions. |
| D-7 | Chart near-values: diagonal `{.9,.9,.92,.4}` against `chart.marker`; pace track .08 against `chart.grid` .07; Insights bar blue `{.40,.66,1}` against `chart.bar`; Compare separator `{.5,.5,.5,.18}` against `divider`. | Accept the chart tokens. |
| D-8 | Timeline cover dim .45 against `cover.dim` .6. | Accept `S.Cover`. A darker dim under a modal is harmless. |
| D-9 | DR's close control turns GOLD on hover through the strip (Style.AddToStrip repaints it), overriding Core's red. Skinning-§7 rescopes the close rest and hover tints to the skin (`close.hot`, red in Ka0s Default). | Let `S.CloseButton` own the close control: drop it from the gold strip, so close goes red on hover. The other controls keep the gold through `text.accent`. |
| D-10 | `S.SquareIcon`/`S.IconBorder` would add a black 1px `icon.border` edge (Ka0s Default sets it since SkinDefs minor 8) to the spell icons, which have none today. | Do not edge the HUD spell icons under Ka0s Default. Call `S.IconBorder` only on the gear cells' mark edge, which is already `{0,0,0,1}` (Results_Gear.lua:78). |
| D-11 | The countdown's fallback number (typed STANDARD_TEXT_FONT, GOLD, THICKOUTLINE) is shown only when the client cannot load the timer art. | Keep it with the exception. If the owner wants it skinned: `hud.font` and `text.accent`. |
| D-12 | The resize grip is Core.MakeResizable art and takes no owner. | Leave it. A library item only if the owner sees it clash in a light skin. |
| D-13 | `S.Checkbox` replaces the Blizzard `UICheckButtonTemplate` look with Ka0s Default's square box: the filter bars, the Compare toggle and the Usage rows change look under Ka0s Default. | Accept: it is the collection's checkbox. Smoke-check. |
| D-14 | The note edit box's edge is gold `input.focus` even without focus. | Use `S.EditBox` (rest `input.border`, gold on focus). |
| D-15 | The clocks under R3: monospace by layout. | Rule the two clock blocks out of the reset and draw them from `font.mono` only while the player has not picked a face. Or take DR-G5 if the owner wants a "Use the skin's font" row on the clocks. Recommend excluding them: no library change. |
| D-16 | Do the Results table's bar and text groups (`resultsTable.*`) count as "HUD style" for the one-time reset? | Yes. They are the same composed groups and draw the same data bars. Give them `fromSkin` and include them in the reset. |
| D-17 | Default for the `*FromSkin` companions: `false` (the composer's default) with the migration setting `true`, or `true` in `defaults/Profile.lua`. | Default `true` in `defaults/Profile.lua`, so new profiles, *Restore defaults* and *Reset all* follow the skin as R3 intends. Keep the per-profile migration step for profiles that stored a pick. |
| D-18 | The flags box's .06 fill and its `.95/.84/.65` and `.94/.84/.65` texts would collapse onto DR-G3's single callout values. | Accept the collapse: differences of .01 cannot be seen. |
| D-19 | Naming: the HUD page already has a tab called "HUD Appearance" (settings/Hud.lua:109), and the skin tab on General will be "Appearance". | Keep both. The standard fixes the General tab's label. Mention the skin in the HUD Appearance tab's companion tooltips. |
| D-20 | Ka0s Default itself changes at adoption (v1.79.0: Oxanium body and title faces, the "Ka0s Default" bar). Every `Style.FONT` label then shows Oxanium. | Expected (CHANGELOG v1.79.0 "Ka0s Default looks different"). Re-look in smoke, and re-pin the golden values in tests. |

## 7. Re-vendor v1.77.0 → v1.79.0 obligations (DR-RV)

- **Whole-folder re-vendor** with `git archive v1.79.0` of `LibKa0s/` into `libs/LibKa0s/` and `tests/_kit/` (the
  kit gains `mock_paint.lua`; `mock_base.lua` changes). Prune icons with the tag's `tools/prune-icons.lua`.
  70 library files change.
- **Toast.lua stops being the exception.** v1.79.0 carries `Toast.lua`, and the vendored copy matches it apart
  from CRLF line endings. When the tag carries it, tests/test_vendor_sync.lua:5-75 **fails on purpose** ("drop this
  exception, the TOC's Toast.lua line and the deviation row"). Remove in the same commit:
  - the AHEAD exception and the byte case in tests/test_vendor_sync.lua (back to the plain `VendorSync.register`)
  - `libs\LibKa0s\Toast.lua` and its three comment lines in DpsRace.toc (after `libs\LibKa0s\LibKa0s.xml`)
  - the `library-stack-§7` row in docs/ARCHITECTURE.md:563, and the "one LibKa0s file vendored ahead" wording at
    :94
  - the "Plus LibKa0s-Toast-1.0 …" paragraph in CLAUDE.md
  - the toast bullet in docs/known-limitations.md:179-183 (and smoke rows SM-DR-TA17..23 get a re-look)
- **Options degradation stub** (settings/OptionsSetup.lua:104-114) gains `AppearanceTab` and `AppearanceRows` (v1.78.0)
  and `SkinPicker` and `HideSkinPicker` (v1.79.0). tests/test_surface_parity.lua:24-31 (`assertSurfaceParity(d.NS.Helpers,
  "LibKa0s-Options-1.0", …)`) goes red until they are there. Check whether any new lib-level constant
  (`APPEARANCE_STRINGS`, …) needs adding to that test's exemption list.
- **CLAUDE.md provenance line:** "Bundles LibKa0s v1.79.0 (MIT)."
- **`LibKa0s icons:` line** (CLAUDE.md): add `eye` for the first-run picker's preview button. `settings` is already
  declared. Then prune, and update the README's icon-set credits.
- **Version mentions:** docs/ARCHITECTURE.md:21 ("v1.77.0") and docs/debug.md:95 (`DIAG_MAX_LINES` "in the vendored
  v1.77.0": re-read the value at v1.79.0).
- **At adoption (DR-01), not at the re-vendor:** `## OptionalDeps:` gains `EllesmereUI` (DpsRace.toc:8;
  skinning-§5). Add the `core/SkinSetup.lua` TOC line after core/CoreSetup.lua and before core/WidgetsSetup.lua.
  Its LOAD-BEARING note follows the TOC's comment convention.
- **Release pins:** no test pins a library minor or the LibKa0s file list beyond the vendor gate. The 16 test files
  that pin colors, listed below, are adoption work (DR-02/03), not re-vendor work:
  mock_widgets, test_chart, test_compare, test_hud, test_insights, test_late_ignore, test_loadout,
  test_results_badges, test_results, test_results_delta, test_results_group, test_results_timeline_controls,
  test_results_timeline_scroll, test_results_usage, test_toast, wow_mock.

## 8. Risks

- **File cap (1500 lines).** modules/Results_Timeline.lua is 1457 lines (43 to spare), and it holds DR-G1's opaque
  SKIN and many paint sites. modules/Results_Detail.lua is 1218, Hud_States.lua 1204, Results_Table.lua 1155,
  Results_Runs.lua 1112, Hud.lua 1093. In the tests, test_hud.lua is 1474 and test_results.lua 1473. New skin
  cases go in a **new** suite (`tests/test_skin.lua`), never appended to those two. Expect Results_Timeline's
  conversion to need a helper moved out of the file (for example into modules/Style.lua).
- **The R3 migration on raw profiles** (section 3): `Skin.ResetToSkin` writes `"@skin"` into a leaf whose
  companion is absent from the raw saved table. Write the companions directly, or seed them first.
- **Hot paths.** The HUD redraws at 4 Hz (`hudLive`) and runs a 20 Hz countdown tick (`hudTick`, PerfSetup.lua
  buckets). Facade calls belong at creation and in the stamped restyle (`HudAppearance.stamp`,
  Hud_Appearance.lua:16-17, 149-155), never in Update. `S.BarTexture` reads the live bar color on every call
  (SkinPaintExtras.lua:250-262), so call it when a row is restyled, not on every value set. Chips, rows, chart
  columns, icons and marks are pooled (NS.Pool): paint once at the factory and repaint through `OnLooksChanged`.
  Do not re-track a pooled row on every acquire.
- **Secret values.** The meter path carries secret values (the four invariants in docs/ARCHITECTURE.md's
  Overview). The facade reads colors and fonts only. Keep paint calls away from code that formats a secret
  value. `S.Text` changes no text.
- **Pooled AceGUI.** The Profiles page's SimpleGroup and AceConfigDialog's children are the only AceGUI widgets
  the addon acquires itself. Paint them with `PaintAceTree` after every `Open`, and never attach an `OnRelease`
  directly.
- **Combat.** Nothing DR skins is secure or protected. The HUD can be open in combat, and a skin switch repaints
  it in combat, which is allowed (no protected frame). The picker defers its show to PLAYER_REGEN_ENABLED (the
  library does this).
- **Shared Blizzard frames.** MenuUtil menus, StaticPopups and RaidWarningFrame must not be painted. Only the
  escape strings DR writes into them change.
- **Markup built once at file load** (Results_Table.lua:632-633, 1037-1038) does not follow a skin switch. Rebuild it
  in an `OnLooksChanged` handler or build it lazily.
- **The two modals** cannot follow the skin at all until DR-G1 lands. That puts M1 (LibKa0s v1.80.0) on DR's
  critical path.

## 9. Effort

**L.** There are about 66 surfaces in about 20 files, two modal windows waiting on a gap, R3 on 10 style keys
with a raw-profile migration subtlety, and 16 color-pinned test files. Choke points (`Style.Text`,
`States.Button`, `Tbl.Panel`, `NS.ApplySkin`, `Charts.Host`, `HudAppearance`) carry most of the conversion.
Results_Timeline.lua's 43-line headroom adds risk.
