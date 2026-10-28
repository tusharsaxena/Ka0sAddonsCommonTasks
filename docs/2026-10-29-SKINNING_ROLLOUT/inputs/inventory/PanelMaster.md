# Inventory: PanelMaster (PM)

Read-only inventory for the skinning rollout (items PM-RV, PM-01..PM-05 in `../../00_PLAN.md`).
Repo `../PanelMaster`, branch `master`, clean, TOC `## Version: 1.3.0`, vendors LibKa0s **v1.77.0**
(`CLAUDE.md` provenance line). Read against LibKa0s v1.79.0 (main checkout) and standard `skinning.md`
§1-§8 plus anti-pattern #107. All paths below are relative to `../PanelMaster` unless they start with
`libs/LibKa0s` (the library checkout, `../LibKa0s/LibKa0s/`).

**What the addon is, for skinning purposes.** PanelMaster draws player-designed backdrop panels on the
screen (`modules/Canvas.lua`): a fill, a border, accent bars and artwork per panel, every one of
them a per-record value in `profile.panels[]` that the player chose. Besides those panels it owns
one on-screen overlay (unlock mode, `modules/Unlock.lua`), three settings pages (General, Panels,
Profiles) plus the landing page, four StaticPopups, and the library's debug console and copy window.
It has no standalone window of its own, and no Widgets, Perf, Sim or test strip. Core's skin half is
deliberately not adopted (`core/CoreSetup.lua:124-128`).

---

## 1. Surfaces

| # | Surface | Built at | Look typed today | Paints through (rung 1) |
|---|---|---|---|---|
| S1 | **Panel frame, fill** (one per panel, named `PanelMaster_Panel_<slug>`) | `modules/Canvas.lua:240` (`newFrame`), fill texture `:256` | `f.bg:SetTexture(path,"REPEAT","REPEAT")` + `SetVertexColor(spec.bg)` at `modules/Canvas.lua:450-451`; values from the record: `bgTexture="Solid"` `core/Constants.lua:358`, `bgColor={0.05,0.05,0.07,0.85}` `:346`, class color flag `bgClassColor` | **None. Player content** (see section 4, E8, and D1). Not painted by the facade. |
| S2 | **Panel border** (BackdropTemplate child) | `modules/Canvas.lua:265` | `SetBackdrop({edgeFile, edgeSize})` + `SetBackdropBorderColor(spec.border)` `modules/Canvas.lua:481-484`; `borderTexture="Solid"` `core/Constants.lua:359`, `borderColor={0.35,0.35,0.40,1}` `:347`, `borderSize=0` | **None. Player content** (E8, D1). |
| S3 | **Accent bars** (4 edges, a statusbar strip each) | `modules/Canvas.lua:288-290` | `bar.fill:SetTexture(path)` + `SetVertexColor(a.color)` / `SetColorTexture` fallback `modules/Canvas.lua:419-425`; `accentTexture="Blizzard"` `core/Constants.lua:392`, `accentColor={1,1,1,1}` `:401` with `accentClassColor=true` (class color shows by default) | **None. Player content** (E8, D1). If D1 is overruled: `S.Resolve("bar.texture", rec.accentTexture, rec.accentTextureFromSkin)` feeding the existing `FetchMedia` call (never `S.BarTexture`, which would override every panel). |
| S4 | **Accent bar border** (BackdropTemplate child per bar) | `modules/Canvas.lua:346` (`applyAccentBorder` `:357`) | `SetBackdrop` + `SetBackdropBorderColor` `modules/Canvas.lua:376-377`; `accentBorderTexture="Solid"` `core/Constants.lua:412`, `accentBorderColor={0,0,0,1}` `:418`, size 1 | **None. Player content** (E8, D1). |
| S5 | **Panel artwork** (bundled catalog, Sunn art packs, custom path) | `modules/Canvas.lua:321`, `:333`; paint `:498-560` | `tex:SetTexture(quad.path)` `:521-523`, `SetVertexColor(art.color)` `:546`, `artColor={1,1,1,1}` `core/Constants.lua:443`; textures from `modules/Artwork.lua`, `modules/SunnArt.lua` | **None. Art** (E9). |
| S6 | **Unlock overlay: outline** (4 edge textures on a child frame, raised above the panel ladder) | `modules/Unlock.lua:104` (frame), `:110` (edges) | `tex:SetColorTexture(C.UNLOCK_OUTLINE_RGB)` `modules/Unlock.lua:212-215`; `C.UNLOCK_OUTLINE_RGB={1.00,0.82,0.00,0.90}` `core/Constants.lua:637` | `S.Color("list.dropLine")` read at `U:Decorate` (Ka0s Default `{1,0.82,0,0.9}` exact, `libs/LibKa0s/SkinDefs.lua:289`; every other skin derives it from its accent at 0.9 through `FOLLOW`, `SkinDefs.lua:460`). Alternative with the same Ka0s Default value: `input.focus` (`SkinDefs.lua:245`). See D3. The thickness stays the player's `unlockOutlineSize` (geometry). |
| S7 | **Unlock overlay: name label** | `modules/Unlock.lua:112` (`CreateFontString(nil,"OVERLAY","GameFontNormal")`) | `o.label:SetTextColor(C.UNLOCK_LABEL_RGB)` `modules/Unlock.lua:220`; `{1.00,0.82,0.00}` `core/Constants.lua:638`; font object `GameFontNormal` `:112` | `S.Text(o.label, "accent")` once at overlay creation (`text.accent` = GOLD `{1,0.82,0,1}`, `SkinDefs.lua:216`; body face). Drop the `SetTextColor` and the font object literal. |
| S8 | **Settings: landing page** (logo, tagline, Slash Commands rows) | `settings/Panel.lua:274-290` (`O.BuildLandingPage`) | none typed by the addon: logo `C.LOGO_PATH` `core/Constants.lua`, rows from `NS.Slash:LandingRows()` (library formats `|cffffff00`) | Library (Options chrome follows the descriptor's `addonName` once registered). The logo is art (E9). |
| S9 | **Settings: General page** (Master controls, Moving panels, New panels tabs) | `settings/Panel.lua:350-397` (`O.CreatePanel`, `O.RenderTabbedSchema(c,"general",afterGroup)` `:395`) | none typed | Library: rows through `O.AceGUI` (painted by SkinAce's proxy), header, tab strip, scroll. **The Skin tab goes here**: `O.RenderTabbedSchema(c, "general", afterGroup, nil, { tabs = { O.AppearanceTab(spec) } })`. There is no Keybindings tab (no `Bindings.xml`, no `KeybindingsTab` call), so the Skin tab is last (skinning-§3). Three groups + Skin = 4 tabs, under the budget of 8. |
| S10 | **Settings: Panels page chrome** (page header band with panel picker and New panel box, tab strip over six editor tabs) | `settings/PanelEditor.lua:497-560` (`H.PageHeader`), `:466-480` (`H.TabStrip`) | none typed; header block's widgets acquired with the file-local raw `AceGUI` (`settings/PanelEditor.lua:7`, `:512`, `:531`, `:550`) | Strip and header: library. **The block's widgets are not painted today**, because they come from raw `LibStub("AceGUI-3.0")`, not `O.AceGUI`. Built once and kept for the session (never released), so they need `Skin:PaintAce(owner, w)` at build **and again on `S.OnLooksChanged`** (LootHistory's pattern for kept widgets, `../LootHistory/core/SkinSetup.lua:580-600`). |
| S11 | **Settings: Panels page editor body** (six tabs, 25 AceGUI acquisitions: 5 SimpleGroup, 5 CheckBox, 5 Dropdown/LSM30, 3 EditBox, 1 Slider, 1 ColorPicker, 1 Heading, 1 Label + the page's own button) | `settings/PanelEditor.lua:233,241,256,302,356,401,424,653,690`; `settings/PanelEditorTabs.lua:123,132,153,180,198,306,337,357,375,632` | `editorHeading` sets `h.label:SetFontObject(_G.GameFontNormalLarge)` `settings/PanelEditor.lua:260-262` (mirrors the library's own `O.Section`, `libs/LibKa0s/OptionsWidgets.lua:568-570`) | Switch the two files' `local AceGUI = LibStub("AceGUI-3.0")` (`settings/PanelEditor.lua:7`, `settings/PanelEditorTabs.lua:7`) to `NS.Helpers.AceGUI` (= `O.AceGUI`, the owner proxy that paints on Create), read lazily at build time, or call `Skin:PaintAce` per widget. The composed `O.BorderGroup`/`O.BarGroup` rows (`settings/PanelEditorTabs.lua:499`, `:550`) already go through the library. The heading's `SetFontObject` stays (it is the library's own order in `O.Section`; see D8). LSM30 pull-outs and ColorPickerFrame stay stock (E2, E3). |
| S12 | **Settings: the "(disabled)" marker** in the panel picker list | `settings/PanelEditor.lua:633` | `" |cff808080(disabled)|r"` (0.5 gray) | Escape built from `S.Color("text.disabled")` (Ka0s Default DIM `{0.5,0.5,0.5,1}` exact, `SkinDefs.lua:216`/`:194`) through a small hex helper. |
| S13 | **Settings: Profiles page** (AceConfigDialog into a SimpleGroup) | `settings/Panel.lua:453-490`; container `:471`, open `:487` | none typed | `Skin:PaintAceTree(owner, container)` after each `AceConfigDialog:Open` (`settings/Panel.lua:487`), as LootHistory does (`../LootHistory/settings/Profiles.lua:69`). The container itself comes from `O.AceGUI` and is painted; AceConfigDialog's children come from raw AceGUI and are not. |
| S14 | **Tooltip lines the addon writes** (GameTooltip, through `O.AttachTooltip`) | `settings/PanelEditorTabs.lua:316`, `:654-655`, `:679`, `:696-702`, `:718-723`, `:766-767`, `:786` (inline `|cffffff00…|r` emphasis inside tooltip bodies) | `|cffffff00` = `{1,1,0}` yellow | No token answers `{1,1,0,1}` today. See gap **PM-G1** and D4. Body and title lines are the library's (`O.AttachTooltip`). The GameTooltip frame stays Blizzard's (E4). |
| S15 | **Debug console + its copy window** (also the `/pm diagnostics` report's copy) | `core/DebugLogSetup.lua:115-178` (`lib:New`, `name`, `addonName`, `font = C.FONT_MONO`) | none typed by the addon. `applySkin`/`skin`/`makeCloseButton` deliberately not passed (`:171-190`) | Library: DebugLog minor 22 takes the owner from `addonName` when neither `skin` nor `applySkin` is passed (`libs/LibKa0s/DebugLog.lua:305`). **Nothing to change**: it follows the owner from the moment `RegisterOwner` runs. The mono `font` stays (sanctioned, debug-logging-§2). |
| S16 | **Minimap button / broker tooltip** | `core/LauncherSetup.lua:169-188` | none typed by the addon (the library draws the status tooltip) | Library. LibKa0s-Launcher-1.0 has no skin owner (`libs/LibKa0s/Launcher.lua`, no `Skin` reference); the icon is the addon's art (E9). Nothing to do here. |
| S17 | **StaticPopups** `KA0S_PANELMASTER_RESETALL`, `_DELETEALL`, `_DELETE`, `_RESET` | `settings/Slash.lua:93`, `:101`, `:118`, `:126` | Blizzard's | Never (E1). |
| S18 | **Chat output** (`NS.PREFIX` `|cff00ffff[PM]|r`, `/pm list` / `/pm panel` dumps, "unlock queued" lines, schema error) | `core/Namespace.lua:19`; `settings/Slash.lua:163,193-214`; `modules/Unlock.lua:175,364`; `settings/Schema.lua:903` | `|cff00ffff`, `|cff33ff99`, `|cffffff00`, `|cff808080`, `|cffffffff`, `|cffff0000` | Never (E5, D5). |
| S19 | **The first-run skin picker** (new, PM-04) | (new) `core/SkinSetup.lua` | — | `O.SkinPicker(spec)` (library; owner defaults to the descriptor's `addonName`). |
| S20 | **The Skin tab** (new, PM-01) | (new) `settings/Panel.lua` General renderer | — | `O.AppearanceTab(spec)` (library). |

Not present (checked): no standalone window of the addon's own, no Widgets factory call
(`grep -rn "Widgets" core modules settings` finds comments only), no perf panel (Perf declined,
`CLAUDE.md`), no sim panel, no test strip, no chart, no HUD font, no bars of the HUD kind.

## 2. Library factories that take an owner

| Factory | Where | Owner today | Action |
|---|---|---|---|
| `LibKa0s-Options-1.0` `lib:New` descriptor `addonName` | `settings/OptionsSetup.lua:185-195` | `addonName` (folder) ✓ | none: the pages follow once `RegisterOwner(addonName)` runs |
| `LibKa0s-DebugLog-1.0` `lib:New` `addonName` | `core/DebugLogSetup.lua:127` | `addonName` ✓ | none |
| `Core.MakeCloseButton(parent, onClick, addonName)` via `NS.MakeCloseButton` | `core/CoreSetup.lua:142-144` | `addonName` ✓ (no caller yet; pinned by `tests/test_libka0s.lua`) | none |
| `O.AppearanceTab(spec)` | new, General renderer | — | `spec.get` / `spec.set` = the `skin.*` read and the write seam; `strings` only if translating (the addon ships enUS only) |
| `O.SkinPicker(spec)` | new, `core/SkinSetup.lua` | defaults to `addonName` | `get`, `set` (write seam), `page = "general"`, `tab = "Appearance"`, `onClose` sets `skin.pickerSeen` |
| `Skin:PaintAce` / `Skin:PaintAceTree` / `Skin:OnRelease` | new, settings/PanelEditor*.lua, settings/Panel.lua | — | owner `addonName`. No host `OnRelease` exists today (`grep -n "OnRelease" settings modules core` finds a comment only), so `Skin:OnRelease` has no caller unless one is added |
| `LibKa0s-Launcher-1.0` | `core/LauncherSetup.lua:169` | takes no owner | — |
| Widgets factories (dropdown, search box, copy window, test strip, autocomplete, drag handle, reorder, line chart) | — | not consumed | — |
| `Core.ApplySkin` | — | not adopted (`core/CoreSetup.lua:124`) | — |

## 3. HUD style settings (O2's one-time reset)

**No schema-row HUD style setting.** The profile's `settings` table (`defaults/Profile.lua:23-63`)
holds `enabled`, `visibility`, `scale`, `alpha`, `snapToGrid`, `gridSize`, `unlockOutlineSize`,
`showLabels`, `defaultWidth`, `defaultHeight`, `defaultStrata`, `defaultAlpha`: behavior and geometry,
no texture, border, font or style color. The unlock overlay's colors are constants, not settings (S6,
S7).

**The on-screen look lives in the panel records**, per panel, in `profile.panels[]` (a structural
registry written only by `NS.Registry`, never a schema row; `defaults/Profile.lua:8-16`). The style
fields and their template defaults (`core/Constants.lua:326-470`):

| Record field | Kind | Default | How S.Resolve / FROM_SKIN / fromSkin would take it |
|---|---|---|---|
| `bgTexture` | LSM `background` | `"Solid"` (`:358`) | no skin token for a backdrop fill texture (`win.bgTexture` is window chrome, `false` in Ka0s Default) |
| `bgColor` | color | `{0.05,0.05,0.07,0.85}` (`:346`) | nearest `win.bg` `{0.06,0.06,0.08,0.92}`: not equal |
| `borderTexture` | LSM `border` | `"Solid"` (`:359`), drawn only when `borderSize>0` (default 0) | `O.BorderGroup{fromSkin=true}` companion `borderTextureFromSkin` -> `bar.borderStyle` (Ka0s Default `"None"`) |
| `borderColor` | color | `{0.35,0.35,0.40,1}` (`:347`) | no companion for a color |
| `accentTexture` | LSM `statusbar` | `"Blizzard"` (`:392`) | `O.BarGroup{fromSkin=true}` companion `accentTextureFromSkin` -> `bar.texture` (Ka0s Default `"Ka0s Default"`, not `"Blizzard"`) |
| `accentColor` / `accentClassColor` | color / bool | white / **true** (`:401-402`) | class color: rung 4 |
| `accentBorderTexture` | LSM `border` | `"Solid"` (`:412`), size 1 | companion -> `bar.borderStyle` (Ka0s Default `"None"`: the 1px black hairline would vanish) |
| `accentBorderColor` | color | `{0,0,0,1}` (`:418`) | `bar.border` `{0,0,0,1}` equal, but no companion exists for a color |
| `artTexture`, `artColor`, `artBlend`, ... | artwork | `"None"`, white | art: rung 4 |

**Recommendation (D1): no HUD reset for PanelMaster.** The panels are the player's own artwork, not
the addon's chrome: the whole addon is a tool for designing them, a layout typically matches another
UI (BenikUI-style strips, Sunn art packs), and other addons and WeakAuras anchor to them by name.
R3 assumes a style setting the addon chose for the player; here every value is a per-panel choice the
player made. Resetting `accentTexture` and the two border styles on every record of every profile
would also **change Ka0s Default's look** (accent `Blizzard` -> `Ka0s Default` bar; the accent's 1px
black border and any panel border -> `None`), which the plan says stops the run to ask. So: PM-03
covers the unlock overlay only (S6, S7) and records the absent reset in `exceptions.tsv`, with a
proof command such as `grep -nE "Texture|Color|font" defaults/Profile.lua` (no style key in the
schema's store) and the record-template cite. Hence `hud_style_settings` is reported empty.

If the owner overrules D1, the narrowest form is opt-in companions on the editor's composed groups
(`fromSkin = true` on `O.BarGroup` `settings/PanelEditorTabs.lua:550` and the accent `O.BorderGroup`
`:584`), defaulting **false**, rendered through `S.Resolve`, with **no** reset migration. A reset
would be one per-profile step in `NS:RunMigrations` (`core/Database.lua:204`, `NS.SCHEMA_VERSION`
2 -> 3 at `core/Namespace.lua:14`) walking every record, which is exactly the restyle-on-upgrade the
template's own comment forbids (`core/Constants.lua:431-434`).

## 4. Exceptions

| # | What | Rung | Reason |
|---|---|---|---|
| E1 | The four StaticPopups (`settings/Slash.lua:93-126`) | 3 | skinning-§7: a StaticPopup is never restyled |
| E2 | AceGUI-3.0-SharedMediaWidgets pull-outs: the LSM30 media pickers (`settings/PanelEditor.lua:302`, and the composed groups' pickers) | 3 | skinning-§7; SkinAce leaves LSM30 widgets stock (`libs/LibKa0s/SkinAce.lua:45`) |
| E3 | `ColorPickerFrame`, opened by the AceGUI ColorPicker swatches (`settings/PanelEditor.lua:356`, composed groups) | 3 | skinning-§7 |
| E4 | GameTooltip's frame (every `O.AttachTooltip`, the launcher tooltip) | 3 | skinning-§7: the frame keeps Blizzard's look; only lines take skin colors |
| E5 | Chat output colors: `NS.PREFIX` cyan (`core/Namespace.lua:19`), the `/pm list` and `/pm panel` dumps (`settings/Slash.lua:163-214`), "unlock queued" (`modules/Unlock.lua:175,364`), the schema error line (`settings/Schema.lua:903`) | 3 | the chat frame is Blizzard's; the prefix is the standard's chat convention, the same in every addon. See D5 |
| E6 | `SettingsPanel` chrome around the three pages | 3 | skinning-§7 (the library paints its own header and backdrop inside the canvas only) |
| E7 | The panels' class colors: `bgClassColor`, `borderClassColor`, `accentClassColor` (default **on**), `accentBorderClassColor`, `artClassColor` (`core/Constants.lua` `C.COLOR_FIELDS`, `C.COLOR_CLASS_SOURCE`) | 4 | class colors keep their meaning |
| E8 | The panels' own fill, border, accent bar and accent-bar border: textures and colors per record (S1-S4; `modules/Canvas.lua:419-484`) | 4 (player content; the plan has no rung for it, so filed as 4) | the player designed each panel; a skin must not repaint a layout the player built to match other UI, and doing so changes Ka0s Default's look. See D1 |
| E9 | Artwork (bundled catalog, Sunn art packs, custom paths; `modules/Canvas.lua:498-560`), the landing logo `C.LOGO_PATH` and the addon icon `C.ICON_PATH` | 4 | art, like spell and item icons |
| E10 | The debug console's mono face `C.FONT_MONO` (`core/DebugLogSetup.lua:131`) | 4 (sanctioned) | debug-logging-§2's aligned columns need a fixed-width face; the console's colors themselves follow the skin (S15) |

## 5. Gaps (rung 2)

One candidate, and it is conditional on D4.

**PM-G1: an emphasis color for words highlighted inside tooltip bodies the addon writes.**
- Component: the inline `|cffffff00…|r` emphasis in the Panels editor's tooltips
  (`settings/PanelEditorTabs.lua:316` frame name; `:654-655` example paths; `:679`; `:696-702` fill
  modes; `:718-723` layers; `:766-767` blend modes; `:786`). The same yellow is the collection's
  command highlight (options-ui-§5 mandates `|cffffff00/<slash> <verb>|r` on the landing rows, which
  the library itself types), so the shape recurs in other addons' tooltips.
- Why no primitive or token fits: no token resolves to `{1,1,0,1}` in Ka0s Default. The `gtip.*`
  set is `gtip.title` GOLD `{1,0.82,0}`, `gtip.body` `{0.9,0.9,0.9}`, `gtip.muted` `{0.5,0.5,0.5}`,
  `gtip.value` white, `gtip.subtle` `{0.7,0.7,0.7}` (`libs/LibKa0s/SkinDefs.lua:218-231`); the
  nearest, `gtip.title`, turns the emphasis gold and changes Ka0s Default's pixels.
- Proposed: token `gtip.emphasis` (color), "a word picked out inside a GameTooltip line the addon
  writes (an option name, a path, a command)". The other skins may keep it yellow or use their
  accent, never dark, since the GameTooltip frame stays Blizzard's in every skin.
- Ka0s Default must reproduce: `{1, 1, 0, 1}` (`|cffffff00`, as typed at the lines above).

No other gap: the unlock outline and label, the disabled marker, the settings widgets and the tool
windows all have an existing primitive and a token whose Ka0s Default value is the value typed today
(section 1).

## 6. Doubtful calls (for DECISIONS.md)

- **D1. Are PanelMaster's panels the "HUD" that O2's reset covers?** Recommendation: **no.** The
  panels are player-authored content. They stay unskinned (E8), PM-03 is the unlock overlay only,
  and there is no reset migration. Applying R3 would restyle every saved panel layout on upgrade and
  change Ka0s Default's look (`Blizzard` -> `Ka0s Default` accent texture, the black accent hairline
  -> `None`). Fallback if overruled: opt-in `fromSkin` companions defaulting false, with no reset.
- **D2. The New-panel template (`C.PANEL_TEMPLATE`, `core/Constants.lua:326`).** Should a panel
  created under a skin start in that skin's colors? Recommendation: **no.** No token equals the
  template's fill `{0.05,0.05,0.07,0.85}` (`win.bg` is `{0.06,0.06,0.08,0.92}`), so this would
  change Ka0s Default, and the "New panels" tab already gives the player a house style.
- **D3. The unlock outline's token.** Recommendation: **`list.dropLine`** (Ka0s Default
  `{1,0.82,0,0.9}` exact; every skin's accent at 0.9 through FOLLOW). It already means "the drag
  target's marker", which is what the outline is. `input.focus` has the same Ka0s Default value but
  means a focused text field. The label is `S.Text(label, "accent")`.
- **D4. Inline emphasis inside tooltip bodies (`|cffffff00`), PM-G1.** Recommendation: **rung 2, one
  token `gtip.emphasis`** if at least one other inventory shows the same inline yellow (likely,
  because the landing-row convention is collection-wide). Otherwise rule it **rung 4, content markup**
  (the standard's own command-highlight convention) and leave the escapes. Either way it should be
  one collection-wide ruling, not a per-addon one.
- **D5. Chat output colors.** Recommendation: **exception (E5)**. The chat frame is Blizzard's, the
  `[PM]` cyan prefix is the standard's per-addon chat tag, and a skin that recolored chat would make
  two addons' lines differ by skin. The run should rule this once for the collection.
- **D6. The picker's eye (`onPreview`).** PanelMaster has no test mode (options-ui-§15 exempts it,
  since unlock mode is its preview), and with D1 the skin shows nowhere on screen except the settings
  pages and the console. Recommendation: **omit `onPreview`** (the eye is hidden) and declare only
  `settings` in the icons line. Alternative for uniformity: declare `eye` as well, unused.
- **D7. Where the `skin.*` keys live.** The plan names `skin.*` (LootHistory uses `appearance.*`).
  Recommendation: a new top-level `profile.skin = { source="ka0s", skin="ka0s", ignoreFonts=false,
  ignorePanel=true, font="", texture="", pickerSeen=false }`, a sibling of `settings` and `panels`,
  as skip-render schema rows routed through `NS.SchemaRuntime.Set`. New keys with AceDB defaults, so
  no migration is owed for them. Check `settings/PanelSchema.lua`'s profile view so the General page
  neither draws nor resets them as ordinary rows. Note also that *Reset all settings* here is
  `db:ResetProfile()`, which takes the player's panels with it (`defaults/Global.lua` notes); the
  skin choice returning to Ka0s Default is the smaller effect of that reset.
- **D8. The editor heading's `SetFontObject(GameFontNormalLarge)` (`settings/PanelEditor.lua:260`).**
  This is a literal font object on an adopted addon's frame (#107's letter), but it copies
  `O.Section` (`libs/LibKa0s/OptionsWidgets.lua:568`), which does the same after the proxy's paint.
  Recommendation: **keep it in step with `O.Section`** and do whatever the library does. If the
  library's heading is ever moved to `S.Text(..., "heading")`, this moves with it. Not a PanelMaster
  finding.

## 7. Re-vendor v1.77.0 -> v1.79.0 obligations (PM-RV)

- **Options degradation stub** (`settings/OptionsSetup.lua:45-139`) gains, beside `KeybindingsTab`
  (`:110`): `AppearanceTab = function() return { key = "Appearance", label = "", render = noop } end`,
  `AppearanceRows = function() return nil end` (v1.78.0), `SkinPicker = function() return nil end`,
  `HideSkinPicker = noop` (v1.79.0). `tests/test_surface_parity.lua:207-237` (`assertSurfaceParity`
  against `LibKa0s-Options-1.0`) is red until it does. Check that its `loadPartial({ Options,
  OptionsWidgets, OptionsScroll })` (`:213`) still produces a degraded arm with the two new files
  (`OptionsAppearance.lua`, `OptionsSkinPicker.lua`) present.
- **Whole-folder copy** from the tag through `git archive`: new files `WidgetsCopyWindow.lua`,
  `DebugLogWindow.lua`, `OptionsAppearance.lua`, `SkinAce.lua`, the Skin major's seven files, `Toast.lua`
  and `OptionsSkinPicker.lua`; `media/fonts/` (the skin faces, Oxanium SemiBold and Bold, their OFL
  texts); `media/textures/` (Glass art and the eight bars). `tests/_kit/` at the paired revision
  (kit 43 or later; `mock_paint.lua` is opt-in).
- **`CLAUDE.md`**: the provenance line `Bundles [LibKa0s](...) v1.77.0 (MIT).` -> the run's tag, in the
  same commit as the bytes. The **icons line** `LibKa0s icons: clear, close, copy.` -> add `settings`
  (and `eye` only if D6 goes the other way), and prune `libs/LibKa0s/media/icons/` with the tag's
  `tools/prune-icons.lua`. The prose "Ten of the seventeen majors are adopted (...)" -> eleven of
  nineteen once `Skin` is adopted (v1.78.0 adds Skin, v1.79.0 adds Toast; `Toast` is vendored but not
  consumed), and the paragraph naming the three icons' uses gains the picker's gear.
- **TOC**: `## OptionalDeps:` (`PanelMaster.toc:8`) gains `EllesmereUI` (skinning-§5); add
  `core\SkinSetup.lua` to the TOC (early, before `settings\OptionsSetup.lua`, after
  `core\CoreSetup.lua`; it must run at file load).
- **Test pins that move**: `tests/test_libka0s.lua:1131-1147` `SEAM_FILES` must list
  `core/SkinSetup.lua` (the test at `:1156` derives every TOC file that resolves a `LibKa0s-` major and
  fails on one not listed). `tests/test_debuglog.lua:172-176` hard-lists source files for the gate
  check, so add the new file if it calls `NS.Debug`. `tests/test_vendor_sync.lua` holds both payloads
  to the provenance tag. No test pins a library minor numerically beyond `MODULES.X == MINOR`
  self-checks (`tests/test_libka0s.lua:44-46,113,291,471-475`), which survive.
- **Ka0s Default looks different at the re-vendor (v1.79.0)**: once PanelMaster registers, its
  settings pages and console draw Oxanium. The smoke checks re-look at Ka0s Default (PM-05).
- **README**: the tests badge count (`README.md:7`, `1091/1091`), and font credits for the faces the
  payload now ships (Oxanium, the skin faces) beside the JetBrains Mono credit (`README.md:~291`).

## 8. Risks

- **Raw AceGUI in the editor** (`settings/PanelEditor.lua:7`, `settings/PanelEditorTabs.lua:7`). Today
  25 widgets bypass `O.AceGUI`, so the owner proxy never paints them. Switching to the proxy fixes the
  editor body, but the Panels page header band is **built once and never released**
  (`settings/PanelEditor.lua:497-520`; `settings/Panel.lua:431-437` builds only on the first render).
  A skin switch re-renders the page, but the band's picker and create box are not re-acquired, so they
  keep the old skin unless `S.OnLooksChanged` re-runs `Skin:PaintAce` on them. Never release the create
  box mid-callback (the file says why, `:497-505`).
- **Pooled AceGUI**: every painted widget must go back stock through SkinAce's `OnRelease`. PanelMaster
  sets no `OnRelease` of its own today, so there is nothing to chain. A new one must use `Skin:OnRelease`.
  The Profiles page (AceConfigDialog) re-opens on every show (`settings/Panel.lua:484-488`), so
  `PaintAceTree` must run after each `Open`, not once.
- **The open-dropdown registry** wraps `O.RenderField` and `O.EnsureScroll` on the instance
  (`settings/Panel.lua:160-215`). The skin's re-render goes through `O.RefreshAllPanels`, so check that
  `forgetDropdowns` still runs before the release, or a stale registry entry closes a released widget.
- **Hot path**: `modules/Canvas.lua:654-690` runs a shared 10Hz `OnUpdate` (mouseover fade). Nothing
  skin-related may run there. Read the overlay tokens in `U:Decorate` only, and only for unlocked panels.
- **Repaint of the unlock overlay** on a skin change: the overlay paints with raw `SetColorTexture` from
  a token read, so the facade does not record it. Hook `S.OnLooksChanged` to re-run `Canvas:Render` for
  unlocked panels only. Or record the label with `S.Text`, which repaints by itself, and the edges by
  re-decorating.
- **Combat**: panels are plain non-secure frames (`modules/Canvas.lua:240`), and unlock is deferred in
  combat (`modules/Unlock.lua:172-179`), so the overlay never shows under lockdown. The picker's queue
  waits out combat. Show it from a post-login timer, as LootHistory does
  (`../LootHistory/core/LootHistory.lua:188`), and hide it from `LifecycleSetup`'s disable path.
- **Taint**: nothing touches a Blizzard frame. Keep it that way: no `PaintAce` on the StaticPopups, and
  no skin on the panels, which other addons and WeakAuras anchor to by global name.
- **EllesmereUI**: one-way paint. Under `eui` only the settings pages and console change; the panels
  are untouched by design (E8).
- **File cap**: no authored file is near 1500 lines. The largest are `modules/Registry.lua` 990,
  `modules/Canvas.lua` 961, `settings/Schema.lua` 907, `settings/PanelEditorTabs.lua` 851,
  `settings/PanelEditor.lua` 778 and `settings/Slash.lua` 768. The new `core/SkinSetup.lua` should stay
  small (LootHistory's is 631 with overrides, ignore flags and the picker).
- **The unlock outline changes in other skins** (accent instead of gold). That is intended, but players
  who find panels by the gold outline will see a different color. Note it in smoke.

## 9. Effort

**M.** The settings and tool windows are library-driven and the addon already passes `addonName`
everywhere. The work is the seam file, the `skin.*` keys and the Skin tab, the picker, routing two
editor files' 25 AceGUI acquisitions through the owner proxy (plus the kept header band and the
Profiles tree), the unlock overlay, the two escape-code sites, the stub and pins, and docs. Under D1
there is no HUD reset or migration.
