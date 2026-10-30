# M0 inventory: DpsRace (prefix DR)

Read-only, 2026-10-30. Repo `/mnt/d/Profile/Users/Tushar/Documents/GIT/DpsRace` at master `4816414`. All paths are
relative to that repo unless prefixed `LibKa0s/` (that is `../LibKa0s/LibKa0s/`, master `ea1d92d`). `libs/` and
`tests/_kit/` were excluded from the search.

DpsRace is named in none of the rollout's nine follow-ups (`99_REPORT.md` "Library follow-ups"), and it carries
**no hand-rolled workaround** for R-1, R-3, R-5, R-6's sentinel *write*, R-7, R-8 or R-9. It has one `stockDefault`
caller (R-2) and one ResetToSkin guard (R-6). Its HUD face reaches the library through `S.Resolve`, so LK-01 fixes
it with no addon code. The work for DR-01 and DR-02 is therefore mostly tests and docs.

---

## 5. Current state (run first)

| Item | Value | Evidence |
|---|---|---|
| Branch | `master`, tracking `origin/master`, in sync | `git status -sb` → `## master...origin/master` |
| Tree | clean: 0 porcelain lines, 0 stashes, one worktree (the main one) | `git status --porcelain \| wc -l` → 0; `git stash list` empty; `git worktree list` |
| HEAD | `4816414 Merge feat/2026-10-29-skinning-rollout` | `git log --oneline -1` |
| Vendored LibKa0s | **v1.80.0** | CLAUDE.md:43 `Bundles [LibKa0s](...) v1.80.0 (MIT).`; icon declaration at CLAUDE.md:44 |
| Tests | `1145 passed, 0 failed, 1 skipped, 1146 total` (exit 0) | `~/.claude/dev-copilot/bin/ka0s-bounded lua tests/run.lua` |
| luacheck | `Total: 0 warnings / 0 errors in 148 files` (exit 0) | `~/.claude/dev-copilot/bin/ka0s-bounded luacheck .` |
| 1500-line cap | holds. Largest: tests/test_hud.lua 1478, tests/test_results.lua 1475, modules/Results_Timeline.lua 1449 | `wc -l` over tracked .lua outside libs/ and tests/_kit/ |

**Gate green on master: yes.**

Cap warning for the implementer: test_hud.lua (22 lines left) and test_results.lua (25 left) are almost full.
Put any new test in `tests/test_skin.lua` / `tests/test_skin_hud.lua`, not in those two.

### Release pins that move with DR-RV (v1.80.0 → v1.81.0)

- CLAUDE.md:43, the provenance line. The re-vendor rolls it.
- docs/ARCHITECTURE.md:21 "the vendored `LibKa0s` v1.80.0".
- docs/debug.md:95 "`DIAG_MAX_LINES` (1200 in the vendored v1.80.0)". Re-check the value in v1.81.0.
- Leave alone, because they are history: docs/ARCHITECTURE.md:134 ("re-vendored LibKa0s v1.80.0", the rollout
  narrative) and docs/smoke-tests.md:21 (the rollout's pending-sign-off header). The next run's rows get a new
  header beside it.
- DEPENDENCIES.md names no LibKa0s version (DEPENDENCIES.md:75 only), so nothing changes there.
- tests/test_vendor_sync.lua holds libs/ and tests/_kit/ to the tag CLAUDE.md names. It follows the provenance
  line and has no literal of its own to move.

---

## 1. Workarounds of library gaps the release closes

### R-2 / LK-02: `stockDefault` and `stock` callers (one; it goes)

| Site | What |
|---|---|
| modules/Hud_States.lua:492-493 | `-- No box under Ka0s Default (stockDefault), as before the skin engine; another skin draws its input.` / `NS.Skin.EditBox(w.customBox, { padInput = false, stockDefault = true })`. This is the idle body's custom race-length box (Builders.idle, created at :489-498, `BackdropTemplate`, `FONT.TEXT` at :491). |

There are no `opts.stock` callers. `git grep -n -e 'stock *=' -- . ':(exclude)libs' ':(exclude)tests/_kit'` finds
nothing in code. The only other hits are prose: docs/known-limitations.md:56 ("the stock one", meaning the Runs
view), which is unrelated.

**What the surface looks like under Ka0s Default afterwards.** The box gets `S.EditBox`'s full paint
(LibKa0s/SkinPaintControls.lua:218-235):

- the flat input box: fill `input.bg` (`CTL_FILL`) and a 1px edge `input.border` (`CTL_LINE`)
  (LibKa0s/SkinDefs.lua:251-252);
- the edge turns `input.focus` gold `{1, 0.82, 0, 0.9}` while the box has the keys (focus hooks at :232-233);
- the typed text in `input.text` = `BODY` (SkinDefs.lua:356) and the skin's body face (`P.font(..., "body")`,
  :227), which is Oxanium SemiBold under Ka0s Default, replacing GameFontHighlightSmall's Friz;
- `padInput = false` stays, so there are no 6px insets.

In short, it matches the note box (`modules/Results_Detail.lua:556`, `NS.Skin.EditBox(w.noteBox)`, D-14: an edge
at rest and gold only while typing), apart from the insets. DR-01 deletes `stockDefault = true` and rewrites the
comment at :492. Keep `{ padInput = false }`: the box is narrow and centered (`SetJustifyH("CENTER")` at :494,
`SetMaxLetters(6)` at :495). Check at the HUD's minimum width (260 px) that six digits still fit with the wider
Oxanium face.

### R-6 / LK-07: ResetToSkin guard (the v6 migration)

| Site | What |
|---|---|
| core/Database.lua:49-53 | The comment: "ResetToSkin, handed a key that is absent, cannot tell it is a bool and writes its "@skin" sentinel into it." |
| core/Database.lua:54-73 | Migration step `to = 6` (per profile). It walks `HudAppearance.FROM_SKIN_KEYS` (modules/Hud_Appearance.lua:46-55) and names only a companion that is **stored as a boolean and not already true** (`type(t[leaf]) == "boolean" and t[leaf] ~= true`, :64). It then calls `resetToSkin(profile, keys)` (:69). With no library it sets `t[leaf] = true` itself (:66). |

The guard does two jobs:

1. It dodges the sentinel bug, which is R-6, the part LK-07 fixes.
2. It keeps DpsRace's own documented rule that an absent companion stays absent, because its default is on.
   schema.md:116 states that rule ("An absent companion is left absent (its default is on)"), and so does
   tests/test_skin_hud.lua:191.

**Recommendation for DR-01: do not change the step's code.** Under LK-07 the filter still matters for job 2.
v6 is a schema step that already ran on every upgraded install, and the runner still replays it for a v5
SavedVariables. The only change is to reword core/Database.lua:49-53, so the comment stops claiming the library
writes `"@skin"` (from v1.81.0 it does not) and keeps the "absent stays absent, its default is on" reason. If
the lead prefers no edit at all, this becomes an `exceptions.tsv` row: the proof is
`git grep -n 'type(t\[leaf\]) == "boolean"' core/Database.lua` → :64, plus test_skin_hud.lua:190-191 still green
after DR-RV.

### R-1 / LK-01: own Ignore-fonts handling for HUD faces or outlines: **none**

DpsRace has no `NS.SkinFontsIgnored`-style patch.

- `git grep -n -e 'FontsIgnored\|IgnoreFonts\|fontsIgnored\|GetIgnore' -- core modules settings` returns nothing.
- The only `ignoreFonts` code is the store and seam plumbing: core/SkinSetup.lua:71, :328, :347, :538;
  settings/General.lua:175-176; defaults/Profile.lua:140.

DpsRace never reads `hud.outline` or `hud.fontSize`. `git grep -n 'hud\.\(outline\|fontSize\)' -- core modules
settings tests ':(exclude)tests/_kit'` returns nothing. The HUD's flags and sizes are always the player's own
(`fontFlags`, `fontSize` in Hud_Appearance.lua:121-126; X4, D-6). So the outline half of R-1 has no surface in
DpsRace.

### R-3 / LK-03: close-button tint handling: **none**

- Every close control goes through the one wrapper `NS.MakeCloseButton` (core/CoreSetup.lua:104-108, which wraps
  `lib.MakeCloseButton(parent, onClick, addonName)` → `S.CloseButton`). Callers: modules/Hud.lua:426,
  modules/Results.lua:199, modules/Results_Gear.lua:279, modules/Results_Timeline.lua:499.
- DpsRace saves and restores no tint, and never passes `stockDefault` to a close.
- The library's own CloseButton calls `P.stockDefault(owner, rec, btn)` with no opts
  (LibKa0s/SkinPaintControls.lua:582), so DpsRace's closes are always painted.
- The tests pin only `close.rest` / `close.hot` and "not the strip's gold": tests/test_hud.lua:1373-1378 and
  tests/test_results.lua:1463-1468. LK-03 changes neither.

Exception proof: `git grep -n 'SetVertexColor\|GetVertexColor' -- core/CoreSetup.lua` → nothing.

### R-5 / LK-05, LK-06: hand-rolled Scope guards around S.Text, WidgetsReorder or other widgets: **none**

- `git grep -n 'Reorder\|DragHandle\|Autocomplete\|LineChart\|__PanelSkinned\|ignorePanel' -- core modules
  settings` shows only the store rows (core/SkinSetup.lua:71, :327; settings/General.lua:171-172).
- No WidgetsReorder, DragHandle, Autocomplete or LineChart is used. Insights charts are DpsRace's own
  (modules/Results_InsightsCharts.lua).
- `S.Text` is used only on DpsRace's own windows, never on the settings panel: `NS.Skin.Text(fs, role)` at
  modules/Style.lua:271, reached through Style.Paint/Style.Text (:266-311). The "Ignore settings panel" Scope
  has nothing to guard there, and Ignore fonts is already honoured by the library's `P.font`
  (LibKa0s/SkinPaint.lua:539 → `P.unfont`).
- The library custom widgets DpsRace uses, all handed this addon as owner, none with a skin or Scope guard of
  its own:
  - the CopyWindow: core/WidgetsSetup.lua:67-77, `addonName = addonName`;
  - the dropdown factory and test strip: core/WidgetsSetup.lua:34 (`owner = addonName`) and :54 (`W.TestStrip`,
    `owner = addonName`);
  - the toast: core/ToastSetup.lua:34-37 (`d.owner = d.owner or addonName`; modules/BestToast.lua:200);
  - the debug console: core/DebugLogSetup.lua:58-62 (`name`, `addonName`, and an explicit
    `font = NS.Constants.FONT_MONO`);
  - the perf panel: core/PerfSetup.lua:22-24, :47;
  - the launcher: core/LauncherSetup.lua:87.

**Conditional, M1 decides.** If LK-06 adds a required option to any of these constructors (an `owner` where
today the library derives it from `addonName`), it lands in "What a consumer owes" and DR-01 wires it at the
lines above. If LK-05 or LK-06 adds names to the facade's `VOCAB` (a new primitive), the degraded facade's name
list at core/SkinSetup.lua:467-475 must grow too. tests/test_skinsetup.lua:346-357 ("the degraded facade answers
every name the live facade carries", through `T.assertSurfaceParity`) goes red until it does. The same applies if
LK-10 puts `DrawsKey` on the facade (`fillFacade`, LibKa0s/Skin.lua:1012-1026) and not only on `lib`.

### R-9 / LK-10: reach into `Skin:__DrawsKey` or other Skin internals: **none**

- `git grep -nE '(Skin|SkinLib|lib|S)[:.]__[A-Za-z]' -- core modules settings` → only
  settings/OptionsSetup.lua:139 `lib.__PatchLSM30Border()` (LibKa0s-Options, not Skin; outside R-9) and the two
  host test seams core/Database.lua:75 and settings/Schema.lua:111.
- The one other Skin-lib call is `SkinLib:Untrack(fs)` at modules/Style.lua:289, a public method
  (LibKa0s/Skin.lua:949).

### R-7 / R-8: literal tooltip or quality colors standing in for `gtip.*` / `q.*`

**Quality (`q.*`): none.** `NS.QualityColor` (core/SkinSetup.lua:271-287) reads the skin's `q.poor..q.legendary`
first (`QUALITY_TOKEN`, :273), then `ITEM_QUALITY_COLORS`. Its callers:

- modules/Results_Gear.lua:248-258 and modules/Results_Loadout.lua:159-168 also try `C_Item.GetItemQualityColor`,
  then fall back to `C.dim`;
- no q literal anywhere: `git grep -n 'q\.[a-z]' -- core modules settings` → only core/SkinSetup.lua:271, :273.

LK-09's exact values flow through with no addon change. The only test, tests/test_loadout.lua:344-345, compares
against `NS.QualityColor(4)` dynamically, so it survives R-8.

**Tooltip lines: a pre-existing gap DpsRace owns (not a library workaround).** The HUD's own tooltips already
read `gtip.*`:

- modules/Hud_States.lua:196-197, :314;
- modules/Style.lua:364, :446;
- modules/Results_Table.lua:232, :248, :264, :652-653;
- modules/Results_Gear.lua:386, modules/Results_Loadout.lua:243, modules/Results_Timeline.lua:558,
  modules/Results_InsightsCharts.lua:817.

Several Results tooltip **lines** still carry literal colors as `{ text, r, g, b }` tables, which
`Style.AddTipLines` passes straight to `AddLine` (modules/Style.lua:362-369). tests/test_skin_literals.lua does
not catch them, because it scans call arguments and `|cff` only (:5-15, :36-40), not table constructors. Under a
non-Ka0s skin these lines stay Ka0s gold and gray, which contradicts SM-DR-SK13 ("The tooltip lines DPS Race
writes take Ember's colors"). Two groups:

- The gold `{.., 1, 0.82, 0}` (= `gtip.title`'s Ka0s Default value, core/SkinSetup.lua:92):
  modules/Results_Timeline.lua:414; modules/Results_Tips.lua:376, :490, :579, :718.
- The dim gray `{.., 0.62, 0.62, 0.68}` (= `dr.dim`'s default, core/SkinSetup.lua:211):
  modules/Results_Tips.lua:49, :147, :167, :197, :231 (`dimLine`); modules/Results_Timeline.lua:412, :858;
  modules/Results_Usage.lua:295.

No ruling covers this. R-7 is the library's DragHandle. It is in this inventory's "literal tooltip colors"
bucket, so the lead should decide whether DR-01 folds it in or files it as an addon issue:

- The fix is `Style.Tok("gtip.title")` and `Style.Tok("dr.dim")` (a live table carries `[1..3]`, so
  `{ text, c[1], c[2], c[3] }` or a helper).
- It keeps Ka0s Default byte-identical.
- The only test literal is a test input, tests/test_tooltips.lua:43 (`{ "Hint", 0.62, 0.62, 0.68 }`), not an
  assertion.
- Other literal tables that are deliberately data, chart or art (rung 4, D-11) are **not** tooltip colors:
  - modules/Countdown.lua:47 (`GOLD`, the countdown art's fallback, D-11);
  - modules/Results_InsightsCharts.lua:91-96 (`DEFAULT_COLORS`, the chart host's fallback for a missing token);
  - modules/Results_Compare.lua:55-56 and modules/Results_Timeline.lua:161, :165 (data hues and corridors);
  - modules/Hud_Chart.lua:94 (a texcoord).

---

## 2. Where DpsRace resolves a HUD face or outline itself

There is one resolver, and it goes **through the library**: `HudAppearance.MediaKey`, modules/Hud_Appearance.lua:92-107.

```lua
local stored = setting(p .. leaf)
local token, S = FOLLOWS[leaf], NS.Skin
if token and S and type(S.Resolve) == "function" then
    local on = setting(p .. leaf .. "FromSkin") == true
    local v = S.Resolve(token, stored, on)
    if type(v) == "string" and v ~= "" then return v, on end
end
return stored, false
```

- `FOLLOWS = { font = "hud.font", barTexture = "bar.texture" }` at :42. It is consumed by `FontAt` (:117-130,
  the face) and `BarAt` (:156-164, the texture).
- Font blocks that follow (`FROM_SKIN_KEYS`, :46-55): `appearance.figures`, `appearance.spellText` and
  `resultsTable.barText`. The two clocks (`appearance.elapsed`, `.left`) have no companion and use their stored
  face (D-15).
- Today `S.Resolve` returns `lib:Token(owner, "hud.font")` whenever `fromSkin` is true, whatever Ignore fonts
  says (LibKa0s/Skin.lua:868-871). LK-01 makes it return `stored` while the owner ignores fonts. **MediaKey then
  draws the stored face with no code change.**

Three things in DpsRace still need DR-01's attention:

1. **MediaKey's second return.** It answers `v, on` (:104). Under Ignore fonts with the companion on it would
   return the stored name with `on == true`, which reads as "true when it is the skin's" (doc comment :92-94). The
   only reader is tests/test_skin_hud.lua:93-99. Production callers drop it (:118, :160). Choose one:
   - return `v, on and v ~= stored`; or
   - reword the doc at :92-94 to "the companion's state".

   Either way, the test at test_skin_hud.lua:87-102 needs an Ignore-fonts case.
2. **The texture half must not move.** LK-01 is fonts only. `bar.texture` through the same `S.Resolve` must keep
   following the skin under Ignore fonts. Pin it with a test.
3. **The bare big texts (STOP, the result card's figures).** `monoFace()` reads `NS.Skin.Token("font.mono")`
   (modules/Hud_States.lua:136-161). That is not a HUD face in R-1's sense, and it is the same value under every
   source:
   - `font.mono` = "JetBrains Mono" only in Ka0s Default (LibKa0s/SkinDefs.lua:213);
   - every Ka0s skin overlays Ka0s Default (LibKa0s/Skin.lua:226-228);
   - EllesmereUI's table starts from it too (LibKa0s/SkinEUI.lua:323), and the Font override never touches it
     (LibKa0s/Skin.lua:727).

   So Ignore fonts changes nothing visible there. **No change**, unless LK-01 extends Ignore fonts to
   `font.mono`, in which case these labels fall back to `NS.Constants.FONT_MONO` (:144), the same face.

The HUD Appearance tab's pickers are the library's composer (settings/Hud.lua:111-173 and
settings/History.lua:94-98, `fromSkin = true`). LK-01's "the picker previews the stored face while Ignore fonts is
on" needs no DpsRace code.

The labels painted through `Style.Paint` → `S.Text` (modules/Style.lua:266-277) already give the face back under
Ignore fonts (library `P.font`). `Style.Hue` → `S.Font` (:287-294) and `NS.Skin.Font(fs)` at
modules/Results_Timeline.lua:568 do too.

---

## 3. Tests that pin current behaviour

| Test | Pins | After the release |
|---|---|---|
| tests/test_skin.lua:237-246 "skin: the custom-length box draws no box under Ka0s Default and the skin's box under another" | `M.__paint(box).backdrop == nil` under Ka0s Default (:241, :245), a box under another skin (:243) | **Moves (R-2).** Ka0s Default now draws the box: assert the backdrop exists under both, and the `input.border` edge under Ka0s Default. Rename it (e.g. "...draws the skin's input box under every skin, Ka0s Default included"). Update docs/test-cases.md:1083 and docs/testing.md:115 ("the custom-length box unboxed under Ka0s Default and boxed under another skin"). |
| tests/test_skin_hud.lua:87-102 "a companion on draws the skin's face or texture, off the stored pick, never rewritten" | `MediaKey` = `Token(hud.font)` and `on == true` while the companion is on | Still green (Ignore fonts off). **Add** a case: `Skin:SetIgnore(OWNER, nil, true)` (or `NS.SetByPath("skin.ignoreFonts", true)`), then every `font` block returns its stored face and every `barTexture` block still the skin's. Settle the second return's meaning (§2.1). |
| tests/test_skin_hud.lua:104-122 Oxanium under Ka0s Default; :124-131 the Results table cells (D-16) | `A.Font(...).path` = LSM fetch of `Token("hud.font")` | Unchanged under Ka0s Default. A new Ignore-fonts assertion fits here or in the case above: `A.Font("figures").path` = the stored "Friz Quadrata TT" path. |
| tests/test_skin_hud.lua:133-153 "a skin switch restyles the blocks and moves the face, never a color" | `otherSkin(Skin, "hud.font")` (:35-41) finds a skin whose `hud.font` differs, else falls back to `bar.texture` (:138) | Still green. Today every non-Ka0s skin's `hud.font` is Friz (`KEEP`, LibKa0s/SkinDefs.lua:525), which differs from Oxanium, so the first skin found moves the face. After R-4 each skin has its own face. Optional: tighten to "two non-Ka0s skins differ" to pin R-4 from the consumer side. |
| tests/test_skin_hud.lua:167-193 the v6 step | :190 "no sentinel in a pick"; :191 an absent companion stays absent | Stays green under LK-07 only while core/Database.lua:64's filter stays (§1, R-6). If DR-01 drops the filter, :191 must change. |
| tests/test_skinsetup.lua:278-288 "the tab's Ignore fonts reaches the library and the profile, one repaint" | `GetIgnore` moves, profile written, `counts.looks == 1` | Unchanged. Optional: assert `HudAppearance.stamp` moved, so the HUD restyles live on the toggle (Style.lua:106-110 → `HudAppearance.Changed`). |
| tests/test_skinsetup.lua:346-357 degraded-facade parity | the degraded `S` (core/SkinSetup.lua:463-494) carries every live facade name | Goes red if v1.81.0 adds a facade name (§1, R-5 conditional). |
| tests/test_skinsetup.lua:359-375 host copy = library Ka0s Default | each `NS.SKIN_FALLBACK` entry (core/SkinSetup.lua:79-109) | Unaffected by R-8: no `q.*` in the copy. Re-run after DR-RV in case another Ka0s Default value moved. |
| tests/test_skin_picker.lua:51-65 the spec | `spec.tab == "Appearance"` (:60), "the Skin tab's key" | Unchanged unless the library renames the tab **key**. R-10 renames the standard's wording. The library already labels the tab "Skin" (settings-panel.md:90). If LK-xx changes `O.AppearanceTab().key`, then core/SkinSetup.lua:399-401, this test and settings-panel.md:90 move together. |
| tests/test_skin_picker.lua (12 tests) | nothing about the title or the label line: `git grep -n 'Choose a skin' tests` → nothing | R-11 needs no test change in DpsRace. The library's own suites pin it. |
| tests/test_hud.lua:1373-1378, tests/test_results.lua:1463-1468 | the close control is `close.rest` / `close.hot`, never the strip's gold | Unchanged by R-3. |
| tests/test_loadout.lua:344-345 | the epic name colored `NS.QualityColor(4)` | Unchanged by R-8 (it compares dynamically). |
| tests/test_skin_literals.lua:132-147 | the literal gate's allow-list (:42-51) | Unchanged. If the tooltip-line literals (§1, R-7) are converted, consider widening `scan` to catch `{ text, n, n, n }` line tables, so the gap stays closed. |

---

## 4. Smoke checks and doc passages whose expectation changes

### docs/smoke-tests.md (section 27, SM-DR-SK*)

| Row | Line | Today | After |
|---|---|---|---|
| SM-DR-SK1 | :631 | "a small window *Choose a skin for Ka0s DPS Race* shows" | **R-11:** the title reads *Choose a skin*; *Ka0s DPS Race* (`NS.BRAND`, core/Namespace.lua:11) sits on its own line above the skin dropdown, not cut off. |
| SM-DR-SK4 | :634 | Ka0s Default "looks as it did before the build ... with these changes only: ..." | **R-2:** add "the idle HUD's *Custom* length box shows the skin's input box (dark fill, thin edge, gold while typing) where it showed none". |
| SM-DR-SK9 | :639 | "switching to Ember moves only their face, never the color or size" | **R-4:** the face moves for real now. Azeroth and Ember both draw Friz today (`KEEP`), so the expected face change does not happen today. Name the two HUD faces once LK-04 picks them. |
| SM-DR-SK10 | :640 | "*Ignore fonts* puts every string back in the face it was given ... and wins over the font override" | **R-1:** say it explicitly for the HUD: with *Ignore fonts* on, the live figures, the spell text and the Results bars' text draw each block's own *Font* (Friz Quadrata in a default profile), even with *Use the skin's font* ticked; bar textures still follow the skin. The HUD Appearance *Font* picker previews that stored face. |
| SM-DR-SK15 | :645 | each skin's body and title face | **R-4:** add a HUD row, or extend this one: under each skin the HUD's figures and spell text draw that skin's own `hud.font` (the faces LK-04 picks, recorded in DECISIONS.md). No Friz fallback except where a skin picks it (WoW Default). |
| SM-DR-SK12 | :642 | the console, Copy, perf panel, test strip, talent Copy window, dropdown menu and toast wear the skin | **Conditional on LK-06:** if the custom widgets now obey Ignore fonts, add "with *Ignore fonts* on each keeps its own face". The debug console passes its own `FONT_MONO` (core/DebugLogSetup.lua:61). |
| SM-DR-SK2 | :632 | Ka0s Default HUD faces | No change (Ka0s Default keeps Oxanium; Ignore fonts is off by default, defaults/Profile.lua:140). |
| SM-DR-SK11 | :641 | Ignore settings panel | No change: the Scope stays, default on (R-2 note), and DpsRace draws no S.Text or WidgetsReorder on its panel. |

The new sign-off header goes beside docs/smoke-tests.md:21-23: "Rows for the skin library follow-ups (LibKa0s
v1.81.0, branch `feat/2026-10-30-skin-library-followups`) ...".

### Docs

| Doc | Line | Change |
|---|---|---|
| docs/ARCHITECTURE.md | :412-413 | "the idle body's custom-length box `S.EditBox` with `stockDefault` (no box under Ka0s Default, as before the skin engine; another skin draws its input)" → the skin's input box under every skin (R-2). |
| docs/ARCHITECTURE.md | :416-421 (HUD style) | "draw the skin's `hud.font` or `bar.texture` through `HudAppearance.MediaKey` while it is on" → add "unless the Scope's *Ignore fonts* is on, which makes a face block draw its stored *Font* (the texture still follows)" (R-1). |
| docs/ARCHITECTURE.md | :21 | v1.80.0 → v1.81.0 (DR-RV). |
| docs/settings-panel.md | :104 | *Ignore fonts* row: "every string keeps its own face and size" → add "the HUD Appearance and Results table blocks draw their own *Font* even with *Use the skin's font* on". |
| docs/settings-panel.md | :242-246 | "On, the block draws the skin's `hud.font` ..." → add the Ignore-fonts exception (R-1). Optionally a line that each skin has its own HUD face (R-4). |
| docs/settings-panel.md | :90 | "its key is `Appearance`, its label *Skin*": no change unless the key changes (R-10 note above). |
| docs/schema.md | :60, :61 | "While `fontFromSkin` is on the block draws the skin's `hud.font`" → "... unless `skin.ignoreFonts`" (R-1). |
| docs/schema.md | :68 | `skin.ignoreFonts`: add that it reaches the HUD and Results table face blocks (R-1). |
| docs/schema.md | :116 | the 5 → 6 row: no behaviour change. If core/Database.lua:49-53 is reworded, keep this row consistent ("An absent companion is left absent" stays true). |
| docs/module-map.md | :61 | `MediaKey(prefix, leaf)` "(the skin's `hud.font` or `bar.texture` through `NS.Skin.Resolve` while the block's companion is on, else the stored pick)" → add "and, for a face, Ignore fonts off" (R-1). |
| docs/testing.md | :115 (`test_skin`) | "the custom-length box unboxed under Ka0s Default and boxed under another skin" → boxed under every skin (R-2). |
| docs/testing.md | :116 (`test_skin_hud`) | add "Ignore fonts giving each face block its stored face, the texture still the skin's" (R-1). |
| docs/test-cases.md | :1083, and the test_skin_hud block (:1089 area) plus the counts table (:1427 area) | the renamed or added test names and the per-file counts. |
| README.md | :34 | "The HUD's fonts and bar textures follow the skin too, unless you untick *Use the skin's font* or *Use the skin's texture* on a block" → add "or tick *Ignore fonts*, which keeps the HUD's own fonts too" (R-1). The README never quotes the picker's title, so R-11 needs nothing there. |
| modules/Hud_Appearance.lua | :12-20 header and :92-97 MediaKey doc | code comments: add the Ignore-fonts case (R-1) and the second return's meaning (§2.1). |
| modules/Hud_States.lua | :492 | comment, deleted or rewritten with the `stockDefault` (R-2). |
| core/Database.lua | :49-53 | comment: no sentinel from v1.81.0 (R-6). |
| locales/enUS.lua | :1057-1058 | *Ignore fonts* tooltip, "Keep every font in this addon as the game draws it. The skin still colors the text." Still true under R-1; optional wording only. |

No doc mentions an Ignore-fonts limitation for the HUD. `grep -n 'Ignore fonts' docs/known-limitations.md` returns
nothing, so there is nothing to retire there.

---

## 6. Nothing to change (exceptions.tsv candidates, each with its proof)

| Ruling / item | Proof command (run in the DpsRace repo) | Expected |
|---|---|---|
| R-1 own HUD Ignore-fonts patch (DR-01 part) | `git grep -n -e 'FontsIgnored' -e 'GetIgnore' -e 'hud\.outline' -- core modules settings` | no output |
| R-3 close tint handling | `git grep -n -e 'SetVertexColor' -e 'GetVertexColor' -- core/CoreSetup.lua` | no output |
| R-5 Scope guards around S.Text / WidgetsReorder | `git grep -n -e 'Reorder' -e '__PanelSkinned' -e 'GetIgnore' -- core modules settings` | no output |
| R-6 sentinel write (code) | only the comment and the filter, kept by design (§1): `git grep -n '"@skin"' -- core modules settings` | core/Database.lua:51 (comment), core/SkinSetup.lua:463 (the degraded facade's `FROM_SKIN` constant, which mirrors the library's) |
| R-7 DragHandle tooltip | `git grep -n 'DragHandle' -- core modules settings` | no output |
| R-8 q.* literals | `git grep -n 'q\.[a-z]' -- core modules settings` | core/SkinSetup.lua:271 and :273 only (token names, no values) |
| R-9 `__DrawsKey` | `git grep -n 'DrawsKey' -- . ':(exclude)libs' ':(exclude)tests/_kit'` | no output |
| R-11 picker title (addon side) | `git grep -n 'Choose a skin' -- core modules settings tests locales` | no output (the title is the library's, LibKa0s/OptionsSkinPicker.lua:106) |

Smoke-row and doc changes for R-11 (SK1), R-1 (SK10) and R-4 (SK9, SK15) are still owed under DR-02, even where
the code has nothing to do.

---

## Item summary for the lead

- **DR-RV:** re-vendor v1.81.0. Roll CLAUDE.md:43, ARCHITECTURE.md:21 and debug.md:95. If facade names were
  added, extend the degraded name list at core/SkinSetup.lua:467-475 (test_skinsetup.lua:346).
- **DR-01:**
  - delete `stockDefault = true` at modules/Hud_States.lua:493 and fix test_skin.lua:237-246;
  - settle MediaKey's second return (modules/Hud_Appearance.lua:92-107) and add the Ignore-fonts test
    (test_skin_hud.lua);
  - reword core/Database.lua:49-53, keeping the filter at :64.
  - Lead's call: convert the 13 literal tooltip-line colors (§1, R-7) to `gtip.title` / `dr.dim`.
- **DR-02:** smoke SK1, SK4, SK9, SK10, SK15 (and SK12 if LK-06 reaches Ignore fonts), plus a new pending-sign-off
  header; the docs table in §4.
