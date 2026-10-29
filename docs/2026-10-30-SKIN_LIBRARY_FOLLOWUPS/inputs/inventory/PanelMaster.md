# M0 inventory: PanelMaster

Read-only inventory for `docs/2026-10-30-SKIN_LIBRARY_FOLLOWUPS/00_PLAN.md` (rulings R-1..R-12). Taken
2026-10-30 at `master` febaed5. Paths are relative to `../PanelMaster` unless they start with `LibKa0s/`,
which means `../LibKa0s/LibKa0s/`. The vendored copies under `libs/` and `tests/_kit/` are out of scope.

## 0. Bottom line

PanelMaster has **no workaround the release deletes**. It has no HUD font, no `stockDefault`/`stock`
caller, no `ResetToSkin` call, no reach into `Skin:__*` internals, no close-button tint handling, no
`gtip.*`/`q.*` stand-ins, and it uses neither `WidgetsReorder` nor any other custom widget of its own. Its
only skin surfaces are the unlock overlay (`S.Text` label and a `list.dropLine` outline), the Panels
picker's *(disabled)* marker, and the AceGUI widgets it acquires outside the Options proxy. The library
draws everything else (settings chrome, debug console and copy window, first-run picker, launcher).

For PanelMaster, M2 therefore comes down to:

- **PM-RV**: the re-vendor, plus the provenance line.
- **PM-02**: docs and smoke for the picker title (R-11). It also covers checks that change only if
  LK-02, LK-05 or LK-06 changes a library-painted surface PanelMaster shows (§4).
- **PM-01**: an exceptions row, or a small hardening change (§6).

Two hazards for the LK implementers are in §7.

## 1. Library-gap workarounds (per ruling)

| Ruling / item | What PanelMaster has | Cite | Change at M2 |
|---|---|---|---|
| R-1 / LK-01 (Ignore fonts on HUD) | No HUD face or outline, so it has no `NS.SkinFontsIgnored`-style patch. The only string it hands to the skin is the unlock label, through `S.Text(o.label, "accent")`. `S.Text` already routes the face through `P.font`, which honours `ignoreFonts` (`LibKa0s/SkinPaintExtras.lua:316-326`, `LibKa0s/Skin.lua:633-637`). | `modules/Unlock.lua:112-118` | None |
| R-2 / LK-02 (retire `stockDefault`/`stock`) | **No caller.** Under Ka0s Default, PanelMaster's own surfaces already paint the Ka0s look: the unlock outline and label, the marker, and the editor widgets once the panel is unignored. Afterwards they look the same. The only visible change is in **library-painted** surfaces that currently use `stockDefault`/`stock` internally: the settings tab strip and content box (`LibKa0s/OptionsTabs.lua:493-504`) and stock-template PageButtons (`LibKa0s/SkinPaintControls.lua:579-582`). It shows on PanelMaster's settings pages **only while Ignore settings panel is off** (default on: `defaults/Profile.lua:82`, `settings/Schema.lua:182`). The Scope switch stays, per R-2. | proof grep §6 row 1 | None in code. Smoke SKIN-3 needs a note (§4) |
| R-3 / LK-03 (CloseButton tint) | No tint handling. `NS.MakeCloseButton` is a pass-through that adds the addon name. | `core/CoreSetup.lua:142-144` | None |
| R-4 / LK-04 (HUD font per skin) | No HUD font. The rollout inventory recorded "no HUD font" (`../Ka0sAddonsCommonTasks/docs/2026-10-29-SKINNING_ROLLOUT/inputs/inventory/PanelMaster.md:46`). The panels belong to the player (D1). | proof grep §6 row 2 | None |
| R-5 / LK-05 (`S.Text`, `WidgetsReorder` obey Scope) | No guard around `S.Text`. The label is called bare (`modules/Unlock.lua:118`). No `WidgetsReorder`. The guard the rollout report credits to "PM" (`../Ka0sAddonsCommonTasks/docs/2026-10-29-SKINNING_ROLLOUT/99_REPORT.md:134-135`) is **`NS.SkinPanelEscape`**, a **color escape** for settings-page markup that answers Ka0s Default while `Skin:GetIgnore(owner)` reports the panel ignored. It is not an `S.Text` guard. LK-05 as written (`00_PLAN.md`, LK-05 row) covers `S.Text` and `WidgetsReorder`, not token or escape reads, so this guard **stays** unless LK-05 also ships a panel-scope-aware `Color`/escape. If it does, PM-01 swaps `NS.SkinPanelEscape` for it. | `core/SkinSetup.lua:131-142` (definition), `settings/PanelEditor.lua:658-664` (only caller), `docs/module-map.md:18` | None, unless LK-05 adds a panel-scoped color read |
| R-5 / LK-06 (custom widgets) | It uses the library's DebugLog console and its CopyWindow (`core/DebugLogSetup.lua:115-190`), the Launcher (`core/LauncherSetup.lua:169`) and the first-run picker. It has no custom widget of its own. Widgets, Toast and Sim are vendored but not consumed (`CLAUDE.md:45-48`). | proof grep §6 row 7 | None in code. Smoke SKIN-4, SKIN-8 and SKIN-20 may change (§4) |
| R-6 / LK-07 (`ResetToSkin` `"@skin"`) | **No `ResetToSkin` call.** D1 rules out an O2 HUD reset (`../Ka0sAddonsCommonTasks/docs/2026-10-29-SKINNING_ROLLOUT/99_REPORT.md:110-111`). The only `"@skin"` is the degraded facade's `FROM_SKIN` constant, a mirror of the library value and not a guard. | `core/SkinSetup.lua:339` | None |
| R-7 / LK-08 (DragHandle `gtip.*`) | No DragHandle and no tooltip color literal. Editor tooltips carry inline `|cffffff00` emphasis as content markup (X9). | `docs/ARCHITECTURE.md:292-293` | None |
| R-8 / LK-09 (`q.*` exact) | No quality color is used. | proof grep §6 row 6 | None |
| R-9 / LK-10 (public `DrawsKey`) | No reach into `__DrawsKey` or any `Skin:__*`. | proof grep §6 row 5 | None. See hazard H-1 |
| R-10 (standard: tab "Skin") | The tab already **renders** "Skin". The **key** stays `"Appearance"` (library key) in `NS.SkinPickerSpec` and the docs. | `core/SkinSetup.lua:253-255`, `settings/Panel.lua:329-347` | None, unless WS-01/LK renames the *key* (not planned) |
| R-11 / LK-11 (picker title) | Its own code passes no title. The library composes "Choose a skin for <OwnerLabel>" (`LibKa0s/OptionsSkinPicker.lua:106,240-245,690`) from `RegisterOwner`'s `label = NS.BRAND` = "Ka0s Panel Master" (`core/SkinSetup.lua:380-384`, `core/Namespace.lua:33`). The test and the smoke check pin the old title (§3, §4). | — | Test and smoke update |

## 2. HUD face or outline the addon resolves itself (R-1)

**None.** PanelMaster never calls `S.Resolve`, `S.Token("hud.*")` or `FROM_SKIN` outside the degraded
facade's own `Resolve` mirror (`core/SkinSetup.lua:356-358`). The `R:Resolve` hits in
`modules/Registry.lua:399` and `settings/Slash.lua:278` resolve panel keys and have nothing to do with skins.
The schema stores no font for panels (`defaults/Profile.lua:23-63`, as cited by the rollout inventory).
Proof: §6 row 2.

## 3. Tests that pin current behaviour

| Test | Cite | Pins | After the release |
|---|---|---|---|
| "Skin picker: the player's close marks it seen; this addon's own hide does not" | `tests/test_skin_picker.lua:224-236`, assertion at **:227** `assertEqual(f.title:GetText(), "Choose a skin for " .. NS.BRAND, ...)` | The R-11 title | **Must change.** The title becomes `"Choose a skin"`. Add an assertion that the addon's name, `NS.BRAND`, is on the new line above the dropdown (field name per LK-11) and is not truncated. |
| "Skin picker: the spec names this owner, its seams, the General page's Skin tab, no eye" | `tests/test_skin_picker.lua:92-104` (`spec.tab == "Appearance"` at :101) | Tab key | Unchanged, unless the key is renamed |
| "Skin literals: the picker's (disabled) marker ..." (three tests) | `tests/test_skin_literals.lua:252-284` | `NS.SkinPanelEscape` behaviour (§1 R-5) | Unchanged, unless LK-05 adds a panel-scoped color read and PM-01 adopts it. The red-under note at :276-277 would then name the new API. |
| "Skin literals: the host copy of Ka0s Default equals the library's Ka0s Default" | `tests/test_skin_literals.lua:203-215` | `NS.SKIN_FALLBACK` = `text.disabled`, `list.dropLine` (`core/SkinSetup.lua:97-105`) | Unchanged. LK-09 touches only `q.*`. It goes red only if a release moves either token's Ka0s Default value. |
| "Skin unlock: the label takes the skin's accent text role once, at creation" | `tests/test_skin_unlock.lua:114-128` | `S.Text(label, "accent")` once. It **replaces `NS.Skin.Text` with a recorder**, so it cannot see the library's behaviour. | Unchanged. See hazard H-2: no test would catch LK-05 un-painting the label under the default Scope. |
| "Skin unlock" outline tests | `tests/test_skin_unlock.lua:59-112` | `list.dropLine` outline | Unchanged |
| "skin settings: with the panel ignored (the default) the editor is left stock", "... Ka0s Default paints the editor like every other skin once the panel is", "... band's picker and create box follow the Scope ..." | `tests/test_skin_settings.lua:103-146` | SkinAce's Scope obedience for PaintAce | Unchanged. LK-02 does not touch PaintAce's ownership, and these assert owner records, not looks. |
| "Skin seam: the tab's Ignore fonts reaches the library and the profile, one repaint" | `tests/test_skinsetup.lua:240-256` | Ignore fonts plumbing | Unchanged |
| "Skin seam: a profile reset puts the skin, its exceptions and overrides back to Ka0s Default" | `tests/test_skinsetup.lua:297-309` | Reset through AceDB defaults, not `ResetToSkin` | Unchanged |
| Vendor gate | `tests/test_vendor_sync.lua` (reads `CLAUDE.md:58`) | Provenance v1.80.0 | Moves with PM-RV |
| Doc counts | `README.md:7` (badge 1140/1140), `docs/test-cases.md:1341` (Total 1140), `docs/test-cases.md:945` (`test_skin_picker.lua (13)`) | Test totals | Roll if PM-01/PM-02 add tests |

## 4. Smoke checks and doc passages whose expectation changes

**Certain (R-11):**

- `docs/smoke-tests.md:1176-1183` **SKIN-15**: "a small window titled **Choose a skin for Ka0s Panel
  Master**". The title becomes **Choose a skin**, and **Ka0s Panel Master** goes on its own line above
  the dropdown, in full and never cut off. Add "Fail: the name truncated".
- `docs/smoke-tests.md:1214-1220` ("Pending sign-off" paragraph): add the re-owed check(s) from this run.
- `docs/ARCHITECTURE.md:295-300` (first-run picker bullet) does not mention the title, so no change is
  needed. `docs/settings-panel.md:73` does not either.

**Conditional on how LK-02/05/06 land (the implementer checks against the release's CHANGELOG):**

- `docs/smoke-tests.md:1126-1134` **SKIN-3**: "then Ka0s Default → … all repaint". With `stockDefault`
  retired (LK-02), Ka0s Default on the **unignored** settings pages now shows the Ka0s look on the tab
  strip, content box and stock arrow buttons, where it used to fade to stock. If LK-02 changes what
  OptionsTabs paints, add a line.
- `docs/smoke-tests.md:1111-1119` **SKIN-1**: "The settings pages look as before too, because **Ignore
  settings panel** is on". This stays true, because the Scope is kept (R-2). The same sentence holds the
  unlock label "in **Oxanium**". If LK-05 gates `S.Text` on the panel Scope for **every** string, this
  becomes false (hazard H-2).
- `docs/smoke-tests.md:1135-1139` **SKIN-4**: "while the debug console and the unlock overlay still wear
  Obsidian". This changes if LK-05/06 makes the DebugLog console, its copy window or `S.Text` obey
  **Ignore settings panel**. They are not settings-panel surfaces, so the expected answer is "unchanged".
- `docs/smoke-tests.md:1149-1153` **SKIN-7**: "Tick **Ignore fonts** → every string goes back to its own
  face". `S.Text` already honours it, and with LK-06 the console's strings should too. The wording
  stands. Re-verify only if LK-06 changes the console's font path.
- `docs/smoke-tests.md:1154-1157` **SKIN-8** (console under Azeroth): unchanged unless LK-06 restyles
  the console or CopyWindow.
- `docs/smoke-tests.md:1200-1205` **SKIN-20** ("the minimap button and its tooltip look as before") and
  `docs/ARCHITECTURE.md:290-292` ("the minimap button stay stock (skinning-§7)"): these change if
  LK-06 skins the Launcher's tooltip or button.
- `README.md:70-74`: the player-facing skin paragraph says "A skin colors the unlock outlines and the
  debug console". It gains "and the minimap tooltip" only if LK-06 skins the launcher.
- `docs/settings-panel.md:56` (Skin tab row: "It changes the settings pages …, the debug console and the
  unlock overlay"): the same condition as above.

**No change (R-1 HUD face under non-Ka0s skins, R-4):** PanelMaster draws no HUD text that reads
`hud.font`, so no smoke check or doc covers a HUD face under the non-Ka0s skins. Proof is grep §6
row 2, plus `grep -n "hud" docs/smoke-tests.md docs/ARCHITECTURE.md`, which finds only the "no HUD reset"
mentions at `docs/smoke-tests.md:34,1113` and `docs/ARCHITECTURE.md:288-289`.

**Tab name (R-10):** `docs/ARCHITECTURE.md:278-280`, `docs/settings-panel.md:66-73` and
`core/SkinSetup.lua:253-255` say the tab is **keyed** `Appearance` and **labelled** Skin. That is still
correct after WS-01, which renames the standard's label, not the key.

## 5. Current state (step 5)

- Branch `master` at **febaed5**, tracking `origin/master` with no ahead or behind. The tree is **clean**
  (`git status -sb`), with 0 stashes and one worktree (the main checkout only).
- Provenance line: `CLAUDE.md:58` "Bundles [LibKa0s](…) v1.80.0 (MIT)." Icon declaration `CLAUDE.md:59`:
  "LibKa0s icons: clear, close, copy, settings." If LK-03 or LK-11 makes the picker or close control draw a
  new Media icon, the declaration and `tests/test_mediasetup.lua:88` must follow.
- Gate on master, run 2026-10-30:
  - `~/.claude/dev-copilot/bin/ka0s-bounded lua tests/run.lua`: **`1140 passed, 0 failed, 1 skipped, 1141 total`** (exit 0)
  - `~/.claude/dev-copilot/bin/ka0s-bounded luacheck .`: **`Total: 0 warnings / 0 errors in 80 files`** (exit 0)
  - 1500-line cap: the largest skin files are `docs/smoke-tests.md` at 1220 lines (a doc), `settings/PanelEditor.lua` at 809, `modules/Unlock.lua` at 515 and `core/SkinSetup.lua` at 436.
- **Gate green.**

## 6. Nothing to change: proof greps (exceptions.tsv candidates for PM-01)

Run from `../PanelMaster`. Each prints nothing, or only the lines noted.

| # | Claim | Command | Output today |
|---|---|---|---|
| 1 | No `stockDefault`/`stock` caller (R-2) | `grep -rnE 'stockDefault\|stock *=' --include='*.lua' --exclude-dir=libs --exclude-dir=_kit --exclude-dir=tests .` | empty |
| 2 | No HUD face or outline resolved by the addon (R-1, R-4) | `grep -rnE 'hud\.(font\|outline)\|FROM_SKIN\|fromSkin' --include='*.lua' --exclude-dir=libs --exclude-dir=_kit --exclude-dir=tests .` | only `core/SkinSetup.lua:339,356,357` (the degraded facade mirror) |
| 3 | No Ignore-fonts patch | `grep -rnE 'SkinFontsIgnored\|FontsIgnored\|GetIgnore' --include='*.lua' --exclude-dir=libs --exclude-dir=_kit --exclude-dir=tests .` | only `core/SkinSetup.lua:136` (the **panel** half, in `NS.SkinPanelEscape`, §1 R-5) |
| 4 | No `ResetToSkin` and no `"@skin"` guard (R-6) | `grep -rnE 'ResetToSkin\|"@skin"' --include='*.lua' --exclude-dir=libs --exclude-dir=_kit --exclude-dir=tests .` | only `core/SkinSetup.lua:339` (the degraded `FROM_SKIN` constant) |
| 5 | No reach into Skin internals (R-9) | `grep -rnE '__DrawsKey\|DrawsKey\|__PanelSkinned\|__FontsIgnored' --include='*.lua' --exclude-dir=libs --exclude-dir=_kit .` | empty |
| 6 | No `gtip.*`/`q.*` stand-ins (R-7, R-8) | `grep -rnE 'gtip\|"q\.\|ITEM_QUALITY_COLORS\|GetItemQualityColor' --include='*.lua' --exclude-dir=libs --exclude-dir=_kit --exclude-dir=tests .` | empty |
| 7 | No custom library widget and no `WidgetsReorder` (R-5) | `grep -rnE 'WidgetsReorder\|Reorder\|DragHandle\|Autocomplete\|LineChart\|Toast' --include='*.lua' --exclude-dir=libs --exclude-dir=_kit --exclude-dir=tests .` | empty |
| 8 | No close-button tint handling (R-3) | `grep -rnE 'CloseButton\(' --include='*.lua' --exclude-dir=libs --exclude-dir=_kit --exclude-dir=tests .` | only `core/CoreSetup.lua:143` (the pass-through) |

Suggested `exceptions.tsv` row: `PM-01  PanelMaster  no workaround to delete: no stockDefault/stock,
HUD font, ResetToSkin, __DrawsKey, tint, gtip/q, Reorder  <grep rows 1,4,5,6,7 above, each must print
nothing>`. Rows 2, 3 and 8 print only the lines this report already explains, so as proofs they should
`grep -v` those lines or count them (for example `| wc -l` = 3, 1, 1).

## 7. Hazards for the LK implementers (found while reading)

- **H-1: the degraded facade mirrors `lib.VOCAB` by hand, and no test holds it.**
  - `core/SkinSetup.lua:340-352` copies the vocabulary list. Its comment at :342-343 says
    "tests/test_surface_parity.lua holds this table to the live facade key for key", but that file has
    no Skin reference (`grep -n "Shell\|Skin\|VOCAB" tests/test_surface_parity.lua tests/degraded_env.lua`
    is empty).
  - If LK-05, LK-06 or LK-10 adds a facade entry to `lib.VOCAB` (`LibKa0s/Skin.lua:107-115`), or a
    `DrawsKey` on the facade (`LibKa0s/Skin.lua:1014-1027`), the degraded `NS.Skin` silently lacks it.
  - PM-RV should mirror any new name. Optionally, PM-01 adds the missing parity test, or corrects the
    stale comment.
- **H-2: LK-05 must not put the unlock label behind the panel Scope.**
  - PanelMaster's default is `ignorePanel = true` (`defaults/Profile.lua:82`). Its one `S.Text` string is
    the unlock overlay label (`modules/Unlock.lua:118`), which is not a settings-panel string.
  - If LK-05 makes `S.Text` skip painting whenever `__PanelSkinned(owner)` is false, the label falls back
    to `GameFontNormal`, which breaks SKIN-1 and SKIN-6.
  - `tests/test_skin_unlock.lua:114-128` stubs `NS.Skin.Text`, so it would stay green. LK-05 should scope
    the panel check to settings-panel strings only, as SkinAce does via the proxy. PM-01 can add a
    library-level test: with the default Scope, the label is recorded for the owner (`Skin.painted`) and
    wears the skin's face.
