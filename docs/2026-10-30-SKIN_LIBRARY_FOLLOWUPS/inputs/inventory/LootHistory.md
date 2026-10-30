# M0 inventory: LootHistory

Read-only inventory for `LH-RV`, `LH-01` and `LH-02` of `00_PLAN.md`. Scope: `/mnt/d/Profile/Users/Tushar/Documents/GIT/LootHistory`,
excluding `libs/` and `tests/_kit/`. Paths below are relative to that repo unless they start with `LibKa0s/` (the library
checkout at `../LibKa0s`, on master at `ea1d92d`, tag `v1.80.0`). Taken 2026-10-30.

## TL;DR

- **The gate is green on master.** The TestData failure that held LootHistory out is fixed on master (`701a1fe LH-FX1`),
  and the bounded-lint branch is merged (`7debc49`). **LootHistory joins the run.**
- **There is almost no workaround to delete.** LootHistory has no HUD and no `stockDefault`/`stock` caller. It does not
  call `ResetToSkin`, does not reach `__DrawsKey`, and has no Scope guard, no Ignore-fonts patch and no close-button tint
  handling. `LH-01` is mostly an exception. Section 6 has the proof greps.
- **What does change:** tests that pin today's library values or minors (the picker title, the rounded `q.epic`, the
  exact v1.78.0/v1.79.0 minor pins), the SKIN-27 smoke check and the settings-panel doc that state the picker title, and
  the version-pin housekeeping a two-tag jump (v1.79.0 → v1.81.0) brings.
- **One design question for the lead (D-LH-1, section 1.4).** The AH price table on the settings panel is painted by the
  host from skin tokens and ignores **Ignore settings panel**. Once LK-05 makes `WidgetsReorder` obey the Scope, that
  table's drag chrome goes stock under the default Scope (panel ignored), while its text stays skinned.

---

## 1. Workarounds of library gaps the release closes

| Ruling | What LootHistory has | Change owed |
|---|---|---|
| R-1 Ignore fonts on the HUD | **No HUD.** Nothing reads `hud.font` / `hud.outline`. There is no `NS.SkinFontsIgnored`-style patch. | None. Exception (proof §6). |
| R-2 retire `stockDefault` / `stock` | **No caller.** The only `stock =` in code is the Browser tab-spec's *view* override, `modules/HoldingsTab.lua:668` `stock = { sortKey = "name", sortAsc = true }`, read at `modules/Browser.lua:363-367`. It is unrelated to the skin option and must **not** be touched. | None. Exception. |
| R-3 `S.CloseButton` tint | No tint handling of its own. Every close mark is `lib.MakeCloseButton(parent, onClick, addonName)` via `core/CoreSetup.lua:292-294` (Browser `modules/Browser.lua:82-84,1030`, Export `modules/Export.lua:486-487`). Core paints it with `S.CloseButton(b, { own = true })` (`libs/LibKa0s/Core.lua:304`; pinned by `tests/test_skin_chrome.lua:188`). The degraded `fallbackCloseButton` (`core/CoreSetup.lua:61-75`) reads `btn.icon` and is the no-library path. | None. The fix lands through the library. Exception. |
| R-4 HUD font per skin | No HUD face is read anywhere. | None. Exception. |
| R-5 `S.Text` / `WidgetsReorder` obey the Scope | `S.Text` calls are all on the **History window**, never the settings panel: `modules/Browser.lua:175`, `:294`, `:1064`, `:1069` and `modules/BrowserTable.lua:981`. So the panel scope never applies to them. Their face already obeys Ignore fonts (`LibKa0s/LibKa0s/SkinPaint.lua:539` via `prim.Text` → `P.font`, `SkinPaintExtras.lua:316-326`). **`WidgetsReorder` is on the settings panel:** the AH price drag list, `settings/Panel.lua:772-797` through `NS.MakeReorderList` (`core/WidgetsSetup.lua:198-207`, `o.owner = addonName` at `:205`). **No hand-rolled guard exists** (no `GetIgnore` / `__PanelSkinned` in code, §6). | No deletion. **Behaviour changes** under the default Scope: see 1.4 and D-LH-1. If LK-05 needs a flag that marks the list as a panel surface rather than inferring it from the owner, the seam `core/WidgetsSetup.lua:198-207` must pass it. |
| R-5/R-6 other custom widgets (LK-06) | Every factory already passes the owner: Dropdown `core/WidgetsSetup.lua:127-130`, SearchBox `:153-154`, ReorderList `:205-206`, LineChart `:265-266`, Autocomplete `:295-296`, TestStrip `:316-317`; CopyWindow by descriptor `modules/Export.lua:373-375` (`addonName`); debug console `core/DebugLogSetup.lua:110`; perf panel `core/PerfSetup.lua:43`; sim panel `modules/Sim.lua:361`. None of these surfaces is on the settings panel, and LootHistory calls no Toast (`grep -rn Toast core modules settings` is empty). | None in code. LK-06 skins them more completely, and smoke SKIN-8 / SKIN-17 should see that (section 4). |
| R-6 `ResetToSkin` `"@skin"` | No `ResetToSkin` call and no `fromSkin` companion: `O.FontGroup/BorderGroup/BarGroup` exist only as the degradation stub, `settings/OptionsSetup.lua:170-172`. `"@skin"` occurs only as the degraded facade's mirror of `lib.FROM_SKIN`, `core/SkinSetup.lua:452,473`, which is not a guard. | None. Exception. |
| R-7 DragHandle tooltip `gtip.*` | The AH list's handle tooltip "Drag to re-rank" (`settings/Panel.lua:775`) is drawn by the library. LootHistory has no literal for it. | None. After LK-08 the tooltip takes LootHistory's `gtip.*` because the list names the owner. |
| R-8 exact `q.*` | `NS.QualityColor` (`core/SkinSetup.lua:239-253`) reads the `q.*` token first and the client's `ITEM_QUALITY_COLORS` second. It is used by `modules/BrowserTable.lua:735`, `modules/BrowserWidgets.lua:16` and `modules/AnalyticsFormat.lua:115`. **No host literal stands in for `q.*`.** The two hex tables are deliberate and on the allow-list: `core/Constants.lua:162-170` (`QUALITY_HEX_FALLBACK`, the Minimum-quality option labels, the client hex passed through, `tests/test_skin_literals.lua` ALLOW at its line 41) and `modules/SimWorld.lua:50` (fixture hyperlinks). | Code: none. **Tests go red** (section 3: `tests/test_skin_table.lua:199,323`, `tests/test_browsertable.lua:1069,1074`). |
| R-9 public `DrawsKey` | No reach into `__DrawsKey` (§6). The tests do reach two other internals: `Skin.__P` / `P.media` at `tests/test_skin_table.lua:372-377`, and `Skin.__ace` at `tests/test_skin_settings.lua:15,55`. | None, unless LK-10 adds `DrawsKey` to the per-owner **facade**. In that case the degraded facade's name list (`core/SkinSetup.lua:458-462`) must gain it, or `tests/test_surface_parity.lua:366-373` goes red (it compares the facades key for key). A lib-level `Skin:DrawsKey` needs nothing, because LootHistory keeps no lib-level Skin stub. |
| R-10 standard tab name | The addon already calls it the **Skin** tab (`docs/settings-panel.md:185`). "Appearance tab" survives only in test comments (`tests/panel_support.lua:114`, `tests/test_skinsetup.lua:5,167,185,260`, `tests/test_libka0s.lua:113,810,871`, where the module is still `OptionsAppearance`) and in dated history notes (`docs/smoke-tests.md:219,2383`). | Optional comment polish only. Do not rewrite the dated history notes. |
| R-11 picker title | `RegisterOwner` already passes `label = NS.BRAND` ("Ka0s Loot History", `core/Namespace.lua:13`) at `core/SkinSetup.lua:571-575`. The library's new layout draws the owner line from it. | Code: none. Tests and docs: section 3 and section 4. |

### 1.4 D-LH-1: the AH price table and Ignore settings panel (needs a lead call)

- The AH price table is a host-drawn block **on the settings panel**: `buildAuctionTable` at `settings/Panel.lua:841-951`.
  Its headers are painted at `settings/Panel.lua:885-887` (`NS.Skin.Font(fs)` and `text.headingAlt`). Its row text,
  ticks and info marks are painted through `paintAuctionRow`, `rebuildTicks` (`:619-625`) and `tipScripts`
  (`:678-693`, with `gtip.value` / `gtip.title`). It is repainted on every switch by `repaintAuctionTable`
  (`:811-825`). Every one of these paints is **unconditional**: none asks whether the owner ignores its panel.
- The new-profile default is `ignorePanel = true` (`defaults/Profile.lua:66`). Under that default today, the panel's
  AceGUI rows and check boxes are stock (`settings/Panel.lua:31-41`, PANEL-24), while the AH table's text **and** its
  reorder chrome are skinned.
- After LK-05, the reorder row boxes, handle tints and ghost go stock under the default Scope. The AH table's own text
  stays in the skin's colors and face. That is a three-way mix on one tab.
- Options:
  - (a) Accept the mix and document it.
  - (b) Gate the host paints on the panel scope. This needs a public scope query; `Skin:__PanelSkinned` is internal
    (`LibKa0s/LibKa0s/Skin.lua:626-631`), the same situation R-9 fixes for `__DrawsKey`, so LK-10 could publish both.
  - (c) Have `paintAuctionRow` read through a library primitive that obeys the Scope.
- Recommendation: (b), if LK-05/LK-10 publish a panel-scope query. It matches R-5's intent that everything on the panel
  obeys the Scope. Otherwise use (a) and record it in DECISIONS.md.
- Whichever is chosen, PANEL-23 and SKIN-17 change (section 4).

## 2. Where the addon resolves a HUD face or outline itself

**Nowhere.** LootHistory has no HUD element. `grep -rnE "hud\.|__FontsIgnored|FontsIgnored|GetIgnore\(" core modules settings` is
empty (§6). The only "HUD" words are prose: the library's Skin-tab note quoted in `docs/smoke-tests.md:332`, and the
font-override description in `docs/schema.md:277` and `docs/settings-panel.md:185`.

Every LootHistory string gets its face through library primitives: `S.Text`, `S.Font`, and the primitives' own text.
Examples are `settings/Panel.lua:885,906` and the `S.Font` sites listed at `docs/ARCHITECTURE.md:418-427`. All of them
already go through `P.font`, which honours Ignore fonts (`LibKa0s/LibKa0s/SkinPaint.lua:539`). R-1 has nothing to add.

## 3. Tests that pin current behaviour (and will move)

### Certain to go red on the v1.81.0 re-vendor

| Test | Pins | Why it moves |
|---|---|---|
| `tests/test_skin_picker.lua:303-306` "Skin picker: the title names this addon" | `f.title:GetText() == "Choose a skin for " .. NS.BRAND` | R-11/LK-11: the title becomes "Choose a skin". Rewrite it to assert the title **and** that the owner line reads `NS.BRAND` above the dropdown. Use whatever field LK-11 publishes; read it from LK-11's docs, never guess it. Its row in `docs/test-cases.md:1550` and its prose in `docs/testing.md:131` ("the title naming this addon") change with it. |
| `tests/test_skin_table.lua:323` "NS.QualityColor reads q.*…" | `rgba({ NS.QualityColor(4) }) == rgba({ 0.64, 0.21, 0.93 })` at `%.3f` | R-8: an exact `q.epic` is `a335ee` = 0.639, 0.208, 0.933. Line 322 (token parity) stays. Replace the literal with the exact bytes (`163/255, 53/255, 238/255`), or drop it in favour of line 322. Row: `docs/test-cases.md:1581`. |
| `tests/test_skin_table.lua:197-199` (inside "on Ka0s Default every table surface draws the value it drew before skins") | the item cell's text color `== rgba({ 0.64, 0.21, 0.93 })` | Same R-8 move. The comment at `:197-198` ("writes the client's quality colors out") stays true. |
| `tests/test_browsertable.lua:1069,1074` "test-mode rows hover a sample tooltip…" | mocks `ITEM_QUALITY_COLORS[4] = {0.64, 0.21, 0.93}` and asserts `lines[1][2] == 0.64` and `lines[1][4] == 0.93` **exactly** | The tooltip's color comes from `NS.QualityColor`, which reads the `q.epic` **token** before the mock (`core/SkinSetup.lua:244-249`). So it is the token's 0.64 that passes today, not the mock's. After R-8 the values are 0.6392… and 0.9333…. Fix: assert against `NS.QualityColor(4)` as `tests/test_skin_table.lua:270-271` does, or against the exact bytes. |
| `tests/test_libka0s.lua:830-877` "v1.78.0: the vendored minors…" | exact `assertEqual` on minors that v1.80.0 already moved: `SkinPaint 10` (`:841`, now 11), `SkinPaintControls 8` (`:843`, now 9), `SkinEUI 1` (`:844`, now 2), `SkinAce 3` (`:845`, now 4), `OptionsCompose 12` (`:865`, now 13) | v1.80.0 CHANGELOG versions paragraph (`LibKa0s/CHANGELOG.md:22-26`). Convert each to `>=` with a "N since v1.80.0, pinned there" comment, as `:836-842` already do for v1.79.0. |
| `tests/test_libka0s.lua:890-914` "v1.79.0: the vendored minors…" | exact `Skin 6` (`:897`, now 7), `SkinDefs 14` (`:898`, now 15), `SkinPaintExtras 4` (`:899`, now 5) | Same. Also check `OptionsSkinPicker 1` (`:907`; LK-11 will move it), `Options 34` (`:904`), `Toast 1` (`:902`) and `KIT_VERSION == 44` (`:913`) against the v1.81.0 versions paragraph. |
| `tests/test_libka0s.lua` likely more exact v1.78.0 pins that LK-05/06/08 move | `Widgets 16` `:847`, `WidgetsReorder 2` `:848`, `WidgetsDragHandle 6` `:849`, `WidgetsLineChart 4` `:850`, `WidgetsAutocomplete 4` `:851`, `WidgetsCopyWindow 1` `:852`, `DebugLog 22` `:854`, `DebugLogWindow 1` `:856`, `PerfPanel 10` `:874`, `SimPanel 7` `:875`, and the Options rows `:860-869` | Whichever LK-05/06/08/11 bump. Read v1.81.0's versions paragraph. |
| **New** pin cases | — | Add `v1.80.0` and `v1.81.0` cases pinning their minors and kit revision, following the file's convention (one case per release; earlier pins relaxed to `>=`). `docs/test-cases.md:1713-1714` gains two rows. `tests/test_libka0s.lua` is 914 lines, so there is headroom under 1500. |
| `tests/test_vendor_sync.lua` (kit gate) | the payload equals the tag named in `CLAUDE.md:58` | Roll `CLAUDE.md:58` to v1.81.0 in the re-vendor commit (or the `(unreleased, branch …)` form while the tag is local, `CLAUDE.md:75`). |

### At risk, depending on the shape of LK-05/LK-06/LK-10

| Test | Risk |
|---|---|
| `tests/test_skin_tools.lua:140-145` "the reorder list seam names the owner" asserts `list.skin ~= nil` | If LK-05 drops the palette (`skin` field) while the owner's panel is ignored, this goes red whenever `ignorePanel` is true. `tests/test_skin_settings.lua:41,200` leave it false before this suite runs, so the case probably holds by order alone. Make the precondition explicit, and add the new behaviour as a case (see below). |
| `tests/test_surface_parity.lua:366-373` (degraded facade vs live, key for key) | Red if v1.81.0 adds a facade member (for example `S.DrawsKey`). Fix: add it to `core/SkinSetup.lua:458-462` (a no-op or `"ka0s"`), plus a degraded meaning if callers need one. |
| `tests/test_surface_parity.lua:380-406` (host copy `NS.SKIN_FALLBACK` equals the live Ka0s Default values) | Red only if v1.81.0 changes a Ka0s Default value that `NS.SKIN_FALLBACK` (`core/SkinSetup.lua:93-190`) copies. R-8 touches `q.*`, which is **not** in the fallback. R-2 and R-7 change no token value. No change expected, but re-run it. |
| `tests/test_surface_parity.lua:156` (Options stub carries the live instance surface) | Red if LK-11 or another item adds an Options instance member. The stub `settings/OptionsSetup.lua:149-153` gains it. |
| `tests/test_skin_table.lua:372-377` (uses `Skin.__P.media`) and `tests/test_skin_settings.lua:55` (`Skin.__ace`) | Internals. Red only if renamed. |

### Tests to add (LH-01, a characterization of the new behaviour)

- The AH drag list follows the Scope: under `NS.ApplySkinIgnore(true, nil)` its row boxes, handle and ghost are stock;
  under `false` they are skinned. This rides on LK-05 and goes beside `tests/test_skin_settings.lua:185`.
- If D-LH-1 (b) is taken: the AH table's headers and row text are stock under Ignore settings panel and skinned without it.

## 4. Smoke checks and doc passages whose expectation changes

### `docs/smoke-tests.md`

| Check | Line | Change |
|---|---|---|
| **SKIN-27** The skin picker on a fresh profile | `:2113-2125` | "a small window titled **Choose a skin for Ka0s Loot History**" (`:2114`) becomes: titled **Choose a skin**, with **Ka0s Loot History** on its own line above the skin dropdown, not truncated. The Fail clause "a title that does not name Ka0s Loot History" (`:2122-2123`) becomes "no Ka0s Loot History line above the dropdown, or a cut-off title or name". Mark it amended by LH-02 (R-11). |
| **SKIN-17** The AH price table | `:2052-2054` | State the Scope: with **Ignore settings panel** off the drag ghost, row boxes and handle follow the skin; with it on (the new-profile default) they are stock (R-5/LK-05). Add that the handle's tooltip ("Drag to re-rank") is in the skin's tooltip colors (R-7/LK-08). Adjust to D-LH-1. |
| **PANEL-23** The AH price table follows the skin | `:342-352` | It does not say which Scope it assumes. Under the default (panel ignored), after LK-05 the drag chrome is stock. Add "with **Ignore settings panel** off" or the D-LH-1 outcome. |
| **PANEL-24** The panel's own controls | `:354-365` | No change unless D-LH-1 (b): then "Turn **Ignore settings panel** on → … those controls go back stock" (`:362`) also covers the AH table's text and drag chrome. |
| **SKIN-8** The tool windows follow the skin | `:2014-2021` | Expectation unchanged. LK-06 may skin more of each tool window (debug console, copy windows, perf/sim panels, test strip, autocomplete, line chart), so re-walk it. Add an Ignore fonts clause if LK-06 brings these widgets' fonts under the Scope. |
| **SKIN-24** Ignore fonts wins | `:2098-2100` | Unchanged: no HUD, and every string already goes back to its own face. Re-walk it, because LK-06 brings the custom widgets' faces under Ignore fonts too. |
| **SKIN-1 / SKIN-7** Ka0s Default look and fonts | `:1958-1969`, `:2004-2012` | R-2 does not change LootHistory (it never used the stock look). R-4 adds HUD faces that LootHistory never draws, so SKIN-7's body-face list (`:2007`, "WoW Default the client's Friz Quadrata") stays. No change. |
| Area index / trigger rows | `:40`, `:98-100` | Count unchanged unless a check is added. If D-LH-1 adds a check, bump `SKIN-1 to 37` (`:40`) and list it. |
| Change log at the end | `:2383-2400` region | Append an LH-02 (2026-10-30) amendment line naming SKIN-27, SKIN-17, PANEL-23 and any others touched. Leave the existing dated lines alone. |

### Other docs

| Doc | Line | Change |
|---|---|---|
| `docs/settings-panel.md` | `:187` | "A small window, **Choose a skin for Ka0s Loot History**, …" becomes the "Choose a skin" title plus the owner line above the dropdown (OptionsSkinPicker's new minor). The sentence about the AH table's check boxes and "nothing is painted while **Ignore settings panel** is on" in the same bullet should name the drag list (LK-05) and the D-LH-1 outcome. |
| `docs/testing.md` | `:131` | The `test_skin_picker.lua` row: "the title naming this addon" becomes "the title "Choose a skin" and the owner line naming this addon". `:126` (`test_widgets.lua` row) and the `test_libka0s.lua` row should note the v1.80.0/v1.81.0 pins. |
| `docs/test-cases.md` | `:1550`, `:1581`, `:1713-1714` | Regenerate after the test renames and additions. |
| `docs/ARCHITECTURE.md` | `:359-368` (picker bullet) | Does not quote the title. No change needed; optionally mention the owner line. |
| `docs/ARCHITECTURE.md` | `:384-391` | "`opts.owner` … the AH drag list": add that the list obeys the Scope (LK-05). |
| `docs/ARCHITECTURE.md` | `:401-441` "Intentional exceptions" | Add D-LH-1's outcome if (a): "the AH price table's host text follows the skin under Ignore settings panel". |
| `docs/ARCHITECTURE.md` | `:418-427` (Fonts) | The phrase "Friz Quadrata, which every other skin without a face of its own still draws" is about the **body** face (only WoW Default keeps Friz for body text). R-4 gives HUD faces only. Unchanged. |
| `README.md` | `:149-162` Credits | Lists every OFL face "bundled inside the LibKa0s payload" (`:170-171`). **If LK-04 registers a new face** for a skin's HUD, it ships in this addon's vendored payload and the credits must name it. `DEPENDENCIES.md:113` says fonts arrive in the payload; it lists none by name, so it needs no change. |
| `CLAUDE.md` | `:58` (and `:75` for the unreleased form), `:59` icon line | Roll the provenance line to v1.81.0. Keep the `LibKa0s icons:` declaration and prune with the tag's `tools/prune-icons.lua`. Re-check the icon list if LK-11's picker layout adds a mark (today it uses `eye` and `settings`, `CLAUDE.md:66`). |

## 5. Current state

- **Branch:** `master`, up to date with `origin/master`, **clean**. No other local or remote branch, no stash, one worktree.
  HEAD `b287253` (2026-10-29, "Merge feat/2026-10-28-skin-overrides-picker: adopt LibKa0s v1.79.0's skin overrides and
  first-run picker").
- **Vendored LibKa0s:** `CLAUDE.md:58` "Bundles [LibKa0s](…) v1.79.0 (MIT)."; `CLAUDE.md:59` declares the icons: ban,
  chat, chevron-down, chevron-right, circle-check, clear, close, confirm, copy, eye, graph, info, lock, segment, settings,
  sort-down, sort-up, spreadsheet.
- **Gate on master (run 2026-10-30):**
  - `~/.claude/dev-copilot/bin/ka0s-bounded lua tests/run.lua` → `1830 passed, 0 failed, 1 skipped, 1831 total`, exit 0.
    The one skip is the kit's own "diagnostics contract: an addon that opts out…" (this addon keeps the default).
  - `~/.claude/dev-copilot/bin/ka0s-bounded luacheck .` → `Total: 0 warnings / 0 errors in 151 files`, exit 0.
  - 1500-line cap: the largest own files are `tests/test_browser.lua` 1459, `modules/BrowserTable.lua` 1407,
    `tests/test_browsertable.lua` 1392 and `modules/Browser.lua` 1384. All are under the cap. Keep new cases out of the
    first three; `tests/test_libka0s.lua` (914) and `tests/test_skin_*.lua` have room.
- **The old red TestData suite is fixed.** The holder-move rollup case was fixed by `701a1fe LH-FX1: Give the
  holder-move rollup test the clock its sample was stamped with`, and the bounded-lint branch merged at `7debc49`.
  Today every TestData case passes, including "the sample rollup books a holder move's loss and gain on each holder".
  **Nothing is red. LootHistory joins the run** (`00_PLAN.md`, "LootHistory joins only on a green gate on master").

### What the v1.79.0 → v1.81.0 re-vendor owes beyond the others

The other fourteen addons are on v1.80.0. LootHistory also absorbs v1.80.0's own "What a consumer owes"
(`LibKa0s/CHANGELOG.md:208-224`):

1. **Owner tokens, slot remap and icon-border family** (Skin minor 7, SkinPaint 11, SkinPaintExtras 5,
   SkinPaintControls 9, SkinEUI 2, SkinDefs 15, OptionsCompose 13): opt-in. LootHistory passes no `tokens`, no
   `opts.tokens`, no `S.IconBorder{fromSkin}` and no `BorderGroup{fromSkin="icon"}`, so it draws what it drew on
   v1.79.0. Nothing is owed.
2. **`Skin:AliasAceType`** is added at the library level. LootHistory keeps no lib-level Skin stub (its degraded arm
   builds only a facade, `core/SkinSetup.lua:446-566`) and does not call it. Nothing is owed. The facade's VOCAB did
   not change in v1.80.0 (`git diff v1.79.0 v1.80.0 -- LibKa0s/Skin.lua` touches no VOCAB entry), so the parity test
   holds for that step.
3. **TreeGroup painting (SkinAce 4):** LootHistory's only `PaintAceTree` is the Profiles page (`settings/Profiles.lua:68-69`,
   AceDBOptions' flat profile table, with no tree group). Nothing is owed.
4. **`opts.stockDefault`** (v1.80.0, opt-in, retired by v1.81.0): never used. Nothing is owed.
5. **Version pins:** the exact pins in `tests/test_libka0s.lua` that v1.80.0 moved (section 3) plus a new v1.80.0 case.
   This is the concrete extra work over the other addons.
6. Kit revision stays 44 through v1.80.0 (`LibKa0s/CHANGELOG.md:26`). Check v1.81.0's.
7. Then v1.81.0's own "What a consumer owes", as for every addon.

Use `/dev-copilot:wow-revendor-libka0s`. Its delta base is the provenance line (v1.79.0), so it writes the span bundle
`docs/revendor/<date>-v1.80.0-v1.81.0/`, because v1.80.0 went unrecorded here.

## 6. Nothing to change: exceptions.tsv candidates (proof commands, run from the LootHistory root)

| Item | Claim | Proof (each prints nothing, exit 1, unless noted) |
|---|---|---|
| LH-01 (R-1/R-4) | No HUD face or outline is resolved, and there is no Ignore-fonts workaround | `grep -rnE "hud\.\|__FontsIgnored\|FontsIgnored\|GetIgnore\(" core modules settings` |
| LH-01 (R-2) | No `stockDefault` / skin `stock` caller | `grep -rn stockDefault core modules settings`. The only `stock =` is the view spec at `modules/HoldingsTab.lua:668`. |
| LH-01 (R-5) | No hand-rolled Scope guard | `grep -rnE "__PanelSkinned\|GetIgnore\|IsPanelSkinned" core modules settings` |
| LH-01 (R-6) | No `ResetToSkin` guard and no fromSkin companion | `grep -rnE "ResetToSkin" core modules settings`. `FROM_SKIN` occurs only in the degraded facade, `core/SkinSetup.lua:452,473`; `FontGroup/BorderGroup/BarGroup` only in the stub, `settings/OptionsSetup.lua:170-172`. |
| LH-01 (R-9) | No `__DrawsKey` reach-in | `grep -rnE "__DrawsKey\|DrawsKey" core modules settings tests --exclude-dir=_kit` |
| LH-01 (R-3) | No close-button tint handling | `grep -rnE "CloseButton.*(Vertex\|Tint)\|closeRest\|GetVertexColor" core modules settings` |
| LH-01 (R-7) | No drag-handle tooltip literal | `grep -rnE "DragHandle\|W\.DragHandle" core modules settings` |

LH-01 is therefore **not empty only if** D-LH-1 (b) is taken, or a test needs re-pointing (the R-8 and R-11 tests in
section 3, which belong to LH-RV's re-vendor commit or to LH-01). LH-02 (docs and smoke) is **not** an exception:
SKIN-27, SKIN-17, PANEL-23 and `docs/settings-panel.md:187` must change.
