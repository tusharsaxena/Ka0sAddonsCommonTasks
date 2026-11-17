# R4: header buttons (#86), Launcher extraEntries (#81), Widgets Bar (#80)

Read-only research against LibKa0s `master` 9bc9cc51 (v1.104.0), WowAddonStandards `master` 3dfb951
(v2.112.2), SkillMaster `main` 19ed391, DropWatcher `master` (read through `git show`). Paths are
relative to `GIT/`.

---

## 0. Summary

| Issue | What it needs | Files / minors that move | Effort | Rides the re-vendor with no adoption? |
|---|---|---|---|---|
| #86 header strip | a new `W.HeaderButtons` factory, a settings-opener registry, and the six library windows migrated to both | new `WidgetsHeader.lua` (minor 1), Core 17→18, Launcher 10→11, DebugLogWindow 4→5, IconBrowserWindow 1→2, SimPanelRender 3→4, PerfPanel 13→14, WidgetsCopyWindow 5→6, OptionsSkinPicker 11→12, (WidgetsDragHandle 13→14 if it gets the mark) | L | **Yes.** The library windows gain the settings mark in every addon on re-vendor, because the Launcher fills the registry. The addons' own windows are the adoption phase. |
| #81 extraEntries | one optional descriptor field and the menu rows it draws | Launcher 10→11 (shared with #86) | S | Yes, as dead code. Only SkillMaster wants it, and it adopts later. |
| #80 Widgets Bar | SkillMaster `modules/Bar.lua` (571 lines) generalized into a new Widgets file | new `WidgetsBar.lua` (minor 1) | M–L | Yes, as dead code. SkillMaster drops its copy in the adoption phase. |

Release: one LibKa0s tag (v1.105.0 proposed). The Widgets version key grows from 7 parts
(`27.1.6.13.7.8.5`) to 9 (with WidgetsHeader and WidgetsBar). So `tests/majors.lua:125-134`,
`LibKa0s.xml:33-39`, `docs/api/Widgets/version-<key>-docs.md` and `members-<key>.json` all change.

---

## 1. #86: standard header buttons on every library window

### 1.1 Inventory: what each library window's title bar carries today

| Window (file:line) | Builder | Right side today, left→right | Left side | How it lays out | Settings mark today |
|---|---|---|---|---|---|
| Debug console, `DebugLogWindow.lua:230-271`, `:446-505` | `buildTitleControls` / `buildTitleBar` | Copy, Clear, Close (`makeIconButton` 18 px slot with 12 px art, `:198-217`; close from `ctx.makeCloseButton`, default `Core.MakeCloseButton`) | `Debug: ON/OFF` toggle plus the Diagnostics link | absolute offsets derived from the close width (`:263-271`), then `S.Header` with `right = {{frame,x}...}`, `left = {toggle}` (`:535-540`) | none. No tooltips, by design: minor 9's label covered the first log line (`:190-197`) |
| Copy window, `WidgetsCopyWindow.lua:189-225`, `:157` | `buildCopyFrame` | Close (`d.makeCloseButton` or Core's) | — | `close:SetPoint("RIGHT", bar, -6)`, then `S.Header(f,{right={f.closeButton}})` | none |
| Perf panel, `PerfPanel.lua:255-300` | inline in the build | Close (Core's, `d.addonName or d.name`). A host `decorate` hook replaces it; no consumer passes one (census below). | — | `TOPRIGHT -6`, then `S.Header` (minor 13) | none |
| Sim step panel, `SimPanelRender.lua:160-182` | `buildChrome` | Close (Core's), unless `d.close == false` | — | `TOPRIGHT -6`. The renderer has no `S.Header` call: its title sits at `CENTER/TOP` by hand. | none |
| Icon browser modal, `IconBrowserWindow.lua:260-300`, `:357-364` | `skinTemplate` (Blizzard template's `ClosePanelButton`) / `plainChrome` (Core's) | Close | — | `S.Header(f,{right={close}})` on both paths | none |
| Skin picker, `OptionsSkinPicker.lua:1213-1240`, `:1183-1188` | `buildChrome` + `buildButtons` | **Close only, in the header.** The gear (`iconButton(f,"settings",...)`, `:1184`) and the eye are on the **dropdown row**, not the title bar (`TOPRIGHT -PAD, -(DD_TOP+...)`), and the dropdown's right edge anchors to them (`anchorDropdown`, `:1176-1181`). | — | `S.Header(f,{title, right={f.close}})` (minor 10) | yes, but on the dropdown row. The gear saves the pending pick, opens `spec.page` on the Appearance tab, then closes the window (`:1017-1030`) |
| Drag handle (HUD strip), `WidgetsDragHandle.lua:581-700` | `dhBuildHelp` / `dhBuildClose` / `dhBuildChrome` | Help (always), then Close (opt-in through `spec.onClose`), at `HELP_HIT 18`, `HELP_INSET 4` | the label | hand-anchored; the host measures and sets the strip's width (`ApplyWidth`, label + PAD + HELP*2) | none |
| Toast, `Toast.lua:324-338` | `decorate` | Close at `TOPRIGHT` | — | `Shell{noTopBar=true}`: **no band** | — (not a window) |
| Callout / WaypointArrow | HUD; Callout uses the DragHandle | — | — | — | — |

Shared geometry already exists. `S.Header` (`SkinPaintExtras.lua:251-268`) chains `spec.right` from
the band's right edge at `pad` 6 and `gap` 4, with `CONTROL_W` 18 (`:154`), and vertically centers
every child. It is **geometry only** and draws nothing. `Core.MakeCloseButton` (`Core.lua:287-325`)
is an 18×18 slot with the catalog's `close` art, tinted `close.rest`/`close.hot` through
`S.CloseButton{own=true}`.

So the library windows already agree on the close mark and on `S.Header` placement (all but the sim
renderer). What differs is everything else: where icon buttons are built (three private factories:
DebugLogWindow `makeIconButton`, OptionsSkinPicker `iconButton`, DragHandle `dhMarkArt`), their art
size (12 px vs `ICON-8`), their tint (palette `icon`/`hot` vs `P.Sk.Button` push-button paint),
whether they have tooltips, and the settings mark, which only the picker has, on its dropdown row.

The two consumer windows the issue points at already roll their own strip:
- SkillMaster `modules/MainWindow.lua:113-135`, left→right: lock, journal, settings, collapse/expand-all, close.
  Built through a private `NS.Chrome.IconButton` (`modules/Chrome.lua:219-234`) with a hand fallback
  chain where there is no skin.
- DropWatcher `modules/WindowTitleBar.lua:367-389`, left→right: badge, lock, layout, minimise, close. **No settings.**
- None of the 19 repos passes `decorate`, `makeCloseButton` or `onSettings` to a library window (git grep
  over every default branch; the only hit is a comment in one `modules/Sim.lua`).

### 1.2 What "settings" opens for each window, and where the opener comes from

No window descriptor has a settings field today. Only `Launcher:New` holds the opener, as
`d.openSettings`, which is **required** (`Launcher.lua:210-212`) and which every addon must pass
(launcher-§1). There is no registry, so a library window cannot reach it.

**Proposed: a settings-opener registry in Core, filled by the Launcher.**
- `Core.RegisterSettingsOpener(owner, fn)` and `Core.OpenSettings(owner, page?) -> boolean` (Core minor 18).
  `Core.HasSettings(owner)` is the presence check.
- `Launcher:New(d)` calls `Core.RegisterSettingsOpener(d.owner or d.name, d.openSettings)` (Launcher minor 11).
  Every rostered addon has a launcher, so **every library window in every addon gets a working
  settings mark from the re-vendor alone**, with no addon edit.
- Each window descriptor gains an optional `onSettings` override, plus `settings = false` with a
  required `settingsOptOut = "<reason>"` (the issue's "opts out only with a reason").
- The opener runs under pcall. A combat refusal is the host's (`O.OpenOptionsPanel` already parks
  in combat, `OptionsRegistry.lua:331-340`), so the button inherits the addon's own combat behavior.

| Window | Settings target (recommended) | Descriptor source | Click side effect |
|---|---|---|---|
| Debug console | the addon's settings panel | `d.addonName` → registry; `d.onSettings` overrides | console stays open |
| Copy window | the addon's settings panel | `d.addonName` | **hide the copy window first.** It is FULLSCREEN strata, so the settings panel would open under it. |
| Perf panel | the addon's settings panel | `d.addonName or d.name` | stays open |
| Sim panel | the addon's settings panel (General, where the Sim mode row sits, options-ui-§15) | `d.addonName` | stays open |
| Icon browser | **opt out**: `settingsOptOut = "opened from a settings row; the panel is already beneath it"` | — | — |
| Skin picker | its existing gear behavior (save the pending pick, `spec.page` + Appearance tab, close), **moved into the header** | `spec.onSettings` / `spec.page`, unchanged | closes, as today |
| Drag handle | opt-in `spec.onSettings` / `settings = true` (see the decision below) | `spec.owner` | — |

### 1.3 Proposed API: `W.HeaderButtons` (new `WidgetsHeader.lua`, Widgets file minor 1)

```lua
local hb = W.HeaderButtons(frame, {
  owner     = "AddonName",      -- skin owner, Media icon folder and registry key (required)
  title     = fs, align = "CENTER", bars = { titleBar }, -- passed through to S.Header
  close     = fn | false,       -- default: frame:Hide(); built by Core.MakeCloseButton(parent, fn, owner)
  makeClose = fn,               -- optional host factory (DebugLog's d.makeCloseButton; BankLedger's decline)
  closeButton = btn,            -- optional: adopt an existing one (IconBrowser's template ClosePanelButton)
  settings  = fn | true | false,-- nil/true: Core.OpenSettings(owner); false needs settingsOptOut
  settingsOptOut = "reason",
  hideOnSettings = bool,        -- modal/transient windows (Copy)
  extras    = { { key = "copy", icon = "copy", glyph = "C", tip = "...", onClick = fn }, ... },
  left      = { ... },          -- left-side controls (the console's toggle), straight to S.Header
  tips      = true,             -- one-line tooltips on every mark (decision Q5)
})
-- hb = { close = btn, settings = btn, extras = { copy = btn, ... },
--        order = { "copy", "clear", "settings", "close" },  -- left→right, read by tests
--        Relayout = fn }
-- frame.headerButtons = hb
W.HeaderButton(parent, owner, icon, glyph, onClick, tip) -> btn  -- the one mark factory, public
W.HEADER = { SIZE = 18, ART = 12, PAD = 6, GAP = 4 }
```

- **One mark factory.** An 18 px slot with 12 px art (the console's measured shape), tinted
  `icon.tint`/`icon.hot` from the owner's skin (the drag handle's tokens), following skin switches
  through `lib.__onSkin`. If the art is missing it falls back to the glyph. It replaces
  DebugLogWindow `makeIconButton` and OptionsSkinPicker `iconButton` (the header use only; the
  picker's reset icons stay the picker's).
- **Placement** goes through `S.Header` (`right = {close, settings, extras...}`, outermost first),
  with the same chain arithmetic by hand where no skin is present. That fallback is SkillMaster's
  `MainWindow.lua:128-140` pattern, and it is needed because Skin is optional.
- **The close stays `Core.MakeCloseButton`, called with three arguments**, so the standalone-windows
  close rules still hold (`standalone-windows.md:30-31`).

### 1.4 Migration per window

- DebugLogWindow: `buildTitleControls` collapses to one `HeaderButtons` call with
  `extras = {copy, clear}` (text-button fallback kept when the art is missing). The
  `f.titleBarOffsets` record is kept, now read from `hb`, because host tests read it (`:478-483`).
  The `adopt` `S.Header` call takes `hb`'s list.
- WidgetsCopyWindow: `close` + `settings` (`hideOnSettings = true`).
- PerfPanel: on the no-`decorate` path. The `decorate` API gains `HeaderButtons` in its helper table.
- SimPanelRender: gains `S.Header`, which closes a small consistency gap, plus settings. `d.close == false` is honored.
- IconBrowserWindow: both chrome paths adopt the existing close and opt out of settings.
- OptionsSkinPicker: the gear moves into the header, and `anchorDropdown` re-anchors to the eye or to
  the frame's right PAD. **The file is 1493/1500 lines**, so this needs a net-zero edit or a peel
  (for example, `buildChrome` and `buildButtons` into `OptionsSkinPickerRows.lua` or a new file).

### 1.5 Standard: current rules and conflicts

- standalone-windows *The Ka0s window edge* (`standalone-windows.md:30-38`, `:49`): the close is
  `MakeCloseButton(parent, onClick, addonName)` through **one addon wrapper**, and BankLedger holds
  the one recorded decline. Conflict for adoption: when an addon window adopts `W.HeaderButtons`,
  the library builds the close, not the wrapper. The bullet needs "…or through `W.HeaderButtons`,
  which takes the owner". The `makeClose` hook keeps BankLedger's decline working.
- standalone-windows *Tooltip placement* (v2.112.0, `:107-150`): title-bar controls are **chrome
  elements**, and their tooltips are attached and centered directly below the top chrome. This
  binds library windows ("these follow the rule in the library's own code"). Two consequences:
  1. If the header marks get tooltips, they must use the chrome placer. That placer is **LibKa0s#92,
     not built yet**. Sequence #92 before #86, or have `WidgetsHeader` carry a minimal chrome placement
     that #92 later absorbs.
  2. The console deliberately has no tooltips (`DebugLogWindow.lua:190-197`), and a chrome-rule tip
     sits right over the log's first line. See decision Q5.
- There is no rule today on header button **order** or on a **settings mark**. Proposed: a new
  standalone-windows bullet, "Title-bar controls (MUST once the addon vendors v1.105.0)":
  close at the corner, settings beside it, extras inward in the host's order, built through
  `W.HeaderButtons`, with an opt-out costing a reason recorded in code and in the ARCHITECTURE
  deviation register. Adoption is owed by each addon's next change, the same shape v2.110.0 used for
  the strip. A new anti-pattern covers a hand-built header strip once the addon vendors v1.105.0
  (sibling of #118). skinning: one line in the §7 tint list (`icon.tint`/`icon.hot` for header marks).
- library-stack Widgets row (`library-stack.md:103`): add `WidgetsHeader.lua` and `WidgetsBar.lua`.

### 1.6 Tests

- `tests/test_header_buttons.lua` (new):
  - order (`hb.order`): close last, settings next to it.
  - opt-out without a reason raises.
  - settings resolves through the registry; an override wins.
  - `hideOnSettings` hides before it opens.
  - a raising opener is caught.
  - a missing-art glyph fallback.
  - the no-skin hand chain matches `S.Header`'s offsets.
  - a skin switch repaints the tints.
- **Acceptance test, one table-driven case per library window:** build the console, copy window,
  perf panel, sim panel, icon browser and skin picker in their existing fixtures (`fixture_*.lua`),
  then assert `frame.headerButtons.order` and the presence of settings and close (the icon browser
  asserts its recorded opt-out instead).
- `test_launcher.lua`: `New` registers the opener, and `Core.OpenSettings(name)` calls it.
- Existing pins that will move: DebugLog `titleBarOffsets`, `test_header_band.lua`, and the picker's
  dropdown anchor tests.

### 1.7 Risks

- **The settings panel opens under the window.** The console is DIALOG and the copy window
  FULLSCREEN; Blizzard's SettingsPanel is HIGH. So modal and transient windows hide on settings, and
  persistent ones may need to stay as they are (smoke check).
- **Combat.** The opener is the host's own, so a combat refusal prints the host's line. That is acceptable.
- **Icon declarations.** Every rostered addon's `LibKa0s icons:` line already names `settings`, or
  `all` (OutfitterReborn, QuickComms). CombatTrail also declares `settings`. So the re-vendor's icon
  prune draws no blank settings mark. `Media.Icon` answers a path without checking the file, so an
  undeclared mark would draw blank (`DebugLogWindow.lua:188-191`). If an extra uses `help`, check each
  repo's declaration first.
- **File caps.** OptionsSkinPicker is at 1493. WidgetsDragHandle is at 1022 (fine).
- **Two consumer windows hand-place their header after `S.Header`.** That is untouched until adoption.

---

## 2. #81: Launcher `extraEntries`

Today: `ENTRIES` is fixed (`Launcher.lua:136-142`). `buildMenu` (`:495-514`) draws the title, the
supplied toggles in ENTRIES order, then Open settings, then Open skin selector. launcher-§2 fixes the
order and forbids any host menu (`launcher.md`, §2, "There is no setting that reassigns… MUST NOT
build its own menu"). SkillMaster records the gap in `docs/known-limitations.md:31-34`. Its journal
has `NS.Journal.IsShown`/`Toggle` (`modules/Journal.lua:1150`, `:1171`), so a Journal entry is a
natural checkbox, the same shape as Show window.

**Proposed descriptor field (Launcher minor 11):**
```lua
extraEntries = {
  { label = L["Journal"],           -- REQUIRED, plain string (the host's locale)
    checked = function() return NS.Journal.IsShown() end,  -- optional: checkbox when present, plain button when nil
    onClick = function() NS.Journal.Toggle() end,          -- REQUIRED
    gated   = true,                 -- optional, default true: grayed with "enable the addon first" while disabled
    clients = { "forever" } },      -- optional, what Compat.ForClient takes (replaces entryClients for extras)
}
```
- **Position:** after the last supplied toggle (Show window) and before Open settings, in declared
  order. This keeps the minor 7 row rule: a checkbox when it is a toggle, a button when it is an action,
  and the same graying either way.
- **`checkDescriptor`** checks the field once, at `New`, and raises at the host's line: the field is a
  table, each entry has a non-empty `label` and a function `onClick`, `checked` is nil or a function,
  `clients` is valid, and the count is ≤ cap.
- **Clicks** go through the same `choose`-style pcall. A raise emits `MENU_FAILED` with the entry's label.
- **Tooltip** unchanged (launcher-§1's status lines are not extended).

**Standard ripple.**
- launcher-§2: amend the fixed order block with `<extra entries>  only where the addon declares them`
  between Show window and Open settings. Bound it: each extra is a secondary window or action the
  addon already exposes through a slash verb, never a duplicate of a built-in entry, never a settings
  shortcut, and its click is the verb's own handler (anti-pattern #81 wording).
- ADDONS.md launcher column: list the extras (SkillMaster: `… · Show window (the skills window) · Journal`).
- Bump the standard's minor.

**Tests (`test_launcher.lua`, `mock_menu.lua`):**
- extras render after Show window and before Open settings.
- `checked` gives a checkbox with a live tick; nil gives a button.
- gated extras gray while disabled and call nothing.
- `gated = false` stays clickable.
- `clients` filters.
- each malformed entry raises at `New` with a named message.
- a raising `onClick` emits `MENU_FAILED`.
- an existing host's menu is unchanged, byte for byte (regression).

**Risks:** low. The cap and the "no duplicates" rule are owner taste (Q8). Today, `docs/api/Launcher/version-11-docs.md` is the only doc ripple.

---

## 3. #80: promote SkillMaster `NS.Bar` to `LibKa0s-Widgets`

### 3.1 What `modules/Bar.lua` is (SkillMaster `main`, 571 lines, fully read)

**Public surface.**
- `Create(parent, styleKey)`
- `bar:SetValues{value,max,bonus,bonusKind,tiers,markers,text,color}`
- `bar:SetTimer(expires)`, `bar:ApplyStyle(style)`
- `NewPool`/`Acquire`/`ReleaseAll`
- pure helpers: `Compute`, `Text`, `FormatTimer`, `TierShade`
- styling helpers: `Color`, `WithClass`, `PlayerColor`, `Swatch`, `ResolveStyle`, `ShowMarkers`, `TooltipRowHeight`
- `Media`, `MakeEdges`, `PaintEdges`, `PaintBorder`
- methods: `Layout`, `LayoutSegments`, `LayoutMarks`, `PaintMarks`, `RedrawTimer`

**Behavior.**
- A base fill clamped to [0,1], and a bonus segment that reaches at most the end (`:221-236`).
- Rank-tier segments on a scale to the last tier, each a darker shade (`TIER_SHADE {1,.8,.64,.5}`, `:114-118`, `:179-187`).
- Markers up to and including the cap (`:189-196`). **The labels are carried, not drawn.** RowTooltip
  draws them as lines (`modules/RowTooltip.lua:191`). The issue's "labeled markers" and "tier ticks"
  are really fractions plus segments; nothing draws tick lines.
- A spark, a reverse fill (`fillDirection == "RIGHT"`), and a text template `{rank} {bonus} / {max}`
  with `{pct}` and `{left}`, collapsing the double spaces an empty token leaves (`:198-215`).
- An expiry timer at 0.2 s, with its OnUpdate armed only while it runs (`:444-476`). This is performance-compliant.
- A secret-width fallback for a tooltip-anchored bar on tainted WoW Forever (`:344-352`). Generic and worth keeping.

**Dependencies on SkillMaster internals.**
| Dependency | Where | Generalization |
|---|---|---|
| `NS.Skin` (owner facade: `Token`, `IsEnabled`, `BarTexture`, `BarBorder`, `HudFont`, `HudFontSize`, `FontFlags`, `FROM_SKIN`) | `:37`, `:91-95`, `:261-262`, `:492-498` | `spec.owner` → `lib.__skinOf(owner)` / `Skin:For(owner)` (Widgets already does this, `Widgets.lua:215-282`). With no owner it uses the library's Ka0s Default values. |
| `NS.SKIN_OWNER_TOKENS` defaults (`sm.barFill`, `sm.barBg`, `sm.bonusTemp`, `sm.bonusPerm`, `sm.barBorder`, `sm.marker`, `sm.spark`, `sm.barText`, `sm.timer`; SkillMaster `core/SkinSetup.lua:42-62`) | `:39` | Library defaults on existing tokens: `bar.fill`, `bar.bg`, `bar.border`, `hud.label` (marker), `hud.text` (spark, text), `sem.info` (timer). A Card-style `tokens` remap (`SkinPaintExtras.lua` `S.Card` opts.tokens) lets a host point a slot at its owner token by name. |
| `NS.db.profile.bars` / `NS.defaults` | `:43-45`, and everything in `ResolveStyle`, `Swatch`, `PlayerColor`, `ShowMarkers`, `TooltipRowHeight` | **Stays in SkillMaster.** The library takes a resolved style table and never reads a profile. |
| `LibKa0s-Core-1.0.ClassColor` | `:47-56` | Stays in the host (`WithClass` is options-ui-§17 swatch logic). |
| LibSharedMedia fetch | `:74-80` | The library has its own media seam. Style takes `texture` (a path or LSM key) and `borderStyle` (an LSM key). |
| `NS.Pool` (LibKa0s-Pool-1.0 or a degrade stub; SkillMaster `core/PoolSetup.lua`) | `:554-571` | Call-time `LibStub("LibKa0s-Pool-1.0", true)`, with no floor on the major (the Widgets shell keeps its no-dependency stance). |
| `HEIGHT_KEY`, `ROW_KEY` style presets tied to profile keys | `:120-128` | The library ships `W.BAR.PRESETS` (`row`, `compact`, `tooltip`, `mini`: height, showText, showMarkers); the host fills the sizes. |

**Other uses of `NS.Bar` in SkillMaster.** `MakeEdges`/`PaintBorder`/`Color`/`WithClass` are also used
for **non-bar frames**: `modules/Detached.lua:234-316`, `GroupsSnap.lua:150-219`, `Rows.lua:126-250`,
and the headers in `Blocks`, `Groups` and `Journal`. Removing `Bar.lua` therefore needs a small host
module (for example, `NS.Edge`/`NS.Colors`) for those helpers. That is adoption-phase work, not library work.

**Tests:** SkillMaster `tests/test_bar.lua`, 157 lines, 11 cases (clamp, temp/perm color, empty cap,
tiers, markers, timer format, timer arm/disarm, timer run-out, resolved style, pool order, secret
width). **Complexity:** max CCN 15 in `PaintBorder` (at the ceiling), `ResolveStyle` 12,
`SetValues`/`Layout` under 10 (`docs/automated-tests/20261110-063942/complexity.txt`).

### 3.2 Proposed Widgets API (`WidgetsBar.lua`, Widgets file minor 1)

```lua
local bar = W.Bar(parent, { owner = "SkillMaster", style = W.BarStyle(owner, "row", overrides) })
bar:SetValues{ value, max, bonus, bonusKind = "temp"|"perm",
               segments = { caps... } | nil,        -- was `tiers`; drawn only while style.segmented
               markers  = { { at, label } },        -- label carried into bar.geom, never drawn (Q11)
               text, color }
bar:SetTimer(expires | nil)
bar:ApplyStyle(style)      -- a full style REPLACES (has .key); a partial merges (current contract)
bar:Park()                 -- the release hook: timer off, points cleared
bar.geom                   -- the last Compute, public, read by tests and tooltips
W.BarStyle(owner, presetKey, overrides) -> style
  -- colors are TOKEN NAMES (strings) or literals ({r,g,b,a}); names resolve at paint time
  -- against the owner, so a skin switch repaints with no host call (lib.__onSkin);
  -- defaults: fill "bar.fill", bg "bar.bg", border "bar.border", marker "hud.label",
  -- spark "hud.text", text "hud.text", timer "sem.info", bonusTemp/bonusPerm (Q10)
W.BarCompute(values, template, segmented) -> geom     -- pure
W.BarText(value, bonus, max, template)                 -- {value} ({rank} alias), {bonus}, {max}, {pct}, {left}
W.BarFormatTimer(seconds)                              -- m:ss / h:mm:ss
W.BarShade(color, i)                                   -- W.BAR.SHADE = { 1, .8, .64, .5 }
W.AcquireBar(pool, parent, opts) / W.ReleaseBars(pool) -- thin, over LibKa0s-Pool-1.0 at call time
W.BAR = { TIMER_TICK = 0.2, TIMER_W = 38, TEMPLATE = "{value} {bonus} / {max}", SHADE, PRESETS }
```

**What changes from the host copy, and why.**
- Token names in style tables, so skin switches follow automatically. SkillMaster today re-resolves
  on its bus `LAYOUT_CHANGED` and re-`ApplyStyle`s on every acquire.
- Edges move to Core's pixel-exact edges (`lib.__pixelEdged`, `Widgets.lua:167`) in place of 1 px at
  UI scale. This is a small visual improvement and a smoke check.
- The border uses `S.BarBorder` exactly as the host does (skinning-§6 semantics kept). The host
  passes `{show, style, size, fromSkin}`.
- `tiers` is renamed `segments`, and `{rank}` becomes `{value}` (with an alias), because the profession
  words are SkillMaster's.
- No profile reads and no class color.

**Estimated size:** 480–560 lines, a new file well under the cap. CCN: split `PaintBorder` (at 15) as it moves.

### 3.3 Tests (LibKa0s `tests/test_widgets_bar.lua` + `fixture_widgets.lua`)

- Port the 11 SkillMaster cases (renamed fields).
- New cases:
  - an owner-less bar draws Ka0s Default.
  - token-name colors repaint on a skin switch (`skin_switch` kit).
  - a literal color does not move on a switch.
  - the `tokens` remap reaches an owner token.
  - reverse fill mirrors the geometry.
  - `{rank}` alias.
  - Park disarms the OnUpdate.
  - an acquire with no Pool major degrades.
  - both clients (`KA0S_KIT_CLIENT=forever`), for the secret-width path.
- Versioning: `tests/majors.lua` gains `WidgetsBar` and `WidgetsHeader` (`minorField`/`probeField`
  pairs), plus `members-<key>.json` regen and the Widgets doc.

### 3.4 Risks

- No consumer adopts in this run. SkillMaster keeps its copy until the adoption phase, so this ships as dead code.
- The adoption needs SkillMaster's non-bar helpers re-homed first.
- A skin-token default for the bonus colors does not exist (Q10).
- SkillMaster vendors v1.101.0. The re-vendor jumps it four tags, which is the general re-vendor plan's concern.

---

## 4. LibStub minors that move (all three issues)

| File / major | Now | After | Issue |
|---|---|---|---|
| `Core.lua` LibKa0s-Core-1.0 | 17 | 18 | #86 (settings registry) |
| `Launcher.lua` LibKa0s-Launcher-1.0 | 10 | 11 | #81 + #86 (registers the opener) |
| `WidgetsHeader.lua` (new, Widgets) | — | 1 | #86 |
| `WidgetsBar.lua` (new, Widgets) | — | 1 | #80 |
| `Widgets.lua` shell | 27 | 27 or 28 (28 only if the shell exposes a helper the new files need) | #80/#86 |
| `DebugLogWindow.lua` | 4 | 5 | #86 |
| `WidgetsCopyWindow.lua` | 5 | 6 | #86 |
| `PerfPanel.lua` | 13 | 14 | #86 |
| `SimPanelRender.lua` | 3 | 4 | #86 |
| `IconBrowserWindow.lua` | 1 | 2 | #86 |
| `OptionsSkinPicker.lua` | 11 | 12 (plus a peel file if needed) | #86 |
| `WidgetsDragHandle.lua` | 13 | 14 (only if Q4 says the strip gets the mark) | #86 |

**Doc ripple:**
- New `docs/api/<Major>/version-<key>-docs.md` and `members-<key>.json` for Core, Launcher, Widgets,
  DebugLog, Perf, Sim, IconBrowser and Options.
- `docs/api/CONSUMERS.md` rows for `W.HeaderButtons`, `W.HeaderButton`, `W.Bar*`,
  `Core.OpenSettings`/`RegisterSettingsOpener`/`HasSettings` ("no host calls them yet").
- CHANGELOG.
- The CLAUDE.md file-size band census, if the picker peels.

---

## 5. Decisions for the owner (each with my recommended answer)

1. **Header order.** **Recommend: left→right `[extras in host order] [settings] [close]`**, with close
   in the corner and settings always next to it, so the two universal marks sit at the same screen
   spot on every window. The alternative is the issue's literal reading, settings leftmost then extras
   then close, which moves settings with every extra. (SkillMaster today: lock, journal, settings,
   toggle, close. DropWatcher has no settings.)
2. **Where "settings" comes from.** **Recommend: a Core registry filled automatically by `Launcher:New`**,
   so every library window works on re-vendor with zero addon edits, and each descriptor keeps an
   `onSettings` override. The alternative is a new required field on every window descriptor, which
   needs adoption in 19 repos before any settings mark appears.
3. **Opt-outs.** **Recommend: the icon browser opts out** (it is opened from a settings row). **The copy
   window keeps settings and hides itself first.** All the others carry it.
4. **Drag handle (HUD strip).** **Recommend: opt-in for this run** (`spec.settings = true`). A default-on
   third mark widens every HUD strip on re-vendor and would fight AuraMaster's capped strips and the
   host-measured `ApplyWidth`. The adoption phase turns it on per addon.
5. **Header tooltips.** **Recommend: yes, a one-line tooltip on every header mark, placed by the chrome
   rule (standalone-windows v2.112.0)**, on the console too, reversing DebugLogWindow minor 10's
   no-tooltip choice, because a bare gear is not discoverable. Sequence it after or with #92's placer.
   The alternative is no tooltips on the console only.
6. **Home of the code.** **Recommend: `W.HeaderButtons` in a new `WidgetsHeader.lua` (Widgets) and the
   opener registry in Core.** DebugLog, Sim and IconBrowser already resolve Widgets at call time. The
   alternative is everything in Core (949 lines today), which needs no cross-major call.
7. **Standard rule now or at adoption.** **Recommend: write the standalone-windows rule in this run**:
   header order plus settings MUST once an addon vendors v1.105.0, owed by each addon's next change,
   amending the one-wrapper close bullet to admit `W.HeaderButtons`. Adoption stays deferred, as the
   owner asked.
8. **`extraEntries` limits.** **Recommend: at most 2 extras, placed between Show window and Open
   settings, `gated` true by default, a per-entry `clients`, and a plain-string label only.** Each extra
   must be a secondary window or action with its own slash verb.
9. **ADDONS.md.** **Recommend: the launcher column lists extras** (SkillMaster gains "· Journal" at adoption).
10. **Bar bonus colors with no owner token.** **Recommend: no new skin tokens.** Default `bonusTemp` to
    `sem.info` and `bonusPerm` to `sem.good`, and let SkillMaster remap to its `sm.bonus*` owner tokens.
    The alternative is new `bar.bonus`/`bar.bonusAlt` library tokens in every skin def, which means a
    Skin minor and kit skin-value churn.
11. **Bar marker labels.** **Recommend: carried in `geom`, not drawn** (today's behavior; RowTooltip
    draws them). The alternative is an opt-in drawn label.
12. **Bar pool helpers.** **Recommend: ship the thin `W.AcquireBar`/`W.ReleaseBars`** so SkillMaster's
    swap is mechanical. The alternative is hosts calling LibKa0s-Pool-1.0 directly with `bar:Park`.
13. **CombatTrail** (a repo, not in ADDONS.md) is in the re-vendor scope as "all Ka0s addons"? **Recommend:
    yes for the re-vendor.** It vendors LibKa0s and declares `settings`. That is the planner's call for the whole run.
