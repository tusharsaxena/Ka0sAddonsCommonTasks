# M0 inventory: AbsorbTracker

Read-only inventory for `docs/2026-10-30-SKIN_LIBRARY_FOLLOWUPS/00_PLAN.md` (rulings R-1..R-11, items AT-RV,
AT-01, AT-02). Repo: `/mnt/d/Profile/Users/Tushar/Documents/GIT/AbsorbTracker` (written `AT/` below), with
`libs/` and `tests/_kit/` left out except where a library line is cited for reference (`LK/` =
`/mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s/`, at master `ea1d92d`, v1.80.0). Every line number is
for AT master `a41affd`.

## 5. Current state (read first)

| What | Value |
|---|---|
| Branch | `master` at `a41affd` ("Merge feat/2026-10-29-skinning-rollout") |
| Tree | clean (`git status --porcelain` empty), 0 stashes, 1 worktree (the repo itself) |
| Vendored LibKa0s | **v1.80.0**: `AT/CLAUDE.md:46` "Bundles [LibKa0s](...) v1.80.0 (MIT)."; icons line `AT/CLAUDE.md:47` "LibKa0s icons: clear, close, copy, help, settings." |
| Other release pins to move at AT-RV | `AT/docs/module-map.md:1010` ("The v1.78.0 to v1.80.0 payloads add two more majors: `LibKa0s-Skin-1.0` ..."); `tests/test_vendor_sync.lua` reads the tag from CLAUDE.md (`AT/tests/test_vendor_sync.lua:8`) |
| Tests | `~/.claude/dev-copilot/bin/ka0s-bounded lua tests/run.lua`: **`954 passed, 0 failed, 1 skipped, 955 total`**, exit 0 |
| Lint | `~/.claude/dev-copilot/bin/ka0s-bounded luacheck .`: **`Total: 0 warnings / 0 errors in 77 files`**, exit 0 |
| 1500-line cap | largest non-vendored Lua file `tests/test_schema.lua` 1084 lines; `core/SkinSetup.lua` 361 |
| **Gate** | **green on master** |

## 1. Workarounds the release closes

### 1a. Own Ignore-fonts handling for the HUD face (R-1 / LK-01): **present, delete**

The one real workaround in this addon. The library's `Resolve`/`Token` do not read `ignoreFonts`
(`LK/LibKa0s/Skin.lua:811-813` Token, `LK/LibKa0s/Skin.lua:868-871` Resolve), so AT checks it itself:

| Site | What |
|---|---|
| `AT/core/SkinSetup.lua:19-21` | header doc for `NS.SkinFontsIgnored()` ("the library's Resolve/Token never check it, only P.font does") |
| `AT/core/SkinSetup.lua:280` | degraded arm: `function NS.SkinFontsIgnored() return false end` |
| `AT/core/SkinSetup.lua:325-331` | live arm: `NS.SkinFontsIgnored()` via `Skin:GetIgnore(addonName)` |
| `AT/core/Data.lua:143-145` | `NS.MediaKey` doc: "Ignore fonts wins for the face ... The library's Resolve/Token do not check it" |
| `AT/core/Data.lua:148` | **the workaround**: `if key == "font" and NS.SkinFontsIgnored and NS.SkinFontsIgnored() then return stored, false end` |

Delete `Data.lua:148` and both arms of `NS.SkinFontsIgnored` together: `tests/test_surface_parity.lua:361-379`
derives the seam's NS members by grepping `core/SkinSetup.lua` and holds the live and degraded sets equal, so
removing only one arm fails it.

**Decision point for the implementer (depends on how LK-01 lands).** `NS.MediaKey` returns `v, on`
(`AT/core/Data.lua:149-155`), and the second value feeds the diagnostics `skin=yes|no` column
(`AT/modules/Diagnostics.lua:193-197`) and is pinned by `AT/tests/test_skin_hud.lua:148-150`
(`fromSkin == false` while ignored).
- If LK-01 makes `Token("hud.font")` answer nil under Ignore fonts, `Resolve` returns nil and MediaKey
  already falls through to `return stored, false` (`Data.lua:153-155`): behaviour identical, test passes.
- If LK-01 makes `Resolve("hud.font", stored, true)` answer `stored`, MediaKey returns `stored, true`:
  same face, but `/at diagnostics` would print `skin=yes` for the stored face and `test_skin_hud.lua:150`
  goes red. Then either keep a small check that reports `on = false` when the library says fonts are
  ignored (through the new public API, not `GetIgnore` by hand), or accept `skin=yes` and re-pin the test
  and SKIN-25. Read LK-01's contract in `LK/docs/api/` before choosing.

After the change, under Ka0s Default with *Use the skin's font* ticked and Ignore fonts on, the bar number
draws the stored `units.<unit>.font` (Friz Quadrata TT on an untouched profile, `AT/docs/schema.md:467`),
exactly as today: the visible behaviour of SKIN-26 does not change; only who enforces it does.

### 1b. HUD outline (R-1 outline half): **nothing to change**

AT never reads `hud.outline` or `hud.fontSize`; the outline is always the player's `fontFlags`:
`AT/core/Data.lua:193-197` (GetFont is "the face only"), `AT/modules/Display.lua:220-221`
(`SetFont(NS.GetFont(unit), NS.Units.Get(unit, "fontSize"), NS.Units.Get(unit, "fontFlags") or "")`),
`AT/modules/Bar.lua:298` (build-time `unitDefaults.fontSize/fontFlags`).
Proof: `git grep -n "hud.outline" -- '*.lua' ':!libs' ':!tests/_kit'` → no hits (only the doc comment
`AT/core/Data.lua:193`). Exceptions row candidate: "AT resolves no HUD outline".

### 1c. `stockDefault` / `stock` callers (R-2 / LK-02): **none**

AT passes neither option anywhere. Proof:
`git grep -n -E "stockDefault|stock *=" -- '*.lua' ':!libs' ':!tests/_kit'` → no hits (the word "stock"
appears only in comments/test names about AceGUI widgets returned to the pool: `AT/core/SkinSetup.lua:40,282`,
`AT/settings/Profiles.lua:86`, `AT/settings/UnitPanel.lua:191`, `AT/tests/test_skin_tools.lua:9,83,101,106`).
The library has no internal `stockDefault = true` caller either (`grep -n "stockDefault *= *true" LK/LibKa0s/*.lua`
→ none), so AT's library surfaces (drag strips, debug console + copy window, perf panel, launcher, picker)
already paint the Ka0s look under Ka0s Default. **After R-2 the look under Ka0s Default does not change** for
any AT surface. Exceptions row candidate.

### 1d. Hand-rolled Scope guards around S.Text / WidgetsReorder / other widgets (R-5 / LK-05, LK-06): **none**

AT uses neither `S.Text` nor `WidgetsReorder`. Proof:
`git grep -n -E "S\.Text|\.Text\(|Reorder|Autocomplete|LineChart|Toast" -- core modules settings` → no hits.
`NS.SkinPaintAce` / `NS.SkinPaintAceTree` (`AT/core/SkinSetup.lua:310-318`) carry no Scope check; the doc
line "Nothing while the owner ignores its settings panel" (`AT/core/SkinSetup.lua:38-41`) describes the
library's own behaviour, pinned by `AT/tests/test_skin_tools.lua:83` ("under the default Scope (Ignore settings
panel) the chrome block stays stock"). Not a workaround.

Custom LibKa0s widgets AT consumes (all affected by LK-06, none guarded here):
- WidgetsDragHandle, `owner = addonName`: `AT/modules/Bar.lua:135-196` (owner at `:142`, tooltip
  descriptors `:150-187`); stub `AT/core/WidgetsSetup.lua:32`.
- DebugLog window + copy window: `AT/core/DebugLogSetup.lua:14,124`.
- Perf panel: `AT/core/PerfSetup.lua:16,113`.
- Launcher (minimap button + tooltip): `AT/core/LauncherSetup.lua:70`.
- OptionsSkinPicker: `AT/core/SkinSetup.lua:226-244`.

**Open dependency on LK-06's Scope semantics (flag for the lead).** AT's docs promise these surfaces wear the
skin regardless of *Ignore settings panel*: `AT/docs/settings-panel.md:345-347` ("the bars, the strips, the
console and the perf panel wear the skin either way"), `AT/docs/ARCHITECTURE.md:366-370`, smoke SKIN-9
(`AT/docs/smoke-tests.md:184`) and SKIN-10 (`:185`), both run with the default Scope (Ignore settings panel
**on**). If LK-06 puts the console/copy/perf/drag strip under the *panel* exception, all four passages and
both checks flip ("stock until you untick Ignore settings panel"). If it puts them under *Ignore fonts* only
(the drag-strip label already keeps its face, `AT/docs/ARCHITECTURE.md:353`), only the font wording changes.

### 1e. ResetToSkin guard against the `"@skin"` sentinel (R-6 / LK-07): **present; keep code, fix rationale**

| Site | What |
|---|---|
| `AT/core/Database.lua:229-233` | comment: "ONLY A STORED COMPANION IS NAMED ... ResetToSkin, handed a bool key that is absent, cannot tell it is a bool and writes its `"@skin"` sentinel into it" |
| `AT/core/Database.lua:241-247` | the guard: only `type(u[key]) == "boolean"` keys are named to `resetToSkin(p, keys)` (`:250`); no-library arm sets them directly (`:246`) |
| `AT/docs/module-map.md:897` | "... naming only a companion that is stored, because an absent one already reads its default and `ResetToSkin` would write its `"@skin"` sentinel into it" |
| `AT/docs/module-map.md:308` | ladder summary line for v6 |
| `AT/docs/ARCHITECTURE.md:358-363`, `AT/docs/data-flow.md:43` | v6 described (no sentinel claim at ARCH; check data-flow wording on edit) |

Library side: `LK/LibKa0s/Skin.lua:886-910` (`lib.ResetToSkin`: an absent value that is not a table and has no
`FromSkin` sibling falls to `parent[leaf] = lib.FROM_SKIN`, `:904`).

Recommendation: **keep the filter**. It is still right after LK-07: an absent companion already reads its
default (`true`), so naming it would only store a redundant explicit value in a raw profile, and the filter
also drives the `moved` count (`:243`) and the debug line (`:253-255`). `AT/tests/test_skin_hud.lua:275`
pins "an absent companion stays absent: it reads on", which holds either way. What changes is the
**rationale**: rewrite `Database.lua:231-233` and `module-map.md:897` to drop the sentinel-bug reason (now
fixed upstream) and keep the "absent reads its default" reason. v6 is stamp-once, so no player is affected.
If the lead prefers deletion: drop the `type(...) == "boolean"` test, hand every `units.<unit>.<companion>`
path, and re-pin `test_skin_hud.lua:275` to whatever LK-07 writes into an absent bool.

### 1f. `Skin:__DrawsKey` or other internals (R-9 / LK-10): **none**

Proof: `git grep -n -E "__DrawsKey|DrawsKey|__Tokens|__Remap|__BaseTokens" -- '*.lua' ':!libs' ':!tests/_kit'` → no hits.
AT reaches only public members: `Skin:For/RegisterOwner/Skins/SetChoice/SetIgnore/GetIgnore/SetOverride/
PaintAce/PaintAceTree` (`AT/core/SkinSetup.lua:90-91,290-354`), `Skin.ResetToSkin` (`AT/core/Database.lua:235`),
and the facade's `Resolve/Token/OnLooksChanged` (`AT/core/Data.lua:149-152`, `AT/settings/Appearance.lua:145-146`,
`AT/core/SkinSetup.lua:301`). Tests read `Skin:GetIgnore/GetOverride/SetIgnore/SetOverride/SetChoice`
(`AT/tests/test_skin_hud.lua:141-164`). After LK-01 the `Skin:GetIgnore` call at `SkinSetup.lua:329` goes with 1a.

### 1g. Close-button tint handling (R-3 / LK-03): **none**

AT never calls `S.CloseButton`. Proof: `git grep -n "CloseButton" -- '*.lua' ':!libs' ':!tests/_kit'` → only the
degraded facade's vocabulary name (`AT/core/SkinSetup.lua:258`), the DebugLog stub `MakeCloseButton`
(`AT/core/DebugLogSetup.lua:76`) and history comments/tests about the DebugLog close mark
(`AT/core/PerfSetup.lua:119`, `AT/tests/test_coresetup.lua:55-112`, `AT/tests/test_perf.lua:472,598`).
No tint is saved or restored. Exceptions row candidate.

### 1h. Literal tooltip / quality colors (R-7 / LK-08, R-8 / LK-09): **none**

AT passes no colors in the drag-strip tooltip descriptors (`AT/modules/Bar.lua:150-187`: title/body/footer
strings only); the widget colors them, so LK-08 reaches AT's three strip tooltips with no AT change. AT has
no item-quality use. Proof:
`git grep -n -E "gtip|ITEM_QUALITY|GetItemQualityColor|q\.(poor|common|uncommon|rare|epic|legendary)" -- core modules settings` → no hits;
the only `|cff` literals are chat colors (`AT/core/DebugLogSetup.lua:65` ON/OFF, `AT/settings/Slash.lua:60`
mirrored note), not tooltip or quality colors. Exceptions row candidate.

### 1i. Degraded facade vocabulary (watch item, any LK that adds a facade name)

`AT/core/SkinSetup.lua:255-263` lists LibKa0s-Skin-1.0's VOCAB (`LK/LibKa0s/Skin.lua:107`) by hand, and
`AT/tests/test_surface_parity.lua:351-358` holds it to the live facade key for key. If v1.81.0 adds a facade
member (e.g. a public DrawsKey on the facade, or a new primitive for LK-05/06), AT-RV must add it to that list
or the parity test goes red. If LK-10's `DrawsKey` lives on the major only, nothing here moves.

## 2. Where AT resolves a HUD face itself

One place: `NS.MediaKey` (`AT/core/Data.lua:146-155`), through the `FOLLOWS` map `font = { "hud.font",
"fontFromSkin" }` (`AT/core/Data.lua:133-139`), consumed by `NS.GetFont` (`AT/core/Data.lua:195-197`), drawn at
`AT/modules/Display.lua:220` (appearance pass) and `AT/modules/Bar.lua:298` (build), reported by
`AT/modules/Diagnostics.lua:193-205`. It already calls `S.Resolve` (`:152`), so after LK-01 the library makes
the stored value win and AT keeps only the call (see 1a's decision point).

The **font picker's preview** is the library composer's, not AT's: the Text block is `H.FontGroup{ fromSkin = true }`
(`AT/settings/Appearance.lua:310-327`), whose `skinValue`/`disabledIf` live in `LK/LibKa0s/OptionsCompose.lua:515-534`
(`hud.font` at `:331`). LK-01 fixes the preview there; AT has nothing to change. AT's own `followsSkin`
(`AT/settings/Appearance.lua:141-149`) governs only `bgTexture` (`bar.texture`, `:237-251`) and `borderSize`
(`bar.borderSize`, `:303`), no font token.

Note for R-4 (LK-04): today `hud.font` under the eight non-Ka0s skins is Friz via SkinDefs' KEEP
(`LK/LibKa0s/SkinDefs.lua:525`; Ka0s Default's `hud.font` at `:307`). With `fontFromSkin` default on, every
non-Ka0s skin will change the bar number's face in AT once LK-04 lands; no code change, only docs/smoke (§4).

## 3. Tests that pin the current behaviour

| Test | Pins | After the release |
|---|---|---|
| `AT/tests/test_skin_hud.lua:137-166` "Ignore fonts keeps the value text on the stored face, over the skin and a font override" | the AT-side check; comment `:138-140` says "The library's Resolve/Token never read ignoreFonts ... so the addon checks it itself"; `:150` `fromSkin == false` while ignored | Keep the behaviour assertions (`:149-161`), rewrite the comment to name the library as the enforcer; `:150` depends on 1a's decision point. The "red under" note must name a check that still fails without LK-01 (e.g. run it against v1.80.0's payload) |
| `AT/tests/test_skin_hud.lua:110-135` "a companion on draws the skin's token; off, the stored pick" | font follows `hud.font` (`:115`) | unchanged under Ka0s Default |
| `AT/tests/test_skin_hud.lua:225-238` "a skin switch repaints every bar..." | `:236` MediaKey font == `S.Token("hud.font")` under **obsidian** (today Friz via KEEP on both sides) | still passes after LK-04 (both sides read the new face); no edit needed |
| `AT/tests/test_skin_hud.lua:254-278` "v6 puts every stored companion back on..." | `:275` "an absent companion stays absent: it reads on"; `:276` "no sentinel written into a pick" | holds if the filter is kept (1e) |
| `AT/tests/test_skin_hud.lua:280-288` "v6 runs once" | stamp-once | unchanged |
| `AT/tests/test_skin_picker.lua:213-223` "Skin picker: the title names this addon, and the eye is hidden" | `:221` `assertEqual(text, "Choose a skin for " .. NS.Constants.BRAND)` | **must change** (R-11): title `"Choose a skin"`, plus an assertion that the addon-name line above the dropdown reads `NS.Constants.BRAND` (field name from LK-11's API) and is not truncated. Rename the test ("the title is Choose a skin, the name line names this addon, and the eye is hidden"); `AT/docs/test-cases.md:904` lists the name |
| `AT/tests/test_surface_parity.lua:351-379` | degraded facade == live facade; seam NS members equal on both paths | goes red if only one `SkinFontsIgnored` arm is removed, or if v1.81.0 adds a facade name (1i) |
| `AT/tests/test_skinsetup.lua:189-235` (Ignore fonts reaches the library and the profile; whole apply; /at set reaches an exception) | SetIgnore plumbing, `Skin:GetIgnore` reads in tests | unchanged |
| `AT/tests/test_skin_tools.lua:83-106` | default Scope keeps the chrome block stock | unchanged unless LK-05/06 change AceGUI Scope rules |
| `AT/tests/test_draghandle.lua` | tooltip placement/owners only (`:298-307,555-585`); no color assertions | unchanged by LK-08 |

`AT/docs/test-cases.md` names to update if test titles change: `:886` (Ignore fonts case), `:904` (picker title case).

## 4. Smoke checks and doc passages whose expectation changes

### Smoke checks (`AT/docs/smoke-tests.md`)

| Check | Line | Change |
|---|---|---|
| **SKIN-5** Every skin on the bars | `:180` | "the number is Oxanium SemiBold on Ka0s Default and Friz Quadrata on the others (no other skin names a HUD face)" → each skin's own HUD face from LK-04 (list them per skin once DECISIONS.md fixes them). R-4 |
| **SKIN-17** First-run picker | `:192` | "a small window titled **Choose a skin for Ka0s Absorb Tracker**" → titled **Choose a skin**, with **Ka0s Absorb Tracker** on its own line above the dropdown, in full; "Fail: ... a title that does not name Ka0s Absorb Tracker" → fail on a cut-off name or a title other than "Choose a skin". R-11 |
| **SKIN-26** Ignore fonts reaches the bars | `:201` | Behaviour unchanged on the bars; add: while Ignore fonts is on, Appearance → Text → **Font** (grayed under *Use the skin's font*) shows your stored face, not the skin's (LK-01 composer preview). Optionally add one non-Ka0s skin so the check covers a skin whose HUD face now differs from Friz (R-4). R-1 |
| SKIN-25 CLI/diagnostics | `:200` | only if 1a's decision makes `skin=` read `yes` while Ignore fonts is on; then add that case |
| SKIN-9, SKIN-10 tool windows / drag strips | `:184-185` | only if LK-06 puts these under *Ignore settings panel* (§1d open dependency); SKIN-10 also: tooltip title/body in the skin's tooltip colors (LK-08) |
| SKIN-3 Ka0s Default elsewhere looks as before | `:178` | **no change** from R-2 (AT and the library pass no stockDefault, §1c); recheck only if LK-06 repaints a surface under Ka0s Default |
| Summary table row | `:17` | wording "the first-run picker" fine; update only if new checks are added |

### Docs

| Passage | Line | Change |
|---|---|---|
| `AT/docs/ARCHITECTURE.md` "The HUD bars" | `:351-354` | "The library's `Resolve`/`Token` never read the exception (only `P.font` does), so `NS.MediaKey` asks `NS.SkinFontsIgnored()` (`core/SkinSetup.lua`) itself." → the library's `Resolve` honours Ignore fonts for `hud.font` (LibKa0s v1.81.0), so `NS.MediaKey` needs no check of its own |
| `AT/docs/ARCHITECTURE.md` drag strips / library surfaces | `:366-370` | per LK-06's Scope semantics (§1d) |
| `AT/docs/module-map.md` 7c row (core/SkinSetup.lua) | `:892` | drop "**`NS.SkinFontsIgnored()`** answers the applied *Ignore fonts* (`Skin:GetIgnore`; false without the library), which `NS.MediaKey` reads because the library's `Resolve`/`Token` do not"; update the line count (361) |
| `AT/docs/module-map.md` row 8 (core/Data.lua) | `:895` | line count (383) and any MediaKey/Ignore-fonts wording |
| `AT/docs/module-map.md` row 10 (core/Database.lua) | `:897` | the `"@skin"` sentinel rationale (§1e) |
| `AT/docs/module-map.md` libs row | `:1010` | "v1.78.0 to v1.80.0 payloads" → v1.81.0 |
| `AT/docs/settings-panel.md` first-run picker | `:356-357` | "a small `DIALOG` window titled *Choose a skin for Ka0s Absorb Tracker*" → titled *Choose a skin*, the addon's name above the dropdown |
| `AT/docs/settings-panel.md` Scope paragraph | `:345-347` | per §1d |
| `AT/docs/schema.md` `skin.ignoreFonts` | `:441` | "every font keeps the face the addon set" → add "the HUD bars' number included: it draws the unit's stored Font over the skin's" (R-1 now library-enforced) |
| `AT/docs/schema.md` `fontFromSkin` | `:472` | add "unless Ignore fonts is on" |
| `AT/core/SkinSetup.lua` header | `:19-21` | delete with 1a |
| `AT/core/Data.lua` comment | `:143-145` | rewrite with 1a |
| `AT/core/Database.lua` comment | `:229-233` | rewrite with 1e |
| `AT/README.md` FAQ / Credits | `:86`, `:145-155` | FAQ fine. Credits list "Seven more SIL OFL faces, one family per skin" (`:147-154`): extend only if LK-04 ships a face not already listed |
| `AT/docs/testing.md` | — | no skin passage; `git grep -n -i skin docs/testing.md` → no hits. Nothing to change |
| `AT/CLAUDE.md` | `:46` | provenance v1.80.0 → v1.81.0 at AT-RV |

The Skin tab label (R-10) is already "Skin" in AT's docs (`AT/docs/settings-panel.md:336` "`Appearance` and
labeled *Skin*"); the key `"Appearance"` in `AT/core/SkinSetup.lua:192-194` is the library's tab key and stays.

## 6. Nothing to change (exceptions.tsv candidates)

| Ruling | Claim | Proof command (run in `AT/`) |
|---|---|---|
| R-1 outline | AT resolves no HUD outline | `git grep -n "hud.outline" -- '*.lua' ':!libs' ':!tests/_kit' \| grep -v "^core/Data.lua:193:"` → empty |
| R-2 | no stockDefault / stock caller | `git grep -n -E "stockDefault\|stock *=" -- '*.lua' ':!libs' ':!tests/_kit'` → empty |
| R-3 | no S.CloseButton tint handling | `git grep -n -E "S\.CloseButton\|:CloseButton\|SetVertexColor" -- core modules settings` → empty |
| R-5 | no S.Text / WidgetsReorder / hand-rolled Scope guard | `git grep -n -E "S\.Text\|Reorder\|GetIgnore" -- core modules settings \| grep -v "^core/SkinSetup.lua:\(19\|32[89]\):"` → empty (the GetIgnore at `:19,:328-329` is 1a's, removed by AT-01; after AT-01 the bare command is empty) |
| R-7 | no literal tooltip colors | `git grep -n -E "gtip\|SetTextColor" -- modules/Bar.lua` → empty |
| R-8 | no quality colors | `git grep -n -E "ITEM_QUALITY\|GetItemQualityColor\|q\.(poor\|common\|uncommon\|rare\|epic\|legendary)" -- core modules settings` → empty |
| R-9 | no internal reach-in | `git grep -n -E "__DrawsKey\|DrawsKey\|__Tokens" -- '*.lua' ':!libs' ':!tests/_kit'` → empty |

## Summary of AT work

- **AT-RV**: re-vendor v1.81.0; `CLAUDE.md:46`, `docs/module-map.md:1010`; extend the degraded VOCAB list
  (`core/SkinSetup.lua:255-263`) if the facade grows.
- **AT-01**: delete `core/Data.lua:148` and `NS.SkinFontsIgnored` (both arms, `core/SkinSetup.lua:280` and
  `:325-331`, header `:19-21`); settle the `skin=` reporting decision (1a); re-word `core/Database.lua:229-233`
  (keep the filter); move `tests/test_skin_hud.lua:137-166` and `tests/test_skin_picker.lua:213-223`.
- **AT-02**: smoke SKIN-5, SKIN-17, SKIN-26 (+ SKIN-9/10/25 conditionally); ARCHITECTURE `:351-354`,
  module-map `:892,:895,:897`, settings-panel `:356-357`, schema `:441,:472`, test-cases `:886,:904`.
