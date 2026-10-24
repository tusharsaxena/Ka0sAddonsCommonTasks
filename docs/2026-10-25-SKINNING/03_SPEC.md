# Spec: Ka0s skins, leg 1 (engine + LootHistory prototype)

Binding inputs: [`inputs/OWNER_SCOPE.md`](inputs/OWNER_SCOPE.md) (the owner's rulings R1-R8). Evidence:
[`inputs/LIBKA0S_INTERNALS.md`](inputs/LIBKA0S_INTERNALS.md), [`inputs/LOOTHISTORY_SURFACES.md`](inputs/LOOTHISTORY_SURFACES.md),
[`inputs/ACEGUI_AND_ENGINE_RESEARCH.md`](inputs/ACEGUI_AND_ENGINE_RESEARCH.md). Token source:
[`inputs/mockup-tokens.dc.html`](inputs/mockup-tokens.dc.html) (its `BASE` and `SKINS` tables). Where an item spec in
`plan-data/items.json` is more precise than this page, the item binds.

## 1. Intent

Every visual element of a Ka0s addon is drawn from a **skin**, chosen **per addon** in a new **Appearance** settings
tab. Nine skins ship with LibKa0s; **Ka0s Default** is today's look, pixel for pixel. Alternatively the addon can take
its look from **EllesmereUI** when EllesmereUI (with its Blizzard Skin module) is loaded, its third-party skinning is
on and the addon's entry in its Third-Party Addons list is on. Leg 1 builds the engine in LibKa0s and converts
**LootHistory** end to end, then stops for the owner's in-game smoke test. Leg 2 (a later bundle) rolls out to the
other 14 addons, migrates PGFE's bridge onto the library and applies the HUD reset (R3).

### Goals

- G1. A skin is **data**: a token table. Adding a skin is adding a table.
- G2. One painting vocabulary, **EllesmereUI-compatible names** (`Shell`, `Panel`, `Inset`, `FadeRegions`,
  `FadeNineSlice`, `Button`, `WhiteButtonLabel`, `StateButtonLabel`, `EditBox`, `Checkbox`, `Dropdown`, `ScrollBar`,
  `Tab`, `SetTabSelection`, `CloseButton`, `PageButton`, `SquareIcon`, `SortHeaderBar`, `Font`, `White`, `ApplyBarFill`,
  `GetAccentColor`, `GetPanelColor`, `GetFont`, `OnLooksChanged`, `IsEnabled`, `GetStyle`, `apiVersion`) plus Ka0s
  extras. Addon code calls the vocabulary once at frame creation; the provider (Ka0s or EllesmereUI) does the painting.
- G3. Ka0s skins switch **live** (no reload). EllesmereUI → Ka0s needs a reload (EllesmereUI's paint is one-way).
- G4. **Per addon** (R1): two addons sharing one loaded LibKa0s copy can show different skins at once.
- G5. **Everything** (R2): windows, panels, dialogs, list rows, tooltips owned by the addon, the settings pages
  (library chrome *and* the AceGUI rows), the debug console, perf/sim panels, copy windows, test strips, dropdown menus
  and charts.
- G6. Ka0s Default reproduces today's look exactly: every existing golden and color pin stays green with no rewrite.

### Non-goals (leg 1)

- Converting any addon but LootHistory. Re-vendoring v1.78.0 into any consumer but LootHistory.
- Restyling Blizzard's shared frames: `SettingsPanel` chrome, `StaticPopup*`, `GameTooltip` itself,
  `ColorPickerFrame`, the AceGUI-3.0-SharedMediaWidgets pull-out lists. (Tooltips the addon *fills* keep Blizzard's
  frame; item 7 below covers the one exception the library owns.)
- Changing meaning-carrying colors in Ka0s Default: item quality, class colors, gain/loss, Bind-on-Pickup. Other skins
  may override the *legibility* of these (Azeroth and High Contrast need darker/brighter quality colors, as the mockup
  shows) through semantic tokens; the hue meaning never changes.
- Running on the WoW Forever client (LibKa0s#44).

### Anti-goals (a failure even if it works)

- A skin applied by one addon leaking into another addon's frames, including through AceGUI's shared widget pool.
- Any taint: no `Hide`/`SetParent`/`SetScript` on Blizzard frames, no `SetBackdrop` on Blizzard templates, nothing
  written onto a Blizzard frame's table; per-frame state lives in a weak-keyed table on the library.
- Copying EllesmereUI code or media (its license reserves all rights). Mirror names and the token model only.

## 2. The skin format

A skin is `{ key, label, desc, swatches = {4 hex}, tokens = {...} }` registered with `Skin:RegisterSkin(def)`. Keys
and labels: `ka0s` Ka0s Default, `obsidian` Obsidian, `azeroth` Azeroth, `glass` Glass, `contrast` High Contrast,
`ember` Ember, `wow` WoW Default, `midnight` WoW Midnight, `forever` WoW Forever. Default `ka0s`.

Tokens are flat. Colors are `{r, g, b, a}` (0-1). Every skin is complete: `tests` assert each skin defines every
token in the schema (a skin derives from `ka0s` and overrides; the resolved table is complete). The schema groups:

- **Fonts**: `font.body`, `font.title`, `font.mono` (LSM keys or paths), `font.bodySize`, `font.titleSize`,
  `font.outline`, `font.shadow`.
- **Window**: `win.bg`, `win.bgTexture` (optional tiled texture), `win.border`, `win.borderSize`, `win.borderStyle`
  (`flat` | `nine:<lsm-border-key>`), `win.inner` (inner rule, may be nil), `win.radius` (0 or a rounded nine-slice key),
  `title.bg`, `title.text`, `title.align` (`LEFT`|`CENTER`), `title.height`, `divider`, `foot.bg`, `close.rest`,
  `close.hot`.
- **Text roles**: `text.body`, `text.muted`, `text.heading`, `text.accent`, `text.disabled`, `text.link`.
- **Controls**: `btn.bg` (+ `btn.bgTop`/`btn.bgBottom` for a vertical gradient), `btn.border`, `btn.text`,
  `btn.hover`, `btn.radius`; `btnPrimary.*` same fields; `input.bg`, `input.border`, `input.text`, `input.placeholder`,
  `input.focus`; `check.bg`, `check.border`, `check.mark`; `slider.track`, `slider.trackBorder`, `slider.fill`,
  `slider.thumb`; `scroll.track`, `scroll.thumb`, `scroll.width`; `tab.bg`, `tab.text`, `tab.border`, `tab.onBg`,
  `tab.onText`, `tab.onLine`; `nav.bg`, `nav.border`, `nav.text`, `nav.selBg`, `nav.selText`, `nav.selBar`;
  `drawer.bg`, `drawer.border`, `drawer.text`; `menu.bg`, `menu.border`, `menu.hover`.
- **Lists**: `list.header.bg`, `list.header.text`, `list.stripe`, `list.hover`, `list.sel`, `list.selOutline`.
- **Overlays**: `popup.bg`, `popup.border`, `tooltip.bg`, `tooltip.border` (library-owned tooltips only), `strip.*`
  (test/sim strip), `cover.dim` (combat cover).
- **HUD**: `bar.texture` (LSM statusbar key), `bar.gloss` (bool), `bar.bg`, `bar.border`, `bar.borderStyle`,
  `icon.border`, `glow.color`, `hud.font`, `hud.fontSize`, `hud.outline`.
- **Charts**: `chart.axis`, `chart.grid`, `chart.crosshair`, `chart.series` (ordered list of colors).
- **Semantic** (legibility overrides only): `q.poor` .. `q.legendary`, `sem.good`, `sem.bad`, `sem.warn`,
  `sem.info`. Ka0s Default sets these to today's exact values and other skins inherit them unless they need contrast.

The mockup's CSS tokens map onto this schema (`win` → `win.bg`, `btnBg` → `btn.bg`, ...). Visual effects WoW cannot
draw are approximated and documented in the skin's comment: no blur (Glass = translucency + rounded corners), CSS
`ridge`/`outset` bevels become Blizzard border textures (`Interface\\DialogFrame\\UI-DialogBox-Border` family for WoW
Default) or two-tone 1px edges, gradients use `SetGradient` on a white texture.

**Ka0s Default's tokens are today's constants**, collected from the tables in `inputs/LIBKA0S_INTERNALS.md` §2 and
`inputs/LOOTHISTORY_SURFACES.md` §3 (e.g. `win.bg` = `{.06,.06,.08,.92}`, `win.border` = `{0,0,0,1}`, `win.inner` =
`{.24,.24,.27,.85}`, `title.text` = `{1,.82,0}`, `nav.selBg` from `SELECT_RGB {.3,.5,1}`). Where two call sites draw the
same role in different colors today, Ka0s Default keeps both with two tokens rather than change a pixel; the list of such
splits is recorded in the LibKa0s API doc as candidates for leg 2.

**Fonts shipped (R7)**, OFL 1.1, static instances, each with its license file, under the payload's `media/fonts/`:
Barlow Regular + SemiBold, Cinzel SemiBold, Atkinson Hyperlegible Regular + Bold. Registered with LibSharedMedia as
`Ka0s Barlow`, `Ka0s Barlow SemiBold`, `Ka0s Cinzel`, `Ka0s Atkinson`, `Ka0s Atkinson Bold`, Western-locale mask only
(Cinzel and Atkinson lack Cyrillic; on another locale the skin falls back to the client font). Per-skin fonts: Ka0s
Default and WoW Default use today's client fonts; Obsidian, Glass, WoW Forever: Barlow; Azeroth, Ember, WoW Midnight:
Cinzel titles over the client body font; High Contrast: Atkinson at +2pt. Paths resolve from the folder of the
LibKa0s copy that won at load (never a hard-coded addon name).

**Textures shipped**: white rounded-corner nine-slice TGAs for Glass (radius 8) and a 1px two-tone bevel set for WoW
Default buttons/inputs if Blizzard art does not serve; everything else uses `WHITE8x8` or in-client Blizzard
textures/atlases (listed in `inputs/ACEGUI_AND_ENGINE_RESEARCH.md` §5). New LSM catalogs `border` and `background`
register the shipped and in-client keys.

## 3. The engine: `LibKa0s-Skin-1.0`

A new major (file `LibKa0s/Skin.lua` primary, secondaries as the 1500-line cap and CCN 15 require, e.g.
`SkinDefs.lua` for the nine token tables, `SkinPaint.lua` for the Ka0s primitives, `SkinAce.lua` for AceGUI rows,
`SkinEUI.lua` for the EllesmereUI provider), floored on Core, paired on the shell's minor like the Widgets
secondaries.

- **Owners.** `Skin:RegisterOwner(owner, opts)` at the consumer's file load, `owner` = the addon folder name.
  `opts.get()` returns `{source, skin}` from the addon's profile; `opts.set(source, skin)` writes it (used by
  copy-to-all); `opts.label`. State is a registry keyed by owner on the library (`lib.owners = lib.owners or {}`), so it
  survives a minor upgrade. A frame painted for an owner is recorded in a weak-keyed table `lib.painted[frame] =
  {owner, prim, opts, regions}`; `lib.byOwner[owner]` is a weak set of its frames.
- **Facade.** `Skin:For(owner)` returns `S`, the owner's facade, with the vocabulary of G2 plus Ka0s extras:
  `TitleBar`, `Divider`, `Footer`, `Card`, `Slider`, `NavItem`, `Drawer`, `ListRow` (stripe/hover/selection),
  `MenuFrame`, `Tooltip` (library-owned frames only), `Strip`, `Cover`, `Text(role)`, `Token(name)`,
  `Color(name)`, `ChartStyle()`, and HUD helpers (`BarStyle`, `IconBorder`, `GlowColor`). Signatures match
  EllesmereUI's where the name exists (`S.Shell(frame, opts)`, `S.Checkbox(cb, opts)` ...). Every primitive is
  idempotent and records what it created so a repaint reuses it.
- **Providers.** `source = "ka0s"`: primitives paint from the owner's resolved skin. `source = "eui"`: when the gate
  (§5) holds, EllesmereUI's facade paints the vocabulary names it has and the Ka0s extras paint from EllesmereUI's
  getters (`GetAccentColor`, `GetPanelColor`, `GetFont`); when the gate fails, the owner falls back to its Ka0s skin
  and the Appearance tab says which condition failed.
- **Live repaint.** `Skin:SetChoice(owner, source, skin)` resolves the new skin, then repaints every frame in
  `lib.byOwner[owner]` (each record re-runs its primitive in repaint mode) and fires `OnLooksChanged` listeners for
  that owner only. Cost: one pass over the owner's recorded frames; no OnUpdate, no events. Switching away from `eui`
  sets a pending-reload flag and asks for a reload (popup) instead of repainting.
- **Unowned callers.** Library factories that have no owner today (`Core.ApplySkin`, `MakeCloseButton`, `W.Dropdown`,
  the shared dropdown popup menu, `W.SearchBox`, `W.CopyWindow`, `W.TestStrip`, `W.Autocomplete`, `W.DragHandle`,
  `W.ReorderList`, `W.LineChart`, SimPanel/PerfPanel buttons) take an optional `owner` (descriptor field or trailing
  argument, additive). Without one they paint Ka0s Default exactly as today. The shared popup menu repaints to its
  opener's owner each time it opens. `lib.SKIN` stays exported unchanged for backward compatibility.
- **AceGUI rows.** `OptionsWidgets` paints each widget it acquires for owner X through `SkinAce`: stock regions are
  faded by alpha (their prior alpha, font, colors and backdrop recorded in the weak table), Ka0s overlay textures are
  created once per widget object and reused, and the widget's per-instance `OnRelease` is wrapped (chained, as
  `OptionsScroll.lua` does) to restore every recorded value and hide the overlays before the widget returns to the
  shared pool. The Dropdown's pull-out is painted on open for its owner and restored on close. Never touch widgets the
  library did not acquire; step aside (paint nothing) if another skinning addon (ElvUI, AddOnSkins) has already skinned
  the widget. LSM30 pull-outs and `ColorPickerFrame` stay stock (non-goal).
- **Settings chrome.** Options header, tab strip, secondary strip, nav rail, drawers, the combat cover, the id inputs
  and suggestion lists, the keybind rows and the always-visible scrollbar take the page's owner from the Options
  instance (`d.addonName`; required for skinning, absent = Ka0s Default).
- **HUD sentinel (R3).** `Skin.FROM_SKIN = "@skin"`. `S.Resolve(kind, value)` returns the skin's value when `value`
  is the sentinel, else `value`. `Skin.ResetToSkin(profileTable, keyList)` sets each listed key to the sentinel (and a
  color's companion `fromSkin` bool to true). OptionsCompose's font/statusbar/border pickers gain a "From skin" entry
  that previews the skin's resolved value. Leg 1 ships and tests the helpers; LootHistory has no HUD, so their first
  adopters are leg 2's.

## 4. Settings: the Appearance tab

`O.AppearanceTab(opts)` (a new Options secondary, so no band file grows past its trigger) renders, on the owner's
General page after Interface and before Keybindings:

1. **Skin source**: Ka0s skins | EllesmereUI. The EllesmereUI choice is disabled with a hint when the gate fails; its
   three conditions are listed with a check or a cross and a one-line fix each.
2. **Skin**: a choice grid of the nine skins, each with its four swatches, label and one-line description (as the
   mockup's picker). Selecting one repaints live.
3. **Copy to every Ka0s addon**: a button that writes this addon's `{source, skin}` into every other registered owner
   through its `opts.set` and repaints them; a confirmation names the addons it will change.
4. A note: "Skins change every visual element. HUD style options follow the skin unless you set them yourself."

Two controls minimum per tab (LootHistory's `tests/test_schema.lua:719`) is satisfied. Profile keys:
`appearance.source` (`"ka0s"`), `appearance.skin` (`"ka0s"`), default-merged by AceDB; no migration in leg 1. A
profile switch, copy or reset re-applies through `SetChoice`.

## 5. The EllesmereUI provider

Moved from PGFE's `core/EUIBridge.lua` / `modules/EUISkin.lua` into `SkinEUI.lua`, keyed by owner:

- `EllesmereUI.RegisterSkin(owner, cb)` at `RegisterOwner` time (the consumer's file load), presence-guarded. `cb`
  keeps the facade; it paints only while that owner's source is `eui`. A facade missing a needed primitive is refused
  before painting (fail closed, latched, logged once).
- Gate: `EllesmereUI.RegisterSkin` is a function and `C_AddOns.IsAddOnLoaded("EllesmereUIBlizzardSkin")`;
  `EllesmereUIDB.thirdPartySkinsOff` not truthy; `EllesmereUIDB.thirdPartySkinAddons[owner]` not `false`. All reads at
  call time, nil-guarded, never written. This read of another suite's SavedVariables is a **documented deviation** in
  LibKa0s's register (`library-stack-§6`), citing PGFE's 2026-10-09 ratification and R-brief "use the EllesmereUI skin
  if EUI is installed and loaded and third-party skins is enabled"; the WowAddonStandards `skinning` section (§7)
  carves it out by name.
- Ka0s → EllesmereUI applies live (overlays hidden, EllesmereUI primitives run); EllesmereUI → Ka0s offers a reload.
- PGFE's own bridge stays as is in leg 1 (its fourth condition, Premade Groups Filter's own skin, is PGFE's).

## 6. LootHistory (the prototype)

Per `inputs/LOOTHISTORY_SURFACES.md`:

- Re-vendor LibKa0s v1.78.0 (local tag). Register the owner `"LootHistory"` at file load in a new seam file (Browser
  and BrowserTable are at 1327 / 1320 lines), with a TOC row, a `docs/module-map.md` row and a degraded arm pinned by
  `test_surface_parity`.
- Convert every surface: History window (shell, title bar, close, tabs, filter bar, search, dropdowns, the three flat
  button copies merged onto `S.Button`, table header with sort arrows, rows with stripe/hover/selection, row menu,
  scrollbars, footer), Export window (including its never-tinted `titleFS`), Insights cards and charts (series palette
  from `chart.series`), Timeline (line chart owner), Holdings, the sim panel and test strip, and library-owned
  tooltips. Constants move to tokens; semantic colors to `q.*`/`sem.*` tokens whose Ka0s Default values are today's.
- Live repaint on `SETTINGS_CHANGED "skin"` through `B:OnSettingsChanged` and the tab registry, and on
  `B:AdoptProfile`. Pooled rows tint in the bind step (or both pool lists are walked). Markup built once at load (sort
  arrows, AH price ticks, quality labels) is rebuilt on a skin change.
- `settings.alpha` stays whole-window opacity, independent of a skin's background alpha.
- Goldens (`tests/analytics_golden.txt`, `tests/panel_auction_golden.txt`) and every color pin stay green unchanged
  under Ka0s Default. New suites pin: each surface paints from tokens; a skin switch repaints without a reload; another
  owner's skin never reaches LootHistory frames.
- Docs: ARCHITECTURE, module-map, schema, settings-panel, smoke-tests (one row per skin plus EllesmereUI), test-cases.

## 7. The standard

WowAddonStandards gets a new section `skinning` (next minor version after v2.88.0): every visual element of an addon
paints through the LibKa0s Skin facade with the addon as owner; the Appearance tab on General; per-addon choice; the
EllesmereUI provider and its named read of `EllesmereUIDB`; hard-coded chrome colors become an anti-pattern **for an
addon that has adopted skins** (commencement: leg 2's rollout, so the 14 unconverted addons are not instantly
non-compliant); the library-stack module table and major count gain `LibKa0s-Skin-1.0`; the options-ui General tab
order gains Appearance.

## 8. Versions and branches

WowAddonStandards v2.88.0 → v2.89.0. LibKa0s v1.77.0 → **v1.78.0** (local annotated tag; pushed only on the owner's
merge go-ahead). LootHistory: no version bump. Branch `feat/2026-10-25-skinning` in WowAddonStandards, LibKa0s,
LootHistory and Ka0sAddonsCommonTasks. The LibKa0s release re-vendors **only LootHistory** in leg 1; the other
consumers stay on v1.77.0 until leg 2 (recorded as a lead's call in the execution record, since `docs/releasing.md`
step 8 normally re-vendors every consumer with the release).

## 9. Left to the builder

File splits, exact primitive internals, which Blizzard textures serve WoW Default/Midnight bevels, the exact
`win.bgTexture` used for WoW Forever's faint texture, and test layout, within the gates (1500 lines, CCN 15, luacheck
0/0, every suite green).
