# M0 inventory: DropWatcher (DW)

Read-only inventory, 2026-10-30. Repo `../DropWatcher` at `master` 8851923, clean. Paths are relative to
`../DropWatcher` unless they say otherwise; `libs/` and `tests/_kit/` were read only for reference. Library
paths are `../LibKa0s/LibKa0s/...` (the working tree, the same code DW vendors at v1.80.0).

## 5. Current state (asked last, put first)

| What | Value |
|---|---|
| Branch | `master` (HEAD `8851923 Merge feat/2026-10-29-skinning-rollout`) |
| Tree | clean (`git status --short` prints nothing) |
| Provenance line | `CLAUDE.md:44` `Bundles [LibKa0s](...) v1.80.0 (MIT).`; icon declaration `CLAUDE.md:45` |
| Other v1.80.0 pins (roll at DW-RV) | `core/SkinSetup.lua:9`, `docs/ARCHITECTURE.md:14`, `docs/module-map.md:4`, `docs/smoke-tests.md:46`, `:2921`, `:2929`, `:3095` |
| `ka0s-bounded lua tests/run.lua` | `1790 passed, 0 failed, 1 skipped, 1791 total` (exit 0) |
| `ka0s-bounded luacheck .` | `Total: 0 warnings / 0 errors in 202 files` (exit 0) |
| 1500-line cap | largest own file `modules/WindowCells.lua` 1165 lines; `core/SkinSetup.lua` 643 |

**Gate: green on master.**

## Headline

DropWatcher has **very little to delete**. It never called `stockDefault`/`stock`, `__DrawsKey`, `S.CloseButton`
directly, `WidgetsReorder`, the drag handle, `BarStyle` or `hud.font`/`hud.outline`. It has three real items:

1. **R-8 workaround (delete):** `NS.QualityColor`'s "token equals the library's rounded Ka0s Default, so draw the
   client's color instead" ladder (`core/SkinSetup.lua:209-242`). Its tests and fixtures move to the exact values.
2. **R-6 guard (conditional):** migration step 10 seeds an absent `borderStyleFromSkin` companion with `false` so
   `ResetToSkin` never writes `"@skin"` into the LSM key `icons.borderStyle` (`core/Database.lua:205-237`). It can go
   only if LK-07 also covers "a non-bool key whose companion is absent". See the note under 1b.
3. **R-11 docs:** the picker title "Choose a skin for Ka0s Drop Watcher" in SKIN-19 and settings-panel.md.

The degraded facade's vocabulary list must also follow any facade member the release adds (R-9 / LK-10). One risk
needs the library implementer's attention: R-5 / LK-05 must not make `S.Text` consult **Ignore settings panel** for
window strings, because DW defaults `ignorePanel = true` and calls `S.Text` 23 times, all on the window (see 1d).

## 1. Workarounds of library gaps the release closes

### 1a. R-8 / LK-09: the rounded `q.*` tokens (DELETE)

- `core/SkinSetup.lua:209-211` `QUALITY_TOKEN`, the six qualities the schema names (keep).
- `core/SkinSetup.lua:213-221` `qualityDefault` / `defaultQuality(name)`: reads the library's Ka0s Default
  `q.*` values once via `lib:ResolveSkin(lib.DEFAULT)`. **Workaround: delete.**
- `core/SkinSetup.lua:223-225` `sameColor(c, r, g, b)`. **Delete** (only `NS.QualityColor` uses it).
- `core/SkinSetup.lua:227-242` `NS.QualityColor(q)`; the doc comment at `:227-232` says the schema writes the
  client's colors "to two places (q.epic 0.64, 0.21, 0.93 against the client's a335ee)". Line `:237`
  `if r ~= nil and not sameColor(defaultQuality(name), r, g, b) then return r, g, b end` is the workaround. After
  LK-09 Ka0s Default's `q.*` is the client's color, so the ladder becomes: the skin's `q.*` token when it answers,
  else `ITEM_QUALITY_COLORS[q]` (qualities outside q.poor..q.legendary, and the degraded facade, which carries no
  `q.*`), else nil. Rewrite the comment to match.
- Callers (no change; they go through `NS.QualityColor`): `modules/CompactGroup.lua:168`,
  `modules/DetailCard.lua:398`, `modules/OfferPanel.lua:286`, `modules/HistoryCard.lua:298`,
  `modules/WindowGroup.lua:709`, `modules/WindowHistory.lua:443`, `modules/TipMarks.lua:173`,
  `modules/IconStyle.lua:136` (and `IS.QualityColor`, `modules/IconStyle.lua:132`).
- Doc row that encodes the workaround: `docs/ARCHITECTURE.md:318` ("a quality reads the skin's `q.*` only where a
  skin overrides it, else the client's"). Reword to "the skin's `q.*` (Ka0s Default's is the client's own)".
- Degraded arm: `NS.SKIN_FALLBACK` (`core/SkinSetup.lua:138-168`) carries no `q.*`, so the degraded load keeps
  falling through to `ITEM_QUALITY_COLORS`. No change; if the implementer adds `q.*` to the host copy,
  `tests/test_surface_parity.lua:209` holds them to the library's new exact values.
- A cosmetic consequence: under a skin that drew its `q.*` equal to the old rounded value by coincidence,
  nothing changes. Only Ka0s Default's values move (by under 1/255 per channel), so no pixel a player sees moves
  under Ka0s Default. The escapes built from them (`NS.SkinEscape`, `core/SkinSetup.lua:202-207`) can move by one
  byte in a channel. See the tests in 3a.

### 1b. R-6 / LK-07: `ResetToSkin`'s sentinel (CONDITIONAL)

- `core/Database.lua:205-212` the comment and `NS.HUD_SKIN_KEYS = { "borderStyle" }`.
- `core/Database.lua:214-223` the doc comment: "ResetToSkin decides by the companion's PRESENCE, and AceDB strips a
  value equal to its default from the stored table, so a missing companion is seeded false first: the reset then
  always lands on the companion, never the FROM_SKIN sentinel in the LSM key."
- `core/Database.lua:228-230` **the guard**: `if icons[key .. "FromSkin"] == nil then icons[key .. "FromSkin"] = false end`.
- `core/Database.lua:231-236` the call `Skin.ResetToSkin(icons, NS.HUD_SKIN_KEYS)` and the library-absent arm.
- Library code: `../LibKa0s/LibKa0s/Skin.lua:886-911`. For `borderStyle` (a string, not a table) with no
  `borderStyleFromSkin` beside it, `:901` falls to `else parent[leaf] = lib.FROM_SKIN`, so the sentinel lands in the
  LSM key. DW's case is **not** the bool case R-6 names ("writes `"@skin"` into an absent bool companion"), and it
  is not the case LK-07 describes ("leaves an absent bool companion a bool"). The library cannot know a companion
  exists when it is absent and the key is a string.
- **Verdict for the implementer:** the guard goes only if LK-07 gives `ResetToSkin` a way to say "this key has a
  companion" (for example a `{ companion = true }` entry or an `opts.companions` set) or rules that a string key
  with an absent companion gets the companion set rather than the sentinel. If LK-07 fixes only the bool case, DW
  keeps the guard and DW-01's ResetToSkin part becomes an `exceptions.tsv` row (proof below, §6).
- A related defensive read stays either way: `modules/IconStyle.lua:87-103` `IS.Follow`, whose `:98-99` turns a
  stored FROM_SKIN sentinel back into the shipped default. It guards stored data that already exists (and an
  older library), not the library's gap, so it stays.

### 1c. R-2 / LK-02: `stockDefault` / `stock` (NOTHING)

DW never asks for the stock look. The facade calls in the whole addon are `NS.Skin.Color` (13), `.Text` (23),
`.Font` (11), `.OnLooksChanged` (5), `.ScrollBar` (4), `.Inset` (1) and `.Token` (1); none takes an opts table
with `stock` or `stockDefault`. The chrome (Shell, title bar, close buttons) is painted through Core
(`core/CoreSetup.lua:100-114`, `NS.ApplySkin` and `NS.MakeCloseButton`) and the dropdowns, search box and strips
through Widgets (`core/WidgetsSetup.lua:39-80`, each with `owner = addonName`), neither with a stock option.

**What DW looks like under Ka0s Default afterwards:** unchanged. SKIN-2 (`docs/smoke-tests.md:2935-2947`) already
records Ka0s Default as the Ka0s look (Oxanium, the title band, the corridor scroll bars). The one library-internal
`stock` user that touches DW is the options tab strip (`../LibKa0s/LibKa0s/OptionsTabs.lua:501-503`, and the
content panel at `:492-495`). That is library code, it shows only with **Ignore settings panel** off (DW's
default is on, `defaults/Profile.lua:215`), and LK-02 owns it.

### 1d. R-5 / LK-05, LK-06: Scope guards around library widgets (NOTHING TO DELETE, ONE RISK)

- DW has **no hand-rolled Scope guard around a library widget**: no guard around `S.Text`, and no
  `WidgetsReorder`, `WidgetsDragHandle`, `WidgetsAutocomplete` or `WidgetsLineChart` use (grep in §6).
- DW's own Scope reads are for **host raw frames on the settings panel**, not library widgets, and they stay:
  - `core/SkinSetup.lua:181-187` `NS.SkinPanelIgnored()` (public `Skin:GetIgnore`) and `:189-197`
    `NS.SkinPanelColor(name)`, used by `settings/PageEditors.lua:121-131` (`paintHeader`, `paintLabel`,
    `paintStripe`, the Situations table's own strings and stripes) and `settings/PageEditors.lua:243-256` (the
    session-held AceGUI cells repaint via `NS.SkinPaintAce`, and the library refuses while the panel is ignored).
  - These would only go if LK-05/06 publishes a host helper for "paint this raw region for the panel scope". The
    plan does not promise one, so they stay.
- **Risk for LK-05:** DW calls `S.Text` 23 times, every one on a window, card, toast or strip string and none on
  the settings panel (`grep -rln 'NS.Skin.Text(' settings` prints nothing). Files: `modules/DetailCard.lua:246`,
  `:267`, `:686`; `modules/CompactChrome.lua:284`; `modules/DropsStrip.lua:139`, `:142`;
  `modules/OfferPanel.lua:135`, `:138`, `:165`, `:201`; `modules/WindowHistory.lua:509`, `:528`;
  `modules/Window.lua:437`, `:622`; `modules/Toast.lua:286`, `:292`; `modules/WindowFooter.lua:196`;
  `modules/WindowGroup.lua:692`, `:941`; `modules/WindowRows.lua:147`; `modules/WindowTitleBar.lua:179`, `:255`,
  `:294`. DW's default is `skin.ignorePanel = true` (`defaults/Profile.lua:215`). If LK-05 made `S.Text` consult
  Ignore settings panel for every string, every new DW profile's window text would lose its skin colors. LK-05
  must scope the panel check to strings on the owner's settings panel. Under **Ignore fonts**, `S.Text` already
  gives the face back (`../LibKa0s/LibKa0s/SkinPaint.lua:539`), and that is the expected behaviour.
- LK-06 (custom widgets) reaches DW only through what DW already builds for its owner: the debug console
  (`core/DebugLogSetup.lua:82-115`; `addonName` is the owner, `../LibKa0s/LibKa0s/DebugLogWindow.lua:18-26`) and
  its Copy window, the launcher (`core/LauncherSetup.lua:84`), the sim panel (`modules/Sim.lua:273`,
  `modules/SimPanel.lua`), the perf panel (`core/PerfSetup.lua:47`), the toast (`core/ToastSetup.lua:29-35`,
  `d.owner = addonName`) and the Widgets dropdown, search box and strips (`core/WidgetsSetup.lua:39-80`). Every one
  already passes the owner, so DW needs **no code change** for LK-06. Only the looks and the Scope behaviour
  change, which SKIN-11/12 cover (§4).

### 1e. R-9 / LK-10: `__DrawsKey` (NOTHING TO DELETE, ONE KNOCK-ON)

- No reach into `Skin:__DrawsKey`, `__PanelSkinned`, `__FontsIgnored` or any other `__` internal of the Skin major
  (grep in §6).
- **Knock-on:** the degraded facade enumerates the live facade's vocabulary at `core/SkinSetup.lua:518-526`, and
  `tests/test_surface_parity.lua:199-207` holds the two key for key, with nothing ignored. If LK-10 (or any LK item)
  adds a member to the `Skin:For(owner)` facade (for example `S.DrawsKey`), DW's degraded table must answer it or
  the parity test goes red at re-vendor. The same goes for any facade name LK-02 removes. This is part of DW-RV
  ("meet the release's What a consumer owes").

### 1f. R-3 / LK-03: close-button tint (NOTHING)

- DW has no tint handling of its own. Every close control is `NS.MakeCloseButton` (`core/CoreSetup.lua:108-114`,
  callers `modules/WindowTitleBar.lua:301`, `modules/DetailCard.lua:687`, `modules/OfferPanel.lua:140`, and the
  toast's `f.close`, `modules/Toast.lua:331`). Core paints it through the owner's facade with
  `S.CloseButton(b, { own = true })` (`../LibKa0s/LibKa0s/Core.lua:303-304`; the proof grep below matches no
  `CloseButton(..., {` in DW itself), so LK-03's save-and-restore applies
  to DW's close buttons with no DW change.

### 1g. R-7 / LK-08: tooltip and quality literals (NOTHING)

- No literal tooltip color: DW's tooltip lines read `gtip.*` and the owner tokens that follow them
  (`modules/Window.lua:219`, `:233`; `modules/WindowCells.lua:1016`; `modules/TipGrid.lua:119`;
  `modules/WindowGroup.lua:449` `dw.tipHint`, following `gtip.muted` at `core/SkinSetup.lua:115`;
  `dw.tipLabel` following `gtip.title` at `core/SkinSetup.lua:131`). The literal gate
  (`tests/test_skin_literals.lua:143`) forbids any other literal outside `core/SkinSetup.lua`.
- No literal quality color. The only `a335ee` hits are comments and a link-format pattern
  (`modules/TipMarks.lua:166`, `:176`).
- No drag handle (R-7's subject) in DW.

## 2. Where DW resolves a HUD face or outline itself (R-1)

- **None for `hud.font` / `hud.outline`.** DW's only HUD per `docs/ARCHITECTURE.md:285-291` is the item icon's
  border (style and thickness from `icon.borderStyle` / `icon.borderSize` via `IS.Follow`,
  `modules/IconStyle.lua:94-103`). DW has no HUD text setting, no `fromSkin = "font"` composer row (its only
  `fromSkin` is `"icon"`, `settings/ComposedRows.lua:47`) and no `BarStyle` call. R-1 / LK-01 and R-4 / LK-04 need
  no DW change.
- **Adjacent, outside R-1's letter, for DECISIONS.md:** DW resolves one face itself, the monospace glyph face.
  `NS.SkinMonoFont()` (`core/SkinSetup.lua:284-292`) reads `NS.Skin.Token("font.mono")`, fetches it from LSM and
  falls back to `NS.Constants.FONT_MONO`. `NS.SkinMono(fs, size)` (`:297-299`) sets it with a raw `SetFont`
  through `NS.SkinPaint`, outside the library's `P.font`. `modules/TipGrid.lua:103` sets it directly. So with
  **Ignore fonts** on, the verdict glyphs keep the skin's `font.mono` while every library-painted string goes back
  to its own face. Users: `modules/CompactGroup.lua:209`, `modules/DetailCard.lua:128`, `modules/Toast.lua:273`,
  `modules/WindowGroup.lua:545`, `:590`, `modules/WindowHistory.lua:366`, `modules/TipGrid.lua:103`. The glyphs
  ▲ ≈ ▼ need a face that carries them, and "the stored value" for these strings is `C.FONT_MONO` (JetBrains Mono,
  which carries them). If the lead extends R-1's spirit to `font.mono`, the change is one line in
  `NS.SkinMonoFont`: return `NS.Constants.FONT_MONO` while `Skin:GetIgnore(addonName)` answers fonts = true. Under
  Ka0s Default that is the same face. The library's override already leaves `font.mono` alone
  (`../LibKa0s/LibKa0s/Skin.lua:659`, `:727`), and SKIN-16 says the glyphs "keep their monospace face" under an
  override. **The recommendation is no change**: the face is chosen for glyph coverage, not for looks. Record it
  in DECISIONS.md either way.

## 3. Tests that pin each current behaviour

### 3a. R-8 (q.* exact)

- `tests/test_skin_chrome.lua:214-225` "an item quality keeps the client's color unless the skin overrides it".
  Its comment `:215-216` says "Ka0s Default's q.* tokens are the client's colors rounded to two places". It sets
  `ITEM_QUALITY_COLORS[4]` to 163/255, 53/255, 238/255 and expects that under Ka0s Default. It survives the change
  (the token then equals the client's color) but the comment and title must be rewritten. The switched half
  (`:221-223`) is unchanged.
- `tests/test_icon_style.lua:17` fixture `QUALITY_COLORS = { [3] = { 0, 0.44, 0.87 }, [4] = { 0.64, 0.21, 0.93 } }`
  (the rounded values), used at `:156`. Assertions `:162`, `:164` (`sameColor(b.iconBorder, 0.64, 0.21, 0.93, 0.75)`)
  and `:174-175` (`near(r, 0.64)`), with `near` at 1e-6 (`:27`). **Red after the change:** once the token is read
  directly, Ka0s Default answers 163/255 (0.6392...), not the mock's 0.64. Move the fixture and the expected values
  to the client's exact colors (a335ee, 0070dd).
- `tests/test_detail_card.lua:425-433` "Replaces reads ... the name in its quality color" sets
  `ITEM_QUALITY_COLORS[3] = { 0, 0.44, 0.87 }` and expects `"|cff0070deOld Helm|r"` (`:433`). **Red after the
  change:** the token's exact rare escapes to `|cff0070dd`. Move the fixture and the expectation to `0070dd`
  (the client's real rare).
- `tests/test_compact_group.lua:175-180` reads `m.ITEM_QUALITY_COLORS[4]` if set and compares the item text to
  `q.r`. Check it after the change: it passes only while the mock's table equals the token.

### 3b. R-6 (ResetToSkin)

- `tests/test_skin_hud.lua:149-173` "migrate 10: every stored profile's icon border goes back on the skin once, its
  pick kept".
- `tests/test_skin_hud.lua:175-193` "it runs once; a player's later pick survives the next load".
- `tests/test_skin_hud.lua:195-206` "idempotent on a raw table, the companion seeded so no sentinel lands; without
  the library too". `:200` asserts `raw.icons.borderStyle == "Solid"` ("never the FROM_SKIN sentinel in an LSM
  key"). This pins the guard's outcome and must stay green whether or not the guard goes. If the guard is
  removed, add a case with `icons = {}` (no stored style, no companion) under the live library, which is the case
  the seeding protects.

### 3c. R-11 (picker)

- No test pins the title text (`grep -n -i 'choose a skin' tests/*.lua` prints nothing).
  `tests/test_skin_picker.lua:70-83` pins the spec (`owner`, `get`, `set`, `page = "general"`,
  `tab = "Appearance"`, `onPreview`, `onClose`). If LK-11 changes the spec contract (for example a `label` field,
  or the owner's label read from `RegisterOwner`'s `label = NS.BRAND`, `core/SkinSetup.lua:580`), update it here.
  The "Appearance" key is the tab's key, not its label (the label is "Skin" since OptionsAppearance minor 3):
  `tests/test_settings_pages.lua:17-18`, `tests/test_skin_setup.lua:166`, `:259-261`, `:271`,
  `tests/test_skin_picker.lua:65`, `:79`, `:290`. R-10 renames the label in the standard only, so they stay.

### 3d. R-5 / LK-05, LK-06 (Scope)

- `tests/test_skin_settings.lua:156` "the Situations cells follow a skin switch and the Ignore settings panel,
  live" and `:178-206` "the Situations headers, labels and stripes stay Ka0s Default with the settings panel
  ignored" pin DW's own panel guard (1d). They stay.
- `tests/test_skin_settings.lua:247` "the debug console, perf panel, sim panel, test strip and toast are this
  owner's" and `:269` "the live debug console is painted for this owner" pin the tool windows' owner. LK-06 should
  leave them green. If LK-06 makes the tool windows obey Ignore fonts, add an assertion here.
- `tests/test_skin_chrome.lua:80` (Ka0s Default pixels), `:98` (switch repaints): must stay green with the
  default `ignorePanel = true`. This is the regression net for the 1d risk.

### 3e. R-9 / LK-10 (facade members)

- `tests/test_surface_parity.lua:199-207` (degraded facade vs live facade, key for key) goes red if the facade
  gains or loses a member.
- `tests/test_surface_parity.lua:209` (host-copy tokens equal the library's Ka0s Default) stays green: no
  `NS.SKIN_FALLBACK` entry is a `q.*` or a token LK-04 changes (LK-04 changes non-Ka0s skins only).

### 3f. R-1 / R-4 (HUD font)

- None. Nothing in DW reads `hud.font` / `hud.outline`. The mono face is pinned by `tests/test_skin_chrome.lua:148-159`
  (`font.mono` is "JetBrains Mono", `NS.SkinMonoFont() == C.FONT_MONO`), which stays green under Ka0s Default
  whatever §2's decision is.

## 4. Smoke checks and doc passages whose expectation changes

| Where | Today | After v1.81.0 |
|---|---|---|
| `docs/smoke-tests.md:3049-3058` **SKIN-19** | "a small window, **Choose a skin for Ka0s Drop Watcher**, shows: a dropdown of the skins, an eye, a gear, and **Apply**" (`:3050-3052`) | Title **Choose a skin**; **Ka0s Drop Watcher** on its own line above the skin dropdown, never cut off; the window wide enough for it (R-11). Result cleared to owed. |
| `docs/settings-panel.md:99-101` | "a small window, **Choose a skin for Ka0s Drop Watcher**, with a dropdown of the skins, ..." | Same rewrite as SKIN-19. |
| `docs/smoke-tests.md:3004-3009` **SKIN-12** tool windows | each wears DW's skin; the console keeps its monospace face | Add LK-06's new reach (the Copy window and any widget LK-06 newly skins) and the Scope (Ignore fonts on gives the tool windows' strings back their own face, if LK-06 rules so). The console's face is DW's `C.FONT_MONO` (`core/DebugLogSetup.lua:86`). |
| `docs/smoke-tests.md:3033-3038` **SKIN-16** Ignore fonts | "Tick **Ignore fonts** → every string goes back to the game's face" | Unchanged for the window. If §2 is decided "no change", add "the verdict glyphs keep their monospace face" (true today, and unstated). If LK-06 covers the tool windows, they now follow too. |
| `docs/smoke-tests.md:2998-3002` **SKIN-11** strips and sim panel | the strips and the step panel wear the skin | Unchanged expectation; re-run on v1.81.0 (LK-06 touches the sim panel). |
| `docs/smoke-tests.md:2935-2947` **SKIN-2** Ka0s Default | the Ka0s look with three visible changes | **Unchanged** (R-2 retires nothing DW used). Re-run only as part of SKIN-1's load. |
| `docs/smoke-tests.md:3025-3031` **SKIN-15** fonts | "WoW Default the client's Friz Quadrata" | **Unchanged**: that is `font.body`; R-4 changes `hud.font` only, which DW never draws. |
| `docs/smoke-tests.md:2929-2931` **SKIN-1** | "Loads clean on LibKa0s v1.80.0" | v1.81.0; a new run row per the rollout's pattern (the frozen results stay; add a v1.81.0 owed block like `:3095`). |
| `docs/smoke-tests.md:46` index row | "on LibKa0s v1.80.0" | Name v1.81.0 and the new checks. |
| `docs/ARCHITECTURE.md:318` | "a quality reads the skin's `q.*` only where a skin overrides it, else the client's" | "the skin's `q.*` (Ka0s Default's are the client's own colors)" (R-8). |
| `docs/ARCHITECTURE.md:292-296` first-run picker | no title quoted | No change needed; optional mention of the name line. |
| `docs/ARCHITECTURE.md:14`, `docs/module-map.md:4`, `core/SkinSetup.lua:9` | "LibKa0s v1.80.0" | v1.81.0 (DW-RV). |
| `docs/testing.md:215` | `test_skin_chrome` "... quality colors ..."; `test_skin_hud` "... idempotent and sentinel-free" | Reword "quality colors" if the test's title changes; the sentinel phrase stays if the guard stays. Test totals move. |
| `docs/schema.md:414` step 10 | "a missing companion is seeded `false` first, so the reset lands on the companion" | Only if the guard goes (1b): "the reset sets the companion". |
| `docs/module-map.md:27` | lists `NS.QualityColor` as a call-site helper | Unchanged (the helper stays, only its body shrinks). |
| `README.md:65` | "a small picker offers them the first time you log in" | Unchanged (no title quoted). |
| `docs/known-limitations.md` | no skin entry (`grep -n -i 'ignore fonts\|picker\|quality' docs/known-limitations.md` prints nothing relevant) | Unchanged. |

Stock-look smoke rows: DW has none (it never kept a stock look under Ka0s Default). HUD face under non-Ka0s skins:
DW has no HUD text, so no check changes.

## 6. Nothing to change: proofs (exceptions.tsv rows)

Run from `../DropWatcher`. Each prints nothing.

| Item / ruling | Proof command |
|---|---|
| R-1 / LK-01, R-4 / LK-04: no HUD face or outline resolved by DW | `grep -rnE 'hud\.(font\|outline)\|BarStyle\(\|fromSkin *= *"font"' core modules settings` |
| R-2 / LK-02: no stockDefault / stock caller | `grep -rnE 'stockDefault\|stock *=' core modules settings` |
| R-3 / LK-03: no close-button tint handling | `grep -rnE 'CloseButton\(.*\{\|SetVertexColor' core modules settings \| grep -i close` |
| R-5 / LK-05: no Scope guard around S.Text / WidgetsReorder | `grep -rnE 'Reorder\|NS\.Skin\.Text\(' settings` |
| R-6 / LK-07 (only if LK-07 fixes the bool case alone) | `grep -n 'FromSkin"\] == nil' core/Database.lua` prints `core/Database.lua:229` (the guard stays, justified in 1b); the bool case does not occur: `grep -n 'HUD_SKIN_KEYS =' core/Database.lua` lists only `borderStyle`, a string |
| R-7 / LK-08: no drag handle | `grep -rnE 'DragHandle' core modules settings` |
| R-9 / LK-10: no reach into Skin internals | `grep -rnE '__DrawsKey\|__PanelSkinned\|__FontsIgnored\|:__[A-Z]' core modules settings \| grep -i skin` |
| R-10 / WS-01: tab key "Appearance" is the library's key, not a label DW writes | `grep -rn '"Appearance"' core settings` prints only key uses: `core/SkinSetup.lua:434` (`tab = "Appearance"`), `settings/SchemaRows.lua:592` (`SKIN_GROUP`) and the comments `settings/SchemaRows.lua:586`, `settings/Panel.lua:77`. The label "Skin" is the library's; no DW change |

Items that DO change in DW: **DW-RV** (re-vendor, provenance `CLAUDE.md:44`, the pins in §5, the degraded facade
vocabulary `core/SkinSetup.lua:518-526` against any facade change); **DW-01** (R-8 `NS.QualityColor`
simplification `core/SkinSetup.lua:209-242` with tests `tests/test_icon_style.lua:17`, `:162-175`,
`tests/test_detail_card.lua:429-433`, `tests/test_skin_chrome.lua:214-225`; R-6 guard `core/Database.lua:228-230`
only if LK-07 covers it); **DW-02** (SKIN-19, settings-panel.md:99-101, SKIN-12/16 notes, ARCHITECTURE.md:318, the
v1.81.0 pins and the owed block).
