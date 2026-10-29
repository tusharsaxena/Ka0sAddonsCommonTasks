# M0 inventory: the library's custom widgets (LK-06) and the drag handle's tooltip (LK-08)

Read-only inventory of `../LibKa0s` on `master` at `ea1d92d` (v1.80.0 merged; the run branch
`feat/2026-10-30-skin-library-followups` did not exist in LibKa0s when this was read). Every citation
is `path:line`, relative to the LibKa0s repo root (`LibKa0s/<file>.lua` is the payload, `tests/`,
`docs/api/`), unless it names another repo. Nothing was edited, run or committed.

Scope: LK-06 (R-5, every custom widget the library draws outside AceGUI, skinned and obeying the
Scope switches) and LK-08 (R-7, WidgetsDragHandle's tooltip title and body take `gtip.*`). `S.Text`
and `WidgetsReorder` are LK-05 and appear here only where they share a mechanism.

---

## 0. How skinning and the Scope work today (what every item below builds on)

- **Token reads.** `Skin:Token(owner, name)` / `Skin:Color` (`LibKa0s/Skin.lua:811-822`) resolve the
  owner's full table (`__Tokens`, `LibKa0s/Skin.lua:804-807`). Facade `S.Token`, `S.Color`
  (`LibKa0s/Skin.lua:1016-1018`).
- **Repaint.** Primitives record through `Skin:Track` (`LibKa0s/Skin.lua:928-946`) and `Repaint`
  replays them (`LibKa0s/Skin.lua:986-1000`). Widgets that read tokens directly re-run a recorded
  function on `OnLooksChanged` through `lib.__onSkin` (`LibKa0s/Widgets.lua:142-155`).
- **Owner check for the Widgets major.** `skinOf(owner)` answers the Skin major only for a
  registered owner (`LibKa0s/Widgets.lua:120-126`, exported `lib.__skinOf`); Core's equivalent is
  `Core.__SkinFacade` (`LibKa0s/Core.lua:192-198`).
- **Ignore fonts** is enforced in ONE place: `P.font` gives the string back its own face when
  `__FontsIgnored(owner)` (`LibKa0s/SkinPaint.lua:537-539`; flag at `LibKa0s/Skin.lua:634-637`). So
  any string painted through `P.font` / `P.label` / `S.Text` / `S.Font` / `S.White` / a primitive
  that labels (Button, Dropdown, EditBox, Tab, NavItem, Cover, Shell's `frame.title`) obeys it for
  free. A string a widget never routes through `P.font` draws its template's face (Friz) in every
  skin, so it neither follows the skin nor has anything to ignore. A widget that calls
  `fs:SetFont(<skin face>)` itself BYPASSES Ignore fonts.
- **Ignore settings panel** is enforced only by the Options chrome (`lib.__chromeSkin`,
  `LibKa0s/OptionsScroll.lua:259-265`, and everything built on it: `__chromePaint`
  `LibKa0s/OptionsScroll.lua:316-331`, `__chromeAway` `:269-277`, `paintPage` `:384-396`, the
  instance members `:453-488`) and by `Skin:PaintAce` (`LibKa0s/SkinAce.lua:802-806`). Nothing in
  the Widgets major, Core, the tool windows or Toast asks it. Per skinning.md §7 the panel exception
  covers the settings panel only; the addon's windows, HUD and tool windows are not the panel
  (`../WowAddonStandards/standards/standards/skinning.md:5`).
- **`__chromeAway` no longer means "away from Ka0s Default".** It returns nil only when
  `P.isDefault(owner)` is true (`LibKa0s/OptionsScroll.lua:269-277`), and `P.isDefault` answers false
  always since SkinPaint minor 6 (`LibKa0s/SkinPaint.lua:170-173`). So every "away from Ka0s Default
  only" call site now paints under Ka0s Default too. See finding F-1 (section 6).
- **New tokens.** Schema groups are strings in `LibKa0s/SkinDefs.lua:106-170`; Ka0s Default values
  in `KA0S` (`LibKa0s/SkinDefs.lua:208-372`); the eight other skins come from their mockup maps
  (`MOCK_MAP` `:425-466`), the washes (`:469-479`), `FOLLOW` (`:482-488`, copies the source token
  when the skin set it and the follower is nil) and `KEEP` (`:524-525`); per-skin overrides go in a
  skin's `extra` table. The `eui` source is Ka0s Default with EllesmereUI's accent, panel color and
  font laid over the tokens named in `ACCENT_TOKENS` / `PANEL_TOKENS` / `FONT_TOKENS`
  (`LibKa0s/SkinEUI.lua:104-107`, `derive` `:304-317`): a new token is Ka0s Default's value under
  `eui` unless it is added to one of those lists. Bumping a token means `DEFS_MINOR` 15 -> 16
  (`LibKa0s/SkinDefs.lua:94`), the token tables and per-skin tables in
  `docs/api/Skin/version-7.15.11.5.9.2.4-docs.md` (token rows `:410-670`, per-skin tables
  `:1160-1320`), and a pin like `tests/test_widgets_skin.lua:438-453`.
- **Ka0s Default's font is Oxanium** (`font.body` "Ka0s Oxanium SemiBold", `LibKa0s/SkinDefs.lua:212`).
  Every string LK-06 newly routes through `P.font` changes face under Ka0s Default from the
  template's Friz Quadrata to Oxanium. See decision D-1 (section 5).

Per-skin values quoted below ("·" = inherits Ka0s Default) are the docs' tables,
`docs/api/Skin/version-7.15.11.5.9.2.4-docs.md:1166-1185` (Text) and `:1290-1315`
(Menus, Lists, Icons).

---

## 1. Inventory, family by family

Legend: **Owner**: how it learns its skin owner. **Skinned**: surfaces painted from tokens when
owned. **Gaps**: literals or template fonts still drawn while OWNED (the unowned fallback literals are
by design and listed only where a gap shares them). **Scope**: panel = Ignore settings panel,
fonts = Ignore fonts.

### 1.1 Widgets.lua: dropdown, shared popup menu, search box, test strip

- **Owner**: `opts.owner` (`LibKa0s/Widgets.lua:541-543`, `:670-677`, `:730-731`); the shared menu
  follows its opener (`skinMenu`, `LibKa0s/Widgets.lua:300-319`), back to Ka0s Default through
  `DEFAULT_OWNER` (`:167`) on an owner-less open.
- **Skinned**:
  - Dropdown button: `S.Dropdown` (`LibKa0s/Widgets.lua:543`) = box from `input.*`, arrow via
    `icon.arrow` (P.glyph), label `input.text` + body font (`LibKa0s/SkinPaintControls.lua:325-339`).
    Unowned literals: `SKIN` `LibKa0s/Widgets.lua:98-104`, arrow `:479`.
  - Menu frame: `S.MenuFrame` (`LibKa0s/Widgets.lua:305`), backdrop only
    (`LibKa0s/SkinPaintExtras.lua:214-237`). Row colors from `menu.textSel` / `menu.text` /
    `menu.hover` (`LibKa0s/Widgets.lua:306-310`, applied in `paintMenuRow` `:263-276`).
    Unowned literals `MENU_PAL` `:165`, backdrop `:327-328`, row highlight `:216`.
  - SearchBox: `S.EditBox` (`LibKa0s/Widgets.lua:672`) = box, typed text, body font, hint in
    `input.placeholder` + body font, focus edge (`LibKa0s/SkinPaintControls.lua:218-235`); icon in
    `icon.tint` (`LibKa0s/Widgets.lua:603-607`, `:673-676`). Unowned: `:632-635`, `:645`, `:651`.
  - TestStrip wash: `S.Strip` (`LibKa0s/Widgets.lua:731`, `LibKa0s/SkinPaintExtras.lua:176-179`).
    Unowned: `STRIP_FILL` `:686-689`.
- **Gaps (owned)**:
  - G-W1 menu row label font: `GameFontHighlightSmall` (`LibKa0s/Widgets.lua:192`), never re-fonted;
    the menu's width is measured in the same template (`menu.measure`, `:174-185`). Rows are pooled
    across every addon (`:186-188`, `:377-395`).
  - G-W2 TestStrip text: `GameFontNormalSmall` (`LibKa0s/Widgets.lua:743`), neither colored nor
    fonted (the template's gold `1, 0.82, 0`). The strip's icon (`:733-740`) is host art carrying
    meaning: leave it.
  - (not a gap) the glyph column `b.glyph` (`:209`, `SetFont(dd.__glyphFont, 11, "")` `:250-252`) is
    the host's mono face by contract (`:33-34`); leave it.
- **Tokens**: G-W1 font role `body` (no color change: `menu.text` already applied). G-W2 color
  `text.accent` (Ka0s Default GOLD `1, 0.82, 0, 1` = the template's NORMAL_FONT_COLOR exactly,
  `LibKa0s/SkinDefs.lua:189`, `:226`) + body font: `S.Text(text, "accent")`. No new token.
- **Scope**: fonts obeyed once G-W1/G-W2 go through `P.font`. Panel: not the settings panel
  (addon windows: LootHistory, BankLedger, MultiMeters, DropWatcher filter bars). A host that puts
  one on a settings page needs LK-05's panel mechanism (section 4.2).
- **Implementation notes**: G-W1 must re-font the pooled rows on EVERY open for the opener (as
  `__pal` is), put the stock template back on an owner-less open (the `DEFAULT_OWNER` facade reads
  Ka0s Default, whose `font.body` is Oxanium, so painting through it would NOT restore minor 15's
  look; restore with `SetFontObject(GameFontHighlightSmall)` or `P.unpaint` of the row's record),
  and measure in the font the rows now wear (re-font `menu.measure` with the same call before
  `menuWidth`, `:173-185`), else long labels truncate. Pooled rows painted for owner A then opened by
  owner B: `Skin:Track` gives the frame back to A's look first (`LibKa0s/Skin.lua:931-936`), so
  route through a tracked facade call (`S.Font`/`S.Text`), not a bare `SetFont`.

### 1.2 WidgetsAutocomplete.lua

- **Owner**: `opts.owner` (`LibKa0s/WidgetsAutocomplete.lua:414`); palette read on every show
  (`palette` `:125-130`).
- **Skinned**: row text `menu.text`, highlight `menu.hover` (`:125-130`, applied `:218-222`); the
  list's backdrop copies the box's colors (`skin` `:197-203`), so a skinned SearchBox carries it.
  Unowned literals `AC.BORDER/BG/TEXT/HIGHLIGHT` `:79-80`, highlight `:162`.
- **Gaps (owned)**: G-A1 row label font `h.__font` = `opts.font or AC.FONT` (`:168`, `:414`;
  `AC.FONT = "GameFontHighlightSmall"` `:78`), never re-fonted. Paint only when the host passed no
  `opts.font` (a host face wins, as the chart's does). Consumers: BankLedger
  (`../BankLedger/modules/Browser.lua`), LootHistory (`../LootHistory/core/WidgetsSetup.lua`).
- **Tokens**: font role `body`. No new token.
- **Scope**: fonts via `P.font`; panel: not the settings panel.

### 1.3 WidgetsCopyWindow.lua

- **Owner**: the descriptor's `addonName` when registered and no `applySkin` (`LibKa0s/WidgetsCopyWindow.lua:153`).
- **Skinned**: window through `Core.ApplySkin(f, nil, owner)` -> `S.Shell` (`:157`), which also
  colors and fonts `f.title` (`LibKa0s/SkinPaint.lua:992-993`; title built at
  `LibKa0s/WidgetsCopyWindow.lua:190-193`); dense fill `win.bgDense` (`:131-136`); scroll bar
  `S.ScrollBar` (`:143`); close via `Core.MakeCloseButton(bar, ..., d.addonName)` -> `S.CloseButton`
  (`:201-205`, `LibKa0s/Core.lua:303-304`).
- **Gaps (owned)**:
  - G-C1 the resize grip: `Core.MakeResizable` draws the client's chat size-grabber art
    (`LibKa0s/Core.lua:603-605`, set at `:675-677`), untinted, and `MakeResizable` takes no owner
    (`opts` read at `:640-760`). Shared with every Core-resizable window (debug console, perf and sim
    panels, copy windows, hosts' windows).
  - (not a gap) the edit box face is the host's path (`:214`), mono by contract (`:209-213`); its
    text color is the client default (white). Optional only: `log.text` (Ka0s Default WHITE,
    `LibKa0s/SkinDefs.lua:232`) would keep Ka0s Default exact. Recommend leaving it.
- **Tokens**: G-C1 needs a NEW token (no existing one leaves the art as drawn under Ka0s Default):
  see T-3 `icon.grip` (section 3).
- **Scope**: fonts (title) via Shell; panel N/A.

### 1.4 WidgetsLineChart.lua

- **Owner**: `opts.owner` (`LibKa0s/WidgetsLineChart.lua:557`, repaint `:545-552`, `:574`).
- **Skinned**: axis, grid, crosshair, marker, line, series from `S.ChartStyle()`, label color
  `text.disabled` (`:77-85`); unowned `lib.LINE_CHART` `:62-66`.
- **Gaps (owned)**: G-L1 axis/tick labels' face `c.__opts.font or "GameFontDisableSmall"`
  (`:330`), colored (`:333-334`) but never fonted. Paint only without a host `opts.font`. Labels are
  pooled per chart (`acquireLabel` `:325-337`): font each new one once; S.Text-tracking each is fine
  (weak registry). Consumer: LootHistory (Insights).
- **Tokens**: font role `body`; color stays `text.disabled` (Ka0s Default DIM `0.5` = the template's
  gray). An `S.Text(fs, "disabled")` call would cover both.
- **Scope**: fonts via `P.font`; panel N/A.

### 1.5 WidgetsDragHandle.lua (LK-06 label font; LK-08 tooltip, section 2)

- **Owner**: `spec.owner` (`LibKa0s/WidgetsDragHandle.lua:755`, `dhPalette` `:186-194`, repaint
  `:544-555`, hooked `:768`).
- **Skinned**: strip fill `handle.bg`, edge `handle.edge`, label color `text.accent`, marks
  `icon.tint` / `icon.hot` (`:186-194`, `:529-555`). Unowned `DH_PAL` `:181-182`, `HELP_TINT(_OVER)`
  `:176-177`. Tests: `tests/test_widgets_skin.lua:307-337`.
- **Gaps (owned)**:
  - G-D1 label face `spec.labelFont or "GameFontNormalSmall"` (`:200`, `:575-589`) never fonted.
  - G-D2 tooltip title/body/footer literals (`:335-342`): LK-08, section 2.
  - (art) `HELP_FALLBACK` / `CLOSE_FALLBACK` (`:149`, `:153`) are only the no-Media rungs; tinted.
- **Measuring constraint for G-D1**: the label is measured on a hidden per-face measurer in the
  TEMPLATE face (`lib.__DragHandleMeasurer` `:214-225`, `dhLabelWidth` `:236-241`, `Measure`
  `:653-655`); the measurer exists because AuraMaster's anchor answers secret geometry
  (`:202-209`). If the label is re-fonted, the measurer must be set to the same path/size/flags
  (`measurer:SetFont(label:GetFont())` after the paint, or a measurer keyed by owner+face), else
  `ApplyWidth` sizes the strip for Friz and Oxanium/Inter text truncates. Only when the host passed
  no `spec.labelFont`; no consumer passes one today (grep of AbsorbTracker, AuraMaster,
  ConsumableMaster, KickCD, QuickComms found none).
- **Tokens**: font role `body` (or `S.Text(label, "accent")`, which also replaces the label color
  write in `dhRepaint` `:551`). No new token.
- **Scope**: fonts via `P.font`; panel N/A (a HUD strip). Consumers: AbsorbTracker
  `../AbsorbTracker/modules/Bar.lua:135`, AuraMaster `../AuraMaster/modules/Anchors.lua:690`,
  ConsumableMaster `../ConsumableMaster/modules/MacroBar.lua:276`, KickCD
  `../KickCD/modules/Castbar_Handle.lua:92` and `../KickCD/modules/IconGrid_Handle.lua:133`,
  QuickComms `../QuickComms/core/WidgetsSetup.lua:26`.

### 1.6 WidgetsReorder.lua (LK-05's; noted for the shared mechanism)

- Tooltip literal `GameTooltip:AddLine(tip, 1, 1, 1)` (`LibKa0s/WidgetsReorder.lua:626`) ->
  `gtip.value` (WHITE, exact). Whoever lands LK-05 should take it, or LK-06d (section 4) does.

### 1.7 Core.lua: window skin, close control, resize grip

- `Core.ApplySkin(frame, skin, owner)` -> `S.Shell` (`LibKa0s/Core.lua:218-227`); `MakeCloseButton`
  -> `S.CloseButton` (`:269-307`). Both done (Core minor 13). Unowned `lib.SKIN` `:94-108`,
  `CLOSE_REST/HOT` literals `:286-296`. Close glyph fallback `GameFontNormalLarge` (`:291`) is
  colored by `S.CloseButton`; its face is not fonted (minor; leave it, it is a glyph).
- Gap G-C1 (the grip) as in 1.3: `LibKa0s/Core.lua:595-605`, `:675-677`.

### 1.8 Toast.lua

- Owner `d.owner`; chrome is `Core.ApplySkin(f, nil, S.d.owner)` and
  `Core.MakeCloseButton(..., S.d.owner)` (`LibKa0s/Toast.lua:215-223`). The body is the host's
  builder (`:261-276`). No literal color, font or texture in the file. **Nothing to do**; panel N/A.

### 1.9 Launcher.lua

- Draws no frame: the LDB tooltip lines go into whatever tooltip the broker display hands it
  (`LibKa0s/Launcher.lua:302-319`), and the options menu is the client's `MenuUtil`
  (`:384-396`, a Blizzard shared frame, skinning.md §7). Literals: status words `GREEN`/`RED`
  `|cFF00FF00` / `|cFFFF0000` (`:116`, used `:283-285`); other lines pass no color.
- The standard fixes those two colors as the tooltip's only color:
  `../WowAddonStandards/standards/standards/launcher.md:24`, `:35`. **Recommend no item**: record the
  exclusion in DECISIONS (a token pair would be identical in all nine skins, and no skin sets
  `sem.on` / `sem.off` to follow, `LibKa0s/SkinDefs.lua:327-328`).

### 1.10 DebugLogWindow.lua (+ DebugLog.lua)

- **Owner**: `d.addonName` when no `skin` / `applySkin` (`LibKa0s/DebugLog.lua:301-312`); palette
  `PALETTE` (`LibKa0s/DebugLogWindow.lua:111-124`) refilled on switch (`adopt` `:501-509`).
- **Skinned**: window/title/divider (Core.ApplySkin -> Shell; `f.title` `:420-427`), scroll bar
  `S.ScrollBar` (`:503`), status rule `S.Divider` (`:504`), every text and icon color (rest, icon,
  hot, diag, diagHot, on, off, rule, count, ts, tag, text). Unowned literals `:92-98`, `:118-124`,
  track/thumb `:382-384`, divider fallback `:437-438`.
- **Gaps (owned)**: G-DL1 four label faces never fonted: Copy/Clear text buttons
  `GameFontNormalSmall` (`:147`), the Diagnostics link (`:260`), the ON/OFF toggle (`:466`). The log
  and line counter use the host's mono path (`:356`, `:408`) by contract (`font.mono` exists,
  `LibKa0s/SkinDefs.lua:213`, but the descriptor names the face; leave it).
- **Width**: the console's minimum width measures these strings (`textWidth`,
  `buildDiagnosticsLink` `:256-273`); font them before measuring (adopt runs after build,
  `:525+`), or re-measure on `OnLooksChanged`.
- **Not surfaces**: the chat acknowledgement `|cff40ff40` / `|cffff4040`
  (`LibKa0s/DebugLog.lua:612-613`) and `FormatColored` (`:164-167`) are chat / copy text, not a
  skinned surface (skinning.md:5 lists none). Leave them.
- **Tokens**: font role `body`. No new token. **Scope**: fonts via `P.font`; panel N/A.

### 1.11 PerfPanel.lua

- **Owner**: `d.addonName or d.name` (`LibKa0s/PerfPanel.lua:124`), palette `:86-96`, adopted
  `:275-292`.
- **Skinned**: window (ApplySkin), title (`frame.title` `:244-247`, Shell), row colors from tokens
  (`sem.on`, `sem.step*`, `text.faint`, `text.accent`), dot (`:318-319`). Unowned `COLORS` `:51-61`,
  `CMD_COLOR` `:65`, `HOVER*` `:68`.
- **Gaps (owned)**: G-P1 row command and label faces `GameFontNormalSmall` (`:170`, `:181`) never
  fonted. The label is anchored between bounds (`:177-185`), so no measuring issue.
- **Tokens**: font role `body`. **Scope**: fonts via `P.font`; panel N/A.

### 1.12 SimPanel.lua

- **Owner**: `d.addonName` (`LibKa0s/SimPanel.lua:153-172`, `TOKENS` `:158-160`, adopt `:388-396`).
- **Skinned**: window, title (`:248-250`), each button box (`S.Shell(b, { noTopBar = true })`
  `:707`), row and button label colors, dot and check (`:369-380`).
- **Gaps (owned)**:
  - G-S1 the picker's two dropdowns are built with NO owner: `W.Dropdown(pk, SCENARIO_W)` and
    `W.Dropdown(pk, SIZE_W)` (`LibKa0s/SimPanel.lua:764`, `:773`). They draw Widgets minor 15's
    literals in every skin, and their menu opens owner-less (put back to Ka0s Default). Fix: pass
    `{ owner = <the panel's owner> }` (the panel frame's `__skin` owner / `P.ctx.d.addonName`).
  - G-S2 row `cmd` and `text` faces (`:333`, `:339`) and the button label (`:709`)
    `GameFontNormalSmall`, never fonted.
  - G-S3 the row tooltip (`showTip`, `:681-694`): `AddLine(.., 1, 1, 1)` (`:688`, `:692`) and
    `AddDoubleLine(.., 0.9, 0.82, 0.5, 1, 1, 1)` (`:690`); the title `SetText` passes no color
    (`:685`).
- **Tokens**: G-S2 font role `body`. G-S3 white -> `gtip.value` (WHITE, exact,
  `LibKa0s/SkinDefs.lua:239`); the double line's left `0.9, 0.82, 0.5` matches no token
  (`text.headingAlt` is `0.91, 0.77, 0.42`, `drawer.summarySet` `0.91, 0.85, 0.66`): either a NEW
  token T-4 `gtip.key` (section 3) or accept `gtip.title` (gold) as a recorded Ka0s Default change.
- **Scope**: fonts via `P.font`; panel N/A.

### 1.13 SimTimeline.lua

- Logic only (the step machine, `LibKa0s/SimTimeline.lua:1-60`); draws nothing. **Nothing to do**.

### 1.14 Glow.lua

- Delegates to LibCustomGlow with the HOST's `knobs.color` (`LibKa0s/Glow.lua:80-92`); no literal.
  The skin's `glow.color` reaches hosts through `S.GlowColor` (`LibKa0s/SkinPaintExtras.lua:424`)
  and OptionsCompose. **Nothing to do**.

### 1.15 Options chrome (settings panel: Ignore settings panel APPLIES)

Everything here is painted through `O.__chromePaint` / `__chromeSkin`, so it already stands down
under Ignore settings panel and gives its targets back (`LibKa0s/OptionsScroll.lua:296-331`).
Gaps are what those calls do not reach.

- **OptionsDrawer.lua** (head `newHead` `LibKa0s/OptionsDrawer.lua:112-136`, dress `:240-263`, box
  `:356`). Painted by `S.Drawer` (`LibKa0s/SkinPaintControls.lua:706-728`).
  - G-O1 label (`GameFontNormal`, `LibKa0s/OptionsDrawer.lua:125`) and summary
    (`GameFontHighlightSmall`, `:130`) are TINTED only: `drawerText` uses `P.tint`, not `P.label`
    (`LibKa0s/SkinPaintControls.lua:706-710`), so no skin face and nothing for Ignore fonts to do.
    Fix in the primitive: `P.label(owner, rec, fs, T, token, "body")` for both (the summary keeps its
    smaller stock size through `P.fontSize`'s scaling, `LibKa0s/SkinPaint.lua:520-528`).
  - G-O2 chevron `CHEVRON_TEX` (`LibKa0s/OptionsDrawer.lua:76`, `:121-124`) untinted in-client
    yellow arrow art. Token `icon.arrow` through `P.glyph` (the dropdown's arrow precedent,
    `LibKa0s/SkinPaintControls.lua:333-334`; Ka0s Default GOLD on desaturated art, as every other
    arrow since SkinDefs minor 12, `LibKa0s/SkinDefs.lua:76-79`). Pass it as `opts.chevron` to
    `S.Drawer`.
  - G-O3 hover highlight `HOVER_TEX` quest-log art, ADD, alpha .35 (`:75`, `:117-120`), untinted.
    NEW token T-2 `list.hoverArt` (section 3).
  - G-O4 tooltip `SetText(label, 1, 1, 1)` + `AddLine(tip, nil...)` (`:284-285`): LK-06d.
- **OptionsNav.lua** (entry `newEntry` `LibKa0s/OptionsNav.lua:164-180`, dress `:186-206`, rail
  `:133-144`, `:218`). Painted by `S.NavItem` (label via `P.label`, sel tint) and `S.Panel{nav}`.
  - G-O5 hover highlight `SELECT_TEX` ADD (`:52`, `:169-172`), untinted: T-2.
  - G-O6 tooltip `SetText(.., 1, 1, 1)` (`:153`), `AddLine(.., nil..)` (`:154`): LK-06d.
  - (not a gap) the rail's tooltip-border backdrop art (`:57-64`) is recolored by
    `nav.bg`/`nav.border` (`LibKa0s/SkinPaintExtras.lua:243-248`); its style token is not applied,
    by design (it keeps its art).
- **OptionsTabs.lua**: tabs `S.Tab` (`LibKa0s/OptionsTabs.lua:500-504`; label via `P.label`,
  `LibKa0s/SkinPaintControls.lua:497-500`), content panel and rule (`:492-496`, `:1025`, `:1087`).
  Template font objects at `:342-344`, `:357` are re-fonted by `S.Tab`.
  - G-O7 tooltip `SetText(.., 1, 1, 1)` (`:715`), `AddLine(.., nil..)` (`:717`): LK-06d.
  - Unowned literals `CHROME_RULE_COLOR` `:185`, glow/fill `:193`, `:218`, `:276` are the
    panel-ignored look: leave them.
- **OptionsIdList.lua**:
  - Help mark tinted from tokens through `__chromeAway` (`LibKa0s/OptionsIdList.lua:553-563`); see
    F-1: under Ka0s Default it now reads `text.accent` (gold `1, 0.82, 0`) instead of
    `ID_HELP_TINT` `0.82, 0.65, 0.21` (`:185`), contrary to its own comment (`:553-554`).
  - G-O8 entry highlight `ID_ENTRY_HILITE` (`:87`, set on an AceGUI InteractiveLabel `:822-823`);
    SkinAce's label painter does not touch the highlight (`LibKa0s/SkinAce.lua:487-495`): T-2.
  - G-O9 tooltip `SetText(name, 1, 1, 1)` (`:613`), `AddLine(line, 0.8, 0.8, 0.8, true)` (`:615`):
    LK-06d. `0.8` matches no token exactly (`text.value` is `0.8, 0.8, 0.82`,
    `LibKa0s/SkinDefs.lua:237`; `gtip.subtle` `.7`; `gtip.body` `.9`): NEW token T-5 `gtip.detail`
    or accept `gtip.body` with a recorded `+.1` change.
- **OptionsIds.lua** (the id suggestion popup, `suggestFrame` `LibKa0s/OptionsIds.lua:1012-1028`;
  painted by `S.MenuFrame(f, { popup = true })` at `:1117`, backdrop only).
  - G-O10 suggestion rows: label `GameFontHighlightSmall` (`:1002`, via `newSuggestLine` `:982-998`),
    neither colored nor fonted (the template's white). Token: `menu.text` + body font (Ka0s Default
    `0.9` vs the template's `1.0`: a recorded change, consistent with the dropdown menu's rows,
    `LibKa0s/Widgets.lua:309`), or `text.highlight` (WHITE in all nine skins,
    `LibKa0s/SkinDefs.lua:238`) to keep Ka0s Default exact. Recommend `menu.text` (D-4).
  - G-O11 the "more" line `GameFontDisableSmall` (`:1025`): `text.disabled` (DIM `0.5` = the
    template's gray) + body font. Exact.
  - G-O12 row highlight `SUGGEST_HIGHLIGHT` (`:911`, `:1003`): T-2.
  - G-O13 `ID_GRAY = "|cff808080"` inline in labels (`:678`): `text.disabled` as hex (the docs
    already map LedgerFormat's `|cff808080` to `text.disabled`,
    `docs/api/Skin/version-7.15.11.5.9.2.4-docs.md:716-717`). Needs the owner at string-build time.
  - Unowned backdrop `SUGGEST_BACKDROP` `:912-917`, `SetBackdropColor(0, 0, 0, 0.92)` `:1020`: by
    design (the popup recolor restores it).
- **OptionsWidgets.lua**: `O.AttachTooltip` (`LibKa0s/OptionsWidgets.lua:516-535`), the tooltip on
  EVERY settings row and control: `SetText(label, 1, 1, 1)` (`:524`), `AddLine(tooltip, nil..)`
  (`:527`). G-O14: LK-06d. `TextRow` font objects (`:160-161`, `:380`, `:568-569`) are AceGUI rows
  painted by SkinAce: not LK-06.
- **OptionsKeybinds.lua**: key button tooltip `SetText(S.KEY, 1, 1, 1)` (`:730`), three
  `AddLine(.., nil..)` (`:731`, `:736-737`). G-O15: LK-06d. Row labels colored via `__chromeAway`
  (`:657-663`), affected by F-1.
- **OptionsCombat.lua**: the cover, `S.Cover` with its text (`LibKa0s/OptionsCombat.lua:213-241`,
  primitive `LibKa0s/SkinPaintExtras.lua:183-188`, `P.label`). Done. Unowned `:221-224`.
- **Options.lua**: the page header, `S.Text(panel.title, "title")` and the divider tint
  (`paintPage`, `LibKa0s/OptionsScroll.lua:384-396`; built `LibKa0s/Options.lua:640-655`). Done.
  `COMBAT_REFUSED` / `COMBAT_LOCKED_NOTICE` `|cffaaaaaa` (`:217`, `:224`) are chat lines: leave.
- **OptionsAppearance.lua** (the Skin tab): AceGUI rows (SkinAce) and `muted` via `__chromeAway`
  (`:252-257`). `MARK_OK` / `MARK_FAIL` (`:121-122`) are the client's ready-check art (meaning) and
  `SWATCH` (`:123`) draws skin data: leave. Nothing to do.
- **OptionsCompose.lua**: AceGUI pickers; `S.Resolve` (`:519-520`) is LK-01's. Nothing to do here.

### 1.16 OptionsSkinPicker.lua (a dialog, not the settings panel; LK-11 edits the same file)

- **Owner**: `spec`'s owner, facade `P.Sk` (`LibKa0s/OptionsSkinPicker.lua:706`).
- **Skinned**: window `Core.ApplySkin(f, nil, P.owner)` (`:643`), title (`f.title` `:637-641`, via
  Shell), dropdown `S.Dropdown` (`:612`, its `dd.arrow` `:603-608` via `icon.arrow`, `dd.text`
  fonted), list `S.MenuFrame` (`:591`), rows `S.ListRow` (`:371`, `:572-573`) with
  `text.body` color (`:368-372`), buttons `S.Button` (`:538`, `:552`; icon `btn.icon` and glyph
  `btn.text` via `labelOf`), close control via Core.
- **Gaps / scope questions**:
  - G-K1 each row's name is set in THAT skin's own face by a bare `fs:SetFont(path, size, "")`
    (`:565-568`, `skinFace` `:286-291`), deliberately (header `:66-68`). It bypasses Ignore fonts.
    D-3 asks whether Ignore fonts should put the rows back on the owner's own face.
  - G-K2 tooltips `GameTooltip:SetText(self.__tip or "")` (`:297-305`), no color: nothing literal;
    leave unless LK-06d decides to color nil-colored lines (D-2).
  - Panel scope: the picker is a first-run dialog, not the settings panel; today it paints
    regardless of Ignore settings panel. D-3 confirms.
- **Sequencing**: LK-11 rewrites the title line (`TITLE_FOR` `:106`, `titleText` `:240-245`, title
  anchors `:637-641`, `WIDTH` `:120`). Land LK-11 first and let LK-06 touch this file only for
  G-K1, or fold G-K1 into LK-11's commit.

---

## 2. LK-08: WidgetsDragHandle's tooltip (R-7)

### 2.1 The literals

`dhTooltipLines` (`LibKa0s/WidgetsDragHandle.lua:335-342`):

| Band | Literal | Line | Where drawn |
|---|---|---|---|
| title | `1, 0.82, 0` (`tr or 1, tg or 0.82, tb or 0`) | `:338` | `tip:SetText` `:348` |
| body | `1, 1, 1` (`dhBand(t.body, 1, 1, 1)`) | `:339` | `tip:AddLine(.., true)` `:349` |
| footer | `0.6, 0.6, 0.6` (`dhBand(t.footer, 0.6, 0.6, 0.6)`) | `:340` | after a `" "` spacer `:350-353` |

An entry's own `{ text, r, g, b }` color wins over the band default (`dhEntry` `:282-288`,
`dhBand` `:293-303`); keep that. The tooltip is always `GameTooltip` (`:374-376`): only the line
colors change, never the frame (skinning.md §7,
`../WowAddonStandards/standards/standards/skinning.md:89-91`).

Call sites (all three must get the palette): strip `:766`
(`dhShowTooltip(handle, spec, spec.tooltip)`), help mark `:445-448`, close mark `:495-498`; the
placed path `dhShowPlaced` `:362-369` redraws the same evaluated lines.

### 2.2 The tokens (Ka0s Default value; the eight skins; eui)

| Band | Token | Ka0s Default | Exact today? | Obsidian / Azeroth / Glass / HC / Ember / WoW / Midnight / Forever | eui |
|---|---|---|---|---|---|
| title | `gtip.title` | `1, 0.82, 0, 1` (`LibKa0s/SkinDefs.lua:226`) | yes | · / `#F5C542` / · / `#FFE600` / `#FFB45A` / · / `#F6D27A` / `#FFD100` | Ka0s Default |
| body (rec.) | `gtip.value` | `1, 1, 1, 1` (`LibKa0s/SkinDefs.lua:239`) | yes | white in all eight (no skin sets it; docs `:1166-1185` has no row) | Ka0s Default |
| body (alt.) | `gtip.body` | `0.9, 0.9, 0.9, 1` (`:226`) | no (1.0 -> 0.9) | · / `#E9DDBC` / · / `#FFFFFF` / · / · / · / · | Ka0s Default |
| footer (rec.) | NEW `gtip.footer` (T-1) | `0.6, 0.6, 0.6, 1` | yes | FOLLOW `gtip.muted`: `#9B9BA4` / `#B8A07A` / `#C9CFDB` / `#E0E0E0` / `#C7A993` / `#B8B8B8` / `#B4AFC8` / `#A39E97` | Ka0s Default |
| footer (alt.) | `gtip.muted` | `0.5, 0.5, 0.5, 1` (`:226`) | no (0.6 -> 0.5) | as the row above | Ka0s Default |

**Recommendation** (D-5): title `gtip.title`, body `gtip.value`, footer a new `gtip.footer` that
FOLLOWs `gtip.muted`. That keeps Ka0s Default pixel-exact (skinning.md:64, "every golden and color
pin it carried stays green unchanged") and matches what the consumers already do by hand:
AuraMaster colors the title `gtip.title` and the body `gtip.value`
(`../AuraMaster/modules/Anchors.lua:538-544`, `:582-589`, `:614-620`) and ConsumableMaster's own
macro tooltip does the same (`../ConsumableMaster/core/MacroDisplay.lua:196-207`), so M2 can delete
AM's workaround with no visible change. The trade-off: `gtip.value` is white in every skin, so the
body only moves if a skin later sets it; `gtip.body` follows Azeroth and High Contrast but changes
Ka0s Default by 0.1. The footer has no exact existing token; footers are used by AbsorbTracker
(`../AbsorbTracker/modules/Bar.lua:172-179`) and ConsumableMaster
(`../ConsumableMaster/modules/MacroBar.lua:339-346`).

### 2.3 Implementation sketch

1. `DH_PAL` (`:181-182`): add `title = { 1, 0.82, 0 }`, `body = { 1, 1, 1 }`,
   `footer = { 0.6, 0.6, 0.6 }` (the unowned look; `tests/test_widgets_draghandle.lua:416-431` pins
   it and must stay green unchanged).
2. `dhPalette` (`:186-194`): `title = tok("gtip.title", DH_PAL.title)`,
   `body = tok("gtip.value", DH_PAL.body)`, `footer = tok("gtip.footer", DH_PAL.footer)` (fallback
   to the literal keeps a Skin copy without T-1 working).
3. `dhTooltipLines(t)` -> `dhTooltipLines(t, pal)` using `pal.title/body/footer` as band defaults;
   `dhShowTooltip(frame, spec, t)` -> also take the handle (or its `__pal`), read AT HOVER, so a skin
   switch applies without a rebuild (`dhRepaint` already swaps `handle.__pal`, `:544-546`). The help
   and close closures have `handle` in scope (`dhBuildHelp(handle, ...)` `:420`,
   `dhBuildClose(handle, ...)` `:473`).
4. `DRAG_MINOR` 6 -> 7 (`:56`), header line; Widgets docs: a new version file after
   `docs/api/Widgets/version-16.2.6.4.4.1-docs.md` (the key's third field is WidgetsDragHandle's
   minor; coordinate with LK-05's Reorder bump and LK-06a's Widgets bump so one new key carries
   all three).
5. T-1 in SkinDefs (section 3), docs token row next to `gtip.subtle`
   (`docs/api/Skin/version-7.15.11.5.9.2.4-docs.md:433`) and the per-skin Text table (`:1166-1185`).
6. Tests (fail without the change): in `tests/test_widgets_skin.lua` beside `:315-337`, an owned
   handle under Ka0s Default draws exactly `1,0.82,0` / `1,1,1` / `0.6,0.6,0.6`; under Azeroth the
   title is `#F5C542`, the footer `#B8A07A`; a `SetChoice` between hovers changes the next hover's
   colors with no rebuild; a band entry's own color still wins under a skin; another owner's handle
   is unaffected. The hover recorder is `hover` in `tests/test_widgets_draghandle.lua:48`. A
   SkinDefs pin: `gtip.footer` is `0.6,0.6,0.6,1` in Ka0s Default and equals `gtip.muted` in each of
   the eight skins.

Scope: GameTooltip lines are not the settings panel and carry no font of ours: neither switch
applies (the strip itself is a HUD element).

---

## 3. New tokens (each: Ka0s Default = today's look; a value per skin; eui)

| Id | Token | Group (`LibKa0s/SkinDefs.lua`) | Kind | Ka0s Default | The eight skins | eui | Needed by |
|---|---|---|---|---|---|---|---|
| T-1 | `gtip.footer` | Text (`:114-121`) | color | `0.6, 0.6, 0.6, 1` | FOLLOW `gtip.muted` (all eight set it: Obsidian `#9B9BA4`, Azeroth `#B8A07A`, Glass `#C9CFDB`, High Contrast `#E0E0E0`, Ember `#C7A993`, WoW Default `#B8B8B8`, WoW Midnight `#B4AFC8`, WoW Forever `#A39E97`) | Ka0s Default (not in any SkinEUI list) | LK-08 footer |
| T-2 | `list.hoverArt` | Lists and cards (`:145-152`) | color, nilable (`false` = leave the art) | `false`: the in-client ADD highlight art drawn as the client draws it | FOLLOW `text.accent` (Obsidian `#4DB8FF`, Azeroth `#E2B659`, Glass `#B69CFF`, HC `#FFE600`, Ember `#FF7A33`, Midnight `#B48CFF`, Forever `#C9A07A`); WoW Default `false` through its `extra` (the client's own look) | add to `ACCENT_TOKENS` (`LibKa0s/SkinEUI.lua:104-105`) so EllesmereUI's accent tints it, else `false` | G-O3, G-O5, G-O8, G-O12 |
| T-3 | `icon.grip` | Lists and cards (beside `icon.arrow`) | color, nilable (`false` = leave the art) | `false`: the client's size-grabber art untouched | FOLLOW `icon.tint` (Obsidian `#9B9BA4`, Azeroth `#B8A07A`, Glass `#C9CFDB`, HC `#E0E0E0`, Ember `#C7A993`, Midnight `#B4AFC8`, Forever `#A39E97`); WoW Default `false` via `extra` | Ka0s Default (`false`) | G-C1 |
| T-4 | `gtip.key` (optional) | Text | color | `0.9, 0.82, 0.5, 1` | FOLLOW `gtip.title` (Azeroth `#F5C542`, HC `#FFE600`, Ember `#FFB45A`, Midnight `#F6D27A`, Forever `#FFD100`; Obsidian, Glass, WoW keep Ka0s Default's) | Ka0s Default | G-S3 left column (only if D-6 keeps Ka0s Default exact) |
| T-5 | `gtip.detail` (optional) | Text | color | `0.8, 0.8, 0.8, 1` | FOLLOW `gtip.body` (Azeroth `#E9DDBC`, HC `#FFFFFF`; the rest keep `0.8`) | Ka0s Default | G-O9 lines (only if D-6 keeps Ka0s Default exact) |

Notes for the implementer:
- `false` is how Ka0s Default says "none" (`LibKa0s/SkinDefs.lua:17-19`, `:344-348`); `P.glyph`
  and `P.tint` leave the property alone (and give a prior back) for a falsy token
  (`LibKa0s/SkinPaint.lua:396-435`), so T-2 / T-3 painted through `P.glyph` (desaturate, then tint)
  draw today's art under Ka0s Default and WoW Default, and a tinted art everywhere else.
- `FOLLOW` runs inside `translate` before Ka0s Default is laid under it (`:528-549`), so a follower
  whose Ka0s Default is `false` still follows in the eight skins; an `extra` `false` stops it (the
  `out[f[1]] == nil` test, `:540`).
- Each new token needs a schema entry, the `KA0S` value, the FOLLOW row, a docs row, a per-skin
  table row, and a pin in the style of `tests/test_widgets_skin.lua:438-453`. One `DEFS_MINOR` bump
  covers all of them (`:94`).

---

## 4. Proposed split of LK-06 (roughly equal items)

### 4.1 The items

| Id | Family | Files | What | New tokens | Size |
|---|---|---|---|---|---|
| **LK-06a** | Widgets controls | `LibKa0s/Widgets.lua`, `LibKa0s/WidgetsAutocomplete.lua`, `LibKa0s/WidgetsLineChart.lua`, `LibKa0s/WidgetsDragHandle.lua` (label only) | G-W1 (menu row font, measure, owner-less give-back), G-W2 (strip text `text.accent` + font), G-A1, G-L1, G-D1 (+ measurer). Each only where the host named no face. Panel flag from LK-05 offered on every owned constructor (4.2). | none | M |
| **LK-06b** | Tool windows and Core | `LibKa0s/DebugLogWindow.lua`, `LibKa0s/PerfPanel.lua`, `LibKa0s/SimPanel.lua`, `LibKa0s/Core.lua` (grip), `LibKa0s/WidgetsCopyWindow.lua` (grip owner) | G-DL1, G-P1, G-S1 (dropdown owner), G-S2, G-S3 (tooltip), G-C1 (`MakeResizable` takes `opts.owner`; Copy, DebugLog, Perf and Sim pass theirs) | T-3 (+ T-4 if D-6) | M |
| **LK-06c** | Options chrome | `LibKa0s/SkinPaintControls.lua` (Drawer), `LibKa0s/OptionsDrawer.lua`, `LibKa0s/OptionsNav.lua`, `LibKa0s/OptionsIdList.lua`, `LibKa0s/OptionsIds.lua` | G-O1 (Drawer label/summary through `P.label`), G-O2 (chevron `icon.arrow`), G-O3/O5/O8/O12 (hover art T-2), G-O10/O11/O13 (suggest popup rows, more line, ID gray). All through `__chromePaint` / `__chromeSkin`, so Ignore settings panel holds and gives back. | T-2 | M |
| **LK-06d** | Tooltip lines the library writes | `LibKa0s/OptionsWidgets.lua` (`O.AttachTooltip`), `LibKa0s/OptionsDrawer.lua`, `LibKa0s/OptionsNav.lua`, `LibKa0s/OptionsTabs.lua`, `LibKa0s/OptionsKeybinds.lua`, `LibKa0s/OptionsIdList.lua`, (`LibKa0s/WidgetsReorder.lua:626` if LK-05 leaves it) | G-O4, O6, O7, O9, O14, O15: the settings tooltips' explicit `1, 1, 1` titles -> `gtip.value`, IdList's `0.8` lines -> T-5 or `gtip.body`; only while `O.__chromeSkin()` answers a facade (Ignore settings panel puts the literals back). One helper (e.g. `O.__tipColor(token, r, g, b)`) so six sites share it. Lands with or right after LK-08 (same token decision). | T-5 if D-6 | S-M |

LK-08 stays its own item (section 2). Suggested order: LK-08 + T-1, then LK-06d (reuses the gtip
decision), LK-06a, LK-06b, LK-06c. LK-06a and LK-08 both touch `LibKa0s/WidgetsDragHandle.lua`:
one minor bump for the file (7), or land LK-08 first and LK-06a takes 8; LK-06a, LK-05 and LK-08
all move the Widgets docs key, so write ONE new Widgets docs version file at the last of them.

No item (record in DECISIONS with the evidence): Toast (1.8), Launcher (1.9), SimTimeline (1.13),
Glow (1.14), Core window and close control (1.7), OptionsCombat, Options.lua's header,
OptionsAppearance, OptionsCompose (1.15), chat-markup strings (`LibKa0s/DebugLog.lua:612-613`,
`LibKa0s/Options.lua:217`, `:224`, `LibKa0s/Slash.lua:36-143`).

### 4.2 The Scope mechanism every item shares

- **Ignore fonts**: route every newly skinned string through a tracked facade call (`S.Text`,
  `S.Font`, `S.White`) or a primitive that calls `P.label` / `P.font`; never a bare `SetFont` with
  a skin face. Then Ignore fonts gives the string its own face back live (SetIgnore repaints,
  `LibKa0s/Skin.lua:611-624`). A test per family: owned, Ignore fonts on -> the template face is
  back; off -> the skin face.
- **Ignore settings panel**: only the Options chrome (LK-06c, LK-06d) is the settings panel; use
  `O.__chromePaint` / `O.__chromeSkin()` exactly as the existing chrome does. For the Widgets
  controls a HOST may place on a settings page, adopt whatever flag LK-05 designs for
  `WidgetsReorder` (the consumers' hand-rolled guards it replaces:
  `../ConsumableMaster/core/SkinSetup.lua:183`, `:530-542`, `../PanelMaster/core/SkinSetup.lua:134-137`,
  `../PrettyChat/core/SkinSetup.lua:135`) on every Widgets constructor that takes an owner
  (Dropdown, SearchBox, TestStrip, Autocomplete, LineChart, DragHandle), so one rule covers them.
  M2's per-addon inventories should say whether any host draws one on its settings page.

---

## 5. Decisions the run must take (for DECISIONS.md)

- **D-1 Ka0s Default's face on the newly fonted strings.** Routing G-W1, G-W2, G-A1, G-L1, G-D1,
  G-DL1, G-P1, G-S2, G-O1, G-O10, G-O11 through `P.font` turns them from the template's Friz
  Quadrata into Oxanium under Ka0s Default (`LibKa0s/SkinDefs.lua:212`), as every AceGUI row and
  primitive-labelled string already is. Without it Ignore fonts has nothing to act on, so R-5 implies
  it. Recommend: accept as R-5's change, record it, and list the strings in the smoke test.
- **D-2 Nil-colored tooltip lines.** `AddLine(text, nil, nil, nil, true)` lines (O.AttachTooltip
  body, Drawer, Nav, Tabs, Keybinds) and `SetText(text)` with no color (SkinPicker, SimPanel) carry
  no literal; their color is the client's default (not verified headless). Recommend: leave them
  alone. Do NOT use `__chromeAway` to mean "away from Ka0s Default" (F-1).
- **D-3 The skin picker under the Scope.** Is the first-run picker the settings panel (Ignore
  settings panel)? Recommend no: it is a standalone dialog. Should Ignore fonts put its rows'
  per-skin preview faces (G-K1) back on the owner's face? Recommend no (the rows exist to preview
  each skin), but this is R-1's sibling question; ask only if the lead is unsure.
- **D-4 Suggestion popup rows (G-O10)**: `menu.text` (follows every skin, Ka0s Default 1.0 -> 0.9)
  vs `text.highlight` (exact, white in all nine). Recommend `menu.text`, for parity with the
  dropdown menu.
- **D-5 LK-08's body and footer** (section 2.2). Recommend `gtip.value` and new `gtip.footer`.
- **D-6 Exact Ka0s Default for the off-palette tooltip grays** (SimPanel's `0.9, 0.82, 0.5`, IdList's
  `0.8`): new T-4 / T-5, or `gtip.title` / `gtip.body` with a recorded change. Recommend the new
  tokens only if the lead holds "Ka0s Default unchanged" strictly for tooltips; otherwise
  `gtip.body` for IdList and `gtip.title` for SimPanel's key column.

---

## 6. Findings outside the strict scope (for the lead)

- **F-1 `__chromeAway` is `__chromeSkin`.** `P.isDefault` answers false always
  (`LibKa0s/SkinPaint.lua:170-173`), so `lib.__chromeAway` (`LibKa0s/OptionsScroll.lua:269-277`)
  never returns nil for a skinned owner. Every caller documented as "away from Ka0s Default only"
  now paints under Ka0s Default: the IdList help mark (`LibKa0s/OptionsIdList.lua:553-563`; its
  comment says Ka0s Default "must draw the mark exactly as minor 5 did", but it now draws
  `text.accent` gold `1, 0.82, 0` instead of `0.82, 0.65, 0.21`, red `sem.bad` `1, 0.33, 0.33` instead
  of `0.90, 0.24, 0.24`, dim `text.disabled` `0.5` instead of `0.35, 0.35, 0.36`), the Keybinds
  labels (`LibKa0s/OptionsKeybinds.lua:657-663`), the Skin tab's muted labels
  (`LibKa0s/OptionsAppearance.lua:252-257`) and the page's opaque backdrop
  (`LibKa0s/OptionsScroll.lua:362-381`). Either the helper and its comments are corrected to say what
  it does, or the IdList help tints gain tokens whose Ka0s Default values are the four constants.
  Not an LK-06 item unless the lead folds it into LK-06c.
- **F-2 SimPanel's dropdowns** (G-S1) are a plain defect (built without the owner the rest of the
  panel uses), independent of R-5's wording.
