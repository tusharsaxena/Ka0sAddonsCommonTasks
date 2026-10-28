# Inventory: KickCD (prefix KC)

Read-only M0 inventory of `../KickCD` at `master` (vendors LibKa0s v1.77.0, `CLAUDE.md:44`;
`LibKa0s icons: clear, close, confirm, copy, help, info, segment`, `CLAUDE.md:45`). Line numbers are
`master` as read on 2026-10-29. Library references are LibKa0s v1.79.0 (main checkout).

KickCD is mostly **HUD**: per unit (target, focus; focus `link = true` by default and then renders
with Target's tables) an icon grid, a cast bar and a unit label. It draws **no window of its own**.
Everything else it shows is library-drawn (settings pages, launcher, debug console, perf panel,
sim panel, drag handles, sim strip, reorder list) or a page that acquires AceGUI widgets itself.

## 1. Surfaces

### 1a. HUD (XX-03)

| # | Surface | Built | Look typed today | Rung-1 paint |
|---|---|---|---|---|
| H1 | Icon button + spell icon texture | `modules/IconGrid_Render.lua:205` (btn), icon painted `modules/IconGrid.lua:307` | Spell texture (game meaning). TexCoord zoom from `icons.zoom`. Ready tint `SetVertexColor(1,1,1)` `IconGrid_Render.lua:710,717`; cooldown tint by curve (secret) `IconGrid_Ticker.lua:85` | **None.** Spell icon is rung 4; the tint is a player setting written by a secret curve and must never be routed through a recording primitive (see Risks R1). |
| H2 | Per-icon border (BackdropTemplate child) | `IconGrid_Render.lua:222`; painted `IconGrid_Render.lua:810-818` (`ApplyAppearance`) | edgeFile = LSM border `icons.borderTexture` (default `"Blizzard Tooltip"`, `defaults/Profile.lua:67`), edgeSize `icons.borderSize` (2, `:70`), color `icons.borderColor` {0,0,0,1} (`:68`) + class-color companion | `S.Resolve("bar.borderStyle", cfg.borderTexture, cfg.borderTextureFromSkin)` then the existing LSM fetch. Size and color stay player settings (no composer companion; `icon.border` {0,0,0,1} and `bar.borderSize` 1 exist but are NOT reset, see §3 and D1/D3). Do **not** use `S.IconBorder` (flat edge only, records the pooled frame). |
| H3 | Cooldown countdown text | `IconGrid_Render.lua:275` (`NumberFontNormal`); painted `:880-898` (`ApplyTextConfig`) | Font `icons.cooldownTextFont` `"Friz Quadrata TT"` (`Profile.lua:72`), size 14, flags `OUTLINE`, color white `{1,1,1,1}`, shadow off -> `SetShadowOffset(1,-1)` + `SetShadowColor(0,0,0,1)` when on (`:894-898`) | Face through `S.Resolve("hud.font", cfg.cooldownTextFont, cfg.cooldownTextFontFromSkin)` + LSM fetch; size/flags/color/shadow stay player settings. Text itself is `SetFormattedText` on a secret duration in the ticker (`IconGrid_Ticker.lua:91`): never `S.Text` it. |
| H4 | Charges badge | `IconGrid_Render.lua:284` (`NumberFontNormal`) | Font object only, no setting | Doubtful D4: face from `S.BarStyle().font` (hud.font), size and flags kept from the font object, applied in `ApplyTextConfig` and on `OnLooksChanged`. Or left on `NumberFontNormal`. |
| H5 | Ready glow (LibCustomGlow on a host frame) | host `IconGrid_Render.lua:296`; started `:473-500` | Color `icons.primaryGlowColor` / `secondaryGlowColor` {1,1,0,1} (`Profile.lua:135,139`); degenerate fallback `0.95,0.95,0.32,1` (`:410`) | Player setting, kept (D3). `S.GlowColor()` (glow.color) exists if the owner later wants a follow-skin companion; no composer row for it today. |
| H6 | Cooldown swipe | `IconGrid_Render.lua:231` (`CooldownFrameTemplate`) | Blizzard template art | Untouched (rung 3, Blizzard template). |
| H7 | Cast bar root + two backgrounds | `modules/Castbar_Frame.lua:220-247` (root `KickCDCastbar` / `KickCDCastbarFocus`, bg textures `:245-248`); painted `modules/Castbar_Skin.lua:400-403` | `SetColorTexture(bgColor)` per state, default {0,0,0,0.5} (`Profile.lua:267,287`) + class companion | Player color, kept. Equals `bar.bg` {0,0,0,0.5} exactly, so a later follow-skin companion would be pixel-neutral on Ka0s Default (D3). |
| H8 | Two stacked StatusBars (int / unint) | `Castbar_Frame.lua:256-263`; painted `Castbar_Skin.lua:408-415` | Texture `castbar.(un)interruptible.statusBarTexture` `"Blizzard Raid Bar"` (`Profile.lua:258,278`); color yellow {1,0.85,0.05,1} / red {0.85,0.10,0.10,1}; alpha via secret curve | Texture through `S.Resolve("bar.texture", sc.statusBarTexture, sc.statusBarTextureFromSkin)` + `Castbar.FetchStatusBarTexture`. **Not** `S.BarTexture`: it records the bar and re-applies the skin texture on every switch, overriding a player pick, and reads the live tint. Bar colors are meaning (rung 4, E4). |
| H9 | Spark | `Castbar_Frame.lua:286-289` | `Interface\CastingBar\UI-CastingBar-Spark`, ADD blend | Untouched in-client art (D6). |
| H10 | Cast bar spell icon | `Castbar_Frame.lua:292`, `Castbar.lua:446,732` | Spell texture / question mark | Rung 4. |
| H11 | Name + time text | `Castbar_Frame.lua:298,302`; font `Castbar_Skin.lua:291-314`; colors `Castbar.lua:574,616` (name, via secret curve), `Castbar_Skin.lua:420` (time) | Font `castbar.font` `"Friz Quadrata TT"` (`Profile.lua:183`), size 10, `OUTLINE`, shadow off; name color per state white, time color white | Face through `S.Resolve("hud.font", c.font, c.fontFromSkin)`; colors stay player settings. Never `S.Text` (the name color is written by `C_CurveUtil` on a secret bool, Risks R1). |
| H12 | Two cast-bar borders (BackdropTemplate) | `Castbar_Frame.lua:318-319`; painted `Castbar_Skin.lua:91-106` | edgeFile `castbar.(un)interruptible.borderTexture` `"Blizzard Tooltip"` (`Profile.lua:272,292`), size 2, color black | `S.Resolve("bar.borderStyle", sc.borderTexture, sc.borderTextureFromSkin)`; size/color player settings (D1). |
| H13 | Unit label | `modules/UnitLabel.lua:165-169` (`KickCDUnitLabelTarget/Focus`, `GameFontNormal`); font `:89-105`; color `:118-124` | Font `label.style.font` `"Friz Quadrata TT"` (`Profile.lua:311`), size 14, `OUTLINE`, gold {1,0.82,0,1} (`:315`), shadow off | Face through `S.Resolve("hud.font", style.font, style.fontFromSkin)`. Color is a player setting (gold equals `text.accent`, not reset). |
| H14 | Drag handles (grid, cast bar) | `modules/IconGrid_Handle.lua:131-150`, `modules/Castbar_Handle.lua:91-110` | Library `KW.DragHandle`, no owner | Hand `owner = addonName` (§2). |
| H15 | Simulation strip | `modules/SimStrip.lua:65-69` | Library `W.TestStrip(kind="sim")`, no owner | Hand `owner = addonName` (§2); amber/cyan stay meaning (skinning-§7). |

### 1b. Settings pages (XX-02 / XX-04)

All pages are LibKa0s-Options pages; the descriptor already names the folder (`settings/OptionsSetup.lua:157`,
`addonName = addonName`), so once the owner is registered the library chrome (header, tabs, nav rail,
drawers, every `O.*` row and the `O.AceGUI` proxy) follows the skin with no host code. Host-acquired
AceGUI widgets:

| # | Surface | Built | Today | Rung-1 paint |
|---|---|---|---|---|
| P1 | Units band: Copy from Target button, Unit dropdown, host SimpleGroup | `settings/Panel_Render.lua:113,136,169` | `AceGUI = Helpers.AceGUI or NS.AceGUI` (`:164`) | Painted by the `O.AceGUI` proxy once registered (Options minor 34 wraps `O.AceGUI`). Verify `NS.AceGUI` (`OptionsSetup.lua:261`, the `onAceGUI` callback) receives the proxied table; if not, `Skin:PaintAce(owner, w)`. |
| P2 | Linked-Focus inert strip | `Panel_Render.lua:265-296` (`deadenStrip`) | `SetDesaturated(true)` on every region of the library's tab buttons | Unchanged; see Risks R6 (desaturates the skin's tab fills too). |
| P3 | Spells page rows: remove button, spell icon, name label, enable checkbox, known glyph, spacer, category dropdown, row group | `settings/Spells_Rows.lua:76,117,145,163,191,221,228,282` | Raw `LibStub("AceGUI-3.0")` (`settings/Spells.lua:647`) | Switch to `H.AceGUI` (proxy) or `Skin:PaintAce(owner, w)` per widget; any host `OnRelease` through `Skin:OnRelease`. |
| P4 | Remove-mark tint | `Spells_Rows.lua:249` `REMOVE_TINT = {1,0.3,0.3}`; disabled tint `0.45,0.45,0.45` `:89` | Typed | `close.hot` (Ka0s Default `{1,0.3,0.3,1}`, exact). Disabled arm is unreachable (no caller passes `disabled`), see D7. |
| P5 | Known / not-known glyph | `Spells_Rows.lua:36-37,193` | `Interface\RaidFrame\ReadyCheck-Ready/NotReady` | Rung 4 (ready-check meaning, Blizzard art). |
| P6 | "not tracked" tag | `settings/Spells.lua:411` `"|cffff8000"` | Typed escape | `sem.warn` (Ka0s Default `{1,0.5,0,1}` = ff8000, exact) as an escape built from `S.Color`. |
| P7 | Spells header: class/spec dropdown, add host group | `settings/Spells_Header.lua:160,196` | Raw AceGUI handed from Spells; labels carry `RAID_CLASS_COLORS` escapes `:56-64,118-122` and class/spec icon markup | Paint the two widgets (as P3); class colors and icons rung 4. `H.IdInput` (`:228`) is library-drawn. |
| P8 | Spells reorder list | `settings/Spells.lua:595-600` | `W.ReorderList{...}`, no owner | Hand `owner = addonName` (§2). |
| P9 | AceGUI-missing fallback label | `settings/Spells.lua:521-525` | `GameFontNormal` (gold) FontString | `S.Text(fs, "accent")` (gold, Ka0s Default exact) or leave: degraded-only (D8). |
| P10 | Profiles page (AceDBOptions via AceConfigDialog into a SimpleGroup) | `settings/Profiles.lua:22,47` | Raw AceGUI; AceConfigDialog acquires the rows | `Skin:PaintAceTree(owner, container)` after `Open`, as LootHistory does (`LootHistory/settings/Profiles.lua:69`). |
| P11 | General page | `settings/General.lua:324` (`RenderTabbedSchema`, Master controls only, no Keybindings tab) | Library | Add the Appearance tab: `opts.tabs = { H.AppearanceTab(spec) }` (no Keybindings tab, so last). Tab count becomes 2. |
| P12 | Spell / icon tooltips | `IconGrid_Render.lua:314-332`, `Spells_Rows.lua:100-103,128-131,205-208` | `GameTooltip:SetSpellByID` (Blizzard content), `GameTooltip:SetText(str)` with no color | `SetSpellByID` untouched. The two `SetText` lines take a skin color (`gtip.title` or `gtip.value`): D5 decides which matches the client default. |

### 1c. Tool surfaces (XX-04)

| # | Surface | Where | Owner today | Action |
|---|---|---|---|---|
| T1 | Debug console + copy window | `core/DebugLogSetup.lua:168-181` | `name = addonName`, `addonName = addonName` | None beyond registering: the console takes its owner from `addonName` (DebugLog 22.4.1.1). Its `font = Const.FONT_MONO` (`:195`) stays (the window reads `d.font`). |
| T2 | Perf panel | `core/PerfSetup.lua:62-73` | `name`/`addonName = addonName` | None beyond registering. |
| T3 | Sim panel | `modules/Sim.lua:345-346` | `name = "KickCD"` (literal) | Works (equals the folder); prefer `addonName` (D9). |
| T4 | Close control | `core/CoreSetup.lua:247-249` | `lib.MakeCloseButton(parent, onClick, addonName)` | Already owner-aware; no current caller. |
| T5 | Launcher + minimap button + status tooltip | `core/LauncherSetup.lua:100-170` | Library-drawn, LibDBIcon button | Untouched (E2). |
| T6 | Chat printer prefix / gray lines | `core/Constants.lua:22,28`, `core/KickCD.lua:920`, `settings/Panel_Widgets.lua:58`, `settings/Slash.lua:553` | `|cff00ffff[KCD]|r`, `|cff9d9d9d`, `|cff33ff99` | Chat output, not a drawn surface (E5, D10). |
| T7 | First-run picker | new | - | `O.SkinPicker` while `skin.pickerSeen` is false (O3), as LootHistory `core/SkinSetup.lua` `NS.MaybeShowSkinPicker` / `NS.HideSkinPicker`; HideSkinPicker in the stand-down (`core/LifecycleSetup.lua:118`) and first on every profile event. |

## 2. Library factories that take an owner

| Call | File:line | Hand it |
|---|---|---|
| `KW.DragHandle(grid, spec)` | `modules/IconGrid_Handle.lua:133` | `spec.owner = addonName` (WidgetsDragHandle minor 6) |
| `KW.DragHandle(frame, spec)` | `modules/Castbar_Handle.lua:92` | `spec.owner = addonName` |
| `W.TestStrip(UIParent, opts)` | `modules/SimStrip.lua:65` | `opts.owner = addonName` |
| `W.ReorderList{...}` | `settings/Spells.lua:597` | `owner = addonName` |
| `lib.MakeCloseButton` | `core/CoreSetup.lua:248` | already passes `addonName` |
| DebugLog / Perf / Sim descriptors | `core/DebugLogSetup.lua:168`, `core/PerfSetup.lua:62`, `modules/Sim.lua:345` | already carry the folder (`addonName` / `name`) |
| Options descriptor | `settings/OptionsSetup.lua:157` | already `addonName = addonName`; `H.IdInput` (`Spells_Header.lua:228`) follows it |
| `Skin:PaintAce` / `PaintAceTree` / `OnRelease` | Spells rows/header, Profiles | `owner = addonName` (host-acquired AceGUI) |

No Widgets dropdown, search box, copy window, autocomplete or line chart is called by host code.

## 3. HUD style settings (O2, the one-time R3 reset)

Every row below exists per unit, `units.target.*` and `units.focus.*` (8 picker rows per unit, 16 in
all). The composer's `fromSkin = true` on the existing `H.FontGroup` / `H.BorderGroup` /
`H.BarGroup` calls emits a `<pickerPath>FromSkin` bool (OptionsCompose minor 12,
`OptionsCompose.lua:511-532`); its default is overridable through `spec.defaults.<leaf>FromSkin`.
The host draws with `S.Resolve(token, stored, companion)`. `Skin.ResetToSkin(profile, keys)` sets
each listed key's existing `FromSkin` companion to true.

| Setting | Schema key (per unit) | Default (`defaults/Profile.lua`) | Composer call | Companion | Token (Ka0s Default v1.79.0) |
|---|---|---|---|---|---|
| Icon border style | `units.<u>.icons.borderTexture` | `"Blizzard Tooltip"` (`:67`) | `settings/Icons.lua:242` BorderGroup | `...icons.borderTextureFromSkin` | `bar.borderStyle` = `"None"` (**D1**) |
| Icon countdown font | `units.<u>.icons.cooldownTextFont` | `"Friz Quadrata TT"` (`:72`) | `Icons.lua:291` FontGroup | `...icons.cooldownTextFontFromSkin` | `hud.font` = `"Ka0s Oxanium SemiBold"` |
| Cast bar font (both texts) | `units.<u>.castbar.font` | `"Friz Quadrata TT"` (`:183`) | `settings/Castbar.lua:479` FontGroup | `...castbar.fontFromSkin` | `hud.font` |
| Interruptible bar texture | `units.<u>.castbar.interruptible.statusBarTexture` | `"Blizzard Raid Bar"` (`:258`) | `Castbar.lua:536` BarGroup | `...interruptible.statusBarTextureFromSkin` | `bar.texture` = `"Ka0s Default"` |
| Interruptible border style | `units.<u>.castbar.interruptible.borderTexture` | `"Blizzard Tooltip"` (`:272`) | `Castbar.lua:558` BorderGroup | `...interruptible.borderTextureFromSkin` | `bar.borderStyle` = `"None"` (**D1**) |
| Non-interruptible bar texture | `units.<u>.castbar.uninterruptible.statusBarTexture` | `"Blizzard Raid Bar"` (`:278`) | `Castbar.lua:569` BarGroup | `...uninterruptible.statusBarTextureFromSkin` | `bar.texture` |
| Non-interruptible border style | `units.<u>.castbar.uninterruptible.borderTexture` | `"Blizzard Tooltip"` (`:292`) | `Castbar.lua:591` BorderGroup | `...uninterruptible.borderTextureFromSkin` | `bar.borderStyle` (**D1**) |
| Label font | `units.<u>.label.style.font` | `"Friz Quadrata TT"` (`:311`) | `settings/Label.lua:199` FontGroup | `...label.style.fontFromSkin` | `hud.font` |

HUD style values with **no** composer companion, kept as player settings and **not** in the reset
(recommendation D3): sizes (`cooldownTextSize` 14, `castbar.fontSize` 10, `label.style.size` 14,
`borderSize` 2), flags (`OUTLINE`), shadows, text colors, border colors ({0,0,0,1}), cast-bar
backgrounds ({0,0,0,0.5}), glow colors ({1,1,0,1}) and the label's gold.

Wiring notes for the implementer:

- **Defaults.** Each companion needs a default in `defaults/Profile.lua` (the only place a default
  is typed, savedvariables-§2) inside `ICONS_DEFAULT`, `CASTBAR_DEFAULT` (and its two state tables)
  and `LABELSTYLE_DEFAULT`, matching the composer row's default (D2).
- **The reset is per profile, not stamp-gated.** KickCD's runner is account-wide
  (`db.global.schemaVersion`, `core/Database_Migrations.lua:356-393`, `NS.SCHEMA_VERSION = 5`,
  `core/Database.lua:39`), and its own history (KICKCD-R-01, `core/Database.lua:668`, `:742`) is that a
  stamp-gated step converts only the active profile. The reset therefore needs a per-profile marker
  (for example `skin.hudReset`, false by default) checked in a step run from both `MigrateProfile`
  and `Database:OnProfileChanged` (`core/Database.lua:644-688`), like `MigrateColorShape`. Bump
  `NS.SCHEMA_VERSION` to 6 with `migrations[5]` for the account-level half.
- **Focus link.** A linked Focus renders with Target's tables (`NS.Units.*`), so Focus's companions
  are inert while linked, exactly like its pickers; reset both units anyway. `NS.Units.CopyStyling`
  (Copy from Target, `Panel_Render.lua:122`) must copy the companions with the pickers.
- **Repaint.** Subscribe to `NS.Skin.OnLooksChanged` and re-run the existing config path (grid
  `Layout` -> `ApplyAppearance` / `ApplyTextConfig`, `Castbar:Reskin`, `UnitLabel:Apply`), so a skin
  switch or a font/texture override reaches the HUD. Resolve only there, never in the 0.1 s ticker.

## 4. Exceptions

| Id | Rung | What | Reason |
|---|---|---|---|
| E1 | 3 | `CooldownFrameTemplate` swipe on each icon (`IconGrid_Render.lua:231`) | Blizzard template art; a skin never restyles it. |
| E2 | 3 | Launcher minimap button and broker display (LibDBIcon, `core/LauncherSetup.lua`), the status tooltip's frame | Third-party / shared frames; the library draws the tooltip lines. |
| E3 | 3 | `GameTooltip` frame and its `SetSpellByID` content (`IconGrid_Render.lua:320`, `Spells_Rows.lua:130`) | skinning-§7: GameTooltip itself is never skinned; spell tooltip content is Blizzard's. |
| E4 | 4 | Cast-bar fill colors yellow {1,0.85,0.05} / red {0.85,0.10,0.10} (`Profile.lua:259,279`) | Interruptible vs not is the bar's meaning; player swatch with class companion. |
| E5 | 4 | Spell icons (grid `IconGrid.lua:307`, cast bar `Castbar.lua:446`, Spells rows `Spells_Rows.lua:118`) | Game content. |
| E6 | 4 | Class colors and class/spec icon markup in the spec dropdown (`Spells_Header.lua:56-72,118-122`) and every `useClassColor*` companion (`NS.ResolveColor`) | Class color is meaning. |
| E7 | 4 | Ready-check glyphs (`Spells_Rows.lua:36-37`) | Ready / not ready meaning, Blizzard art. |
| E8 | 4 | Cooldown tint {1,0.4,0.4} and ready/cooldown alphas (`Profile.lua:50`), applied through secret curves | State meaning (on cooldown), player setting; secret-value path. |
| E9 | 4 | Sim strip amber/cyan (library `strip.*`) | skinning-§7: meaning colors, the skin changes legibility only. |
| E10 | - | Chat output: `[KCD]` cyan prefix and gray lines (T6) | Not a drawn surface; the prefix is the collection's chat convention (D10). |

## 5. Gaps (rung 2)

**None.** Every surface KickCD draws is painted by an existing primitive or token, or is a
player-set HUD value resolved through `S.Resolve` with the composer's three companions. The near
misses, and why none is a gap:

- *An icon/castbar border style token separate from `bar.borderStyle`.* `bar.borderStyle` and
  `bar.borderSize` are the schema's HUD border tokens and the composer's border companion is bound to
  `bar.borderStyle` for every `BorderGroup`; KickCD's icon and cast-bar borders are the same kind of
  LSM edge. The problem is the **value** Ka0s Default carries (`"None"`), not a missing name: that is
  D1, a consolidation-level ruling, not a new token.
- *A HUD text size/outline companion.* The composer follows only the face; sizes and flags stay
  player values, so nothing needs `hud.fontSize` / `hud.outline` here.
- *The 0.45 gray disabled tint* (`Spells_Rows.lua:89`): unreachable code (D7), so no token is owed.
- *The cast-bar spark*: in-client art with ADD blend, no color to skin (D6).

## 6. Doubtful calls (for DECISIONS.md)

- **D1 (stop-and-ask: alters Ka0s Default today).** Ka0s Default's `bar.borderStyle` is `"None"`
  (`LibKa0s/SkinDefs.lua:299`). KickCD's three border pickers default to `"Blizzard Tooltip"` at 2 px.
  If the R3 reset puts them on the skin, **every KickCD icon and cast-bar border disappears on Ka0s
  Default**, which is a visible regression, not a face swap. Recommendation: add the "Use the skin's
  border" companion (`fromSkin` on the three BorderGroups) but **leave the border companions out of
  the reset and default them false**, so borders keep their stored style until the player opts in.
  The fonts and bar textures do take the reset. Alternative for the consolidator: if several addons
  hit the same wall, rule whether Ka0s Default's `bar.borderStyle` should move off `"None"` (a library
  minor that touches every adopter).
- **D2. Companion default for new profiles.** Recommend `true` for the five font and texture
  companions (a new profile follows the skin, R3's "unless the player has set it") and `false` for the
  three border companions (D1). Set through `spec.defaults.<leaf>FromSkin` and mirrored in
  `defaults/Profile.lua`. The reset marker still runs for every existing profile.
- **D3. Scope of the reset.** Only the eight picker keys per unit in §3 are reset. Colors (border,
  background, glow, text, label gold), sizes, flags and shadows have no composer companion and are
  player palette choices, so they stay. Recommend keeping it that way; a color companion would need
  hand-declared rows and changes `icon.border`/`bar.bg`-equal values to nothing visible on Ka0s
  Default anyway.
- **D4. Charges badge face.** It has no setting and draws `NumberFontNormal`. Recommend it follows
  `hud.font` (face only, size and flags read from the font object), so a skin reaches all HUD text;
  this changes the badge to Oxanium on Ka0s Default, in line with v1.79.0's accepted face change.
- **D5. Tooltip line color.** `GameTooltip:SetText(str)` with no color in `Spells_Rows.lua:102,207`.
  Recommend passing the skin token that equals the client's default for that call (verify in client:
  `gtip.title` gold if the default is NORMAL_FONT_COLOR, `gtip.value` white if HIGHLIGHT), so Ka0s
  Default is pixel-identical.
- **D6. Spark.** Keep `UI-CastingBar-Spark` untouched under every skin (no token describes it).
- **D7. Dead disabled arm** in `makeRowIconBtn` (`Spells_Rows.lua:86-90`): no caller passes
  `disabled`. Recommend deleting the arm rather than inventing a 0.45 token.
- **D8. AceGUI-missing label** (`Spells.lua:523`): recommend `S.Text(fs, "accent")` (gold, exact on
  Ka0s Default); the degraded facade answers the same.
- **D9. Sim descriptor name** literal `"KickCD"` (`modules/Sim.lua:346`): recommend `addonName`, so the
  owner and the folder cannot drift.
- **D10. Chat colors** (`NS.PREFIX` cyan, `NS.GRAY`, `|cff33ff99` list header): recommend exempt as
  chat output (E10). If the consolidator rules chat in scope, `NS.GRAY` maps to `q.poor`-like gray with
  no exact token (`text.muted` is 0.7), which would then be a gap.
- **D11. `deadenStrip`** desaturates the library's tab regions on a linked Focus; under a skin it also
  grays the skin's tab fills. Recommend keep (inert must read inert), and re-look in the smoke.

## 7. Re-vendor v1.77.0 -> v1.79.0 obligations (KC-RV)

- **Options stub** (`settings/OptionsSetup.lua:395-420`): add `AppearanceTab`, `AppearanceRows`
  (v1.78.0, OptionsAppearance minor 1) and `SkinPicker`, `HideSkinPicker` (v1.79.0, OptionsSkinPicker
  minor 1). `AppearanceTab` must answer a tab-shaped value or nil consistently with how General's
  renderer calls it (LootHistory `settings/OptionsSetup.lua:145-153`); `SkinPicker` answers nil.
  `tests/test_surface_parity.lua` is red until they exist.
- **Options file-count pin**: `tests/test_options_panel.lua:576-578`
  (`assertEqual(scanned, 12, "...twelve files at LibKa0s v1.77.0...")`) moves to **14**
  (OptionsAppearance.lua, OptionsSkinPicker.lua).
- **Surface parity**: a `core/SkinSetup.lua` seam adds a seventeenth major with a degradation stub;
  `tests/test_surface_parity.lua:4-14` lists the stubbed seams and gains a Skin case
  (`NS.Skin`, plus whatever helper members the seam publishes).
- **Harness**: `tests/run.lua:53` derives the library list from `LibKa0s.xml`, so the new files
  (`Skin*.lua`, `Toast.lua`, `OptionsAppearance.lua`, `OptionsSkinPicker.lua`) load with no edit.
  `tests/test_coresetup.lua:29` (majors loaded) should be re-read.
- **Whole-folder copy** from the tag (`git archive`), including `media/fonts/` (Oxanium SemiBold/Bold
  + OFL, the skins' families) and `media/textures/` (eight bars); `tests/test_vendor_sync.lua` pins the
  tag; `tests/test_constants.lua:170-198` checks the vendored fonts folder (still JetBrains Mono, re-run).
- **CLAUDE.md** provenance line `CLAUDE.md:44` -> `v1.79.0`; icons line `CLAUDE.md:45` gains **`eye`**
  and **`settings`** (the picker draws them), then the prune (`tools/prune-icons.lua`).
  `tests/test_mediasetup.lua:22-153` reads the declaration.
- **TOC**: `## OptionalDeps` (`KickCD.toc:8`) gains `EllesmereUI` (skinning-§5); the TOC load list
  gains `core\SkinSetup.lua` after `core\CoreSetup.lua` and before any module that builds a frame.
- **Ka0s Default looks different at the re-vendor** only for a registered owner; KickCD's HUD reads its
  own stored LSM keys, so before XX-03 nothing changes on screen.
- **README** font credits (Oxanium and the skin families, OFL) and the badge (XX-05).

## 8. Risks

- **R1 Secret values.** The icon tint (`IconGrid_Ticker.lua:85`), icon alpha, cast-bar alphas and the
  spell-name color (`Castbar.lua:574-620`) are written from `C_CurveUtil` results that can be secret.
  No recording primitive may own those regions: `S.BarTexture` reads the live tint and compares it
  (`SkinPaintExtras.lua:248-275`), `S.Text` rewrites the color on repaint. HUD paint goes through
  `S.Resolve` in the config path only.
- **R2 Pooled icons.** Icons come from LibKa0s-Pool (`core/PoolSetup.lua`); a primitive that records
  a pooled button would follow it into the next spell. Resolve, do not record (or `Skin:Untrack` on
  release).
- **R3 Pooled AceGUI.** Spells rows, header and Profiles use raw `LibStub("AceGUI-3.0")`; painting
  them needs the `OnRelease` restore chain (`Skin:OnRelease`), and the page's own release paths
  (`Spells.lua:500-512`) must stay intact.
- **R4 Combat.** All HUD frames are plain, non-secure frames (`Castbar_Frame.lua:220`,
  `UnitLabel.lua:166`), so a live repaint in combat is legal; the Appearance tab already refuses
  picks in combat. The picker defers to `PLAYER_REGEN_ENABLED`.
- **R5 Perf.** `Icon:Apply` runs on every SPELL_STATE and the ticker at 10 Hz; any `S.*` call there is
  a regression. Keep token reads in `ApplyAppearance` / `ApplyTextConfig` / `Reskin`.
- **R6** `deadenStrip` (D11).
- **R7 Ka0s Default change** (D1, D2, D4): the smoke must re-look at every HUD piece on Ka0s Default.
- **R8 Test churn.** 28 test lines pin `"Friz Quadrata TT"` / `"Blizzard Raid Bar"` /
  `"Blizzard Tooltip"`; stored defaults do not move, but any test that reads the rendered path under
  a default profile changes once companions default true. `tests/test_schema.lua` (1016 lines) and the
  schema-vs-defaults pins gain 16 rows.
- **File cap.** No authored file is near 1500 lines (largest: `modules/IconGrid.lua` 1013,
  `tests/test_schema.lua` 1016, `modules/Castbar.lua` 972, `core/KickCD.lua` 958,
  `settings/Spells.lua` 948, `modules/IconGrid_Render.lua` 939).

## 9. Effort

**L**: no windows, but 16 per-unit HUD companions across three HUD modules and the Focus link, a
per-profile reset outside KickCD's account-wide runner, raw AceGUI on the Spells and Profiles pages,
the picker, and a stop-and-ask on the borders (D1).
