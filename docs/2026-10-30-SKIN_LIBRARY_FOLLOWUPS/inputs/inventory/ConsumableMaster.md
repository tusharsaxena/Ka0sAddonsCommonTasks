# M0 inventory: ConsumableMaster (CM)

Read-only inventory for the LibKa0s v1.81.0 follow-ups (rulings R-1..R-11, `../../00_PLAN.md`).
Scope: `/mnt/d/Profile/Users/Tushar/Documents/GIT/ConsumableMaster`, excluding `libs/` and `tests/_kit/`.
Paths below are repo-relative to that root unless they start `LibKa0s/` (the library checkout,
`../LibKa0s/LibKa0s/`). Line numbers are taken at master `86dfb1b`.

## 0. Summary per ruling

| Ruling | CM has to change? | Where |
|---|---|---|
| R-1 Ignore fonts covers the HUD | **Yes**: remove the HUD Ignore-fonts workaround (`KCM.SkinFontsIgnored` and its two callers). One part, the count text, needs care (§1.1) | `modules/MacroBarButton.lua:143-181`, `core/SkinSetup.lua:46-47,483-485,539-543` |
| R-2 retire stockDefault / stock | **No code**: CM passes neither (grep in §6) | — |
| R-3 S.CloseButton tint | **No code**: CM calls no `S.CloseButton` | — |
| R-4 a HUD font per skin | **Docs and smoke only**: SKIN-4 and SKIN-10 already name per-skin faces the library does not draw today | `docs/smoke-tests.md:582,594` |
| R-5 S.Text / WidgetsReorder obey the Scope | **Yes, in part**: `KCM.SkinPanelOwner` goes and `KCM.SkinPanelText` might go. `SkinPanelColor` and `SkinPanelEscape` stay unless the library adds a scoped colour read (§1.2) | `core/SkinSetup.lua:179-225`, 4 ReorderList sites, 8 SkinPanelText sites |
| R-5 / LK-06 other custom widgets | **Docs and smoke only**: DragHandle, the debug console with its copy window, the perf panel and the launcher are the library's | SKIN-4, SKIN-9, SKIN-11 |
| R-6 ResetToSkin "@skin" in a bool companion | **Probably no**. CM's guard covers a different case (§1.3). Keep it unless LK-07 also covers it | `core/Database.lua:125` |
| R-7 DragHandle tooltip gtip.* | **No code**. CM passes no colours, only text (§6). The smoke check gains one line | `modules/MacroBar.lua:276-330` |
| R-8 q.* exact | **No**: CM has no quality colours | — |
| R-9 public DrawsKey | **No**: no `__DrawsKey` reach-in | — |
| R-10 tab named "Skin" in the standard | **No code**: the tab KEY stays `"Appearance"` (`LibKa0s/OptionsAppearance.lua:3-4,590`), and CM passes the key | `core/SkinSetup.lua:379` unchanged |
| R-11 picker title | **No code**: CM sets no title; the library builds it from the owner label `"Ka0s Consumable Master"` (`core/SkinSetup.lua:100,496`). Smoke SKIN-17 and SKIN-22 change | `docs/smoke-tests.md:608,616` |

## 1. Workarounds of library gaps that the release closes

### 1.1 R-1 / LK-01: the HUD's own Ignore-fonts handling

The workaround is the predicate plus its two callers.

- `core/SkinSetup.lua:46-47` (header doc): "`KCM.SkinFontsIgnored()` true while the Scope's "Ignore fonts" is on … The HUD's own SetFont calls (modules/MacroBarButton.lua) ask it."
- `core/SkinSetup.lua:539-543`: the live predicate, `Skin:GetIgnore(addonName)`'s second half.
- `core/SkinSetup.lua:483-485`: the degraded stub, `function KCM.SkinFontsIgnored() return false end`.
- **Label face**, `modules/MacroBarButton.lua:170-181`, `BB.LabelFace(cfg)`. Lines 175-179 short-circuit to `cfg.labelFont` while Ignore fonts is on, and map a stored `FROM_SKIN` to nil. Line 180 is the normal path, `BB.Follow("hud.font", cfg.labelFont, cfg.labelFontFromSkin)`.
  - **After LK-01**, `S.Resolve` makes the stored value win under Ignore fonts. `BB.Follow` (`modules/MacroBarButton.lua:84-93`) already turns a stored `FROM_SKIN` into nil (lines 88-90). So `BB.LabelFace` reduces to line 180 alone, and lines 175-179 are deleted.
  - The one caller is `modules/MacroBarButton.lua:392`, `fontFile(BB.LabelFace(cfg), btn.label:GetFont())`. Keep `BB.LabelFace` as a one-liner or inline it.
  - **Check for the implementer:** LK-01's `Resolve(owner, kind, value, fromSkin)` with `value == FROM_SKIN` under Ignore fonts. Today `LibKa0s/Skin.lua:868-870` returns the token. The stored value then IS the sentinel, so `BB.Follow` still has to answer nil (the shipped default face) for it. Lines 88-90 already do that if Resolve returns the sentinel or nil.
- **Stack count face**, `modules/MacroBarButton.lua:114-168`. The parts are `countFace` (118), `namedFontObject` (123-129), `restoreCountFont` (133-141) and `BB.ApplyCountFont` (143-168). Line 151, `if KCM.SkinFontsIgnored and KCM.SkinFontsIgnored() then return restoreCountFont(fs) end`, is the workaround. Lines 153 (`S.Token("hud.font")`) and 166 (`S.Token("hud.outline")`) read the skin's HUD face and outline directly. There is no stored value for the count (the doc comment is at `modules/MacroBarButton.lua:69-70`: "The count text has no setting, so it simply takes the skin's HUD face and outline (D6)").
  - **This is the R-1 surface that cannot simply be deleted.** LK-01 says Token honours Ignore fonts, "the stored value wins". The count has no stored value, so LK-01 has to define what `Token("hud.font")` answers under Ignore fonts: nil, KEEP, or the token anyway. Consequences:
    - If it answers **nil**, line 154 (`if type(face) ~= "string" then return end`) returns early and leaves a count the skin already reached on the skin's face. That breaks the live toggle that `tests/test_skin_hud.lua:171-202` pins. Fix: replace line 151 with `if type(face) ~= "string" then return restoreCountFont(fs) end` at line 154, and keep `countFace` and `restoreCountFont`. The library cannot reach this put-back itself, because these `SetFont` calls are not recorded paints (`modules/MacroBarButton.lua:146-148`).
    - If it **still answers the skin's face**, the line 151 guard (or an equivalent) has to stay. That is no longer a library gap but the addon's own choice for a string with no setting. Re-word the comment at `modules/MacroBarButton.lua:146-148` ("library_gap…") either way.
  - Callers: `modules/MacroBarButton.lua:491` (every bar button, from `ApplyStyle`) and `modules/MacroBarFlyout.lua:420` (every flyout entry).
- **Outline**: the label's outline is the player's `cfg.labelFlags` (`modules/MacroBarButton.lua:397-399`) and never `hud.outline`, so it is unaffected. The count's outline is `hud.outline` at line 166, and the count paragraph above covers it.
- **Dead-export consequence**: if both callers drop `KCM.SkinFontsIgnored`, remove it from both arms (`core/SkinSetup.lua:485,539-543`) and from the header (46-47). The member-parity test `tests/test_skin.lua:82-99` does not list it, so nothing there breaks. Its only test reads are `tests/test_skin_hud.lua:179,201`.
- **Composer picker preview** (LK-01's second half): the Labels font picker is the library composer's `fromSkin` row (`settings/MacroBar.lua:476-489`, `fromSkin = true` at 488, companion `fontFromSkin` at 484). CM has no workaround here. The library fixes it, and only the smoke check changes (§4).

### 1.2 R-5 / LK-05: hand-rolled Scope guards around S.Text and WidgetsReorder

The gap is stated in `core/SkinSetup.lua:179-192`: "library_gap (LibKa0s v1.80.0): only PaintAce and the Options chrome ask __PanelSkinned. S.Text always applies the skin's color AND body face, and ReorderList's `owner` always takes the owner's palette…". It is confirmed in the library: `LibKa0s/SkinPaintExtras.lua:316-327` (`prim.Text` never asks `__PanelSkinned`), `LibKa0s/WidgetsReorder.lua:56-61,539` (`skinPalette(opts.owner)` never asks it), and `LibKa0s/Skin.lua:628-631` (`__PanelSkinned`).

The helpers, in `core/SkinSetup.lua`:

| Helper | Lines | After LK-05 |
|---|---|---|
| `KCM.SkinPanelOn()` | 533-537 (live), 484 (degraded), doc 40-41 | Stays while any of the three below stays |
| `KCM.SkinPanelOwner()` | 206-211, doc 45 | **Delete.** Pass `owner = addonName` always, once ReorderList obeys the Scope. Verify that a list with `owner` under Ignore settings panel draws the same minor-1 defaults as `owner = nil` (`LibKa0s/WidgetsReorder.lua:48-61`) |
| `KCM.SkinPanelText(fs, role, stockFont)` | 213-225, doc 44 | **Conditional, see the caveat below** |
| `KCM.SkinPanelColor(name)` / `KCM.SkinPanelEscape(name)` | 194-204, doc 42-43 | **Stay.** They feed raw colours (`SetColorTexture`, `SetVertexColor`, ghost colours, tooltip escapes) that no library primitive draws, so LK-05 does not cover them unless it adds a Scope-aware colour read |
| `stock(name)` (local) | 164-170 | Stays with SkinPanelColor/Escape. It is CM's own "host copy of Ka0s Default", not `opts.stock` |
| `KCM.SkinUntrack` | 545-548, degraded 486 | Only `SkinPanelText` uses it (220). It goes if that goes |

**SkinPanelText caveat.** While the panel is ignored, the helper paints the template face plus CM's stock colour for the ROLE. That is not always the template's own colour:

- `modules/KCMMacroDragIcon.lua:90`: `"accent"` (gold) on a `GameFontHighlight` (white) string.
- `modules/KCMMacroDragIcon.lua:86`: `"sem.unknown"` (gray) on `GameFontHighlight`.
- `modules/KCMIconButton.lua:109`: `"disabled"` (gray) on `GameFontHighlight`.
- `settings/StatPriority.lua:503` and `settings/MacroBar.lua:967`: `"disabled"` (gray) on `GameFontNormal` (gold).

If the release's ignored S.Text only restores the string's pre-paint colour, these rows lose their state colours under Ignore settings panel. SKIN-7 (`docs/smoke-tests.md:588`) promises those colours "exactly as before". So `SkinPanelText` can become `KCM.Skin.Text(fs, role)` only if LK-05's ignored path still applies the role's stock (Ka0s Default) colour on the template face. Otherwise keep it. Raise this with the LK-05 implementer.

SkinPanelText call sites (8):

- `modules/KCMIconButton.lua:109,114`
- `modules/KCMMacroDragIcon.lua:86,90`
- `modules/KCMItemRow.lua:276,277`
- `settings/StatPriority.lua:503`
- `settings/MacroBar.lua:967`

SkinPanelOwner call sites (4, all `W.ReorderList({ … owner = KCM.SkinPanelOwner(), … })`):

- `settings/Category.lua:752` (call at 747, comment 751)
- `settings/Category.lua:979` (call at 974, comment 978)
- `settings/StatPriority.lua:622` (call at 613, comment 621)
- `settings/MacroBar.lua:1060` (call at 1052, comment 1059)

SkinPanelColor / SkinPanelEscape sites (they stay, listed for completeness):

- `modules/KCMIconButton.lua:32,110`
- `modules/KCMScoreButton.lua:84`
- `settings/Category.lua:143,151,159`
- `settings/StatPriority.lua:471,590,743`
- `settings/MacroBar.lua:911,1024`

Comments that name the gap and must be re-worded:

- `core/SkinSetup.lua:183-192`
- `modules/KCMItemRow.lua:273-275`
- `modules/KCMIconButton.lua:14-15`
- `modules/KCMMacroDragIcon.lua:83-84`
- `settings/StatPriority.lua:501-502`
- `settings/MacroBar.lua:965-966`
- the per-site "(KCM.SkinPanelOwner)" lines above

### 1.3 R-6 / LK-07: ResetToSkin guard

- `core/Database.lua:122-135`, `D.HUD_SKIN_KEYS` plus `D.MigrateHudSkinV4`. Line 125 seeds any absent `<key>FromSkin` companion to `false`, so that `Skin.ResetToSkin(bar, D.HUD_SKIN_KEYS)` (line 129) finds a companion and sets it true. Without the seed, the library writes `FROM_SKIN` into the LSM key itself (`LibKa0s/Skin.lua:900-905`). The rationale is the comment at `core/Database.lua:113-118`.
- CM names the **media keys** (`barBorderStyle`, `buttonBorderStyle`, `labelFont`), not the bool companions. R-6 as written ("writes `"@skin"` into an absent bool companion") is the companion-named-directly case (`LibKa0s/Skin.lua:902-905`, where `v == nil` falls to `else`), and CM never hits it. **Keep line 125 unless LK-07 also makes "an absent companion beside a string key" set the companion instead of the sentinel.** If it does, line 125 and its comment (113-118) can go, and `tests/test_skin_hud.lua:339-351` keeps passing unchanged as the proof. Either way, this goes in `exceptions.tsv` or in CM-01 depending on LK-07's final contract.
- The degraded branch at `core/Database.lua:130-132` stays.

### 1.4 Items with no workaround in CM (proof in §6)

- No `stockDefault` or `stock =` caller (R-2).
- No `S.CloseButton` (R-3). `KCM.MakeCloseButton` (`core/CoreSetup.lua:207-209`) wraps LibKa0s-Core's `lib.MakeCloseButton`, not the Skin primitive, and has no caller (`tests/test_surface_parity.lua:132-144`).
- No `__DrawsKey` (R-9).
- No literal `q.*` or quality colour (R-8). `core/ItemSetup.lua:11-13` documents that CM has no rarity concept.
- The tooltip lines CM writes already take `gtip.*`: `core/MacroDisplay.lua:199,205` and `settings/Category.lua:138-159`. The DragHandle's tooltips are text-only specs (`modules/MacroBar.lua:304-310,318-327`), so R-7 changes nothing in CM's code.

## 2. Where CM resolves a HUD face or outline itself (R-1)

| Site | Reads | Stored value that must win after R-1 |
|---|---|---|
| `modules/MacroBarButton.lua:180` → `BB.Follow` → `S.Resolve` (`modules/MacroBarButton.lua:87`) | `hud.font` for the button and flyout labels | `macroBar.labelFont` (default `"Friz Quadrata TT"`; companion `labelFontFromSkin`, `defaults/Profile.lua:235`). The library's Resolve does this after LK-01 |
| `modules/MacroBarButton.lua:153` → `S.Token("hud.font")` | the stack count face (bar and flyout) | **none**: the count's own face is its font object's (`NumberFontNormal`, `docs/ARCHITECTURE.md:366-367`), restored by `restoreCountFont` |
| `modules/MacroBarButton.lua:166` → `S.Token("hud.outline")` | the stack count outline | none (the font object's flags, restored with the face) |
| `core/SkinSetup.lua:457-460` (degraded `S.Resolve`) | no Ignore concept without the library | n/a, unchanged |

The other `BB.Follow` reads are border styles, not fonts, and are unaffected:

- `modules/MacroBarButton.lua:439,448`
- `modules/MacroBar.lua:380-381`
- `modules/MacroBarFlyout.lua:468-469`

## 3. Tests that pin the current behaviour

**R-1 (the HUD under Ignore fonts)**

- `tests/test_skin_hud.lua:168-202`, "Skin HUD: Ignore fonts puts the count and label back on their own faces, live".
  - It reads `KCM.SkinFontsIgnored()` at 179 and 201. Replace those reads with `Skin:GetIgnore(OWNER)` if the predicate is removed.
  - Its red-under comment (168-170) names the library gap and needs re-wording.
  - The expected behaviour stays the same: label = stored Friz (192-193), count put back (186-190), fresh count untouched (195-197). Keep the test as the regression proof.
- `tests/test_skin_hud.lua:143-166`, "the label and count faces are the skin's HUD font". This one is unchanged.
- Header `tests/test_skin_hud.lua:10`: the "(D6)" count bullet is unchanged.

**R-5 (the panel Scope)**

- `tests/test_skin_surfaces.lua:340-379`: the section comment (344-348) names the gap. The test "the panel helpers answer the stock look while the panel is ignored" pins `SkinPanelOwner()` at 366 and 369. Drop those assertions if SkinPanelOwner goes. The colour and escape assertions (370-375) stay.
- `tests/test_skin_surfaces.lua:381-402`, "the item row stays stock while the panel is ignored". It pins the template face plus the stock colours through `SkinPanelText`. Keep it (it becomes the proof that LK-05's ignored S.Text gives the same result) or adapt it.
- `tests/test_skin_surfaces.lua:404-432`, "the icon and score buttons stay stock while the panel is ignored". It pins the disabled gray on the `GameFontHighlight` label (420), which is exactly the case in the §1.2 caveat.
- `tests/test_skin_surfaces.lua:434-459`, "the settings surfaces read the skin only through the panel helpers". It **bans** a direct `KCM.Skin.Text(` and `owner = addonName` in `settings/*.lua` and `modules/KCM*.lua` (449-450). It must be relaxed in step with any deletion: allow `owner = addonName` once SkinPanelOwner goes, and `KCM.Skin.Text(` if SkinPanelText goes.
- `tests/test_skin.lua:162-190`, "every library factory that takes an owner is handed this addon's". It accepts `owner = KCM.SkinPanelOwner()` (comment 180-181, pattern 182). It already accepts `owner = addonName`, so only the comment and the alternative need cleaning.
- `tests/test_locale.lua:545-549` pins the literal text `KCM.SkinPanelText(self.label, "sem.unknown"` and `KCM.SkinPanelText(self.label, "accent"` in `modules/KCMMacroDragIcon.lua`. Update it if SkinPanelText is renamed or inlined.
- `tests/test_skin_settings.lua:116-126`, "with Ignore settings panel on, the default, nothing is painted" (AceGUI). Unchanged.

**R-6**

- `tests/test_skin_hud.lua:339-351`, "the reset writes no sentinel into a raw profile". It pins the line-125 seed. Keep it.

**R-11 and R-4**

- Nothing pins the picker title: `tests/test_skin_picker.lua:60` checks only `spec.tab == "Appearance"`.
- No test pins `hud.font` under a non-Ka0s skin: `tests/test_skin_hud.lua:206-220` (`"wow"`) checks only the icon border.

**Consequences after the test edits**

- **Badge and inventory**: if any test is added, removed or renamed, regenerate `docs/test-cases.md` (CLAUDE.md:123). The affected lines are 1047-1075, including 1057-1060 and 1068. Also bump the README `[Tests]` badge.
- **Degraded facade vocabulary**: if LK-05 or LK-06 add a facade VOCAB name, the degraded list at `core/SkinSetup.lua:445-453` must gain it. `tests/test_skin.lua:73-80` holds it key for key against the live facade.

## 4. Smoke checks and doc passages whose expectation changes

### Smoke checks (`docs/smoke-tests.md`)

- **SKIN-4** (line 582): "each time … the labels' and counts' face redraw in that skin (Ka0s Default Oxanium, Obsidian Inter, Azeroth Vollkorn, Glass Nunito, High Contrast Atkinson Hyperlegible, Ember Bitter, WoW Default Friz Quadrata, WoW Midnight Philosopher, WoW Forever Fira Sans)".
  - **This is wrong today.** Every non-Ka0s skin's `hud.font` is Friz Quadrata through KEEP (`LibKa0s/SkinDefs.lua:524-525,541-543`). Only Ka0s Default sets it (`LibKa0s/SkinDefs.lua:307`). The list names the skins' BODY faces.
  - Rewrite it with LK-04's per-skin HUD faces once `DECISIONS.md` fixes them.
  - Also add: the drag handle's tooltips take the skin's tooltip colours (R-7).
- **SKIN-10** (line 594): "On **WoW Forever** → the bar's labels and counts read Fira Sans". This is wrong today for the same reason. Replace it with LK-04's WoW Forever HUD face. The Ignore-fonts half (labels in the player's own Labels font, counts in the game's number font, live) already describes R-1. Keep it, and add that the Labels font picker on Macro Bar → Labels previews the stored face, not the skin's, while Ignore fonts is on (LK-01's composer half).
- **SKIN-17** (line 608): "a small window titled **Choose a skin for Ka0s Consumable Master**". It becomes: titled **Choose a skin**, with **Ka0s Consumable Master** on its own line above the dropdown, not truncated (R-11).
- **SKIN-22** (line 616): "close it → the other opens, titled for its addon". It becomes: "naming its addon above the dropdown" (R-11).
- **SKIN-6** (line 586) and **SKIN-7** (line 588): the expectations stay the same; they become the regression check for LK-05 replacing the addon's helpers. If LK-06 makes the drag ghosts and handles obey the Scope, SKIN-6's list ("the drag ghosts and handles") stays correct.
- **SKIN-9** (line 592), the tool windows: add that switching back to Ka0s Default restores the debug console's and perf panel's close mark to its own tint (R-3, LK-03). LK-06 also brings the Scope to these library windows, and the expectation follows LK-06's rule.
- **SKIN-11** (line 596): "hover and right-click the minimap button → the game's tooltip and menu". This changes only if LK-06 skins the Launcher's tooltip lines or menu. Check against LK-06's widget list.
- **SKIN-1** (line 576) and **SKIN-23** (line 620): unchanged. Under Ka0s Default nothing moves, and SKIN-1 already says the tool windows read Oxanium.
- The section intro (`docs/smoke-tests.md:568`) names "LibKa0s v1.80.0", and the index row at line 21 lists the SKIN topics. Add a dated sub-note or new checks for v1.81.0 rather than rewriting history.
- Also, at lines 660-662: the summary says "the addon's own rows under Ka0s Default, whose face moves to Oxanium and is flagged". That contradicts SKIN-7 ("these rows keep Friz Quadrata") and is pre-existing drift. Fix it while editing.

### ARCHITECTURE (`docs/ARCHITECTURE.md`)

- 329-331: the list of published helpers names `SkinPanelOwner` and `KCM.SkinFontsIgnored` ("the macro bar's count and label faces ask it"). Drop whichever go.
- 360-368: "*Ignore fonts* wins over both: the library's `hud.font` token never asks the exception (a library gap in v1.80.0) … so `BB.ApplyCountFont` and `BB.LabelFace` ask `KCM.SkinFontsIgnored` themselves". Rewrite it for the library's own handling, and keep the count's put-back explanation if §1.1's first option is taken.
- 386-397: "the library's `S.Text` … never asks whether the owner ignores its settings panel, and neither does `ReorderList`'s `owner` (a library gap in v1.80.0). So while … `SkinPanelOwner` hands the reorder lists no owner." Rewrite it per what §1.2 deletes.
- 404-407: "the four reorder lists `owner = KCM.SkinPanelOwner()` (this addon while the settings panel is skinned, none while it is ignored)". This becomes `owner = addonName`.
- 316: "adopted `LibKa0s-Skin-1.0` … at LibKa0s v1.80.0". Add the v1.81.0 follow-up note.

### Other docs

- `docs/module-map.md`:
  - 625-628: the API block lists `SkinPanelOwner`, plus `SkinFontsIgnored` with "the HUD's own faces ask it".
  - 799: the `core/SkinSetup.lua` row says "(…which the library's `S.Text` and `ReorderList` do not honor)" and "`KCM.SkinFontsIgnored` (… since `hud.font` does not honor *Ignore fonts*)".
  - 675: the `Skin-1.0` consumer row, to check.
  - 830: the `modules/MacroBarButton.lua` row does not mention Ignore fonts, so it needs no change.
- `docs/macro-bar.md:121-129`: "With the Skin tab's *Ignore fonts* ticked, the count goes back to the game's number font and the label to the player's own *Labels font*, live." The behaviour is unchanged. The wording is fine, and only the mechanism changes (no edit needed unless the mechanism is named).
- `docs/settings-panel.md:212-216`: "(painted from `KCM.Skin` through the panel helpers, so they too stay stock while *Ignore settings panel* is on)". Adjust it if the helpers go.
- `docs/testing.md:14`: the headless-tests row lists the skin suites by name, which is unaffected unless a suite is renamed. `docs/testing.md:156` says "vendored from LibKa0s v1.80.0". Roll it at re-vendor.
- `README.md`:
  - 71 (first-run picker: "a small window asks you to choose a skin") still holds under R-11. No change.
  - 130 (troubleshooting: Ka0s Default's Oxanium) is unchanged.
  - The README carries no Ignore-fonts or per-skin HUD face text.
- `CLAUDE.md:61` (provenance line `v1.80.0`) and `CLAUDE.md:88` ("`Skin` at v1.80.0") are rolled at CM-RV.
- Source comments that name v1.80.0 gaps: `core/SkinSetup.lua:103` (the "v1.80.0, Skin minor 7" history is fine to keep), `core/SkinSetup.lua:183`, `tests/run.lua:542` (kit note), `tests/test_surface_parity.lua:273` (history is fine).

## 5. Current state

- **Repo:** `/mnt/d/Profile/Users/Tushar/Documents/GIT/ConsumableMaster`, branch `master`, tracking `origin/master` with nothing ahead or behind (`## master...origin/master`), HEAD `86dfb1b` "Merge feat/2026-10-29-skinning-rollout". The working tree is **clean**: no stash and one worktree.
- **Vendored LibKa0s** (`CLAUDE.md:61`): "Bundles [LibKa0s](https://github.com/tusharsaxena/LibKa0s) v1.80.0 (MIT)."
  - Icons (`CLAUDE.md:62`): "LibKa0s icons: clear, close, copy, help, info, segment, settings."
- **Gate on master, run 2026-10-30:**
  - `~/.claude/dev-copilot/bin/ka0s-bounded lua tests/run.lua` printed `1292 passed, 0 failed, 1 skipped, 1293 total` (exit 0).
  - `~/.claude/dev-copilot/bin/ka0s-bounded luacheck .` printed `Total: 0 warnings / 0 errors in 138 files` (exit 0).
  - 1500-line cap: the largest non-vendored Lua file is `settings/MacroBar.lua` at 1227 lines, followed by `settings/Category.lua` (1186) and `tests/test_schema.lua` (1173). Under the cap.
  - **Gate green.**
- Line counts of the files CM-01 edits:
  - `core/SkinSetup.lua`: 578
  - `modules/MacroBarButton.lua`: 595
  - `settings/MacroBar.lua`: 1227
  - `settings/Category.lua`: 1186
  - These are all deletions, so the cap is no risk.

## 6. Nothing to change: proofs for `exceptions.tsv`

Run each from `/mnt/d/Profile/Users/Tushar/Documents/GIT/ConsumableMaster`. An empty output proves the claim. Each was run at `86dfb1b` and printed nothing, except R-8, which printed one comment-only line.

| Ruling | Claim | Command |
|---|---|---|
| R-2 | no `stockDefault` / `stock` caller | `git grep -n -E 'stockDefault\|stock[[:space:]]*=' -- ':!libs' ':!tests/_kit'` |
| R-3 | no `S.CloseButton` caller | `git grep -n -E '(Skin\|S)[.:]CloseButton\(' -- ':!libs' ':!tests/_kit'` |
| R-7 | the DragHandle spec passes no colour | `sed -n 276,340p modules/MacroBar.lua \| grep -n -iE 'color\|\{ *[0-9.]+ *,'` |
| R-8 | no quality colour in code | `git grep -n -E '"q\.[a-z]+"\|ITEM_QUALITY_COLORS\|GetItemQualityColor' -- core modules settings` (prints only `core/ItemSetup.lua:12`, a comment that says they appear nowhere) |
| R-9 | no `__DrawsKey` reach-in | `git grep -n 'DrawsKey' -- ':!libs' ':!tests/_kit'` |
| R-10 | the tab key `"Appearance"` is unaffected by the standard's rename | `git grep -n 'tab = "Appearance"' core/SkinSetup.lua` (one hit: `core/SkinSetup.lua:379`, the key, which LibKa0s keeps per `LibKa0s/OptionsAppearance.lua:3-4`) |
| R-11 | CM sets no picker title | `git grep -n -E 'TITLE_FOR\|title[[:space:]]*=' -- core/SkinSetup.lua` |
| R-6 | conditional: CM names no bool companion to ResetToSkin | `grep -n 'HUD_SKIN_KEYS =' core/Database.lua` → `{ "barBorderStyle", "buttonBorderStyle", "labelFont" }` (media keys only) |

## 7. Notes for the M2 implementer

- **CM-RV:** re-vendor from the tag (`git archive v1.81.0`), prune icons with the same declaration, then roll `CLAUDE.md:61,88` and `docs/testing.md:156`.
- **CM-01, in order:**
  1. §1.1 label (delete `modules/MacroBarButton.lua:175-179`).
  2. §1.1 count (one of the two options, decided by LK-01's Token contract).
  3. Drop `KCM.SkinFontsIgnored` if it has no callers left.
  4. §1.2: `SkinPanelOwner` goes, and the 4 ReorderList sites take `owner = addonName`.
  5. `SkinPanelText` goes only under LK-05's stock-colour contract.
  6. §1.3 per LK-07.
  7. Tests per §3.
- **CM-02:** the smoke and doc edits in §4, plus `docs/test-cases.md` and the README badge if the suite changed.
