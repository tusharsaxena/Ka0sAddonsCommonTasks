# Inventory: MultiMeters (prefix MM)

Read-only M0 inventory, 2026-10-29. Repo `../MultiMeters` at `c8aa972` (master content; the run branch
`feat/2026-10-29-skinning-rollout` is checked out with no commits on it), vendoring LibKa0s v1.77.0
(`CLAUDE.md` provenance line). Library read at the v1.79.0 main checkout. Every `file:line` below is
MultiMeters' unless prefixed. Token names are from `LibKa0s/SkinDefs.lua`'s schema; Ka0s Default values
quoted from `SkinDefs.lua:200-345`.

**The shape of this addon.** The meter window is a Ka0s window (Core `ApplySkin` today) whose whole body
is HUD: rows of StatusBar cells, class-tinted, with per-window style settings. **All style is per
window**: `profile.windows[i].{frame,header,columnHeader,rows,bars,text,icons,tooltip}`
(`defaults/Profile.lua:55-492`, copied per window by `NS.DefaultWindow` `:505`). Schema paths read
`window.<group>.<key>` against the active window. Colors carry options-ui-§17 color **modes**
(`custom | class | stat`, plus `skin` already on `header.dividerColorMode`), resolved by one helper,
`surfaceColor` (`modules/Window.lua:920-936`, published `NS.SurfaceColor`). That helper is the natural
seam for a `skin` mode.

**The data rule binds the skin too.** Every meter number is a secret value; a frame handed one via
`SetValue` has secret geometry, so layout is computed from config and never read back (CLAUDE.md).
Nothing in the skin path may read a cell back (see Risks R1).

## 1. Surfaces

### 1a. The meter window chrome (MM-02)

| Surface | Built | Typed today | Paints it (rung 1) |
|---|---|---|---|
| Window frame (backdrop + edge) | `modules/Window.lua:570` (`BackdropTemplate`); skin `:631`, `:790` (`NS.ApplySkin` = `lib.ApplySkin`, no owner, `core/CoreSetup.lua:282`) | `ApplyBorder` `:850-888` rewrites the backdrop: `bgFile = NS.SKIN.bgFile` `:861` (a constants-table read, #107), player `frame.borderStyle` "Blizzard Tooltip" / `borderSize` 2 / `borderColor` (0,0,0,1) / `backdropColor` (0,0,0,0.75), defaults `defaults/Profile.lua:105-112`, fallbacks `:877-887`; toggles Core's `frame.innerBorder` `:856-857` | `NS.ApplySkin(frame)` -> `lib.ApplySkin(frame, nil, addonName)` (Core minor 13 hands it to `S.Shell`), or `S.Shell(frame, { noTopBar = true })` directly; the fill/edge become HUD style settings with a `skin` mode reading `win.bg`, `win.border`, `win.borderStyle`, `win.borderSize`, `win.inner` (see §3 and D1). Re-run `ApplyBorder` after every repaint (OnLooksChanged, R3 below) |
| Title text | `Window.lua:612`; styled `modules/Window_Header.lua:355-365` | `SetFont(header.font)` `:363`; `SetTextColor(headerColor)` `:396`, default gold (1,0.82,0) `defaults/Profile.lua:248`; TEST MODE word `|cffff2020` `:380` | Face `S.Resolve("hud.font", header.font, header.fontFromSkin)` (D2); color `skin` mode -> `title.text` (1,0.82,0,1, exact). TEST MODE word -> `sem.modeTest` (D7) |
| Header strip background | `Window.lua:629` (`self.headerBG`, BORDER layer) | `SetColorTexture(header.bgColor)` `Window_Header.lua:422`, default (0,0,0,0.5) `Profile.lua:254`; no mode since v9 | `header.bgColorFromSkin` companion (D3) -> `title.bg` (Ka0s Default 0.04,0.04,0.05,0.9) |
| Divider | `Window.lua:615`; placed `Window_Header.lua:465-480` | mode `skin` leaves ApplySkin's tint (`divider` 0.24,0.24,0.27,0.85); `class`/`custom` write `:476`/`:478` | `skin` mode -> `S.Divider(frame.divider)` (`divider`, exact). Already follows the skin; keep |
| Session line (segment name, "restricted" notice) | `Window.lua:664-668`; styled `Window_Header.lua:505-522` | header font `:519`, `headerColor` `:521`; `NS.GRAY` = `|cff9d9d9d` (`core/Namespace.lua:42`) in `:1217`, `:1240`, `:1242` | Same as title (face + `title.text`); gray -> gap MM-G4 |
| Header controls (close, minimize, lock, settings, segment, reset, export) | `modules/HeaderControls.lua:432-452` (art: `NS.Icon` TGA -> atlas -> ASCII ladder `:226-276`) | rest `frame.controlColor` (0.7,0.7,0.72) / hover `controlHoverColor` (1,0.82,0) via `controlColor` `:561-586`; `SetVertexColor` `:245`, `:263` (atlas rung white), `:693`; glyph `SetFont`/`SetTextColor` `:271-272`, `:690` | `skin` mode on both: rest `icon.tint` (0.7,0.7,0.72, exact), hover `btn.hover` (gold, exact) (D4). NOT `S.CloseButton`: its hover is `close.hot` red, and the close control here is one of seven siblings that must match |
| Column header strip | `Window.lua:676-678`; `Window_Header.lua:530-547` (buttons), `:624-700` | font `columnHeader.*` `:643`; label color `surfaceColor(colHeader.colorMode, ...)` default gold `:631-632`, `stat` per column, `name` forced white `:651`; strip bg `:727` (0,0,0,0); per-column bg `:680`; sort arrow tinted label color `:599`, ASCII `:616-618` | Face `hud.font` companion; label color `skin` mode -> `list.header.text` (gold, exact); strip bg: `skin` mode available, `list.header.bg` (D5). Arrow keeps the label tint (it is `icon.arrow`-gold under Ka0s Default either way). `S.SortHeaderBar` not used: the labels are per-column frames with stat colors |
| Test-mode strip / sim strip | `Window.lua:546-549`, `:696-700` (`W.TestStrip`), placed `Window_Header.lua:803-821` | library amber / cyan | `opts.owner = addonName` (Widgets 16) -> `S.Strip`, `strip.test` / `strip.sim` |
| "No meter" notice | `Window.lua:688-690`; `Window.lua:806` font; text `Window_Header.lua:1326-1334` | `SetFont(header face, text.size, "")`, no color (stock white); reason line `NS.GRAY` `:1332` | `S.Font(notice, S.Color("text.highlight"))` keeping MM's size, or keep font from the header face resolve; gray -> MM-G4 |
| Empty state ("No combat data yet") | `Window.lua:1354-1366` | `GameFontNormalLarge` + `SetTextColor(1,0.82,0)` `:1359`; `GameFontHighlightSmall` + `SetTextColor(1,1,1)` `:1364` | `S.Text(e.title, "heading")` (`text.heading`, exact); `S.Font(e.text, S.Color("text.highlight"))` (exact) |
| Resize grip | `Window.lua:720` (`NS.MakeResizable`, Core minor 10) | library art | Core's grip takes no owner in v1.79.0; nothing to do |

### 1b. The HUD: rows and cells (MM-03)

| Surface | Built | Typed today | Paints it (rung 1) |
|---|---|---|---|
| Cell StatusBar texture | `modules/Row.lua:549`; `Cell:ApplyBarSkin` `:606-610` | `SetStatusBarTexture(barTexture(bars.texture))` `:608`; LSM fetch, fallback `Interface\TargetingFrame\UI-StatusBar` `:345-349`; default "Blizzard Raid Bar" `Profile.lua:327` | `S.Resolve("bar.texture", bars.texture, bars.textureFromSkin)` then MM's own LSM fetch, re-run on OnLooksChanged (D6, not `S.BarTexture`: R1) |
| Cell fill color | `Row.lua:879` | `barColor(cfg.bars, entry, key)`: class (default) / stat / custom (0.35,0.55,0.85) | Meaning (class, stat): exception E5/E6. `customColor` stays the player's |
| Cell background | `Row.lua:883`; name cell `Row_NameCell.lua:432` | `cellBackground`: class tint at `bgAlpha` 0.1 (default), stat, custom (0,0,0), none | Meaning by default; `custom` stays the player's (D5) |
| Cell text (left / right) | `Row.lua:552-557` | `ApplyTextStyle` `:762-776`: `SetFont(text.font)` `:769-770`, `SetTextColor(text.color)` white `:771-772`; class/stat modes `:741-757` | Face `hud.font` companion; color `skin` mode -> `text.highlight` (WHITE, exact). Size, outline, shadow, alpha stay the player's |
| Name text | `Row.lua:701-710` | class color, else `SetTextColor(1,1,1,a)` `:709` | Class: E5. Fallback white -> `text.highlight` (exact) |
| Unit / spell icons | `Row_NameCell.lua:355-385` | spec icon, class atlas `CLASS_ICON_TCOORDS`, drill-down spell icon | E6 (game art). No `S.IconBorder` (D9) |
| Name-cell bar | `Row_NameCell.lua:421` | `SetStatusBarColor(0,0,0,0)` (a hidden fill, functional) | Untouched: not a look |
| Cell border | `modules/Row_Border.lua:100-160`, `:205`, `:245-256` | `bars.border` off by default; LSM edge `:127` or four flat textures `:156`, `:251`; color `cellBorderColor` black / class | `bars.borderStyleFromSkin` -> `bar.borderStyle` ("None", exact); color `skin` mode -> `bar.border` (0,0,0,1, exact); thickness stays the player's |
| Row stripe (alternating) | `Row.lua:1060-1062` (`row.bg`) | `SetColorTexture(1,1,1,0.05)` `:1164`, gated by `rows.alternatingBackground` (default off) | gap MM-G2 |
| Row mouseover highlight | `Row.lua:1099-1102` | `SetColorTexture(1,1,1,0.10)` `:1101` (white wash) | gap MM-G1 |
| Self highlight edge (3px) | `Row.lua:1093-1097`, width `:991` | `SetColorTexture(1,0.82,0, 1 or 0)` `:1134` | `S.Color("text.accent")` (gold, exact), alpha kept as the on/off gate |

Hot path: `RowProto:Update` (`Row.lua:1150+`) and `Cell:SetValue` (`:859-890`) run for every visible row on
every refresh (throttle 0.25s). Token reads there must come from upvalues refreshed on OnLooksChanged
(`WindowProto:RefreshUpvalues` exists), never `S.Color` per call (R2).

### 1c. Tooltips the addon writes (MM-03)

GameTooltip itself is never painted (E1). What the addon writes:

| Surface | Built | Typed today | Paints it (rung 1) |
|---|---|---|---|
| Section headings ("Death recap", "Deaths", "Spell breakdown", "Targets", "All statistics") | `modules/Tooltip_Builders.lua:436`, `:442`, `:518`, `:577`, `:658`, `:935` | `AddLine(..., 1, 0.82, 0)` | `gtip.title` (exact) |
| Hint lines ("and N more", "Click for details", "No data yet") | `Tooltip_Builders.lua:607`, `:687`, `:770`, `:940` | `0.6, 0.6, 0.6` | gap MM-G3 |
| White lines (icon line, death row name, label) | `Tooltip_Builders.lua:247`, `:1031`; `Tooltip_Lines.lua:698` | `1, 1, 1` | `gtip.value` (WHITE, exact) |
| Double-line headers | `Tooltip_Builders.lua:427-429`, `:756-757` | left = class color (E5), right gold `1,0.82,0` | right `gtip.title` (exact) |
| Stat rows on the name tooltip | `Tooltip_Builders.lua:892-893` | `statColor` per stat | E7 (stat identity) |
| Tooltip bar overlays (spell / target / death lines): carrier + StatusBar on GameTooltip | `modules/Tooltip_Lines.lua:91`, `:99`; bg placeholder `SetColorTexture(0,0,0,0.35)` `:103` (overwritten every draw) | per draw `:569-666`: fonts `:572-574` (`tooltip.font`), text `tooltip.textColor` white `:596-598`, texture `tooltip.barTexture` `:643`, fill `barColor` (class default) `:659`, bg `barBgColor`+`barBgAlpha` `:664`, LSM border `:529-541` | Face `tooltip.fontFromSkin` -> `hud.font`; text `skin` mode -> `gtip.value`; texture `tooltip.barTextureFromSkin` -> `bar.texture`; border `tooltip.barBorderStyleFromSkin` -> `bar.borderStyle`, color `skin` -> `bar.border`; fill and bg stay mode-driven (E5) |
| Death recap row columns | `Tooltip_Lines.lua:255-285` (`time`, `caster`) | `SetFont(path,size,flags)` `:262`, `:278` | same face resolve as above |
| GameTooltip's own TextLeftN fonts | `modules/Tooltip.lua:860-1000` (`applyLineFont` `:881`, color `:889-890`; restore `SetFontObject(GameTooltipText)` `:987-988`, `SetTextColor(1,1,1)` `:997-998`) | the tooltip face and `textColor` on lines MM wrote, restored on teardown | Face/color through the same resolves; the restore keeps putting Blizzard's object back (E1, D10) |
| Column-block glyph tooltip | `settings/ColumnBlocks.lua:159-164` | `AddLine(..., 1, 1, 1)` | `gtip.value` (exact) |

### 1d. The export modal and copy window (MM-02 / MM-04)

| Surface | Built | Typed today | Paints it (rung 1) |
|---|---|---|---|
| Modal frame | `modules/Export_Modal.lua:729` | `NS.ApplySkin(modal)` `:836` (no owner) | `lib.ApplySkin(modal, nil, addonName)` / `S.Shell(modal)` |
| Title bar + caption + close | `Export_Modal.lua:208-231` (`TITLEBAR_H` 26 `:154`) | caption `GameFontNormal` (gold) `:218`; `NS.MakeCloseButton` (owner already passed, `core/CoreSetup.lua:294-296`) | `S.TitleBar(bar)` (`title.bg`, `title.text`, `font.title`) (D8: Ka0s Default now draws a `title.bg` band here) |
| Flat buttons (CSV, chat) | `makeButton` `:246-293`, `setEnabled` `:307-316` | backdrop `skinColor("bg")` = Core.SKIN.bg (0.06,0.06,0.08,0.92) `:261`, edge `skinColor("innerBorder")` (0.24,0.24,0.27,0.85) `:262` (constants-table reads, #107); icon `SetVertexColor(1,1,1)` `:277`; label white, hover `skinColor("title")` gold `:287`, disabled `0.4` `:290-292`, `:314` | `S.Button(btn)`: `btn.bg`, `btn.border`, `btn.text`, `btn.hover`, `btn.icon`, `text.disabled` (D8: fill, edge alpha, icon and disabled gray each move slightly) |
| Selectors (metric, channel, lines) | `makeSelector` `:714-720` (`W.Dropdown`) | library dropdown | `opts.owner = addonName` |
| Whisper row + caption + edit box | `:767-795` | row backdrop as the buttons `:778-779`; caption `skinColor("title")` `:788`; box `GameFontHighlightSmall` `:795` | `S.EditBox(whisperBox)` on the row as its box, or `S.Inset(whisperRow)` (`input.*`); caption `S.Text(caption, "accent")` (gold, exact) |
| Warning line | `:809-815` | `SetTextColor(0.9, 0.25, 0.25)` `:815` | D7 (`sem.off` 0.9,0.3,0.3 nearest) |
| Copy window | `ensureCopyWindow` `:361-380` (`W.CopyWindow`) | `applySkin = NS.ApplySkin` `:375` (runs **instead of** the owner skin, Widgets doc `:796`); font `Const.FONT_MONO` | Drop `applySkin` (the descriptor's `addonName` is the owner from Widgets 16); keep the mono font (it is content) |

### 1e. Settings pages the addon builds itself (MM-04)

| Surface | Built | Typed today | Paints it (rung 1) |
|---|---|---|---|
| Library chrome (pages, tabs, nav rail, drawers, scroll) | `settings/OptionsSetup.lua:153` (`addonName` in the descriptor) | library | Follows the owner once registered (Options 33) |
| Appearance tab (new) | General page `settings/General.lua:258-263` (`H.RenderTabbedSchema`, `tabs = { H.KeybindingsTab(...) }`) | — | `O.AppearanceTab(spec)` with `before` = the Keybindings key |
| Column blocks (Columns page) | `settings/ColumnBlocks.lua:141-171` (raw frames reparented into an AceGUI SimpleGroup `:267`), label `:189-196` | label gold `1,0.82,0` `:193` / gray `0.5` `:195`; ghost text color `{1,0.82,0}` / `{0.5,0.5,0.5}` `:298`; glyph `ReadyCheck-Ready/NotReady` `:72-73` | label `S.Text(label, "accent")` / `"disabled"` (both exact); ghost colors from `S.Color("text.accent")` / `S.Color("text.disabled")`; glyphs E6 |
| Reorder list | `ColumnBlocks.lua:237-255` (`W.ReorderList`) | library | `opts.owner = addonName` |
| AceGUI it acquires: SimpleGroup, Heading | `ColumnBlocks.lua:267`, `:314` | stock | `Skin:PaintAce(owner, w)` (no host `OnRelease` today) |
| AceGUI it acquires: action Dropdown, window-name EditBox | `settings/Windows.lua:81`, `:381` | stock | `Skin:PaintAce(owner, w)`; callbacks are `OnValueChanged` / `OnEnterPressed`, not `OnRelease` |
| Profiles page (AceConfigDialog in a SimpleGroup) | `settings/Profiles.lua:91-100` | stock (AceDBOptions) | `Skin:PaintAceTree(owner, container)` after each `AceConfigDialog:Open` (R4) |
| StaticPopups (reset all, reset meter data, reset window) | `settings/General.lua:82`, `:136`; `modules/HeaderControls.lua:385` | Blizzard | E2 |

### 1f. Tool surfaces (MM-04)

| Surface | Built | Owner today | To do |
|---|---|---|---|
| Debug console | `core/DebugLogSetup.lua:365-375` | `name`, `addonName` = folder | Nothing: follows the owner once registered (DebugLog 22) |
| Perf panel | `core/PerfSetup.lua:74-83` | `name`, `addonName` | Nothing (Perf 15.1.1.10) |
| Sim panel | `core/SimSetup.lua:141` | `name` | Nothing (Sim 2.3.7) |
| Export copy window | see 1d | `addonName`, but `applySkin` overrides | Drop `applySkin` |
| Test / sim strips | see 1a | none | `opts.owner` |
| Launcher (minimap button, broker tooltip) | `core/LauncherSetup.lua:297` (`Launcher:New`) | Launcher 5 takes no owner | Nothing; the tooltip is GameTooltip (E1) |
| First-run picker (new) | — | — | `O.SkinPicker` after login, held to `PLAYER_REGEN_ENABLED` in combat (LootHistory `NS.MaybeShowSkinPicker`) |

## 2. Library factories that take an owner

| Call | Site | Today | Change |
|---|---|---|---|
| `Core.ApplySkin(frame[, skin[, owner]])` | `core/CoreSetup.lua:282` (`NS.ApplySkin = lib.ApplySkin`); callers `Window.lua:631`, `:790`, `Export_Modal.lua:836` | no owner | wrap: `NS.ApplySkin = function(f) return lib.ApplySkin(f, nil, addonName) end` (or call `S.Shell`); `tests/test_coresetup.lua:353` pins `NS.ApplySkin == lib.ApplySkin` and must move |
| `Core.MakeCloseButton(parent, onClick, addonName)` | `CoreSetup.lua:294-296` | owner passed | none |
| `W.TestStrip(parent, opts)` x2 | `Window.lua:546`, `:696` | no owner | `owner = addonName` |
| `W.Dropdown(parent, width, opts)` x3 | `Export_Modal.lua:715` | no owner | `owner = addonName` |
| `W.ReorderList(opts)` | `settings/ColumnBlocks.lua:241` | no owner | `owner = addonName` |
| `W.CopyWindow(descriptor)` | `Export_Modal.lua:366` | `addonName` + `applySkin` | drop `applySkin` |
| `W.CloseMenu()` | `Export_Modal.lua:851` | — | none (singleton follows the opener) |
| DebugLog / Perf / Sim descriptors | 1f | folder name | none |
| Options descriptor `addonName` | `OptionsSetup.lua:153` | folder name | none |
| `Skin:PaintAce` / `PaintAceTree` | 1e | — | new, for the self-acquired widgets |

No `SearchBox`, `Autocomplete`, `DragHandle` or `LineChart` calls.

## 3. HUD style settings (O2, the one-time R3 reset)

Every key is per window (`profile.windows[i].<path>`; schema path `window.<path>`). Companions follow the
composer's naming (`<picker key>FromSkin`, `OptionsCompose.lua:511-531`); the composed groups are in
`settings/Schema_Compose.lua:871-1240` (`FRAME_BORDER_ROWS`, `HEADER_TEXT_ROWS`, `BARS_BAR_ROWS`,
`BARS_BORDER_ROWS`, `BARS_TEXT_ROWS`, `TIP_BAR_ROWS`, `TIP_BARBORDER_ROWS`, `TIP_TEXT_ROWS`,
`COLHEAD_TEXT_ROWS`, `COLHEAD_BG_ROWS`).

| # | Key | Kind | Default | Follows the skin through | Reset (R3) |
|---|---|---|---|---|---|
| H1 | `header.font` | font | "Friz Quadrata TT" | FontGroup `fromSkin` -> `header.fontFromSkin`; `S.Resolve("hud.font", v, c)` (D2) | companion true |
| H2 | `columnHeader.font` | font | "Friz Quadrata TT" | `columnHeader.fontFromSkin`; `hud.font` | companion true |
| H3 | `text.font` (cells) | font | "Friz Quadrata TT" | `text.fontFromSkin`; `hud.font` | companion true |
| H4 | `tooltip.font` | font | "Friz Quadrata TT" | `tooltip.fontFromSkin`; `hud.font` | companion true |
| H5 | `bars.texture` | statusbar | "Blizzard Raid Bar" | BarGroup `fromSkin` -> `bars.textureFromSkin` (keys map `barTexture = "texture"`); `bar.texture` | companion true |
| H6 | `tooltip.barTexture` | statusbar | "Blizzard Raid Bar" | `tooltip.barTextureFromSkin`; `bar.texture` | companion true |
| H7 | `bars.borderStyle` | border | "None" | BorderGroup `fromSkin` -> `bars.borderStyleFromSkin`; `bar.borderStyle` | companion true |
| H8 | `tooltip.barBorderStyle` | border | "None" | `tooltip.barBorderStyleFromSkin`; `bar.borderStyle` | companion true |
| H9 | `frame.borderStyle` (+ `borderSize` 2) | border | "Blizzard Tooltip" | BorderGroup companion maps to `bar.borderStyle`, the wrong token for a window edge: omit it and use a `skin` choice that hands the edge to `S.Shell` (`win.borderStyle`, `win.borderSize`) (D1) | to skin |
| H10 | `frame.backdropColor` (+ `backdropColorMode`) | color + mode | (0,0,0,0.75), `custom` | new `skin` mode -> `win.bg` (D1) | `custom` -> `skin` |
| H11 | `frame.borderColor` (+ `borderColorMode`) | color + mode | (0,0,0,1), `custom` | `skin` -> `win.border` | `custom` -> `skin` |
| H12 | `header.color` (+ `colorMode`) | color + mode | (1,0.82,0,1), `custom` | `skin` -> `title.text` (also session line) | `custom` -> `skin` |
| H13 | `header.bgColor` | color, no mode | (0,0,0,0.5) | `header.bgColorFromSkin` companion (D3) -> `title.bg` | `Skin.ResetToSkin` sets the companion (a color key) |
| H14 | `header.dividerColor` (+ `dividerColorMode`) | color + mode | `skin` | already `skin` -> `divider` | none needed |
| H15 | `columnHeader.color` (+ `colorMode`) | color + mode | gold, `custom` | `skin` -> `list.header.text` | `custom` -> `skin` |
| H16 | `columnHeader.bgColor` (+ `bgColorMode`) | color + mode | (0,0,0,0), `custom` | `skin` -> `list.header.bg` (D5) | D5 |
| H17 | `text.color` (+ `colorMode`) | color + mode | white, `custom` | `skin` -> `text.highlight` | `custom` -> `skin` |
| H18 | `tooltip.textColor` (+ `colorMode`) | color + mode | white, `custom` | `skin` -> `gtip.value` | `custom` -> `skin` |
| H19 | `frame.controlColor` (+ mode) | color + mode | (0.7,0.7,0.72), `custom` | `skin` -> `icon.tint` | `custom` -> `skin` |
| H20 | `frame.controlHoverColor` (+ mode) | color + mode | (1,0.82,0), `custom` | `skin` -> `btn.hover` (D4) | `custom` -> `skin` |
| H21 | `bars.borderColor` (+ mode) | color + mode | (0,0,0,1), `custom` | `skin` -> `bar.border` | `custom` -> `skin` |
| H22 | `tooltip.barBorderColor` (+ mode) | color + mode | (0,0,0,1), `custom` | `skin` -> `bar.border` | `custom` -> `skin` |
| H23 | `tooltip.barBgColor` (+ mode, `barBgAlpha` 0.1) | color + mode | (0,0,0), `custom` | `skin` -> `bar.bg` RGB, the player's alpha kept (D5) | D5 |
| H24 | meta `window.font`, `window.barTexture`, `window.colorMode`, `window.fontOutline` | broadcast rows, "read by nothing" (`Profile.lua:62-75`, `settings/Schema.lua:327-351`) | — | add `skin` to the meta color mode (broadcasts H10-H23); a meta "Use the skin's font / texture" that broadcasts the companions (D11) | n/a |

Not style, not reset: `bars.colorMode` (class), `bars.customColor`, `bars.bgColorMode` (class) and
`bgColor`, `tooltip.barColor(Mode)` (class), `tooltip.barBgAlpha`, every size, outline, shadow, alpha,
thickness, spacing and geometry key (`hud.fontSize` / `hud.outline` exist but no composer companion
governs them, D12), `profile.statColors` (E7), `rows.*` toggles.

**How the reset lands.** A step `migrations[19]` (v19 -> v20) in the account-wide runner
(`core/Database.lua:1070-1094`, `CURRENT_DB_VERSION` `:61`) walking every stored profile (the
`sv.profiles` walk at `:293-310`) and every `profile.windows[i]`:

1. backfill the new companion keys (they are absent from stored windows; `EnsureWindowShape` or the step
   itself writes `false` first);
2. `Skin.ResetToSkin(window, { "header.font", "columnHeader.font", "text.font", "tooltip.font",
   "bars.texture", "tooltip.barTexture", "bars.borderStyle", "tooltip.barBorderStyle", "header.bgColor" })`
   per window (never one call on the profile: `walk` splits on dots and cannot reach the numeric
   `windows` array, `LibKa0s/Skin.lua:633-645`);
3. each listed mode `custom` -> `skin`, and the window edge onto the skin (D1).

`WINDOW_TEMPLATE` gains the companions and `skin` modes as the defaults for new windows (D13).
`profile.skin.pickerSeen` defaults `false` (O3).

## 4. Exceptions

| # | What | Rung | Reason |
|---|---|---|---|
| E1 | GameTooltip's frame and backdrop (every tooltip `Tooltip*.lua`, the launcher's broker tooltip, column-block glyph tooltip) | 3 | skinning-§7. Only the lines MM writes (1c) and its own overlay frames on it (`Tooltip_Lines.lua:91`) take skin colors; `Tooltip.lua`'s font swap on TextLeftN keeps restoring `GameTooltipText` (D10) |
| E2 | StaticPopups `MULTIMETERS_RESET_ALL`, `MULTIMETERS_RESET_METER_DATA` (`settings/General.lua:82`, `:136`) and the header reset confirm (`HeaderControls.lua:385`) | 3 | skinning-§7 |
| E3 | AceGUI-3.0-SharedMediaWidgets pull-outs (`LSM30_Statusbar` / `LSM30_Font` / `LSM30_Border` rows, `settings/Schema.lua:336`, `:344`, the composed media rows) | 3 | skinning-§7 |
| E4 | ColorPickerFrame (every color swatch row) and the SettingsPanel chrome | 3 | skinning-§7 |
| E5 | Class colors: name text (`Row.lua:701-710`), bar fill / bg / border / text `class` modes, header `class` modes (`PlayerClassRGB`), tooltip name lines (`nameColor`) | 4 | game meaning |
| E6 | Spec, class and spell icons (`Row_NameCell.lua:355-385`, tooltip `|T...|t` icons `Tooltip_Builders.lua:247`, `:543`, `:667`), the ready-check glyphs on column blocks (`ColumnBlocks.lua:72-73`) | 4 | game art with meaning |
| E7 | Per-statistic identity colors: `profile.statColors` from `Const.STAT_COLORS` (`defaults/Profile.lua:721-727`), worn by every `stat` mode and the name tooltip's stat rows | 4 | a categorical key the player tunes (like DPS Race's per-player colors); D14 |
| E8 | The test strip's amber and the sim strip's cyan | 4 | library meaning colors; legibility only via `strip.*` (through `owner`) |
| E9 | Chat output: `NS.PREFIX` `|cff00ffff[MM]|r` (`core/Namespace.lua:35`), `/mm` yellow (`settings/Slash.lua:227`, `:578`), `/mm window list` (`modules/WindowManager.lua:781-788`), the diagnostics report's escapes (`core/Diagnostics*.lua`, sink `core/Diagnostics.lua:127-130`: chat or the copy window) | 3 | not a drawn surface; the prefix color is slash-commands' rule. D15 |

## 5. Gaps (rung 2)

Each: no token holds the value in the role, and the nearest one would change Ka0s Default's pixels.

| Id | Component | Ka0s Default must reproduce | Why no primitive / token fits | Proposed |
|---|---|---|---|---|
| MM-G1 | Meter row mouseover wash | `SetColorTexture(1, 1, 1, 0.10)` `modules/Row.lua:1101`, on the row overlay, OVERLAY layer, shown on hover when `rows.mouseoverHighlight` (default on) | `list.hover` is gold (1,0.82,0,0.10): a hue change on every hovered row. No white 0.10 token (`list.boxEdge` 0.12, `tab.glow` 0.15). `S.ListRow` paints `list.hover` | token `list.hoverAlt` (1,1,1,0.10) |
| MM-G2 | Meter row alternating stripe | `SetColorTexture(1, 1, 1, 0.05)` `Row.lua:1164` on `row.bg` (BACKGROUND), even rows when `rows.alternatingBackground` (default off) | `list.stripe` is (1,1,1,0.03), `list.box` 0.06, `chart.track` 0.06: none at 0.05 | token `list.stripeAlt` (1,1,1,0.05) |
| MM-G3 | Tooltip hint / overflow line | `GameTooltip:AddLine(text, 0.6, 0.6, 0.6)` `Tooltip_Builders.lua:607`, `:687`, `:770`, `:940` | `gtip.muted` 0.5 and `gtip.subtle` 0.7 bracket it; `sem.unknown` is 0.6 but means "no quality" | token `gtip.hint` (0.6,0.6,0.6,1) |
| MM-G4 | Dim text inside the window (session line "restricted ..." notes, the notice's reason line) | escape `|cff9d9d9d` (`core/Namespace.lua:42`) at `Window_Header.lua:1217`, `:1240`, `:1242`, `:1332` | `text.muted` 0.7, `text.disabled` 0.5, `sem.unknown` 0.6 (0x99); `q.poor` is 0.62 (0x9e) and means item quality | token `text.dim` (0x9d/255 x3, 1), read as an escape the way LootHistory's `NS.SkinEscape` does |

## 6. Doubtful calls (for DECISIONS.md)

- **D1. The meter window's fill and edge.** Today the window wears `frame.backdropColor` (0,0,0,0.75) and a
  2px "Blizzard Tooltip" edge over ApplySkin; `S.Shell` under Ka0s Default draws `win.bg`
  (0.06,0.06,0.08,0.92) and a flat 1px black edge with `win.inner`. Recommend: treat both as HUD style
  (H9-H11) that the R3 reset puts on the skin, so the window becomes a Ka0s Default window; a player's
  later pick keeps `ApplyBorder`'s path. It visibly changes every existing window's frame, as O2 intends;
  the alternative (omit H9-H11 from the reset) keeps today's look and leaves the meter window the one
  Ka0s window that never follows a skin.
- **D2. Header and column-header faces: `hud.font` or `font.title`?** The FontGroup companion is hard-wired
  to `hud.font` (`OptionsCompose.lua`, the disabled picker shows it), so recommend `hud.font` for all four
  faces (Ka0s Default: Oxanium SemiBold). Using `font.title` would make the picker display a face the
  window does not draw. `S.Shell` puts `font.title` on `frame.title`, so MM's `ApplyTitle` must run after
  every Shell repaint (R5).
- **D3. `header.bgColor` has no mode** (removed in v9). Recommend a `header.bgColorFromSkin` companion
  (what `ResetToSkin` sets on a color key) rather than reviving a mode; Ka0s Default draws `title.bg`
  (0.04,0.04,0.05,0.9) where today is (0,0,0,0.5).
- **D4. Header control hover color.** No `icon.*` token is gold (`icon.hot` is white; `close.hot` red).
  Recommend `btn.hover` (gold, the hover role); rest `icon.tint` (exact). Not `S.CloseButton` for the
  close control, which would turn its hover red beside six gold siblings.
- **D5. Backgrounds that ship transparent or class-tinted** (`columnHeader.bgColor` (0,0,0,0),
  `tooltip.barBgColor`). Recommend: offer `skin` in their modes but leave them out of the R3 reset, so the
  reset does not add a header fill (`list.header.bg` 1,1,1,0.04) no one had. `bars.bgColorMode` stays
  `class` (meaning).
- **D6. Cell bars: `S.Resolve` + MM's own fetch, not `S.BarTexture`.** `S.BarTexture` records each bar and,
  on every repaint, reads the bar's current color back (`GetStatusBarColor`) on a StatusBar holding a
  secret value; and a bar painted from the skin keeps its record after the player unticks the companion.
  Recommend resolving the key and re-running `ApplyConfig` from one OnLooksChanged listener (overrides
  are honored: `Skin:Token` goes through `withOverrides`, `Skin.lua:569-583`).
- **D7. Near-miss reds.** TEST MODE title word `|cffff2020` (1,0.125,0.125) `Window_Header.lua:380` ->
  `sem.modeTest` (1,0.15,0.15); export warning (0.9,0.25,0.25) `Export_Modal.lua:815` -> `sem.off`
  (0.9,0.3,0.3). Recommend accepting both (deltas 0.025 and 0.05); the alternative is two more reds in a
  schema that has six.
- **D8. The export modal takes the library's controls.** Its buttons and whisper row copy Core.SKIN's
  window fill (0.06,0.06,0.08,0.92) and inner edge (0.24,0.24,0.27,0.85), white icons and a 0.4 disabled
  label; `S.Button` draws `btn.bg` (0.1,0.1,0.12,0.9), `btn.border` (alpha 0.9), `btn.icon` 0.85 and
  `text.disabled` 0.5, and `S.TitleBar` adds a `title.bg` band. Recommend accepting: the comment at
  `Export_Modal.lua:117-122` says this frame is one of four copies collection-wide, and the shared
  button is the point.
- **D9. No `S.IconBorder` on row icons.** Ka0s Default's `icon.border` is black: adding it would draw an
  edge the rows never had. Recommend leaving the icons bare.
- **D10. `Tooltip.lua`'s font swap on GameTooltip's own TextLeftN lines** (`:860-1000`) predates skins and
  is restored on teardown. Recommend keeping it (the lines are MM's; the frame is not touched) with the
  face from H4; flag for the reviewer against skinning-§7.
- **D11. Meta rows** (`window.font`, `window.barTexture`, `window.colorMode`): recommend `skin` in the meta
  color mode and a meta companion pair that broadcasts the per-surface companions, so "one control for
  every surface" still holds.
- **D12. Font sizes and outlines stay the player's.** `hud.fontSize` (12) and `hud.outline` ("OUTLINE")
  exist, but no composer companion governs size or outline, and resetting them would restyle every
  grid. Recommend not resetting them.
- **D13. New windows follow the skin.** Recommend `WINDOW_TEMPLATE` (and the schema row defaults the
  composer emits, `false` today) default the companions to `true` and the modes to `skin`, so Reset to
  defaults lands on the skin. Needs a composer `default` override or a host-side row patch.
- **D14. Stat colors stay meaning (E7)**, not `chart.series`: the player configures them on the General
  page and every `stat` mode reads them.
- **D15. Diagnostics markup** (`core/Diagnostics*.lua` escapes) is report content routed to chat or the
  copy window; recommend leaving it (E9) as LootHistory left its chat prefix.
- **D16. A `skin` color mode vs per-color `FromSkin` companions.** MM's colors already carry modes
  (options-ui-§17) and one already has `skin`. Recommend a `skin` value in every style mode (label
  "Skin", replacing the divider's "Ka0s skin", `Schema_Compose.lua:248`) resolved in `surfaceColor` with
  a token argument, and companions only for the composed media pickers and H13.

## 7. Re-vendor v1.77.0 -> v1.79.0 obligations (MM-RV)

- **Options stub** (`settings/OptionsSetup.lua:368-383`, the no-op name list, plus value answers below it):
  `AppearanceTab` (an inert entry, as LootHistory's stub `settings/OptionsSetup.lua:145-148`),
  `AppearanceRows` (nil), `SkinPicker` (nil), `HideSkinPicker` (no-op). `tests/test_surface_parity.lua`
  goes red until it does.
- **Whole folder** `libs/LibKa0s/` and `tests/_kit/` from the tag by `git archive`: new
  `WidgetsCopyWindow.lua`, `DebugLogWindow.lua`, `OptionsAppearance.lua`, the seven `Skin*.lua` files,
  `Toast.lua`, `OptionsSkinPicker.lua`; fonts (five skin faces, Oxanium SemiBold/Bold + OFL); textures
  (two Glass, eight generated bars). `tests/test_vendor_sync.lua` holds the payload to the tag named in
  CLAUDE.md.
- **CLAUDE.md provenance**: `Bundles [LibKa0s](...) v1.77.0 (MIT).` -> the run's tag; `LibKa0s icons:`
  gains `eye` (the picker; `settings` is already declared), then `tools/prune-icons.lua`, and the README
  icon credits in step. `tests/test_mediasetup.lua:94-101` drawn-icon list gains `eye` (library-drawn,
  picker) and notes `settings` is also the picker's.
- **Pins that move**: `tests/test_coresetup.lua:353` (`NS.ApplySkin == lib.ApplySkin`) once the owner is
  passed; comments naming v1.77.0 in `settings/OptionsSetup.lua` and `tests/test_options_panel.lua:1243`
  (prose only). No test pins a library minor except `test_coresetup.lua:279-295` (Core >= 10 fixture,
  unaffected).
- **Sim and TestStrip host re-look**: MM is named in v1.79.0's consumer note as both; its strips and sim
  panel draw as before until the owner registers, then follow the skin. Smoke re-look.
- **Ka0s Default looks different after adoption**: Oxanium faces and the "Ka0s Default" bar reach every
  surface following the skin; the LSM lists gain the new faces and bars.
- **TOC**: `## OptionalDeps` gains `EllesmereUI` (skinning-§5; the line at `MultiMeters.toc:8` has none).
- **docs/test-cases.md** regenerated (case counts move with the new suites).

## 8. Risks

- **R1. Secrets.** A primitive that reads a cell back (`S.BarTexture`'s repaint reads the StatusBar's
  color; any `Get*` on a cell) touches a frame with secret geometry. Keep the HUD on resolve-and-set
  (D6); `S.*` on chrome only. No primitive may receive a meter value.
- **R2. Hot path.** `RowProto:Update` / `Cell:SetValue` run per row per refresh; `Skin:Token` with an
  override set calls `LSM:Fetch` per read (`withOverrides` -> `resolves`). Resolve tokens into the
  window's upvalues on OnLooksChanged and ApplyConfig only; Perf-scenario budgets in
  `tests/perf.lua` should stay flat.
- **R3. Repaint order.** `S.Shell`'s replay rewrites the backdrop, edge, `frame.title` font and
  `frame.divider`, undoing `ApplyBorder`, `ApplyTitle` and the divider's `class`/`custom` modes. One
  OnLooksChanged listener must re-run `ApplyConfig` on every live window (SetChoice fires listeners after
  the repaint). `innerBorder` handling in `ApplyBorder` (`Window.lua:856-857`) changes meaning under
  Shell (Core's inner rule is cleared; Shell draws `win.inner` on its edge holder).
- **R4. Pooled AceGUI.** Self-acquired widgets (`Windows.lua:81`, `:381`, `ColumnBlocks.lua:267`, `:314`)
  need `PaintAce`; the Profiles page's AceConfigDialog tree is re-acquired on every `Open`, so paint after
  each. Any future host `OnRelease` goes through `Skin:OnRelease`. Column blocks are raw frames kept in a
  private attic (`ColumnBlocks.lua:105`), not pooled AceGUI: safe.
- **R5. Layering.** Shell's edge holder sits one level over the window frame; rows, the drag bar and the
  header controls sit at `LAYERS.LEVEL` offsets (`core/Constants.lua`; `tests/test_layers.lua`). Check the
  holder does not cover the controls band or steal the drag bar's mouse.
- **R6. Migration reach.** `ResetToSkin` on a key whose companion is absent writes `"@skin"` into an LSM
  key; stored windows lack the companions, so backfill first. The runner is account-wide; it must reach
  every profile in `sv.profiles`, not just `db.profile`.
- **R7. Combat.** The picker defers to `PLAYER_REGEN_ENABLED`; settings writes are combat-locked
  (Options 27). A skin switch never needs a protected call (no secure frames: the binding button
  `core/LauncherSetup.lua:153` is a plain Button).
- **R8. File cap (1500).** `settings/Schema.lua` 1448, `modules/Window.lua` 1440, `settings/Schema_Compose.lua`
  1408, `modules/Aggregator.lua` 1343, `modules/Window_Header.lua` 1337, `modules/Row.lua` 1260,
  `core/Database.lua` 1252, `locales/enUS.lua` 1167, `modules/Tooltip.lua` 1155. The `skin` modes and
  companions land in the first three; expect a split (e.g. the schema's color-mode rows, or `ApplyBorder` /
  the empty state out of `Window.lua`) before adding.
- **R9. Test pins of today's colors.** `tests/test_row*.lua`, `test_window_header*.lua`,
  `test_headercontrols.lua`, `test_tooltip_*.lua`, `test_export_modal.lua`, `test_schema_defaults.lua`,
  `test_database_migrations.lua` assert literals and defaults; under Ka0s Default with the gap tokens they
  stay green except where D1, D3, D7 and D8 move a pixel.

## 9. Effort

**XL.** A meter whose whole body is per-window HUD style: about 23 style settings across nine composed
groups and ten color modes to put on the skin, an R3 migration over every profile and every window,
the window shell's player-owned edge to reconcile with `S.Shell`, four gap tokens, and three authored
files within 100 lines of the cap that need splitting first.
