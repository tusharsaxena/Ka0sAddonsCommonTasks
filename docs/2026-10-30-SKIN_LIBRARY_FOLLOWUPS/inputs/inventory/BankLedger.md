# M0 inventory: BankLedger (prefix BL)

Read-only inventory for the run `feat/2026-10-30-skin-library-followups` (rulings R-1..R-12 in `../../00_PLAN.md`).
Scope: `/mnt/d/Profile/Users/Tushar/Documents/GIT/BankLedger`, excluding `libs/` and `tests/_kit/`. Every path below is
relative to that repo unless it starts with `LibKa0s/`, which means `/mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/`.

**In short:** BankLedger needs very little code work. It has no HUD, and the rollout already removed its
only `stockDefault` caller and the close-tint workaround that went with it (BL-A1, d20a28b). It never reaches
`__DrawsKey` or `ResetToSkin`, and it has no hand-rolled Scope guard. What changes is one pinned test (the
picker title), the picker's docs and smoke checks, and a few comments and doc lines that still mention the
retired `stockDefault`. Expect BL-01 to be close to empty, and expect BL-02 to carry most of the work.

---

## 5. Current state (run first)

| Fact | Value | Evidence |
|---|---|---|
| Branch | `master`, tracking `origin/master`, no divergence (`## master...origin/master`) | `git status -sb` |
| Tree | clean | `git status -sb` printed nothing else |
| HEAD | `647e34f Merge feat/2026-10-29-skinning-rollout` | `git log --oneline -1` |
| Stashes / extra worktrees | 0 / none (only the main worktree at 647e34f) | `git stash list \| wc -l` → 0; `git worktree list` |
| Vendored LibKa0s | **v1.80.0** | `CLAUDE.md:48` "Bundles [LibKa0s](…) v1.80.0 (MIT)." |
| Icons line | `chevron-down, chevron-right, clear, close, confirm, copy, export, eye, info, search, settings, sort-down, sort-up` | `CLAUDE.md:49` |
| Tests | `1509 passed, 0 failed, 1 skipped, 1510 total` (runner exit 0) | `~/.claude/dev-copilot/bin/ka0s-bounded lua tests/run.lua` (tail) |
| The one skip | `SKIP diagnostics contract: an addon that opts out lands the report and leaves logging off — this addon keeps the default …` (a kit case that does not apply; not a skin case) | test output line 1499 |
| Lint | `Total: 0 warnings / 0 errors in 111 files` (exit 0) | `~/.claude/dev-copilot/bin/ka0s-bounded luacheck .` |
| 1500-line cap | OK. Largest non-vendored Lua is `tests/test_browser.lua` at 1442 lines (then `modules/Browser.lua` 1322 and `modules/LedgerTable.lua` 1046) | `wc -l` |

**Gate: GREEN on master.**

LibKa0s majors this addon consumes (one `LibStub("LibKa0s-*-1.0")` each, Widgets 3 times, Sim twice): Bus, Core,
DebugLog, Env, Item, Launcher, Lifecycle, Media, Options, Pool, Schema, Sim, **Skin**, Slash, **Widgets**. It does
not consume WidgetsReorder, WidgetsDragHandle, WidgetsLineChart or Toast (grep of `Reorder|DragHandle|LineChart|Toast`
over `core modules settings` finds nothing).

---

## 1. Workarounds of library gaps the release closes

### R-1 / LK-01: Ignore fonts on the HUD (`NS.SkinFontsIgnored`-style patches): **none. BankLedger has no HUD.**

- Proof: `grep -rniE 'hud' core modules settings defaults locales` finds no `hud.font`, no `hud.outline` and no
  HUD element. The only Scope code is the plain write/apply seam: `core/SkinSetup.lua:95` (paths),
  `:294-297` (write `{ panel, fonts }`), `:314-318` (`storedIgnore`), `:630-636` (`NS.ApplySkinIgnore` →
  `Skin:SetIgnore`), `:654` (applied with the stored pair).
- The docs already say so: `docs/smoke-tests.md:1075-1077` ("Bank Ledger has no HUD, so the rollout's one-time
  HUD style reset (O2) changes nothing here … BL-03 is recorded as an exception").
- → **exceptions.tsv** row (see §6).

### R-2 / LK-02: `stockDefault` / `stock` callers: **none left in code. BL-A1 already removed the last one.**

- Proof: `grep -rnE 'stockDefault|stock *=' --include='*.lua' core modules settings` finds only comments.
  BL-A1 (`git show d20a28b`) retired the close control's `stockDefault`, the class-colored hover, the
  `bl.closeRest` owner token, and BL-02's switch-back re-tint workaround (the weak list plus its `OnLooksChanged`
  listener, 138c643).
- **How it looks under Ka0s Default afterwards: unchanged.** Every BL surface already paints the Ka0s look under
  Ka0s Default. The close control already takes `close.rest`/`close.hot` there (`modules/Browser.lua:96-102,128`).
  Retiring `stockDefault` changes no BL pixel.
- The library still uses `opts.stock` internally on settings tabs (`LibKa0s/LibKa0s/OptionsTabs.lua:495,503`).
  BL's settings pages are stock by default anyway (`ignorePanel = true`, `defaults/Profile.lua:84`), so this only
  matters with Ignore settings panel off. Re-check SKIN-8 there (§4).
- **Stale mentions of the retired option (XX-01/XX-02 tidy, optional but recommended):** each says "no
  `stockDefault`". That stays true, but after R-2 it describes an option that no longer exists:
  - `modules/Browser.lua:98-99` (comment: "no `stockDefault`, and no hover scripts of the host's own")
  - `docs/ARCHITECTURE.md:509-510` ("BL-A1 retired `bl.closeRest` with the `stockDefault` it served")
  - `docs/ARCHITECTURE.md:543-544` ("with no `stockDefault` and no host hover scripts")
  - `docs/ARCHITECTURE.md:695` (the `standalone-windows` decline row: "(no `stockDefault`, no host hover scripts)")
  - `docs/windows.md:32-33` ("with no `stockDefault`")
  - `docs/module-map.md:38` ("BL-A1: no `stockDefault`, no host hover scripts")
  - `tests/test_skin_windows.lua:226` (comment) and `:250` (comment "red under: the BL-02 stockDefault")
- **Test pinning it:** `tests/test_skin_windows.lua:255-259` reads `Skin.painted[close].calls.CloseButton[1]` and
  asserts `not opts.stockDefault`. After LK-02 that assert passes vacuously. Either drop those lines or keep them
  as a regression guard. It also reaches into `lib.painted`, a library internal (see R-9 below).

### R-3 / LK-03: `S.CloseButton` prior-tint save: **workaround already gone (BL-A1). Nothing left to delete.**

- `B:MakeCloseButton` (`modules/Browser.lua:104-130`) builds the art untinted: a WHITE texture at `:110-114`, or
  the × FontString at `:116-123` with `SetFont(STANDARD_TEXT_FONT, 24, "")` then `NS.Skin.Font(x)`. It then calls
  `NS.Skin.CloseButton(close)` with no opts (`:128`). There is no host hover script and no host tint.
- After LK-03 the library saves the art's own tint on first paint: white for the texture, and the FontString's
  default for the glyph. It restores that tint on unpaint. BL never unpaints its close control under any skin, so
  nothing on screen changes. The rollout's follow-up 6 (`docs/2026-10-29-SKINNING_ROLLOUT/99_REPORT.md`) was found
  by BL only because of the now-retired `stockDefault`.
- Degraded arm: the host facade's `S.CloseButton` (`core/SkinSetup.lua:549-566`) tints from the host copy and
  saves nothing. That is correct, because without the library there is no skin switch.
- Tests that pin the close control (all should stay green, behaviour unchanged): `tests/test_skin_windows.lua:248-264`
  (Ka0s Default rest/hot), `:266-280` (switch and back), plus the cases listed in `docs/test-cases.md:1608-1611`;
  `tests/test_marks.lua:74,83,91,481`.

### R-5 / LK-05, LK-06: hand-rolled Scope guards around `S.Text`, `WidgetsReorder` and other widgets: **none.**

- `S.Text` is called only on **window** strings, never on settings-page strings:
  `modules/Browser.lua:236,289` (tab labels), `:1108` (test badge), `:1173,1178` (footers);
  `modules/LedgerTable.lua:742`; `modules/SessionWindow.lua:612`; `modules/Insights.lua:165`;
  `modules/InsightsWidgets.lua:460,791,833,883,896,928`. None is guarded by a Scope read. Proof:
  `grep -rnE 'ignorePanel|ignoreFonts|IsIgnor|GetIgnore' core modules settings` finds only the seam's
  paths and writes (`core/SkinSetup.lua:95,295-296`).
- BL does not use `WidgetsReorder` (no hit for `Reorder`).
- **Library custom widgets BL consumes that LK-06 will skin and scope.** BL passes each the owner and does not
  paint any of them itself:
  - `W.Dropdown` via `B:MakeDropdown` (`modules/Browser.lua:315-323`, owner `:322`; it injects `glyphFont = C.FONT_MONO`
    at `:320`, the mono ▲/▼ face). Called at `:905,972,981,990,999,1007,1015,1023` and `modules/Export.lua:413`.
  - `W.SearchBox` via `B:MakeSearchBox` (`modules/Browser.lua:333-339`, owner `:337`).
  - `W.Autocomplete` via `B:MakeAutocomplete` (`modules/Browser.lua:350-356`, owner `:354`).
  - `W.TestStrip` ×2 (test and sim strips) via `buildModeStrip` (`modules/Browser.lua:871-886`, owner `:874`).
  - `W.CopyWindow` (`modules/Export.lua:278-299`, `addonName` as owner `:282`, `font = FONT_MONO` `:284`).
  - `W.CloseMenu` (`modules/Browser.lua:1210,1257`; `modules/Export.lua:450`).
  - The DebugLog console and its copy window (`core/DebugLogSetup.lua:84,94,141`: `addonName`, no `applySkin`).
  - The Launcher tooltip (`core/LauncherSetup.lua:283-288`: the host line in `gtip.subtle`).
  - The Sim panel and strip (`modules/Sim.lua:228ff`, `d.panel`).
  - The settings panel's library options widgets: `O.IdList` (`settings/Panel.lua:408`), `O.SubTabStrip` (`:481`),
    `O.TextRow` (`:143`), `O.InlineButtonPair` (`:172`), `O.AppearanceTab` (`:787`), `O.KeybindingsTab` (`:790`).
  - Pinned by `tests/test_skinsetup.lua:306` ("every Widgets factory this addon calls is handed the owner").
  Nothing in BL changes for LK-06. The **expectations** of SKIN-7, SKIN-8 and SKIN-10 do (§4).
- **One host-side scope gap to decide (XX-01 candidate, not a workaround):** the Filters tab's id list
  hands the library a pre-colored empty text, `emptyText = (NS.SkinEscape("text.disabled") or "") .. "(none)|r"`
  (`settings/Panel.lua:421`). It reads the skin token even while **Ignore settings panel** is on, so the "(none)"
  stays in the skin's `text.disabled` on an otherwise stock page. Under Ka0s Default that is `|cff808080`, the same
  bytes as before, so the gap shows only under a non-default skin with Ignore settings panel on. Once LK-05/06
  makes `O.IdList` obey the Scope, this host escape is the one thing left on the page that ignores it. Options:
  (a) pass plain "(none)" and let the library paint its empty text in `text.disabled` (if LK-06 gives IdList an
  empty-text role), or (b) leave it and record it. Documented at `docs/settings-panel.md:156-158`.

### R-6 / LK-07: `ResetToSkin` guards against `"@skin"`: **none.**

- Proof: `grep -rn 'ResetToSkin' core modules settings tests/*.lua` finds nothing. `"@skin"` appears only as
  the degraded facade's `FROM_SKIN` constant and its `Resolve` (`core/SkinSetup.lua:457,477-480`), which mirror the
  library's contract and are not a guard. BL has no `FROM_SKIN` bool companion.

### R-9 / LK-10: reach into `Skin:__DrawsKey` or other internals

- **Production code:** none. `grep -rn 'DrawsKey\|Skin\.__\|Skin\.painted' core modules settings` finds nothing.
- **Tests only** (they read library internals; a DrawsKey rename does not break them, but they would break if
  LK-03 or LK-06 changes the record shape):
  - `tests/test_skin_windows.lua:254-256`: `Skin.painted[close]`, `rec.owner`, `rec.calls.CloseButton`
  - `tests/test_libka0s.lua:507-509`: `Skin.painted[D._frameForTest]`, `rec.owner`
  - `tests/test_skin_tools.lua:62-65` (`ownerOf`): `Skin.__ace[w].owner`, used at `:124,149`
  `lib.painted` is documented in `LibKa0s/LibKa0s/Skin.lua:22`, so it is semi-public. `__ace` is internal. If LK-10
  adds a public "which owner painted this" read, switching these tests to it is a cheap improvement. It is not
  required.

### R-7 / LK-08 and literal tooltip colors standing in for `gtip.*`: **none.**

- Every tooltip line BL writes reads a `gtip.*` token at hover time: `modules/Browser.lua:395-396` (body),
  `:862-866` (strip tip title/body); `modules/LedgerTable.lua:538-550` (gold movement, column header),
  `:614-623` (`gtip.muted` hints); `modules/InsightsWidgets.lua:30-32,75-76` (cached `W.TIP_*` from `gtip.*`) used
  at `:427,469-470,798`; `core/LauncherSetup.lua:286-287` (`gtip.subtle`).
- The literal-color gate `tests/test_skin_literals.lua` (allow-list `:41-48`) already enforces this. Its only
  allowed literals are the quality-option hex (`core/Constants.lua`), the chat prefix and the slash fallback.
- BL does not use WidgetsDragHandle, so LK-08 does not touch it.

### R-8 / LK-09: literal quality colors standing in for `q.*`: **none to delete. BL already reads `q.*`.**

- `NS.QualityColor(q)` (`core/SkinSetup.lua:239-255`) reads the skin's `q.poor..q.legendary` token first and falls
  back to `ITEM_QUALITY_COLORS` (needed for qualities 6-8 and for a skin that leaves `q.*` alone, so it **stays**).
  Callers: `modules/LedgerTable.lua:46,208,211-217,461-465`; `modules/Browser.lua:512-513,700`;
  `modules/InsightsWidgets.lua:128-129` → `modules/Insights.lua:736,743,862`.
- **What R-8 changes on screen:** today Ka0s Default draws the library's **rounded** values
  (`LibKa0s/LibKa0s/SkinDefs.lua:370-371`: poor 0.62, uncommon {0.12,1,0}, rare {0,0.44,0.87},
  epic {0.64,0.21,0.93}, legendary {1,0.5,0}). After LK-09 it draws the client's exact values
  (9d9d9d, 1eff00, 0070dd, a335ee, ff8000). These are sub-byte or one-byte moves on item names, the Quality
  column, the Quality dropdown options, autocomplete suggestions and Insights' quality labels. No BL code changes.
- Comment that becomes exactly true after R-8: `core/SkinSetup.lua:243-244` ("Ka0s Default writes the client's own
  colors out"). Doc: `docs/ARCHITECTURE.md:585-586` ("item quality (`q.*`, the client's values under Ka0s
  Default)"). Both are true after R-8 and need no edit.
- **Host copy:** `NS.SKIN_FALLBACK["q.common"] = {1,1,1,1}` (`core/SkinSetup.lua:163`). White is exact before and
  after R-8, so the parity test `tests/test_surface_parity.lua:631-656` stays green. No other `q.*` is in the
  host copy.
- **Tests:** none pins a rounded value. `tests/test_autocomplete.lua:162-167` compares with `NS.QualityColor(3)`
  itself, so it survives. Proof: `grep -rnE '0\.62|0\.44|0\.87|0\.64, ?0\.21' tests/*.lua core modules` finds only
  unrelated `chart.*` and `menu.*` values.
- The settings panel's Minimum-quality labels use the client hex directly (`core/Constants.lua:240-255`, allow-listed
  at `tests/test_skin_literals.lua:42-43`, documented at `docs/ARCHITECTURE.md:578`). That is game meaning, the
  same as `q.*` after R-8. No change.

### R-11 / LK-11: picker title: **no host code. One test and the docs change.**

- BL hands `O.SkinPicker` a spec with no title (`core/SkinSetup.lua:376-387`). The library builds the title from
  `TITLE_FOR = "Choose a skin for %s"` (`LibKa0s/LibKa0s/OptionsSkinPicker.lua:106,240,690`) and the owner label,
  which is `NS.BRAND_NAME` (`core/SkinSetup.lua:598-603`). BL does not localize that string (no hit in `locales/`).
- **Test that must move:** `tests/test_skin_picker.lua:272-276` "Skin picker: the title names this addon" asserts
  `f.title:GetText() == "Choose a skin for " .. NS.BRAND_NAME`. Under LK-11 it becomes the title
  `"Choose a skin"` plus the addon name (`NS.BRAND_NAME`) on its own line above the dropdown. Assert it through
  whatever field LK-11 exposes, for example `f.label`/`f.owner`. Rename the case to match, and regenerate the
  matching `docs/test-cases.md:1631` entry with the test count badge.

### R-4 / LK-04: HUD fonts for the non-Ka0s skins: **nothing (no HUD).**

### R-10 / WS-01: the standard renames the tab "Appearance" → "Skin": **nothing in BL unless the library renames the key.**

- BL already shows "Skin" (the library's label). "Appearance" in BL is the **group key**, not a label:
  `core/SkinSetup.lua:380-384` (picker spec `tab = "Appearance"`), `settings/Schema.lua` (the skipRender group),
  `tests/test_skin_picker.lua:106,128`, `tests/test_schema.lua:308,344`, `tests/panel_support.lua:74-80`,
  `tests/test_libka0s_slash.lua:98-104`, `tests/test_panel_filters.lua:876-880`, `docs/ARCHITECTURE.md:517`
  ("Skin tab (key `Appearance`)"). WS-01 changes only the standard's text. If LK-11 or LK-06 changes the key
  `O.SelectTab` expects, every line above moves with it.

---

## 2. Where BankLedger resolves a HUD face or outline itself: **nowhere.**

BL resolves faces only through `S.Font` / `S.Text` / the primitives (`modules/LedgerTable.lua:582,600,756,996`;
`modules/SessionWindow.lua:362,449`; `modules/InsightsWidgets.lua:507,516,583,589,638,645,711,720,855,861`;
`modules/Export.lua:354`; `modules/Browser.lua:120,382`). It types a face only for:
- the mono ▲/▼ glyph, `C.FONT_MONO` (`modules/LedgerTable.lua:591`, `modules/SessionWindow.lua:373`,
  `modules/Browser.lua:320`, `modules/Export.lua:284`), the documented debug-logging-§2 exception;
- the close fallback ×, `STANDARD_TEXT_FONT` then `NS.Skin.Font` (`modules/Browser.lua:117-120`);
- Insights card resizes that read the current face back (`modules/InsightsWidgets.lua:480-496,929-930`).
None of these is a HUD face, so R-1 asks nothing of BL.

---

## 3. Tests that pin current behaviour (by ruling)

| Ruling | Test | Line | Changes? |
|---|---|---|---|
| R-11 | `tests/test_skin_picker.lua` "the title names this addon" | 272-276 | **Yes**: new title plus the label line |
| R-11 | `tests/test_skin_picker.lua` other picker cases (spec, preview, Apply, close, eye, degraded) | 106-366 | Re-run only. The layout change may move `f.dd`, `f.apply` and `f.close`; `pickRow` must still find the rows |
| R-2 | `tests/test_skin_windows.lua` close control, `not opts.stockDefault` | 255-259 | Vacuous after LK-02: drop or keep as a guard |
| R-3 | `tests/test_skin_windows.lua` close rest/hot under Ka0s Default and on switch | 248-280 | No (stays green; R-3 restores only on unpaint) |
| R-3 | `tests/test_marks.lua` close art | 74-120, 481 | No |
| R-8 | `tests/test_autocomplete.lua` quality-colored suggestion | 162-167 | No (compares with `NS.QualityColor`) |
| R-8 | `tests/test_surface_parity.lua` host copy == library Ka0s Default | 631-656 | No (`q.common` is white either way) |
| any new vocab | `tests/test_surface_parity.lua` degraded facade answers every live facade name | 604-606 | **Yes, if** LK-01..11 adds a facade name (for example a public `DrawsKey` on `For()`'s facade or a new primitive): add it to the degraded list `core/SkinSetup.lua:462-470` or the case goes red |
| R-5 | `tests/test_skin_tools.lua` Ignore settings panel paints nothing | 144-150 | Re-run. If LK-05/06 makes `O.IdList`/`O.SubTabStrip` obey the Scope, this case might widen to cover them |
| R-5 | `tests/test_skinsetup.lua` every Widgets factory handed the owner | 306 | No |
| R-1 | `tests/test_skinsetup.lua` Ignore fonts reaches library and profile | 253 | No |
| internals | `tests/test_skin_tools.lua:62-65` (`Skin.__ace`), `tests/test_libka0s.lua:507`, `tests/test_skin_windows.lua:254` (`Skin.painted`) | — | Only if LK changes those record shapes |

---

## 4. Smoke checks and doc passages whose expectation changes

### `docs/smoke-tests.md`

- **SKIN-19** (`:1170-1176`): "a small window, **Choose a skin for Ka0s Bank Ledger** … a dropdown of the skins, an
  eye and a gear beside it, **Apply** under it". **R-11:** the title becomes "Choose a skin". "Ka0s Bank Ledger"
  sits on its own line above the dropdown, untruncated, and the window grows to fit. Fail: the name cut off or
  missing.
- **SKIN-26** (`:1201-1205`): "one picker opens, naming one addon". It still names the addon, but now on the label
  line. Reword it to "the addon named above its dropdown".
- **SKIN-20 / 21 / 22 / 23** (`:1177-1193`): they describe the dropdown, eye and gear. If LK-11 moves them, re-read
  each for layout words. No behaviour changes.
- **SKIN-10** (`:1133-1138`): "Turn **Ignore fonts** on → every string goes back to the game's own face … the debug
  console keeps its mono face". **R-5/LK-06:** the library widgets (dropdowns and their menu, the search box and
  its suggestions, both mode strips, the copy windows, the sim panel) must now **also** keep their own face with
  Ignore fonts on. Extend the check to name them. Fail: one of them still in the skin's face. (Today they may follow
  the skin's face regardless; that is exactly the gap R-5 closes.)
- **SKIN-8** (`:1119-1125`): with **Ignore settings panel** on, "Bank Ledger's pages go back to the game's look".
  **R-5/LK-06:** the library-drawn page widgets (the Filters sub-strip `O.SubTabStrip`, the id list `O.IdList`, the
  landing page) must now also go stock with it on, and be skinned with it off. Add: "the id list's *(none)* follows
  too" if §1's `settings/Panel.lua:421` is fixed, or note it as the known exception if not. **R-2:** with Ignore
  settings panel off under Ka0s Default, the library's tab art (`OptionsTabs.lua` `stock = …`) now paints the Ka0s
  look rather than staying stock. Check the expectation wording if it says "stock under Ka0s Default".
- **SKIN-7** (`:1112-1118`): the tool windows follow the skin. Unchanged under the default Scope; with Ignore
  fonts on, see SKIN-10.
- **SKIN-1** (`:1066-1079`): "the same colors … as before the rollout". **R-8** makes quality colors exact again
  (sub-byte moves), so this stays true. Optionally add a line: "item quality colors are the client's exact values".
  The HUD sentence at `:1075-1077` stays (no HUD).
- **SKIN-9** (`:1126-1132`): body/title faces per skin. **R-4** adds HUD faces, but BL has no HUD, so no change.
- **SKIN-4 / LEDG-35** (`:1094-1100`, `:554-558`): the close control. No change from R-3. LEDG-35's re-run is still
  owed from BL-A1 (`:1347-1348`).
- **DEGRADED-15** (`:1271-1277`): no change (the degraded facade is the host's).
- **"Owed" ledger** (`:1345-1348`): add this run's rewritten checks (SKIN-8, SKIN-10, SKIN-19, SKIN-26 and the
  picker layout checks) as owed.

### Doc passages

- `docs/settings-panel.md:129-130`: "A small window, **Choose a skin for Ka0s Bank Ledger**: a dropdown of the skins
  …". Rewrite it for R-11 (title "Choose a skin"; the addon's name on its own line above the dropdown).
- `docs/settings-panel.md:150-158`: "nothing is painted while **Ignore settings panel** is on" and the `(none)` in
  `text.disabled`. Extend this to the library page widgets per LK-05/06, and settle the `(none)` escape (§1).
- `docs/settings-panel.md:352` (row table: `ignoreFonts` "every string keeps its own face and size"). After LK-05/06
  it is literally true of the library widgets too. Wording can stay; optionally say "including the library's
  widgets".
- `docs/ARCHITECTURE.md:518-526` (first-run picker paragraph): it does not quote the title. No change unless the
  layout is mentioned.
- `docs/ARCHITECTURE.md:509-510, 543-544, 695`; `docs/windows.md:32-33`; `docs/module-map.md:38`;
  `modules/Browser.lua:98-99`: the retired `stockDefault` mentions (§1 R-2).
- `docs/ARCHITECTURE.md:584-586` ("Game-meaning colors: item quality (`q.*`, the client's values under Ka0s Default)
  … **and the close control's Ka0s Default hover**"). The close-hover clause is **already stale** since BL-A1 (the
  hover is `close.hot`, not a game color). Drop it in BL-02.
- `docs/ARCHITECTURE.md:591-595` (Fonts bullet: "with **Ignore fonts** on every string keeps its own face and size …
  **the close button's × keeps its own**"). The × clause is **already stale** since efbf369 (`modules/Browser.lua:118-120`
  now applies `NS.Skin.Font` to the fallback ×). Fix it in BL-02. If LK-06 lands, extend "every string" to the
  library widgets.
- `docs/testing.md`: no skin, picker or Ignore-fonts passage (`grep -niE 'skin|picker|stockDefault' docs/testing.md`
  finds only luacheck `ignore` lines). No change beyond the regenerated test count if the doc carries one.
- `README.md`: no picker title, no Ignore-fonts or HUD passage (`grep -niE 'picker|ignore fonts|Choose a skin'
  README.md` → only `:194`, the icon credit for the picker's eye and gear). No change, apart from a test-count badge
  if BL-02 changes the count.
- `docs/test-cases.md:1631` (generated): the renamed picker-title case.
- `CLAUDE.md:48`: the provenance line rolls to v1.81.0 (XX-RV). Check `:49` (icons) against the v1.81.0 catalog if
  LK-11 adds a mark to the picker.

---

## 6. Nothing to change (exceptions.tsv candidates, each with its proof)

| Would-be item | Why none | Proof command (run in `/mnt/d/Profile/Users/Tushar/Documents/GIT/BankLedger`) |
|---|---|---|
| BL HUD Ignore-fonts patch (R-1/LK-01) | No HUD, no `hud.*` read | `git grep -nE 'hud\.(font\|outline)\|SkinFontsIgnored' -- core modules settings defaults` → no output |
| BL HUD face per skin (R-4) | No HUD | same as above |
| BL `stockDefault`/`stock` callers (R-2) | Removed by BL-A1 (d20a28b) | `git grep -nE 'stockDefault\s*=\|stock\s*=\s*\{' -- '*.lua' ':!libs' ':!tests/_kit'` → no output |
| BL close-button tint handling (R-3) | Removed by BL-A1. The host passes no opts and sets no hover | `git grep -nE 'HookScript\("On(Enter\|Leave)"' -- modules/Browser.lua` shows only the strip's tooltip hooks (`:878,884`), none on the close; `sed -n 104,130p modules/Browser.lua` |
| BL ResetToSkin guard (R-6) | Never called | `git grep -n ResetToSkin -- ':!libs' ':!tests/_kit'` → no output |
| BL `__DrawsKey` reach-in (R-9) | Never called | `git grep -n DrawsKey -- ':!libs' ':!tests/_kit'` → no output |
| BL DragHandle tooltip colors (R-7) | Widget not used; every host tooltip line is `gtip.*` (gate `tests/test_skin_literals.lua`) | `git grep -n DragHandle -- core modules settings` → no output |
| BL `q.*` literals (R-8) | Already reads `q.*` through `NS.QualityColor` | `git grep -nE '0\.62, ?0\.62\|0\.12, ?1, ?0\|0, ?0\.44\|0\.64, ?0\.21' -- core modules settings` → no output |
| BL hand-rolled Scope guards (R-5) | None | `git grep -nE 'ignorePanel\|ignoreFonts\|IsIgnor\|GetIgnore' -- core modules settings` → only `core/SkinSetup.lua:95,295,296` (the write seam) |

**Expected BL items:** **BL-RV** (re-vendor v1.81.0, roll `CLAUDE.md:48`, meet "What a consumer owes", add any new
facade name to the degraded list at `core/SkinSetup.lua:462-470` so `tests/test_surface_parity.lua:604` stays green).
**BL-01** is small: the vacuous `stockDefault` assert (`tests/test_skin_windows.lua:255-259`), the
`modules/Browser.lua:98-99` comment, and optionally the `settings/Panel.lua:421` `(none)` scope gap. If the
implementer leaves the `(none)` gap, BL-01 can instead be an exception with the R-2/R-3 proofs above. **BL-02**:
`tests/test_skin_picker.lua:272-276`, `docs/settings-panel.md:129-130,150-158`, SKIN-8/10/19/26 (+20-23 layout
words), the owed ledger, the stale ARCHITECTURE lines (`:509-510,543-544,584-586,591-595,695`), `docs/windows.md:32-33`,
`docs/module-map.md:38`, and the regenerated `docs/test-cases.md`.
