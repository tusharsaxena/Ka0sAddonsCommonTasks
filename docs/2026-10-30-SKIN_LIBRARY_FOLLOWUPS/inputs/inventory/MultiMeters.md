# M0 inventory: MultiMeters

Read-only inventory for the LibKa0s v1.81.0 follow-ups (rulings R-1..R-11, `00_PLAN.md`). Scope: `../MultiMeters`
excluding `libs/` and `tests/_kit/` (read only for reference). Every path below is relative to
`/mnt/d/Profile/Users/Tushar/Documents/GIT/MultiMeters/` unless it starts with `LibKa0s/` (=
`/mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/LibKa0s/`, the library source at master ea1d92d).

**Bottom line:** MultiMeters carries **no** `stockDefault`/`stock` caller, no `__DrawsKey` reach-in, no
Ignore-fonts patch, no hand-rolled Scope guard around `S.Text`/`ReorderList`, no close-button tint handling, and
no literal tooltip/quality colour. It carries **one** library-gap workaround (the `ResetToSkin` bool backfill,
R-6). Every HUD face resolves through the library (`S.Resolve`), so R-1 lands in MultiMeters with **no code
change**. The rest of MM-01/MM-02 is: the R-6 backfill, one tooltip string made untrue by R-1, keeping the degraded
facade stub at parity if the facade gains names, an optional R-5 follow-through on the Columns editor's own
colours, and doc and smoke-check rewording (R-1, R-4, R-11).

## 5. Current state (run first)

| Fact | Value | Evidence |
|---|---|---|
| Branch | `master`, tracking `origin/master`, **clean** | `git status -sb` → `## master...origin/master` with no entries |
| Head | `6c5e837 Merge feat/2026-10-29-skinning-rollout: the LibKa0s skinning rollout` | `git log --oneline -1` |
| Other branches | none local; `origin/master` only | `git branch -a` |
| Vendored LibKa0s | **v1.80.0** | `CLAUDE.md:62` "Bundles [LibKa0s](...) v1.80.0 (MIT)."; icon declaration `CLAUDE.md:63` |
| Tests on master | `2415 passed, 0 failed, 1 skipped, 2416 total` (exit 0) | `~/.claude/dev-copilot/bin/ka0s-bounded lua tests/run.lua` |
| Lint on master | `Total: 0 warnings / 0 errors in 171 files` (exit 0) | `~/.claude/dev-copilot/bin/ka0s-bounded luacheck .` |
| Gate | **green** | both of the above |

## 1. Workarounds of library gaps the release closes

### R-6 / LK-07: the `ResetToSkin` `"@skin"` guard (the only workaround)

- `core/Database.lua:1076-1081`: the doc comment says the backfill exists because "LibKa0s-Skin-1.0's
  ResetToSkin, handed an absent key, cannot tell it is a bool and writes its "@skin" sentinel into it".
- `core/Database.lua:1082-1093` `v20FollowSkin(w, resetToSkin)`. The workaround line is
  **`core/Database.lua:1088`**: `if type(g[leaf]) ~= "boolean" then g[leaf] = false end`, which backfills every
  absent `<key>FromSkin` companion to `false` before calling `resetToSkin(w, keys)` (`:1092`).
- Caller: `migrations[19]` (v19 → v20), `core/Database.lua:1104-1114`, which reads `Skin.ResetToSkin` at `:1106-1107`.
- The key list is `Database.FROM_SKIN_KEYS`, `core/Database.lua:1070-1074`.
- Library cause: `LibKa0s/Skin.lua:891-912` `lib.ResetToSkin`. An absent leaf with no `<leaf>FromSkin` sibling
  falls to `parent[leaf] = lib.FROM_SKIN` (`:906`).
- **What changes:** after LK-07, the backfill at `:1088` can go and the comment at `:1076-1081` can be rewritten.
  This holds **only if** LK-07 recognises an absent `*FromSkin` leaf as a bool. MultiMeters names the companions
  directly (`header.fontFromSkin` and so on), so `parent[leaf .. "FromSkin"]` is never what detects them. The
  implementer must check LK-07's actual detection rule before deleting the line. If LK-07 leaves an absent companion
  `nil` instead of `true`, the v20 test below goes red, and the line should stay.
- The degraded arm (no library) sets `g[leaf] = true` directly at `:1089` and is unaffected.
- The step is a one-time migration, stamped account-wide. Removing the backfill only changes what an account still
  on schema v19 sees on its first load of the new build. The end state is the same, with every companion `true`.

### R-2 / LK-02: `stockDefault` / `stock` callers: **none**

- Proof: `grep -rnIE --exclude-dir={libs,_kit,.git,audits,reviews,automated-tests,revendor,perf-analysis,superpowers} 'stockDefault|stock *=' .`
  gives 0 hits.
- Under Ka0s Default, every MultiMeters surface already paints the Ka0s look, so R-2 changes no MultiMeters-owned
  surface. Under Ka0s Default today:
  - The meter window chrome follows the skin through its `skin` modes (`core/SkinSetup.lua:167-189`;
    `core/Database.lua:1116-1146`).
  - The export modal uses `S.Shell/TitleBar/Inset/Text/Font` with no opts besides `noTopBar`
    (`modules/Export_Modal.lua:792-799`) and `S.Button(button)` with none (`:260`).
  - The empty state calls `S.Text` (`modules/Window.lua:1415-1418`).
- Library-internal `stock` callers that reach MultiMeters' settings pages are the library's to change:
  `LibKa0s/OptionsTabs.lua:495` (`Panel`, `stock = panel.__ka0sHalves`) and `:503` (the tab art). With **Ignore
  settings panel** unticked under Ka0s Default, those surfaces will move from stock art to the Ka0s look after
  LK-02. No MultiMeters code is involved, but smoke SKIN-9 (`docs/smoke-tests.md:1789-1795`) is where the owner
  would see it.
- **Exception row:** MM-01 has nothing for R-2 (grep above).

### R-9 / LK-10: `Skin:__DrawsKey` reach-in: **none**

- Proof: `grep -rnIE <same excludes> 'DrawsKey' .` gives 0 hits.
- **Knock-on to check at re-vendor:** `tests/test_skinsetup.lua:310-316` holds the **degraded facade stub**
  (`core/SkinSetup.lua:418-426`, the hand list of VOCAB names, plus `:428-453`) key for key against the live facade
  with `T.assertSurfaceParity` (`tests/_kit/asserts.lua:320`).
  - If LK-10 (or LK-05/06) adds any name to the per-owner **facade** (`Skin:For(owner)`), not just to `lib`, that
    test goes red until the name is added to the list at `core/SkinSetup.lua:419-426` (or given a host meaning
    below it).
  - If the new name lives only on `lib` (`Skin:DrawsKey(owner)`), nothing changes.

### R-1 / LK-01: own Ignore-fonts handling for the HUD: **none**

- Proof: `grep -rnIE <same excludes> 'FontsIgnored|hud\.outline' .` gives 0 hits.
- MultiMeters reads the Scope only to store it and hand it to `Skin:SetIgnore`: `core/SkinSetup.lua:92`, `:291-294`,
  `:309-313`, `:499-505`. The rows are at `settings/Schema_Skin.lua:52-61`.
- Nothing in MultiMeters reads `ignoreFonts` to choose a face.

### R-5 / LK-05, LK-06: hand-rolled Scope guards around `S.Text`, `WidgetsReorder` or other widgets: **none**

- `S.Text` is called with no guard at `modules/Export_Modal.lua:796` and `:798` (the export modal) and at
  `modules/Window.lua:1416-1417` (the empty state). These are not settings-panel surfaces.
- `W.ReorderList` is called with `owner = NS.name` and no guard at `settings/ColumnBlocks.lua:235-258` (owner at
  `:252`). The drag handle (WidgetsDragHandle) comes in through ReorderList.
- The other custom library widgets MultiMeters uses all hand over the owner and none is guarded. After LK-06 each
  obeys the Scope library-side, with no MultiMeters change:
  - `W.CopyWindow` with `addonName`: `modules/Export_Modal.lua:327-345`
  - `W.Dropdown` with `owner = NS.name`: `modules/Export_Modal.lua:679`
  - `W.TestStrip` × 2 with `owner = NS.name`: `modules/Window.lua:571-577` and `:724`
  - the debug console, the perf panel and the sim panel, through their seams (`tests/test_skin_tools.lua:37-60`
    pins that each is painted for this owner)
- **The opposite gap, an MM decision for MM-01 and not a deletion.** The Columns editor (a settings-panel surface)
  paints three colours of its own straight from the skin and ignores **Ignore settings panel**:
  - `settings/ColumnBlocks.lua:194`: the block label, `text.accent` / `text.disabled`
  - `settings/ColumnBlocks.lua:301`: `ghostTextColor`, passed into ReorderList
  - `settings/ColumnBlocks.lua:163`: the glyph tooltip, `gtip.value`

  Once LK-05 makes ReorderList's drop line and ghost go stock under Ignore settings panel, the ghost's text colour
  will still be the skin's, because MultiMeters supplies it. Under Ka0s Default the two looks are identical (gold,
  0.5 gray, white), so only non-default skins show it. If the run wants R-5 to hold fully on this page, MM-01 should
  gate these three colours on the owner's panel exception (`Skin:GetIgnore(owner)`, already used in tests at
  `tests/test_skinsetup.lua:191`) or take them from whatever the library exposes for this in v1.81.0. Otherwise,
  record it in `DECISIONS.md` as accepted.

### R-3 / LK-03: close-button tint handling: **none**

- Every MultiMeters close control except the header strip's is built by the library: `NS.MakeCloseButton` →
  `lib.MakeCloseButton` (`core/CoreSetup.lua:294-296`), which calls `S.CloseButton(b, { own = true })`
  (`LibKa0s/Core.lua:302-304`). Its users are the export modal (`modules/Export_Modal.lua:212-213`) and the perf
  panel and debug console (`core/PerfSetup.lua:193-211`). LK-03's save-and-restore happens inside the library.
- The meter window's own header close control is **deliberately not** `S.CloseButton`, because its hover would be
  `close.hot` red beside six gold siblings (`modules/HeaderControls.lua:558-561`, `docs/ARCHITECTURE.md:335`).
  `tests/test_headercontrols.lua:932-934` pins that it is not built through `NS.MakeCloseButton`. It is not a
  workaround, so nothing changes.
- Proof: `grep -rnIE <same excludes> 'S\.CloseButton|Skin\.CloseButton' .` gives only those two comment hits.

### R-7 / LK-08 and R-8 / LK-09: literal tooltip or quality colours: **none**

- Every tooltip line MultiMeters writes takes `NS.SkinColor("gtip.title"|"gtip.value")` or `mm.tipHint`. See
  `modules/Tooltip_Builders.lua:255, 437, 444, 451, 526, 553, 585, 666, 676, 765, 943, 1039`,
  `modules/Tooltip_Lines.lua:698` and `settings/ColumnBlocks.lua:163`. `mm.tipHint` follows `gtip.muted`
  (`core/SkinSetup.lua:110`).
- No `q.*` token and no item-quality colour exist anywhere. Proof: `grep -rnIE <same excludes> '"q\.[a-z]+"' .`
  and `ITEM_QUALITY|GetItemQualityColor` both give 0 hits.
- The host copy `NS.SKIN_FALLBACK` (`core/SkinSetup.lua:127-142`) holds no `q.*` and no changed token. It is held to
  the live library's Ka0s Default by `tests/test_skinsetup.lua:334-350`, so LK-09 cannot turn it red. If LK-08 (or
  any item) **changes a Ka0s Default value** of `gtip.title`/`gtip.value` or one of the other twelve copied tokens,
  that test goes red and the copy must follow.
- LK-08 recolours the drag handle's tooltip in the Columns editor (ReorderList's handle, `handleTooltip` at
  `settings/ColumnBlocks.lua:249`). No MultiMeters code is involved; `tests/test_columnblocks.lua:589-600` checks
  only the text and the icon.

### R-11 / LK-11: picker title: no code

- MultiMeters passes no title. The spec is at `core/SkinSetup.lua:355-363`, and the owner label "Ka0s Multi Meters"
  is registered at `core/SkinSetup.lua:470`. The library builds the title (`LibKa0s/OptionsSkinPicker.lua:106`
  `TITLE_FOR = "Choose a skin for %s"`, `:240`). No MultiMeters test asserts the title text: `grep -n 'Choose a
  skin' tests/*.lua` gives 0 hits.
- The degraded `Helpers.SkinPicker` / `HideSkinPicker` stubs (`settings/OptionsSetup.lua:436-440`) need a change
  only if LK-11 changes the call signature.

## 2. Where MultiMeters resolves a HUD face or outline itself

All HUD faces go through **one** function, `NS.SkinMediaKey(group, key, token)` (`core/SkinSetup.lua:241-249`). It
calls the owner facade's `S.Resolve(token, stored, group[key.."FromSkin"] == true)` (`:245`), and that call is
`lib:Resolve` (`LibKa0s/Skin.lua:868-871`), the exact function LK-01 changes. So after LK-01, with Ignore fonts on,
the stored pick wins on every one of these sites with **no MultiMeters edit**:

| Surface | Site |
|---|---|
| Title + session line (header) | `modules/Window_Header.lua:158-161` `headerFont` |
| Column labels | `modules/Window_Header.lua:262-265` `columnHeaderFont` |
| Cell text | `modules/Row.lua:777-780` `Cell:ApplyTextStyle` |
| Window notice | `modules/Window.lua:835-836` (the header group's face) |
| Tooltip lines | `modules/Tooltip.lua:305` `media("font", "hud.font", "Friz Quadrata TT")`, through the local `media` helper ending at `:280` |
| Bar textures / border styles (not fonts, so R-1 does not apply) | `modules/Tooltip.lua:292, 300`; Row.lua via `NS.SkinMediaKey(..., "bar.texture"/"bar.borderStyle")` |

- **Outline:** MultiMeters never follows `hud.outline`. Every outline is the player's (`modules/Window_Header.lua:159,
  263`; `modules/Row.lua:781`; DECISIONS X4, stated at `core/SkinSetup.lua:237-238`). The R-1 outline half has
  nothing to change. Proof: grep `hud\.outline` gives 0 hits.
- **Degraded facade `S.Resolve`** (`core/SkinSetup.lua:433-436`) has no Ignore-fonts notion. That is harmless,
  because the degraded `S.Token("hud.font")` answers nil (there is no `hud.font` in `NS.SKIN_FALLBACK` or
  `NS.SKIN_TOKENS`), so `SkinMediaKey` already falls back to the stored pick (`:248`). No change.
- **The composer's picker preview (LK-01, second half).** MultiMeters' eight HUD pickers use the library composer's
  `fromSkin` companion (`settings/Schema_Compose.lua:593-616`, `followsSkin`; font paths at `:166-176`). While a
  companion is on, the library shows the skin's face in the disabled picker (`LibKa0s/OptionsCompose.lua:514-535`,
  `skinValue` → `S.Resolve(token, nil, true)`). After LK-01, with Ignore fonts on, it previews the stored face. No
  MultiMeters code changes, but **one string becomes untrue**:
  - `settings/Schema_Compose.lua:603` and `locales/enUS.lua:801-802`: "Draw this text in the skin's font. The font
    picker is kept but not read while this is on." With Ignore fonts ticked, the picker **is** read. MM-02 should
    reword it, for example by adding "unless Skin → Ignore fonts is ticked". Rewording changes a locale key, so
    every locale file that carries the key moves with it.
- **R-4 / LK-04 effect on MultiMeters:** under the eight non-Ka0s skins, the HUD (title, labels, cells, notice,
  tooltip lines) moves from Friz Quadrata (SkinDefs KEEP) to each skin's own face. No MultiMeters code is involved.

## 3. Tests that pin the current behaviour

| Test | Pins | Effect of v1.81.0 |
|---|---|---|
| `tests/test_skin_hud.lua:196-223` "the v20 step puts every window of every profile on the skin, keeping the picks" | that the v20 step leaves every companion `true` and never writes `"@skin"` (comment `:197`) | Stays the guard when the `core/Database.lua:1088` backfill is removed. It must stay green, which proves LK-07 suffices. |
| `tests/test_skin_hud.lua:225-246`, `:248-260` | v20 runs once; junk / absent group | unaffected; re-run |
| `tests/test_skin_hud.lua:103-128`, `:130-151` | the HUD draws `hud.font` while the companion is on | Ignore fonts is off in these cases, so they still pass. **Add** a case: with `Skin:SetIgnore(OWNER, nil, true)` and the companion on, the cell, title, labels and `tooltipConfig(cfg).font` draw the **stored** face. Red before LK-01, green after. |
| `tests/test_skinsetup.lua:225-236` "the tab's Ignore fonts reaches the library and the profile, one repaint" | the Scope write reaches `Skin:GetIgnore` | unaffected; the natural neighbour for the new HUD case |
| `tests/test_skinsetup.lua:310-316` degraded-facade parity | the stub at `core/SkinSetup.lua:419-426` equals the live facade's names | red if v1.81.0 adds a facade name (LK-10's public DrawsKey or an LK-05/06 primitive) |
| `tests/test_skinsetup.lua:334-350` host-copy tokens equal the live Ka0s Default | `NS.SKIN_FALLBACK` | red only if a copied token's Ka0s Default value moves (none planned; LK-09 touches `q.*`, which is not copied) |
| `tests/test_skinsetup.lua:292-307` "every library widget factory this addon calls is handed the owner" | the `owner = NS.name` counts per file | unaffected unless LK-06 changes a factory's owner key |
| `tests/test_columnblocks.lua:524-538` ghost colour | `ghostTextColor` = gold / 0.5 gray under Ka0s Default | unaffected; extend it if MM-01 gates the colours on the panel exception (§1 R-5) |
| `tests/test_columnblocks.lua:589-600` handle tooltip text and icon | text only | unaffected by LK-08 |
| `tests/test_skin_picker.lua:52-230` | the picker spec, when it shows, close and seen; the window cases drive the library's real picker (`:182-219`) | no title assertion; re-run after LK-11 in case the frame's shape changes |
| `tests/test_skin_tools.lua:97-115` | tooltip lines on `gtip.*` under Ka0s Default and another skin | unaffected |
| `tests/test_skin_window.lua:128-151` | chrome under Ka0s Default and live skins | unaffected (no `stockDefault`) |
| `tests/test_headercontrols.lua:932-934` | the header close is not `NS.MakeCloseButton` | unaffected |
| `tests/test_settings_pin.lua:87` | the `skin.ignoreFonts` row shape | unaffected |

No test pins "HUD ignores Ignore fonts" or "a non-Ka0s skin draws Friz Quadrata on the HUD": `grep -n
'Friz\|ignoreFonts' tests/test_skin_*.lua` finds only the row-default and write cases above.

## 4. Smoke checks and doc passages whose expectation changes

### `docs/smoke-tests.md`

| Check | Lines | Change |
|---|---|---|
| **SKIN-4** | `:1749-1767`, phrase at `:1754-1755` "its faces take the skin's own family (Azeroth's Vollkorn, for one; a skin with no face of its own draws Friz Quadrata)" | R-4: every skin now has its own HUD face. Drop the Friz clause and name what the owner should see (each skin's face per `DECISIONS.md`). |
| **SKIN-5** | `:1769-1775`, "While a companion is ticked its picker is grayed and shows the stored pick, never the skin's name" | The library shows the **skin's** value in the disabled picker (`LibKa0s/OptionsCompose.lua:527-535`), so this text was already wrong before the run. After LK-01, with Ignore fonts on, it shows the stored face. Reword to both states. |
| **SKIN-8** | `:1786-1788` "tick **Ignore fonts** → every string the addon draws keeps its own face…" | R-1: this expectation is **untrue today for the HUD**: the title, labels, cells and tooltip lines keep the skin's face because `S.Resolve` ignores the Scope. After LK-01 it becomes true. State it explicitly: "including the HUD (title, column labels, cells, tooltip lines), which draws each window's own Font pick even with *Use the skin's font* ticked; the companion's grayed picker then shows that pick". |
| **SKIN-2** | `:1725-1741` "with **Ignore fonts** ticked they keep Friz Quadrata" (export modal, empty state) | no change. Those surfaces go through `S.Text/S.Font` (`P.font` → `__FontsIgnored`, `LibKa0s/SkinPaint.lua:539`), which already honours the Scope. Re-read if LK-05 changes `S.Text`'s font path. |
| **SKIN-9** | `:1789-1795` the settings pages, Ignore settings panel, "Columns editor's blocks (labels in the skin's accent …)", "Tick Ignore settings panel → this addon's pages are stock again" | R-5: the ReorderList's drop line, ghost and handle now go stock with Ignore settings panel. Say so. Note the Columns labels/ghost text colour decision from §1. R-2: with Ignore settings panel **unticked** under Ka0s Default, the library's tab and panel art (formerly kept stock) are Ka0s-styled. |
| **SKIN-12** | `:1805-1807` tool windows wear the skin | R-5/LK-06: add that with Ignore fonts ticked they keep their own faces (and that the Scope now reaches them), per what LK-06 implements |
| **SKIN-15** | `:1814-1819` "a small window titled **Choose a skin for Ka0s Multi Meters** opens … a dropdown showing Ka0s Default …" | R-11: the title is **"Choose a skin"**, and "Ka0s Multi Meters" sits on its own line above the dropdown, not truncated |
| SKIN-16..21 | `:1820-1840` | no expectation change (they reference the picker by behaviour, not by title) |
| Summary row | `:34` "SKIN-1 to SKIN-24 …" | add "(amended by the skin library follow-ups)" if the doc convention needs it. The amendment-note style is at `:1868-1869` and `:1722-1724`. |

The intro paragraph `:1695-1706` ("What does not: … sizes, outlines and thicknesses") still holds, because the HUD
outline never follows.

### `docs/ARCHITECTURE.md`

- `:354-365` **The HUD**: add that, with **Ignore fonts** on, `S.Resolve` answers the stored pick (LK-01), so the
  HUD keeps each window's own faces. `:363-365` cites `Skin.ResetToSkin` for the v20 step; it stays true, but if
  the backfill goes, drop any implication of a backfill (there is none on these lines; it is in schema.md).
- `:370-375` **The export modal**: no change (already "kept unless **Ignore fonts** is ticked").
- `:376-379` **The settings pages**: add that the library's custom widgets (the Columns ReorderList, the drag
  handle) now obey Ignore settings panel (R-5), plus the §1 decision about the block colours.
- `:380-386` **The first-run picker**: optionally name the title ("Choose a skin", with the addon's label above
  the dropdown).
- `:335` the header close is not `S.CloseButton`: no change.

### Other docs

- `docs/schema.md:87`, the v19 → v20 row: "set on through LibKa0s-Skin-1.0's `ResetToSkin`, one call per window,
  **backfilled to `false` first**". If the backfill at `core/Database.lua:1088` goes, drop that clause and explain
  that LK-07 makes it unnecessary. Also `docs/schema.md:145` "`ignoreFonts = false`, -- the Scope: leave every
  font the client's": still true, and after R-1 also true for the HUD. Optionally clarify "(the HUD: each
  window's own pick)".
- `docs/settings-panel.md:117-126` ("while it is ticked the picker beside it is disabled … and shows the stored
  pick, and the surface draws the skin's token"). This is the same inaccuracy as SKIN-5. Reword: it shows the
  skin's value, or the stored pick while Ignore fonts is on, and the surface draws the stored pick while Ignore
  fonts is on.
- `docs/settings-panel.md:64` (the General row's Skin tab prose: "the Scope (**Ignore settings panel**, on for a
  new profile, and **Ignore fonts**)"): no change required.
- `README.md:50` ("The window fonts and bar textures follow the skin too, while each **Use the skin's font** … box
  … is ticked. Untick one and your own pick comes back.") Optionally add: "or tick Ignore fonts on the Skin tab
  to keep every font your own". It is not wrong after R-1. README carries no picker title.
- `docs/testing.md`: no skin-Scope or picker-title passage (`grep -n -i 'ignore fonts\|Choose a skin\|stock'
  docs/testing.md` gives 0 relevant hits). If a new HUD/Ignore-fonts test is added, list it where testing.md lists
  `tests/test_skin_hud.lua`, and update any case counts there and in `docs/test-cases.md` (generated: `grep -n
  'Skin picker' docs/test-cases.md` → `:2545`).
- `docs/module-map.md:314` (SkinSetup row): no change unless the degraded stub gains names.

## 6. Nothing to change (exceptions.tsv candidates)

Proof command for each row (run from the repo root; zsh needs the array form):

```
cd /mnt/d/Profile/Users/Tushar/Documents/GIT/MultiMeters && P=(--exclude-dir=libs --exclude-dir=_kit --exclude-dir=.git --exclude-dir=audits --exclude-dir=reviews --exclude-dir=automated-tests --exclude-dir=revendor --exclude-dir=perf-analysis --exclude-dir=superpowers)
```

| Ruling | Claim | Command | Result on master 6c5e837 |
|---|---|---|---|
| R-2 | no `stockDefault` / `stock` caller | `grep -rnIE $P 'stockDefault\|stock *=' .` | 0 hits |
| R-9 | no `__DrawsKey` reach-in | `grep -rnIE $P 'DrawsKey' .` | 0 hits |
| R-1 | no own Ignore-fonts handling, no `hud.outline` | `grep -rnIE $P 'FontsIgnored\|hud\.outline' .` | 0 hits |
| R-3 | no close-button tint handling | `grep -rnIE $P 'S\.CloseButton\|Skin\.CloseButton' .` | 2 hits, both comments explaining the header close is not `S.CloseButton` (`docs/ARCHITECTURE.md:335`, `modules/HeaderControls.lua:560`) |
| R-8 | no `q.*` / quality literal | `grep -rnIE $P '"q\.[a-z]+"\|ITEM_QUALITY\|GetItemQualityColor' .` | 0 hits |
| R-7 | no literal tooltip colour | `grep -rnE $P 'AddLine\([^)]*[0-9]\.[0-9]+ *, *[0-9]' --include='*.lua' .` | 0 hits |
| R-5 | no hand-rolled Scope guard | `grep -rnIE $P 'GetIgnore\|PanelSkinned\|ignorePanel' --include='*.lua' core modules settings` | only the store/apply seam (`core/SkinSetup.lua:92, 292, 310`) and the schema row; none guards a paint |
| R-11 | no picker-title code | `grep -rnI $P 'Choose a skin' .` | 1 hit, `docs/smoke-tests.md:1815` (doc only) |

The only MM-01 code items are:

- **R-6:** the `core/Database.lua:1088` backfill and its comment `:1076-1081`, conditional on LK-07's detection
  rule.
- **R-1:** the tooltip string `settings/Schema_Compose.lua:603` / `locales/enUS.lua:801-802`.
- **The degraded-stub parity** at `core/SkinSetup.lua:419-426`, if the facade grows.
- **Optionally (R-5 follow-through):** the three Columns-editor colours at `settings/ColumnBlocks.lua:163, 194,
  301`.

Everything else is MM-02 (docs and smoke checks) and MM-RV.
