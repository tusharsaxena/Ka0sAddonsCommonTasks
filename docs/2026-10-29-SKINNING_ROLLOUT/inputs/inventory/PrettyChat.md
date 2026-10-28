# Inventory: PrettyChat (prefix PC)

Read-only inventory for M0 of `docs/2026-10-29-SKINNING_ROLLOUT/`. Repo `../PrettyChat`, which was on branch
`feat/2026-10-29-skinning-rollout` at `ce135f7` (same commit as master) with a clean tree. It vendors LibKa0s
v1.77.0 (`CLAUDE.md:44`) and declares `LibKa0s icons: clear, close, copy` (`CLAUDE.md:45`). Library
references are to the LibKa0s main checkout at `4e1ae41` (v1.79.0).

**Shape of the addon.** PrettyChat is frameless (`core/Constants.lua:77-104`). It rewrites Blizzard chat
format strings, and its only `CreateFrame` is the event-only `PrettyChatCombatWatcher` at
`modules/Override.lua:218`. It draws no window, texture or font string of its own: `grep -rnE
'SetStatusBarTexture|LSM30_|CreateTexture|CreateFontString|SetBackdrop' core modules settings` prints
nothing. Everything visible comes from one of these:

- its settings pages (library chrome, plus AceGUI widgets that `settings/Panel.lua` and `settings/Profiles.lua`
  acquire themselves);
- lines it writes onto GameTooltip;
- library tool windows (the debug console and its copy window);
- the launcher (LibDBIcon);
- Blizzard StaticPopups;
- chat text.

**It has no HUD.**

## 1. Surfaces

"Lib-auto" means a library-drawn surface. It follows the skin with no PrettyChat code once
`Skin:RegisterOwner("PrettyChat")` has run, because the descriptor already passes the folder name as
`addonName` (§2).

### 1a. Library-drawn (lib-auto once the owner registers)

| # | Surface | Built at | Typed look today | Paints through |
|---|---|---|---|---|
| L1 | Settings main canvas, sub-page canvases, header title, breadcrumb, divider, header Defaults buttons, scroll + scrollbar | `settings/OptionsSetup.lua:269` (`lib:New`, `addonName = addonName` at :282); pages at `settings/Panel.lua:799` (General), `:815` (Categories), `settings/Profiles.lua:93` | none in PC | Options chrome → `S.Panel`/`S.Text`/`S.Divider`/`S.Button`/`S.ScrollBar`; `title.text`, `text.heading`, `divider`, `btn.*`, `scroll.*` |
| L2 | Categories page primary tab strip (8 category tabs, tooltips) | `settings/Panel.lua:690` (`H.TabStrip`) | none | `S.Tab` / `S.SetTabSelection`: `tab.*` |
| L3 | General page `Master controls` tab strip and composed rows (Enable, General visibility dropdown, Debug console, Minimap button, Test lead button, Reset all settings) | `settings/Panel.lua:158` (`H.RenderTabbedSchema`), `settings/Schema.lua:123` (`MASTER_SPEC`, `frameless = true`), `:887` | none | Library makers and the Options AceGUI proxy: `check.*`, `input.*`, `btn.*`, `tab.*` |
| L4 | Category Enable checkbox above the tree | `settings/Panel.lua:487` (`H.RenderField`) | none | Library maker: `check.*`, `text.body` |
| L5 | Landing page (logo, TOC notes, Slash Commands section heading and rows) | `settings/Panel.lua:768-774` (`LANDING_SPEC`), `:853` (`H.BuildLandingPage`) | Logo path `settings/Panel.lua:34-35` (brand art, see §4). Alias row gray, see H4 | Library: `text.heading`, `text.body` |
| L6 | Combat cover over open pages | library (OptionsCombat) | none | `S.Cover`: `cover.dim`, `cover.text` |
| L7 | Debug console window, its title bar, Copy, Clear and Close controls, toggle, Diagnostics link, log and line count | `core/DebugLogSetup.lua:177` (`lib:New`, `addonName = addonName` at :189, `font = NS.Const.FONT_MONO` at :193) | Font face: `core/Constants.lua:74-75` (JetBrains Mono through `NS.MediaFont`, falling back to `STANDARD_TEXT_FONT`) | DebugLogWindow (minor 22) through `Core.ApplySkin(frame, …, owner)`: `win.*`, `title.*`, `close.*`, `log.ts`, `log.tag`, `log.text`, `log.count`, `sem.on`, `sem.off`, `scroll.*` |
| L8 | Debug copy window (Copy in the console) | library (`WidgetsCopyWindow`, opened from the console) | none | Copy window: `win.*`, `input.*`, `btn.*` |
| L9 | Skin tab (new, PC-01) | `O.AppearanceTab` through `H.RenderTabbedSchema` opts.tabs on the General page | n/a | `OptionsAppearance` paints itself |
| L10 | First-run skin picker (new, PC-04) | `O.SkinPicker` | n/a | `OptionsSkinPicker` paints itself; it draws the Media icons `settings` and, when `onPreview` is given, `eye` |

### 1b. PrettyChat-acquired AceGUI widgets (PC-04: `Skin:PaintAce` / `PaintAceTree`)

`settings/Panel.lua:20` resolves `LibStub("AceGUI-3.0")` directly. That bypasses the Options AceGUI proxy,
so the library paints none of these and PC has to paint them itself.

| # | Widget | Built at | Typed look today | Paints through |
|---|---|---|---|---|
| A1 | `SimpleGroup` row1 (Flow) | `settings/Panel.lua:250` | none (no chrome) | No `SkinAce` painter (none needed) |
| A2 | `CheckBox` "Rewrite this message" | `settings/Panel.lua:254` | stock | `PaintAce` → `PAINT.CheckBox`: `check.*`, `text.body`, `text.disabled` |
| A3 | `Label` GLOBALNAME caption | `settings/Panel.lua:269`; gray escape at `:271` (`Color.gray` = `|cffaaaaaa`, `core/Constants.lua:39`) | `|cffaaaaaa` | `PaintAce` → `PAINT.Label` (font, `text.body`). The escape needs a token, see H1 and gap PC-G2 |
| A4 | `EditBox` Original (disabled) | `settings/Panel.lua:275` | stock | `PaintAce` → `PAINT.EditBox`: `input.bg`, `input.border`, `input.text`/`text.body`, `text.disabled`, `input.focus` |
| A5 | `EditBox` New | `settings/Panel.lua:292` | stock | `PAINT.EditBox` (as A4) |
| A6 | `EditBox` Preview (disabled). It shows the rendered sample with the player's own `|c` escapes; error text is gray | `settings/Panel.lua:303`; refresh `:349-350`; error gray from `modules/Override.lua:607` (`renderOrError`, `Color.gray`) | `|cffaaaaaa` on error | `PAINT.EditBox`. The error gray needs a token (H1 / PC-G2). The player's sample colors stay as they are (§4 E7) |
| A7 | `SimpleGroup` resetRow | `settings/Panel.lua:316` | none | none needed |
| A8 | `Button` "Reset message" | `settings/Panel.lua:319` | stock | `PaintAce` → `PAINT.Button`: `btn.*` |
| A9 | **`TreeGroup`**: the string list pane plus the editor content pane. Row buttons `OptionsListButtonTemplate`, selected row `LockHighlight`, tree scrollbar `UIPanelScrollBarTemplate`, dragger | `settings/Panel.lua:510-534` | AceGUI stock (TreeGroup v49, `libs/AceGUI-3.0/widgets/AceGUIContainer-TreeGroup.lua:621-689`): see gap PC-G1 | **No `SkinAce` painter for TreeGroup** (`LibKa0s/SkinAce.lua` has `PAINT.Button/CheckBox/Slider/EditBox/MultiLineEditBox/Heading/Label/InteractiveLabel/Icon/ColorPicker/InlineGroup/ScrollFrame/Dropdown` only). Gap **PC-G1** |
| A10 | Profiles page: a `SimpleGroup` container plus everything `AceConfigDialog:Open` draws into it (AceDBOptions dropdowns, buttons, edit box, descriptions, headings) | `settings/Profiles.lua:72-79` (container), `:110` (`libs.dialog:Open(APP, container)`) | stock | `Skin:PaintAceTree(owner, container)` **after every `Open`**, as LootHistory's `settings/Profiles.lua:69` does; repeated on every redraw (`settings/Profiles.lua:121-141`) |

`buildStringRow` (`settings/Panel.lua:242`) puts A1 to A8 into the TreeGroup content pane. A single
`Skin:PaintAceTree(owner, tree)` after `buildStringRow` reaches all of them, because `PaintAceTree`
recurses `children` even where the container itself has no painter. Panel.lua sets no `OnRelease` of its own,
so no `Skin:OnRelease` chaining is needed today.

### 1c. Host-typed colors on library or Blizzard surfaces (PC-02)

| # | Text | At | Today | Token |
|---|---|---|---|---|
| H1 | Gray note text on the settings pages: the A3 caption, the A6 error, and "(original not available)" in the panel | `settings/Panel.lua:271`, `modules/Override.lua:607` | `|cffaaaaaa` (0.667) | **No exact token.** `text.muted` = 0.7/0.7/0.72 (`|cffb3b3b8`); `cover.text` = 0.667 is exact but means the combat cover's text. Gap **PC-G2** (`text.note`). Write it through a host `NS.SkinEscape(name)` like LootHistory's `core/SkinSetup.lua:215` |
| H2 | Categories page footnote (`H.TextRow`) | `settings/Panel.lua:708-710` | `|cffaaaaaa` | as H1 |
| H3 | GameTooltip lines PC writes for a tree row: title, GLOBALNAME line, body | `settings/Panel.lua:425-436` (`showStringTooltip`) | title `SetText(label, 1, 1, 1)` `:427`; GLOBALNAME `|cffaaaaaa` `:428`; "(original not available)" / error `|cffaaaaaa` `:430`, `:433`; body is the rendered sample `:435` | Title: `gtip.value` (WHITE, exact). Doubtful D2, because the library's own `O.AttachTooltip` (`LibKa0s/OptionsWidgets.lua:524`) still types 1,1,1. Gray lines: no exact `gtip.*` (`gtip.subtle` = 0.7, `gtip.muted` = 0.5). Gap **PC-G2** (`gtip.note`). The sample keeps its own colors (§4 E7). GameTooltip's frame is never touched (§4 E2) |
| H4 | Landing page alias row "/prettychat is an alias for /pc" | `settings/Panel.lua:761` | `|cffaaaaaa` | as H1 (`text.note`) |

## 2. Library factories that take an owner

| Factory | Call site | Owner today | Action |
|---|---|---|---|
| `LibKa0s-Options-1.0` `lib:New` | `settings/OptionsSetup.lua:269` | `addonName = addonName` (`:282`) | None. Once registered it becomes the owner (Options minor 31 and later) |
| `LibKa0s-DebugLog-1.0` `lib:New` | `core/DebugLogSetup.lua:177` | `addonName = addonName` (`:189`); no `skin` or `applySkin` (`:227-236`), so the owner is honored (`LibKa0s/DebugLog.lua:305`) | None. See D4 on `font` |
| `Core.MakeCloseButton` via `NS.MakeCloseButton` | `core/CoreSetup.lua:162-164` | `addonName` | None (no caller today) |
| `O.AppearanceTab(spec)` / `O.AppearanceRows` | new, PC-01 | `spec.owner` defaults to the descriptor's `addonName` | Pass `get`/`set` = the skin seam |
| `O.SkinPicker(spec)` / `O.HideSkinPicker()` | new, PC-04 | defaults to `addonName` | `get`, `set`, `page = "General"`, `onClose` writes `skin.pickerSeen` |
| `Skin:PaintAce` / `PaintAceTree` / `OnRelease` | new, PC-04 (A2-A10) | explicit `owner` argument | Bind the owner in `core/SkinSetup.lua` (`NS.SkinPaintAce(w)` / `NS.SkinPaintAceTree(c)`, LootHistory's `core/SkinSetup.lua:588-596`) |
| `LibKa0s-Launcher-1.0` `Launcher:New` | `core/LauncherSetup.lua:120` | takes no owner (not skin-aware in v1.79.0) | None. The minimap button is LibDBIcon's (§4 E4) |
| Core printer `lib:New`, Schema, Slash, Lifecycle, Env, Media | various | not visual | None |

No Widgets factory (dropdown, search box, test strip, autocomplete, drag handle, reorder list, line chart) is
called anywhere in PC.

## 3. HUD style settings

**No HUD.** The schema is bool and string only, with no color, font, border, bar or `LSM30_` row
(`settings/OptionsSetup.lua:335-339`; `tests/test_surface_parity.lua:166-182` lists `ColorPair`,
`FontGroup`, `BorderGroup` and `BarGroup` as live-only because nothing calls them). Nothing for
`S.Resolve`, `Skin.FROM_SKIN`, a `fromSkin` companion or the O2 reset. **PC-03 is an exception**, with this
proof command:

```
cd ../PrettyChat && ! grep -rnE 'SetStatusBarTexture|LSM30_|CreateTexture|CreateFontString|SetBackdrop|type = "color"' core modules settings defaults \
  && [ "$(grep -rn 'CreateFrame(' core modules settings | wc -l)" = 1 ]   # the one hit is modules/Override.lua:218, the event-only PrettyChatCombatWatcher
```

No migration step is owed, so `core/Database.lua` `SCHEMA_VERSION` does not move for O2. New `skin.*` keys
are new defaults, not a stored-path move, so they need no step either (the same reasoning as
`defaults/Profile.lua:26-32`).

## 4. Exceptions

| # | Rung | What | Where | Reason |
|---|---|---|---|---|
| E1 | 3 | `PRETTYCHAT_RESET_ALL`, `PRETTYCHAT_RESET_CATEGORIES` StaticPopups | `settings/Panel.lua:43-78` | skinning-§7: never a StaticPopup |
| E2 | 3 | GameTooltip's frame (only PC's lines are recolored, H3) | `settings/Panel.lua:425-436` | skinning-§7 |
| E3 | 3 | Blizzard SettingsPanel chrome and the AddOns list (TOC `## IconTexture`, rainbow `## Title`) | `PrettyChat.toc:2,6` | skinning-§7. The Title escapes are a ratified `toc-file-§1` deviation (brand mark) |
| E4 | 3 | LibDBIcon minimap button, the launcher tooltip and the Blizzard context menu | `core/LauncherSetup.lua:114-215` | Third-party and Blizzard frames. Launcher-1.0 takes no owner, and drawing tooltip lines yourself is anti-pattern #89 |
| E5 | 4 | Brand art: landing logo `prettychat.logo.tga`, launcher icon `prettychat.logo.128.tga` | `settings/Panel.lua:34-35`, `core/LauncherSetup.lua:115-116` | Branding art, the same in every skin (launcher-§4 requires the same file in all three places) |
| E6 | 4 | Chat output palette: the `[PC]` cyan prefix (brand mark), the slash-commands-§5 schema palette (`listHead` 33ff99, `azure` 3399ff, `yellow`, `white`), `note()` / `cmd()` | `core/Constants.lua:37-56`, `core/Util.lua:27,32`, `settings/Slash.lua:372,391` and every `NS.Print` | Chat text is not a frame the addon draws, and §5's codes are a MUST ("MUST NOT be substituted", `core/Constants.lua:45-47`) |
| E7 | 4 | The product's content: shipped default format strings (79 escapes in `defaults/Defaults.lua`, e.g. `:20`), the player's own formats, and their rendered samples in the Preview EditBox and the tooltip body | `defaults/Defaults.lua`, `settings/Panel.lua:349,435` | These are the player's chat colors (the addon's output), not chrome |
| E8 | 4 | `/pc test` report markup: brand-green labels `Name:` / `Original:` / `Formatted:`, gold `Category:`, gray errors. The same lines go to chat and to the debug console | `modules/Override.lua:17-19,665,681` | Report content shared with the chat path. The console's own ts, tag and text colors follow the skin (L7). See D3 |

## 5. Gaps (rung 2)

### PC-G1: `SkinAce` has no TreeGroup painter (primitive-option: `PAINT.TreeGroup` for `Skin:PaintAce`)

- **Why no primitive fits.** The TreeGroup is a **pooled AceGUI container** shared with every addon's
  AceConfigDialog. skinning-§7 requires that whatever a paint changes is restored on `"OnRelease"`, and only
  `Skin:PaintAce` gives that. Composing facade primitives on its sub-frames (`S.Panel` on
  `treeframe`/`border`, `S.NavItem` on the row buttons, `S.ScrollBar` on the tree scrollbar) records them in
  `lib.painted`, and nothing restores them: `Skin:Untrack` (`LibKa0s/Skin.lua:707`) only forgets. The next
  addon that acquires the TreeGroup would inherit PC's skin, which is the leak anti-pattern #107 names.
  `PaintAceTree(tree)` still paints the editor widgets inside, but leaves the two panes, the row buttons and
  the tree scrollbar stock under every skin.
- **No new token needed.** `nav.*` already describes exactly this look. OptionsNav was built as "AceGUI's
  TreeGroup tree pane" (`LibKa0s/OptionsNav.lua:12`), and its `PANE_FILL`/`PANE_BORDER` (`:63-64`) are
  TreeGroup's stock values.
- **What Ka0s Default must reproduce** (AceGUI TreeGroup v49, `libs/AceGUI-3.0/widgets/AceGUIContainer-TreeGroup.lua`):
  - tree pane and content pane backdrop `PaneBackdrop`: bg `Interface\ChatFrame\ChatFrameBackground`, edge
    `Interface\Tooltips\UI-Tooltip-Border`, edgeSize 16, insets 3/3/5/3 (`:621-626`). Fill `0.1, 0.1, 0.1,
    0.5`, border `0.4, 0.4, 0.4` (`:645-647`, `:687-689`). Maps to `nav.bg` = {0.1,0.1,0.1,0.5} and
    `nav.border` = {0.4,0.4,0.4,1}: **exact**;
  - row buttons `OptionsListButtonTemplate` (`:320`). Level 1 text `GameFontNormal` (gold 1, 0.82, 0) and
    hover `GameFontHighlight` (white) (`:76-77`), deeper levels `GameFontHighlightSmall` (`:80-81`). Maps to
    `nav.text` GOLD and `nav.selText` WHITE: **exact**;
  - selected row `LockHighlight` (`:68`), the template's `UI-QuestLogTitleHighlight` ADD highlight. Maps to
    `nav.selBg` = {0.3,0.5,1,1}, OptionsNav's tint of the same texture (`OptionsNav.lua:52-53,176`);
  - tree scrollbar `UIPanelScrollBarTemplate`, width 16, with a `BACKGROUND` texture `0, 0, 0, 0.4`
    (`:670-682`). The `scroll.track` that `PAINT.ScrollFrame` uses is `0.24, 0.24, 0.27, 0.4` in Ka0s Default,
    so the tree scrollbar's look would move slightly (D5);
  - the dragger stays transparent (`:664`).
- **Recurrence.** PrettyChat is the only addon in the collection that acquires a TreeGroup itself
  (`grep -rn 'TreeGroup")'` over the addons' `core/`, `modules/` and `settings/`). Any AceConfigDialog page
  with a tree, which the library already proxies, would also benefit.
- **Fallback if M1 declines it:** record A9 as an exception (the TreeGroup stays AceGUI stock in every skin)
  and paint only its children.

### PC-G2: no token answers PrettyChat's gray note text `#aaaaaa` (tokens `text.note`, `gtip.note`)

- **Why no token fits.** No Ka0s Default token rounds to `aa aa aa` apart from `cover.text`
  (`LibKa0s/SkinDefs.lua:297`, {0.667,0.667,0.667,1}). That token means the combat cover's text, and other
  skins tune it for that role. `text.muted` = {0.7,0.7,0.72} gives `b3b3b8`, `gtip.subtle` = {0.7,0.7,0.7}
  gives `b3b3b3`, and `gtip.muted` = DIM 0.5 gives `808080`. Using any of them would change Ka0s Default's
  pixels, which the plan says must stop for the owner. A tooltip gray needs a `gtip.*` of its own, because
  "no skin darkens a gtip one" (`SkinDefs.lua:57`).
- **Recurrence.** `|cffaaaaaa` appears in the authored code of AuraMaster, ConsumableMaster and QuickComms
  as well as PrettyChat.
- **What Ka0s Default must reproduce:** `text.note` = `{ 0.667, 0.667, 0.667, 1 }` (`|cffaaaaaa`,
  `core/Constants.lua:39`), used at `settings/Panel.lua:271,708-710,761` and `modules/Override.lua:607`.
  `gtip.note` = the same value, used at `settings/Panel.lua:428,430,433`. The other skins can derive
  `text.note` from `text.muted` and `gtip.note` from `gtip.subtle` (FOLLOW).

## 6. Doubtful calls (for DECISIONS.md)

- **D1. PC-G2 or an existing token.** Recommendation: add `text.note` and `gtip.note` in M1, since three
  more addons share the gray. If the owner prefers no new tokens, `text.muted` and `gtip.subtle` are the
  nearest, but they change Ka0s Default by 9 levels per channel and need the owner's word.
- **D2. Tooltip title color** (`settings/Panel.lua:427`, `1, 1, 1`). Recommendation: `S.Color("gtip.value")`
  (WHITE, exact on Ka0s Default). The library's own `O.AttachTooltip` still types 1,1,1, so a library item
  could move both onto one token later; `gtip.value` is close enough for now.
- **D3. `/pc test` report markup in the skinned debug console** (E8). Recommendation: keep it as report
  content, not chrome. The same lines are printed to chat, and their palette is the brand green and the
  §5-style gold.
- **D4. The console font** `font = NS.Const.FONT_MONO` (`core/DebugLogSetup.lua:193`). DebugLogWindow
  applies `d.font` to the log and the line count (`LibKa0s/DebugLogWindow.lua:356,408`), not `font.mono`.
  Recommendation: keep it. The console is the library's frame, and Ka0s Default's `font.mono` is the same
  JetBrains Mono. A library item could later make the console read `font.mono` for an owner.
- **D5. TreeGroup scrollbar under Ka0s Default** (PC-G1). Recommendation: use `scroll.track` like
  `PAINT.ScrollFrame` does, for consistency with every other painted AceGUI scrollbar. This differs from
  stock `0,0,0,0.4`; if the owner wants the stock value exactly, the painter could leave the track art alone
  under `ka0s`.
- **D6. Picker preview.** PrettyChat has no test mode. Recommendation: pass
  `onPreview = function() PrettyChat:TestToConsole() end` (`settings/Panel.lua:130`), which opens the
  skinned console with a report, and declare both `eye` and `settings`. The other option is to omit
  `onPreview`, which hides the eye, and declare `settings` only.
- **D7. Schema path for the skin keys.** The plan names `skin.*`, but PC's paths are `<Category>.<…>` with
  per-row `get`/`set` closures (`settings/Schema.lua:826-828`). Recommendation: store them under
  `db.profile.skin.{source,skin,ignorePanel,ignoreFonts,font,texture,pickerSeen}` with schema paths
  `skin.*`, `page = "General"`, `group = "Appearance"`, `skipRender = true`, declared in
  `defaults/Profile.lua`'s `NS.ProfileDefaults.profile.skin`. Check that `/pc list`'s category listing
  (`settings/Slash.lua:372`) does not present `skin` as a message category.
- **D8. The skin rows' write tail.** `Schema.Set`'s `announce` runs `PrettyChat:ApplyStrings()` for every row
  that is not `sessionOnly` (`settings/Schema.lua:837-839`). A skin pick would then re-apply all 79 format
  globals for nothing. Recommendation: skip the re-apply for `skin.*` rows (a row flag such as
  `noReapply = true` read in `announce` and in `ResetRows`'s `reapply` at `:1068`), keeping the
  `NotifyPanelChange`.

## 7. Re-vendor v1.77.0 → v1.79.0 obligations (PC-RV)

1. **Options degradation stub** (`settings/OptionsSetup.lua`, the stub table that ends at `:257`) gains
   `AppearanceTab` and `AppearanceRows` (v1.78.0) and `SkinPicker` and `HideSkinPicker` (v1.79.0). Without
   them, `tests/test_surface_parity.lua:141` (`assertSurfaceParity(parityBare.NS.Helpers,
   "LibKa0s-Options-1.0", …)`) is red. LootHistory's shape (`settings/OptionsSetup.lua:140-153`):
   `AppearanceTab = function() return { key = "Appearance", label = "Skin", render = noop } end`,
   `AppearanceRows = function() return nil end`, `SkinPicker = function() return nil end`,
   `HideSkinPicker = noop`. `APPEARANCE_STRINGS` and `SKIN_PICKER_STRINGS` are lib-level, not instance
   members, so no live-only entry is needed.
2. **Whole-folder copy** from the run's tag via `git archive`: new files `Toast.lua`,
   `OptionsSkinPicker.lua`, `OptionsAppearance.lua`, `SkinAce.lua`, `WidgetsCopyWindow.lua`,
   `DebugLogWindow.lua`, the Skin major's files, the new fonts (Oxanium plus seven skin families) and the bar
   textures. `tests/_kit/` is copied whole too (kit revision 44 at v1.79.0; PC is on 42 per
   `docs/testing.md:125`).
3. **Provenance line** `CLAUDE.md:44` becomes `v1.79.0` (or v1.80.0 if M1 releases).
   `tests/test_vendor_sync.lua` reads it by pattern, so no literal pin moves there.
4. **Icons line** `CLAUDE.md:45` becomes `clear, close, copy, eye, settings`. The picker draws `settings`, and
   `eye` too if D6 is accepted. Then run the tag's `tools/prune-icons.lua`. `tests/test_libka0s.lua:543-568`
   checks only that `info` is absent, so it stays green. Add `OFL`/`LICENSE` credits in the README to match
   (step 6).
5. **Version-stamped docs** that name v1.77.0: `docs/ARCHITECTURE.md:363`, `docs/module-map.md:183` (the XML
   load list gains Toast, Skin, SkinDefs, SkinPaint*, SkinAce, SkinEUI, OptionsAppearance,
   OptionsSkinPicker, WidgetsCopyWindow, DebugLogWindow in the tag's order), `docs/testing.md:125`.
   Historical mentions such as `core/Constants.lua:91` and the smoke ids DIAG-26/27 stay.
6. **Ka0s Default looks different at the re-vendor** (CHANGELOG v1.79.0 "What a consumer owes"), but only for
   a registered owner, so nothing changes visibly before PC-01. **README font credits** (`README.md:98-99`
   names JetBrains Mono only) gain Oxanium and the seven skin faces (Inter, Vollkorn, Nunito, Atkinson
   Hyperlegible, Bitter, Philosopher, Fira Sans), all SIL OFL 1.1, as LootHistory's `README.md:151-162` does.
7. **TOC** (PC-01): add `EllesmereUI` to `## OptionalDeps` (`PrettyChat.toc:8`, skinning-§5), and
   `core\SkinSetup.lua` after `core\CoreSetup.lua` with its load-order note. The test loader reads the TOC.
8. **Test pins that will move:** the schema row counts and snapshot (`tests/settings_snapshot.lua`,
   `tests/test_schema.lua`, `tests/test_panel_categories.lua`), and the "measured stub set" case
   (`tests/test_libka0s.lua:571-586`). The library-absent load must build the same rows, so the `skin.*`
   rows have to be declared host-side, not through a library composer. Also `tests/test_doc_structure.lua`
   for the new docs and the test badge count `README.md:7`.

## 8. Risks

- **Pooled AceGUI.** A1-A10 are pooled widgets. Paint them only through `Skin:PaintAce`/`PaintAceTree`,
  never with facade primitives. Panel.lua re-renders on every tab or string click (`buildCategoriesBody`
  → `ClearScroll`) and the widgets are released and re-acquired, so the paint has to happen after every
  build. The TreeGroup stays unpainted until PC-G1 lands. The Profiles container is reused across redraws and
  `AceConfigDialog:Open` re-acquires its children, so it needs `PaintAceTree` after each `Open`.
- **Live repaint of open settings pages** happens through the library's re-render. PC's own bespoke pane is
  repainted only if PC re-runs the paint: subscribe `NS.Skin.OnLooksChanged` → `NS.Config` refresh, or rely
  on the next-frame re-render of the page (skinning-§2).
- **Profile events.** Re-apply the choice in the shared adopt path `reloadProfile` (`core/PrettyChat.lua:77-103`,
  which already calls `NS.Config.RefreshProfilesPage`), and hide or re-queue the picker there.
- **The stand-down latch.** The picker must not show while the addon is stood down (`NS.Lifecycle`,
  `core/LifecycleSetup.lua`; `tests/test_disabled.lua` asserts that "disabled" means inert). Skin writes
  must still work while disabled (setup, not feature).
- **Combat.** The picker queue and the Appearance tab handle their own combat refusal. Show the picker from
  `OnEnable` deferred (LootHistory uses `NS.After(2, …)`), never mid-combat on its own.
- **Taint.** None expected. No Blizzard frame is touched, and the StaticPopups and GameTooltip frame are left
  alone.
- **Frameless invariant.** The picker and the Skin tab are library frames, so `tests/test_layers.lua`
  (no strata or level set in `core/`, `modules/` or `settings/`) stays true. Do not add a strata call.
- **Performance.** There is no hot path. The only cost is D8 (an `ApplyStrings` pass per skin write) if
  it is not fixed.
- **File cap.** Nothing is near 1500 lines. Largest authored files: `settings/Schema.lua` 1115 (gains about
  50 lines of skin rows), `tests/test_libka0s.lua` 936, `tests/test_override.lua` 905, `settings/Panel.lua`
  854, `modules/Override.lua` 755. The generated `GlobalStrings/` is carved out (layout-§1).

## 9. Effort

**M.** There is no HUD and no window of its own. The work is the seam, seven skipped schema rows, the tab,
the picker, painting the bespoke Categories pane and the Profiles page, four escape sites, the re-vendor's
four stub members, and docs and tests. Two upstream gaps (a TreeGroup painter and two tokens) gate parts of
PC-02 and PC-04.
