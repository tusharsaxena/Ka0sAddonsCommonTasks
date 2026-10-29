# Inventory: BankLedger (prefix BL)

Read-only inventory for M0 of `docs/2026-10-29-SKINNING_ROLLOUT/00_PLAN.md`, items BL-RV and BL-01..BL-05.
Repo `../BankLedger`, read at the head of `feat/2026-10-29-skinning-rollout` (no commits beyond master), which
vendors LibKa0s v1.77.0 (`CLAUDE.md:48`). The library was read at v1.79.0 (`../LibKa0s` at `4e1ae41`).

BankLedger is LootHistory's closest sibling in the collection: it has the same Browser, pooled table, row menu,
Insights charts, export modal, copy window, debug console and sim panel. Most of its literals are LootHistory's
values, which SkinDefs already holds as tokens, so leg 1's LootHistory recipe applies almost line for line
(`../LootHistory/core/SkinSetup.lua`: `NS.Skin`, `NS.SkinColor`, `NS.SkinEscape`, `NS.SkinBar`,
`NS.QualityColor`, `NS.SkinPaintAce(Tree)`, `NS.SkinOnRelease`, `NS.MaybeShowSkinPicker`, `NS.SKIN_FALLBACK`).

**There is no HUD.** All of BankLedger's output is windows, a modal, a popup menu, tooltip lines and settings
rows. So BL-03 has nothing to do and goes in `exceptions.tsv`, and O2's one-time reset does not apply.

Below, "S" is the owner facade `Skin:For("BankLedger")` (published as `NS.Skin`). A token named in a cell
equals today's literal exactly unless the cell says otherwise.

## 1. Surfaces

### 1.1 The ledger window (`modules/Browser.lua`)

| Surface | Built | Typed today | Paint (rung 1) |
|---|---|---|---|
| Window `BankLedgerWindow` (backdrop, edge, inner rule, title tint, divider) | `Browser.lua:1022`, skinned `:1159` via `B:ApplySkin` `:78` -> `NS.ApplySkin` = `lib.ApplySkin` (`core/CoreSetup.lua:181`) with NO owner | Core.SKIN (library), and the degraded copy `CoreSetup.lua:102-122` (`0.06,0.06,0.08,0.92`, `0,0,0,1`, `0.24,0.24,0.27,0.85`, title `1,0.82,0`) | `S.Shell(frame)`, or `Core.ApplySkin(f, nil, "BankLedger")`: `win.bg`, `win.border`, `win.inner`, `title.text`, `divider`, `title.bg` band. The degraded arm reads `NS.SKIN_FALLBACK` (the LH pattern) |
| Title bar + title FontString | `:1039`, `:1052` (`GameFontNormal`) | gold via ApplySkin | `S.TitleBar(titleBar, { text = title })` or Shell's `frame.title` (`title.text`, `font.title`); see D6 |
| Divider | `:1064` | `0.24,0.24,0.27,0.85` via ApplySkin | `S.Divider(divider)` (`divider`) |
| Test badge (degraded only: shown when no TestStrip was built) | `:1057` | `SetTextColor(1,0.15,0.15)` `:1060` | `S.Color("sem.modeTest")` (exact) and `S.Text`'s font |
| Close button (shared by 3 windows) | `B:MakeCloseButton` `:103` | rest `CLOSE_REST {0.85,0.85,0.85}` `:101`, `:117`, `:128`; hover = player's class color `:110`; glyph `SetFont(STANDARD_TEXT_FONT,24)` `:125` | `S.CloseButton(close)` on the button as built (`close.icon` / `close.glyph`): `close.rest`, `close.hot`. **Changes Ka0s Default's tints**; see D1 |
| Tab strip (History, Insights): labels, 2px underline | `CreateTabStrip` `:259-287`; selection `:244` | `SKIN.tabActive {1,0.82,0}`, `SKIN.tabIdle {0.7,0.7,0.72}` `:24-25`; underline `:277` | LH's way: `S.Text(label, active and "accent" or "muted")` (`text.accent` / `text.muted`, equal to today's values), underline `S.Color("tab.onLine")`. Re-run in `SelectTab` and on `OnLooksChanged`. See D5 |
| Filter-bar dropdowns (Group, Date, Direction, Store, Quality, Type, Sub-type, Character) | `B:MakeDropdown` `:301` -> `W.Dropdown` | library | pass `owner = "BankLedger"` in the opts (Widgets `:541`) |
| Dropdown option colors (Direction, Store, Quality) | `:437`, `:448`; quality labels `core/Constants.lua:243` (hex escapes, `QUALITY_HEX_FALLBACK` `:231`) | `C.DirectionRGB`, `C.StoreRGB`, `ITEM_QUALITY_COLORS` | direction: `sem.good` / `sem.bad`; store: exception E7; quality: `q.*` through an `NS.QualityColor` / `NS.SkinEscape`-style helper. `C.QUALITY_OPTIONS` is built at file load (`Constants.lua:240`), so it has to be rebuilt on `OnLooksChanged` or built lazily |
| Search box | `B:MakeSearchBox` `:318` -> `W.SearchBox` | library | `owner` in opts (Widgets `:670`) |
| Search suggestions (autocomplete) | `B:MakeAutocomplete` `:334` -> `W.Autocomplete`; row colors `suggestColor` `:671-679` | `LT.MONEY_RGB {1,0.91,0.55}`; quality from `ITEM_QUALITY_COLORS` | `owner` in opts (WidgetsAutocomplete `:414`); gold row = gap BL-G1; quality = `q.*` |
| Flat bar buttons (Save / Reset / Clear / Export) | `makeBarButton` `:353` | backdrop `0.1,0.1,0.12,0.9` / `0.24,0.24,0.27,0.9` `:358-359`; label `GameFontHighlightSmall`, hover `1,0.82,0` `:371`, rest `1,1,1` `:379`; tooltip line `0.9` `:374` | `S.Button(b)`: `btn.bg`, `btn.border`, `btn.text`, `btn.hover`, body font; tooltip line `gtip.body` |
| Test / sim strips | `buildModeStrip` `:820` -> `W.TestStrip`; tooltip `:831-832` | library amber / cyan; tooltip title `1,0.82,0`, body `0.9` | `owner` in TestStrip opts (Widgets `:730`, `strip.test` / `strip.sim`); tooltip lines `gtip.title`, `gtip.body` |
| Footers ("Showing X of Y", DB size) | `:1111`, `:1114` (`GameFontDisableSmall`) | template gray (0.5) | `S.Text(fs, "disabled")` (`text.disabled`), as LH `Browser.lua:1064` does. Not `S.Footer`: that adds a `foot.bg` band |
| Resize grip | `NS.MakeResizable` `:1132` -> `Core.MakeResizable` | client art | none: `MakeResizable` takes no owner; geometry and art stay put |

### 1.2 The History table (`modules/LedgerTable.lua`)

| Surface | Built | Typed today | Paint (rung 1) |
|---|---|---|---|
| Header buttons | `LT:MakeHeaderButton` `:667` (`GameFontNormalSmall`) | `HEADER_RGB {1,0.82,0}` `:172`, `:674`; tooltip title `1,0.82,0` `:679`, desc `0.9` `:680` | `S.SortHeaderBar(header, { texts = ... })` or per label `S.Color("list.header.text")` + `S.Font`; tooltip `gtip.title` / `gtip.body` |
| Sort arrows and group expanders (inline `|T` markup, tinted) | `markup` `:151`, `HEADER_TINT` `:173`, `ARROW_ASC/DESC` `:176-177`, `GROUP_SHUT/OPEN` `:181-182` | the tint `1,0.82,0` baked into the escape at FILE LOAD | `list.header.text` from the facade, and the four strings rebuilt in an `OnLooksChanged` listener (they are file-scope today) |
| Header frame (no fill today) | `LT:Attach` `:632` | none | `S.SortHeaderBar` paints `list.header.bg` (Ka0s Default `{1,1,1,0.04}`), which adds a faint band. Either accept it (LH precedent, `BrowserTable.lua:953`) or color only the labels. Folded into D6 |
| Scroll bar (`FauxScrollFrameTemplate`) | `:640` | client art | `S.ScrollBar(scroll.ScrollBar)` (`scroll.track`, `scroll.thumb`), as LH `BrowserTable.lua:969` does |
| Pooled rows: stripe and hover | `LT:BuildRow` `:485-500`; `NS.Util.ApplyRowTint` `core/Util.lua:165-174` | stripe `1,1,1,<rowStripeAlpha>`, hover `1,0.82,0,<rowHoverAlpha>` (player settings, defaults 0.03 / 0.10) | RGB from `list.stripe` / `list.hover`, alpha per D2 |
| Cells | `:506` (`GameFontHighlightSmall`), painters `:422-477` | item/quality `ITEM_QUALITY_COLORS` `:417`, gold `MONEY_RGB` `:426`; direction `C.DirectionRGB` `:435`; store `C.StoreRGB` `:446`; char `RAID_CLASS_COLORS` or `0.9` `:454`; others `0.9` `:476` | `S.Font(fs)` once at build (face only); colors at bind: `q.*`, gap BL-G1, `sem.good` / `sem.bad`, E7, E3 (class) with fallback `text.body`, `text.body` |
| Direction glyph (mono) | `:514-515` `SetFont(C.FONT_MONO, 12)` | JetBrains Mono, color = the direction's | stays `C.FONT_MONO` (E10); color `sem.good` / `sem.bad` |
| Group header row | `:523-525` (`GameFontNormalSmall`), count escape `|cff808080` `:806` | `HEADER_RGB` | `S.Color("list.header.text")` + font; the count `NS.SkinEscape("text.disabled")` (rounds to `808080`) |
| Empty text | `:657` (`GameFontDisableLarge`) | template | `S.Text(empty, "disabled")` |
| Row tooltips | `:533-546` | hint `0.5` `:537`, `:545`; gold title `MONEY_RGB` `:543`; Amount `0.9` and `1,1,1` `:544` | `gtip.muted`; gap BL-G1 (or `gtip.title`, see D4); `gtip.body` / `gtip.value`. Item hyperlink tooltip: E1 |
| Row context menu (popup, UIParent) | `EnsureRowMenu` `:832-838` | `menu` backdrop `0.06,0.06,0.08,0.98`, edge `0.62,0.5,0.18,1` | `S.MenuFrame(rowMenu, { alt = true })` (`menu.bg`, `menu.borderAlt`), as LH `BrowserTable.lua:1255` does |
| Menu entries | `:906-927` | hl `1,0.82,0,0.15` `:914`, text `0.9` `:922`, disabled `0.5` `:926`; Delete `|cffff5555` `:890` | `menu.hover`, `menu.text`, `text.disabled`, `NS.SkinEscape("sem.danger")`; `S.Font` on each entry |

### 1.3 The session window (`modules/SessionWindow.lua`)

| Surface | Built | Typed today | Paint (rung 1) |
|---|---|---|---|
| Window `BankLedgerSessionWindow` | `:534`, skinned `:625-630` (degraded arm: bare `SetBackdrop`) | as the ledger window | `S.Shell` / owner ApplySkin; title bar `:547`, title `:560`, divider `:565`, close `:572` as in 1.1 |
| Header cells | `BuildHeaderCells` `:446-462` | `1,0.82,0` `:453`; tooltip `1,0.82,0` / `0.9` `:458-459` | `list.header.text` (or `S.SortHeaderBar`); `gtip.title`, `gtip.body` |
| Scroll bar (Faux) | `:591` | client art | `S.ScrollBar(scroll.ScrollBar)` |
| Pooled rows: stripe, hover, cells, glyph | `SW:BuildRow` `:342-380` | same as 1.2 (`ApplyRowTint`, `GameFontHighlightSmall`, `C.FONT_MONO`) | same as 1.2; cells colored by the shared `LT:PaintCell` |
| Row tooltip (gold) | `:397-399` | `1,0.91,0.55` (a second literal copy of MONEY_RGB), `0.9`, `1,1,1` | gap BL-G1 / `gtip.body` / `gtip.value` |
| Sim strip | `buildStrip` `:483-485`; tooltip `:493-494` | library cyan; `1,0.82,0` / `0.9` | `owner` in TestStrip opts; `gtip.title`, `gtip.body` |
| Empty text | `:608` | template | `S.Text(empty, "disabled")` |

### 1.4 Insights (`modules/Insights.lua`, `modules/InsightsWidgets.lua`)

| Surface | Built | Typed today | Paint (rung 1) |
|---|---|---|---|
| Pane scroll (`UIPanelScrollFrameTemplate`) | `Insights.lua:122` | client art | `S.ScrollBar(scroll.ScrollBar)` (LH `Analytics.lua:59`) |
| KPI cards | `W.MakeCard` `InsightsWidgets.lua:397-437` | `0.10,0.10,0.12,0.85` / `0.24,0.24,0.27,0.90` `:401-402`; value `GameFontNormalHuge` gold `:407`, `:412`; caption `GameFontDisableSmall` `:416`; shrink-to-fit `SetFont(card.fontFile, …)` `:445-449`; tooltip gold / `0.9` `:431-432` | `S.Card(card, { title = value })` (`card.bg`, `card.border`, `text.heading`); caption `S.Text(caption, "disabled")`; tooltip `gtip.title` / `gtip.body`. The shrink pass has to re-read the base font after the paint and on every `OnLooksChanged` (R4) |
| Section headers | `W.MakeSectionHeader` `:824-829` | `GameFontNormal`, `W.GOLD` | `S.Text(fs, "heading")` |
| Section dividers (title plus two rules) | `W.MakeSectionDivider` `:833-852` | `SetFont(file, size*1.5)` `:838`; gold `:840`; rules `W.GOLD, 0.35` `:844`, `:849` | `S.Text(fs, "heading")`, then the 1.5x size from the skinned size; rules `S.Divider(line, { token = "section.rule" })` (`{1,0.82,0,0.35}`, exact) |
| Bars (ranked list): fill, track, label, value | `W.MakeBar` `:456-475`; colored `Insights.lua:272-280` | track `1,1,1,0.06` `:464`; fill `color, 0.95` (`Insights.lua:273`); label = bar color; value `W.MUTED {0.8,0.8,0.82}` | fill `S.BarTexture(fill, r, g, b, 0.95)` (LH `NS.SkinBar`); track `chart.track`; value `text.value`; label font `S.Font`. Fill colors: `chart.series` (PALETTE `:51-58` is exactly SERIES), `chart.other` (`W.NEUTRAL`), `sem.good` / `sem.bad`, E7 stores, `q.*`, E3 class |
| Stacked bars + segments | `W.MakeStackedBar` `:576-605`; segments `:631` | track `:584`; `spec.color, 0.95` | same; segment `S.BarTexture` |
| Back-to-back bars | `W.MakeBackToBackBar` `:647-679`; `:709` | track `:655`, baseline `0.55,0.55,0.60,0.9` `:658` | `chart.track`, `chart.axisAlt` (exact), `S.BarTexture` |
| Headline split bar | `W.MakeSplitBar` `:506-537`; `:562`, `:569-571` | track `:510`, baseline `:513`, sides `color, 0.9`, side texts = side color | `chart.track`, `chart.axisAlt`, `S.BarTexture`; sides are `sem.good` / `sem.bad` |
| Day / hour strips: bar, axis label, axis line | `W.MakeStripBar` `:721-743`; `stripAxisLine` `Insights.lua:377-385` | fill `0.40,0.60,0.95,0.9` `:725`; label `0.7,0.7,0.72` `:731`; axis `0.45,0.45,0.5,0.8` | `chart.bar` (exact, BarTexture with its color), `text.muted`, `chart.axis` (exact) |
| Legend swatches | `W.MakeSwatch` `:806-822`; `Insights.lua:354` | swatch `color, 0.95`; label `0.8,0.8,0.82` `:814`; tooltip `W.MUTED` `:819` | swatch: flat `SetColorTexture` from the same token color (a 10px legend chip, no bar texture); label `text.value`; tooltip gap BL-G2 |
| Ranked-list panels + rows | `W.MakeListPanel` `:759-772`; `W.MakeListRow` `:785-800`; colored `Insights.lua:452-463` | `0.08,0.08,0.10,0.60` / `0.24,0.24,0.27,0.70` `:763-764`; title `GameFontNormalSmall` gold `:767`; name `row.nameColor or W.MUTED`; right `W.MUTED` | `S.Panel(p)` (`panel.bg`, `panel.border`, exact); `S.Text(title, "heading")`; name `q.*` / E3 / `text.value`; right `text.value` |
| Cursor tooltip lines | `W.CursorTooltip` `:375-389`, callers `:473`, `:604`, `:677` (`W.GOLD`), `:522`, `:599`, `:673`, `:799` (default `{1,1,1}`), strip bar `:737` (`1,1,1`) | gold, white | `gtip.title`, `gtip.value` |
| Signed money / count escapes | `W.SignedMoney` / `W.SignedCount` `:122-136` | `|cff808080`, `|cff40ff40`, `|cffff4040` | `NS.SkinEscape("text.disabled" / "sem.goodAlt" / "sem.badAlt")`, each rounds to today's bytes (LH's LedgerFormat used the same pair) |
| Quality / class fallbacks | `W.QualityColor` `:95-99`, `W.ClassColor` `:101-105` | fallbacks `{0.60,0.60,0.62}`, `{0.70,0.70,0.72}` | `q.*` with `sem.unknown` (D9); `text.muted` (exact) |
| Empty text | `Insights.lua:162` | `GameFontDisableLarge` | `S.Text(fs, "disabled")` |

### 1.5 Export modal and copy window (`modules/Export.lua`)

| Surface | Built | Typed today | Paint (rung 1) |
|---|---|---|---|
| Modal `BankLedgerExportWindow` | `:371`, skinned `:446` | ApplySkin (no owner) | `S.Shell(frame, { noTopBar = true })` + `S.TitleBar(tbar, { text = t })`: the modal's bar is 26px (`:388`), not `title.height` 30, so Shell's top band would overhang it (D6; LH `Export.lua:485` does the TitleBar) |
| Title, close | `:391`, `:395` | gold; class-color close | as 1.1 |
| Data set dropdown | `:406` via `B:MakeDropdown` | library | `owner` (through `B:MakeDropdown`) |
| "Export to CSV" button + mark | `makeButton` `:334-358` | `0.1,0.1,0.12,0.9` / `0.24,0.24,0.27,0.9` `:339-340`; mark `0.85` `:347`; label hover `1,0.82,0` / rest `1,1,1` `:354-355` | `S.Button(b)` (`btn.*`; `b.icon` takes `btn.icon` 0.85, exact) |
| CSV copy window | `ensureCopyWindow` `:279-298` -> `W.CopyWindow` | library; passes `applySkin` `:287` | **drop `applySkin`**: WidgetsCopyWindow `:153` gives the owner path (`d.addonName`) only when `applySkin` is absent |

### 1.6 Library tool surfaces this addon configures

| Surface | Where | Today | Owner-aware change |
|---|---|---|---|
| Debug console + its copy window | `core/DebugLogSetup.lua:81-160` | passes `applySkin` `:142` (and `addonName`) | **drop `applySkin`**: DebugLog `:305` makes the console an owned window only when `d.skin == nil and d.applySkin == nil` |
| Sim step panel | `modules/Sim.lua:405-423` (`name = addonName`) | library | none: SimPanel minor 7 picks up the registered owner by name |
| Perf panel | none | the addon holds the performance-§12 exemption | nothing |
| Launcher tooltip line | `core/LauncherSetup.lua:284` | `AddLine(…, 0.7,0.7,0.7)` | `gtip.subtle` (exact; LH's same line) |
| Minimap button | LibDBIcon | third-party | E5 |

### 1.7 Settings page widgets the addon acquires itself

All on the owned General page (`settings/Panel.lua`); the library paints its own makers' rows. Each of these needs
`Skin:PaintAce(owner, w)` / `PaintAceTree` (LH `settings/Panel.lua:39`, `settings/Profiles.lua:69`):

- `makeMultiCheck`: SimpleGroup `:78`, a CheckBox per store `:82`.
- `makeClearAll`: SimpleGroup `:257`, Button "Clear all…" `:259`.
- `makeFilterSection`: Label `:373`. The IdList's `emptyText = "|cff808080(none)|r"` `:406` becomes `NS.SkinEscape("text.disabled")`.
- Filters sub-strip host: SimpleGroup `:460` (layout nil, raw `O.SubTabStrip` buttons on it: the library's).
- `settings/Profiles.lua:53`: the SimpleGroup AceConfigDialog fills, so `PaintAceTree(container)` after it fills.

No host `OnRelease` is set on any of them (grep finds none), so nothing needs chaining through `Skin:OnRelease` today.

### 1.8 Out-of-window text

- Chat prefix `NS.PREFIX = "|cff00ffff[BL]|r"` (`core/Namespace.lua:18`) and the disabled line `|cFFFFFF00` (`settings/Slash.lua:292`): chat output, not a frame the addon draws. Left as they are (E9).

## 2. Library factories that take an owner

| Factory | Call site(s) | What to pass |
|---|---|---|
| `Core.ApplySkin(frame, skin, owner)` | `NS.ApplySkin` = `lib.ApplySkin` (`core/CoreSetup.lua:181`), reached from `Browser.lua:79` (all 3 windows plus the two applySkin hooks) | `(f, nil, "BankLedger")`, or replace it with `S.Shell` |
| `W.Dropdown(parent, width, opts)` | `Browser.lua:303` (8 filter dropdowns plus the export modal's data set) | `opts.owner` |
| `W.SearchBox(parent, nil, opts)` | `Browser.lua:322` | `opts.owner` |
| `W.Autocomplete(editBox, opts)` | `Browser.lua:338` | `opts.owner` |
| `W.TestStrip(frame, opts)` | `Browser.lua:823`, `SessionWindow.lua:485` | `opts.owner` |
| `W.CopyWindow(d)` | `Export.lua:282` | `d.addonName` is already passed; remove `d.applySkin` |
| `DebugLog:New(d)` | `core/DebugLogSetup.lua:174` | `d.addonName` is already passed; remove `d.applySkin` |
| `Sim:New(d)` | `modules/Sim.lua:406` | `name = addonName` already (nothing to do) |
| `Core.MakeCloseButton(parent, onClick, addonName)` | not called: the addon draws its own 24x24 close (`Browser.lua:103`) | D1 |
| Options descriptor `addonName` | `settings/OptionsSetup.lua` | already the folder name (check it at BL-01) |
| `O.AppearanceTab(spec)`, `O.SkinPicker(spec)` | new at BL-01 / BL-04 | spec get / set through the write seam |

`Core.MakeResizable` (`Browser.lua:1132`, `SessionWindow.lua:617`) takes no owner. `W.CloseMenu` is a function, not
a factory.

## 3. HUD style settings

**No HUD.** BankLedger draws no bar, icon, glow or HUD text, and no saved setting styles a HUD. O2's one-time
reset has nothing to reset: BL-03 goes in `exceptions.tsv`, proved by
`grep -rnE 'StatusBar|SetStatusBarTexture|LSM|SharedMedia' core modules settings defaults`, which finds no HUD
style key.

Two saved settings do style a window surface: `settings.rowStripeAlpha` (default 0.03) and
`settings.rowHoverAlpha` (default 0.10) (`settings/Schema.lua:112`, `:119`; `defaults/Profile.lua:61-62`). They are
not HUD and so are outside O2; their treatment is D2.

## 4. Exceptions

| # | Rung | What | Where | Reason |
|---|---|---|---|---|
| E1 | 3 | GameTooltip's frame (item hyperlink tooltips, every tooltip's chrome) | `LedgerTable.lua:536`, `SessionWindow.lua:394` and every `SetOwner` | skinning-§7: only the lines the addon writes take skin colors |
| E2 | 3 | StaticPopups (`KA0S_BANKLEDGER_RESETALL`, the filter lists' clear confirms) | `settings/Panel.lua:262`, the Schema confirms | skinning-§7 |
| E3 | 4 | Class colors (`RAID_CLASS_COLORS`) on the Character column, Insights per-character labels, class icon markup | `LedgerTable.lua:453`, `InsightsWidgets.lua:101`, `Insights.lua:671-714` | game meaning (their fallbacks do skin: `text.body`, `text.muted`) |
| E4 | 4 | Item quality colors | `LedgerTable.lua:416-420`, `InsightsWidgets.lua:95`, `Constants.lua:230-245`, `Browser.lua:677` | game meaning; read through `q.*` (Ka0s Default = the client's values), never re-hued |
| E5 | 3 | LibDBIcon minimap button and the LibDataBroker display | `core/LauncherSetup.lua` | third-party shared objects; the library draws the tooltip |
| E6 | 3 | Blizzard SettingsPanel chrome, including the header Defaults button the addon reaches | `settings/Panel.lua:55` (`setDefaultsAction`) | skinning-§7; the button is Blizzard's |
| E7 | 4 (doubtful, D3) | The store identity palette `C.StoreRGB` (bank gold, warband cyan `0,0.8,1`, guild magenta `0.93,0.45,0.88`, bags `0.75,0.75,0.78`) | `core/Constants.lua:80-85`; used `LedgerTable.lua:446`, `Browser.lua:448`, `Insights.lua:250` | categorical meaning of the addon's own (which store), the same footing as DPS Race's per-player colors; no token holds three of the four values |
| E8 | 4 | Coin glyphs and class icons in text (`|T` money and class art) | `NS.Util.FormatMoney`, `ClassIconMarkup` | game art |
| E9 | n/a | Chat output colors (`NS.PREFIX` cyan, the disabled line's yellow) | `core/Namespace.lua:18`, `settings/Slash.lua:292` | chat text, not a surface the addon draws (no frame) |
| E10 | n/a (keep) | The ▲/▼ direction glyph's mono face `C.FONT_MONO` | `LedgerTable.lua:515`, `SessionWindow.lua:373`, the dropdown `glyphFont` `Browser.lua:306` | glyph coverage: the client font has no ▲/▼ (debug-logging-§2's mono exception). Every skin's `font.mono` is JetBrains Mono today anyway |
| E11 | 3 | The resize grip art | `Core.MakeResizable` | library-owned, takes no owner |

## 5. Gaps (rung 2)

Two tokens, both colors. Everything else composes from existing primitives and tokens.

### BL-G1: `sem.goldAlt`, the pale gold of a gold movement

- **Today:** `MONEY_RGB = { 1.00, 0.91, 0.55 }` (`modules/LedgerTable.lua:36`, published `LT.MONEY_RGB` `:38`), used for
  the Item and Quality cells of a gold row (`:426`), the gold row's tooltip title (`:543`), the session window's
  copy of it (`modules/SessionWindow.lua:398`, the literal `1, 0.91, 0.55`) and the search suggestion
  (`modules/Browser.lua:674`).
- **Why no token fits:** it is a meaning color (a row is money, not an item, so it has no quality). The nearest
  token is `sem.gold` `{1,0.86,0.55}` (LootHistory's `C.GOLD_RGB`), which is 0.05 off in green. The others
  (`text.headingAlt` 0.91,0.77,0.42; `drawer.summarySet` 0.91,0.85,0.66) are neither the value nor the role. LK-A3
  set the precedent: a split value gets an `*Alt` token (`sem.goodAlt`, `sem.badAlt`, `sem.warbandAlt`) rather than
  moving a pixel.
- **Ka0s Default must reproduce:** `{ 1.00, 0.91, 0.55, 1 }`. The other skins can follow `sem.gold` (FOLLOW), as
  the dark skins inherit the `*Alt` tokens. The alternative, mapping to `sem.gold` with no library change, is D4.

### BL-G2: `gtip.valueAlt`, the legend swatch's tooltip line

- **Today:** `W.CursorTooltip(self, self._tip, W.MUTED)` (`modules/InsightsWidgets.lua:819`), where
  `W.MUTED = { 0.80, 0.80, 0.82 }` (`:22`), writes a GameTooltip line in that gray.
- **Why no token fits:** a line written onto GameTooltip takes a `gtip.*` token (skinning-§7), and no skin darkens
  a `gtip.*` one, because the tooltip frame stays Blizzard's dark whatever the skin. The `gtip` set is title GOLD,
  body 0.9, muted 0.5, value 1.0, subtle 0.7, so none is 0.80/0.80/0.82. `text.value` holds the exact value but
  is a window-text token, and a light skin may darken it (Azeroth set every window token in ink until minor 8),
  which would make it illegible on the dark tooltip.
- **Ka0s Default must reproduce:** `{ 0.80, 0.80, 0.82, 1 }`. The other skins take the same value (no skin changes
  a `gtip` token). If the owner rules it too small for a token, use `gtip.body` (0.9), a 0.1 shift on one hover
  line (D10).

## 6. Doubtful calls (for DECISIONS.md)

| # | Call | Recommendation |
|---|---|---|
| D1 | The close control: BL's own 24x24 button, rest `0.85`, hover = **the player's class color** (`Browser.lua:101-133`), against the rescoped standalone-windows close bullet (`close.rest` 0.7 / `close.hot` red under Ka0s Default) | `S.CloseButton(close)` on BL's own button, which keeps its 24x24 geometry and the `close` mark, and accept the skin's tints. LootHistory made the same change at LH-02 (it moved to `lib.MakeCloseButton`). This **changes Ka0s Default's look** (class hover lost), so ask the owner |
| D2 | `rowStripeAlpha` / `rowHoverAlpha`: player sliders that set the row tints' alpha (Interface > Windows) | Keep both sliders. Color the RGB from `list.stripe` / `list.hover` and the alpha from the slider, so Ka0s Default is unchanged (the defaults equal its token alphas). Other skins' own stripe and hover alphas are not used while the slider stands. The alternative is to retire the sliders, or give them a fromSkin companion; neither is owed under O2 (not HUD) |
| D3 | Store identity palette `C.StoreRGB` (E7) | Rung 4: keep it, as the addon's own categorical meaning (like DPS Race's colors). The owner may move it to rung 2 (four `sem.store*` tokens) if a skin should be able to retune legibility |
| D4 | Gold movement color: new `sem.goldAlt` (BL-G1) or reuse `sem.gold` | BL-G1, a new token: it keeps Ka0s Default exact |
| D5 | Tab labels: `S.Text(label, "accent" / "muted")` (LH `Browser.lua:286-295`, chosen for legibility) or `tab.onText` / `tab.text` | LH's text roles; both resolve to today's values under Ka0s Default |
| D6 | Shell's `title.bg` top band and SortHeaderBar's `list.header.bg`: both are bands BL does not draw today (Ka0s Default sets them since SkinDefs minor 8, and LH wears them) | Accept them on the two main windows (their title bars are 30px, so the band fits) and on the table headers, matching LH. On the export modal (26px bar) use `Shell(…, { noTopBar = true })` + `S.TitleBar(tbar)`, as LH's Export does |
| D7 | Insights data bars: `S.BarTexture` (Ka0s Default's textured "Ka0s Default" bar) or keep flat `SetColorTexture` | `S.BarTexture` for every data bar (ranked, stacked, back-to-back, split, strip), as LH's `NS.SkinBar` does. Keep the legend chip flat. It is a visible change on Ka0s Default, which v1.79.0 already made collection-wide |
| D8 | First-run picker `onPreview` | Wire it to open the ledger window (`B:Show`) in test mode (`LT:SetTestMode(true)`). Test mode refuses in combat (`LedgerTable_TestMode.lua:249`), so preview must not be offered in combat; the picker is held to `PLAYER_REGEN_ENABLED` anyway |
| D9 | `W.QualityColor` fallback `{0.60,0.60,0.62}` (unknown quality, headless) | Use `sem.unknown` `{0.6,0.6,0.6}`: the same role in LH (Insights' no-quality gray), and in game it is reached only for an unknown quality id. A 0.02 blue shift, so no token for it |
| D10 | BL-G2 (`gtip.valueAlt`) or `gtip.body` for one legend tooltip | BL-G2, to keep Ka0s Default exact. Only one line uses it, so if the owner prefers no token, `gtip.body` |
| D11 | The degraded `SessionWindow.lua:628` arm (bare backdrop, no edge colors, when `NS.Browser` is absent) | Remove it: `NS.Browser` always loads first in the TOC, and the Skin degraded facade (`NS.Skin.Shell` routed to `NS.ApplySkin`) covers the no-library case |

## 7. Re-vendor v1.77.0 -> v1.79.0 obligations (BL-RV)

- **Whole folder from the tag** (`git archive`): v1.78.0 and v1.79.0 add `Skin.lua`, `SkinDefs.lua`, `SkinPaint.lua`,
  `SkinPaintExtras.lua`, `SkinPaintControls.lua`, `SkinEUI.lua`, `SkinAce.lua`, `OptionsAppearance.lua`,
  `OptionsSkinPicker.lua` and `Toast.lua`, each of which must arrive with its shell. The media add the eight skin
  font families plus Oxanium (`media/fonts/`) and the generated bars (`media/textures/`). `tests/run.lua:56` loads
  `Loader.xmlFiles("libs/LibKa0s/LibKa0s.xml")`, so there is no hand-kept file list to move. The kit's
  `test_libka0s.lua:345` checks XML order only.
- **Options degradation stub** (`settings/OptionsSetup.lua:~230-276`) gains `AppearanceTab` and `AppearanceRows`
  (v1.78.0) and `SkinPicker` and `HideSkinPicker` (v1.79.0). Each answers nil or a no-op, never the library's words
  (anti-pattern #47). `tests/test_surface_parity.lua` (`Kit.assertSurfaceParity` via `Kit.setSurfaceSource`,
  `tests/run.lua:84-86`) goes red until they are there.
- **Provenance line** `CLAUDE.md:48` -> the run's tag (v1.79.0, or v1.80.0 if M1 ships BL-G1 / BL-G2), and the
  kit-revision line `CLAUDE.md:51` -> that tag's `Kit.VERSION`. The vendor gate `tests/test_vendor_sync.lua` reads
  both.
- **Icons line** `CLAUDE.md:49` gains **`eye`** and **`settings`** (the picker's buttons,
  `OptionsSkinPicker.lua:624-626`), or the prune removes them. It becomes: chevron-down, chevron-right, clear, close,
  confirm, copy, export, eye, info, search, settings, sort-down, sort-up. Then run `tools/prune-icons.lua` from the
  tag, and update the README's icon-set credits.
- **`## OptionalDeps`** in `BankLedger.toc` gains `EllesmereUI` (skinning-§5, v1.78.0's owe for an adopter).
- **Ka0s Default looks different at the re-vendor** (v1.79.0): Oxanium faces and the Ka0s Default bar. It reaches BL
  only once it registers an owner (BL-01), but `docs/smoke-tests.md` re-looks at every window.
- **Release pins to check:** `tests/test_libka0s.lua:64` (`lib.MINOR >= 10` for Core; still holds),
  `tests/test_mediasetup.lua:66-82` (`JetBrains Mono` path and `C.FONT_MONO`; still holds),
  `tests/test_marks.lua` (icon names and the declaration), `tests/test_reset_routes.lua:203` (the v1.77.0 wording
  note), `tests/test_panel.lua:402-406` (the AceGUI minor). Regenerate `docs/test-cases.md`.
- **`docs/api/CONSUMERS.md` in LibKa0s** is outside this repo. The skinning census records BL's new exports there.

## 8. Risks

- **File cap.** `tests/test_browser.lua` is **1442** lines, 58 from the 1500 cap, so the skin suites for the windows
  belong in a new `tests/test_skin*.lua` and not in it. `modules/Browser.lua` (1259) and `modules/Insights.lua`
  (1004) can take the facade calls but not a new subsystem; `settings/Schema.lua` (977) gains the `skin.*` rows.
  `core/SkinSetup.lua` will be about 450-600 lines (LH's is 631).
- **Hot paths.** `LT:PaintCell` runs about 7 x 30 times per scroll tick and is allocation-free by design
  (`LedgerTable.lua:459-461`). Resolve the token colors **once per skin** (cache them in an `OnLooksChanged`
  listener), never `S.Color` per cell. Use `S.Font` at row build only. `NS.Util.ApplyRowTint` runs per bind: cache
  its RGB the same way.
- **Pooled rows and markup baked at load.** The sort arrows, the expanders (`LedgerTable.lua:173-182`) and
  `C.QUALITY_OPTIONS` (`Constants.lua:240`) are built once at file load with the color in the string. A skin switch
  must rebuild them and re-bind the visible rows (`LT:Bind`, `SW:Bind`, `Insights:Refresh`). LH subscribes to
  `NS.Skin.OnLooksChanged`, never to `SETTINGS_CHANGED`.
- **Shrink-to-fit fonts.** `W.SetCard` resets to the captured `card.fontFile/baseSize` (`InsightsWidgets.lua:427-449`)
  and `MakeSectionDivider` scales the template size by 1.5 (`:838`). Both would undo or double-scale the skin's face
  and size unless the base is re-captured after the paint and on each switch.
- **Pooled AceGUI widgets.** The seven acquisitions in 1.7 must be painted with `Skin:PaintAce` and restored on
  release, or a CheckBox or Button rides the shared pool into another addon in this skin. The Filters sub-strip's raw
  buttons on a pooled SimpleGroup (`Panel.lua:456-470`) are the library's (`O.SubTabStrip`), which drains them
  before release.
- **The singleton row menu** (`LedgerTable.lua:832`) belongs to BL, not the library, so `S.MenuFrame` records it
  against the owner. It is safe, but it closes on window hide, so a repaint while it is open is harmless.
- **The `eui` source.** The windows and the modal are BL's own frames, so they are handed to EllesmereUI's facade.
  The pooled rows and the pooled Insights widgets are pooled within BL only (`NS.Pool`, `W.NewPool`), never across
  addons, so they are BL's objects and fine. The AceGUI widgets keep the library technique (skinning-§5).
- **Taint and combat.** There are no secure frames: the toggle button `BankLedgerToggleWindow`
  (`core/LauncherSetup.lua:144`) is a plain hidden Button used for a CLICK binding, and every window is non-secure
  and non-protected. The picker and test-mode preview are held to out of combat (D8).
- **Degraded install.** With no LibKa0s the stub facade must route `Shell` to the `CoreSetup.lua:102` fallback and
  answer `NS.SKIN_FALLBACK` colors. `tests/test_surface_parity.lua` should pin every fallback entry to the live Ka0s
  Default value, as LH does.

## 9. Effort

**L.** There is no HUD and no migration, but the addon has about 40 painted surfaces across three windows, a modal, a
popup menu, the Insights widget kit (about 10 widget kinds), allocation-free cell painters that need a per-skin
color cache, load-time markup to rebuild, seven self-acquired AceGUI widgets, two applySkin hooks to drop, and two
probable library tokens (BL-G1, BL-G2). That is close to LootHistory's own leg-1 footprint, with LH's code as the
template.
