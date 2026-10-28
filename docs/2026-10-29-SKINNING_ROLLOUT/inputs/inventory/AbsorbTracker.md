# Inventory: AbsorbTracker (AT)

Read-only M0 inventory for the skinning rollout (`../../00_PLAN.md`, items AT-RV, AT-01..AT-05).
Repo `../AbsorbTracker`, branch `master` at `32824f2`, vendors LibKa0s v1.77.0 (`CLAUDE.md:46`), icons
line `clear, close, copy, help` (`CLAUDE.md:47`). The rollout's library tag is v1.79.0 (no rung-2 gap here,
see section 5). Paths below are relative to the addon root unless they start with `LibKa0s/`.

What the addon is, visually: **three HUD bars** (player / target / focus), plain frames with a backdrop
background, a StatusBar fill, a border frame and a value FontString, each with a LibKa0s drag strip when
unlocked. Everything else it shows is drawn by the library: four settings pages (landing/About, General,
Appearance, Profiles), the debug console and its copy window, the perf panel, the minimap button. No test
strip (options-ui-§15 exempts it from Test mode; unlocking is its preview), no sim, no windows of its own,
no tooltips of its own (the strip's tooltips are the widget's).

Owner string: `AbsorbTracker` (the folder; `addonName` in every setup file already).

## 1. Surfaces

| # | Surface | Built at | What it types today | Paints through (rung 1) |
|---|---|---|---|---|
| S1 | HUD bar root, backdrop **background** (x3, `AbsorbTrackerFrame`, `...TargetFrame`, `...FocusFrame`) | `modules/Bar.lua:225`, backdrop `:239-247`, repainted `modules/Display.lua:194-203` | `bgFile = C.FALLBACK_TEXTURE` (`core/Constants.lua:7`, `Interface\TargetingFrame\UI-StatusBar`) at build, then `NS.GetBgTexture` (`core/Data.lua:123-130`, LSM key `bgTexture` = `"Blizzard Raid Bar"`, `defaults/Profile.lua:17`); color **literal** `SetBackdropColor(0.2, 0.2, 0.2, 0.8)` at `modules/Bar.lua:248` (anti-pattern #107), then `NS.GetBgColor` (`core/Data.lua:240-244`, stored `bgColor` `{.2,.2,.2,.8}`, `defaults/Profile.lua:38`) at `modules/Display.lua:203`; insets `max(1, floor(borderSize/4))` `modules/Display.lua:190` | Texture: `S.Resolve("bar.texture", bgTexture, barTextureFromSkin)` then `LSM:Fetch` (doubtful D3: governed by the bar texture's companion). Color: the player's `bgColor` / class palette (see D5; `bar.bg` is nil in Ka0s Default). Drop the build-time literal: build with `NS.GetBgColor(unit)` or nothing (the appearance pass paints before first show). |
| S2 | HUD bar **fill** (StatusBar) | `modules/Bar.lua:259-266`, repainted `modules/Display.lua:186-187` | Texture `NS.GetBarTexture` (`core/Data.lua:114-121`, LSM `barTexture` = `"Blizzard Raid Bar"`, `defaults/Profile.lua:16`; fallback `C.FALLBACK_TEXTURE`); color **literal** `SetStatusBarColor(0.4, 0.7, 1, 0.8)` at `modules/Bar.lua:265` (#107), then `NS.GetBarColor` (`core/Data.lua:234-238`, stored `barColor` `{.4,.7,1,.8}`, `defaults/Profile.lua:37`, or class color) | `S.Resolve("bar.texture", barTexture, barTextureFromSkin)` -> `LSM:Fetch("statusbar", key)` -> `SetStatusBarTexture`, inside `NS.GetBarTexture`. **Not `S.BarTexture`** (risk R2). Color stays the host's (`S.BarTexture`'s own contract: "the color is the bar's own"); D5. Build-time literal replaced by `NS.GetBarColor(unit)`. |
| S3 | HUD bar **border** frame (BackdropTemplate, edge only) | `modules/Bar.lua:270-281`, repainted `modules/Display.lua:204-210` | `edgeFile = NS.GetBorder` (`core/Data.lua:132-139`, LSM border `"Blizzard Tooltip"`, `defaults/Profile.lua:18`; fallback `C.FALLBACK_BORDER` `core/Constants.lua:8`); `edgeSize = 12` literal at build (`modules/Bar.lua:276`), then stored `borderSize` (12, `defaults/Profile.lua:19`); color from the **constants table** `unitDefaults.borderColor` at `modules/Bar.lua:279-280` (#107 names "a constants-table entry"), then `NS.GetBorderColor` (`core/Data.lua:246-250`, `{.5,.5,.5,1}`, `defaults/Profile.lua:20`) | `S.Resolve("bar.borderStyle", border, borderFromSkin)` and `S.Resolve("bar.borderSize", borderSize, borderFromSkin)` (D4) inside `NS.GetBorder` / the appearance pass; color: the player's `borderColor` / class (D5; `bar.border` is nil in Ka0s Default). Build-time edge from `NS.GetBorderColor(unit)`. |
| S4 | HUD **value text** (FontString on the overlay frame; also the unlocked placeholder `"Absorb"`) | `modules/Bar.lua:291-294`; repainted `modules/Display.lua:212-230`; placeholder `modules/Display.lua:41-42, 83` | Face `NS.GetFont` (`core/Data.lua:141-148`, LSM `"Friz Quadrata TT"`, `defaults/Profile.lua:21`; fallback `C.FALLBACK_FONT` `core/Constants.lua:9`), size 12, flags `"OUTLINE"` (`defaults/Profile.lua:22-23`); color `NS.GetFontColor` (`core/Data.lua:253-257`, white `defaults/Profile.lua:31`, or class); shadow literal `SetShadowColor(0,0,0,1)` / offset `(1,-1)` when `fontShadow` (`modules/Display.lua:224-230`) | `S.Resolve("hud.font", font, fontFromSkin)` -> `LSM:Fetch("font", key)`; size and flags stay the player's (D4: `hud.fontSize` 12 and `hud.outline` `"OUTLINE"` in Ka0s Default equal AT's defaults); color the player's (no HUD text-color token; D5). Shadow: the on/off is the player's (options-ui-§16 font block); the black shadow color is a drop-shadow constant, not chrome (D7). |
| S5 | Bar **text overlay** frame | `modules/Bar.lua:285-288` | nothing (mouse-off host for S4) | nothing to paint |
| S6 | Unlocked **drag strip** per bar (LibKa0s-Widgets `DragHandle`, label, `?` help mark, X close mark) | `modules/Bar.lua:132-198` (`Widgets.DragHandle(bar, {...})` at `:135`) | No colors typed by AT; art `NS.Icon("help")` / `NS.Icon("close")` (`modules/Bar.lua:140, 179`, `core/MediaSetup.lua:249-252`); palette is the widget's `DH_PAL` | Hand the widget `owner = addonName` (WidgetsDragHandle minor 6, `LibKa0s/WidgetsDragHandle.lua:53-55, 186-194`): `handle.bg`, `handle.edge`, `text.accent` (label), `icon.tint`, `icon.hot`. Bar.lua must capture the folder name (`local addonName, NS = ...`; today `local _, NS = ...` at `:1`). |
| S7 | Drag strip **tooltips** (strip, `?`, X) on GameTooltip | descriptors `modules/Bar.lua:150-183`, placement `NS.Util.PlaceTooltipBeside` `:85-101` | No colors typed by AT; the widget writes the lines | The widget, with its owner (S6). GameTooltip's frame is never painted (exception E3). |
| S8 | Settings: landing/About page (logo + slash rows) | `settings/About.lua` (`Helpers.BuildLandingPage`), logo `core/Constants.lua:38` | logo path only | Library chrome via the descriptor's `addonName` (`settings/OptionsSetup.lua`, descriptor `addonName = addonName`) once the owner registers: header, title, divider, scrollbar (`S.Shell`/`S.TitleBar`/`S.Divider`/`S.ScrollBar`, `title.text`, `divider`, `scroll.*`, `text.heading`). Logo is addon art (E8). |
| S9 | Settings: **General** page (Master controls, Behavior tabs) | `settings/General.lua:391` (`H.CreatePanel`), render `:422-433` (`H.RenderTabbedSchema(c, "general", { [H.MASTER_GROUP] = masterTail })`) | none | Library chrome + `O.AceGUI` proxy rows (automatic for a registered owner). **Gains the Skin tab** (AT-01): `opts.tabs = { H.AppearanceTab(spec) }` as RenderTabbedSchema's 5th arg (`pairWith` nil). The page has no Keybindings tab, so it lands last (`OptionsTabs` places a host tab "last when this render draws no such tab"); tab count 2 -> 3, inside options-ui-§13's budget. |
| S10 | Settings: **Appearance** page (per-unit bar look: Size, Fill, Background, Border, Text) | `settings/Appearance.lua:315` (`H.CreatePanel`), rows `:126-306` via `H.BarGroup` `:176`, `H.ColorPair` `:215`, `H.BorderGroup` `:239`, `H.FontGroup` `:260`, hand row `bgTexture` `:201-214` (`LSM30_Statusbar`) | none | Library chrome + proxy rows. The three composers take `fromSkin = true` (AT-03); see section 3. |
| S11 | Appearance page **chrome block** widgets AT acquires itself: Unit `Dropdown`, enable `CheckBox`, *Link to Player* `CheckBox`, *Copy from Player* `Button` | `settings/UnitPanel.lua:211, 232, 248, 259`; two plain layout frames `:150` (no art) | none | `NS.AceGUI` is the instance's `O.AceGUI` (handed by `onAceGUI`, `settings/OptionsSetup.lua:157`; `LibKa0s/OptionsRegistry.lua:214`), the owner proxy that paints on `Create`. Follow LootHistory (`settings/Panel.lua:33-41`): an explicit `Skin:PaintAce(owner, w)` after each Create so the host does not depend on which handle it got. No host `OnRelease` exists (grep), so nothing to chain through `Skin:OnRelease`. |
| S12 | Settings: **Profiles** page (AceDBOptions via AceConfigDialog into a `SimpleGroup`) | `settings/Profiles.lua:39-75`, container `:68` from **raw** `LibStub("AceGUI-3.0")` (`:25`) | none | `Skin:PaintAceTree(owner, container)` after `AceConfigDialog:Open` (LootHistory `settings/Profiles.lua:69` precedent); prefer `NS.AceGUI or LibStub(...)` for the container as LootHistory does (`:32`). AceConfigDialog's children come from AceGUI itself, past the proxy, hence the tree paint. |
| S13 | **Debug console** + its **copy window** | `core/DebugLogSetup.lua:123-135` (descriptor `addonName = addonName`) | none (library) | Automatic once registered: DebugLogWindow takes the descriptor's `addonName` as owner (`LibKa0s/DebugLogWindow.lua:18-26`; `log.ts`, `log.tag`, `log.text`, `log.count`). Nothing to change in AT beyond registering. |
| S14 | **Perf panel** | `core/PerfSetup.lua:35-45` (descriptor `addonName = addonName`) | none (library) | Automatic once registered (`LibKa0s/PerfPanel.lua:72-77`; `sem.step*`, `text.faint`). |
| S15 | **Minimap button** + LDB/launcher tooltip | `core/LauncherSetup.lua:107-131` | icon path only | Not skinned (E4). |
| S16 | Reset-all confirmation **StaticPopup** `ABSORBTRACKER_RESET_ALL` | `settings/General.lua:359-373`, shown `:140` | none | Never painted (E2). |
| S17 | **Chat** output: `NS.PREFIX` cyan `|cFF00FFFF[AT]|r` (`core/Namespace.lua:10`), stub disabled line gold (`settings/Slash.lua:35`), mirror note gray `|cff808080` (`settings/Slash.lua:60`), debug ON/OFF `|cff40ff40` / `|cffff4040` (`core/DebugLogSetup.lua:65`) | as cited | hex escapes | Not a frame; slash-commands' mandated colors (E7). The ON/OFF pair is D8. |
| S18 | **New: first-run skin picker** (AT-04) | to be added | — | `H.SkinPicker(spec)` (`O.SkinPicker`, OptionsSkinPicker minor 1), library-drawn. |
| S19 | **New: Skin tab** (AT-01) | to be added on General | — | `H.AppearanceTab(spec)`, library-drawn. |

Settings rows that open Blizzard/third-party pop-outs (the color rows' `ColorPickerFrame`, the LSM30
statusbar/border/font pull-outs) are E1/E5.

## 2. Library factories that take an owner

| Factory | Call site | Owner today | Change |
|---|---|---|---|
| `LibKa0s-Widgets-1.0` `DragHandle(parent, spec)` | `modules/Bar.lua:135` | none | add `owner = addonName` to the spec (WidgetsDragHandle minor 6). Bars are built at **file load**, so `core/SkinSetup.lua` must load before `modules/Bar.lua` (it will: core/ precedes modules/ in the TOC). |
| `LibKa0s-Options-1.0` `lib:New(descriptor)` | `settings/OptionsSetup.lua` (descriptor `addonName = addonName`) | already the folder | nothing; the page owner becomes live when `RegisterOwner` runs. |
| `LibKa0s-DebugLog-1.0` `New` | `core/DebugLogSetup.lua:123-135` (`addonName`) | already | nothing. |
| `LibKa0s-Perf-1.0` `New` | `core/PerfSetup.lua:35-45` (`addonName`) | already | nothing. |
| `O.AppearanceTab`, `O.AppearanceRows`, `O.SkinPicker` | new | — | owner defaults to the descriptor's `addonName`. |
| `Skin:PaintAce` / `Skin:PaintAceTree` | new, `settings/UnitPanel.lua`, `settings/Profiles.lua` | — | pass `"AbsorbTracker"` (through a SkinSetup helper, as LootHistory's `NS.SkinPaintAce`). |

Not called and not owed: `Core.ApplySkin`, `MakeCloseButton`, the copy window (the console opens it),
`TestStrip`, `Sim`, `LineChart`, `ReorderList`, `Autocomplete`, the dropdown menu, `Toast`. The Launcher
major takes no owner.

## 3. HUD style settings (O2's one-time R3 reset)

All per unit, under `profile.units.<player|target|focus>.` (`defaults/Profile.lua:333-372`). A mirrored
target/focus reads the player's values through `NS.Units.Get` (`core/Units.lua`), so a companion read through
`NS.Units.Get` follows the mirror for free. The composer's companion path is the **picker's own path** plus
`FromSkin` (`LibKa0s/OptionsCompose.lua:511-529`), and its `defaults` key is the **canonical leaf** plus
`FromSkin`; AT's BorderGroup maps `borderStyle` to `border` (`settings/Appearance.lua:246`), so its
companion is stored at `units.<u>.borderFromSkin` but defaulted through `defaults.borderStyleFromSkin`.

| Key | Default | Token | How it follows the skin | Reset by R3? |
|---|---|---|---|---|
| `barTexture` | `"Blizzard Raid Bar"` (`defaults/Profile.lua:16`) | `bar.texture` (Ka0s Default `"Ka0s Default"`; the owner's Skin-tab texture override reaches it, `Token` is override-aware) | `H.BarGroup{ fromSkin = true }` -> companion `units.<u>.barTextureFromSkin`; `NS.GetBarTexture` resolves `S.Resolve("bar.texture", stored, companion)` | yes: companion true |
| `bgTexture` | `"Blizzard Raid Bar"` (`:17`) | `bar.texture` (no `bar.bgTexture` token) | hand row, no composer companion. Recommended: governed by `barTextureFromSkin` (row gets `disabledIf` that companion) (D3) | yes, through that companion |
| `border` (BorderGroup `borderStyle`) | `"Blizzard Tooltip"` (`:18`) | `bar.borderStyle` (Ka0s Default `"None"`) | `H.BorderGroup{ fromSkin = true }` -> `units.<u>.borderFromSkin` | yes |
| `borderSize` | `12` (`:19`) | `bar.borderSize` (Ka0s Default `1`) | resolved under `borderFromSkin` (D4) | yes, through that companion |
| `font` | `"Friz Quadrata TT"` (`:21`) | `hud.font` (Ka0s Default `"Ka0s Oxanium SemiBold"`) | `H.FontGroup{ fromSkin = true }` -> `units.<u>.fontFromSkin` | yes |
| `fontSize` | `12` (`:22`) | `hud.fontSize` (12) | not governed by the composer's companion; stays the player's (D4) | no |
| `fontFlags` | `"OUTLINE"` (`:23`) | `hud.outline` (`"OUTLINE"`) | stays the player's (D4) | no |
| `fontShadow` | `false` (`:27`) | none (`font.shadow` is the window body face's) | player's | no |
| `fontColor` | white (`:31`) | none for HUD text | player's (D5) | no |
| `barColor` | `{.4,.7,1,.8}` (`:37`) | none (bar fill color is the host's by `S.BarTexture`'s contract) | player's (D5) | no |
| `bgColor` | `{.2,.2,.2,.8}` (`:38`) | `bar.bg` (nil in Ka0s Default) | player's (D5) | no |
| `borderColor` | `{.5,.5,.5,1}` (`:20`) | `bar.border` (nil in Ka0s Default) | player's (D5) | no |
| `barAlpha`, `barWidth`, `barHeight` | `1`, `200`, `20` | — | geometry and opacity, not style | no |
| `useClassColor{Bar,Bg,Border,Text}` | `false` | — | meaning (rung 4, E6) | no |

The reset step (AT-03): `core/Database.lua`'s ladder gains `{ to = 6, apply = ... }` (today ends at 5,
`core/Database.lua:168-196`), walking every stored profile with the file's own `forEachProfile`, and for each
stored `units.<u>` table calls `Skin.ResetToSkin(unitTable, { "barTextureFromSkin", "borderFromSkin",
"fontFromSkin" })` (bool keys named directly are set to `true`, `LibKa0s/Skin.lua:650-670`). **Name the
companions, not the style keys**: on a string key with no companion visible `ResetToSkin` writes the
`"@skin"` sentinel into the media key (`borderStyle`/`font` would then hold a value no LSM list carries), and on
a color table it invents a row-less `<key>FromSkin`. With the library absent the step is a no-op that still
returns (the stamp advances; D2). Moves: `NS.SCHEMA_VERSION` 5 -> 6, `tests/test_database.lua:7-11, 77`, the
"stamped 5" comment in `defaults/Profile.lua:438`.

Also owed in AT-03: `NS.Units.APPEARANCE_KEYS` (`core/Units.lua`) gains the three companions so *Copy from
Player* copies them; `NS.Units.Get` already resolves the mirror. Skin switches reach the bars through
`S.OnLooksChanged(fn)` -> `NS.bus:SendMessage(NS.MSG.APPEARANCE)` (the existing repaint path,
`modules/Display.lua:493-495`), registered once in `core/SkinSetup.lua`.

## 4. Exceptions

| Id | What | Rung | Reason |
|---|---|---|---|
| E1 | `SettingsPanel` chrome around AT's pages | 3 | skinning-§7: a Blizzard shared frame; the library paints only AT's canvas. |
| E2 | `StaticPopup` `ABSORBTRACKER_RESET_ALL` (`settings/General.lua:359`) | 3 | skinning-§7: StaticPopup is never restyled. |
| E3 | `GameTooltip` frame under the drag strip's tooltips (`modules/Bar.lua:147-183`) | 3 | skinning-§7: the frame keeps Blizzard's look; the lines are the widget's, colored with its owner. |
| E4 | LibDBIcon minimap button and the launcher's GameTooltip (`core/LauncherSetup.lua:107`) | 3 | third-party button (LibDBIcon) on the minimap; `LibKa0s-Launcher-1.0` takes no owner; GameTooltip's frame is never painted. |
| E5 | `ColorPickerFrame` (the color rows) and AceGUI-3.0-SharedMediaWidgets' LSM30 pull-outs (bar/background texture, border, font rows; `settings/Appearance.lua:212`) | 3 | skinning-§7 names both. |
| E6 | Class colors on bar, background, border and text (`core/CoreSetup.lua:59-70` `RAID_CLASS_COLORS`; the darkened per-class background palette `core/Data.lua:173-232`, options-ui-§17's named exemption) | 4 | game-meaning colors: the unit's class. |
| E7 | Chat colors: `NS.PREFIX` cyan (`core/Namespace.lua:10`), the disabled line's gold (`settings/Slash.lua:35`, a pinned copy of the library's string), the mirror note's gray (`settings/Slash.lua:60`) | 3 | not a frame the addon draws; slash-commands mandates the cyan tag and the gold/white scheme verbatim (`slash-commands.md:124, 131, 266`). LootHistory left its `NS.PREFIX` literal too. |
| E8 | About-page logo (`core/Constants.lua:38`) and the TOC/launcher icon (`:54`) | 3 | addon brand art, not chrome; no skin token describes it. |

## 5. Gaps (rung 2)

**None.** Every surface composes from existing primitives and tokens: the HUD from `S.Resolve` over
`bar.texture`, `bar.borderStyle`, `bar.borderSize`, `hud.font` plus the three composer companions; the strip from
`DragHandle`'s owner; the settings pages, console and perf panel from the library's owner-aware chrome. The
colors with no token (fill, HUD text) are the host's by the library's own contract (`S.BarTexture`: "the color is
the bar's own") and stay player settings; see D5 for the one candidate that could become a collection-wide
library option if M0's consolidation finds it recurs (a `fromSkin` companion for HUD color rows).

## 6. Doubtful calls (for DECISIONS.md)

- **D1. The R3 reset changes the bars' look on Ka0s Default.** After AT-03 a player on the default skin sees the
  `Ka0s Default` bar texture (not Blizzard Raid Bar), no border (`bar.borderStyle "None"`, size 1, not Blizzard
  Tooltip 12) and Oxanium SemiBold (not Friz Quadrata). That is O2 and v1.79.0's "Ka0s Default looks different"
  working as ruled, not a Ka0s Default regression, but it is the one visible change, and the plan says to stop
  only for a Ka0s Default change. **Recommend:** proceed under O2; say so in the smoke checks and the CHANGELOG.
- **D2. The companions' defaults for new and reset profiles.** The composer emits companions with
  `default = false` (`LibKa0s/OptionsCompose.lua:516`); `spec.defaults[<leaf>FromSkin]` overrides it
  (`:238`). With `false`, a new profile or *Reset all settings* would bring back the pre-skin look while existing
  profiles follow the skin. **Recommend:** default `true` in `defaults/Profile.lua` and in each composer's
  `defaults` (`barTextureFromSkin`, `borderStyleFromSkin`, `fontFromSkin`), so every profile, old, new or reset,
  follows the skin until the player unticks; keep the v6 `ResetToSkin` step anyway as skinning-§6's explicit,
  testable record (it then mostly confirms the default).
- **D3. The background texture.** No `bar.bgTexture` token, and the row is hand-written (no composer companion).
  **Recommend:** let `barTextureFromSkin` govern both textures (background drawn with `bar.texture`, tinted by
  the player's `bgColor`), the `bgTexture` row `disabledIf` that companion. Alternative: a host bool row
  `bgTextureFromSkin`. Not a library gap either way.
- **D4. Which numbers follow the companions.** `fontFromSkin` governs the face only (composer contract), and
  `hud.fontSize`/`hud.outline` equal AT's defaults in Ka0s Default. `borderFromSkin` disables only the style
  picker, yet a skin's `"None"` with the player's size 12 would leave a 3 px empty inset. **Recommend:** resolve
  `borderSize` from `bar.borderSize` while `borderFromSkin` is on (the slider stays enabled but inert, and its
  tooltip says so), and leave font size and outline to the player.
- **D5. HUD colors (fill, background, border, text).** Ka0s Default sets `bar.bg` and `bar.border` to nil
  ("leave the host's") and has no fill or HUD-text token; the composer has no color companion; `ResetToSkin` on
  a color key writes a row-less `<key>FromSkin`. **Recommend:** the four colors stay the player's and are not
  reset. If the consolidation shows other HUD addons (KickCD, MultiMeters, PartyFrameEnhanced) want skin-driven
  HUD colors, raise one LibKa0s option then (a composer `fromSkin` companion for the bar block's color rows reading
  `bar.bg`/`bar.border`), not per addon.
- **D6. The picker's eye.** AT has no Test mode; its preview is unlocking, which is a stored write
  (`locked`), not a transient preview, and the player bar is normally already on screen. **Recommend:** omit
  `onPreview` (the eye is hidden) and declare only `settings` among the picker's icons; or, if the owner wants
  the eye everywhere, make it paint `NS.PaintPlaceholder` on the shown bars without touching `locked`.
- **D7. The value text's drop shadow.** `SetShadowColor(0,0,0,1)` / `(1,-1)` (`modules/Display.lua:224-230`)
  is a literal on an addon frame, but it is the font block's on/off shadow, not chrome. **Recommend:** keep it as
  a named local constant beside `fontShadow` and note it in the anti-pattern #107 review as the font row's own
  rendering, not a skin color.
- **D8. The debug ON/OFF chat colors** (`core/DebugLogSetup.lua:65`, `40ff40` / `ff4040`) equal
  `sem.goodAlt` / `sem.badAlt` byte for byte in Ka0s Default (`LibKa0s/SkinDefs.lua`, LootHistory's
  `LedgerFormat.lua:12, 46-48` precedent), so they could follow the skin with no Ka0s Default change.
  **Recommend:** leave them literal with the rest of the chat (E7); chat is not a skinned surface.
- **D9. When the picker shows.** **Recommend:** at `OnEnable` / `PLAYER_LOGIN` when `skin.pickerSeen` is false
  and the addon is not stood down (`NS.IsStoodDown()`), `page = "general"`, `tab` left to its `"Appearance"`
  default, `onClose` writes `skin.pickerSeen = true` through `NS.SetByPath`; the library's queue handles combat
  and other addons' pickers.
- **D10. Two "Appearance" names.** AT already has an *Appearance* page (the bar look) and the library's tab
  key is `"Appearance"`, labeled **Skin** since OptionsAppearance minor 3. No clash in what the player reads.
  **Recommend:** no rename; the docs say "the Skin tab on General" and "the Appearance page".

## 7. Re-vendor v1.77.0 -> v1.79.0 obligations (AT-RV)

- Re-vendor the whole `libs/LibKa0s/` and `tests/_kit/` from the tag (`git archive`): new files arrive with
  their shells (`WidgetsCopyWindow.lua`, `DebugLogWindow.lua`, `OptionsAppearance.lua`, `SkinAce.lua`, the
  Skin major's files, `Toast.lua`, `OptionsSkinPicker.lua`), plus fonts (five skin faces, Oxanium) and textures
  (two Glass textures, the eight bars). `tests/run.lua`, `tests/perf.lua` and the suites derive the library
  list from `libs/LibKa0s/LibKa0s.xml` (`tests/test_loadorder.lua:148-173` pins the two together), so no hand
  list moves.
- **Options stub** (`settings/OptionsSetup.lua`, the `if not lib then` arm): add `AppearanceTab` and
  `AppearanceRows` (v1.78.0) and `SkinPicker` and `HideSkinPicker` (v1.79.0), inert
  (`AppearanceTab = function() return nil end`, `AppearanceRows = function() return nil end`,
  `SkinPicker = function() return nil end`, `HideSkinPicker = function() end`); `tests/test_surface_parity.lua:98-`
  (`Kit.assertSurfaceParity` over `LibKa0s-Options-1.0`) goes red until they are there. Add a case beside
  `tests/test_optionssetup.lua:294-305` ("the degraded stub answers LibKa0s v1.77.0's four members inert") for
  the four new ones, and the row in `docs/common-tasks.md:264` and `docs/test-cases.md:621` that names them.
- **Provenance:** `CLAUDE.md:46` `v1.77.0` -> `v1.79.0`; `tests/test_vendor_sync.lua` holds the payload to the
  tag that line names.
- **Icons line** `CLAUDE.md:47`: keep `clear, close, copy, help`; add `settings` for the picker's gear, and
  `eye` only if D6 keeps the eye. Prune `media/icons/` with the tag's `tools/prune-icons.lua`; keep the
  README's icon credits in step.
- **Ka0s Default looks different at the re-vendor** (v1.79.0): only once AT registers an owner (AT-01), so
  AT-RV alone changes nothing on screen; AT-05's smoke checks re-look at the settings pages and the bars.
- `## OptionalDeps:` gains `EllesmereUI` (skinning-§5) in AT-01; the TOC gains `core\SkinSetup.lua` with its
  load-order comment (before `modules\Bar.lua`, which builds the strips at file load), and
  `tests/test_loadorder.lua` follows.
- No test in AT pins a library minor or a library file list by hand (grep of `tests/*.lua` outside `_kit`);
  the Widgets parity case pins the members AT reaches (`DRAG_HANDLE,DragHandle`,
  `tests/test_surface_parity.lua:296-347`), which does not move.

## 8. Risks

- **R1 Taint / secure frames / combat:** none of note. The bars are plain frames (no secure template, no
  protected calls); a skin switch repaints them through the existing APPEARANCE path, safe in combat. The
  picker's queue waits out combat itself; the settings pages carry the library's combat cover.
- **R2 Do not record the fill with `S.BarTexture`.** It always paints the skin's texture (or the Skin-tab
  override) and replays on every switch, so a player who unticks *Use the skin's texture* would have the pick
  overwritten at the next skin change. Resolve in `NS.GetBarTexture` and repaint on `S.OnLooksChanged`.
- **R3 `ResetToSkin` with style keys** writes `"@skin"` into `font`/`border` and invents row-less color
  companions (section 3). Name the three companion bools only.
- **R4 Hot path:** `NS.UpdateAbsorbBar` (`modules/Display.lua:425-478`, every throttled
  `UNIT_ABSORB_AMOUNT_CHANGED`) must stay free of resolves; all skin reads belong in `NS.UpdateBarAppearance`
  (`:171-289`), which runs on APPEARANCE only.
- **R5 Pooled AceGUI:** the chrome-block widgets are released by `releaseStaleChromeWidgets`
  (`settings/UnitPanel.lua:291-297`) through `AceGUI:Release`; the library's restore rides on the widget's
  `OnRelease`, and AT sets none of its own, so the restore holds. The Profiles `SimpleGroup` is created once and
  never released: paint it with `PaintAceTree` after each `Open` (AceConfigDialog re-acquires its children).
- **R6 Load order:** `RegisterOwner` must run at file load before `modules/Bar.lua` (strip owner) and before
  `settings/` (the Options proxy is installed at `lib:New` and again at `CreateOptionsPanel`). The bars are built
  at file scope from defaults before the profile exists; the first appearance pass resolves against the
  profile, so the build-time values only need to be non-literal.
- **R7 EllesmereUI source:** under `skin.source = "eui"` the HUD reads `Token(owner, ...)`; verify in-client what
  `bar.texture`/`hud.font` resolve to under the EUI provider (it paints the Ka0s extras from EllesmereUI's accent,
  panel and font) and add a smoke check.
- **R8 Test churn:** `tests/test_data.lua:153-160, 401` and `tests/test_display.lua` exercise the media getters
  with the stored keys; with companions defaulting to true (D2) those cases need the companion set false, or a
  new case each for the skin path. `tests/test_schema.lua` (1069 lines) and `tests/test_widgets.lua` (1073) grow
  with the new rows; still under the 1500-line cap.
- **R9 File cap:** no authored file is near 1500 lines (largest: `settings/Slash.lua` 831,
  `settings/Schema.lua` 553, `modules/Display.lua` 502). New `core/SkinSetup.lua` should stay small (LootHistory's
  is 631, mostly its fallback token table, which AT does not need: AT draws no window chrome of its own).

## 9. Effort

**L.** The windows are all the library's, so AT-02 is small, but AT-03 is a real HUD adoption, the first with all
three composer companions: the getters, the v6 migration, the mirror and copy keys, the bg-texture and border-size
calls, and test churn in the media and display suites. AT-01, AT-04 and AT-RV are routine after LootHistory.
