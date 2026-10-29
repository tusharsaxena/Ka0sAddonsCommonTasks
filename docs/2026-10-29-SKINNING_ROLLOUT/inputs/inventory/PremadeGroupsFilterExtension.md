# Inventory: PremadeGroupsFilterExtension (prefix PG)

Read-only inventory for M0 of `docs/2026-10-29-SKINNING_ROLLOUT/00_PLAN.md`, taken 2026-10-29 at the repo's
`master` content (checkout on branch `feat/2026-10-29-skinning-rollout`, clean, nothing committed on it yet). The
addon vendors LibKa0s v1.77.0 (`CLAUDE.md` provenance line, `LibKa0s icons: clear, close, copy.`). Reference
library state: LibKa0s main at `4e1ae41` (v1.79.0; Skin 6.14.10.4.8.1.3, Options 34.4.35.4.6.10.3.12.8.3.2.5.3.1).

Paths below are relative to `../PremadeGroupsFilterExtension/` unless they name another repo.

## 0. What this addon draws, in one paragraph

PGFE draws **one window of its own**: the filter panel attached under Premade Groups Filter's dialog
(`modules/Panel.lua`). Today it is deliberately **Blizzard/PGF chrome**, not the Ka0s window edge: a
`PortraitFrameTemplateMinimizable` with the `ButtonFrameTemplateNoPortraitMinimizable` border, stock
`UICheckButtonTemplate`, `InputBoxTemplate`, `WowStyle1DropdownTemplate` and `UIPanelButtonTemplate` controls and
`GameFont*` font objects, so the panel reads as part of PGF's metal dialog. That look is a **ratified deviation**
(`docs/ARCHITECTURE.md:473`, standalone-windows / library-stack-§8 / options-ui-§15, owner 2026-10-10). The
optional EllesmereUI skin (`core/EUIBridge.lua` + `modules/EUISkin.lua`, 591 lines) repaints that panel through
EllesmereUI's facade. Everything else it shows is library-drawn (settings pages, debug console and its copy window,
launcher/minimap) or Blizzard's (StaticPopups, GameTooltip, Blizzard_Menu menus, the Group Finder rows it tags).
**No HUD, no test mode, no sim, no perf panel** (performance-§12 exemption).

## 1. Surfaces

Token names are from `LibKa0s/SkinDefs.lua`'s schema (`docs/api/Skin/version-6.14.10.4.8.1.3-docs.md`, *Token
reference*). "Today" is what the code types now.

### 1a. The attached filter panel (`modules/Panel.lua`)

| # | Surface | Built at | Today (colors / fonts / textures typed) | Facade primitive(s) and tokens (rung 1) |
|---|---|---|---|---|
| P1 | Panel frame (the window) | `buildFrame` `modules/Panel.lua:778-801`; `CreateFrame("Frame", FRAME_NAME, dialog, "PortraitFrameTemplateMinimizable")` :779; `f:SetBorder(BORDER_LAYOUT)` :781 (`"ButtonFrameTemplateNoPortraitMinimizable"` :31); portrait hidden :783 | Blizzard template art (NineSlice metal border, `TopTileStreaks`, template Bg); no literal colors | `S.Shell(f)` + `S.FadeNineSlice(f)` (`win.bg`, `win.border*`, `win.inner`, `title.bg*`, `title.height`, `divider`, `font.title`). See gap **PG-G1**: under Ka0s Default every one of these fades the stock art (SkinPaint minor 6) |
| P2 | Collapsed header art: two clipped copies of the border layout | `buildHeaderHalf` / `buildHeaderArt` `modules/Panel.lua:636-665` (`NineSliceUtil.ApplyLayout(slice, layout)` :654) | Blizzard NineSlice layout art; `setHeaderOnly` :667-674 swaps them with `f.NineSlice` and `TopTileStreaks` | `S.FadeRegions(slice)` per slice (the art regions live on the two `slice` frames, children of the clips: Shell's fade never reaches them, as `EUISkin.lua:275-277` notes) or hide the clips while skinned. No token (fade only) |
| P3 | Title text | `f:SetTitle(L.PANEL_TITLE)` :784, re-anchored `centerTitle` :759-765 | template `TitleContainer.TitleText` font object (Blizzard `GameFontNormal`, gold) | `S.Text(f.TitleContainer.TitleText, "title")` (`title.text`, `font.title`) or let `Shell` find it (`Shell` colors `frame.title`; the template's string is `TitleContainer.TitleText`, so pass it to `TitleBar`/`Text` explicitly) |
| P4 | Collapse / expand control | `buildMinMax` :720-729 (`MaximizeMinimizeButtonFrameTemplate`); atlases swapped `setArrowArt` :680-685: `RedButton-Expand` / `RedButton-Condense` (+`-Pressed`, `-Disabled`/`-disabled`) :726-727; template close button hidden :721 | Blizzard red-button atlases | `S.PageButton(mm.MinimizeButton, "up")` / `S.PageButton(mm.MaximizeButton, "down")` (`btn.*`, `icon.arrow`): the closest vocabulary for a collapse/expand arrow. Alternative `S.Button(b)` + `S.FadeRegions(b)` with a host glyph colored `S.Color("icon.arrow")`. Doubtful D5 |
| P5 | Header click strip | `buildHeaderClick` :736-748 | invisible Button, no art | none (no art) |
| P6 | Body container | :790-793 | plain Frame, no art | none |
| P7 | Check buttons (8: `activeCheck`, `keyTargeting`, `smartKeyLevel`, `regionsEnabled`, `playstyleEnabled`, `compositionEnabled`, `experiencedLeader`, `maxAgeEnabled`) | `checkButton` :201-210, `buildActiveRow` :265-277 (`UICheckButtonTemplate`) | Blizzard check art at 32px (`CHECK_SIZE` :45); hit rect stretched over the label :155-159 | `S.Checkbox(cb, { borderInset = 4 })` (`check.bg`, `check.border*`, `check.mark`, `check.radius`, `check.texture`, `check.markTexture`). Under a skin the 32px frame must shrink to 24 as `EUISkin.lua:78-98` does (else the box is 24px+), keeping `stretchHitRect` and the Smart label offset in step |
| P8 | Row labels | `label()` :112-119 (`font or "GameFontHighlight"`); Smart label :253 (`GameFontHighlight`); minutes :443 (`GameFontHighlight`); copy label :577 (`GameFontHighlight`) | `GameFontHighlight` = white 1,1,1, client face | `S.Text(fs, "body")` reads `text.body` 0.9 (not 1.0). Exact white is `text.highlight` (1,1,1), which no `Text` role names; compose `S.Font(fs)` + `fs:SetTextColor(S.Color("text.highlight"))` re-applied from `OnLooksChanged`, or accept `text.body`. Doubtful D6 |
| P9 | Dungeon readout (one line of season dungeons) | :290-297 (`GameFontHighlightSmall`); markup `TARGETED = "|cffffd100%s %d|r"` :59, `NOT_TARGETED = "|cff808080%s %d|r"` :60, used `updateReadout` :163-179 | gold `ffd100` / gray `808080` escapes; small white font | `S.Text(readout, "body")` (small size kept: sizes are relative); markup from tokens rebuilt on `OnLooksChanged`: `text.accent` (1,0.82,0 -> `ffd100` exact) and `text.disabled` (0.5 -> `80` rounded to the byte, as LootHistory's `NS.SkinEscape`). Exact on Ka0s Default |
| P10 | "Regions unsupported" note | :380-383 (`GameFontDisableSmall`) | client disabled gray | `S.Text(fs, "disabled")` (`text.disabled`) |
| P11 | PGF-unsupported line | `f.unsupported = label(f, "", 14, BODY_TOP, "GameFontDisable")` :797 | client disabled gray | `S.Text(fs, "disabled")` |
| P12 | Number boxes: key level (2 digits), max age (3 digits) | `numberBox` :227-246 (`InputBoxTemplate`) | Blizzard input art; `setLocked` :193-197 types `SetTextColor(0.5,0.5,0.5)` locked / `SetTextColor(1,1,1)` unlocked | `S.EditBox(box)` (`input.bg`, `input.border*`, `input.text`, `input.focus`, `input.radius`); locked/unlocked text from `S.Color("text.disabled")` / `S.Color("text.highlight")` (exact today) or `input.text` (0.9, a 0.1 change). Re-run after `S.EditBox` (it sets `input.text`) and on `OnLooksChanged` (Panel.Refresh does both) |
| P13 | Copy box (N-N range) | `buildCopyBox` :558-586 (`InputBoxTemplate`) | Blizzard input art; dimmed via `setLocked` :592 | `S.EditBox(box)` as P12 (no `padInput`: `EUISkin.lua:197-199` says the 6px insets pull it off the right column) |
| P14 | Copy box label dim | `setCopyEnabled` :591-594: `copyLabel:SetTextColor(1,1,1)` / `(0.5,0.5,0.5)` | typed white / gray | `S.Color("text.highlight")` / `S.Color("text.disabled")` |
| P15 | Copy-label hover frame | :581-585 | invisible, no art | none |
| P16 | Multi-select dropdowns (regions, playstyle, composition) | `multiSelect` :330-357 (`WowStyle1DropdownTemplate`, `SELECT_W` 225) | Blizzard dropdown art, template font | `S.Dropdown(dd)` (`input.*`, `icon.arrow`; label `dd.Text`) |
| P17 | Preset dropdown | `buildPresetRow` :526-532 (`WowStyle1DropdownTemplate`) | as P16 | `S.Dropdown(dd)` |
| P18 | Push buttons (5: Save, Save as, Delete, Apply, Clear) | `button()` :121-131 (`UIPanelButtonTemplate`); used :514-522, :601-611 | Blizzard red button art, template font | `S.Button(b)` (`btn.*`; disabled text `text.disabled` following OnEnable/OnDisable, which Save/Delete/Apply rely on). Not `StateButtonLabel`: its Ka0s meaning (accent while on) differs from EllesmereUI's (white/gray), which `EUISkin.lua:219-226` relied on |
| P19 | The menus the dropdowns open | Blizzard_Menu (`dd:SetupMenu`, `root:CreateCheckbox/CreateRadio/CreateDivider/CreateTitle` :347-354, :453-462) | Blizzard's shared menu frames | **Exception** (rung 3): Blizzard shared menu frames |
| P20 | Hover tooltips the panel writes onto `GameTooltip` | `fillTooltip` :80-83 (`tip:SetText(title, 1, 1, 1)`; body `AddLine(text, nil, nil, nil, true)` = client default gold `NORMAL_FONT_COLOR`), `tooltip()` :87-98, `menuTooltip` :103-108 | white title, gold body (Blizzard settings convention) | Lines take skin colors (skinning-§7): title `gtip.value` (1,1,1, exact), body `gtip.title` (1,0.82,0, exact). The frame stays Blizzard's. Doubtful D7 (the names read backwards) |
| P21 | StaticPopups `PGFE_PRESET_SAVE_AS`, `PGFE_PRESET_DELETE` | `definePopups` :482-506 | Blizzard StaticPopup | **Exception** (rung 3) |

The panel's layering (`core/Constants.lua:29-48`, `layerWithDialog` :771-776) is untouched by skinning, except
`LEVEL.ACCENT_RING` (:46), which goes with `modules/EUISkin.lua` (PG-06).

### 1b. Settings pages (`settings/`)

| # | Surface | Built at | Today | Paint (rung 1) |
|---|---|---|---|---|
| S1 | Landing page (logo, notes, slash rows) | `Helpers.BuildLandingPage` `settings/Panel.lua:31-43` | library | library (Options descriptor `addonName = addonName`, `settings/OptionsSetup.lua:90`, is the page's skin owner once registered) |
| S2 | General page chrome, Master controls, Filters tab rows | `settings/Panel.lua:50-94`, `buildGeneralPage` :374-391 | library makers | library |
| S3 | Region tags tab: per-portal heading, preview line (`TextRow` with `fontObject = "GameFontHighlightLarge"` :168), a **host-acquired** `AceGUI:Create("SimpleGroup")` line :173-179 holding the color pickers, reset button pair :183-187 | `renderRegionTab` :155-188 | preview text is region-tag markup (player colors) | `Skin:PaintAce(owner, line)` on the host's SimpleGroup (likely no painter for a layout group: harmless, and the library's own rows inside are painted by their makers); the preview's colors are the player's region colors (exception E3). `GameFontHighlightLarge` is a size choice passed to a library maker (D9) |
| S4 | EllesmereUI skin tab (switch row, 4 condition `InteractiveLabel`s, PGF-skin link `EditBox`, state line, custom `GameTooltip` lines) | `renderEuiTab` :338-359; `statusRow` :304-325 (`AceGUI:Create("InteractiveLabel")` :307, `SetFontObject(GameFontHighlight)` :309); `addPGFSkinLink` :272-297 (`AceGUI:Create("EditBox")` :276); `euiTooltip` :253-265 (`SetText(row.label, 1,1,1)`, red `AddLine(..., 1, 0.25, 0.25)`); markup `|cff999999` :233, `|cff33ff33` :242; icons `ReadyCheck-Ready/NotReady` :221-227 | typed colors and fonts | **Retired by PG-06**: replaced by the library's Skin tab (`O.AppearanceTab`, whose source section draws the same check/cross condition lines). Nothing here is painted; it is deleted |
| S5 | Skin tab (new) | — | — | `O.AppearanceTab({ get, set, owner, strings })` as a host tab in `GENERAL_OPTS.tabs` (`settings/Panel.lua:361-364`). The page has no Keybindings tab, so it lands last. Library-drawn |
| S6 | Profiles page: host-acquired `SimpleGroup` container + AceConfigDialog's AceDBOptions tree | `settings/Profiles.lua:26-38` (`AceGUI:Create("SimpleGroup")` :29) | stock AceGUI | `Skin:PaintAceTree(owner, container)` right after `AceConfigDialog:Open` inside the renderer, as LootHistory does (`../LootHistory/settings/Profiles.lua:65-69`) |
| S7 | Reset-all confirmation | `Settings.EnsureResetPopup` (`settings/Schema.lua:171`), shown `settings/Panel.lua:45-48` | Blizzard StaticPopup | **Exception** (rung 3) |

### 1c. Tool surfaces (library-owned, owner-aware)

| # | Surface | Configured at | Paint |
|---|---|---|---|
| T1 | Debug console, its copy window, the diagnostics report | `core/DebugLogSetup.lua:83-116` (`name`, `addonName = addonName`, `font = NS.FONT_MONO`) | Library (`LibKa0s-DebugLog-1.0` minor 22 takes `addonName` as the skin owner when the descriptor sets neither `skin` nor `applySkin`, `libs/.../DebugLog.lua:301-305` at v1.79.0). Nothing to change beyond registering the owner **before** the console is first built. `font` is the descriptor's mono path, JetBrains Mono = Ka0s Default `font.mono` |
| T2 | Launcher / minimap button and its tooltip | `core/LauncherSetup.lua:169-189` | Library-drawn; `LibKa0s-Launcher-1.0` takes no skin owner at v1.79.0. Not a host surface |
| T3 | Close controls | `NS.MakeCloseButton` wrapper `core/CoreSetup.lua:87-89` already passes `addonName` | no caller in the addon; nothing to do |
| T4 | `NS.ApplySkin = lib.ApplySkin` `core/CoreSetup.lua:83` | published, **no caller** | If kept, bind the owner (`function(f, s) return lib.ApplySkin(f, s, addonName) end`) so a future caller cannot hit anti-pattern #107's owner-less `Core.ApplySkin`; `tests/test_surface_parity.lua:15` compares the namespace arms, so both arms keep the member |
| T5 | Perf panel, sim panel, test strip, copy windows of its own | — | none exist (performance-§12 exemption; no test mode; no sim) |

### 1d. Not the addon's to paint

| Surface | Where | Why |
|---|---|---|
| Region tags on Group Finder rows and applicants | `modules/RegionTags.lua:68-88` (`SetText(tag .. " " .. text)` on Blizzard's `entry.ActivityName` / `member.Name`) | Blizzard font strings; the tag colors are the player's region colors. Exceptions E3, E4 |
| Chat lines | `NS.PREFIX` cyan `core/PGFE.lua:20`; `debug logging |cff40ff40ON|r` / `|cffff4040OFF|r` `locales/enUS.lua:187-188`; schema errors `|cffff0000` `settings/Schema.lua:108,112`; slash hint `|cffFFFF00` `settings/Slash.lua:170`, `locales/enUS.lua:196-197` | Chat is not a frame the addon draws (anti-pattern #107 names frames). Exception E5 |

## 2. Library factories that take an owner

| Factory | Call site | Owner today | Action |
|---|---|---|---|
| `LibKa0s-Options-1.0` `lib:New{ addonName }` | `settings/OptionsSetup.lua:87-113` (`addonName = addonName` :90) | folder name, already | none: becomes the page owner on `RegisterOwner` |
| `LibKa0s-DebugLog-1.0` `lib:New{ addonName }` | `core/DebugLogSetup.lua:83-116` (`addonName = addonName` :85) | folder name, already | none |
| `Core.MakeCloseButton(parent, onClick, addonName)` | `core/CoreSetup.lua:87-89` | folder name, already | none (no caller) |
| `Core.ApplySkin(frame, skin, owner)` | `core/CoreSetup.lua:83` (`NS.ApplySkin = lib.ApplySkin`) | **none** | bind the owner (T4) or drop the export |
| `O.AppearanceTab(spec)`, `O.SkinPicker(spec)` | new | — | `owner` defaults to the descriptor's `addonName`; pass `page = "general"` to the picker |
| `LibKa0s-Widgets-1.0` (dropdown, search box, copy window, strip, autocomplete, drag handle, reorder, line chart), `LibKa0s-Perf-1.0`, `LibKa0s-Sim-1.0` | — | — | not used by the addon |
| `LibKa0s-Launcher-1.0` | `core/LauncherSetup.lua:169` | — | takes no owner at v1.79.0 |

## 3. HUD style settings (O2)

**No HUD.** The addon draws no bars, icons, glows or HUD text (grep of `core/ modules/ settings/` for
`StatusBar`, `SetStatusBar`, `Glow`, `LSMValues`, `FontGroup`, `BorderGroup`, `BarGroup` finds no consumer;
`settings/OptionsSetup.lua:52-55` only stubs the composers). Nothing for `S.Resolve` / `Skin.FROM_SKIN` /
`fromSkin` companions, and no one-time R3 reset. **PG-03 goes to `exceptions.tsv`**, proved by e.g.
`! grep -rnE 'StatusBar|FontGroup|BorderGroup|BarGroup|S\.Resolve' core modules settings`.

The region-tag colors (`profile.regionColors.<key>`, `defaults/Profile.lua:166-184,195`) are **meaning colors the
player sets**, not HUD style: they stay (E3) and are not reset.

## 4. Exceptions

| Id | Rung | What | Where | Reason |
|---|---|---|---|---|
| E1 | 3 | StaticPopups: `PGFE_PRESET_SAVE_AS`, `PGFE_PRESET_DELETE`, the reset-all popup, `PGFE_EUI_SKIN_RELOAD` (the last is deleted by PG-06; the library's `LIBKA0S_SKIN_RELOAD` replaces it) | `modules/Panel.lua:482-506`, `settings/Schema.lua:171`, `modules/EUISkin.lua:412-418` | skinning-§7: a StaticPopup is a Blizzard shared frame. `core/Popup.lua`'s strata lift (frame-layering-§4) is layering, not skinning, and stays |
| E2 | 3 | Blizzard_Menu dropdown menus (the checkbox lists, the preset radio list, divider, title) | `modules/Panel.lua:347-354, 453-462` | Blizzard's shared menu frames; only the dropdown **buttons** (PGFE's own frames) are painted (P16, P17) |
| E3 | 4 | Region tag colors: the twelve player-set bucket colors (defaults `REGION_HEX` `defaults/Profile.lua:166-170`), the tag markup `modules/RegionTags.lua:46-49`, and the Region tags tab's preview line `settings/Panel.lua:141-145,168` | as listed | Identity colors that carry meaning by hue, chosen by the player through the schema; no skin changes which region is which color |
| E4 | 3+4 | The unknown-realm tag `"|cff9d9d9d?|r"` | `modules/RegionTags.lua:50` | Drawn onto Blizzard's Group Finder font strings (never skinned) and part of the region-tag palette. No token reproduces it exactly (`sem.unknown` 0.6 = `99`, `q.poor` 0.62 = `9e`). Owner may overrule to `sem.unknown` (a one-shade change on a Blizzard row) |
| E5 | — | Chat output colors: the mandated cyan `[PGFE]` tag (slash-commands-§4), debug ON/OFF green/red, schema-error red, slash hint yellow | §1d | Chat is not a frame the addon draws; the cyan tag is a standard MUST. Listed so the owner can overrule |
| E6 | 3 | `GameTooltip` the frame (P20), `ColorPickerFrame` (the Region tags pickers) | `modules/Panel.lua:87-108`; `settings/Panel.lua:177` (library color rows) | skinning-§7; only the lines the addon writes take skin colors |
| E7 | 3 | PGF's own dialog (`PremadeGroupsFilterDialog`) and Blizzard's `LFGListFrame.SearchPanel.SearchBox` | `core/PGFBridge.lua`; `modules/Panel.lua:545-549` | Another addon's / Blizzard's frames: PGFE never paints them (that is `PremadeGroupsFilter_EllesmereUI`'s job under EllesmereUI). Only the attached panel, PGFE's own frame, skins |

## 5. Gaps (rung 2)

Strictly the things no existing primitive, option or token can do.

### PG-G1 — a stock target cannot stay stock under Ka0s Default (primitive-option)

- **Component.** The whole attached panel (P1-P4, P7, P8-P14, P16-P18).
- **Why no primitive fits.** Since SkinPaint minor 6 / SkinPaintControls minor 4 ("no skin is special", owner
  ruling 2026-10-26) every control primitive fades a template's stock art and paints from the skin's tokens
  **under Ka0s Default too** (`Shell`, `Button`, `Checkbox`, `EditBox`, `Dropdown`, `PageButton`, and
  `FadeRegions`/`FadeNineSlice`, which `SkinPaint.lua:975-994` now fade under every skin; the doc table's "Ka0s
  Default fades nothing" line is stale). `Text`/`Font` set Ka0s Default's Oxanium face. `Button`'s `keep` keeps the
  art under **every** skin, not only Ka0s Default. A host cannot compose it either: skipping the paint on Ka0s
  Default works at first draw, but a live switch back to Ka0s Default from another skin replays the recorded
  primitives with Ka0s Default's tokens, and there is no public give-back (`Skin:Untrack` forgets a frame without
  restoring it). PGFE's Ka0s Default look **is** the client's stock template look (ratified,
  `docs/ARCHITECTURE.md:473`), so adopting through today's primitives changes Ka0s Default's look, which the plan
  says stops the run for the owner.
- **Proposed.** One option the control and window primitives and `Text`/`Font` accept, e.g. `opts.stockDefault =
  true` (for `Text(fs, role, opts)` / `Font` a trailing opts table): under the owner's **Ka0s Default** the target is
  given back as the client drew it (stock art alpha, font object, colors, holders hidden) and recorded, so a switch
  to any other skin paints it and a switch back gives it back again; under the other eight skins and under `eui` it
  paints as today. Skin Tester shows a stock `UIPanelButtonTemplate` / `UICheckButtonTemplate` /
  `InputBoxTemplate` / `WowStyle1DropdownTemplate` / `PortraitFrameTemplate` row with the option. Only needed if
  the owner keeps the PGF-matching look under Ka0s Default (D1).
- **Ka0s Default must reproduce (exactly today's):** `PortraitFrameTemplateMinimizable` with
  `SetBorder("ButtonFrameTemplateNoPortraitMinimizable")`, portrait hidden (`modules/Panel.lua:779-783`), header
  art clips (:636-665), collapsed height `HEADER_H = 32` (:619) and `ATTACH_RAISE = 3` (:42);
  `MaximizeMinimizeButtonFrameTemplate` with `RedButton-Expand` / `RedButton-Condense` atlases (:722-727);
  `UICheckButtonTemplate` at 32px (:45, :202, :266); `InputBoxTemplate` (:228, :559) with white typed text and
  0.5 gray when locked (:196); `WowStyle1DropdownTemplate` (:331, :526); `UIPanelButtonTemplate` at height 22 then
  the dropdown's height (:122-123, :533-535); `GameFontHighlight` labels (:113, :253, :443, :577),
  `GameFontHighlightSmall` readout (:290), `GameFontDisableSmall` (:380), `GameFontDisable` (:797), the template
  title font (:784).

### PG-G2 — an owner cannot add its own condition to the EllesmereUI gate (primitive-option on `RegisterOwner`)

- **Component.** PG-06's fourth gate condition, `pgf`: "Premade Groups Filter's own EllesmereUI skin is loaded and
  on" (`core/EUIBridge.lua:88-104`, `:133-136`), with four states (missing / disabled / off / on) and their labels and
  fixes (`:106-115`), and the CurseForge link box shown while it is missing (`settings/Panel.lua:267-297, 355`;
  URL `core/EUIBridge.lua:69`).
- **Why no primitive fits.** `Skin:GetEUIStatus(owner)` has exactly four fixed conditions (`eui`, `master`, `own`,
  `facade`; `LibKa0s/SkinEUI.lua` gate); the Skin tab enables the EllesmereUI source from `status.ok` alone and
  draws only those lines; `SetChoice`/`__EnterEUI` paint on the first three plus the facade. An owner has no way to
  hold the EllesmereUI paint back, or to list a fifth line, so after PG-06 the panel would be EllesmereUI-painted under
  a stock PGF dialog whenever the PGF skin addon is missing, disabled or off, which the owner's 2026-10-09 decision 1
  forbade ("the two always match", `docs/superpowers/plans/2026-10-09-eui-skin.md`). The host may not read
  `EllesmereUIDB` itself any more (skinning-§5, anti-pattern #107), and the `off` state needs exactly that read
  (`thirdPartySkinAddons["PremadeGroupsFilter"]`).
- **Proposed.** `RegisterOwner(owner, { euiConditions = { { key, ok = fn(), label, hint }, ... } })`, or a
  library-side `entryOn(name)` exposed for a named sibling entry: each extra condition is appended to
  `GetEUIStatus(owner).conditions`, gates `ok` and the paint like the built-in three, is translated through
  `COND_<key>` strings, and the tab draws it with its fix. The library would read `thirdPartySkinAddons[<name>]` for
  the sibling entry (still inside SkinEUI.lua's carve-out). Ka0s Default is unaffected.
- **Today's behavior to reproduce:** paint only when the PGF skin state is `on` (`EUIBridge.lua:94-104`); labels
  `locales/enUS.lua:211-224`; hint for `on`/missing/disabled/off `EUIBridge.lua:107-115`.

### PG-G3 — `Checkbox`'s `borderInset` is stripped before EllesmereUI sees it (primitive-option on the provider)

- **Component.** The eight check buttons under the `eui` source (P7).
- **Why.** PGFE hands EllesmereUI `S.Checkbox(cb, { borderInset = 4 })` today (`modules/EUISkin.lua:29, 178`), which
  sizes EllesmereUI's box to match PGF's EllesmereUI skin. `LibKa0s/SkinEUI.lua` `ALLOWED.Checkbox = { stockCheck =
  true }` drops every other key (`strip`, `SkinEUI.lua:218-235`), so the same host call under the library's `eui`
  draws EllesmereUI's default inset. The Ka0s `Checkbox` already reads `opts.borderInset`
  (`SkinPaintControls.lua:257-268`).
- **Proposed.** Add `borderInset` to `ALLOWED.Checkbox` (EllesmereUI's facade reads it, per PGFE's own working call).
- **Ka0s Default:** unaffected. EllesmereUI look to keep: `borderInset = 4` on a 24px frame (`EUISkin.lua:29`).

## 6. Doubtful calls (for DECISIONS.md)

| Id | Call | Recommendation |
|---|---|---|
| D1 | **The panel's Ka0s Default look.** Adopting through today's primitives turns the PGF-matching metal panel into Ka0s slate/gold with Oxanium text, under a PGF dialog that stays metal. That changes Ka0s Default's look and contradicts the ratified deviation `docs/ARCHITECTURE.md:473` ("an extension surface must read as part of the host window it attaches to"). | **Stop and ask the owner** (the plan's stop rule). Recommend keeping the PGF look under Ka0s Default through PG-G1 (the panel follows the other eight skins and EllesmereUI, and stays stock on Ka0s Default); the alternative, accepting the flat look, needs the deviation row rewritten and every panel smoke re-looked |
| D2 | **The PGF-skin condition after PG-06.** Without PG-G2 the condition is lost and EllesmereUI paints the panel under an unskinned PGF dialog. | Take PG-G2 into M1. If declined: keep a host-drawn advisory line (no gate) on the Filters tab with the PGF skin's state and the CurseForge link, reading only `C_AddOns` (installed / loaded) and dropping the `off` state, which needs an `EllesmereUIDB` read the host may no longer make |
| D3 | **Migration of `profile.euiSkin` (default `true`) to `skin.source`.** AceDB strips defaults, so almost every profile holds no `euiSkin` and reads `true`. Mapping "not false" to `"eui"` puts `source = "eui"` on every profile, including players without EllesmereUI, whose Skin tab then shows EllesmereUI selected (disabled) with the "used only if EllesmereUI cannot skin" note. | One per-profile step in `NS.MIGRATIONS[2]` (`core/Database.lua:12-15`; walk `db.sv.profiles` raw, so an absent key means the old default `true`): `euiSkin == false` -> `"ka0s"`; otherwise `"eui"` **only when EllesmereUI is present** (`Skin:GetEUIStatus(owner).conditions` `eui` ok, read at OnInitialize, EllesmereUI being an OptionalDep loaded first), else `"ka0s"`; then delete `euiSkin`. Behavior is equivalent: under the library `eui` with the gate closed falls back live to the Ka0s skin, exactly as the old switch did nothing while a condition failed |
| D4 | **PGFE-only EllesmereUI extras not in the library:** the accent ring on checked boxes (`EUISkin.lua:105-133`), the whole-pixel accent mark (`:135-173`) and its `UI_SCALE_CHANGED` / `DISPLAY_SIZE_CHANGED` re-layout (`:381-393`), the minus/plus glyphs on the min/max buttons (`:228-254`, atlases `UI-QuestTrackerButton-Secondary-Collapse/-Expand` :35-36), the 12pt text-box font (`:192-195`), the 25px shell header and flush anchor (`:27-28, 284-292`). | Drop the ring, the mark sizing, the scale events and the 12pt font (library's `Checkbox`/`EditBox`/`Font` under `eui` are EllesmereUI's own); keep only geometry the host owns: the checkbox shrink to 24 and the collapsed height and anchor, chosen from `Skin:GetEUIStatus(owner).painted` (EllesmereUI's shell bar is 25 whatever `title.height` says; keep `EUI_SHELL_HEADER_H = 25` as a host geometry constant). Re-look under EllesmereUI at smoke |
| D5 | Collapse/expand control under a skin (P4). | `S.PageButton(b, "up"/"down")`; on Ka0s Default as D1 decides |
| D6 | White labels (`GameFontHighlight`) vs `text.body` 0.9 (P8, P12, P14). No `Text` role names `text.highlight`. | Use `S.Text(fs, "body")` if D1 accepts the flat look (the whole panel changes anyway). If D1 keeps stock on Ka0s Default, PG-G1's give-back covers it and the other skins use `text.body`. Typed `SetTextColor(1,1,1)` / `(0.5,…)` in `setLocked`/`setCopyEnabled` become `S.Color("text.highlight")` / `S.Color("text.disabled")` either way |
| D7 | GameTooltip line colors (P20): title white, body gold, the Blizzard settings convention, opposite of LootHistory's gold title. | Keep the look: title `gtip.value` (1,1,1), body `gtip.title` (1,0.82,0), both exact today; comment why the names cross |
| D8 | Skin tab EllesmereUI `own` hint names `opts.label`; EllesmereUI's Third-Party list shows the folder name `PremadeGroupsFilterExtension`. | `opts.label = "Ka0s Premade Groups Filter Extension"` (the brand) and `spec.strings.COND_own_HINT` naming the folder, as the old hint did (`locales/enUS.lua:209`) |
| D9 | Region tags preview uses `fontObject = "GameFontHighlightLarge"` on a library `TextRow` (S3). | Keep: a size passed to a library maker, colored by the player's region markup (E3) |
| D10 | Stand-down and the library's paint: today `EUISkin` refuses to paint while stood down (`EUISkin.lua:319-320`, pinned by `tests/test_disabled.lua:207-226`). The library paints recorded frames on `SetChoice`, `OnLooksChanged` and the facade's arrival whatever the host's latch. | Accept: a repaint of a hidden own frame is no SavedVariables write, no event and no visible change. Rewrite `disabled 6` to pin "no frame is built and nothing is registered while stood down", and gate `NS.MaybeShowSkinPicker` on the latch (LootHistory's `standsUp` rule) |
| D11 | Where the picker's combat retry registers `PLAYER_REGEN_ENABLED`: PGFE's rule is that every event is in `NS.FEATURE_EVENTS` (`core/PGFE.lua:149-151`) and `tests/test_disabled.lua:21-26` pins the list. | A one-shot private frame as LootHistory does (`../LootHistory/core/SkinSetup.lua:351-424`), unregistered on fire and on stand-down, documented beside the latch; or add `PLAYER_REGEN_ENABLED` to FEATURE_EVENTS and update the pin. Recommend the one-shot frame |

## 7. Re-vendor v1.77.0 -> v1.79.0 obligations (PG-RV)

1. **Copy both payloads whole** from the run's tag by `git archive` (12 new library files: `Toast.lua`, `Skin.lua`,
   `SkinDefs.lua`, `SkinPaint.lua`, `SkinPaintExtras.lua`, `SkinPaintControls.lua`, `SkinEUI.lua`, `SkinAce.lua`,
   `WidgetsCopyWindow.lua`, `DebugLogWindow.lua`, `OptionsAppearance.lua`, `OptionsSkinPicker.lua`; the skin fonts
   incl. Oxanium; the Glass textures and the eight generated bars) and `tests/_kit/` (kit revision 43+, with
   `mock_paint.lua`).
2. **`tests/loader.lua:13-56` pins the v1.77.0 `LibKa0s.xml` file list by hand.** Add the 12 files in XML order
   (diff of `LibKa0s.xml` v1.77.0 -> v1.79.0: `Toast` after `Glow`; `Skin`, `SkinDefs`, `SkinPaint`,
   `SkinPaintExtras`, `SkinPaintControls`, `SkinEUI`, `SkinAce` after `MediaIcons`; `WidgetsCopyWindow` after
   `WidgetsAutocomplete`; `DebugLogWindow` after `DebugLogGates`; `OptionsAppearance`, `OptionsSkinPicker` after
   `OptionsKeybinds`).
   Without them the harness measures the degradation stubs (anti-pattern #48).
3. **Options degradation stub** (`settings/OptionsSetup.lua:12-85`) gains `AppearanceTab`, `AppearanceRows`
   (v1.78.0), `SkinPicker`, `HideSkinPicker` (v1.79.0): e.g. `AppearanceTab = function() return nil end`,
   `AppearanceRows = function() return nil end`, `SkinPicker = function() return nil end`, `HideSkinPicker =
   function() end`. `tests/test_surface_parity.lua:31-34` (`T.assertSurfaceParity(...Helpers, "LibKa0s-Options-1.0")`)
   is red until it does. Note: a host tab entry built from a stub `AppearanceTab` that answers nil must not be put
   in `GENERAL_OPTS.tabs` as nil (guard it).
4. **DebugLog stub** (`core/DebugLogSetup.lua:24-75`): check the parity list against v1.79.0's DebugLog members
   (DebugLog moved to minor 22 with `DebugLogWindow.lua`); `tests/test_surface_parity.lua:21` pins it.
5. **`CLAUDE.md`**: provenance line `Bundles [LibKa0s](...) v1.79.0 (MIT).` (or the run's tag) in the re-vendor
   commit; icons line becomes `LibKa0s icons: clear, close, copy, eye, settings.` (the picker's Eye and gear,
   `O.SkinPicker`); prune `media/icons/` to it with the tag's `tools/prune-icons.lua`; README icon credits in step.
6. **`tests/test_vendor_sync.lua`** follows the provenance line (kit's gate); nothing else pins a minor
   (`grep -n "MINOR\|MODULES\|1\.77" tests/*.lua` finds no library pin besides the loader list).
7. **Ka0s Default looks different at v1.79.0** (Oxanium, the Ka0s Default bar) only for a registered owner; PGFE
   registers in PG-01, so its smoke re-looks at the panel (and D1) after adoption, not at the re-vendor.
8. **README font credits**: the OFL faces (Oxanium and the eight skins' families) once the addon adopts (PG-05).

## 8. Risks

- **The ratified look (D1).** The single largest risk: today's primitives change the panel's Ka0s Default look;
  M1 must settle PG-G1 or the owner must rule before PG-02.
- **Taint and Blizzard frames.** The panel is PGFE's own frame parented to PGF's (non-secure) dialog; nothing is
  protected and combat lockdown does not apply to it. Never pass PGF's dialog, `LFGListFrame` or the Group Finder
  rows to a primitive (E7). `S.Dropdown` fades a `WowStyle1DropdownTemplate` PGFE created; the Blizzard_Menu it opens
  stays stock (E2). The library's hooks are `HookScript`/`hooksecurefunc` on own frames; the panel's own
  `SetScript` calls (`modules/Panel.lua:125, 203, 241-243, 268, 564-574, 742`) must run **before** the primitive
  (a later `SetScript` drops the primitive's hook).
- **Pooled AceGUI.** Host acquisitions are the Region tab's `SimpleGroup` (`settings/Panel.lua:173`) and the
  Profiles container (`settings/Profiles.lua:29`); the EUI tab's `InteractiveLabel` / `EditBox` (with a permanent
  `__pgfeLinkHook` field written onto a pooled frame, `settings/Panel.lua:284-293`) go away with PG-06, which removes
  a pool-leak shape.
- **EllesmereUI one-way paint.** Under the library a profile switch away from `eui` after it painted asks for a
  reload (`OnReloadRequest`); PGFE's `reloadProfile` (`core/PGFE.lua:170-189`) must call `SetChoice` after the latch
  re-read and raise the library's reload once (not its own `PGFE_EUI_SKIN_RELOAD`).
- **Test fake mismatch.** PGFE's `m.installEUI` (`tests/wow_mock.lua:341-...`) answers `C_AddOns.IsAddOnLoaded` for
  PGFE's reader, which takes the **first** return; `SkinEUI.lua`'s `loaded()` takes the **second**
  (`loadedOrLoading, loaded`). The fake must return both, or every `eui` test reads the child as not loaded.
- **Event pin.** `tests/test_disabled.lua:21-26` pins eight events including `UI_SCALE_CHANGED` and
  `DISPLAY_SIZE_CHANGED`, which leave with `modules/EUISkin.lua`; `tests/test_layers.lua:31,43` pins
  `modules/EUISkin.lua` in its source list and `LEVEL.ACCENT_RING = 3`; `tests/test_settings_layout.lua:32,167-176`
  pins the `euiSkin` row and the "EllesmereUI skin" tab; `tests/run.lua:101-106` lists `test_euibridge`,
  `test_euiskin`, `test_euisettings` (Kit.assertSuiteInventory fails both ways). Each moves with PG-06.
- **Hot path.** `modules/RegionTags.lua`'s Group Finder post-hooks run per row paint; skinning touches nothing
  there. `Panel.Refresh` gains one `OnLooksChanged` subscriber (rare).
- **File cap.** No authored file is near 1500 lines: `modules/Panel.lua` 923, `defaults/Realms.lua` 559 (data),
  `settings/Panel.lua` 404. Closest is `tests/test_panel.lua` at **1215**: put the skin tests in a new
  `tests/test_skin.lua` rather than growing it. PG-06 removes 591 authored lines (`core/EUIBridge.lua` 158,
  `modules/EUISkin.lua` 433) and ~945 test lines (`test_euibridge` 183, `test_euiskin` 442, `test_euisettings` 320).
- **Docs churn (PG-05).** `docs/ARCHITECTURE.md` has an EllesmereUI seams section (`:273` on), the module-map rows
  (`:80, :92`), the event table (`:188-192`), the `euiSkin` setting (`:111-114`), the taint notes (`:228-237`), and two
  deviation rows to retire or rewrite (`:469` library-stack-§6 EllesmereUIDB read, which PG-06 retires; `:473` the
  panel chrome, which D1 decides). The TOC's load-bearing comments name `modules\EUISkin.lua` and
  `core\EUIBridge.lua` (`PremadeGroupsFilterExtension.toc` core and modules blocks).

## 9. PG-06 detail: what the two files do, callers, saved keys, and library coverage

### What they do

- `core/EUIBridge.lua` (158 lines), the only reader of EllesmereUI state: `SKIN_NAME` = folder name (:28);
  `IsSuiteReady` (`EllesmereUI.RegisterSkin` + `EllesmereUIBlizzardSkin` loaded, :49-52); `IsMasterOn`
  (`EllesmereUIDB.thirdPartySkinsOff`, :56-59); `IsEntryOn(name)` (`thirdPartySkinAddons[name] ~= false`, :62-66);
  `PGF_SKIN_URL` (:69); `installed()` via `C_AddOns.DoesAddOnExist` / `GetAddOnInfo` (:74-86); `PGFSkinState`
  (missing/disabled/off/on, :94-99) and `IsPGFSkinOn` (:102-104); `Conditions()` (four `{key, ok, label, hint}`,
  :120-138); `GateOpen()` (:143-148); `WhyClosed()` (:152-158).
- `modules/EUISkin.lua` (433 lines): registers `EllesmereUI.RegisterSkin(SKIN_NAME, onFacade)` at file load (:430-433);
  keeps the facade, `OnLooksChanged(repaintLooks)` (:423-428); `REQUIRED` facade shape (:42-43); `TryApply` paints once
  when S held + gate + switch + not stood down + panel built (`blocked` :319-331, `TryApply` :337-359), pcall'd,
  latching `paintFailed`; paints: `S.Shell` + `S.FadeNineSlice` + portrait/header-art alpha 0 + title `S.Font`/`S.White`
  + flush re-anchor + min/max glyphs (`paintShell` :270-300); checkboxes shrink + `S.Checkbox{borderInset=4}` + accent
  ring/mark + SetChecked hooks, edit boxes `S.EditBox`/`S.Font`/12pt/insets, dropdowns `S.Dropdown`/`S.Font`, buttons
  `S.Button`/`S.StateButtonLabel`, `S.Font` on every font string of the frame and body (`paintBody` :302-316);
  `OnSwitch` (on paints, off after a paint shows `PGFE_EUI_SKIN_RELOAD`, :363-369); scale re-layout events (:387-393);
  stand-down glyph reset and stand-up retry (:396-410).

### Every caller

| Caller | Uses |
|---|---|
| `modules/EUISkin.lua:66, 327, 431` | `NS.EUIBridge.GateOpen`, `SKIN_NAME` |
| `modules/Panel.lua:701-702` | `f.headerHeight` (set by `EUISkin.paintShell` :284) |
| `modules/Panel.lua:815-817` (`Panel.Create`), `:855-856` (`UpdateVisibility`) | `NS.EUISkin.TryApply()` |
| `core/PGFE.lua:182-188` (`reloadProfile`) | `NS.EUISkin.OnSwitch(p.euiSkin == true)` |
| `core/Constants.lua:17, 44-46` | `LEVEL.ACCENT_RING` (read by `EUISkin.lua:32`) |
| `settings/Panel.lua:190-359` | the `euiSkin` row (`disabledIf`, `validate`, `onChange = EUISkin.OnSwitch`), `Settings.EUISkinStateText` (`IsApplied`, `HasFacade`), `euiTooltip` (`WhyClosed`), `addPGFSkinLink` (`PGF_SKIN_URL`), `renderEuiTab` (`Conditions`, `PGFSkinState`); `GENERAL_OPTS` tab `EUI_GROUP` :363 |
| `modules/Diagnostics.lua:85-94` | `IsSuiteReady`, `IsMasterOn`, `IsEntryOn(SKIN_NAME)`, `IsPGFSkinOn`; `registered`, `HasFacade`, `IsWanted`, `IsApplied` |
| `locales/enUS.lua:199-259` | ~30 EllesmereUI strings (most retire; the PGF-skin ones survive only under PG-G2 or D2's advisory) |
| `PremadeGroupsFilterExtension.toc` | `core\EUIBridge.lua`, `modules\EUISkin.lua` lines and their load-bearing comments; `## OptionalDeps: ... EllesmereUI ...` **stays** (skinning-§5) |
| tests | `tests/test_euibridge.lua`, `tests/test_euiskin.lua`, `tests/test_euisettings.lua`, `tests/test_disabled.lua:205-226`, `tests/test_layers.lua:31, 43`, `tests/test_settings_layout.lua:32, 167-176`, `tests/run.lua:101-106`, `tests/wow_mock.lua` (`installEUI` :341-..., EllesmereUI read-backs :251, :295) |
| docs | `docs/ARCHITECTURE.md` (§8 list), `docs/superpowers/plans/2026-10-09-eui-skin.md` (frozen, leave), `docs/smoke-tests.md`, `docs/settings-panel.md`, `docs/schema.md`, `docs/module-map.md` (to be swept in PG-05) |

### Saved keys

- `profile.euiSkin` (bool, default **true**, `defaults/Profile.lua:194`; schema row `settings/Panel.lua:204-219`;
  CLI `/pgfe set euiSkin` refused while the gate is closed, :210-215). The only persisted EllesmereUI state.
  Migrated by D3 to `skin.source` and deleted; `NS.SCHEMA_VERSION` 1 -> 2 (`core/Database.lua:10`).
- Session-only (not saved): `S`, `applied`, `paintFailed`, `EUISkin.registered`.
- The player's EllesmereUI entry `EllesmereUIDB.thirdPartySkinAddons["PremadeGroupsFilterExtension"]` carries over
  untouched: the library registers the same owner name (the folder).

### What LibKa0s's `eui` provider (SkinEUI minor 1) already covers

| PGFE piece | Library |
|---|---|
| `RegisterSkin` at file load, presence-guarded, retried | `RegisterOwner` registers through a trampoline, retries on `ADDON_LOADED("EllesmereUI")` and `PLAYER_LOGIN` |
| `eui` / `master` / `own` conditions, labels, hints, check/cross lines | `GetEUIStatus(owner).conditions` (+ `facade`), drawn by the Skin tab with `ReadyCheck-Ready/NotReady` |
| `REQUIRED` facade shape, fail closed, latch, one log line | `NATIVE_LIST` check on arrival, `euiRefused[owner]`, `opts.log` |
| `S.OnLooksChanged` repaint | hooked once per owner, repaints records and fires the owner's `OnLooksChanged` |
| one-way paint, reload popup on turning it off | `SetChoice` `reload`, `OnReloadRequest`, `LIBKA0S_SKIN_RELOAD` |
| the switch (`euiSkin`) | `skin.source = "eui"` through the write seam; the tab's source radio |
| Shell/FadeNineSlice/Checkbox/EditBox/Dropdown/Button/Font on own frames | each host primitive call goes to EllesmereUI's facade while it paints the owner |
| pooled-frame safety | AceGUI and shared targets never handed to EllesmereUI |

### What it lacks

1. The `pgf` condition and its four states, link and fixes (PG-G2; D2).
2. `borderInset` through to EllesmereUI's `Checkbox` (PG-G3).
3. PGFE's own EllesmereUI-only decorations and geometry (D4): accent ring, whole-pixel mark, scale re-layout, min/max
   glyphs, 12pt box font, the 25px header and flush anchor, the checkbox shrink and label shift. Geometry stays the
   host's (keyed on `GetEUIStatus(owner).painted`); the decorations are dropped.
4. The stand-down refusal (D10).
5. Diagnostics lines: replace `modules/Diagnostics.lua:85-94` with `Skin:GetChoice(owner)`, `GetEUIStatus(owner)`
   (`ok`, `painted`, `refused`, each condition) and `PendingReload(owner)`; `tests/test_diagnostics.lua` re-pins.

## 10. Effort

**L.** One panel of about 20 widgets is small, but PG-06 deletes two modules and three test suites (~1.5k lines)
and rewrites the migration, the settings tab, Diagnostics and the EllesmereUI test fake, and the panel's Ka0s Default
look (D1 / PG-G1) needs an owner ruling and possibly a library option before PG-02 can land.
