# M0 inventory: PartyFrameEnhanced

Read-only inventory for `docs/2026-10-30-SKIN_LIBRARY_FOLLOWUPS/00_PLAN.md` (rulings R-1..R-12). Taken
2026-10-30 at `master` b64ba84 ("Merge feat/2026-10-29-skinning-rollout"). Paths are relative to
`../PartyFrameEnhanced` unless they start with `LibKa0s/`, which means `../LibKa0s/LibKa0s/` (master
ea1d92d, v1.80.0). The vendored copies under `libs/` and `tests/_kit/` were read for reference only.

## 0. Bottom line

PartyFrameEnhanced has **one workaround the release deletes**: the HUD's own Ignore-fonts patch,
`NS.SkinIgnoresFonts` (`core/SkinSetup.lua:369-376`, degraded twin `:337-338`) and its one caller in
`Element.MediaKeys` (`modules/Element.lua:116`). After LK-01 makes `S.Resolve("hud.font", pick, true)`
answer the stored pick while Ignore fonts is on, that line and the seam go. Everything else in the
ruling list has **no** site here: no `stockDefault` / `stock` caller, no hand-rolled Scope guard, no
`ResetToSkin` call, no reach into `Skin:__DrawsKey`, no close-button tint handling, no `gtip.*` / `q.*`
stand-ins, no `WidgetsReorder` or other custom widget of its own, and no `hud.outline` read.

For PartyFrameEnhanced, M2 comes down to:

- **PF-RV**: the re-vendor, the provenance line (`CLAUDE.md:41`), the vendor line in `docs/smoke-tests.md:58`,
  and the degraded facade's vocabulary list if the release adds facade names (§7 H-2).
- **PF-01**: delete `NS.SkinIgnoresFonts` and the `Element.MediaKeys` patch; move the test that pins it to the
  library's behaviour (§1, §2, §3).
- **PF-02**: smoke SKIN-4 (the per-skin HUD faces, R-4), SKIN-17 and SKIN-23 (the picker title, R-11),
  SKIN-24 (Ignore fonts now the library's), and the ARCHITECTURE / module-map passages that describe the
  patch (§4).

Three hazards for the LK implementers are in §7. The most important: the free-placement holders' caption
is an `S.Text` on a **HUD** surface (`modules/Anchor.lua:302`); LK-05 must not unpaint it under the default
*Ignore settings panel* = on.

## 1. Library-gap workarounds (per ruling)

| Ruling / item | What PartyFrameEnhanced has | Cite | Change at M2 |
|---|---|---|---|
| R-1 / LK-01 (Ignore fonts on HUD) | **The workaround.** `NS.SkinIgnoresFonts()` reads the applied exception through `Skin:GetIgnore(addonName)` because "S.Resolve("hud.font") does not consult it" (doc comment). `Element.MediaKeys` forces the font companion off while it answers true. The degraded arm defines a twin that answers false. Header doc of the seam lists it. | `core/SkinSetup.lua:369-376` (live), `:337-338` (degraded), `:24-25` (header); `modules/Element.lua:110-120` (caller, the patch is `:116`; doc comment `:111-113`) | **Delete** `modules/Element.lua:116` and rewrite `:110-113`'s comment (the library's Resolve now honours the exception). Delete `NS.SkinIgnoresFonts` in both arms (`core/SkinSetup.lua:337-338`, `:369-376`) and its header line `:24-25`; it has no other caller (grep §6 row 9). The parity test derives the seam's members from the file (`tests/test_surface_parity.lua:285-300`), so deleting it from both arms keeps that green. |
| R-2 / LK-02 (retire `stockDefault`/`stock`) | **No caller.** This addon draws no window. Its own surfaces (the HUD's three media keys, the holders' plate and caption) already paint the Ka0s look under Ka0s Default and look the same afterwards. The library-painted surfaces it shows (settings pages, debug console + copy window, perf panel, launcher, first-run picker) do not pass `stockDefault` either: no library module outside `Skin*.lua` names it (grep in `LibKa0s/`: only `Skin.lua`, `SkinPaint.lua`, `SkinPaintControls.lua`, `SkinPaintExtras.lua`). The one library `stock =` list it shows is the settings tab strip and content box (`LibKa0s/OptionsTabs.lua:493-504`), visible on PF's pages only while *Ignore settings panel* is off (default on: `defaults/Profile.lua:25`). | proof grep §6 row 1 | None in code. See hazard H-3 for LK-02. |
| R-3 / LK-03 (CloseButton tint) | No tint handling. `NS.MakeCloseButton` is a pass-through to `LibKa0s-Core`'s `MakeCloseButton` that adds the folder name (not `S.CloseButton`). The only `SetVertexColor` is the HUD background color (`modules/Element.lua:259`). | `core/CoreSetup.lua:110-112`, `:48-51` (degraded) | None |
| R-4 / LK-04 (HUD font per skin) | No own fallback: the HUD asks `S.Resolve("hud.font", …)` and falls back to the player's pick only where the skin answers nothing (`modules/Element.lua:103-108`). Today the eight non-Ka0s skins answer `hud.font` = Friz Quadrata through `KEEP` (`LibKa0s/SkinDefs.lua:523-525`, applied `:542-544`); only Ka0s Default sets its own (`LibKa0s/SkinDefs.lua:307`). So on a default profile (`font = "Friz Quadrata TT"`, `defaults/Profile.lua:78,111,139`) the HUD face does not change across the eight. After LK-04 each skin's face shows on the HUD with no code change here. | `modules/Element.lua:103-120` | None in code. Smoke SKIN-4's face list (§4) and two test comments (§3). |
| R-5 / LK-05 (`S.Text`, `WidgetsReorder` obey Scope) | **No guard.** The one `S.Text` is the free-placement holders' caption, called bare, on a **HUD** surface, not on a settings page. No `WidgetsReorder`. | `modules/Anchor.lua:299-303`, comment `:273`, `:291-294` | None. **Hazard H-1**: LK-05 must not unpaint this caption under the default Scope. |
| R-5 / LK-06 (custom widgets) | No custom widget of its own. It consumes the library's DebugLog console and copy window (`core/DebugLogSetup.lua:92`), the Perf step panel (`core/PerfSetup.lua:25`), the Launcher (`core/LauncherSetup.lua:46`) and the first-run picker (`core/SkinSetup.lua:263`). Their Scope behaviour is library-side. | proof grep §6 row 5 | None in code. Smoke SKIN-8 / SKIN-7 may change wording if LK-06 puts the tool windows under the panel Scope (§4). |
| R-6 / LK-07 (`ResetToSkin` `"@skin"`) | **No `ResetToSkin` call.** The v2 migration writes the `*FromSkin` companions directly **because** ResetToSkin would write `"@skin"` into the LSM key (comment). That is a reasoned choice, not a guard around a library call; the migration stays as is (it never wants the sentinel). The degraded facade's `FROM_SKIN = "@skin"` (`core/SkinSetup.lua:294`) and `storedKey`'s sentinel filter (`:123-126`) mirror the library and are not ResetToSkin guards. | `core/Database.lua:50-69` (comment `:55-57`) | None. Optional: reword `core/Database.lua:55-57` to say the direct write is kept (the step must not depend on library behaviour at a given minor). |
| R-7 / LK-08 (DragHandle `gtip.*`) | No DragHandle, no tooltip color literal. The color literals in the addon are chat lines and the stand-in's look (`core/Namespace.lua:9`, `core/DebugLogSetup.lua:47`, `modules/Preview.lua:43,45`, `modules/StandIn.lua:29`, `settings/Slash.lua:397`), all on the literal gate's allow-list (X7). | proof grep §6 row 4 | None |
| R-8 / LK-09 (`q.*` exact) | No quality color used. | proof grep §6 row 4 | None |
| R-9 / LK-10 (public `DrawsKey`) | No reach into `__DrawsKey` or any `Skin:__*`. The `__` names in the addon are its own seams (`modules/Anchor.lua:46`, `modules/SecureFollow.lua:124`, `core/Database.lua:74`) and one Options publish, `lib.__PatchLSM30Border()` (`settings/OptionsSetup.lua:173`; `libs/LibKa0s/Options.lua:313`), which is not a Skin internal. | proof grep §6 row 2 | None |
| R-10 (standard: tab "Skin") | The tab already renders "Skin". The key stays `"Appearance"` (library key): `NS.SkinPickerSpec` `tab = "Appearance"` (`core/SkinSetup.lua:208-210`), the rows' `group = APPEARANCE` (`settings/General.lua:279-330`), docs `docs/ARCHITECTURE.md:94,408`. | — | None, unless WS-01/LK renames the key (not planned) |
| R-11 / LK-11 (picker title) | Passes no title. The library composes "Choose a skin for <label>" (`LibKa0s/OptionsSkinPicker.lua:14,106,240`) from `RegisterOwner`'s `label = BRAND` = **"Ka0s Party Frame Enhanced"** (`core/SkinSetup.lua:71,350-351`), one of the longer labels in the collection (25 characters). No PF test pins the title (§3). Smoke SKIN-17 and SKIN-23 do (§4). | — | Smoke update; optional new test assertion (§3) |

## 2. HUD face or outline the addon resolves itself (R-1)

**One site: `Element.MediaKeys`** (`modules/Element.lua:114-120`), which resolves `hud.font` through the
facade (`resolved()` at `:103-108` calls `NS.Skin.Resolve(token, pick, true)` at `:105`) and today forces
`fontFromSkin = false` itself while Ignore fonts is on (`:116`). It is called once per restyle by
`Element.Reskin` (`modules/Element.lua:234`), which every HUD feature runs on `OnLooksChanged`
(`modules/CastBars.lua:433`, `modules/TargetFrames.lua:358`, `modules/PetFrames.lua:230`).

- **Face.** After LK-01, `S.Resolve("hud.font", cfg.font, true)` answers `cfg.font` (the section's own
  *Font*, the "HUD element's own font setting") while Ignore fonts is on, so `resolved()` returns the
  pick and `:116` is redundant: delete it. The resolved key still enters the structure signature, so the
  toggle still restyles, provided `Skin:SetIgnore` keeps firing `OnLooksChanged` (it does today; pinned by
  `tests/test_skin_hud.lua:151`).
- **Edge to confirm with LK-01**: `resolved()` treats a non-string or empty answer as "skin left it alone"
  and returns the pick (`modules/Element.lua:106`). Any LK-01 answer for the ignored case (the pick, or
  nil) therefore lands on the pick. No change needed either way.
- **Outline.** PF never reads `hud.outline` (or `hud.fontSize`). The HUD's outline is the player's
  `cfg.fontFlags` (`modules/Element.lua:194`), never the skin's (X4,
  `docs/ARCHITECTURE.md:424-425`). Nothing to change for the outline half of R-1.
- **Override interplay.** The Font override lays over `hud.font` (`LibKa0s/Skin.lua:727`); under
  Ignore fonts the stored pick must win over the override too (LK-01's call; PF expects the pick, as
  SKIN-24 says).
- **Holders' caption.** `S.Text` routes the face through the library's `P.font`
  (`LibKa0s/SkinPaintExtras.lua:316-327`), which already honours Ignore fonts. No change.

## 3. Tests that pin current behaviour

| Test | Cite | Pins | After the release |
|---|---|---|---|
| "skin hud: Ignore fonts gives the HUD the player's own face back, live" | `tests/test_skin_hud.lua:140-164` (asserts `NS.SkinIgnoresFonts()` at **:149** and **:163**; red-under note **:150**; comment **:141-142** "several other skins keep Friz (the library's KEEP)") | R-1 via the addon's own patch | **Must change.** Drop the two `NS.SkinIgnoresFonts` assertions (the seam is deleted); keep every face/texture/memo assertion (`:145`, `:151-158`), which now pin the library's behaviour; rewrite `:150` to "red under: S.Resolve ignoring the owner's ignoreFonts" and `:141-142` (after LK-04 no skin keeps Friz). |
| "skin hud: the structure memo holds the RESOLVED keys, so a skin switch restyles" | `tests/test_skin_hud.lua:126-138` (`:132` asserts Obsidian's `hud.font` ≠ Oxanium; today true only because it is KEEP's Friz) | R-4 indirectly | Passes after LK-04 provided Obsidian's new face is not Oxanium. Comment-only touch if wanted. |
| "skin hud: following the skin, an element draws Ka0s Default's bar, border and HUD face" | `tests/test_skin_hud.lua:92-100` (`:99` pins `"Ka0s Oxanium SemiBold"`) | Ka0s Default `hud.font` | Unchanged (LK-04 does not touch Ka0s Default). |
| "skin hud: a skin switch restyles the live cast bars, target and pet frames" | `tests/test_skin_hud.lua:180-195` (`:182` `want = Token("hud.font")` under Obsidian, `:188` counts fetches of it) | R-4 indirectly | Unchanged in shape; after LK-04 `want` is Obsidian's new face rather than Friz, which makes the test stronger (today the default-profile pick is also Friz). |
| "skin hud: a skin that leaves a token alone falls back to the player's pick" | `tests/test_skin_hud.lua:111-124` (stubs `NS.Skin.Resolve`) | `resolved()` fallback | Unchanged. |
| "skin hud: a companion turned off …", the defaults/rows tests, the v2 migration tests | `tests/test_skin_hud.lua:67-88`, `:102-109`, `:212-257` | companions, O2 reset, direct companion writes (R-6 context) | Unchanged. |
| "parity: the Skin seam publishes the same NS members on both paths" | `tests/test_surface_parity.lua:285-300` | Both arms of `core/SkinSetup.lua` publish the same `NS.*` | Stays green if `NS.SkinIgnoresFonts` is deleted from **both** arms. |
| "parity: the degraded Skin facade answers every name the live facade carries" | `tests/test_surface_parity.lua:276-283` against the vocabulary list `core/SkinSetup.lua:298-306` | Facade vocabulary | Goes red if LK-02..LK-11 add or remove a facade name (e.g. a public `DrawsKey` placed on the facade, or new widget primitives under LK-06). PF-RV adds the name as a no-op (H-2). |
| "parity: each host-copy skin token is the live library's Ka0s Default value" | `tests/test_surface_parity.lua:302-325`; copy `NS.SKIN_FALLBACK` = `text.accent` only (`core/SkinSetup.lua:89-91`) | `text.accent` | Unchanged (LK-09 touches only `q.*`). |
| "skin holders: …" (five tests) | `tests/test_skin_holders.lua:82-115` | Caption via `S.Text(…, "accent")` repaints on every skin; Ka0s Default exact gold | Unchanged **only if** LK-05 keeps HUD `S.Text` painted under *Ignore settings panel* = on (the default; these tests run on the default profile). H-1. |
| Skin picker tests (17) | `tests/test_skin_picker.lua:77-290` | The spec, triggers, seen-marking, eye, Apply. The window cases drive the library's real picker (`:205-282`). **No assertion on the title** (`grep -n title tests/test_skin_picker.lua` is empty). | Unchanged. Optional: add an assertion that the window title is "Choose a skin" and that the owner line above the dropdown reads "Ka0s Party Frame Enhanced" (field name per LK-11). |
| "Skin seam: …" | `tests/test_skinsetup.lua:62-68` (`OwnerLabel` = "Ka0s Party Frame Enhanced"), `:178-202` (SetIgnore/GetIgnore through `/pfe set` and the profile) | the exceptions' write path | Unchanged. |
| Settings layout row for `skin.ignoreFonts` | `tests/test_settings_layout.lua:136` | the row's shape | Unchanged. |
| Vendor sync | `tests/test_vendor_sync.lua` | the provenance line vs. the vendored tag | Moves with PF-RV. |

## 4. Smoke checks and doc passages whose expectation changes

### docs/smoke-tests.md

| Check | Cite | Today's expectation | After the release |
|---|---|---|---|
| Section index row | `docs/smoke-tests.md:28` | "Ignore fonts on the HUD" in the SKIN-1–25 summary | Unchanged wording; add the picker line if a check is added. |
| Library vendor line | `docs/smoke-tests.md:58` | "v1.80.0: … OptionsSkinPicker 1, … Skin 7, SkinDefs 15, SkinPaint 11, SkinPaintExtras 5, SkinPaintControls 9 …, Widgets 16, WidgetsDragHandle 6 …" | The v1.81.0 minors (PF-RV). |
| **SKIN-4** (every skin live on the HUD) | `docs/smoke-tests.md:656-664`, the face list at **:659-661** | "Ka0s Default Oxanium, Obsidian Inter, Azeroth Vollkorn, Glass Nunito, High Contrast Atkinson Hyperlegible, Ember Bitter, WoW Default Friz Quadrata, WoW Midnight Philosopher, WoW Forever Fira Sans". **This is wrong on v1.80.0**: those are the skins' `font.body` faces; the HUD reads `hud.font`, which is KEEP's Friz for all eight (`LibKa0s/SkinDefs.lua:525`). | Replace the eight names with LK-04's picks (from `DECISIONS.md`). Also the failure line "text clipped in a wider face" becomes a real risk to watch. |
| **SKIN-8** (tool windows) | `docs/smoke-tests.md:688-692` | debug console, Copy window, perf panel wear the skin; back on Ka0s Default it "looks as it did before this run" | Only if LK-06 puts these library windows under the panel Scope or changes their Ka0s Default look: say whether *Ignore settings panel* now keeps them stock. Otherwise unchanged. |
| **SKIN-7** (settings pages) | `docs/smoke-tests.md:679-687` | with *Ignore settings panel* unticked each page takes the skin; ticked again every page is stock "while the HUD and holders keep the skin" | The last clause is H-1's expectation and must stay true. If LK-02 changes how the tab strip/content box look under Ka0s Default (H-3), note it here. |
| **SKIN-17** (picker at login) | `docs/smoke-tests.md:730-737`, title at **:731-732** | "a small window titled **Choose a skin for Ka0s Party Frame Enhanced** … a dropdown showing the skin worn now" | "titled **Choose a skin**, with **Ka0s Party Frame Enhanced** on its own line above the dropdown, not cut off". Add to the failure clause: a title or name that is truncated. |
| **SKIN-23** (one picker across addons) | `docs/smoke-tests.md:768-773`, **:770** "close it → the other opens, titled for its addon" | | "the other opens, naming its addon above the dropdown". |
| **SKIN-24** (Ignore fonts reaches the HUD) | `docs/smoke-tests.md:774-779` | behaviour already right (PF-03's patch); "(PF-03; review fix)" | Outcome unchanged; the provenance becomes the library (LK-01). Its "Repeat under **Obsidian** with a section's *Font* set to something other than Friz" (`:778-779`) gains meaning after LK-04 (Obsidian's HUD face is no longer Friz, so the box visibly changes the face on a default profile too). Add: the composer's *Font* picker previews the stored face while Ignore fonts is on (LK-01's picker half), if PF's composer shows that preview. |
| SKIN-6 (holders) | `docs/smoke-tests.md:671-678` | caption takes each skin's accent color and face | Unchanged; must stay true under the default Scope (H-1). |
| SKIN-9 (overrides) | `docs/smoke-tests.md:693-698` | | Unchanged. |

No smoke check here describes a "stock look under Ka0s Default": grep `stock` in `docs/smoke-tests.md` hits only
SKIN-7's "every page here is stock" (the panel Scope, which stays per R-2).

### Other docs

| Doc | Cite | Change |
|---|---|---|
| ARCHITECTURE, HUD bullet | `docs/ARCHITECTURE.md:419-431`, the patch at **:427-429** ("`S.Resolve` does not consult the exception, so `Element.MediaKeys` asks `NS.SkinIgnoresFonts` (`Skin:GetIgnore`) and composes it on this side") | Rewrite: the library's `S.Resolve` keeps each section's own face while Ignore fonts is on (LibKa0s v1.81.0). Also `:423-424` "falls back to the player's pick where a skin leaves the token alone": after LK-04 no Ka0s skin leaves `hud.font` alone; keep it for EllesmereUI / degraded. |
| ARCHITECTURE, one-time reset | `docs/ARCHITECTURE.md:441-444` | Unchanged (Ka0s Default only). |
| ARCHITECTURE, holders | `docs/ARCHITECTURE.md:445-447` | Unchanged, unless LK-05 needs PF to mark the caption as HUD (H-1). |
| ARCHITECTURE, picker | `docs/ARCHITECTURE.md:448-456` | No title quoted; optional sentence on the new layout. |
| ARCHITECTURE, "the library draws the rest" | `docs/ARCHITECTURE.md:457-461` | Update only if LK-06 puts the console / copy window / perf panel under the panel Scope. |
| module-map, SkinSetup row | `docs/module-map.md:22` ("`NS.SkinIgnoresFonts` (the applied *Ignore fonts*, which the HUD's face asks)") | Delete the clause. |
| core/SkinSetup.lua header | `core/SkinSetup.lua:24-25` | Delete (part of PF-01). |
| test-cases | `docs/test-cases.md:582` (test name), `:727` counts | Update if the test is renamed; counts if a picker test is added. |
| testing.md | `docs/testing.md:45-49` | Unchanged unless a test is added. |
| schema.md | `docs/schema.md:32` "skin.ignoreFonts = false … keep every font as the client draws it (the skin still colors the text)" | Accurate for the panel; optionally add "the HUD keeps each section's own *Font*". |
| settings-panel.md | `docs/settings-panel.md:91` (Scope row) | Same optional note as schema.md. `:90` lists `hud.font` among the override's tokens: unchanged. |
| Ignore fonts row tooltip | `settings/General.lua:309` "Keep every font in this addon as the game draws it. The skin still colors the text." | Not exact for the HUD (it keeps the player's own *Font*, not the game's); optional reword, with the locale key (localization cost). Not required by the rulings. |
| README | `README.md:101` (troubleshooting row: bars changed texture and font, "a window asked me to choose a skin") | Unchanged. `README.md:137-147` font credits: add any new face LK-04 introduces (the fonts ship in the LibKa0s payload, credited here). |
| CLAUDE.md | `CLAUDE.md:41` "Bundles LibKa0s v1.80.0 (MIT)." `CLAUDE.md:42` icons line | Roll to v1.81.0 (PF-RV); icons unchanged unless LK-11 adds one. |

## 5. Current state

- Branch **`master`**, tracking `origin/master`, **clean** (`git status -sb` printed only
  `## master...origin/master`). HEAD `b64ba84` "Merge feat/2026-10-29-skinning-rollout: the LibKa0s
  skinning rollout". No run branch yet.
- Vendored LibKa0s: **v1.80.0** (`CLAUDE.md:41`: "Bundles [LibKa0s](https://github.com/tusharsaxena/LibKa0s) v1.80.0 (MIT).").
  `LibKa0s icons: clear, close, copy, eye, settings.` (`CLAUDE.md:42`).
- Gate on master, run 2026-10-30:
  - `~/.claude/dev-copilot/bin/ka0s-bounded lua tests/run.lua` → `538 passed, 0 failed, 1 skipped, 539 total`, exit 0.
  - `~/.claude/dev-copilot/bin/ka0s-bounded luacheck .` → `Total: 0 warnings / 0 errors in 87 files`, exit 0.
  - **Gate green.**

## 6. Proof greps (rows for exceptions.tsv)

Run from `../PartyFrameEnhanced`; each prints nothing (or the stated count):

| # | Claim | Command | Result |
|---|---|---|---|
| 1 | No `stockDefault` / `stock` caller (R-2) | `grep -rnE 'stockDefault\|stock *=' --include='*.lua' core modules settings defaults locales` | 0 lines |
| 2 | No `__DrawsKey` reach (R-9) | `grep -rnE '__DrawsKey\|DrawsKey' --include='*.lua' core modules settings defaults locales` | 0 lines |
| 3 | No `ResetToSkin` call (R-6) | `grep -rnE 'ResetToSkin\(' --include='*.lua' core modules settings defaults locales` | 0 lines (the two hits for `ResetToSkin` are the comment `core/Database.lua:56-57`) |
| 4 | No `gtip.*` / `q.*` stand-in (R-7, R-8) | `grep -rnE 'gtip\.\|\bq\.[a-z]' --include='*.lua' core modules settings defaults locales` | 0 lines |
| 5 | No `WidgetsReorder` or custom widget (R-5) | `grep -rnE 'WidgetsReorder\|Reorder\|DragHandle\|Autocomplete\|LineChart\|Toast' --include='*.lua' core modules settings` | 0 lines |
| 6 | No `hud.outline` read (R-1 outline half) | `grep -rnE 'hud\.outline' --include='*.lua' core modules settings defaults` | 0 lines |
| 7 | No close-button tint (R-3) | `grep -rnE 'S\.CloseButton\|Skin\.CloseButton' --include='*.lua' core modules settings` | 0 lines |
| 8 | No hand-rolled Scope guard (R-5) | `grep -rnE 'GetIgnore' --include='*.lua' core modules settings` | 4 lines, all in `core/SkinSetup.lua:369-375`, the R-1 workaround PF-01 deletes (not a Scope guard) |
| 9 | `NS.SkinIgnoresFonts` has one caller | `grep -rn 'SkinIgnoresFonts' --include='*.lua' core modules settings` | `core/SkinSetup.lua:338,373` (definitions) and `modules/Element.lua:116` (the caller) |

So PF-01's R-2, R-3, R-6, R-7, R-8, R-9 halves and R-5's guard half are exceptions with rows 1-8; PF-01
itself is a real change (R-1).

## 7. Hazards for the LK implementers

- **H-1 (LK-05): `S.Text` on a HUD surface.** `modules/Anchor.lua:302` paints the free-placement caption
  with `NS.Skin.Text(holder.label, "accent")`. It is HUD, not settings panel. If LK-05 makes every `S.Text`
  stand down while *Ignore settings panel* is on (the default, `defaults/Profile.lua:25`), the caption stays
  GameFontNormalSmall's stock gold in the stock face under every skin, and five tests go red
  (`tests/test_skin_holders.lua:82-115`, e.g. `:92` expects Obsidian's `text.accent`), plus smoke SKIN-6 and
  SKIN-7's "while the HUD and holders keep the skin". LK-05 needs a way to tell a panel `S.Text` from a HUD
  one (e.g. scope only targets inside the owner's settings panel, or an opt such as `{ hud = true }`). If it
  is an opt, PF-01 adds it at `modules/Anchor.lua:302` and the degraded `S.Text` (`core/SkinSetup.lua:327-331`)
  accepts and ignores it.
- **H-2 (any LK that adds a facade name): the degraded facade's vocabulary.** `core/SkinSetup.lua:298-306`
  lists every facade name as a no-op, and `tests/test_surface_parity.lua:276-283` holds it to the live facade
  key for key with nothing ignored. A public `DrawsKey` on the facade (LK-10) or new primitives (LK-06) make
  PF's suite red at re-vendor until the name is added there. A name LK-02 removes from the facade would also
  need removing. Put the list of added/removed facade names in "What a consumer owes".
- **H-3 (LK-02): the library's own `stock =` lists.** The settings tab strip and content box hand their
  client art to `S.Tab` / `S.Panel` as `opts.stock` (`LibKa0s/OptionsTabs.lua:493-504`), which is how that art is
  faded (`LibKa0s/SkinPaint.lua:244-256`). Retiring `opts.stock` must keep that art faded under every skin, or
  PF's pages show the client's tab slices under the skin's fill when *Ignore settings panel* is off
  (SKIN-7).
