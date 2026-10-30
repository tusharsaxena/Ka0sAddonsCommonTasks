# M0 inventory: AuraMaster

Read-only inventory taken 2026-10-30 against AuraMaster `master` at `e565220` (vendored LibKa0s v1.80.0).
Every path is relative to `/mnt/d/Profile/Users/Tushar/Documents/GIT/AuraMaster` unless prefixed. `libs/` and
`tests/_kit/` were read only for reference. Rulings and item ids are from `../../00_PLAN.md`.

## 0. Summary

AuraMaster has **two workarounds** that v1.81.0 makes unnecessary, plus **one guard** the implementer should
decide on, and nothing for R-2, R-3, R-8, R-9 or R-10 beyond docs:

| Ruling / item | What AuraMaster has | Action (AM-01 / AM-02) |
|---|---|---|
| R-1 / LK-01 | `NS.SkinFontsIgnored` and its use in `Style.SkinKey` (HUD face under Ignore fonts) | Delete; HUD face resolves through `S.Resolve` alone |
| R-1 outline | none: AM never reads `hud.outline` | Exception row |
| R-2 / LK-02 | no `stockDefault` / `stock` caller | Exception row; no Ka0s Default look change |
| R-3 / LK-03 | no close-button tint handling | Exception row |
| R-4 / LK-04 | no code; smoke SKIN-4 lists each skin's HUD face wrongly today | Docs only (SKIN-4) |
| R-5 / LK-05, LK-06 | no hand-rolled Scope guard; consumes DragHandle, DebugLog windows, Perf panel, IdList/IdInput, Launcher | Exception row for code; SKIN-5/SKIN-8 expectations depend on LK-06's scope semantics (see 4.4) |
| R-6 / LK-07 | v13 migration seeds absent companions `false` before `ResetToSkin` | Keep (frozen step body) or drop the seed; see 1.3 |
| R-7 / LK-08 | `tokenLine` gives the DragHandle tooltip lines their `gtip.*` colors explicitly | Title colors removable; body colors must stay (see 1.4) |
| R-8 / LK-09 | no `q.*` use, no quality literal | Exception row |
| R-9 / LK-10 | no `__DrawsKey` reach-in | Exception row; watch the facade-parity test if LK-10 adds a facade member |
| R-10 / WS-01 | group key "Appearance" is internal; the tab already reads "Skin" | Exception row (unless WS-01 renames keys) |
| R-11 / LK-11 | no code (title is the library's) | Docs only (SKIN-18) |

## 1. Workarounds of library gaps the release closes

### 1.1 R-1 (LK-01): Ignore fonts for the HUD face — `NS.SkinFontsIgnored`

The workaround, in full:

- `core/SkinSetup.lua:23-25` header entry: "NS.SkinFontsIgnored() true while the applied "Ignore fonts" is on
  ... Style.SkinKey reads it for the HUD's face: the library's Resolve and Token never check it, only P.font
  does." Delete the entry.
- `core/SkinSetup.lua:393` degraded arm: `function NS.SkinFontsIgnored() return false end`. Delete.
- `core/SkinSetup.lua:439-445` live arm:
  ```lua
  --- The applied "Ignore fonts". The library's Resolve and Token never read it (only P.font, the
  --- primitives' path, does), so the HUD's face asks here (Style.SkinKey), as AbsorbTracker's does.
  function NS.SkinFontsIgnored()
      if type(Skin.GetIgnore) ~= "function" then return false end
      local _, fonts = Skin:GetIgnore(addonName)
      return fonts == true
  end
  ```
  Delete.
- `modules/Style.lua:60` the only caller:
  `if token == "hud.font" and NS.SkinFontsIgnored and NS.SkinFontsIgnored() then return key end`. Delete.
- `modules/Style.lua:51-52` doc comment ("While the Skin tab's "Ignore fonts" is on (NS.SkinFontsIgnored) a
  `hud.font` pick draws the stored face whatever its companion says: the library's Resolve never reads that
  exception itself."). Rewrite: Ignore fonts is honoured by the library's `S.Resolve` (LK-01), which answers
  the stored key for `hud.font` while it is on.

Callers proven exhaustive: `grep -rn 'SkinFontsIgnored' --include='*.lua' core modules settings` → only
`core/SkinSetup.lua:23,393,440,441` and `modules/Style.lua:51,60`.

**Behaviour after deletion is unchanged** provided LK-01's `S.Resolve("hud.font", stored, true)` answers the
stored value (or nil) while Ignore fonts is on: `Style.SkinKey` (`modules/Style.lua:58-64`) returns `key` when
Resolve answers nil (line 63), so either library answer keeps the stored face. The Font override is covered by
the same path (the override lives inside `Resolve`'s token table, `libs/LibKa0s/Skin.lua:727`).

### 1.2 R-1: where AuraMaster resolves a HUD face itself (section 2 of the brief)

AuraMaster resolves `hud.font` itself, not through a library primitive, because the aura buttons are Blizzard's
pooled engine buttons (`docs/ARCHITECTURE.md:309-310`; `modules/Style.lua:54-57`). The one seam:

- `modules/Style.lua:58-64` `Style.SkinKey(token, key, fromSkin)` → `S.Resolve(token, key, true)`.
- `modules/Style.lua:1052-1057` `Style.FontKey(t, tdef)` calls `Style.SkinKey("hud.font", t.font, ...)` for
  every font block. Its consumers (no change needed, they inherit the fix): `modules/Style.lua:146, 275, 307,
  345`; `modules/FontPrimer.lua:143`; `modules/Style_Text.lua:864`; `modules/Style_TextGlow.lua:92`.
- The bar textures go through the same seam (`modules/Style_Bars.lua:206, 221`, token `bar.texture`); Ignore
  fonts must keep leaving them alone (pinned at `tests/test_skin_hud.lua:175-176`).

After R-1, Ignore fonts makes the stored `font` win through the library: deleting `modules/Style.lua:60` is the
whole change. Every font block's `fontFromSkin` companion (`defaults/Profile.lua:131`, settings rows
`settings/Bars.lua:127`, `settings/Icons.lua:85`, `settings/Text.lua:387`, `settings/Layout.lua:588`) stays.

**`hud.outline`: AuraMaster never reads it.** Flags come from the stored `fontFlags` only
(`modules/Style.lua:131-132, 1054`). `grep -rn 'hud\.outline' --include='*.lua' core modules settings defaults`
→ no hit. Nothing to change for the outline half of R-1 (exception row, section 6).

**`hud.fontSize`: never read** either (`grep -rn 'hud\.fontSize' --include='*.lua' core modules settings` → no
hit).

**The composer's picker preview (LK-01 second half).** AuraMaster's face pickers are the library composer's
(`fromSkin = true` at the settings sites above); `picker.skinValue` is library code
(`libs/LibKa0s/OptionsCompose.lua:515-526`). No AuraMaster code changes; the expectation change is in SKIN-10
(section 4).

### 1.3 R-6 (LK-07): the `"@skin"` guard in the v13 migration

- `core/Database_Migrations.lua:948-951` comment: "THE COMPANION IS SEEDED BEFORE THE CALL. A container stored
  before v13 holds no companion, and ResetToSkin, handed a string pick with no `<leaf>FromSkin` beside it,
  writes its "@skin" sentinel INTO THE PICK ... So each companion that is not a bool is laid down as false
  first".
- `core/Database_Migrations.lua:990` the guard: `if type(parent[companion]) ~= "boolean" then parent[companion] = false end`.
- `core/Database.lua:440-445` the v13 step row passes `Skin.ResetToSkin` (or nil) to `Database.MigrateV13`.
- The library behaviour it guards: `libs/LibKa0s/Skin.lua:900-905` (`parent[leaf.."FromSkin"] ~= nil` takes the
  companion branch; a string pick with no companion gets `lib.FROM_SKIN`).

Recommendation for AM-01: this is the body of a **frozen, already-shipped schema step** (`docs/schema.md:831-832`,
"a step already pushed is never extended again"), and the seed is harmless under any LK-07 contract. Keep the
code; at most reword the comment to say the seed predates LK-07. If the implementer removes the seed, it is only
safe if LK-07 makes `ResetToSkin` create a missing `<leaf>FromSkin` companion for a string pick (LK-07 as worded
— "leaves an absent bool companion a bool" — may cover only the bool case). Record whichever is chosen in
`exceptions.tsv` / DECISIONS.

### 1.4 R-7 (LK-08): DragHandle tooltip colors via `tokenLine`

- `modules/Anchors.lua:499-503` `tokenLine(text, token)`: a `{ text, r, g, b }` entry whose r, g, b read
  `NS.Skin.Color(token)` on each hover.
- `modules/Anchors.lua:539-543` doc comment explaining the colors (title `gtip.title`, body `gtip.value`, the
  attached line `gtip.title`).
- `modules/Anchors.lua:581-589` `tooltipSpec`: title `gtip.title`; body[1] (how-to) `gtip.value`; body[2]
  (attached) `gtip.title`.
- `modules/Anchors.lua:613-620` `closeTooltipSpec`: title `gtip.title`; body[1] `gtip.value`.
- The library defaults the colors replace: `libs/LibKa0s/WidgetsDragHandle.lua:332-341` (`title` 1, 0.82, 0;
  `body` 1, 1, 1; `footer` 0.6 gray).

What can go once LK-08 lands: **the two title colors only** (lines 582-585 and 614-617 become plain
functions), since the library title will take `gtip.title`. **The body lines must keep their colors:**
- body[2] (the attached line) is deliberately gold inside the white body band (the colored form exists for it,
  `libs/LibKa0s/WidgetsDragHandle.lua:276-279`);
- body[1] uses `gtip.value` (Ka0s Default white, `libs/LibKa0s/SkinDefs.lua:239`), while `gtip.body` is
  `BODY = { 0.9, 0.9, 0.9 }` (`libs/LibKa0s/SkinDefs.lua:192, 226`). If LK-08 maps the body band to `gtip.body`,
  dropping AuraMaster's color would move the how-to line from white to 0.9 gray on Ka0s Default. Keep it unless
  LK-08 maps the body band to `gtip.value`.

Keeping `tokenLine` entirely is also correct (explicit colors win over band defaults,
`libs/LibKa0s/WidgetsDragHandle.lua:297`); trimming the titles is optional tidiness, not a requirement.

### 1.5 Nothing else to remove (each proved in section 6)

- `stockDefault` / `opts.stock`: no caller in AuraMaster code (R-2). Under Ka0s Default nothing AuraMaster draws
  is kept stock today, so **R-2 changes no AuraMaster surface**: the HUD, the unlock furniture, the settings
  pages (with Ignore settings panel off), the debug console, its copy window and the perf panel already paint
  the Ka0s look under Ka0s Default. The vendored library has no internal `stockDefault = true` caller either
  (`grep -rn 'stockDefault *= *true' libs/LibKa0s` → none); its one `stock = {...}` use is OptionsTabs' fade
  list for tab art (`libs/LibKa0s/OptionsTabs.lua:495, 503`), a library concern for LK-02.
- Hand-rolled Scope guards around `S.Text`, `WidgetsReorder` or another widget: none. AuraMaster calls no
  `S.Text` (`grep -rnE 'Skin\.Text\(|S\.Text\(' core modules settings` → none) and uses no `WidgetsReorder`.
  Its own AceGUI painting defers the Scope to the library (`core/SkinSetup.lua:416-430`, `Skin:PaintAce`
  honours ignorePanel; pinned `tests/test_skin_picker.lua:252-256`).
- `Skin:__DrawsKey` or other internals: none (`grep -rn 'DrawsKey' core modules settings tests/*.lua` → none).
- Close-button tint: none. Every close control is `NS.MakeCloseButton` → `lib.MakeCloseButton`
  (`core/CoreSetup.lua:172-174`, pinned by `tests/test_setups.lua:41-50`); no `SetVertexColor` on a close mark
  (`grep -rn SetVertexColor core modules settings` lists only HUD regions and Compat).
- Literal tooltip colors: only the DragHandle lines (1.4), already token-driven. Quality colors: none
  (`grep -rnE 'ITEM_QUALITY|GetItemQualityColor|"q\.' core modules settings defaults` → none).

## 2. Custom LibKa0s widgets AuraMaster consumes (for LK-05 / LK-06)

| Widget | Where | Owner passed |
|---|---|---|
| WidgetsDragHandle (strip, ?, X, tooltips) | `modules/Anchors.lua:464-465, 688-700` | `owner = NS.name` (`modules/Anchors.lua:693`; pinned `tests/test_skinsetup.lua:296-305`) |
| DebugLog window + copy window | `core/DebugLogSetup.lua` | library-resolved |
| Perf panel | `core/PerfSetup.lua` | library-resolved |
| Options IdList / IdInput | `settings/GeneralSpells.lua:857`, `settings/Filters.lua:847` | page owner |
| Launcher (minimap button, status tooltip) | `core/LauncherSetup.lua:44, 87` | — |
| First-run skin picker (OptionsSkinPicker) | `core/SkinSetup.lua:273-279, 325` | `owner = addonName` |

Not used: WidgetsReorder, WidgetsAutocomplete, WidgetsLineChart, Toast, SimPanel (`grep -rnE
'Reorder|Autocomplete|LineChart|Toast|SimPanel' --include='*.lua' core modules settings` → no code hit).

## 3. Tests that pin current behaviour

| Test | Pins | Change with the release |
|---|---|---|
| `tests/test_skin_hud.lua:158-182` "Ignore fonts keeps every font block on its stored face, over the skin and a font override" | The R-1 workaround: comment 159-161 names `NS.SkinFontsIgnored`; asserts `NS.SkinFontsIgnored()` at 168 and 171 | **Must change.** Drop the two `NS.SkinFontsIgnored` asserts and rewrite 159-161 ("red under: a library Resolve that ignores ignoreFonts, or a Style.SkinKey that bypasses Resolve"). Keep 172-176 (stored face under Ignore fonts, over an override; textures unaffected) and 181: they now characterize LK-01 through AuraMaster's seam and must stay green. |
| `tests/test_skin_hud.lua:142-156` font block on/off | `Style.FontKey` resolution with Ignore off | None |
| `tests/test_skin_hud.lua:104-122` picker shows the skin's value while on | `picker.skinValue == NS.Skin.Token(token)` with Ignore fonts off | None expected; optionally add a case: with Ignore fonts on, a `hud.font` picker previews the stored face (LK-01) |
| `tests/test_skin_hud.lua:213-223` facade answering nil → stored key | `Style.SkinKey` nil fallback (line 63), which keeps the delete safe | None |
| `tests/test_skin_hud.lua:290-292` and `317-344` v13 seeding before ResetToSkin ("red under: an unseeded companion reaching ResetToSkin") | The R-6 guard (1.3) | None if the seed is kept; if removed, 337-338's `unseeded` assertion goes and the case is rewritten to rely on LK-07 |
| `tests/test_skin_surfaces.lua:101-125` tooltip lines take gtip colors | `tokenLine` colors on every title and body line (1.4) | If titles lose their color: assert `spec.tooltip.title` / `spec.closeTooltip.title` carry no color and that the library draws `gtip.title` (needs the real widget) or drop 119 and 122; keep 120, 121, 123 |
| `tests/test_surface_parity.lua:108-116` degraded facade answers every live facade name, key for key | `core/SkinSetup.lua:355-363` vocabulary list | **Watch:** any facade member v1.81.0 adds (e.g. a public `DrawsKey` if LK-10 puts it on the facade, or a new primitive from LK-05/06) turns this red until the degraded list adds it |
| `tests/test_surface_parity.lua:118-136` host-copy tokens equal the library's Ka0s Default | `NS.SKIN_FALLBACK` (`core/SkinSetup.lua:129-143`: `gtip.title`, `gtip.value`, ...) | None expected (no `q.*` in the copy); red if LK-08/09 move a copied value |
| `tests/test_skinsetup.lua:126-147` and `tests/settings_pin.lua:292-293, 336-337` | `skin.ignorePanel` default true, `skin.ignoreFonts` default false | None (R-2 keeps the Scope switch, default on) |
| `tests/test_skin_picker.lua:54-66` spec | owner, page "general", tab "Appearance" | None (title is the library's; no AM test pins "Choose a skin for") |
| `tests/test_setups.lua:68-80` picker icons (eye, settings) | icon declaration | None unless LK-11 adds art |
| `tests/test_skinsetup.lua:296-305` DragHandle built for this owner | `owner` passed | None |

`docs/test-cases.md:2020-2032` lists `test_skin_hud.lua` (11) and `:2009-2018` `test_skin_surfaces.lua` (8);
update the wording/counts if a case is renamed, added or removed (`docs/test-cases.md:2627` holds the count).

## 4. Smoke checks and doc passages whose expectation changes

### 4.1 `docs/smoke-tests.md`

- **SKIN-4** (`docs/smoke-tests.md:2312-2323`): says every HUD string takes "the skin's own family (Obsidian
  Inter, Azeroth Vollkorn, Glass Nunito, High Contrast Atkinson Hyperlegible, Ember Bitter, WoW Midnight
  Philosopher, WoW Forever Fira Sans, WoW Default Friz Quadrata, Ka0s Default Oxanium)". Today that is wrong for
  the HUD: `hud.font` falls back to Friz Quadrata under the eight non-Ka0s skins
  (`libs/LibKa0s/SkinDefs.lua:524-525, 541-543`; only Ka0s Default sets it, `:307`). After R-4/LK-04 rewrite
  the list with the faces LK-04 picks (from the run's `DECISIONS.md`), and reset its Result line.
- **SKIN-10** (`docs/smoke-tests.md:2366-2372`): the HUD half ("every container's text ... draws its own Font
  pick even with Use the skin's font ticked and a Font override set") already describes R-1's outcome via the
  workaround; it stays true. Add LK-01's picker expectation: with Ignore fonts on, a ticked **Use the skin's
  font** face picker (dimmed) shows the stored face, not the skin's. Reset Result (the plan names AM SKIN-10).
- **SKIN-18** (`docs/smoke-tests.md:2407-2413`): "a small window titled for Ka0s Aura Master opens" → the
  window is titled **Choose a skin**, with **Ka0s Aura Master** on its own line above the dropdown, not cut
  off (R-11). Reset Result. (BRAND label is `core/SkinSetup.lua:90`, handed at `:405`.)
- **SKIN-5** (`:2325-2331`) and **SKIN-8** (`:2349-2352`): conditional on LK-06's scope semantics. A new profile
  starts with Ignore settings panel **on** (`defaults/Profile.lua:54`; smoke preamble `:2271-2272`). If LK-06
  puts the debug console, its copy window and the perf panel under "Ignore settings panel", SKIN-8 must first
  turn it off (or expect stock windows while it is on); if it puts the DragHandle strip under it, SKIN-5 the
  same. If they obey only Ignore fonts, add to SKIN-8/SKIN-10 that their text keeps the client face with
  Ignore fonts on. Settle after LK-06 and amend accordingly.
- **SKIN-2** (`:2290-2299`, Ka0s Default unchanged): no change from R-2 (no AM surface was kept stock).
- **SKIN-17** (`:2402-2405`, tooltip lines readable in the skin's colors): unchanged; the strip tooltip still
  follows `gtip.*`.
- The index row (`docs/smoke-tests.md:32`) and the owed-checks paragraph (`:2485-2492`): add the re-opened
  checks (SKIN-4, SKIN-10, SKIN-18, and SKIN-5/8 if amended) under this run's name.

### 4.2 `docs/ARCHITECTURE.md`

- `docs/ARCHITECTURE.md:313-316`: "While the Skin tab's Ignore fonts is on (`NS.SkinFontsIgnored`,
  `Skin:GetIgnore`) every font block draws its stored face, companion or override notwithstanding, because the
  library's `Resolve` never reads that exception itself (only its primitives' font path does); AbsorbTracker
  does the same." Rewrite: the library's `S.Resolve` honours Ignore fonts for `hud.font` (LibKa0s v1.81.0), so
  `Style.SkinKey` needs no check of its own.
- `docs/ARCHITECTURE.md:319-320` ("Oxanium and the Ka0s Default bar in place of Friz Quadrata and Blizzard"):
  still true for Ka0s Default; no change. Optionally note that each other skin now carries its own HUD face.
- `docs/ARCHITECTURE.md:330-334` first-run picker: no title wording; no change needed.

### 4.3 Other docs

- `docs/module-map.md:70` (`core/SkinSetup.lua` row): "`NS.SkinFontsIgnored` (the applied Ignore fonts, which
  `Style.SkinKey` reads for the HUD's face)" → remove.
- `docs/module-map.md:100` (`modules/Style.lua` row): check for the SkinKey/Ignore-fonts clause when editing.
- `docs/module-map.md:248-249` (`test_skin_surfaces.lua`, `test_skin_hud.lua` rows): adjust if cases change.
- `docs/module-map.md:319` "LibKa0s v1.80.0" → v1.81.0 (XX-RV).
- `docs/schema.md:825-830` v13 text ("A companion that is not yet a bool is seeded `false` first, so
  `ResetToSkin` never writes its `"@skin"` sentinel into a pick"): keep if the seed stays; if removed, say the
  library no longer does so (LK-07). It describes a shipped step, so prefer keeping it accurate to the code.
- `docs/settings-panel.md:384-389` (the Skin tab, "keyed by the Appearance group"): no change for R-10 unless
  WS-01 renames the key; `:738-739` label face picker: unchanged.
- `README.md:66-72`: "Ignore fonts keeps every font as you picked it" stays true; "a small window offers the
  skins with a preview" stays true. No change.
- `docs/testing.md`: no skin passage (`grep -ni skin docs/testing.md` → none). No change.
- `CLAUDE.md:36` provenance `v1.80.0` → `v1.81.0`; `DEPENDENCIES.md:91, 98` tag pins → `v1.81.0`;
  `tests/test_setups.lua:70` comment mentions the v1.80.0 re-vendor (comment only, may stay).

## 5. Current state

- Repo: `/mnt/d/Profile/Users/Tushar/Documents/GIT/AuraMaster`, branch `master`, HEAD `e565220` ("Merge
  feat/2026-10-29-skinning-rollout"), `## master...origin/master` (in step), **clean** (`git status -sb`), no
  stash, one worktree.
- Vendored LibKa0s: `CLAUDE.md:36` "Bundles [LibKa0s](https://github.com/tusharsaxena/LibKa0s) v1.80.0 (MIT)."
  and `CLAUDE.md:37` "LibKa0s icons: clear, close, copy, eye, help, info, settings."
- Gate on master, run 2026-10-30:
  - `~/.claude/dev-copilot/bin/ka0s-bounded lua tests/run.lua` → exit 0, tail:
    `2212 passed, 0 failed, 1 skipped, 2213 total (16 shards)`
  - `~/.claude/dev-copilot/bin/ka0s-bounded luacheck .` → exit 0, `Total: 0 warnings / 0 errors in 188 files`
  - 1500-line cap: largest non-vendored files `defaults/Categories.lua` 1344, `tests/test_filtercompiler.lua`
    1311, `tests/test_style.lua` 1206; `core/SkinSetup.lua` 475.
- **Gate: green.**

## 6. Nothing to change (exceptions.tsv candidates, each with its proving command)

Run from the AuraMaster root; each prints nothing unless the row says otherwise (verified 2026-10-30).

| Item | Claim | Proof |
|---|---|---|
| AM-01 / R-1 outline | AuraMaster never reads `hud.outline` (or `hud.fontSize`) | `grep -rnE 'hud\.(outline\|fontSize)' --include='*.lua' core modules settings defaults` |
| AM-01 / R-2 | no `stockDefault` or `stock =` caller | `grep -rnE 'stockDefault\|[^a-zA-Z_.]stock *=' --include='*.lua' core modules settings defaults` |
| AM-01 / R-3 | no close-button tint handling (the one other hit is the degraded facade's vocabulary name, `core/SkinSetup.lua:358`) | `grep -rnE 'CloseButton' --include='*.lua' core modules settings \| grep -vE 'MakeCloseButton\|core/SkinSetup.lua:358'` |
| AM-01 / R-5 | no hand-rolled Scope guard, no `S.Text`, no WidgetsReorder | `grep -rnE 'Skin\.Text\(\|S\.Text\(\|Reorder\|IsEnabled\(owner\|GetIgnore' --include='*.lua' core modules settings \| grep -vE 'core/SkinSetup.lua:(23\|44[23]):'` (after AM-01 deletes `NS.SkinFontsIgnored`, drop the `grep -v`) |
| AM-01 / R-8 | no `q.*` token, no quality literal | `grep -rnE 'ITEM_QUALITY\|GetItemQualityColor\|"q\.' --include='*.lua' core modules settings defaults` |
| AM-01 / R-9 | no `__DrawsKey` reach-in | `grep -rn 'DrawsKey' --include='*.lua' core modules settings tests/*.lua` |
| AM-02 / R-10 | the tab label is the library's "Skin"; "Appearance" is only the internal group/tab key (`settings/General.lua:174`, `core/SkinSetup.lua:271,276`, `settings/OptionsSetup.lua:340-342`, which already labels it "Skin") | `grep -rn '"Appearance"' --include='*.lua' core modules settings` lists only those key sites (not an empty-output proof; record the listing) |

## 7. Notes for the implementer

- Order: XX-RV (re-vendor from the `v1.81.0` tag) first; then delete 1.1 and rewrite
  `tests/test_skin_hud.lua:158-182` in the same commit, so the case goes red if LK-01 is missing from the
  vendored copy (run it once against v1.80.0 to confirm it fails without the library fix).
- After the re-vendor, run `tests/test_surface_parity.lua` first: a new facade member breaks the degraded
  vocabulary list (`core/SkinSetup.lua:355-363`).
- `NS.SkinFontsIgnored` is not referenced by any test other than `tests/test_skin_hud.lua:168,171`, nor by
  `tests/degraded_env.lua` (`grep -rn SkinFontsIgnored tests/*.lua`).
