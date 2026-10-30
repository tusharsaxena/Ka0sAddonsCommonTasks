# M0 inventory: KickCD

Read-only inventory for the LibKa0s v1.81.0 follow-ups (rulings R-1..R-11 of `../../00_PLAN.md`). Scope is
`/mnt/d/Profile/Users/Tushar/Documents/GIT/KickCD`, excluding the vendored `libs/` and `tests/_kit/` (read only
for reference). All paths below are relative to the KickCD repo root unless they say otherwise. Read on
2026-10-30 at master `c006208`.

## 0. Bottom line

KickCD carries **almost no workaround** that the release closes. The rollout built it on the library's own
seams: no `stockDefault`/`stock` caller, no `__DrawsKey`, no `S.CloseButton`, no `q.*` token, no hand-rolled Scope
guard around `S.Text` or `ReorderList`, and no Ignore-fonts patch on the HUD. Every HUD face goes through
`S.Resolve`, so **R-1 reaches the HUD without a code change**. What KC-01/KC-02 actually have to do:

- **Tests:** add the R-1 case (Ignore fonts on, so the HUD draws the stored face and the charges badge falls back to
  `NumberFontNormal`), move the picker-title assertion (R-11), and hold the degraded facade's vocabulary to any
  name v1.81.0 adds (surface parity). Optionally relax the ResetToSkin guard comment (R-6).
- **Docs and smoke checks:** SKIN-6 and ARCHITECTURE (HUD face under non-Ka0s skins, R-4), SKIN-14 (Ignore fonts
  on the HUD, R-1), SKIN-22 and test_skin_picker (picker title, R-11), and SKIN-11 (the reorder ghost and drop line
  obey the panel Scope, R-5). SKIN-1 and SKIN-11 change too if LK-06 puts the tool windows under the panel Scope.

## 1. Workarounds of library gaps the release closes

### 1a. Own Ignore-fonts handling for HUD faces or outlines (R-1): none

- The addon calls `GetIgnore` in one place only, `core/SkinSetup.lua:116`, and that call is the **settings-panel**
  Scope (see 1c). Nothing reads `ignoreFonts` except the schema row `settings/General.lua:306` and the seam
  `core/SkinSetup.lua:89,210,227`.
- No `NS.SkinFontsIgnored`-style helper exists. Proof:
  `grep -rn 'GetIgnore\|IsFontsIgnored\|ignoreFonts' core modules settings` returns only
  `core/SkinSetup.lua:112,116` and `settings/General.lua:306` (plus the path constant at `core/SkinSetup.lua:89`).
- KickCD reads no `hud.outline` anywhere. Its outline is always the player's own flags (rollout decision X4).
  Proof: `grep -rn 'hud\.outline' core modules settings defaults tests/*.lua docs/*.md` returns nothing.

### 1b. `stockDefault` / `stock` callers (R-2): none

- Proof: `grep -rnE 'stockDefault|stock\s*=' core modules settings defaults` returns nothing.
- KickCD's only direct call to a painting primitive is `NS.Skin.Text(fallbackLabel, "accent")` at
  `settings/Spells.lua:542` (the AceGUI-missing label). Proof: grep for
  `(NS\.Skin|S)\.(Shell|Panel|...|Text|Token|Color)\(` over `core modules settings`, excluding `core/SkinSetup.lua`,
  returns only that line.
- **The surface under Ka0s Default afterwards.** Nothing KickCD paints passes stock opts, so R-2 changes no
  KickCD-owned surface. The library's own tool windows that KickCD hosts (the debug console and copy window, the perf
  panel, the sim panel, the drag handles, the sim strip and the reorder list) were checked in the vendored copy: the
  only `stock =` callers in non-Skin library files are `libs/LibKa0s/OptionsTabs.lua:495,503` (the options chrome's
  tab art). So under Ka0s Default, with **Ignore settings panel off**, the options panel's tab strip moves from its
  stock halves to the Ka0s look. With the default (Ignore settings panel on), the panel stays stock: per R-2 that
  switch stays, default on. KickCD's HUD is untouched by R-2.

### 1c. Hand-rolled Scope guards around S.Text, WidgetsReorder and other library widgets (R-5): none, and one adjacent guard that stays

- `S.Text`, at `settings/Spells.lua:542`, has **no** Scope guard. After LK-05 it obeys Ignore settings panel. With
  the default (panel ignored), the label stays `GameFontNormal`'s own gold, which is the same color as Ka0s Default's
  `text.accent`, so nothing visible changes. The comment at `settings/Spells.lua:541` ("The skin's accent role: gold
  on Ka0s Default ...") can gain "(stock while the Scope ignores the panel)". This is optional.
- `W.ReorderList{ owner = addonName, ... }` at `settings/Spells.lua:611-632` has no Scope guard. After LK-05 its drag
  ghost and drop line are stock while Ignore settings panel is on. **No code change is needed**, but the smoke check
  SKIN-11 changes (see section 4).
- The drag handles `modules/IconGrid_Handle.lua:133-155` and `modules/Castbar_Handle.lua:92-...`, and the sim strip
  `modules/SimStrip.lua:65-72`, are all owner-only with no guard. LK-06 decides whether these HUD-side tool surfaces
  fall under the panel Scope. KickCD has no code to change either way.
- **The adjacent guard that stays: `pageColor`** at `core/SkinSetup.lua:111-121`, documented at
  `core/SkinSetup.lua:33-36` and `docs/ARCHITECTURE.md:355-358`. It makes `NS.SkinColor` / `NS.SkinEscape` answer the
  Ka0s Default host copy while Ignore settings panel is on, because `S.Color` does not consult the Scope. No ruling
  makes `S.Color` / `S.Token` Scope-aware (R-5 covers widgets), so this guard is **not** made unnecessary by v1.81.0.
  Keep it, unless LK-05/LK-06 also add a Scope-aware color read; if they do, it becomes a candidate.
  Pinned by `tests/test_skin_settings.lua:283-315`.
  Exceptions row: `grep -n 'GetIgnore' core/SkinSetup.lua` shows the one guard, on color tokens, not widgets.

### 1d. ResetToSkin guards against the `"@skin"` sentinel (R-6): one guard, which can stay

- `core/Database_Migrations.lua:376-384`: `MigrateHudSkin` names only companions whose stored value is a boolean
  (`type(parent[leaf]) == "boolean"`, line 380). The rationale is the comment at `core/Database_Migrations.lua:341-343`:
  "ResetToSkin writes the FROM_SKIN sentinel into a key it finds neither a table nor a bool".
- The call is `Skin.ResetToSkin(p, keys)` at `core/Database_Migrations.lua:389-390`.
- **After LK-07** the sentinel rationale is obsolete. The filter is still *semantically right*: an absent companion
  reads AceDB's default `true` (`defaults/Profile.lua:76,82,194,270,287,294,311,331`), so only a stored `false` needs
  the reset, and dropping the filter would write `true` into keys AceDB already defaults. Recommendation: keep the
  filter and rewrite the comment at 341-343 to give the AceDB-default reason. Also reword the test's "red under"
  line at `tests/test_skin_hud.lua:377-378`. The assertion `label.style.fontFromSkin == nil` at
  `tests/test_skin_hud.lua:387` stays valid, since the step never names the key.
  Treat this as a doc-only change, or an exception if the implementer leaves the comment.
- The library's current behaviour is at `libs/LibKa0s/Skin.lua:886-...` (the `lib.ResetToSkin` doc,
  "any other key takes the FROM_SKIN sentinel").

### 1e. Reach into `Skin:__DrawsKey` or other internals (R-9): none

- Proof: `grep -rn 'DrawsKey' core modules settings defaults tests/*.lua` returns nothing.
- The only `__`-prefixed library reads are test-side mock fields (`LSM.__registered`, `__libs`), and none is a Skin
  internal.

### 1f. Close-button tint handling (R-3): none

- KickCD never calls `S.CloseButton`. Its close controls are Core's `lib.MakeCloseButton(parent, onClick, addonName)`
  through `NS.MakeCloseButton`, at `core/CoreSetup.lua:243-249` (degraded stub at `core/CoreSetup.lua:136` and
  `core/DebugLogSetup.lua:107`).
- Proof: `grep -rnE 'CloseButton' core modules settings | grep -v MakeCloseButton` returns only
  `core/SkinSetup.lua:368`, the vocabulary *string* in the degraded facade's name list, which is not a call.

### 1g. Literal tooltip or quality colors standing in for `gtip.*` / `q.*` (R-7, R-8): none

- The Spells rows' own hint already reads `gtip.title`: `settings/Spells_Rows.lua:77-85`
  (`GameTooltip:SetText(text, NS.SkinColor("gtip.title"))`), with host copy `core/SkinSetup.lua:108`.
- The drag-strip tooltip is the library's. KickCD passes only text (`modules/IconGrid_Handle.lua:149-152`; the cast
  bar handle the same), never a color. LK-08 changes its title and body colors under non-Ka0s skins with no KickCD
  change.
- No `q.*` token anywhere. Proof: `grep -rnE '"q\.[a-z]' core modules settings defaults tests/*.lua` returns nothing.
  LK-09 does not touch KickCD.

## 2. Where KickCD resolves a HUD face itself (R-1)

Every HUD face goes through **one** seam, `NS.SkinResolve(kind, value, fromSkin)` at `core/SkinSetup.lua:143-154`,
which calls the library's `S.Resolve(kind, value, true)` (line 151) and falls back to the stored `value` when the
skin answers nil (line 152). The library's `Resolve` today is `libs/LibKa0s/Skin.lua:866-871`: it ignores the Scope.
Once LK-01 makes `Resolve` answer the stored value for `hud.font` while Ignore fonts is on, every site below draws
the HUD element's own pick **with no KickCD code change**. They are listed so the tests can pin each one:

| Site | Stored value handed in | Under R-1 with Ignore fonts on |
|---|---|---|
| `modules/Castbar_Skin.lua:164-166` `Castbar.LabelFont(c)` → `NS.SkinResolve("hud.font", c.font, c.fontFromSkin)` (both cast-bar texts; signed into the structure signature at `modules/Castbar_Skin.lua:184`) | `castbar.font` | the stored cast-bar face; the signature moves, so `Reskin` rebuilds |
| `modules/IconGrid_Render.lua:887-891` `ApplyTextConfig`: the countdown, `NS.SkinResolve("hud.font", cfg.cooldownTextFont, cfg.cooldownTextFontFromSkin)` | `icons.cooldownTextFont` | the stored countdown face |
| `modules/UnitLabel.lua:91-96` `applyLabelFont`: `NS.SkinResolve("hud.font", sv(style,"font"), style.fontFromSkin)` | `label.style.font` | the stored label face |
| **`modules/IconGrid_Render.lua:853-862` `applyChargesFont`**: `NS.SkinResolve("hud.font", nil, true)`. The charges badge has **no setting of its own** (DECISIONS D4) and always passes `fromSkin = true` with a nil value | none | `Resolve` answers nil, so `NS.SkinResolve` answers nil (line 152), so `LSM:Fetch("font", "", true)` answers nil, so the badge keeps `NumberFontNormal`'s face (line 861-862). This is the badge's "own font". **Edge case for LK-01:** if LK-01 returns the token whenever the stored value is nil, the badge keeps the skin's face under Ignore fonts. The KickCD test must pin whichever LK-01 chooses, and the lead may want LK-01 to answer nil (so a host's own fallback wins). |

- **Live repaint on toggle:** `Skin:SetIgnore` repaints and fires OnLooksChanged (`libs/LibKa0s/Skin.lua:611-623`).
  The three HUD modules subscribe at `modules/Castbar_Events.lua:242-251`, `modules/IconGrid.lua:938-942` and
  `modules/UnitLabel.lua:271-275`, so ticking Ignore fonts repaints the HUD live. Nothing to add.
- **Outline:** no site resolves `hud.outline`. Flags come from the player (`modules/UnitLabel.lua:97`,
  `modules/Castbar_Skin.lua` near `:310`, `modules/IconGrid_Render.lua` after `:893`).
- **The composer pickers** that preview the skin's face, which LK-01 changes on the library side (the preview is
  `libs/LibKa0s/OptionsCompose.lua:513-521`): `settings/Icons.lua:310` (countdown), `settings/Castbar.lua:488`
  (cast-bar texts) and `settings/Label.lua:212` (label). KickCD passes only `fromSkin = true`, so there is nothing to
  change.
- **Degraded arm:** `core/SkinSetup.lua:379-386` (the host `S.Resolve`). Without the library there is no Scope, so
  there is nothing to change.
- **Docs that describe the seam and need the Ignore-fonts clause added:** `core/SkinSetup.lua:39-40` and `:143-147`
  (header and function doc), `docs/module-map.md:442` (the `NS.SkinResolve` sentence), `docs/castbar.md:46`, and
  `docs/schema.md:322` and `:428`. Each says "the skin's token while the companion is set". After R-1 each becomes
  "... unless the Scope's Ignore fonts is on, when the stored pick wins".

## 3. Tests that pin current behaviour

| Test | Pins | Change for v1.81.0 |
|---|---|---|
| `tests/test_skin_picker.lua:245-254` "the title names this addon, and the eye is hidden": `assertEqual(text, "Choose a skin for Ka0s KickCD")` at :252 | the R-11 title | **Must change.** The title becomes `"Choose a skin"`, plus an assertion that the owner's label `Ka0s KickCD` (from `RegisterOwner`'s `label = L["Ka0s KickCD"]`, `core/SkinSetup.lua:413`) is on the new line above the dropdown. Read it off whatever field LK-11 exposes (the shared mock FontString keeps no text, so spy on `SetText` as :248-251 do). The test name and `docs/test-cases.md` change with it. |
| `tests/test_skin_hud.lua:222-242` "the countdown follows hud.font and the charges badge takes the skin's face" | badge and countdown on `hud.font` with Ignore fonts off | Stays. **Add** a sibling: with `Skin:SetIgnore(OWNER, nil, true)` the countdown, cast-bar and label fetches are the stored picks (`Friz Quadrata TT` by default) and the badge falls back to `NumberFontNormal`'s face (`Fonts\\ARIALN.TTF` in this file's `boot`, :36). It is red on v1.80.0, so it is the "fails without it" pin for KC's side of R-1. |
| `tests/test_skin_hud.lua:117-131`, `:244-257` | cast bar and label on `hud.font` while following | Stay (Ignore fonts off). |
| `tests/test_skin_hud.lua:259-274`, `:276-289` | Obsidian's `hud.font` drawn on a switch, and not drawn while stood down, both reading `Skin:ResolveSkin("obsidian")["hud.font"]` | Stay green. **Note:** under v1.80.0 that value is the KEEP fallback (Friz Quadrata). After LK-04 it is Obsidian's own face, which makes :287's `assertFalse` meaningful rather than coincidental, since Friz is also the stored default. No edit needed. |
| `tests/test_skin_hud.lua:376-390` "the step names only companions that read a boolean" | the ResetToSkin guard | Stays green after LK-07. Reword the `red under` comment (:377-378); see 1d. |
| `tests/test_skin_hud.lua:364-374` | degraded `NS.SkinResolve` keeps the stored pick | Stays. |
| `tests/test_skin_settings.lua:283-315` "with Ignore settings panel on, the page's tokens stay Ka0s Default's" | `pageColor` guard (1c) | Stays (the guard stays). |
| `tests/test_skin_settings.lua:261-274` | Spells hint titled in `gtip.title` | Stays. |
| `tests/test_skinsetup.lua:79-90`, `:135-140`, `:153-172` | Scope defaults and `skin.ignoreFonts` round-trip | Stay. |
| `tests/test_skinsetup.lua:183-202` | every Widgets factory names the owner | Stays (LK-05/06 read the same `owner`). |
| `tests/test_surface_parity.lua:320-322` "the degraded Skin facade answers every name the live facade carries" | the degraded facade's name list `core/SkinSetup.lua:365-373` and its extras `:375-396` | **Goes red if v1.81.0 adds any member to `Skin:For(owner)`'s facade**, for example a public `DrawsKey` on S (LK-10), a Scope helper (LK-05/06) or a fonts-ignored read (LK-01). The implementer adds each new name to the degraded table, as a no-op or an honest degraded answer, in the re-vendor commit. A lib-level `Skin:DrawsKey(owner)` that is not on the facade does not trip it. |
| `tests/test_surface_parity.lua:324-339` | host copy `NS.SKIN_FALLBACK` (`core/SkinSetup.lua:103-109`) equals Ka0s Default | Stays: none of `title.text`, `text.accent`, `close.hot`, `sem.warn`, `gtip.title` is moved by LK-09 (q.* only). |
| `tests/test_options_panel.lua:554-580` | the Options major is **fourteen files** at v1.79.0 | Goes red if v1.81.0 adds or removes an `Options*.lua` file (LK-11 may not). Move the count with the re-vendor if so. |
| `tests/test_vendor_sync.lua` / `tests/_kit/vendor_sync.lua` | the copy equals the tag named on `CLAUDE.md:42` | Moves with XX-RV (provenance line). |

## 4. Smoke checks and doc passages whose expectation changes

All in `docs/smoke-tests.md` (1471 lines; **29 lines under a 1500 cap**, if the cap is applied to docs, so prefer
rewording in place to adding checks).

| Where | Today | After v1.81.0 | Ruling |
|---|---|---|---|
| **SKIN-6** `docs/smoke-tests.md:1295-1306` | "the HUD text reads in **Oxanium** under Ka0s Default and in **Friz Quadrata** under every other skin (the library gives only Ka0s Default a HUD face of its own ...)" | Each skin's own HUD face, listed per skin from LK-04's `DECISIONS.md`. Fail clause: "a HUD string in Friz Quadrata under a non-Ka0s skin" | R-4 |
| **SKIN-14** `docs/smoke-tests.md:1355-1359` | "The HUD is not one of those strings ... it keeps drawing the skin's (or the override's) face while they are ticked." | With Ignore fonts on, every HUD text draws its own font setting (the cast bar's, the countdown's and the label's stored face) even with **Use the skin's font** ticked, and the charges badge draws the client's number font. The composer's font picker beside a ticked box shows the stored face, not the skin's. Untick Ignore fonts, and the skin's (or the override's) face is back on the HUD too. | R-1 |
| **SKIN-12** `docs/smoke-tests.md:1345-1350` | the font override reaches HUD texts whose box is ticked | Unchanged with Ignore fonts off. Optionally add "(with Ignore fonts off)". | R-1 |
| **SKIN-22** `docs/smoke-tests.md:1388-1395` | "a small window titled **Choose a skin for Ka0s KickCD**" ... Fail: "a title that does not name Ka0s KickCD" | Title **Choose a skin**. **Ka0s KickCD** on its own line above the dropdown, never cut off. Fail: a truncated name or a title that still carries it. | R-11 |
| **SKIN-11** `docs/smoke-tests.md:1338-1344` | "drag a Spells row (the reorder ghost and drop line) → each wears Azeroth". No Scope stated, so it runs on the default (panel ignored) | The reorder ghost and drop line wear Azeroth only with **Ignore settings panel** off, and are stock with it on (LK-05). If LK-06 puts the debug console, copy window, perf and sim panels, drag strips and sim strip under the panel Scope too, the whole check needs "with Ignore settings panel off" and a stock-with-it-on clause. **Depends on LK-06's Scope call.** | R-5 |
| **SKIN-1** `docs/smoke-tests.md:1248-1261` | "The debug console, perf panel and sim panel keep their edge and colors; their text reads in Oxanium, the log lines in JetBrains Mono", with "(the Skin tab's **Ignore settings panel** is on)" | Unchanged unless LK-06 makes those windows obey the panel Scope, in which case they are stock on the default Scope. The HUD part is unchanged (R-2 does not touch the HUD). | R-5 / R-2 |
| **SKIN-9** `docs/smoke-tests.md:1320-1330` | settings pages stock with Ignore settings panel on; skinned (Obsidian) with it off | With it off under **Ka0s Default**, the options tab strip now wears the Ka0s look (`libs/LibKa0s/OptionsTabs.lua:495,503` drops `stock`). "Pick Ka0s Default → the first look is back" now means the Ka0s look, not the stock tabs. Reword if the check names the tab art. | R-2 |
| **SKIN-15** `docs/smoke-tests.md:1360-1364` | under EllesmereUI "the HUD draws Ka0s Default's HUD media" | Unchanged unless LK-04 gives the `eui` source its own `hud.font` (the plan only says `eui` gets a value "where it adds a token"; `hud.font` is not new). Check against the release notes. | R-4 |
| **SKIN-2 / SKIN-7** `:1262-1272`, `:1307-1315` | "the font picker beside it is grayed and shows the skin's face" | Unchanged (Ignore fonts off in both). | — |
| SKIN-10, SKIN-21, CAST-10 (`:688-690`), DEGRADED-16 (`:1189-1193`) | | Unchanged. CAST-10 asserts text and placement only, not the tooltip's colors; LK-08's `gtip.*` is the same gold and white on Ka0s Default. | — |

Docs:

- `docs/ARCHITECTURE.md:330-332`: "The texts follow `hud.font`, which is Oxanium under Ka0s Default and Friz Quadrata
  under every other skin; the charges badge ... takes `hud.font`'s face". **R-4:** each skin's own face. **R-1:** add
  "unless the Scope's Ignore fonts is on, when each text draws its own pick and the badge the client's number font".
- `docs/ARCHITECTURE.md:340-347` "What Ka0s Default looks like": tool windows "keep their edge and colors but take
  v1.79.0's Ka0s Default faces". Update the version reference, and the Scope sentence if LK-06 moves the tool windows
  under the panel Scope (R-2/R-5).
- `docs/ARCHITECTURE.md:355-358`: "`S.Color` itself does not consult the Scope". Still true unless LK-05/06 change
  it; re-check against the release.
- `docs/ARCHITECTURE.md:359-363` "The tool surfaces": add that the reorder list (and, per LK-06, the rest) obey the
  Scope switches.
- `docs/ARCHITECTURE.md:364-375` picker paragraph: does not quote the title. Add "titled *Choose a skin*, the addon's
  name above the dropdown" if wanted (R-11).
- `docs/schema.md:86` "`ignoreFonts` ... every string keeps its own face" is now true of the HUD too; `:322`, `:428`
  as in section 2.
- `docs/module-map.md:442`, `docs/castbar.md:46`: the `NS.SkinResolve` description gains the Ignore-fonts clause
  (R-1).
- `docs/testing.md:178-192`: the skin-suite paragraph. Add the new Ignore-fonts HUD case, and change "the real
  window's title" to name the new title and label line.
- `docs/test-cases.md:1407-1424`: regenerate from `lua tests/run.lua --list` after the test renames and additions
  (`tests/test_list_mode.lua:44-46` holds it to the runner).
- `README.md:96` (Skins paragraph): says nothing about Ignore fonts or the picker title, so it is unchanged.
  `README.md:164-175` (font credits): **if LK-04 registers a face the library did not ship before**, this credits
  list must name it (the re-vendor brings the file). Today's eight faces are Oxanium, Inter, Nunito, Vollkorn,
  Bitter, Philosopher, Fira Sans and Atkinson Hyperlegible, plus JetBrains Mono at `README.md:160`.
- `docs/settings-panel.md:97` (the Skin tab key `Appearance`, label **Skin**): unchanged by R-10, which renames the
  standard's text, not the key. `core/SkinSetup.lua:299-301` (`tab = "Appearance"`) and
  `tests/test_skin_picker.lua:112` hold the key. Change them only if LK-11 or the release renames the tab key, which
  no ruling asks for.
- `CLAUDE.md:42` provenance line: `v1.80.0` becomes `v1.81.0` (XX-RV). `CLAUDE.md:43` declares the icons
  `clear, close, confirm, copy, help, info, segment, settings`; re-prune if LK-11 adds a mark to the picker.

## 5. Current state

- **Branch:** `master`, tracking `origin/master`, up to date (`## master...origin/master`). Head `c006208` "Merge
  feat/2026-10-29-skinning-rollout: the LibKa0s skinning rollout".
- **Tree:** clean (`git status -sb` shows nothing). No stash (`git stash list` is empty). One worktree (the main
  one). Local branches: `master` only.
- **Vendored LibKa0s:** `CLAUDE.md:42`, "Bundles [LibKa0s](https://github.com/tusharsaxena/LibKa0s) v1.80.0 (MIT)."
- **Gate on master (run 2026-10-30):**
  - `~/.claude/dev-copilot/bin/ka0s-bounded lua tests/run.lua` gave `1555 passed, 0 failed, 1 skipped, 1556 total`,
    exit 0.
  - `~/.claude/dev-copilot/bin/ka0s-bounded luacheck .` gave `Total: 0 warnings / 0 errors in 153 files`, exit 0.
  - Line cap: the largest touched Lua files are `modules/IconGrid_Render.lua` 963, `core/SkinSetup.lua` 472 and
    `modules/Castbar_Skin.lua` 498, all far under 1500. `docs/smoke-tests.md` has 1471 lines.
- **Gate green: yes.**

## 6. Exceptions (nothing to change), with proof commands

Run each from the KickCD repo root. Each returns no match, or only the line named.

| Ruling / item | Claim | Proof |
|---|---|---|
| R-2 (KC-01 part) | no `stockDefault` / `stock` caller | `grep -rnE 'stockDefault\|stock\s*=' core modules settings defaults` → nothing |
| R-3 | no `S.CloseButton` use, so no tint handling | `grep -rnE 'CloseButton' core modules settings \| grep -v MakeCloseButton` → only `core/SkinSetup.lua:368` (vocabulary string) |
| R-7 | no literal colors fed to the drag handle tooltip; own hint already `gtip.title` | `grep -n 'gtip' settings/Spells_Rows.lua core/SkinSetup.lua` → `Spells_Rows.lua:77,83`, `SkinSetup.lua:108`; `grep -nE 'color\|Color' modules/IconGrid_Handle.lua modules/Castbar_Handle.lua` shows no tooltip color passed |
| R-8 | no `q.*` token | `grep -rnE '"q\.[a-z]' core modules settings defaults tests/*.lua` → nothing |
| R-9 | no `__DrawsKey` reach-in | `grep -rn 'DrawsKey' core modules settings defaults tests/*.lua` → nothing |
| R-1 (code) | no own Ignore-fonts HUD patch; every HUD face goes through `S.Resolve` | `grep -rn 'GetIgnore' core modules settings` → only `core/SkinSetup.lua:116` (panel-Scope color guard); `grep -rn 'SkinResolve("hud.font"' modules` → the four sites in section 2 |
| R-5 (code) | no hand-rolled Scope guard around `S.Text` / `ReorderList` | `grep -n 'GetIgnore\|ignorePanel' settings/Spells.lua` → nothing (comment at `:520` only names the Scope) |
| R-6 | the guard stays (AceDB default reason), comment-only reword | `sed -n 341,343p core/Database_Migrations.lua; sed -n 378,384p core/Database_Migrations.lua` |
| R-10 | the tab key `Appearance` is not renamed by a standard text change | `grep -n '"Appearance"' core/SkinSetup.lua settings/General.lua` |

## 7. Work list for KC-RV / KC-01 / KC-02 (suggested)

1. **KC-RV:** re-vendor from `v1.81.0` (`git archive`), prune icons per `CLAUDE.md:43`, and roll `CLAUDE.md:42`. Add
   any new facade name to the degraded table `core/SkinSetup.lua:365-396` (parity test). Move
   `tests/test_options_panel.lua:578`'s file count if the Options major's file set moved. Update `README.md:164-175`
   credits for any new HUD face.
2. **KC-01:** no workaround to delete. Add the R-1 HUD test (section 3, including the charges-badge fallback). Rewrite
   the R-6 comment at `core/Database_Migrations.lua:341-343` and `tests/test_skin_hud.lua:377-378`. Add the
   Ignore-fonts clause to `core/SkinSetup.lua:39-40,143-147`. Optionally add the `settings/Spells.lua:541` comment.
3. **KC-02:** move `tests/test_skin_picker.lua:245-254` to the new title and label line. Update SKIN-6, SKIN-14,
   SKIN-22 and SKIN-11 (and SKIN-1 and SKIN-9 per LK-06 and the tab art), `docs/ARCHITECTURE.md:330-332,340-347,359-363`,
   `docs/schema.md:86,322,428`, `docs/module-map.md:442`, `docs/castbar.md:46` and `docs/testing.md:178-192`, and
   regenerate `docs/test-cases.md`.
