# LibKa0s internals: design input for the skin module

Read-only survey of `../LibKa0s` at `e9e2d53` (master, v1.77.0, kit revision 42), taken 2026-10-25.
Paths are relative to `../LibKa0s/` unless another repo is named. "The payload" means the inner
`LibKa0s/` folder that every consumer vendors to `libs/LibKa0s/`.

## 1. Module conventions

### Adding a new LibStub major

The Glow major (`LibKa0s/Glow.lua:52-63`, added at v1.75.0) is the smallest template:

1. **The file.** Floor on Core before registering: `local core = LibStub("LibKa0s-Core-1.0", true)`,
   `NEEDS_CORE = 1`, `return` before `NewLibrary` if the floor fails (`Glow.lua:52-54`). This leaves
   the module absent rather than half-wired. Then `LibStub:NewLibrary(MAJOR, MINOR)`, `lib.MAJOR,
   lib.MINOR`, and `lib.MODULES = lib.MODULES or {}; lib.MODULES.<File> = MINOR` (`Glow.lua:56-63`).
   State that must survive a minor upgrade is written `lib.x = lib.x or {}`. The CCN-15 ceiling rules
   out large branchy painters, so use data tables (Core's `ACCENTS`, `Core.lua:113-116`).
2. **`LibKa0s/LibKa0s.xml`** gets a `<Script file=...>` row. Load order matters: Core loads first and
   Media tenth. Core cannot use Media at load time, which is why `MakeCloseButton` resolves Media at
   call time (`Core.lua:244-247`). `tests/run.lua:24` derives the headless load list from this XML.
3. **`tests/majors.lua`** gets a `MAJORS` row: `major`, `files` (in XML order), `primary`, optional
   `paired`. `tests/test_versioning.lua` and `tools/gen-api-members.lua` both iterate it
   (`tests/majors.lua:1-12`). A major in the XML but missing from this table is checked by nothing.
4. **`CHANGELOG.md`**: the release's version block names every file's new minor and the major's
   version key. `tests/test_versioning.lua:107` fails when the block and `lib.MODULES` disagree.
5. **`docs/api/<Major>/version-<key>-docs.md`**: the key is every file's minor joined with `.` in
   XML order (`tests/test_versioning.lua:150-163`, folder from `apiFolder`, `:146`). Skeleton (Glow):
   Status/Supersedes/Superseded-by table, then *What this major is*, *Members*, *Adopting it*, *What
   is not here*, *Vendoring*. Add a row to `docs/api/README.md` too. `test_versioning.lua:165` fails
   if the document is missing.
6. **`lua tools/gen-api-members.lua`** writes `docs/api/<Major>/members-<key>.json`.
   `test_versioning.lua:192` regenerates it and compares.
7. **New suites** must be listed by name in `tests/run.lua:83-107`. `Kit.assertSuiteInventory`
   reconciles that list against disk.
8. **Outside the repo:** `README.md`'s module table (`README.md:38`, `:128`), `docs/releasing.md`'s
   minor list (step 2, `:28-39`) and paired-guard list (`:454-455`), its *Consumers* table, and
   upstream `WowAddonStandards/standards/standards/library-stack.md:92` (the module table) and
   `:128` ("Sixteen of the seventeen majors floor on Core"). That makes this a standards change too.
9. **The kit revision** (`Kit.VERSION = 42`, `testkit/framework.lua:20`) moves only if `testkit/`
   changes: bump it, write `docs/api/testkit/version-<n>-docs.md`, and re-copy `testkit/` to
   `tests/_kit/`. `tests/test_kitsync.lua` compares the two byte for byte (`docs/releasing.md:26-27`,
   `:413-437`).

### Secondary files paired on a shell's minor

A major can span files: Widgets has five, Options twelve and Sim three. The primary owns `MINOR`.
Each secondary file looks the major up with `LibStub(major, true)` (no `NewLibrary`), carries its own
`<X>_MINOR`, and guards itself on both numbers (`WidgetsLineChart.lua:28-41`):

```lua
if lib.__chartMinor and lib.__chartMinor >= CHART_MINOR
  and lib.__chartShellMinor == lib.MINOR then return end
lib.__chartMinor, lib.__chartShellMinor = CHART_MINOR, lib.MINOR
lib.MODULES.WidgetsLineChart = CHART_MINOR
```

The secondary therefore re-runs when the winning shell changes, and never attaches to a shell from a
different vendored copy. `tests/test_versioning.lua:130-145` asserts `lib[probeField] == lib.MINOR`
and `lib[minorField] == lib.MODULES[file]` for every `paired` row. Options goes further: its
secondaries publish `lib.__AttachX(O, d)`, and `lib:New` calls each one behind an `if
lib.__AttachX then` guard. A partial copy then degrades at call time instead of failing at load
(`docs/releasing.md:457-485`). Adding a file to an existing major moves that major's version key,
which means a new API document.

### What v1.78.0 requires (`docs/releasing.md:15-262`)

1. Green gate: `lua tests/run.lua` (Lua 5.1) and `luacheck .` at 0/0.
2. Bump the minor of every changed file. A file you did not touch does not move.
3. New major or new file: add the `tests/majors.lua` row.
4. Add the CHANGELOG version block.
5. Write the API document for every major whose minor moved: copy the current one, mark the old one
   Superseded with a *Moving to...* section, add the README row, regenerate the manifests. A Sim or
   `W.TestStrip` change also triggers the preview and simulation re-look.
6. `lua tests/run.lua --list` into `docs/test-cases.md` (CRLF).
7. Roll the provenance template (`releasing.md:315`) and the README standards pointer, run the green
   gate, commit, then on a clean tree run `tests/_kit/run-automated-tests.sh --release 1.78.0`.
   Write `ANALYSIS.md`, add the release-gate and *Preview and simulation re-look* lines to the
   CHANGELOG, and commit the bundle as a second commit. Check the tag's hard preconditions against
   `manifest.json`: release not null, `dirty` false, lint/tests/complexity `pass`,
   `complexity.warnings` 0 (`:190-219`). Then tag the second commit with a **local annotated tag**,
   the practice recorded in `CHANGELOG.md:1602` and `:1669` ("Tagged locally, not published") and at
   `releasing.md:600`. The push waits on the owner.
8. **Re-vendor every consumer**, as part of the release and not a follow-up (`:246-249`):
   `cp -r LibKa0s/. <Addon>/libs/LibKa0s/`, run both `diff -r`, roll the CLAUDE.md provenance line
   with the `LibKa0s icons:` line under it, then `lua tools/prune-icons.lua <Addon>`, then the
   addon's gate (`:283-290`). Always the whole folder, never one module (`:441-456`). Re-vendor from
   the tag, because each consumer's `test_vendor_sync` resolves the tag its provenance line names
   (`:387-391`).
9. Re-sweep the Consumers table.

### The 1500-line cap and CCN 15

`layout-§1` caps every authored `.lua` file at 1500 lines, `tests/` and `testkit/` included. The kit
gate is `tests/_kit/test_layout_cap.lua`, and its census lives under `CLAUDE.md` *Files over the
1500-line cap* (`CLAUDE.md:97-146`). Files between 1000 and 1500 lines are on notice and carry a
tracked register row (`CLAUDE.md:80`).

These band files are relevant here: `OptionsWidgets.lua` (1444, trigger 1450 or the next maker),
`OptionsIds.lua` (1375), `OptionsTabs.lua` (1350, trigger the next member), `Options.lua` (1320,
trigger the next member), `OptionsIdList.lua` (1251), `DebugLog.lua` (1008, trigger the next window
feature, seam `DebugLogWindow.lua`) and `testkit/mock_base.lua` (1464, re-check at 1490 or more than
30 added lines). **Retrofitting skin calls into the Options files will fire several triggers.**
Painting should go through a thin `S.<Primitive>(owner, frame, ...)` call, not inline code, and new
kit mocks belong in a sibling file, not `mock_base.lua`.

CCN 15 is a release gate (`automated-tests-§3`), measured by the kit's sighted lizard. Raw `lizard`
cannot see Lua functions.

## 2. Hardcoded visual constants a skin must replace

Kind: **L** = library-built frame (CreateFrame, BackdropTemplate, textures); **A** = AceGUI widget
(shared and pooled across addons); **B** = Blizzard template or atlas.

| file:line | Name | Value | Paints | Kind | Skin token |
|---|---|---|---|---|---|
| Core.lua:92-107 | `lib.SKIN` | bg/edge WHITE8x8, edgeSize 1, insets 1, bg `.06,.06,.08,.92`, border `0,0,0,1`, innerBorder/divider `.24,.24,.27,.85`, title `1,.82,0` | every Ka0s tool window via `ApplySkin` (`:181-188`); hosts call it 78 times on their own frames | L | `window.bg`, `window.border`, `window.innerBorder`, `divider`, `title`, `edgeFile`, `edgeSize` |
| Core.lua:142-152 | inner border | child BackdropTemplate frame, 1px inset | 1px highlight | L | `window.innerBorder` |
| Core.lua:207-212 | `CLOSE_SIZE/ART`, `CLOSE_REST`, `CLOSE_HOT` | 18/12, `.7,.7,.72`, `1,.3,.3` | close X tint, rest/hover | L | `close.rest`, `close.hot` |
| Core.lua:261 | glyph fallback | `GameFontNormalLarge`, U+00D7 | close with no Media | L | `font.large` |
| Core.lua:567-569 | resize grip | `UI-ChatIM-SizeGrabber-*` | resize grip | B | `grip` (optional) |
| Widgets.lua:85-91 | `SKIN` (file-local) | fill `.1,.1,.12,.9`, line `.24,.24,.27,.9`, focus `1,.82,0,.9`, height 20 | dropdown button, SearchBox | L | `control.fill`, `control.border`, `control.focus`, `control.height` |
| Widgets.lua:95-96 | `CHEVRON_FALLBACK`, `CHECK_FALLBACK` | Blizzard paths | dropdown arrow and menu check | B | `icon.chevron`, `icon.check` |
| Widgets.lua:107,123,140 | menu fonts | `GameFontHighlightSmall` | popup rows | L | `font.small` |
| Widgets.lua:147 | menu row hover | `1,.82,0,.15` | popup row highlight | L | `accent` at alpha `.15` |
| Widgets.lua:198-204 | menu text | selected `1,.82,0`, normal `.9,.9,.9` | popup row text | L | `text.selected`, `text.normal` |
| Widgets.lua:223-232 | shared popup `menu` | `.06,.06,.08,.98` / `0,0,0,1` | the one popup menu for all addons | L | `menu.bg`, `menu.border` |
| Widgets.lua:343-348,368,383 | Dropdown | `SKIN.fill/line`, `GameFontHighlightSmall`, arrow `.7,.7,.72` | dropdown button | L | `control.*`, `icon.tint` |
| Widgets.lua:496,514-539 | SearchBox | `SKIN.fill`, focus border, icon `.7,.7,.72`, hint `GameFontDisableSmall` | search box | L | `control.*`, `text.disabled` |
| Widgets.lua:577-579,652-712 | CopyWindow | backdrop `.06,.06,.08,.95`, title `GameFontNormal`, `UIPanelScrollFrameTemplate` | export window | L+B | `window.bgDense`, `font.normal`, scrollbar |
| Widgets.lua:791-794,842 | `STRIP_FILL` | test `1,.65,.15,.12`, sim `.35,.8,1,.12`, `GameFontNormalSmall` | test/sim strip | L | `strip.test`, `strip.sim` (semantic, may stay fixed) |
| WidgetsAutocomplete.lua:60,66-72 | `lib.AUTOCOMPLETE` (published) | BORDER `.24,.24,.27,.9`, BG `.1,.1,.12,.9`, TEXT `.9,.9,.9`, HIGHLIGHT `1,.82,0,.15`, FONT `GameFontHighlightSmall` | suggestion list; inherits the box's backdrop colors first (`:181-182`) | L | `control.*`, `text.normal`, `accent` |
| WidgetsDragHandle.lua:145,149 | help/close fallbacks | Blizzard paths | handle marks | B | `icon.*` |
| WidgetsDragHandle.lua:172-173 | `HELP_TINT(_OVER)` | `.7,.7,.72` / `1,1,1` | help mark | L | `icon.tint`, `icon.hot` |
| WidgetsDragHandle.lua:179 | `LABEL_FONT_DEFAULT` | `GameFontNormalSmall` | handle label | L | `font.small` |
| WidgetsDragHandle.lua:507,542 | strip bg, label | `0,0,0,.75`, `1,.82,0` | drag strip | L | `handle.bg`, `title` |
| WidgetsReorder.lua:85-92 | `lib.ROW_BOX` (published) | FILL `1,1,1,.06`, DIM `.03`, EDGE `.12`, EDGE_DIM `.06` | reorder rows | L | `row.fill`, `row.edge` |
| WidgetsReorder.lua:33,117,123 | handle art, ghost | `UI-SortArrow`, ghost bg `.12,.12,.12,.95`, `GameFontNormal` | drag ghost | L | `row.ghostBg` |
| WidgetsReorder.lua:418-422,494,648-649 | per-opts defaults | icon white, text `1,.82,0`, line `1,.82,0,.9`, handle `.7,.7,.7` / gold | ghost, drop line, handle | L | `accent`, `icon.tint` |
| WidgetsLineChart.lua:50-56 | `lib.LINE_CHART` (published) | AXIS `.45,.45,.5,.8`, GRID `1,1,1,.07`, CROSSHAIR `1,1,1,.35`, MARKER `.8,.8,.8,.6`, LINE `.4,.6,.95,1`; labels `GameFontDisableSmall` (`:304`) | chart | L | `chart.*` |
| Options.lua:629-643 | panel header | `GameFontNormalHuge`; atlas `Options_HorizontalDivider` tinted to the title color | settings page title and rule | B | `font.huge`, `title`, `divider` |
| Options.lua:775 | Defaults button | AceGUI `Button` | header button | A | Button primitive |
| Options.lua:859 | page scroll | AceGUI `ScrollFrame` | body | A | ScrollBar primitive |
| OptionsTabs.lua:80-83,155,160 | `TAB_ATLAS`, `PANEL_ATLAS` | `Options_Tab_*`, `Options_Tab_Active_*`, `Options_InnerFrame` | tab strip, content box | B | Tab / Inset primitives |
| OptionsTabs.lua:173-176 | tab fill and glow gradients | `.10/.15` grey at `.85`; glow white `.15` to 0 | tab backing | L | `tab.bg`, `tab.glow` |
| OptionsTabs.lua:181 | `CHROME_RULE_COLOR` | `1,.82,0,.16` | banner/strip hairline | L | `accent` at low alpha |
| OptionsTabs.lua:331-353 | tab fonts | `GameFontNormalSmall` / `GameFontHighlightSmall` | tab labels | L | `font.small`, `text.selected` |
| OptionsTabs.lua:950 | PageBanner dropdown | AceGUI `Dropdown` | banner | A | Dropdown |
| OptionsTabs.lua:1236 | disabled notice | `GameFontHighlightSmall` | notice row | A | `font.small` |
| OptionsNav.lua:50-62 | rail | select `UI-QuestLogTitleHighlight` tinted `.3,.5,1`; labels gold/white; `PANE_BACKDROP` (ChatFrameBackground plus UI-Tooltip-Border 16) fill `.1,.1,.1,.5`, border `.4,.4,.4`; cap atlas `Options_Tab_Active_Left` | NavRail | L+B | NavRail: `nav.select`, `nav.pane*`, `text.*` |
| OptionsDrawer.lua:63-75 | drawer palette | gold, white, summary `.91,.85,.66` / `.5`, head fill `.08,.07,.06,.9` (open `.13,.11,.08,.95`), edge `.18,.16,.14` (open `.42,.33,.13`), box fill/edge, `UI-QuestLogTitleHighlight`, `ChatFrameExpandArrow`, WHITE8X8 | Drawer head and box (on AceGUI SimpleGroups, `:284-344`) | L on A | Drawer tokens |
| OptionsDrawer.lua:123,128 | fonts | `GameFontNormal`, `GameFontHighlightSmall` | label, summary | L | `font.normal/small` |
| OptionsWidgets.lua:167-917 | row makers | AceGUI `SimpleGroup`, `Heading` (`GameFontNormalLarge`, :565), `Label`, `Button`, `CheckBox`, `Slider`, `Dropdown`/`LSM30_*`, `EditBox`, `ColorPicker` | every schema row | A | Checkbox, Slider, Dropdown, EditBox, Button, Heading |
| OptionsWidgets.lua:351-361 | landing logo texture | host path | landing page | L on A | none |
| OptionsIds.lua:675,694,676 | status tints | warn `1,.5,0`, neutral white, `|cff808080` | id input status | A | `text.warn`, `text.muted` |
| OptionsIds.lua:909-918,1012-1023 | suggest popup | `UI-QuestTitleHighlight`, UI-Tooltip-Background/Border 16, bg `0,0,0,.92`, `GameFontHighlightSmall`/`DisableSmall` | id suggestions | L+B | Tooltip / menu tokens |
| OptionsIds.lua:1272-1283 | id input | AceGUI EditBox/Button/Label | id row | A | EditBox, Button |
| OptionsIdList.lua:73,84,182-198,257 | list art | `transmog-icon-remove`, `UI-QuestTitleHighlight`, help tint `.82,.65,.21` / over white / dim `.35,.35,.36` / blocked `.9,.24,.24`, `InformationIcon` fallback | id list rows (AceGUI Icon, InteractiveLabel, CheckBox) | A+B | `icon.*`, `text.danger` |
| OptionsKeybinds.lua:658-839 | keybind rows | AceGUI Label, Button, SimpleGroup, InteractiveLabel; no literals | Keybindings tab | A | Button |
| OptionsScroll.lua:35-40,270 | `GUTTER`, `THUMB_ON/OFF` | 20; `1,1,1,1` / `.5,.5,.5,.6`; preload `SetFont(path,12)` | always-shown scrollbar tint | A+B | ScrollBar: `scroll.thumb`, `scroll.thumbOff` |
| OptionsCombat.lua:219-222 | combat cover | dim `0,0,0,.6`, `GameFontNormalLarge`, text `.667` grey | combat lock overlay | L | `overlay.dim`, `text.muted` |
| OptionsCompose.lua:555,560,569,598,602,628 | row **defaults** | font `Friz Quadrata TT`, size 12, flags `OUTLINE`, border `None`, size 1, bar `Blizzard` | FontGroup, BorderGroup, BarGroup | (data) | the "From skin" sentinel targets |
| DebugLog.lua:169 | `FormatColored` | `|cff6f8faf` timestamp, `|cffc9a66b` tag | console lines | L | `log.ts`, `log.tag` |
| DebugLog.lua:201,209-220 | console size, link and button colors | 700x344; diag `1,.5,0`/`1,.72,.28`; rest `.7,.7,.72`, hot `1,.82,0` | console title bar | L | `link.*`, `button.rest/hot` |
| DebugLog.lua:541-674 | console chrome | BackdropTemplate, `GameFontNormal(Small)`, divider (skin or `0,0,0,1`), track `.24,.24,.27,.3`, thumb `.5,.5,.55,.85`, status rule, line count `.6,.6,.62`, `SetFont(d.font, size)` | debug console | L | window, scrollbar, `font.mono` |
| DebugLog.lua:604,942-944,957-958 | state colors | hover gold, on `.3,.85,.3`, off `.9,.3,.3`, `|cff40ff40`/`|cffff4040` | toggle label | L | `state.on/off` |
| PerfPanel.lua:38-63,95,132,150-151,188-201,263 | `COLORS` per state, `CMD_COLOR`, hover colors, title font | done/used `.3,.85,.3`, ready `.9,.9,.92`, busy gold, locked `.4,.4,.42`, cancel `.8,.32,.32`, cmd `.45,.45,.48` | perf panel | L | `state.*`, `text.muted` |
| SimPanel.lua:125-149,225-370,662-670 | the same palette, duplicated | as PerfPanel, plus button REST/HOT/OFF; `makeButton` calls `core.ApplySkin(b)` with no owner | sim panel | L | as above |
| PerfCommands.lua:107-207, PerfSampler.lua:231,245, Slash.lua:41-42,746, Schema.lua:203, Options.lua:208-215 | chat color escapes | assorted `|cff...` | chat lines | (chat) | out of scope: chat, not frames |
| Launcher.lua:116 | `GREEN/RED` | `|cFF00FF00` / `|cFFFF0000` | LDB tooltip status | B (GameTooltip) | Tooltip, optional |
| Glow.lua | none | knobs come from the host | LCG glows | none | none |

There are no visual constants in `SimTimeline.lua`, `Glow.lua` or `OptionsRegistry.lua`. The gold
`1, .82, 0` (the Blizzard `NORMAL_FONT_COLOR`) is written out separately in at least 14 places, so it
is effectively the `accent` token. The gray `.7,.7,.72` and the panel blue-black `.06,.06,.08`
recur in the same way.

## 3. How a factory could find the active skin, which is per addon

**One loaded copy serves every addon.** LibStub keeps the highest minor of each major
(`docs/releasing.md:10-13`), so `lib`, every file-local (Widgets' `SKIN`, the shared `menu` at
`Widgets.lua:223`) and every published table (`lib.SKIN`, `lib.ROW_BOX`, `lib.LINE_CHART`,
`lib.AUTOCOMPLETE`) is a single object shared by all Ka0s addons. Options already works this way:
`lib.LAYOUT` is copied into instance scalars because handing out the shared table "lets one host's
mutation retune every other host's panels" (`Options.lua:522-525`).

Skin state therefore has to be a registry keyed by the consumer's folder name, something like
`lib.__owners = lib.__owners or {}` so it survives a minor upgrade. Every painter call has to say
whose frame it is painting. Painted-frame memory for live repaint should be a weak-keyed set per
owner. Published constant tables cannot vary per addon, so they stay as the default skin's values
and the factories stop reading them directly.

**How factories learn their owner today:**

| Surface | Owner available? | How |
|---|---|---|
| Media `Icon/Texture/Font/RegisterLSM` | yes, required | `addonName` first argument (`Media.lua:264-310,376`) |
| Options instance and every `O.*` maker (Widgets rows, Tabs, Nav, Drawer, Ids, IdList, Keybinds, Compose, Combat cover) | yes, through the closure `d` | `lib:New(d)` (`Options.lua:478`). `d.mainPanelName` is required, but `d.addonName` is only "RECOMMENDED" (`Options.lua:389`), read today by `OptionsIdList.lua:499` |
| OptionsTabs file-level painters (`drawContentPanel`, `OptionsTabs.lua:410`; `edgeTexture`, `dressTabFill`) | indirect | get `ctx`, which `O.CreatePanel` makes per instance (`Options.lua:655`), so an owner can ride on `ctx` |
| `lib.__PatchLSM30Border` (`Options.lua:307`) | no, process-global | re-registers an AceGUI widget type for the whole session |
| DebugLog `lib:New(d)` | yes | `d.name` required (`DebugLog.lua:383`), `d.addonName` optional (`:733`). Already has per-instance `d.skin` and `d.applySkin` (`:425-508`) |
| Perf panel | yes | `d.addonName or d.name` (`PerfPanel.lua:225`) |
| Sim panel | yes, required | `d.addonName` (`SimPanel.lua:163`). **But** `makeButton` (`:669`) and `build` (`:376`) call `core.ApplySkin(frame)` with no owner |
| Launcher `lib:New(d)` | yes, required | `d.name` folder name (`Launcher.lua:213-216`); tooltip only |
| `W.CopyWindow(d)` | yes, required | `d.addonName` (`Widgets.lua:736`) plus optional `d.applySkin` |
| `W.Dropdown(parent, width, opts)`, `W.SearchBox`, `W.TestStrip`, `W.Autocomplete(editBox, opts)`, `W.DragHandle(parent, spec)`, `W.LineChart`, `W.ReorderList(opts)` | **no** | no owner argument; `opts`/`spec` would need a new `owner` field |
| `W.CloseMenu` and the shared popup menu | **no** | one menu for every addon: it must repaint per owner on each open |
| `Core.ApplySkin(frame, skin)` | **no** | optional skin table only; called 78 times by 13 hosts on their own windows |
| `Core.MakeCloseButton(parent, onClick, addonName)` | optional | falls back to the U+00D7 glyph when no name is passed |
| `Glow.Start` | n/a | host-supplied knobs |
| Schema, Slash, Lifecycle `New` | no name field | not painters |

There is precedent for an owner argument that degrades when absent: `MakeCloseButton`'s optional
`addonName` (`Core.lua:217-239`). Applied here, a factory called without an owner would paint the
`ka0s` default skin.

## 4. Media: shipping fonts and textures

**Layout.** `LibKa0s/media/{icons,fonts,textures}` lives inside the payload. The root `media/` holds
only `logos/`, which do not ship. Paths are built as `Interface\AddOns\<addonName>\libs\LibKa0s\media\...`
(`Media.lua:71-75,241-244`), always from the caller's own addon name, because a vendored copy cannot
know its own folder. The catalogs are `lib.FONTS` (`:147`, one entry: JetBrains Mono plus its OFL
file) and `lib.TEXTURES` (`:166`, seven `Ka0s Gradient/Underline/Overline` statusbars). Paths are
extensionless except fonts (`:250-262`).

**LSM registration.** `lib.RegisterLSM(addonName, vendorPath)` (`Media.lua:376-404`) registers every
`FONTS` entry as `font`, using one langmask for all faces (western plus ruRU, `fontLangmask`, `:336`,
applied at `:381-387`), and every `TEXTURES` entry as `statusbar` (`:399`). LSM keeps the first
registration of a key. Each consumer offers its own path, but the bytes are identical, so whichever
copy wins draws the same thing (`:358-363`). Call it at file load. **No `border` or `background`
media type is registered today.** Nine-slice borders and a stone background need new catalogs (for
example `lib.BORDERS`, `lib.BACKGROUNDS`) and new loops: a Media minor bump.

**Prune flow.** `tools/prune-icons.lua` touches only `libs/LibKa0s/media/icons` (`:39`), and
`testkit/vendor_sync.lua` holds only `media/icons` to the declaration (`:103-104`). Fonts and textures
ship whole-folder to every consumer (`library-stack.md:113`, `:117`), so **new fonts and textures
survive re-vendoring and the prune.** The gates you hit instead:

- `tests/test_media.lua:149-204`: every `TEXTURES` name has a file and every file has a name; every
  `FONTS` entry ships with its license file. New `.ttf`/`.otf` files therefore each need a
  `{ file=, license= }` entry and an OFL text beside them.
- `tests/test_prose.lua`: the payload is ASCII apart from the em dash. Font family names must be
  ASCII.
- Every consumer's `test_vendor_sync` diffs `libs/LibKa0s` against the tag byte for byte.

**Four OFL families.** Barlow, Cinzel, Atkinson Hyperlegible and Inter would add several weights
each. JetBrains Mono Regular alone is 274 KB (`LibKa0s/media/fonts/`), so expect roughly 1-3 MB on
every consumer, compared with about 18 MB of icons before pruning.

The single langmask is wrong for some of these. Cinzel and Atkinson Hyperlegible have no Cyrillic, so
masking them ruRU would draw boxes. `FONTS` entries need a per-face `langmask` field.

Nine-slice art should be white `.tga` tinted at runtime, as the icons already are (`Core.lua:252-256`
"art ships WHITE"). It gets regenerated by `tools/artwork/` and never edited in a consumer
(`releasing.md:280-281`).

## 5. Testkit mocks for headless primitives

`testkit/mock_base.lua:124-245` `stubFrame` gives every frame:

- real `Show/Hide/IsShown`, `SetEnabled/IsEnabled`;
- `SetScript/GetScript/HookScript` (a real chaining wrapper, `:157-164`) and `__fire`;
- `GetHeight/GetWidth` (0 unless armed by `__setGeom`);
- a **recording** `SetAtlas` (`__atlas`, sizes from `ATLAS_SIZES`, `:205-210`);
- recorded `RegisterEvent`/`RegisterUnitEvent`.

**Every other capitalized method answers through the metatable (`:235-240`): it returns the frame and
records nothing.** That covers `SetColorTexture`, `SetBackdrop`, `SetBackdropColor`,
`SetBackdropBorderColor`, `SetVertexColor`, `SetTextColor`, `GetTextColor`, `SetFont`, `SetFontObject`,
`SetGradient`, `SetTexCoord`, `SetNormalTexture`, `SetHighlightTexture`, `SetStatusBarTexture`,
`GetRegions`, `GetChildren` and `GetFont`. `CreateTexture` and `CreateFontString` return the frame
itself, which is a documented, deliberately kept divergence (`:34-45`).

Opt-in recorders exist as siblings: `mock_lines.lua` (`CreateLine`, records color, texture and layer),
`mock_layers.lua` (strata and level, revision 42), and `mock_resize.lua`. The AceGUI fake records
widget calls and pools a CheckBox texture with `SetVertexColor`/`GetVertexColor` (`:1258-1263`).
LibKa0s's own suites hand-roll paint spies per fixture (`tests/fixture_draghandle.lua:51-54`,
`fixture_geom.lua:107`, `fixture_sim_panel.lua:75-76`).

**Missing for skin tests:**

- distinct texture and font-string objects;
- recorded backdrop table and colors, `SetColorTexture`, `SetVertexColor`, `SetTextColor`,
  `SetFont`/`SetFontObject` (answered back by `GetFont`);
- `SetGradient`;
- `GetRegions`/`GetChildren` (for `FadeRegions`);
- `NineSlice` and `NineSliceUtil` (nothing in the kit);
- `SetAlpha`/`GetAlpha` on regions;
- LSM `HashTable`/`Fetch` for border and background.

The precedent says this belongs in an opt-in `testkit/mock_paint.lua`, a kit revision with its own
API document, because `mock_base.lua` is at 1464 lines.

## 6. Settings data

**Schema rows.** Rows are host-owned arrays handed to `Schema:New{ rows = ... }` (`Schema.lua:254`)
and rendered by `OptionsWidgets` dispatch (`:921-945`):

- the four types `bool`, `number`, `string`, `color` (`Schema.lua:69`);
- `string` with `values` renders a Dropdown;
- `dialogControl = "LSM30_Font" | "LSM30_Statusbar" | "LSM30_Border"` renders the AGSMW widget,
  falling back to a stock Dropdown when that widget is not registered (`OptionsWidgets.lua:776-779`);
- `dialogControl = "EditBox"` renders free text;
- enums use `values` (a map or `{ value, text }` list) plus `sorting` (`enumList`, `:107-140`);
- `O.ChoiceGrid(ctx, spec)` (`:1254`) is the choice grid;
- row fields: `default`, `validate`, `normalize`, `onChange(value, id)` (`Schema.lua:484-485`, run
  before the host's `announce`), `disabledIf`, `isPercent`, `min/max/step`, `sessionOnly`,
  `startsLine`.

LSM lists come from `O.LSMValues(type)` (`Options.lua:1239-1251`), a deferred closure over
`LSM:HashTable` that answers `LSM_NONE` rather than an empty list.

**Defaults** are each host's AceDB defaults. `S.Default`/`ApplyDefault` read `row.default`
(`Schema.lua:635-647`). The composers bake in literal defaults (`OptionsCompose.lua:555-628`).

**Migrations.** LibKa0s owns none ("owns no migration, no AceDB defaults", `Schema.lua:15-17`). The
standard puts it in each addon: `savedvariables` requires `global.schemaVersion = 0` in defaults, a
`STEPS` runner in `core/Database.lua` that owns the stamp, and per-profile steps that walk every
stored profile (`WowAddonStandards/standards/standards/savedvariables.md:18-65`). Examples:
`PremadeGroupsFilterExtension/core/Database.lua:17-26`, `QuickComms/core/Database.lua:25-31`,
`KickCD/core/Database_Migrations.lua`.

**What this means for the new settings:**

- `appearance.skin` and `appearance.source` (`ka0s` or `eui`) are plain `string` rows with `values`.
  A skin catalog getter can supply the values like `LSMValues` does. `onChange` calls the library's
  per-owner `SetSkin(owner, ...)`.
- A "From skin" sentinel needs a reserved key, for example `"__skin"`, added to the font, statusbar
  and border lists. `O.LSMValues` would need an opt-in for that. The `LSM30_*` widgets preview by
  looking up `LSM:Fetch(key)`, so a sentinel that is not an LSM key previews as the fallback face or
  as nothing. A plain Dropdown or a library-registered pseudo-entry may be needed.
- Color "From skin" has no natural sentinel in a `color` row. It needs either a companion bool, like
  the existing `useClassColor*` companions (`OptionsCompose.lua:564,608,637`), or a reserved table.
- The composer defaults have to change to the sentinel. That is an OptionsCompose minor bump, and it
  changes defaults for every adopter.
- The one-time reset to the sentinel must be **one per-profile step in every adopting addon's own
  runner**. The library can ship a helper, such as `Skin.MigrateToSentinel(profile, paths)`, but not
  the stamp. AceDB `removeDefaults` will strip a stored sentinel that equals the new default, which
  is the intended outcome.

## 7. EllesmereUI in LibKa0s, and what would move from PGFE

**In LibKa0s today: nothing.** The only mention is the comment at `Options.lua:755` about skinning
addons hooking `AceGUI:RegisterAsWidget`. Repo-wide grep for `ellesmere` over `LibKa0s/`, `testkit/`,
`tests/` and `CLAUDE.md` comes back empty.

**The deviation register format.** `CLAUDE.md:51-58,69-80` uses the columns
`| Rule | What differs | Why | Decided | Re-check trigger |`, with Rule as `filename-§N`. It currently
holds eight rows, and the eighth is the band tracker. A library read of `EllesmereUIDB` would need a
new row against `library-stack-§6` / anti-patterns #29 ("MUST NOT read a suite's ... SavedVariables",
`library-stack.md:66-71`), or an upstream carve-out. PGFE's ratified row
(`PremadeGroupsFilterExtension/docs/ARCHITECTURE.md:469`) has the trigger "EllesmereUI ships a public
query for its third-party switches, or the standard gains a carve-out". Promoting the read into the
library is a natural moment to take the carve-out upstream, so that 14 consumers do not each inherit
an unratified read.

**PGFE's integration, against EllesmereUI 9.4 and facade apiVersion 3:**

- `core/EUIBridge.lua:36-158` is the only reader. It defines:
  - `IsSuiteReady`: `EllesmereUI.RegisterSkin` is a function and `EllesmereUIBlizzardSkin` is loaded;
  - `IsMasterOn`: `EllesmereUIDB.thirdPartySkinsOff` is not truthy;
  - `IsEntryOn(name)`: `thirdPartySkinAddons[name] ~= false`;
  - `PGFSkinState` / `IsPGFSkinOn`, which are PGFE-specific;
  - `Conditions`, `GateOpen`, `WhyClosed`, which return localized labels and hints.

  Every read is at call time, nil-guarded and pcall'd, and nothing is written.
- `modules/EUISkin.lua` registers at **file load** with
  `EllesmereUI.RegisterSkin(<folder name>, onFacade)` (`:430-432`). EllesmereUI calls back **once
  per session**, at PLAYER_LOGIN or live, and only while the master switch and that entry are on. The
  callback keeps the facade `S`. `REQUIRED` (`:42-43`) checks the facade's shape before painting.
  The paint is pcall'd and fails closed with a latch (`:330-350`). It is **one-way**: only a reload
  removes it, and switching off offers `POPUP_RELOAD` (`:356-364`). `S.OnLooksChanged` drives a live
  repaint of colors and fonts (`:371-379`), and `UI_SCALE_CHANGED` / `DISPLAY_SIZE_CHANGED` re-lay
  pixel-sized accents (`:388-393`).

**What generalizes into a library `eui` provider:** per-owner `RegisterSkin` at load, the facade
keeper, the `REQUIRED` shape check, the fail-closed latch, the three generic gate conditions keyed
by owner name (the PGF-skin condition stays in PGFE), `OnLooksChanged` fan-out to the owners, and
the scale re-layout. PGFE's `m.installEUI` fake (`docs/ARCHITECTURE.md:53`) is the model for a kit
EllesmereUI fake. The localized gate strings would need to move into the library's `STRINGS`.

## Risks and open points

1. **Shared singletons.** One loaded copy means the popup menu (`Widgets.lua:223`), the published
   tables (`lib.SKIN`, `ROW_BOX`, `LINE_CHART`, `AUTOCOMPLETE`) and `__PatchLSM30Border` are the same
   object for every addon. Skin state must be keyed by owner, the menu must repaint on every open,
   and the published tables stay frozen as default values (`-1.0` is additive-only).
2. **AceGUI pooling.** AceGUI hands a widget frame painted for addon A to addon B. Every AceGUI paint
   must be undone in `OnRelease` (the existing hygiene: `OptionsWidgets.lua:329-361`,
   `OptionsDrawer.lua:298-300`). Otherwise skins leak across addons, and into non-Ka0s addons too.
3. **Owner plumbing.** Seven Widgets factories, `Core.ApplySkin` and SimPanel's buttons have no owner.
   Options' `d.addonName` is optional. Making it required is a breaking change; leaving it optional
   needs a default-skin fallback.
4. **EllesmereUI paint is one-way.** "Live-switchable" holds for `ka0s`. Moving `eui` to `ka0s`, or
   turning EllesmereUI off, needs a reload, and the eui provider must not claim otherwise.
5. **EllesmereUI only knows owners that registered before login.** `RegisterSkin` must be called at
   file load under each consumer's folder name. A consumer that never declares itself never appears
   in EllesmereUI's Third-Party list.
6. **Standards.** A library read of `EllesmereUIDB` needs a LibKa0s register row or an upstream
   carve-out to `library-stack-§6`. A new major also edits `library-stack.md:92` and `:128`.
7. **Line cap.** Retrofitting `OptionsWidgets.lua` (1444 of a 1450 trigger), `OptionsTabs.lua`,
   `Options.lua`, `OptionsIds.lua` and `DebugLog.lua` will fire band triggers. Plan the peels, and
   keep each call site to a single `S.X(owner, frame)` line.
8. **Font langmask.** One mask is applied to every face today. Cinzel and Atkinson need a per-face
   mask, and CJK clients need a fallback face for every skin.
9. **"From skin" sentinel versus `LSM30_*` previews and AceDB `removeDefaults`.** Color settings have
   no sentinel shape. The migration has to live in each addon's runner, so every adopter takes a
   schema step.
10. **Payload size.** Fonts and textures are not pruned, so every consumer carries every skin's
    assets, about 1-3 MB.
11. **Kit work.** `mock_base.lua` sits at 1464 lines. The paint recorder and the EllesmereUI fake need
    new kit files and a kit revision, and every consumer then re-vendors the kit.
12. **Host-painted windows.** Thirteen hosts call `ApplySkin`/`SKIN` 78 times on their own frames.
    They follow a skin switch only if they adopt the owner-aware call.
