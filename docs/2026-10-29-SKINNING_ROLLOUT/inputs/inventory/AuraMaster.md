# AuraMaster (AM): skinning inventory

Read-only inventory for items AM-RV and AM-01..AM-05 of `00_PLAN.md`. The source was `../AuraMaster` at
`feat/2026-10-29-skinning-rollout`, which was clean and equal to master at read time and vendors LibKa0s
v1.77.0. The library was read at the main checkout, v1.79.0 (`4e1ae41`). Every `file:line` is in
AuraMaster unless it says otherwise.

The owner's answers relayed with this run apply as follows: **O2 kept** (the one-time HUD reset runs for every
player, §3); **O3, the picker is shown to everyone** (`skin.pickerSeen` defaults to false on every profile);
**O4 does not apply** (AuraMaster has no EllesmereUI bridge; `grep -rn Ellesmere core modules settings` finds only a
comment at `core/Compat.lua:31`).

## Shape of the addon, for the implementer

- **AuraMaster is mostly a HUD.** It has no standalone window. What it draws is:
  - the aura containers (bars, icons and text lines dressed onto the buttons of Blizzard's `CustomAuraContainerTemplate`
    engine);
  - its unlock furniture (the drag strip, outline, snap marks, frame picker, test marker and name label);
  - its settings pages, which `LibKa0s-Options-1.0` renders;
  - two library tool windows (the debug console with its copy window, and the perf panel).
- **Every HUD style value belongs to one container.** The values live under `profile.containers[id].{bars|icons|text|label}`
  (`defaults/Profile.lua:137-297`), so the R3 reset walks the containers, not one profile table.
- **Use one font choke point and two texture sites.** `Style.FontKey` (`modules/Style.lua:1030-1034`) resolves the
  font for every text path: `Style.ApplyFont` (`:124-135`), the measure helpers (`:237`, `:269`, `:307`), the text glow
  (`modules/Style_TextGlow.lua:110`) and `modules/FontPrimer.lua`. The bar fill and background textures are fetched only
  at `modules/Style_Bars.lua:206` and `:218`. Resolving through `S.Resolve` at these three sites reaches the whole HUD.
- **Never hand an engine button to a recorded primitive.** The buttons' sizes and levels read **secret** once the
  engine lays them out (`modules/Style.lua:340-358`, `docs/midnight-quirks.md`). A recorded paint (`S.BarTexture`,
  `S.IconBorder`, `S.SquareIcon`) would also put thousands of pooled engine regions into the skin registry. The HUD
  therefore paints through `S.Resolve`, `S.Token` and `S.Color` read at dress time, with one `S.OnLooksChanged`
  listener that re-applies every container. This is rung 1: it composes existing facade calls.

## 1. Surfaces

The Tokens column names tokens from `SkinDefs.lua`'s schema. "User" means a per-container setting the player owns.
The skin never overrides a user value except through the R3 companions in §3.

### 1a. HUD (dressed on engine buttons and preview placeholders)

| Surface | Built at | Typed today | Paints through (rung 1) |
|---|---|---|---|
| Bar fill texture | `modules/Style_Bars.lua:46-52` (StatusBar alpha 0 at `:47-48`, fill Texture `:51`); painted `:204-209` | `Style.Fetch("statusbar", b.barTexture, C.FALLBACK_TEXTURE)` `:206`; `C.WHITE_TEXTURE` `:47` (hidden driver); fallback `core/Constants.lua:14` | `S.Resolve("bar.texture", b.barTexture, b.barTextureFromSkin)` into `Style.Fetch`. The color stays user (`barColor`) |
| Bar background texture | `modules/Style_Bars.lua:43`; painted `:218-221` | `Style.Fetch("statusbar", b.bgTexture, …)` `:218` | `S.Resolve("bar.texture", b.bgTexture, b.bgTextureFromSkin)`. The color stays user (`bgColor`, which equals `bar.bg` in Ka0s Default) |
| Bar border, icon border (Bars, Icons, Text styles) | `Style.NewBorder` `modules/Style.lua:385-389`, solid strips `:376-379`, backdrop host `:462-471`; dressed by `Style.ApplyBorder` `:494+` | `"Solid"` LSM key registered at `modules/Style.lua:34` (WHITE8X8); `SetBackdrop`/`SetBackdropBorderColor` `:485-488`; strip `SetColorTexture` `:422` | User style, size and color. An optional `S.Resolve("bar.borderStyle", …)` is **not** recommended (see §6 D1). Never `S.IconBorder`, because these are secret-size frames |
| Bar/Icons/Text fonts (name, time, stacks; text line; glow copies) | FontStrings `modules/Style_Bars.lua:78-80`, `modules/Style_Icons.lua:54-55`, `modules/Style_Text.lua:172`, glow copies `modules/Style_TextGlow.lua:135` | `fs:SetFont(path,size,flags)` `modules/Style.lua:126`, `:237`, `:269`, `:307`, `modules/Style_TextGlow.lua:110`; `C.FALLBACK_FONT` Friz `core/Constants.lua:16`; default face `"Friz Quadrata TT"` `defaults/Profile.lua:115` | `Style.FontKey`: `S.Resolve("hud.font", t.font, t.fontFromSkin)`. Size, flags and color stay user (`hud.fontSize` and `hud.outline` are not followed, §3) |
| Spark | `modules/Style_Bars.lua:54-59` | `"Interface\\CastingBar\\UI-CastingBar-Spark"` `:59`; color user `:234` | Exception (Blizzard art, §4). The color stays user |
| Pandemic wash | `modules/Style_Bars.lua:84-86`, `modules/Style_Icons.lua:57-59` | `C.WHITE_TEXTURE`; user `pandemicColor` `Style_Bars.lua:300`, `Style_Icons.lua:156` | User color. Nothing to paint |
| Expiring time color | `modules/Style.lua:1021`, `modules/Style_Text.lua:661` | user `expiringColor` | User. Nothing to paint |
| Dispel edges, dispel backdrop, dispel word, dispel bar tint | `modules/Style_Icons.lua:47-49`, `modules/Style_Text.lua:119-123`, `:361-367`, `:674-679`; word `:432`; `modules/Style_Bars.lua:196-199`, `:307-337`; `core/Compat.lua:403-412` | `profile.dispelColors` / `C.DEFAULT_DISPEL_COLORS` `core/Constants.lua:319-325` | Exception, rung 4 (game meaning) |
| Text glow ring | `modules/Style_TextGlow.lua:107-135` | user `glowColor` (default black) `defaults/Profile.lua:293`; `fs:SetTextColor` `:113` | Stays user. `S.GlowColor`/`glow.color` is **not** followed (Ka0s Default's is gold, §6 D3) |
| Aura icons (Bars icon, Icons, Text icon) | `modules/Style_Bars.lua:40`, `modules/Style_Icons.lua:28`, `modules/Style_Text.lua:143` | `SetTexture(aura.icon)` `Style_Bars.lua:347`, `Style_Icons.lua:203`, `Style_Text.lua:692` | Exception, rung 4 (spell icons) |
| Cooldown swipe | `modules/Style_Icons.lua:31` (`CooldownFrameTemplate`) | Blizzard's | Exception, rung 3 |
| Container name label (optional, locked or not) | `modules/Container.lua:827-829`; dressed `:832` via `Style.ApplyFont` | default gold font block `defaults/Profile.lua:124-129` (`fontColor 1,0.82,0`) | HUD font: `S.Resolve("hud.font", lc.font.font, lc.font.fontFromSkin)` through `Style.FontKey`. The color stays user |
| Test-mode placeholders | `modules/Preview.lua:119-123` (plain Buttons), dressed by the same `Style.*` code | as the HUD rows above | As the HUD rows above, so they need no extra work |

### 1b. Unlock furniture and overlays (AuraMaster's own frames, not engine buttons)

| Surface | Built at | Typed today | Paints through (rung 1 unless a gap is named) |
|---|---|---|---|
| Drag strip (fill, edge, label, help and close marks) | `modules/Anchors.lua:672-694`, `KW.DragHandle(anchor, {...})` | edge `Anchors.STRIP_EDGE = {size 1, 1,0.82,0,0.6}` `:488`, painted by the host `edge = NS.Style.DrawEdge` `:689`; fill, label and mark tints are library literals | Pass `owner = addonName` (DragHandle minor 6). The library then reads `handle.bg`, `text.accent`, `icon.tint` and `icon.hot`. **The host edge is not repainted by the library** (`WidgetsDragHandle.lua:542-543`), so AuraMaster redraws it from `S.Color("handle.edge")` (Ka0s Default `{1,0.82,0,0.6}`, exact) at build time and in its `OnLooksChanged` listener. `modules/Anchors_Snap.lua:393` and `:469` restore the edge from `STRIP_EDGE` and must read the token too |
| Strip label: attached-name gray | `modules/Anchors.lua:635` | `"|c" .. C.ATTACHED_NAME_COLOR` = `ff8c8a84` (`core/Constants.lua:305`) | **Gap AM-G2** (no token holds 0.549, 0.541, 0.518) |
| Strip label and test marker: TEST tag | `modules/Anchors.lua:638`, `modules/Preview.lua:259` | `C.TEST_TAG_COLOR = "ffff8000"` `core/Constants.lua:295` | `sem.warn` `{1,0.5,0,1}`. The escape rounds to `ff8000` exactly (§6 D5) |
| Strip tooltip (GameTooltip lines) | spec `modules/Anchors.lua:560-605` | the attached line `{1,0.82,0}` `:603`; the title and body take the library's DragHandle defaults (`WidgetsDragHandle.lua:335-338`: gold, white) | Per-line colors from tokens: attached line `gtip.title` (exact); body `gtip.value` (WHITE, exact). The frame is GameTooltip (§4) |
| Close-mark tooltip | `modules/Anchors.lua:590-605` (`closeTooltipSpec`) | library defaults | as above |
| Unlocked outline | `modules/Container.lua:796-797` | `NS.Style.DrawEdge(o, 1, 1,1,1, OUTLINE_ALPHA)`, `OUTLINE_ALPHA = 0.35` `:28` | **Gap AM-G3** (white at 0.35: no token. `chart.crosshair` holds that value, but it is a chart role) |
| Snap or detach highlight (box, two dots, line) | `modules/Anchors_Snap.lua:409-450`; painted `:430-436`; state `:810` | `C.SNAP_COLOR {0.25,0.90,0.35,1}` `core/Constants.lua:164`; `C.DETACH_COLOR {0.95,0.25,0.25,1}` `:174` | **Gap AM-G4** (meaning pair, no exact `sem.*`) |
| Frame picker outline | `modules/FramePicker.lua:114-115` | `DrawEdge(outline, 2, 0.2,0.8,1,1)` | **Gap AM-G5** (no token. `sem.info` is `{0.3,0.8,1}`) |
| Frame picker label | `modules/FramePicker.lua:118`, text `:68-71` | `GameFontNormalLarge` (gold); hint `|cffaaaaaa` | `S.Text(label, "accent")` for the frame name; hint `cover.text` `{0.667,…}` (exact, §6 D6) |
| Test marker (frame and text) | `modules/Preview.lua:275-279` | font = template label font (Friz 12, gold, OUTLINE) `:278`; text TEST escape `:259` | Font through `Style.ApplyFont`/`Style.FontKey` (`hud.font`); text `sem.warn` |
| Preview extent, priming frame, event frames, Blizzard-frames hider | `modules/Preview.lua:221`, `modules/FontPrimer.lua:98`, `modules/EmptyWatch.lua:328`, `modules/ContainerManager.lua:812`, `modules/TimedSpells.lua:135`, `modules/Anchors_Snap.lua:828`, `modules/BlizzardFrames.lua:25` | none visible | Nothing to paint |

### 1c. Settings pages

The library renders the pages from the descriptor (`settings/OptionsSetup.lua:136-138`). Its `addonName` is already
the folder name, so once the owner is registered the chrome, the rows the library acquires and the composed groups
follow the skin with no AuraMaster code. AuraMaster draws or acquires the following itself.

| Surface | Built at | Typed today | Paints through |
|---|---|---|---|
| **`AuraMasterDropdown` widget type** (every schema row with `values`, through `settings/Schema.lua:327-328`, plus six hand-built ones) | registered `settings/OptionsSetup.lua:70-86`; type name `core/Constants.lua:62`; `NS.CreateDropdown` `:90-96`; callers `settings/Filters.lua:110`, `settings/Containers.lua:177`, `:190`, `settings/GeneralSpells.lua:538`, `settings/GeneralUserCategories.lua:407`, `settings/Text.lua:254` | stock Dropdown art, text justified LEFT `:81-82` | **Gap AM-G1.** `Skin:PaintAce` dispatches on `rawget(widget,"type")` (`LibKa0s/SkinAce.lua:670`), and `AuraMasterDropdown` has no painter, so every dropdown on every AuraMaster page stays stock under all nine skins |
| Hand-acquired Buttons | `settings/GeneralSpells.lua:600`, `settings/Layout.lua:608`, `settings/GeneralUserCategories.lua:294`, `:361`, `:455` | stock | `Skin:PaintAce(owner, w)` (an `NS.SkinPaintAce` seam). Release work goes through `Skin:OnRelease` |
| Hand-acquired EditBoxes | `settings/GeneralUserCategories.lua:216`, `:381`; Text preview (disabled) `settings/Text.lua:297` | stock; the preview text is colored by the user's font color `settings/Text.lua:283-287` | `PaintAce`. The preview escape is a user color and stays |
| Hand-acquired Label | `settings/Layout.lua:636` | stock | `PaintAce` |
| Profiles page (AceConfigDialog over AceDBOptions) | `settings/Profiles.lua:38-48` (`SimpleGroup`) | stock | `Skin:PaintAceTree(owner, container)` after each `AceConfigDialog:Open`, as LootHistory does (`../LootHistory/settings/Profiles.lua:69`) |
| Plan-warning lines | `settings/OptionsSetup.lua:479` | `|cffffa040` (1, 0.627, 0.251) | **Gap AM-G6** (no orange at that value. `sem.warn` is `ff8000`) |
| Container picker suffix `(unit type, style)` | `settings/OptionsSetup.lua:424` | `|cff888888` (0.533) | **Gap AM-G7**, grouped with the other gray notes |
| Muted notes (Layout, Text) | `settings/Layout.lua:678`, `:721`; `settings/Text.lua:57`, `:203`, `:210`, `:345`, `:520`, `:526` | `|cff808080` | `text.disabled` `{0.5,0.5,0.5}` rounds to `80` exactly (§6 D7) |
| Gold emphasis (Text) | `settings/Text.lua:58`, `:145` | `|cffffd100` | `text.heading` (or `text.accent`), exact |
| Secondary gold (growth note, "yours" marker) | `settings/Layout.lua:653`; `settings/GeneralSpells.lua:402` | `C.SECONDARY_GOLD = "ffd9b861"` `core/Constants.lua:300` | **Gap AM-G8** (0.851, 0.722, 0.380; `text.headingAlt` is 0.91, 0.77, 0.42) |
| Filters "See spells" link and "(info)" | `settings/Filters.lua:329-330`, `:374`, `:387` | `|cff6699ff`, `|cffbbbbbb` | **Gap AM-G9** (`text.link` is **orange** `ff8000` in Ka0s Default; there is no blue link token and no 0.733 gray) |
| Unit, aura-type and style labels in dropdowns; HELPFUL/HARMFUL type marks | `settings/Containers.lua:77-89`; `settings/GeneralSpells.lua:401`, `:487` | `C.UNIT_COLORS`, `C.AURA_TYPE_COLORS`, `C.STYLE_COLORS` `core/Constants.lua:55-57` | Exception, rung 4 (identity palette, §4 and §6 D8) |
| Container banner, nav rail, tabs, Master controls, landing/About page | library (`Helpers.PageBanner`, `RenderTabbedSchema`, `BuildLandingPage`) | none in AuraMaster | follows `addonName` |

### 1d. Tool surfaces (library, handed the owner already)

| Surface | Built at | Owner today | After adoption |
|---|---|---|---|
| Debug console and its copy window | `core/DebugLogSetup.lua:131-200` (`lib:New`) | `addonName = addonName` `:138` | Follows automatically. DebugLog minor 22 treats `addonName` as the skin owner once it is registered (`LibKa0s/DebugLog.lua:301-311`). Nothing to change |
| Perf panel | `core/PerfSetup.lua:29-36` | `addonName = addonName` `:33` | Follows automatically (PerfPanel minor 10, `LibKa0s/PerfPanel.lua:72-77`) |
| Close marks | `core/CoreSetup.lua:168-170` (`NS.MakeCloseButton` passes `addonName`) | yes | Follows |
| Launcher (LibDBIcon button and its tooltip) | `core/LauncherSetup.lua` | n/a | The minimap button is LibDBIcon's (exception). The tooltip lines are the library's |
| Sim panel, test strip, copy windows of its own | none: AuraMaster has no Sim, no `TestStrip` and no `CopyWindow` of its own | n/a | Nothing to do |
| **First-run skin picker (new, O3)** | n/a | n/a | `O.SkinPicker(spec)`: `onPreview` toggles AuraMaster's test mode (`NS.Preview`/`SetTestMode`, refused in combat); `onSettings` opens General > Appearance; held to `PLAYER_REGEN_ENABLED` in combat, like LootHistory's `NS.MaybeShowSkinPicker` |

## 2. Library factories that take an owner

| Factory | Call site | Owner passed today | Action |
|---|---|---|---|
| `KW.DragHandle(anchor, spec)` | `modules/Anchors.lua:674` | **no** | add `owner = addonName`, and repaint the host `edge` on `OnLooksChanged` (§1b) |
| `lib.MakeCloseButton(parent, onClick, owner)` | `core/CoreSetup.lua:169` | yes (`addonName`) | none |
| `DebugLog:New{ addonName }` | `core/DebugLogSetup.lua:138` | yes | none |
| `Perf:New{ addonName }` | `core/PerfSetup.lua:33` | yes | none |
| Options descriptor `addonName` | `settings/OptionsSetup.lua:138` | yes (folder) | none. Note that `settings/General.lua:56`'s `addonName = "Aura Master"` is MasterControls' display label, not an owner, and must stay a label |
| `Core.ApplySkin(frame, keys, owner)` | `NS.ApplySkin` published at `core/CoreSetup.lua:159`, no caller in AuraMaster | n/a | if a caller ever appears, wrap it with the owner the way `NS.MakeCloseButton` is wrapped |
| `O.SkinPicker`, `O.AppearanceTab`/`O.AppearanceRows` | new | n/a | the spec's `owner`/`get`/`set` through the write seam |
| `Skin:PaintAce` / `PaintAceTree` / `OnRelease` | new, for §1c's hand-acquired widgets | n/a | owner bound in a `core/SkinSetup.lua` seam (`NS.SkinPaintAce`, `NS.SkinPaintAceTree`, `NS.SkinOnRelease`) |

## 3. HUD style settings (O2's one-time reset)

Every key below sits under **each container record**, `profile.containers[id]`, whose template is
`defaults/Profile.lua:137-297`. The composer emits `<key>FromSkin` companions when the spec passes `fromSkin = true`
(`LibKa0s/OptionsCompose.lua:310-345`, `:509-530`). AuraMaster's composed groups are at `settings/Bars.lua:46`, `:83`,
`:102`, `:122`, `:171`; `settings/Icons.lua:45`, `:84`; `settings/Text.lua:382`, `:456`; and `settings/Layout.lua:584`.

**Reset these.** Each is a font or texture picker that has a composer companion:

| Schema key (container-relative) | Default today | Token | How it follows |
|---|---|---|---|
| `bars.barTexture` | `"Blizzard"` `defaults/Profile.lua:214` | `bar.texture` (Ka0s Default `"Ka0s Default"`) | BarGroup `fromSkin` → `bars.barTextureFromSkin`; draw `S.Resolve("bar.texture", v, fromSkin)` at `Style_Bars.lua:206` |
| `bars.bgTexture` | `"Blizzard"` `:219` | `bar.texture` | BarGroup (keys-mapped, `settings/Bars.lua:83-85`) → `bars.bgTextureFromSkin`; at `Style_Bars.lua:218` |
| `bars.name.font`, `bars.time.font`, `bars.stacks.font` | `"Friz Quadrata TT"` `:115`, `:231-233` | `hud.font` (`"Ka0s Oxanium SemiBold"`) | FontGroup `fromSkin` → `<prefix>fontFromSkin`; resolved once in `Style.FontKey` |
| `icons.time.font`, `icons.stacks.font` | same `:251-252` | `hud.font` | same |
| `text.font.font` | same `:271` | `hud.font` | same |
| `label.font.font` | same `:209`, `:124-129` | `hud.font` | same (`settings/Layout.lua:584`) |

**Do not reset these** (§6 D1 to D4 give the reasons):

| Key | Default | Token | Why not |
|---|---|---|---|
| `bars.borderStyle`, `bars.iconBorderStyle`, `icons.borderStyle`, `text.iconBorderStyle` | `"Solid"` (`:222`, `:225`, `:245`, `:275`); icon borders shown by default | `bar.borderStyle` = `"None"` in **all nine** skins | A reset would remove every Icons container's border on every profile |
| `*.fontSize`, `*.fontFlags` | 10 to 12, `"OUTLINE"` | `hud.fontSize` 12, `hud.outline` | The composer has no companion for them. Per-element sizes are layout, not style |
| Colors: `barColor`, `bgColor`, `borderColor`, `iconBorderColor`, `fontColor`, `sparkColor`, `glowColor`, `pandemicColor`, `expiringColor` | player's | `bar.bg`, `bar.border`, `icon.border`, `glow.color` exist | The composer offers no color `fromSkin`. `glow.color` (gold) would turn the default black glow gold |

**How to run it.** Add a schema step `{ to = 13 }` at the end of `SCHEMA_STEPS` (`core/Database.lua:337-438`, current
`to = 12` at `:431`), with its body in `core/Database_Migrations.lua`. Use `eachProfile` (`:320`), and for each stored
container call `Skin.ResetToSkin(c, KEYS)` (`LibKa0s/Skin.lua:650-670`).

**Caution about the sentinel.** `ResetToSkin` writes the companion only when `<leaf>FromSkin` already exists on the
parent table, or when the value is a table. A string key with no companion gets `"@skin"` written into the picker's
own key (`Skin.lua:658-664`), which the LSM picker and the CLI cannot render. The step must therefore either seed the
companions (`<leaf>FromSkin = false`) before the call, or set the companions to true directly. Never let the sentinel
reach `barTexture` or `font`. Without the library, the step must still set the companions. It must not raise, and the
ladder stops on a raise (`:455-472`).

**New containers.** The template should default the reset companions to **true**, so a container created after the
step follows the skin like a migrated one does (§6 D2). The schema rows' `default` must match this, or the
defaults-drift tests go red.

## 4. Exceptions

**Rung 3: a skin never touches these (skinning-§7)**

- Blizzard's aura engine (`CreateFrame("AuraContainer", …, "CustomAuraContainerTemplate")`, `modules/Container.lua:449`,
  `modules/Container_Twins.lua:114`) and the buttons it pools. Only AuraMaster's own regions on them are dressed, and
  only through `Style.*` with resolved values. No primitive records an engine button. The reasons are secret
  geometry, taint and the pool.
- `CooldownFrameTemplate` swipe (`modules/Style_Icons.lua:31`).
- The Blizzard buff and debuff frames that `modules/BlizzardFrames.lua:25` reparents to a hidden parent. That is a
  feature, not a skin, and it is unchanged.
- GameTooltip itself: aura tooltips and the strip and close-mark tooltips. Only the lines AuraMaster writes take tokens.
- StaticPopup confirmations (`settings/OptionsSetup.lua:121`; the Containers delete and confirm-write popups).
- `ColorPickerFrame` (every color row) and the AceGUI-3.0-SharedMediaWidgets `LSM30_*` pull-outs (font, statusbar
  and border pickers; `lib.__PatchLSM30Border()` `settings/OptionsSetup.lua:345`).
- `SettingsPanel` chrome.
- The LibDBIcon minimap button.
- Chat output: `|cff…` escapes in printed lines (`settings/Slash.lua:214`, `:225`, `:272`, `:528`, `:614`;
  `settings/Layout.lua:172`, `:180`; `settings/Containers.lua:112`, `:143`; `modules/Preview.lua:38`;
  `modules/FramePicker.lua:147`; `modules/CastAura.lua:116`; `settings/OptionsSetup.lua:375`; the degraded
  `core/DebugLogSetup.lua:72`). `DEFAULT_CHAT_FRAME` is Blizzard's, and LootHistory kept its chat escapes the same way
  (§6 D9).
- The spark art `Interface\CastingBar\UI-CastingBar-Spark` (`modules/Style_Bars.lua:59`): Blizzard art, the same under
  every skin. Its tint is the user's.

**Rung 4: meaning colors stay**

- Dispel-type colors (`profile.dispelColors`, `C.DEFAULT_DISPEL_COLORS` `core/Constants.lua:319-325`) everywhere they
  tint: bar fill and background, icon edge, text backdrop and edge, the dispel word (`modules/Style_Text.lua:432`),
  and `core/Compat.lua:412`.
- Class colors (every `useClassColor*` companion, through `NS.ResolveColor` and `NS.ClassColor`).
- Spell and aura icons.
- Player-set HUD colors (fill, background, border, font, spark, pandemic, expiring, glow). These are the player's
  choices, not chrome, and the composer has no color companion.
- AuraMaster's identity palette for unit, aura type and style in dropdown labels and spell-list marks
  (`core/Constants.lua:55-57`, `settings/Containers.lua:77-89`, `settings/GeneralSpells.lua:401`). Player blue, target
  orange, buff green and debuff red mean the same thing on every page. The owner may overrule this (§6 D8).

## 5. Gaps (rung 2)

Each gap below has a concrete reason: either no primitive reaches the widget, or no token holds the exact value
Ka0s Default must keep.

| Id | What | Why no primitive or token fits | Proposed | Ka0s Default must reproduce |
|---|---|---|---|---|
| **AM-G1** | AuraMaster's own AceGUI type `AuraMasterDropdown`, used by every dropdown row and six hand-built dropdowns | `Skin:PaintAce` looks the painter up by `rawget(widget,"type")` (`LibKa0s/SkinAce.lua:670`); `lib.__acePaint` has `Dropdown` and nothing for a host type. A host cannot add to `__acePaint` (a private table that a newer minor replaces) without patching the library (anti-pattern #107). The type exists for a real reason: AceGUI's per-type pool leaked LEFT justification across addons (`settings/OptionsSetup.lua:56-62`) | **primitive-option**: `Skin:PaintAce` honours a base type for a host-registered widget type. Either a widget field the host sets at construction (`widget.paintAs = "Dropdown"`, read by `rawget`) or `Skin:AliasAceType(hostType, baseType)` | exactly what `PAINT.Dropdown` draws for a stock Dropdown under Ka0s Default today (`input.bg {0.1,0.1,0.12,0.9}` under `input.border {0.24,0.24,0.27,0.9}` at `input.borderSize 1`, text `input.text`, label `text.body`), with AuraMaster's LEFT justification (`settings/OptionsSetup.lua:81-82`) untouched by paint and restore |
| **AM-G2** | Strip label's attached-name gray | No token holds `8c8a84`. The nearest are `sem.neutral {0.62,0.62,0.66}` and `text.muted {0.7,0.7,0.72}` | **token** `handle.textDim` (strip label, dimmed state) | `{0.549, 0.541, 0.518, 1}` (`ff8c8a84`, `core/Constants.lua:305`, used `modules/Anchors.lua:635`) |
| **AM-G3** | Unlocked placement outline | No token holds white at 0.35 in a window or HUD role (only `chart.crosshair`, a chart role) | **token** `handle.outline` | `{1, 1, 1, 0.35}` (`modules/Container.lua:28`, `:797`) |
| **AM-G4** | Snap and detach marks (a go/no-go meaning pair) | `sem.statusOk {0.30,0.95,0.35}` and `sem.statusBad {1,0.32,0.32}` are near but not equal | **token** pair `sem.attach`, `sem.detach` | `{0.25, 0.90, 0.35, 1}` and `{0.95, 0.25, 0.25, 1}` (`core/Constants.lua:164`, `:174`) |
| **AM-G5** | Frame picker outline | `sem.info {0.3,0.8,1}` is near but not equal | **token** `handle.pick` | `{0.2, 0.8, 1, 1}` at 2px (`modules/FramePicker.lua:115`) |
| **AM-G6** | Plan-warning lines on the container pages | `sem.warn` is `{1,0.5,0}`; nothing holds `ffa040` | **token** `sem.warnAlt` | `{1, 0.627, 0.251, 1}` (`settings/OptionsSetup.lua:479`) |
| **AM-G7** | Settings grays: container-picker suffix, Filters "(info)" | No token at 0.533 or 0.733 | **tokens** `text.note` (0.533) and `text.noteAlt` (0.733), or fold both under D7/D10 | `|cff888888` `settings/OptionsSetup.lua:424`; `|cffbbbbbb` `settings/Filters.lua:330` |
| **AM-G8** | Secondary gold | `text.headingAlt {0.91,0.77,0.42}` is near but not equal | **token** `text.headingMuted` | `{0.851, 0.722, 0.380, 1}` (`ffd9b861`, `core/Constants.lua:300`) |
| **AM-G9** | Blue in-panel link ("See spells") | `text.link` is orange in Ka0s Default; there is no blue link token | **token** `text.linkAlt` | `{0.4, 0.6, 1, 1}` (`settings/Filters.lua:329`) |

AM-G2 to AM-G9 are all one-value tokens of the kind SkinDefs minor 6 added for LootHistory. If the owner prefers
folding them into the nearest existing token, Ka0s Default's pixels move by a few percent, and under the plan
that is an ask (§6 D10).

## 6. Doubtful calls (for DECISIONS.md)

- **D1. Border style is outside the R3 reset, and gets no `fromSkin` companion.** `bar.borderStyle` is `"None"` in
  all nine skins, and AuraMaster's Icons style shows a `"Solid"` border by default (`defaults/Profile.lua:245`).
  Resetting it would strip the border from every icon. AuraMaster's `"Solid"` is also its own secret-safe strip path
  (`modules/Style.lua:376-424`), which an LSM border key from a skin would replace with the backdrop path that only
  redraws after a `/reload`. **Recommend:** reset fonts and bar textures only.
- **D2. New containers follow the skin.** The template defaults `barTextureFromSkin`, `bgTextureFromSkin` and every
  `fontFromSkin` to true, so containers made after the step match migrated ones. **Recommend: yes.** This changes
  `tests/settings_pin.lua` and the default pins in `tests/test_render_coverage.lua`, `tests/test_anchors_label.lua`,
  `tests/test_fontprimer.lua`, `tests/test_diagnostics.lua` and `tests/test_enchantreset.lua` (24 Friz and Blizzard
  pins).
- **D3. The glow color does not follow `glow.color`.** Ka0s Default's is gold, and AuraMaster's default glow is a
  black legibility ring. **Recommend:** keep it as a user color, with no companion.
- **D4. HUD font size and flags do not follow `hud.fontSize` and `hud.outline`.** The composer has no companion for
  them, and AuraMaster's per-element sizes (10 to 12) are part of each layout. **Recommend:** keep them user-owned.
- **D5. The TEST tag uses `sem.warn`.** Ka0s Default's test-mode token `sem.modeTest` is red `{1,0.15,0.15}`, which
  is LootHistory's TEST mark, but AuraMaster's TEST is orange. `sem.warn` reproduces `ff8000` exactly. **Recommend:**
  `sem.warn`, unless the owner wants every addon's TEST mark unified on `sem.modeTest`, which would change AuraMaster's
  look.
- **D6. The frame-picker hint uses `cover.text`.** It is the exact value (0.667) and the picker is an overlay like
  the combat cover. **Recommend:** `cover.text`, with no new token.
- **D7. The gray `|cff808080` notes use `text.disabled`.** It is the exact value, but the role is "muted note", not
  "disabled". `text.muted` would move them from 0.5 to 0.7. **Recommend:** `text.disabled`. The consolidation may
  prefer one collection-wide note-gray token.
- **D8. The identity palette stays as a rung-4 exception.** These are unit, aura-type and style colors in dropdown
  labels. They carry meaning inside AuraMaster but are not game-meaning colors. **Recommend:** keep them as an
  exception and list them for the owner to overrule. The alternative is three to ten new tokens.
- **D9. Chat line colors are out of scope**, because the chat frame is Blizzard's. LootHistory set the precedent.
  **Recommend:** list them as an exception.
- **D10. AM-G2 to AM-G9: new tokens, or fold into the nearest token.** **Recommend:** add the tokens in the M1
  library release (exact Ka0s Default, with the other skins deriving them through FOLLOW from `text.muted`,
  `sem.good`/`sem.bad`, `sem.info`, `sem.warn`, `text.headingAlt` and `text.accent`). If the consolidation finds the
  same near-misses in other addons, it may merge them into shared tokens instead.
- **D11. AM-G1 could instead retire `AuraMasterDropdown`**, by painting stock `Dropdown`s and restoring LEFT
  justification in a chained `Skin:OnRelease`. That does not work for the schema rows, which the library's makers
  acquire through `dialogControl`, so AuraMaster cannot attach a release hook to them. **Recommend:** the library
  option (AM-G1). Other addons that register a custom widget type would benefit too.
- **D12. A skin switch in combat.** The repaint listener (`S.OnLooksChanged`) calls `FontPrimer.PrimeAll()` and then
  `CM.RequestApply(nil, true)`. An apply under lockdown waits, as today's config changes do. **Recommend:** accept
  that the HUD restyles when combat ends, and say so in `docs/smoke-tests.md`.

## 7. Re-vendor v1.77.0 → v1.79.0 obligations (AM-RV)

- **Copy the whole folder from the tag** (`git archive`, never the working tree): `libs/LibKa0s/` and
  `tests/_kit/`.
  - v1.78.0 adds `WidgetsCopyWindow.lua`, `DebugLogWindow.lua`, `OptionsAppearance.lua` and `SkinAce.lua`, the Skin
    major's files (`Skin.lua`, `SkinDefs.lua`, `SkinPaint*.lua`, `SkinEUI.lua`), five skin fonts and two Glass
    textures.
  - v1.79.0 adds `Toast.lua`, `OptionsSkinPicker.lua`, the Oxanium faces and the eight bar textures.
  - The test loaders read the file list from `libs/LibKa0s/LibKa0s.xml` (`tests/run.lua:21`,
    `tests/test_loadorder.lua:198`), so no test pins a static file list.
- **Update the Options degradation stub** (`settings/OptionsSetup.lua:300-317`). It gains **`AppearanceTab`,
  `AppearanceRows`** (v1.78.0) and **`SkinPicker`, `HideSkinPicker`** (v1.79.0); `tests/test_surface_parity.lua`
  (`Kit.assertSurfaceParity`) is red until they are there.
- **Roll the CLAUDE.md provenance line** (`CLAUDE.md:36`) to `v1.79.0`, or to v1.80.0 if M1 releases one. The vendor
  gate is `tests/test_vendor_sync.lua`.
- **Icons.** `CLAUDE.md:37` says `LibKa0s icons: clear, close, copy, help, info.` The picker draws `eye` (because
  AuraMaster passes `onPreview` for test mode) and `settings`, so the line becomes
  `clear, close, copy, eye, help, info, settings`. `tests/test_setups.lua:70` hard-codes the library-drawn set
  `{ close, copy, clear, info }` and must add `eye` and `settings` with a comment naming the picker.
- **Expect Ka0s Default to look different** once AuraMaster adopts (v1.79.0): Oxanium faces and the Ka0s Default bar
  texture. Before AM-01 registers the owner, nothing changes.
- **Update the TOC.** Add `EllesmereUI` to `## OptionalDeps` (`AuraMaster.toc:8`, skinning-§5). Add
  `core\SkinSetup.lua` after `core\CoreSetup.lua` and before `core\Bus.lua` (any time before the first module that
  draws), with a `# LOAD-BEARING:` note, and add it to the order `tests/test_loadorder.lua` pins.
- **Release pins.** No test pins a LibKa0s minor or tag besides the vendor gate. The `LibKa0s v1.xx` mentions in
  `tests/test_pages_*.lua` are comments only.

## 8. Risks

- **Taint and secret values on engine buttons.** Their regions live on Blizzard's aura engine buttons, whose
  geometry reads secret. A primitive that creates holder frames or reads sizes (`S.IconBorder`, `S.SquareIcon`,
  `P.edges`) raises or taints there. Paint the HUD only with resolved values inside AuraMaster's existing `Style.*`
  dress.
- **The pool and registry on a hot path.** Containers pool hundreds of buttons. Recorded primitives
  (`S.BarTexture`) would track every pooled region in the skin registry and replay them on every switch.
  `S.Resolve` at dress time costs one table read per dress. Keep `S.Token` and `S.Resolve` out of per-aura
  `UNIT_AURA` paths: the dress runs per apply, not per aura event, which is already true.
- **The blank-name regression (#24).** The skin's `hud.font` (Oxanium) is an addon-supplied, lazily loaded font,
  exactly the case `modules/FontPrimer.lua` exists for. FontPrimer resolves through `Style.FontKey`, so it must use
  the same `S.Resolve` path, and the `OnLooksChanged` listener must prime before it requests the apply (a
  CONFIG_CHANGED-style ordering). Otherwise every bar name stays blank after a skin switch, or after the reset on
  first login.
- **Combat lockdown.** The settings page and the picker (deferred to `PLAYER_REGEN_ENABLED`), test-mode preview
  (refused in combat, `modules/Preview.lua:38`), the frame picker and the anchor work are already gated. The skin
  listener must go through `CM.RequestApply` and never touch anchors directly.
- **Pooled AceGUI widgets.** Paint every hand-acquired widget (§1c) through `Skin:PaintAce`. None of them sets
  `SetCallback("OnRelease")` today (`grep -rn OnRelease settings modules core` finds nothing), so there is no chain
  conflict. Until AM-G1 lands, the `AuraMasterDropdown` pool is never painted. That is safe, but stock.
- **The migration ladder.** The v13 step raises the stamp only if it does not raise (`core/Database.lua:455-472`). It
  must survive missing LibKa0s, which means setting the companions directly, with no Skin call needed. It must also
  survive containers with partial blocks: the backfill runs on load, so seed the companions defensively.
- **File cap (1500).** None of the authored code is at risk:
  - `defaults/Categories.lua` 1344 (data, untouched);
  - `modules/Anchors_Snap.lua` 1140;
  - `settings/Schema.lua` 1057 (gains the `skin.*` rows);
  - `modules/Style.lua` 1034 (gains the resolve);
  - `settings/Filters.lua` 1017;
  - `modules/Container.lua` 1008.

  Among the tests, `tests/test_filtercompiler.lua` (1311) and `tests/test_style.lua` (1205) are the closest. Put the
  skin cases in a new `tests/test_skin.lua` rather than growing `test_style.lua`. The documentation is already over
  1500 lines (`docs/test-cases.md` 2575, `docs/smoke-tests.md` 2295), and AM-05 adds per-skin smoke rows to it.
- **The General page tab budget.** Appearance is the last tab (AuraMaster has no Keybindings tab). It is drawn through
  AuraMaster's own `Helpers.RenderPage` mapping (`settings/General.lua:184-189`, `tabs = { GS.TABS[1], GD.TAB }`), so
  `O.AppearanceTab`'s `{key, label, tooltip, before, render}` has to fit that host tab shape.

## 9. Effort

**L.** AM-01 to AM-04 are each medium:
- a per-container R3 migration with the sentinel caution;
- the font and texture resolve, plus FontPrimer;
- about 13 hand-acquired widgets and a custom dropdown type that needs a library option;
- about eight furniture colors that need new tokens;
- docs that are already over 2,000 lines.

The HUD's secret-geometry constraints rule out the simple recorded-primitive route.
