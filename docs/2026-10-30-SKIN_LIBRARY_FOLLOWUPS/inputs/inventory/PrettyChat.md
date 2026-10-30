# M0 inventory: PrettyChat

Read-only inventory for the LibKa0s v1.81.0 follow-ups (rulings R-1..R-11 of `../../00_PLAN.md`). Scope is
`/mnt/d/Profile/Users/Tushar/Documents/GIT/PrettyChat`, excluding the vendored `libs/` and `tests/_kit/` (read only
for reference). Every path below is relative to the PrettyChat repo root unless it says otherwise. Read on
2026-10-30 at master `cfd8c58`.

## 0. Bottom line

PrettyChat is a chat-formatting addon with **no HUD** and **no frame of its own** (`docs/ARCHITECTURE.md:201-204`,
`:235-237`; `docs/smoke-tests.md:762-764`). It carries **no workaround** of the gaps v1.81.0 closes, apart from one
adjacent panel-Scope color guard (`NS.PanelEscape`) that LK-05 as written does not replace. No `stockDefault`/`stock`
caller, no `hud.*` read, no `__DrawsKey`, no `ResetToSkin`, no `S.CloseButton`, no `q.*`, no `S.Text`, no
`ReorderList`, no other library widget it calls. So **PC-01 is almost certainly an exception** (one row per
ruling, section 6) unless LK-05 ships a panel-scoped color read.

What PC-RV / PC-02 actually have to do:

- **PC-RV:** re-vendor v1.81.0, roll the provenance line (`CLAUDE.md:44`) and the four other "v1.80.0" mentions
  (section 5), and keep the degraded facade stub (`core/SkinSetup.lua:305-313`) in step with any facade vocabulary
  name v1.81.0 adds (the parity test `tests/test_skinsetup.lua:295-299` goes red otherwise).
- **PC-02:** the picker-title smoke check SKIN-10 (`docs/smoke-tests.md:830-837`, R-11); the README font credits if
  LK-04 ships a new face (`README.md:106-115`); and, **only if LK-06 puts the library tool windows (debug console,
  copy window) under the Scope**, SKIN-1/3/8/10/13/16 and `docs/settings-panel.md:164-166`, plus the test
  `tests/test_skin_picker.lua:332-344` (hazard H-1). A pre-existing doc drift (`docs/settings-panel.md:177-182`)
  is worth fixing in the same pass (section 4.3).

## 1. Workarounds of library gaps the release closes

### 1a. Own Ignore-fonts handling for HUD faces or outlines (R-1 / LK-01): none

- PrettyChat has no HUD. Nothing reads `hud.font` / `hud.outline`, no `fromSkin` companion, no FontGroup, no
  `NS.SkinFontsIgnored`-style helper. Proof (section 6, row 1) returns only the **degraded** stub's own
  `S.Resolve` (`core/SkinSetup.lua:317-320`), which no host code calls (proof row 8).
- The only `ignoreFonts` handling is the plumbing of the stored Scope half into `Skin:SetIgnore`:
  `core/SkinSetup.lua:70` (path), `:184` (write seam), `:199-202` (`storedIgnore`), `:372-378`
  (`NS.ApplySkinIgnore`), and the schema row `settings/Schema.lua:566-570` (`onChange = NS.ApplySkinIgnore(nil, v)`).
  This is the library's own seam, not a workaround; it stays as is.
- `docs/ARCHITECTURE.md:235-237` ("No HUD ... no `fromSkin` companion") stays true after R-1.

### 1b. `stockDefault` / `stock` callers (R-2 / LK-02): none

- Proof: section 6, row 2 (`grep -rnE 'stockDefault|stock[[:space:]]*='` over the addon's own Lua, rc=1).
- The word "stock" in the addon source is prose only: `core/SkinSetup.lua:38`, `:329`, `settings/Profiles.lua:45`,
  `settings/Panel.lua:575` (AceGUI widgets go back to the pool "stock", i.e. unpainted). None is an option.
- **The surface under Ka0s Default afterwards.** Nothing PrettyChat paints passes stock opts, and no non-Skin
  library file in the vendored copy passes `stockDefault` either (`grep -rn stockDefault libs/LibKa0s/*.lua`
  hits only `Skin.lua`, `SkinPaint.lua`, `SkinPaintControls.lua`, `SkinPaintExtras.lua`). So R-2 changes **no**
  PrettyChat surface:
  - With **Ignore settings panel on** (the default, `defaults/Profile.lua:72`) the settings pages stay the
    client's, as today (SKIN-1, `docs/smoke-tests.md:766-777`).
  - With it **off**, the options chrome's tab strip already fades its atlas slices through `opts.stock`
    (`libs/LibKa0s/OptionsTabs.lua:502-503`, a fade list honoured under every skin, see
    `../lib-stock-close-picker.md` section 3). If LK-02 keeps `opts.stock` as the fade list (the recommendation
    there) nothing moves; if it removes it literally, LK-02 must fade those slices another way, still a library
    concern. SKIN-5 (`docs/smoke-tests.md:797-803`, Ka0s Default, panel skinned) keeps its expectation either way.
  - The debug console and its copy window are painted through the owner's facade (`libs/LibKa0s/DebugLogWindow.lua:24-27`),
    not under `stockDefault`, so they wear the Ka0s look today and still will.

### 1c. Hand-rolled Scope guards around S.Text, WidgetsReorder and other library widgets (R-5 / LK-05, LK-06)

- **No guard around `S.Text`, `WidgetsReorder` or any other library widget**: PrettyChat calls none of them
  (section 6, row 7; the only hit is a comment naming the copy window's frame global, `core/DebugLogSetup.lua:178`).
- **One adjacent guard, `NS.PanelEscape`** (the guard the rollout report's follow-up 4 credits to "PC",
  `../../../2026-10-29-SKINNING_ROLLOUT/99_REPORT.md`, "Library follow-ups" item 4). It is a **color escape** for
  settings-page markup, not an `S.Text` guard:
  - Definition `core/SkinSetup.lua:128-139`; it answers the token's Ka0s Default copy from `NS.SKIN_FALLBACK`
    while `Skin:GetIgnore(addonName)` reports the panel ignored (`:135`), else `NS.SkinEscape` (`:138`).
    Header doc `core/SkinSetup.lua:16-18`. Landed in `99140a8` ("PC-02: Fix the settings notes recoloring while
    the Scope ignores the panel").
  - Callers (all `pc.note`): the GLOBALNAME caption `settings/Panel.lua:284`, the Categories footnote
    `settings/Panel.lua:733-735`, the landing alias row `settings/Panel.lua:786`.
  - **Verdict: stays.** LK-05 as written (`00_PLAN.md`, LK-05 row) covers `S.Text` and `WidgetsReorder`, not token
    or escape reads. The notes are markup inside AceGUI Labels / `H.TextRow`, not `S.Text` targets. If LK-05 also
    ships a panel-scope-aware `Color`/escape read (the same conditional PanelMaster's inventory records for its
    `NS.SkinPanelEscape`, `../PanelMaster.md:33`), PC-01 swaps `NS.PanelEscape`'s body for it and keeps the name
    (it is in the published-member parity list, `tests/test_skinsetup.lua:305`, and three doc tables, section 4).
- The list tooltip deliberately has **no** Scope guard: GameTooltip is Blizzard's frame, outside the Scope
  (`core/SkinSetup.lua:132`, `settings/Panel.lua:440-441`; pinned by `tests/test_skin_surfaces.lua:153-158`).
  Unchanged by R-5.
- The Categories/Profiles AceGUI trees are painted through `NS.SkinPaintAceTree` (`core/SkinSetup.lua:361-364`;
  callers in `settings/Panel.lua` and `settings/Profiles.lua`), and the panel Scope is honoured **inside the
  library** (`PaintAceTree` is a no-op for an owner that ignores its panel, `docs/settings-panel.md:184-185`).
  No host guard; unchanged.

### 1d. `ResetToSkin` guards against the `"@skin"` sentinel (R-6 / LK-07): none

- PrettyChat has no `fromSkin` bool companion and never calls `ResetToSkin` (section 6, row 4). The only `"@skin"`
  is the degraded stub's own `FROM_SKIN` constant (`core/SkinSetup.lua:301`), mirroring the live facade's field
  for the parity test. Stays.

### 1e. Reach into `Skin:__DrawsKey` or other Skin internals (R-9 / LK-10): none

- Proof: section 6, row 3. The addon reads no `Skin.__*` member. (Tests read `Skin.__ace`,
  `tests/test_skin_picker.lua:221-224`, and `Skin.painted`, `:341`, to observe painting; those are test-side
  observers, unaffected by LK-10. Re-check after the re-vendor that both still exist.)

### 1f. Close-button tint handling (R-3 / LK-03): none

- PrettyChat calls no `S.CloseButton` (section 6, row 5). `NS.MakeCloseButton` (`core/CoreSetup.lua:162-164`,
  degraded stub `:99`) is Core's close mark wrapper, has **no host caller** (`docs/ARCHITECTURE.md:90`), and the
  console's × is the library's own: `libs/LibKa0s/Core.lua:269-308`, which tints it at `:286-288` and then calls
  `S.CloseButton(b, { own = true })` at `:304`. LK-03 fixes the save/restore inside the library; nothing here
  changes. (`core/DebugLogSetup.lua:235-242` records the decision not to pass a `makeCloseButton`.)

### 1g. Literal tooltip / quality colors standing in for `gtip.*` / `q.*` (R-7 / LK-08, R-8 / LK-09): none

- The one tooltip PrettyChat writes, the Categories list entry's (`settings/Panel.lua:436-452`), already reads
  `gtip.value` for its title (`:443`) and the owner token `pc.tipNote` (follows `gtip.subtle`,
  `core/SkinSetup.lua:85`) for its lines (`:442`, `:444-449`). No literal. Pinned by
  `tests/test_skin_surfaces.lua:193-201` ("settings/ writes no typed gray and no typed tooltip color").
- No `q.*` token, `ITEM_QUALITY_COLORS` or `GetItemQualityColor` (section 6, row 6). Item quality colors in chat come
  from the client's own item links inside the formats.
- Literal colors that remain are **out of skin scope on purpose** (`docs/ARCHITECTURE.md:239-242`, decisions X7/D3):
  the `[PC]`/slash palette `core/Constants.lua:37-55`, the debug ack `core/DebugLogSetup.lua:131`, the test report
  `modules/Override.lua:17-19`, `:610`, `:668`, `:684`, the `/pc list` headers `settings/Slash.lua:372`, `:391`,
  and the shipped formats `defaults/Defaults.lua:20-135`. None stands in for `gtip.*`/`q.*`.
- R-8 does not touch PrettyChat's host-copy token check: `NS.SKIN_FALLBACK` holds only `pc.note`, `pc.tipNote`
  and `gtip.value` (`core/SkinSetup.lua:93-96`), and `tests/test_skinsetup.lua:316-330` holds them to the live
  library. Stays green unless v1.81.0 moves `gtip.value` (not planned).

## 2. Where the addon resolves a HUD face or outline itself

**Nowhere.** No HUD, no `hud.*`, no `Resolve`/`Token`/`Font`/`GetFont` call by host code (section 6, rows 1 and 8).
R-1 needs no addon change. R-4 (per-skin HUD fonts) draws on nothing PrettyChat shows.

The only fonts PrettyChat names: the console's monospace `NS.Const.FONT_MONO` handed to DebugLog
(`core/DebugLogSetup.lua:195`), which is the log face and stays JetBrains Mono under every skin and with Ignore fonts
(SKIN-1, SKIN-3, SKIN-8, `docs/smoke-tests.md:772`, `:786`, `:819-820`).

## 3. Tests that pin current behaviour

| Test | Path:line | Pins | After v1.81.0 |
|---|---|---|---|
| Skin seam: the degraded facade answers every name the live facade carries | `tests/test_skinsetup.lua:295-299` | key-for-key parity of the stub list `core/SkinSetup.lua:305-313` with the live facade, nothing ignored | **Goes red if v1.81.0 adds a facade name** (e.g. a public `DrawsKey` on the facade, LK-10, or a new primitive for LK-06). PC-RV adds each new name to the stub list as a no-op (or a real answer if it is a query). |
| Skin seam: the seam publishes the same NS members on both paths | `tests/test_skinsetup.lua:302-314` | `PanelEscape` among the NS members | Unchanged (the name stays even if its body changes). |
| Skin seam: each host-copy skin token is the live library's Ka0s Default value | `tests/test_skinsetup.lua:316-330` | `pc.note`, `pc.tipNote`, `gtip.value` | Unchanged (R-8 moves only `q.*`). |
| Skin surfaces: while the Scope ignores the settings panel the page notes keep #aaaaaa | `tests/test_skin_surfaces.lua:89-106` | `NS.PanelEscape`'s ignore arm | Unchanged, unless LK-05 adds a panel-scoped color read and PC-01 adopts it (then the "red under" note at `:90-91` names the new API). |
| Skin surfaces: unticking Ignore settings panel recolors the open page's notes live | `tests/test_skin_surfaces.lua:108-115` | `NS.PanelEscape`'s skinned arm + the library re-render | Unchanged. |
| Skin surfaces: notes / alias row / tooltip under Ka0s Default and another skin | `tests/test_skin_surfaces.lua:51-87`, `:135-151` | `pc.note`, `pc.tipNote`, `gtip.value` | Unchanged. |
| Skin surfaces: the tooltip lines follow the skin whatever the Scope says | `tests/test_skin_surfaces.lua:153-158` | GameTooltip outside the Scope | Unchanged (R-5 is about library widgets; GameTooltip is Blizzard's). |
| Skin surfaces: settings/ writes no typed gray and no typed tooltip color | `tests/test_skin_surfaces.lua:193-201` | no literal tooltip color | Unchanged. |
| Skin picker: the spec names this owner, its seams and the Skin tab, with no eye | `tests/test_skin_picker.lua:66-80` | `spec.tab == "Appearance"` (`:76`), the tab **key** | Unchanged: R-10 renames the tab in the standard only; the library's key stays `"Appearance"` (`libs/LibKa0s/OptionsAppearance.lua:3`, `:47`, `:590`; `libs/LibKa0s/OptionsSkinPicker.lua:505`). Only if LK-11 or WS-01 changes the key does this move. |
| Skin picker: show/hide/seen cases | `tests/test_skin_picker.lua:84-215` | the picker's lifecycle | Unchanged by R-11 (title/layout only). **No PrettyChat test pins the picker title** (`grep -n "Choose a skin" tests/*.lua` returns nothing). Optional: PC-01 may add one asserting the title is "Choose a skin" and the label "Ka0s Pretty Chat" (`core/SkinSetup.lua:73`) is shown on its own line; then `docs/test-cases.md:689-699` and `:789` (count 14) move. |
| Skin widgets: while the Scope ignores the settings panel (the default) nothing is painted | `tests/test_skin_picker.lua:280-285` | the library's PaintAceTree honouring the panel Scope | Unchanged. |
| **Skin tools: the debug console is owned by this addon** | `tests/test_skin_picker.lua:332-344` | under the **default profile** (Ignore settings panel ON) the console window is painted through the skin for this owner (`:341-343`) | **Hazard H-1:** goes red if LK-06 puts the debug console under the "Ignore settings panel" Scope. Then PC-01 sets the Scope to paint the panel (or splits the assertion into both arms). Stays green if LK-06 scopes tool windows by Ignore fonts only, or leaves them always skinned. |
| Skin seam: a skin write re-applies no chat string | `tests/test_skinsetup.lua:149-167` | `skin.ignoreFonts` write path | Unchanged. |
| Skin seam: stored exceptions applied with the skin | `tests/test_skinsetup.lua:262-273` | `SetIgnore(owner, false, true)` applied from the profile | Unchanged. |

No PrettyChat test pins `stockDefault`, the HUD face, `ResetToSkin`, `__DrawsKey`, the close-mark tint or `q.*`.

## 4. Smoke checks and doc passages whose expectation changes

### 4.1 `docs/smoke-tests.md` (section SKIN, `:753-874`)

| Check | Path:line | Changes because | New expectation |
|---|---|---|---|
| Section intro | `:755-760` | names "LibKa0s v1.80.0" | v1.81.0, and the run bundle `docs/2026-10-30-SKIN_LIBRARY_FOLLOWUPS/` beside the rollout's. |
| **SKIN-10** first-run picker | `:830-837` (title at `:831-832`) | R-11 | Titled *Choose a skin*; **Ka0s Pretty Chat** on its own line above the skin dropdown, whole (never cut off). New fail: the addon name truncated or missing, or the old "Choose a skin for ..." title. |
| SKIN-12 one picker at a time | `:843-847` | R-11 (indirect) | Optional: "each picker names its addon above the dropdown" so the owner can tell which is up. |
| SKIN-1 Ka0s Default as before | `:766-777` | **only under H-1** (LK-06 puts the console under the panel Scope) | Default profile has Ignore settings panel on, so the console chrome would stay the client's / pre-skin look rather than "Ka0s Default ... in Oxanium" (`:772-776`). |
| SKIN-3 each skin live (console) | `:784-788` | **only under H-1** | Needs "untick Ignore settings panel first" for the console and copy window to repaint. |
| SKIN-8 fonts, Ignore fonts | `:817-823` | R-1 is HUD-only, PrettyChat has no HUD, so no change from R-1. **Under H-1/LK-06** the console's chrome follows Ignore fonts through the new widget Scope instead of today's path; the expectation text is unchanged (already "back to the game's faces live"). | Unchanged unless LK-06 alters which faces the console's chrome falls back to. |
| SKIN-13 skin pick while disabled → console follows | `:853-854` | **only under H-1** | "with Ignore settings panel off". |
| SKIN-16 CLI → console repaints | `:865` | **only under H-1** | same caveat. |
| SKIN-5 Ka0s Default, panel skinned | `:797-803` | R-2: none (no stockDefault on any PC surface, section 1b) | Unchanged, provided LK-02 keeps `opts.stock` as the fade list (or replaces the OptionsTabs fade). |
| SKIN-2 the Skin tab | `:778-783` | none (tab already labeled **Skin**; R-10 only renames the standard) | Unchanged. |
| SKIN-6 notes and tooltip lines | `:804-811` | none (PanelEscape stays; tooltip outside the Scope) | Unchanged. |

No smoke check here covers a HUD face, a HUD under non-Ka0s skins (R-4), the stock look (R-2) or Ignore fonts on a
HUD (R-1): PrettyChat has no HUD (`:762-764`). A new check is **not** needed for R-3/R-7/R-8/R-9 (no PC surface).
Optional new check for R-3: the console's × after a skin switch back to Ka0s Default keeps its rest/hover colors
(library behaviour; the Skin Tester carries the primary check).

### 4.2 Doc passages

| Doc | Path:line | Change |
|---|---|---|
| CLAUDE.md provenance | `CLAUDE.md:44` | `v1.80.0` → `v1.81.0` (PC-RV). `LibKa0s icons:` line `:45` (`clear, close, copy, settings`) stays unless v1.81.0 changes the picker's icon needs. |
| testing.md | `docs/testing.md:125` | "vendored LibKa0s v1.80.0 (kit revision 44)" → v1.81.0 and its kit revision. |
| ARCHITECTURE libraries | `docs/ARCHITECTURE.md:412` | `v1.80.0` → `v1.81.0`. `:414` "since v1.80.0" for Skin adoption stays (historical). |
| module-map load order | `docs/module-map.md:185` | "(LibKa0s v1.80.0)" → v1.81.0, and the XML order if v1.81.0 adds or reorders files. |
| settings-panel.md picker | `docs/settings-panel.md:187-197` | Does not quote the title today; optional: add "titled *Choose a skin*, with the addon's name above the dropdown" (R-11). |
| settings-panel.md "what follows the skin" | `docs/settings-panel.md:164-166` | **Only under H-1**: "the debug console and its copy window always" becomes "while Ignore settings panel is off" (or whatever Scope LK-06 assigns). Same for `docs/ARCHITECTURE.md:201-204` (library surfaces list) and `README.md:36` ("the look of PrettyChat's debug console and, if you want, its settings pages"). |
| README credits | `README.md:106-115` | **Only if LK-04 registers a new OFL face** for some skin's HUD font: the credits list "seven more ... faces, one family per skin" becomes inaccurate (PrettyChat ships the whole payload, so it ships the font). Add the face and its authors; adjust "seven"/"one family per skin". If LK-04 reuses only the eight faces already shipped, no change. |
| ARCHITECTURE § Skins | `docs/ARCHITECTURE.md:218-224`, `:235-237` | Unchanged (PanelEscape stays; still no HUD). Only if LK-05 adds a panel-scoped color read and PC-01 adopts it: `:219-221` names the new API. Same for `docs/module-map.md:52`, `:235` and `docs/ARCHITECTURE.md:64`, `:91`. |
| docs/schema.md | `docs/schema.md:20` | group `Appearance` is the tab key: unchanged. |
| test-cases.md | `docs/test-cases.md:689-699`, `:789` | Only if a test is added/renamed (generated list and counts). |

### 4.3 Pre-existing doc drift found while reading (not caused by the release)

- `docs/settings-panel.md:177-182` says the gray notes "are colors rather than panel paint, so they follow the skin
  whatever the Scope says". Since `99140a8` (PC-02) the page notes read `NS.PanelEscape` and keep `#aaaaaa` while
  Ignore settings panel is on (`core/SkinSetup.lua:128-139`; `docs/ARCHITECTURE.md:218-221`;
  `tests/test_skin_surfaces.lua:89-106`). Only the tooltip lines follow the skin whatever the Scope says.
  Suggest PC-02 corrects the sentence while it is in the file.

## 5. Current state

- **Branch:** `master`, tracking `origin/master`, **clean** (`git status --short --branch` → `## master...origin/master`,
  nothing else). Head `cfd8c58` (Merge feat/2026-10-29-skinning-rollout). No stash, one worktree (the main one),
  no other local branch.
- **Vendored LibKa0s:** `CLAUDE.md:44` — "Bundles [LibKa0s](https://github.com/tusharsaxena/LibKa0s) v1.80.0 (MIT)."
  Icons line `CLAUDE.md:45` — "LibKa0s icons: clear, close, copy, settings."
- **Gate on master (run 2026-10-30):**
  - `~/.claude/dev-copilot/bin/ka0s-bounded lua tests/run.lua` (exit 0), totals verbatim:
    `631 passed, 0 failed, 1 skipped, 632 total`
    (the skip is the kit's declared one: "diagnostics contract: an addon that opts out lands the report and leaves
    logging off — this addon keeps the default ...").
  - `~/.claude/dev-copilot/bin/ka0s-bounded luacheck .`, totals verbatim:
    `Total: 0 warnings / 0 errors in 62 files`
  - The 1500-line cap runs inside the suite (`tests/run.lua:84-86`) and passed. Largest skin file:
    `core/SkinSetup.lua` 399 lines.
  - **Green.**

## 6. Nothing to change: proof greps (exceptions.tsv candidates)

Run from the PrettyChat root, over the addon's own Lua:
`grep -rnE '<pattern>' --include='*.lua' --exclude-dir=libs --exclude-dir=_kit --exclude-dir=tests .`

| # | Ruling / item | Pattern | Result |
|---|---|---|---|
| 1 | R-1 / LK-01 (HUD Ignore fonts) | `hud\.\|FontsIgnored\|fromSkin\|FromSkin\|FontGroup` | only `core/SkinSetup.lua:317-318`, the degraded stub's `S.Resolve` parameter (no host caller, row 8) |
| 2 | R-2 / LK-02 (stockDefault/stock) | `stockDefault\|stock[[:space:]]*=` | nothing (rc=1) |
| 3 | R-9 / LK-10 (`__DrawsKey`) | `DrawsKey\|__Draws` | nothing (rc=1) |
| 4 | R-6 / LK-07 (ResetToSkin) | `ResetToSkin\|"@skin"` | only `core/SkinSetup.lua:301`, the degraded stub's `FROM_SKIN` constant |
| 5 | R-3 / LK-03 (close tint) | `S\.CloseButton\|Skin\.CloseButton\|\.CloseButton\(` | nothing (rc=1) |
| 6 | R-8 / LK-09 (`q.*`) | `"q\.\|q\.[a-z]+"\|ITEM_QUALITY_COLORS\|GetItemQualityColor` | nothing (rc=1) |
| 7 | R-5 / LK-05, LK-06 (widget guards) | `ReorderList\|DragHandle\|S\.Text\|Skin\.Text\|NS\.Skin\.Text\|Toast\|LineChart\|Autocomplete\|CopyWindow` | only `core/DebugLogSetup.lua:178` (a comment) and `GlobalStrings/*` (Blizzard string data containing "TOAST") |
| 8 | R-1 (host resolves a face) | `Skin\.(Resolve\|Token\|Font\|GetFont)\b\|\.Resolve\(` over `core modules settings` | nothing |
| 9 | R-7 / LK-08 (tooltip literals) | `SetText%([^)]*, 1, 1, 1%)` is already pinned absent by `tests/test_skin_surfaces.lua:193-201`; `settings/Panel.lua:443` reads `gtip.value` | — |

Suggested exceptions.tsv rows: **PC-01** (no workaround to delete) with rows 1-8 as proof, **conditional** on LK-05
not shipping a panel-scoped color read; if it does, PC-01 becomes "swap `NS.PanelEscape`'s body" and is a real item.

## 7. Hazards for the implementer

- **H-1 (LK-06 and the debug console).** PrettyChat's only skinned surfaces outside the settings panel are the
  library's debug console and copy window, which today follow the skin **regardless of Ignore settings panel**
  (`docs/settings-panel.md:164-166`; pinned by `tests/test_skin_picker.lua:332-344` under the default profile).
  If LK-06 makes these tool windows obey the "Ignore settings panel" switch, a new PrettyChat profile shows **no
  skin anywhere** by default, and SKIN-1/3/10/13/16, three doc passages and that test change (sections 3, 4.1, 4.2).
  The lead should decide which Scope switch governs tool windows before PC-01/PC-02 start; the owner's R-5 answer
  says "like the AceGUI widgets", which reads as the panel switch.
- **H-2 (facade parity).** Any name v1.81.0 adds to the per-owner facade must be added to the stub list at
  `core/SkinSetup.lua:305-313` in the PC-RV commit, or `tests/test_skinsetup.lua:295-299` goes red.
- **H-3 (picker label).** The label the picker shows is `Skin:OwnerLabel` = `"Ka0s Pretty Chat"`
  (`core/SkinSetup.lua:73`, `:340`; pinned `tests/test_skinsetup.lua:53`). LK-11 needs nothing from the addon, but
  SKIN-10 wording must quote it.
