# LootHistory surfaces: input for the skinning prototype

Read-only survey of `../LootHistory` at `master` `2520eef` (2026-10-24, v1.5.0, LibKa0s v1.77.0
vendored). `libs/` and `tests/_kit/` are out of scope apart from the LibKa0s parts that draw on
LootHistory's behalf, which are named so the facade knows where host reach ends. Every `file:line`
is into `../LootHistory`.

## 1. Gate, conventions and the docs a change must touch

### Green gate (from `CLAUDE.md` and `docs/testing.md:235-255`)

| Check | Command | Bar |
|---|---|---|
| Headless suites | `lua tests/run.lua` (from the repo root, Lua 5.1) | all pass; the vendor-sync cases must **pass, not skip** |
| Lint | `luacheck .` | 0 warnings / 0 errors; no top-level `ignore`, no bare `-- luacheck: ignore` (`tests/test_lintconfig.lua`) |
| File cap | `tests/_kit/test_layout_cap.lua` (runs inside `run.lua`) | no authored `.lua` over 1500 lines unless censused in `docs/ARCHITECTURE.md:462` |
| Complexity | `bash tests/_kit/run-automated-tests.sh --suite complexity` | release check only: no function above CCN 15. Never raw `lizard` |
| Prose | `tests/_kit/test_prose.lua` | US English in every authored file |

**Headroom against the cap:** `modules/Browser.lua` 1327, `modules/BrowserTable.lua` 1320,
`settings/Schema.lua` 1184, `settings/Panel.lua` 1177. Skin wiring cannot be inlined into the two
browser files. It needs a file of its own.

### Conventions that bind a skin change

- **A new file is a TOC line.** The loader derives the load list from `LootHistory.toc`
  (`docs/testing.md:9-16`), and `tests/test_harness.lua` pins that derivation. A new seam goes in
  `core/` after `core/CoreSetup.lua:65` and before `core/WidgetsSetup.lua:83` (Widgets resolves
  art at call time, so it does not care either way). `docs/module-map.md` needs a row and a
  load-order entry, and its count ("59 authored source files") changes.
- **Every LibKa0s seam has a degraded arm that answers the whole surface.**
  `tests/test_surface_parity.lua` derives the NS name set from each seam file and compares the
  live and stub arms. A `core/SkinSetup.lua` needs a parity case of its own.
- **A setting is one row in four places** (`docs/common-tasks.md:15-47`): the default in
  `defaults/Profile.lua`, a row in `settings/Schema.lua` whose `default` reads `PD.settings.<path>`,
  the library row vocabulary (`type = "string"`, `values` holding `text`), and an `onChange` that
  sends `NS.MSG.SETTINGS_CHANGED`. A new tab needs a `GENERAL_TABS` entry (`settings/Panel.lua:986`)
  in the same position as its rows, and `tests/test_panel.lua` compares the two lists.
- **Tab rules from the suite.** No tab may hold fewer than two controls
  (`tests/test_schema.lua:719`), so an Appearance tab with only a skin dropdown fails. A tab's name
  may not contain its page's name (`:735`). Rows in a group must be contiguous.
- **Locales.** Since the 2026-09-08 `localization-§1` row (`docs/ARCHITECTURE.md:425`) the addon
  is English only. New panel labels may be literals, which is what the rest of Schema does. Strings
  shown in the History window's mode marks route through `NS.L`, so follow that pattern if the skin
  touches the marks.
- **Media.** Art comes from LibKa0s-Media first and Blizzard second, never from the addon
  (`docs/common-tasks.md:216-294`). A mark the catalog lacks is added upstream. `WHITE8X8` is the
  one sanctioned flat fill. The "No LSM media pickers, by design" bullet (`:290-294`) and the TODO at
  `modules/Browser.lua:14-15` both say a user-configurable skin "belongs at the LibKa0s seam". This
  prototype is what retires that TODO.
- **Deviations.** Anything that departs from the standard (for example an Appearance tab the
  `options-ui` sections do not yet name) is either recorded as a row in `docs/ARCHITECTURE.md`
  `## Documented deviations` or changed upstream in WowAddonStandards. CLAUDE.md says to stop and
  flag it.
- **Goldens are never regenerated to make a change pass.** `tests/analytics_golden.txt` (559 `ct=`
  color entries) and `tests/panel_auction_golden.txt` pin colors. The default skin must reproduce
  today's values byte for byte. A deliberate color change rewrites the golden in its own commit and
  says so (`tests/test_analytics_layout.lua:11-13`).

### Docs that list settings, modules or surfaces

| Doc | What changes |
|---|---|
| `docs/module-map.md` | new seam file row, TOC order and file count |
| `docs/schema.md` | the `db.profile` shape (`:38`) and the rows table (`:242`); state that the new key needs no migration |
| `docs/settings-panel.md` | the "What each tab covers" table (`:22-34`) and a per-option entry for the Appearance tab |
| `docs/browser.md` | the re-skin seam paragraph (`:14`), Bound colors (`:113`), the row menu "gold border" (`:133`) |
| `docs/common-tasks.md` | the Media house rule (`:243-249`, `:290-294`); add a "Skin a new surface" recipe |
| `docs/ARCHITECTURE.md` | settings-schema summary, the documentation map if a doc is added, and any deviation row |
| `docs/profiles.md` | the skin is per profile, so it moves with a profile switch |
| `docs/smoke-tests.md` | new `SKIN-n` block and an index row (`:13-40`). The owner runs these |
| `docs/test-cases.md` | regenerate with `lua tests/run.lua --list > docs/test-cases.md`, then the README Tests badge (`README.md:7`) |
| `docs/testing.md` | the suite table (`:63+`) for each new `test_skin_*.lua`, plus the suite list in `tests/run.lua:61-99` |
| `README.md` | the `## Usage` prose that names settings tabs, and the FAQ (`:116`) |

## 2. Surface inventory

The **Primitive** column names the facade primitive and its token (`chrome.*` for chrome,
`text.*` for font roles, `sem.*` for semantic colors).

### 2.1 History window shell (`modules/Browser.lua`)

| Element | Created | Styling today | Primitive / token |
|---|---|---|---|
| Window `LootHistoryWindow` | `:924` `BackdropTemplate` | `B:ApplySkin(frame)` `:1089` → `NS.ApplySkin` = `Core.ApplySkin` (`Core.SKIN`: bg `.06,.06,.08,.92`, border black, inner `.24,.24,.27,.85`) | **Shell** (`chrome.bg`, `chrome.border`, `chrome.innerBorder`) |
| Title bar frame | `:947` | none (transparent) | **TitleBar** |
| Title text | `:966` `GameFontNormal`, exposed as `frame.title` | tinted gold by ApplySkin (`Core.SKIN.title`) | **TitleBar** / `text.title` |
| Mode badge (degraded only) | `:973` `GameFontNormalLarge` | `SetTextColor` from `TEST_MARK`/`SIM_MARK` `:976`, `:630` | `sem.modeTest`, `sem.modeSim` |
| Divider | `:980` texture, `frame.divider` | tinted by ApplySkin (`Core.SKIN.divider`) | **TitleBar** / `chrome.divider` |
| Close button | `:988` `B:MakeCloseButton` → `NS.MakeCloseButton` → `Core.MakeCloseButton` | library rest `.7,.7,.72`, hot `1,.3,.3` (`libs/LibKa0s/Core.lua:211-212`) | **CloseButton** (`chrome.closeRest`, `chrome.closeHot`) |
| Resize grip | `:1050` `NS.MakeResizable` | Blizzard `UI-ChatIM-SizeGrabber` art (library) | leave as is (`docs/common-tasks.md:236-242`) |
| Tab strip and tabs | `LayoutTabButtons` `:251-274`; label `GameFontNormal` `:264`; underline texture `:266` | label `SKIN.tabActive`/`tabIdle` `:169`; underline `SKIN.tabActive` `:267` | **Tab** (`chrome.tabActive`, `chrome.tabIdle`, `chrome.tabUnderline`) |
| Panes | `CreatePane` `:149` | none | none |
| Filter host | `:1002` | none | none |
| Test and sim strips | `buildModeStrip` `:906` → `NS.MakeTestStrip` → `W.TestStrip` (`core/WidgetsSetup.lua:295`) | library amber or cyan by `kind` | library-owned (see 2.10); `sem.modeTest`/`sem.modeSim` |
| Strip tooltips | `testTip`/`simTip` `:892-902` | `AddLine(...,1,1,1)` | **Tooltip** `text.body` |
| Footer and DB footer | `:1018`, `:1021` `GameFontDisableSmall` | font object only | `text.muted` |
| Graying of unhonored filters | `setHonored` `:193-199` | `SetAlpha(0.4)` (`GRAY_ALPHA` `:184`) | `chrome.disabledAlpha` |
| Master alpha and scale | `B:ApplyChrome` `:1125-1130` | `SetScale`, `SetAlpha(settings.alpha)` | not a skin token. It multiplies on top of the skin |

### 2.2 Filter bar (`modules/BrowserFilterBar.lua`)

| Element | Created | Styling today | Primitive / token |
|---|---|---|---|
| Ten dropdowns (group, dir, date, bound, quality, type, subtype, source, zone, char) | `B:BuildFilterBar` `:405-520` through `NS.MakeDropdown` (`core/WidgetsSetup.lua:118`) | library `Widgets.lua:85` file-local `SKIN`; option `color` from quality (`BrowserWidgets.lua:14`) and class (`:73`) | **Dropdown** (library); option colors are `sem.quality[q]`, `sem.class[cf]` |
| Search box | `:437` `NS.MakeSearchBox` → `W.SearchBox` (gold focus line) | library | **SearchBox** |
| Plain search (degraded) | `makePlainSearch` `:365-386` | backdrop `.1,.1,.12,.9`/`.24,.24,.27,.9`, placeholder `GameFontDisableSmall` | **EditBox** (`chrome.controlBg`, `chrome.controlBorder`, `text.muted`) |
| Autocomplete list | `:445` `NS.MakeAutocomplete` | library; row color from `qualityColor` `:78` | library; `sem.quality` |
| Export, Save, Reset and Clear buttons | `makeBarButton` `:330-360` | backdrop `.1,.1,.12,.9` / border `.24,.24,.27,.9`; icon vertex `.85` `:343`; label hover gold `:350`, rest white `:357`; tooltip `.9` `:353` | **Button** (`chrome.controlBg`, `chrome.controlBorder`, `text.body`, `text.accent` on hover, `chrome.icon`) |

### 2.3 History table (`modules/BrowserTable.lua`)

| Element | Created | Styling today | Primitive / token |
|---|---|---|---|
| Header frame | `Attach` `:917` | none | **SortHeader** host |
| Header cells | `MakeHeaderButton` `:955-987`, `GameFontNormalSmall` | gold `:971` (`GOLD_R..` `:33`); bound lock vertex gold `:964` | **SortHeader** / `text.heading` |
| Sort arrows | `ARROW_ASC`/`ARROW_DESC` `:326-327`, built **at file load** | gold baked into `NS.IconMarkup` | **SortHeader** / `text.heading` (must be rebuilt after a skin change) |
| Header tooltip | `:974-983` | title `1,.82,0`, body `.9` | **Tooltip** (`text.title`, `text.body`) |
| Scroll | `:925` `FauxScrollFrameTemplate` | Blizzard scrollbar art | **ScrollBar** |
| Row host | `:935` | none | none |
| Empty text | `:943` `GameFontDisableLarge` | font object | `text.muted` |
| Row (pooled) | `BuildRow` `:745-851`, `Button` | none | **ListRow** |
| Stripe | `:751-753` | `1,1,1,.03`, shown on even rows `:1156` | **ListRow** / `chrome.rowStripe` |
| Hover | `:756-758` HIGHLIGHT | `1,.82,0,.10` | **ListRow** / `chrome.rowHover` |
| Selection | none | no selected-row state exists | (n/a) |
| Cells | `:763` `GameFontHighlightSmall` | `PaintCell` `:1132-1152`: quality `:1142`, class `:1146`, qty `:1148`, default `.9` `:1150` | `text.body`; `sem.quality`, `sem.class`, `sem.dir.*`, `sem.gold` |
| Direction glyph | `:772` `SetFont(C.FONT_MONO)` | `LedgerFormat.Color(dir)` `:1117-1127` | `sem.dir.in/out/move` (font stays mono) |
| Bound lock | `:781-785` | vertex color and alpha from `BOUND_STYLE` `:1185-1187` | `sem.bound.*` |
| Group header row | `:788-792` `GameFontNormalSmall` | gold `:790`; chevron gold `:1169-1171`; count `|cff808080` `:1173` | `text.heading`, `text.muted` |
| Row tooltip | `:800-826` | item hyperlink; gold amount `C.GOLD_RGB` `:806`; inferred `.62` `:821`; hint `.5` `:823`; sample tooltip `:727-738` | **Tooltip** (`text.muted`); the item text is Blizzard's |
| Row menu (also used by Holdings) | `EnsureRowMenu` `:1203-1221`, `BackdropTemplate`, POPUP strata | bg `.06,.06,.08,.98`, border muted gold `.62,.5,.18,1` `:1209-1210` | **Panel** variant `menu` (`chrome.menuBg`, `chrome.menuBorder`) |
| Menu items | `ShowMenu` `:1273-1316` | hover `1,.82,0,.15` `:1288`; enabled `.9` `:1300`; disabled `.5` `:1304`; Delete `|cffff5555` `:1263` | **ListRow** (`chrome.menuHover`, `text.body`, `text.disabled`, `sem.danger`) |

### 2.4 Export (`modules/Export.lua`)

| Element | Created | Styling today | Primitive / token |
|---|---|---|---|
| Modal `LootHistoryExportWindow` | `:463` `BackdropTemplate`, MODAL strata | `NS.Browser:ApplySkin(frame)` `:530` | **Shell** (or **Dialog**) |
| Title bar and title | `:483`, `GameFontNormal` `:493` stored as `frame.titleFS` | **not tinted by ApplySkin**: the field is `titleFS`, not `title`, and there is no `divider` | **TitleBar** (bring this in line) |
| Close | `:496` | library | **CloseButton** |
| Data Set dropdown | `:476` `NS.MakeDropdown` | library | **Dropdown** |
| Export to CSV button | `makeButton` `:418-440` (a second copy of `makeBarButton`) | same values as 2.2 | **Button** |
| Copy window | `ensureCopyWindow` `:365-386` → `NS.CopyWindow` | `applySkin` hook → `B:ApplySkin` `:374`; JetBrains Mono 10 | **Shell** through the hook |

### 2.5 Insights (`modules/Analytics.lua`, `AnalyticsCharts.lua`, `AnalyticsLedger.lua`)

| Element | Created | Styling today | Primitive / token |
|---|---|---|---|
| Scroll | `Analytics.lua:49` `UIPanelScrollFrameTemplate` | Blizzard | **ScrollBar** |
| KPI cards (14, `CARD_DEFS` `:23-38`) | `:62-87` `BackdropTemplate` | bg `.1,.1,.12,.85`, border `.24,.24,.27,.9` `:65-66`; number `GameFontNormal`/`Huge` gold `:76`; caption `GameFontDisableSmall` `:77`; shrink-to-fit `SetFont` `:172-175` | **Card** (`chrome.cardBg`, `chrome.cardBorder`, `text.accent`, `text.muted`) |
| Ledger card values | `UpdateCards` `:125-152` | `LedgerFormat.SignedMoney` inline `|cff40ff40`/`ff4040`/`808080` (`LedgerFormat.lua:33-45`) | `sem.gain`, `sem.loss`, `sem.neutral` (escapes built at call time) |
| Section headers (19) | `sectionHeader` `AnalyticsCharts.lua:179-184` | `GameFontNormal` + gold `:182` | `text.heading` |
| Section dividers (LOOT, CURRENCY, GAINS & LOSSES) | `sectionDivider` `:188-210` | rules `1,.82,0,.35` `:192/:195`; title ×1.5 gold `:199-201` | `chrome.sectionRule`, `text.heading` |
| List panels (Top Zones, Top Items, Top Items By Value) | `listPanel` `:212-224` | bg `.08,.08,.10,.6`, border `.24,.24,.27,.7`; title gold `:220` | **Panel** (`chrome.panelBg`, `chrome.panelBorder`, `text.heading`) |
| Horizontal bar (pooled) | `makeBar` `:34-53` | track `1,1,1,.06` `:41`; fill = series color `:250`; label = row color `:254`; value `.8,.8,.82` `:256` | `chart.track`, `chart.series[n]` / `sem.*`, `text.body` |
| Stacked bar (pooled, 9 segments) | `makeStackedBar` `:68-98` | track `:75`; segments `:113`; value `:283` | as above |
| Day or hour strip bar (pooled) | `makeStripBar` `:124-145` | fill `.40,.60,.95,.9` `:128`; axis label `.7,.7,.72` rotated `:135`; count-0 alpha `.12` `:356` | `chart.bar`, `text.muted` |
| Strip axis line | `renderStrip` `:344-345` | `.45,.45,.5,.8` | `chart.axis` |
| List row (pooled) | `makeListRow` `:148-161` | name = row color `:392`; count `.8,.8,.82` `:393` | `text.body`; `sem.quality` |
| Legend swatch (pooled) | `makeSwatch` `:164-177` | swatch = series `:300`; label `.8,.8,.82` `:170` | `chart.series`, `text.muted` |
| Cursor tooltips | `showCursorTooltip` `:21-31` | gold title for bars `:50/:95`, white for segments and rows `:89/:158`, `.9` for swatches `:174` | **Tooltip** |
| Empty text | `Analytics.lua:223` `GameFontDisableLarge` | font object | `text.muted` |
| Ledger back-to-back bar (pooled) | `AnalyticsLedger.lua:85-110` | track `:95`; center axis `.55,.55,.60,.9` `:97`; loss/gain = `C.DirRGB` `:128/:131`; tooltip gold and `.9` `:105-106` | `chart.track`, `chart.axis`, `sem.loss`, `sem.gain` |
| Ledger caveat | `:141`, gold `:150` | `GameFontDisableSmall` recolored gold | `text.accent` (or `sem.warning`) |

### 2.6 Timeline (`modules/Timeline.lua`, `TimelineModel.lua`)

| Element | Created | Styling today | Primitive / token |
|---|---|---|---|
| Header bar, title, hint | `buildHeader` `:199-214`: title `GameFontNormal` `:203`, hint `GameFontDisableSmall` `:208` | font objects | `text.heading`, `text.muted` |
| Total-only toggle | `makeToggle` `:167-196` (a third copy of the bar button) | backdrop `.1/.24` `:172-173`; box `.24,.24,.27` `:176`; tick gold `:179`; hover gold, rest white `:190/:193` | **Checkbox** (button style) |
| Line chart | `TL:Attach` `:249` → `NS.MakeLineChart` (`core/WidgetsSetup.lua:243`, font `GameFontDisableSmall`) | library `lib.LINE_CHART` axis, grid, crosshair, marker (`libs/LibKa0s/WidgetsLineChart.lua:50-55`); series colors from the host | **Chart**: library chrome (`chart.axis/grid/crosshair`) + host `chart.series` |
| Series colors | `TM.Color` `TimelineModel.lua:230-235`; Total `C.TIMELINE.TOTAL` `:330` | class color, Warband `.25,.75,.95`, other `.7,.7,.72`, Total gold; marker `.8,.8,.8,.6` | `sem.class`, `sem.warband`, `chart.total`, `chart.other`, `chart.marker` |
| Empty and missing messages | `:255`, `:261` `GameFontDisable` | font object | `text.muted` |
| Flow strip and axis | `buildBody` `:231-235`; axis `.45,.45,.5,.8` `:234` | | `chart.axis` |
| Flow bars (pooled) | `makeFlowBar` `:143-151`; `paintFlow` `:341-355` | up = `C.TIMELINE.GAIN`, down = `LOSS`, `.9` alpha | `sem.gain`, `sem.loss` |
| Legend entries (pooled) | `makeLegendEntry` `:153-162`; `RenderLegend` `:427-456` | series color, or `.5` at `DIM_ALPHA` `.4` `:439-441` | `chart.series`, `text.disabled` |
| Hover tooltip | `TL:OnHover` `:527-547` | title gold `:540`; gain and loss rows `:544-545` | **Tooltip** + `sem.gain/loss` |
| Strip and legend tooltips | `Compat.ShowLinesTooltip`/`ShowAmountTooltip`/`ShowTextTooltip` (`core/Compat.lua:629-676`) | gold title `1,.82,0`, body `.9`, hint `.5` | **Tooltip** (centralize these in Compat) |

### 2.7 Holdings (`modules/HoldingsTab.lua`)

| Element | Created | Styling today | Primitive / token |
|---|---|---|---|
| Header cells | `makeHeaderCell` `:437-445` `GameFontNormalSmall` | gold `:441` (`GOLD_R` `:18`, restated) | **SortHeader** |
| Sort arrows | `:304-305` at file load | gold baked | rebuild after a skin change |
| Scroll | `:486` `UIPanelScrollFrameTemplate` | Blizzard | **ScrollBar** |
| Row (pooled) | `makeRow` `:324-357` | stripe `1,1,1,.03` `:328`; hover `1,.82,0,.10` `:330`; detail `GameFontDisableSmall` `:333`; header gold `:337` | **ListRow** (same tokens as 2.3) |
| Cells | `setCell` `:388-391` default white; quality `:395/:398`; holder class or Warband `.4,.78,1` `:308`; total `.85` `:415`; stale age `.5`/`.85` `:417-418` | `sem.quality`, `sem.class`, `sem.warband`, `text.body`, `text.muted` |
| Group header | `bindHeader` `:423-432` | chevrons gold; count `|cff808080` | `text.heading`, `text.muted` |
| Row menu | reuses `BrowserTable:ShowMenu` `:346`; "Forget" `|cffff5555` `:284` | | `sem.danger` |
| Tooltips | `HT.ShowTooltip` `:263-268` through Compat | | **Tooltip** |

### 2.8 Settings panel (`settings/`)

The canvas, tab strip, AceGUI widgets, scroll patch, Defaults button, Profiles page and Keybindings
tab are LibKa0s-Options' (`settings/OptionsSetup.lua:189`) and draw inside Blizzard's Settings
frame. The host draws only these:

| Element | Created | Styling today | Primitive / token |
|---|---|---|---|
| Landing logo | `Panel.lua:23-24`, passed `:910-911` | addon art | leave as is (branding) |
| AH price table host | `Panel.lua:811`; header `GameFontNormalSmall` gold `GOLD_RGB = .91,.77,.42` `:566`, `:832-834` | a different gold from everywhere else | `text.heading` |
| AH price rows (pooled slots) | `:844-860`; `paintAuctionRow` `:696-722` | addon `.86`/`.5` `:708`; module `.9`/`.5` `:711`; status `STATUS_RGB` `:583-587`; info vertex `1`/`.55` `:722` | `text.body`, `text.disabled`, `sem.ok/warning/danger` |
| Tick marks | `TICK_ON/OFF` `:600-603` at file load | status tint baked into `IconMarkup` | `sem.ok`, `sem.danger` (rebuild) |
| Info tooltip | `:643-652` | title white | **Tooltip** |
| Quality threshold option labels | `core/Constants.lua:166-180` at file load | `|cff<qualityHex>` | `sem.quality` (Blizzard-owned, keep) |

### 2.9 Popups, chat and the launcher

- **StaticPopupDialogs** (`settings/Slash.lua:7-160`: PURGE, PRUNE, FORGET_HOLDER, RESETALL,
  CLEAR_BLACKLIST, CLEAR_WHITELIST, CLEAR_CURRENCY, CLEAR_FILTERS, LEDGER_RESET, LEDGER_RESET_CONFIRM).
  They use Blizzard's StaticPopup frames, and the only color is the inline `|cffffd100` in
  LEDGER_RESET (`:119-127`). Restyling `StaticPopup1..4` affects every addon and risks taint, so a
  **Dialog** primitive would mean replacing them with addon-owned frames. That is a scope decision.
- **Chat** uses the printer's cyan `[LH]` (`core/Namespace.lua:18`). Chat is not a frame, so leave it.
- **Launcher**: the LibDBIcon button and LDB tooltip are LibKa0s-Launcher's (`core/LauncherSetup.lua:134`).
  The host adds one gray line, `.7` (`:206`). The minimap art is the addon logo (`:50-51`).
- **GameTooltip** is a shared global. The facade should only color the **lines** the addon adds
  (`text.title`, `text.body`, `text.muted`) and never restyle the tooltip's backdrop.

### 2.10 Library-drawn surfaces the host cannot reach today

| Surface | Where | Host hook |
|---|---|---|
| Debug console and its copy window | `core/DebugLogSetup.lua:159-161` | `applySkin` exists and routes through `B:ApplySkin` |
| Export copy window | `modules/Export.lua:374` | `applySkin` exists |
| Simulation step panel | `libs/LibKa0s/SimPanel.lua:377`, `:669` (`core.ApplySkin(frame)` with the default skin) | **none**; needs a descriptor `skin`/`applySkin` |
| Performance panel | `libs/LibKa0s/PerfPanel.lua:237` | **none** |
| Dropdown, SearchBox, Autocomplete, TestStrip, ReorderList | `libs/LibKa0s/Widgets.lua:85` file-local `SKIN` | **none**; needs per-instance or per-addon skin |
| LineChart chrome | `libs/LibKa0s/WidgetsLineChart.lua:50-55` `lib.LINE_CHART` | read-only shared table; needs per-instance opts |
| Settings canvas and AceGUI | LibKa0s-Options + Blizzard | out of scope for a per-addon skin |

## 3. Hardcoded colors and fonts

There are 50 `SetTextColor` calls across `core/`, `modules/` and `settings/` (Analytics 14,
BrowserTable 11, Panel 6, CoreSetup 4, Timeline 4, Browser 3, HoldingsTab 3, and the rest), plus
about 40 `SetColorTexture`/`SetVertexColor`/`SetBackdrop*Color` calls.

The **Kind** column separates two things:

- **chrome**: the frame's look. It changes with the skin.
- **sem**: the color carries meaning (quality, gain or loss, class, a series identity). It comes
  from the skin's semantic block, defaults to today's values, and a skin should change it only
  deliberately.

| Where | Value | Meaning | Kind | Token |
|---|---|---|---|---|
| `Core.SKIN` (`libs/LibKa0s/Core.lua:92-107`) + degraded copy `core/CoreSetup.lua:224-243` | bg `.06,.06,.08,.92`; border `0,0,0,1`; inner and divider `.24,.24,.27,.85`; title `1,.82,0` | window edge | chrome | `chrome.bg/border/innerBorder/divider`, `text.title` |
| `Browser.lua:16-24` `SKIN` | tabActive `1,.82,0`; tabIdle `.7,.7,.72`; heights | tab labels and underline | chrome | `chrome.tabActive/tabIdle` (heights stay layout constants) |
| `BrowserTable.lua:33`, `HoldingsTab.lua:18` `GOLD_R/G/B` | `1,.82,0` | header, group header, arrows, chevrons | chrome | `text.heading` |
| `Panel.lua:566` `GOLD_RGB` | `.91,.77,.42` | AH table header (an off-gold) | chrome | `text.heading` |
| `BrowserTable.lua:753`, `HoldingsTab.lua:328` | `1,1,1,.03` | row stripe | chrome | `chrome.rowStripe` |
| `BrowserTable.lua:758`, `HoldingsTab.lua:330` | `1,.82,0,.10` | row hover | chrome | `chrome.rowHover` |
| `BrowserTable.lua:1209-1210` | `.06,.06,.08,.98` / `.62,.5,.18,1` | row menu bg and border | chrome | `chrome.menuBg/menuBorder` |
| `BrowserTable.lua:1288` | `1,.82,0,.15` | menu hover | chrome | `chrome.menuHover` |
| `BrowserTable.lua:1300/:1304`; `:1150`, `:1146` | `.9` / `.5` | enabled or disabled text; default cell | chrome | `text.body`, `text.disabled` |
| `BrowserFilterBar.lua:335-336`, `Export.lua:423-424`, `Timeline.lua:172-173` | `.1,.1,.12,.9` / `.24,.24,.27,.9` | control bg and border (three copies) | chrome | `chrome.controlBg/controlBorder` |
| `BrowserFilterBar.lua:343`, `Export.lua:431` | vertex `.85` | button icon | chrome | `chrome.icon` |
| `BrowserFilterBar.lua:350/:357`, `Export.lua:436-437`, `Timeline.lua:190/:193` | `1,.82,0` / `1,1,1` | button label hover and rest | chrome | `text.accent`, `text.body` |
| `Timeline.lua:176/:179` | `.24,.24,.27,1` / `1,.82,0,1` | toggle box and tick | chrome | `chrome.checkBox`, `chrome.checkMark` |
| `Analytics.lua:65-66` | `.1,.1,.12,.85` / `.24,.24,.27,.9` | KPI card | chrome | `chrome.cardBg/cardBorder` |
| `Analytics.lua:76` | `1,.82,0` | KPI number | chrome | `text.accent` |
| `AnalyticsCharts.lua:216-217` | `.08,.08,.10,.6` / `.24,.24,.27,.7` | list panel | chrome | `chrome.panelBg/panelBorder` |
| `AnalyticsCharts.lua:182, 201, 220`; `AnalyticsLedger.lua:150` | `1,.82,0` | section and panel headings, caveat | chrome | `text.heading` |
| `AnalyticsCharts.lua:192/:195` | `1,.82,0,.35` | section rule | chrome | `chrome.sectionRule` |
| `AnalyticsCharts.lua:41, 75`; `AnalyticsLedger.lua:95` | `1,1,1,.06` | bar track | chrome | `chart.track` |
| `AnalyticsCharts.lua:345`; `Timeline.lua:234`; `LINE_CHART.AXIS` | `.45,.45,.5,.8` | axis line | chrome | `chart.axis` |
| `AnalyticsLedger.lua:97` | `.55,.55,.60,.9` | back-to-back center axis | chrome | `chart.axis` |
| `AnalyticsCharts.lua:128` | `.40,.60,.95,.9` | day or hour strip fill (same as `LINE_CHART.LINE`) | chrome | `chart.bar` |
| `AnalyticsCharts.lua:135, 170, 256, 283, 393` | `.7,.7,.72` / `.8,.8,.82` | axis label, legend, value | chrome | `text.muted` |
| `HoldingsTab.lua:415, 418` | `.85` / `.5` | totals, stale age | chrome | `text.body`, `text.muted` |
| `Panel.lua:708, 711, 722` | `.86/.9/1` vs `.5/.55` | live vs inactive AH row | chrome | `text.body`, `text.disabled` |
| `Compat.lua:634-635, 645-648, 659, 674` | `1,.82,0` / `.9` / `.5` | tooltip title, body, hint | chrome | `text.title`, `text.body`, `text.muted` |
| `Browser.lua:605-608` `TEST_MARK`/`SIM_MARK` | `1,.15,.15` / `.3,.8,1` | degraded mode badge | sem | `sem.modeTest/modeSim` |
| `Constants.lua:113-117` `C.DirRGB` | IN `.35,.80,.45`; OUT `1,.33,.33`; MOVE `.62,.62,.66` | gain, loss, transfer (shared with BankLedger) | **sem** | `sem.gain`, `sem.loss`, `sem.transfer` |
| `Constants.lua:123` `C.GOLD_RGB` | `1,.86,.55` | gold-row amount | **sem** | `sem.gold` |
| `LedgerFormat.lua:35-44` | `|cff40ff40`, `|cffff4040`, `|cff808080` | signed counts and money (**not** `DirRGB`) | **sem** | `sem.gain/loss/neutral` (unify with DirRGB) |
| `Constants.lua:358-368` `C.TIMELINE` | TOTAL `1,.82,0,1`; WARBAND `.25,.75,.95`; OTHER `.7,.7,.72`; MARKER `.8,.8,.8,.6`; GAIN and LOSS = DirRGB | Timeline series | **sem** | `chart.total`, `sem.warband`, `chart.other`, `chart.marker` |
| `HoldingsTab.lua:308` | `.4,.78,1` | Warband label (differs from `C.TIMELINE.WARBAND`) | **sem** | `sem.warband` (unify) |
| `BrowserTable.lua:45-51` `BOUND_STYLE` | UNBOUND `.6,.6,.6,.4`; BOE `.92,.92,.92,.95`; BOP `.30,.82,.42`; WARBAND `.30,.58,.98`; WARBAND_UE `.95,.52,.12` | bind state lock | **sem** | `sem.bound.*` |
| `AnalyticsFormat.lua:71-75` `BOUND_COLOR` | BOP `.85,.45,.45` (reddish), BOE `.55,.80,.60` (green) … | bound chart | **sem** | `sem.bound.*`. Note the conflict: BoP is green in the table and red in Insights |
| `AnalyticsFormat.lua:43-63` `SOURCE_COLOR` | 36 per-source triples | source identity | **sem** | `chart.source[key]` |
| `AnalyticsFormat.lua:124-131` `PALETTE` | 21 triples (three 7-hue ramps) | ranked categorical series | **sem** | `chart.series[1..21]` |
| `AnalyticsFormat.lua:28` `NEUTRAL` | `.55,.62,.72` | "Other" segment and fallback | **sem** | `chart.other` |
| `AnalyticsFormat.lua:96-107` | class or quality fallback `.7,.7,.72` / `.6` | missing class or quality | sem | fallback only |
| `ITEM_QUALITY_COLORS`, `RAID_CLASS_COLORS` (many sites) | Blizzard | quality, class | **sem (Blizzard)** | `sem.quality`, `sem.class`: pass through and do not reskin by default |
| `Panel.lua:583-586` `STATUS_RGB` | `.30,.95,.35` / `1,.82,.10` / `1,.32,.32` | collecting, not collecting, missing | **sem** | `sem.ok/warning/danger` |
| `BrowserTable.lua:1263`, `HoldingsTab.lua:284` | `|cffff5555` | destructive menu item | **sem** | `sem.danger` |
| `Slash.lua:119-127` | `|cffffd100` | popup emphasis | chrome | `text.accent` |
| Fonts | `GameFontNormal(Small/Large/Huge)` = gold heading; `GameFontHighlightSmall` = body; `GameFontDisable(Small/Large)` = muted; `C.FONT_MONO` (JetBrains Mono) for the dir glyph, copy box and console | | chrome | `font.title`, `font.heading`, `font.body`, `font.muted`, `font.accent`; `font.mono` must stay mono (`Constants.lua:118-120`) |

## 4. Creation and refresh: where to skin

| Surface | Build | Refresh | Skin at build | Repaint on skin change |
|---|---|---|---|---|
| Window shell | lazy `EnsureFrame` `Browser.lua:921`, first `B:Show` | `SelectTab` `:155` recolors the tabs each time | `B:ApplySkin(frame)` `:1089` (already a seam) | re-run `B:ApplySkin(frame)`; recolor the tabs through `SelectTab`'s loop (`:166-171`), which must read tokens, not `SKIN.tabActive` |
| Tabs | `LayoutTabButtons` `:251`, created once per tab | `SelectTab` | underline color at `:267` | underline `SetColorTexture` |
| Filter bar | once in `BuildFilterBar` `:397` | `LayoutFilterBar` geometry only | `makeBarButton` | walk `self._barCtl`; dropdowns through the library |
| History rows | **pooled**: `BuildRow` via `NS.Pool.Acquire` `:740-742`; `Bind` `:1072` releases all rows and reacquires the visible ones on every scroll or refresh | `BindRow`/`PaintCell` repaint **text** colors on every bind | stripe and hover in `BuildRow` (`:751-758`) | text is free (next `Bind`); stripe and hover need a walk over `rowPool.free` + `rowPool.active` (Pool exposes both, `libs/LibKa0s/Pool.lua:61-62`), or move stripe and hover tint into `BindRow` |
| Header cells | `BuildHeaderCells` `:1010` creates once and reuses, called on every `Bind` | `UpdateHeaderArrows` `:991` re-sets text | `MakeHeaderButton` | recolor `header.buttons[*]`; **rebuild `ARROW_ASC/DESC`** (file-load constants `:326-327`) |
| Row menu | lazy singleton `EnsureRowMenu` `:1203`; buttons pooled in `m.buttons` | `ShowMenu` recolors enabled and disabled text per show | backdrop in `EnsureRowMenu` | re-backdrop `rowMenu`; hover textures on `m.buttons` |
| Insights | `Attach` once (lazy via `BuildPane`); `BuildCharts` creates headers, dividers, panels and 30+ pools | `Refresh` → `Layout` → `LayoutCharts` releases every pool and re-colors fills, labels and values per render | factories `makeBar`, `makeSwatch`, … | track, axis and strip fill are set in the factories only, so walk the pools or move them into the renderers; cards, headers and dividers need a direct walk (`self.cards`, `self.headers`, the dividers, `ledgerUI`) then `Refresh()` |
| Timeline | `Attach` once; strip and legend pools | `Refresh` releases and re-renders the strip and legend each time | `makeToggle`, `buildBody` | re-skin the toggle and strip axis; the chart needs a library re-chrome call; then `TL:Refresh()` |
| Holdings | `Attach` once; `self.rows` pool | `HT:Refresh` releases and reacquires every row and repaints cell text | `makeRow` (stripe, hover, header gold) | walk the pool for stripe, hover and header color; recolor header cells; rebuild the arrows (`:304-305`) |
| Export modal | lazy `EnsureFrame` `Export.lua:453` | `E:Open` per open | `B:ApplySkin(frame)` `:530` | re-run it; recolor `titleFS` and `csvBtn` |
| AH price table | raw host, pooled slots, parked across tab switches (`OptionsSetup.lua:27-32`) | `paintAuctionRow` per refresh | | header gold walk; rebuild `TICK_ON/OFF` (`Panel.lua:600-603`) |

**Live repaint hook.** Nothing re-skins today. The obvious path:

1. The skin row's `onChange` sends `NS.MSG.SETTINGS_CHANGED, "skin"`. That is how `settings.scale`,
   `settings.alpha` and `settings.locked` already notify (`Schema.lua:192-209`).
2. `B:OnSettingsChanged` (`Browser.lua:1240`) already receives `SETTINGS_CHANGED` and calls
   `NS.Export:ApplyChrome()`. Add a `B:ApplySkinAll()` that re-skins the window, tabs, filter bar
   and menu, then calls each tab spec's new `reskin()` (the registry `B:RegisterTab` `:277` is the
   natural fan-out), then rebuilds the file-load markup constants and refreshes the visible tab.
3. `B:AdoptProfile` (`Browser.lua:823`, reached from `NS.OnProfileEvent`, `core/LootHistory.lua:95-104`)
   must re-skin too, because the skin is per profile.
4. The bus target `B.__ev` exists only while the addon is enabled (`B:Enable` `:1271`). A skin
   changed while stood down is applied at the next `EnsureFrame` or `AdoptProfile`, which read the
   setting fresh.
5. The library windows (debug console, copy windows, sim panel, perf panel) need a LibKa0s-side
   re-skin entry. The two with `applySkin` hooks re-skin only when a frame is built.

## 5. Settings panel, defaults and migrations

- **Declaration.** `settings/Schema.lua` builds one array `S.Schema` (`:503-505`): the composed Master
  controls rows (`O.MasterControls{…}` `:76-142`, stamped `:152-230`) spliced first, then `ROWS`.
  Each row carries `page = "General"`, `group = <tab>` and optionally `subgroup`. `OptionsSetup.lua`
  gives the library a descriptor (`rowsForPage`, `get`/`set` → `NS.Schema`, `buildMain` → Panel).
  `Panel.lua` registers one subcategory, "General" (`:1131-1171`, page at `:1144`), whose renderer `renderGeneral`
  (`:1051-1104`) draws `O.TabStrip` from `GENERAL_TABS` (`:986-1007`) and renders the active
  group's rows via `renderGroupRows` (`:1027-1039`), or a custom `build` (Filters, Keybindings).
  The Profiles page is the library's (`Panel.lua:1164`).
- **Current tabs:** Master controls, Capture, Filters, AH price, Interface, History, then
  Keybindings, which is always last (options-ui-§20). Master controls is always first
  (options-ui-§15).
- **Where Appearance goes:** a new `{ key = "Appearance" }` in `GENERAL_TABS`, probably straight
  after **Interface** (both are about the window), with its rows declared contiguously in `ROWS`
  right after the Interface block (`Schema.lua:369-444`). It needs at least two rows to pass
  `test_schema.lua:719`, for example `settings.skin` (dropdown of nine skins plus "EllesmereUI")
  and a second real control (a "follow EllesmereUI when present" checkbox, a font-size or
  background-opacity override, or a "Preview" button). Check the standard before naming the tab:
  if options-ui does not name an Appearance tab, a collection-wide rule belongs upstream in
  WowAddonStandards rather than in this addon.
- **Profile defaults.** `defaults/Profile.lua:10-72`. Add `settings.skin = "<default skin id>"` (and
  any sibling keys) there. A new key with a default needs **no migration**: AceDB merges it into
  every profile, as with `sim.stepDelay` (`Profile.lua:52-55`).
- **Migrations.** These are account-wide: `db.global.schemaVersion` (floor `0` at
  `defaults/Global.lua:18`), steps appended to `MIGRATIONS` (`core/Database.lua:245`), the runner
  at `:399-411`, and `NS.SCHEMA_VERSION = 14` (`:390`). No step is profile-scoped
  (`docs/schema.md:422`). A skin key needs none, unless the default skin is ever **renamed**. In
  that case use a v15 step that rewrites the raw profiles, the pattern v12 and v14 used.
- **Existing `alpha`.** The Master controls row `settings.alpha` (composed; stamped `Schema.lua:198-203`,
  default `1.0`) is applied as `frame:SetAlpha(alpha)` to the History window and Export modal only
  (`Browser.lua:1125-1130`, `Export.lua:586-588`), together with `settings.scale` ×
  `settings.windowScale`. It is whole-frame opacity, so a skin's `chrome.bg` alpha multiplies
  under it. Keep the two separate, and say so in `settings-panel.md`.
- **Reset paths.** Every schema row is reset by Defaults, `/lh reset`, `/lh resetall` and profile
  reset for free, and `/lh get|set settings.skin` works through `Schema:Get/Set` with no extra code.
  Give the row a `values` table so `set` validates input.

## 6. Tests

- **The harness.** `tests/run.lua` + `tests/wow_mock.lua` over the kit's `mock_base.lua`. Frames are
  catch-all stubs that record script handlers (`__fire`). The local mock adds FontStrings that
  record `SetTextColor` into `fs.__color` (`wow_mock.lua:308-312`), sizes, `SetPoint`, and
  whitelisted `RAID_CLASS_COLORS`/atlas sets. Suites spy on other setters with `rawset`
  (`SetColorTexture` → `__ct` in `test_analytics_layout.lua:37`, `SetBackdropBorderColor` in
  `test_widgets.lua:570-574`, `SetVertexColor` in `test_panel_auction.lua:34`).
- **Suites that pin visuals** (any default-skin drift turns these red):
  - `test_analytics_layout` with `analytics_golden.txt`: every pooled widget's text color and fill
  - `test_panel_auction` with `panel_auction_golden.txt`: status colors
  - `test_widgets`: menu row gold or `.5` (`:77-81`, `:188`), search focus border gold (`:613`)
  - `test_browsertable:62`: the BOUND_STYLE lock markup
  - `test_ledgerformat`: DirRGB and GOLD_RGB
  - `test_constants:365`: DirRGB arity
  - `test_timeline:377` and `test_timelinetab:516`: gold Total title, class line colors
  - `test_mediasetup:181-183`: IconMarkup tint
  - `test_browser`: `B.SKIN.minH`
  - `test_teststrip`, `test_layers`, `test_debuglog` (applySkin routed through `B:ApplySkin`),
    `test_surface_parity`
- **Source-grep tests are the house style** (`test_layers.lua:70` "no strata literal…",
  `test_panel.lua:799-802`), and a skin gate fits that style.
- **Natural new suites:**
  - `tests/test_skin_seam.lua`: the seam resolves the active skin from `settings.skin`, falls back
    to the default for an unknown id, uses EllesmereUI only when present, has a degraded arm with no
    library, and gets a `test_surface_parity` case.
  - `tests/test_skin_tokens.lua`: the default skin reproduces every value in section 3 exactly
    (which keeps the goldens green); every skin defines every token; semantic tokens default to
    `DirRGB`/`GOLD_RGB` and the rest.
  - `tests/test_skin_surfaces.lua`: switching the skin repaints the window edge, tabs, bar buttons,
    pooled rows (free and active), the row menu, cards, list panels, Timeline toggle and Holdings
    rows, and rebuilds the arrow, chevron and tick markup. Drive it through the mock's
    `__color`/`__ct` spies after `Schema:Set("settings.skin", …)`.
  - `tests/test_skin_literals.lua`: a source gate that fails on any color literal in
    `SetTextColor`/`SetColorTexture`/`SetBackdrop*Color`/`|cff` outside the skin seam and an
    allow-list (quality and class pass-through, `Constants` semantic tables). It is falsifiable by
    planting a literal.
  - The Appearance-tab cases go in `test_schema.lua` and `test_panel.lua` (`GENERAL_TABS` order).
- Each new suite is added to the list in `tests/run.lua:61-99`, which `Kit.assertSuiteInventory`
  checks in both directions, and to the `docs/testing.md` suite table.

## 7. The pre-LibKa0s skin in `core/CoreSetup.lua:218-244`

This is the **degraded arm** of the LibKa0s-Core seam. It defines `NS.ApplySkin` only
when `LibStub("LibKa0s-Core-1.0", true)` returns nil (`:44`, `:143`), that is when `libs/LibKa0s` is
missing from the install. The comment at `:218-222` says why it lives here:

- **Load order.** `LibKa0s.xml` loads in the TOC before every addon file (`LootHistory.toc:29`), and
  `core/CoreSetup.lua` is the first LibKa0s seam the TOC loads (`:46-49`). It sits before
  `core/LootHistory.lua` and before every module that takes a load-time upvalue from it
  (`:33-42`). Defining `NS.ApplySkin` on **both** arms here means every caller (`B:ApplySkin`
  `Browser.lua:64`, Export `:530`, the copy window `:374`, the DebugLog closure
  `DebugLogSetup.lua:159`) finds the same name whether or not the library loaded. The DebugLog
  closure resolves `NS.Browser` at frame-build time because `core/` loads before `modules/`
  (`DebugLogSetup.lua:150-153`, `:23`).
- **Drift.** The live arm publishes `lib.ApplySkin` by reference (`:261`). A host copy on the live
  path would drift from `Core.SKIN`, so the copy runs only where the library is absent. It is
  "byte-for-byte the skin modules/Browser.lua applied before the seam existed", so a degraded
  install looks like a working one. The same holds for `fallbackCloseButton` (`:58-73`) and
  `fallbackMakeResizable` (`:82-117`).
- **Effect on the facade.** The skin seam follows the same two-arm shape. With no library, the
  Appearance tab cannot render, because the Options stub draws nothing
  (`OptionsSetup.lua:49-187`). The degraded arm should expose the facade's full name set and
  answer only the default skin, with this copy as its window edge. Do not grow this fallback into a
  second implementation of nine skins.

## Recommended conversion order

1. **The seam and tokens first** (`core/SkinSetup.lua`, or the LibKa0s facade plus a thin seam).
   Start with a default skin that reproduces every value in section 3, `test_skin_tokens`, and a
   parity case. With no surface touched yet, every golden stays green, which proves the default
   is a no-op.
2. **Window edge and title bar**, through the existing `B:ApplySkin` seam (window, Export modal,
   copy window, debug console): four windows for one call site. Fix Export's `titleFS` and its
   missing divider at the same time.
3. **The three bar-button copies** (`BrowserFilterBar.lua:330`, `Export.lua:418`, `Timeline.lua:167`)
   collapse into the **Button**/**Checkbox** primitives. Most of the chrome literals go in this step.
4. **Tabs and the tooltip helpers.** The tabs are `SKIN.tabActive`/`tabIdle`. The tooltips are the
   Compat Show* family plus the direct `GameTooltip:AddLine` sites in BrowserTable, AnalyticsCharts,
   AnalyticsLedger and Timeline.
5. **History table and row menu.** Covers pooled rows (stripe, hover), header gold, the arrows and
   chevrons rebuilt from tokens, and the semantic `DirRGB`, `GOLD_RGB` and `BOUND_STYLE`. Holdings
   follows straight after (same row shape, `GOLD_R` restated).
6. **Insights.** Cards, panels, headers and dividers are chrome. `PALETTE`, `SOURCE_COLOR`,
   `BOUND_COLOR` and `NEUTRAL` move into the skin's `chart` block. Rewrite `analytics_golden.txt`
   only for a deliberate change, in its own commit. Settle the BoP green-or-red conflict as an owner
   call.
7. **Timeline.** Series and flow colors on the host side; the line-chart chrome needs a
   LibKa0s-side per-instance option.
8. **Settings host bits** (AH price header, status colors, tick marks), then the Appearance tab, the
   live repaint hook, and the `AdoptProfile` re-skin.
9. **Library-only surfaces**: Widgets `SKIN`, SimPanel, PerfPanel, LineChart. These are LibKa0s
   work that LootHistory then adopts at a re-vendor.

## Risks

- **The file cap.** Browser.lua and BrowserTable.lua are at about 1325 lines. Inline skin code will
  breach 1500. Put the mapping in a new file.
- **The goldens.** 559 recorded colors in `analytics_golden.txt`, plus the auction golden. Any
  rounding difference in the default skin (for example `0.82` against `0.820`, or alpha written
  where it was omitted) is a diff. `SetColorTexture` arity also matters: the library comment at
  `Core.lua:110-112` warns that collapsing 3 and 4 components drops alpha.
- **File-load markup.** `ARROW_ASC/DESC` (2 files), `TICK_ON/OFF` and `C.QUALITY_OPTIONS` are built
  once at load. The `LedgerFormat` `|cff` escapes are built per call, but inline textures ignore
  `SetTextColor`. A live switch leaves these stale unless they become functions.
- **Pooled frames.** Textures colored only in factories (stripe, hover, track, axis, strip fill)
  keep the old skin on frames sitting in the `free` list. Either walk free and active, or move the
  tint into the bind or render path. The second is cheaper to keep correct.
- **Semantic tokens.** Semantic colors are shared across addons (DirRGB is BankLedger's). A skin
  that retints gain and loss splits the two addons visually. The seam should keep semantic colors
  default-locked unless a skin opts in. Quality and class colors are Blizzard's and should pass
  through untouched.
- **Shared globals.** GameTooltip and StaticPopup are shared. Restyling either reaches other
  addons and can taint. Limit the facade to line colors and to addon-owned dialog frames.
- **Library reach.** The dropdowns, search box, autocomplete, test strip, sim panel, perf panel and
  line chart have no per-addon skin input today. Without LibKa0s changes, "every visual element"
  is not achievable from LootHistory alone.
- **Standards.** An Appearance tab, a per-addon skin setting and EllesmereUI sourcing all need a
  standard home (options-ui, standalone-windows, library-stack-§8). Done only in the addon, each is
  an unratified deviation under this repo's CLAUDE.md.
- **Degraded install.** The stub must answer the facade's whole surface (`test_surface_parity`), or
  a missing library fails late and far from the cause.
