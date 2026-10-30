# M0 inventory: WhatGroup

Read-only inventory for the LibKa0s v1.81.0 follow-ups (rulings R-1..R-11 of `../../00_PLAN.md`). The scope is
`/mnt/d/Profile/Users/Tushar/Documents/GIT/WhatGroup`, excluding the vendored `libs/` and `tests/_kit/`, which were
read only for reference. Paths are relative to the WhatGroup repo root unless they say otherwise. Read on 2026-10-30
at master `d8e52f4` ("Merge feat/2026-10-29-skinning-rollout").

## 0. Bottom line

WhatGroup has **no HUD** (`docs/ARCHITECTURE.md:310-312`, `docs/smoke-tests.md:765-767`). It carries **no
workaround** that v1.81.0 closes: no `stockDefault`/`stock` caller, no Ignore-fonts patch, no hand-rolled Scope
guard, no `ResetToSkin` call, no `__DrawsKey` reach-in, no close-button tint handling and no literal tooltip or quality
color. So **WG-01 is an exception** (proof greps in section 6). The real work is in **WG-RV and WG-02**:

- **R-11 (the picker title)** is the one certain test and smoke change:
  - `tests/test_skin_picker.lua:202-205` asserts `"Choose a skin for " .. NS.BRAND_NAME`.
  - `docs/smoke-tests.md:875` (SKIN-18) quotes the old title.
  - `docs/test-cases.md:745` carries the test name.
- **Re-vendor knock-ons:**
  - Version comments: `tests/loader.lua:44`, `tests/test_libka0s.lua:64`, `docs/settings-panel.md:546`.
  - The `tests/loader.lua` file list, if v1.81.0 adds a library file.
  - The degraded facade's name list, `core/SkinSetup.lua:317-325`, if the facade gains a member. It is pinned by
    `tests/test_surface_parity.lua:231-239`.
  - The provenance line, `CLAUDE.md:48`.
- **Smoke checks that depend on how LK-05/LK-06 are built:**
  - SKIN-9 (the debug console), `docs/smoke-tests.md:830-834`.
  - SKIN-10 (the minimap tooltip and menu "look as before"), `:835-841`.
  - SKIN-8, `:821-829`, for the R-2 tab strip under Ka0s Default with the panel unignored.

## 1. Workarounds of library gaps the release closes

### 1a. Own Ignore-fonts handling for HUD faces or outlines (R-1): none

- WhatGroup draws no HUD. It has no `hud.font` or `hud.outline` read, no `fromSkin` companion, and no
  `NS.SkinFontsIgnored`-style helper.
- The addon reads Ignore fonts only as a stored value: `core/SkinSetup.lua:74` (path), `:161` (write), `:182`
  (read) and `:396-402` (`NS.ApplySkinIgnore` → `Skin:SetIgnore`). The schema default is `defaults/Profile.lua:65`.
- Proof: `grep -rnE 'hud\.(font|outline)|GetIgnore|FontsIgnored|IgnoreFonts|fromSkin|FromSkin' core modules
  settings defaults locales` returns only the degraded facade's `S.Resolve` signature at `core/SkinSetup.lua:329-330`.
  That code mirrors the library's API and is not a HUD resolver (see 1d).
- The popup's strings already obey Ignore fonts through the library. They are painted with `NS.Skin.Text`
  (`modules/FrameSkin.lua:56,60,63`), and the library's `S.Text` already goes through `P.font` / `P.unfont`
  (`inputs/inventory/lib-fonts-scope.md:218`). SKIN-17 already expects every popup string in the game's face with
  Ignore fonts on (`docs/smoke-tests.md:866-872`). Nothing changes.

### 1b. `stockDefault` / `stock` callers (R-2): none in the addon; one library surface changes look

- Proof: `grep -rnE 'stockDefault|stock *=' core modules settings defaults locales` returns nothing.
- Every primitive call the addon makes passes no opts:
  - The popup window goes through `NS.ApplySkin(f, nil, addonName)` at `modules/Frame.lua:867`, which is Core's
    ApplySkin → `S.Shell`.
  - Its strings use `S.Text` (`modules/FrameSkin.lua:56-63`), and its Close button uses `S.Button(btn)`
    (`modules/FrameSkin.lua:65`).
  - The two AceGUI paints are `NS.SkinPaintAce` and `NS.SkinPaintAceTree` (`core/SkinSetup.lua:386-394`).
- **What the addon's surfaces look like under Ka0s Default afterwards:**
  - **The popup:** unchanged. It already paints the Ka0s look under Ka0s Default, including the flat Close button
    (rollout D4; `docs/smoke-tests.md:769-780` SKIN-1).
  - **The debug console and copy window:** unchanged. They are painted for the owner through the descriptor's
    `addonName` (`core/DebugLogSetup.lua:209-214`). The vendored `DebugLog*.lua` passes no `stock` opts (proof:
    `grep -nE 'stock *=|stockDefault' libs/LibKa0s/DebugLog*.lua` returns nothing).
  - **The settings chrome: this one changes.** The only non-Skin `stock` callers in the vendored v1.80.0 are
    `libs/LibKa0s/OptionsTabs.lua:495` (`Panel` with `stock = panel.__ka0sHalves`) and `:503` (the tab art,
    `stock = { art.left, art.mid, art.right }`). After LK-02, under **Ka0s Default** with **Ignore settings panel
    off**, General's tab strip (Master controls | Notifications | Skin | Keybindings) and the page panel wear the
    Ka0s look instead of their stock halves. With the default (Ignore settings panel on) they stay stock: R-2 keeps
    that switch, defaulting to on (`defaults/Profile.lua`; `docs/settings-panel.md:316`).
  - **The Test notification button and the Profiles tree:** already the Ka0s look under Ka0s Default when the panel
    is not ignored. This is pinned by `tests/test_skin_tools.lua:80-83`, which stays.

### 1c. Hand-rolled Scope guards around S.Text, WidgetsReorder and other library widgets (R-5): none

- **`S.Text`.** It is used only on popup strings, at `modules/FrameSkin.lua:56` (labels, `wg.label`), `:60` (values,
  `text.highlight` / `wg.placeholder`) and `:63` (the teleport note), with no guard. These are **window** strings,
  not settings-panel strings. Under the LK-05 shape proposed in `inputs/inventory/lib-fonts-scope.md:264-296`
  (`S.Text(fs, role[, opts])`, gated only with `opts.panel = true`), they are untouched.
  - **Constraint for LK-05:** if LK-05 instead gated `S.Text` on Ignore settings panel unconditionally, every popup
    label and value would go stock under the default Scope. That would be a regression in what the player sees.
  - These tests are the guard. Each boots on the default profile (`ignorePanel = true`) and asserts the token
    colors, so they would go red:
    - `tests/test_frame_skin.lua:94-103` (labels in `wg.label`)
    - `:105-123` (values and placeholders)
    - `:125-135` (the note)
    - `:160-184` (a live repaint)
  - **The degraded `S.Text`** (`core/SkinSetup.lua:346-352`) takes `(fs, role)`. A third `opts` argument is
    ignored harmlessly, so nothing changes.
- **WidgetsReorder, the drag handle, autocomplete, line chart, Toast, sim and perf panels:** not used. Proof:
  `grep -rnE 'ReorderList|WidgetsReorder|DragHandle|AttachDragHandle|Toast|PerfPanel|SimPanel|Autocomplete|LineChart'
  core modules settings` returns nothing. They are loaded only because the XML loads them (`tests/loader.lua:52-64`).
- **The custom library widgets WhatGroup does host** are relevant to LK-06's Scope decision, but none needs addon
  code:
  - **The debug console and its copy window** (`core/DebugLogSetup.lua:209-214`; painted for the owner, pinned by
    `tests/test_skin_tools.lua:127-143`, which runs with `ignorePanel = false` and stays green either way).
  - **The launcher** (`core/LauncherSetup.lua:109`, LibDBIcon minimap button, its tooltip and its menu).
  - **The first-run picker** (`core/SkinSetup.lua:271-291`).
- **No Scope guard exists in the addon at all.** Proof: `grep -rn 'GetIgnore' core modules settings` returns
  nothing. Unlike KickCD's `pageColor` guard, there is no host guard to keep or delete.

### 1d. ResetToSkin guards against the `"@skin"` sentinel (R-6): none

- The addon never calls `ResetToSkin`. Proof: `grep -rnE 'ResetToSkin' core modules settings defaults` returns
  nothing.
- The only `"@skin"` is the degraded facade's `FROM_SKIN` field at `core/SkinSetup.lua:313`, used by its `S.Resolve`
  at `:329-332`. This mirrors the library's `lib.FROM_SKIN = "@skin"` (`libs/LibKa0s/Skin.lua:99`, facade
  `:1015`), so that the degraded surface matches the live one. It is **not** a guard and **stays**.
  `tests/test_surface_parity.lua:231-239` holds it.

### 1e. Reach into `Skin:__DrawsKey` or other internals (R-9): none

- Proof: `grep -rn 'DrawsKey' core modules settings defaults tests/*.lua` returns nothing.
- **Re-vendor knock-on.** If LK-10 puts a public `DrawsKey` on the **owner facade** (`Skin:For(owner)`, built at
  `libs/LibKa0s/Skin.lua:1015-1016` from `lib.VOCAB` at `:107`), then `tests/test_surface_parity.lua:231-239` goes red
  until the name is added to the degraded list at `core/SkinSetup.lua:317-325`, with an honest degraded answer
  (`"ka0s"`). A lib-level `Skin:DrawsKey(owner)` that is not on the facade does not trip the test. The same applies
  to any other facade member v1.81.0 adds. The test compares keys only, so the facade `apiVersion = 3`
  (`core/SkinSetup.lua:313` vs `libs/LibKa0s/Skin.lua:1015`) is not compared, but it should move if the library's
  does.

### 1f. Close-button tint handling (R-3): none

- WhatGroup never calls `S.CloseButton`. Proof: `grep -rnE 'CloseButton\(' core modules settings` returns only the
  `NS.MakeCloseButton` seam at `core/CoreSetup.lua:171-173` (and the degraded stub at `:107`). That seam forwards to
  Core's `lib.MakeCloseButton`, which itself calls `S.CloseButton(b, { own = true })`
  (`libs/LibKa0s/Core.lua:269-307`, the call at `:304`).
- `NS.MakeCloseButton` has **no caller** in the addon (`tests/test_mediasetup.lua:23` says so). The popup's footer
  Close is the skin's `S.Button` (`modules/FrameSkin.lua:65`; `docs/ARCHITECTURE.md:494`). The close marks WhatGroup
  shows belong to the library's windows: the debug console, the copy window, and the picker
  (`libs/LibKa0s/OptionsSkinPicker.lua:644-645`). LK-03 fixes their tint inside the library with no addon change.
- Proof: `grep -rn 'SetVertexColor' core modules settings` returns nothing.

### 1g. Literal tooltip or quality colors standing in for `gtip.*` / `q.*` (R-7, R-8): none

- Proof: `grep -rnE '"q\.|gtip\.' core modules settings defaults locales` returns nothing.
- The addon's one tooltip is the teleport button's spell tooltip (`modules/Frame.lua:546-548`,
  `GameTooltip:SetSpellByID`). It has no color argument, and SKIN-10 keeps it Blizzard's
  (`docs/smoke-tests.md:835-841`).
- Every color literal outside the seam is **chat output** on the gate's allow-list
  (`tests/test_skin_literals.lua:43-64`): the `[WG]` prefix, the chat summary's colors and the command highlights. None
  stands in for a tooltip or a quality color. The gate itself is `tests/test_skin_literals.lua:146-188`.
- WhatGroup hosts no drag handle (LK-08 does not reach it) and reads no `q.*` token (LK-09 does not reach it).

## 2. Where WhatGroup resolves a HUD face or outline itself (R-1): nowhere

- There is no HUD, no `hud.font` / `hud.outline`, no composer font picker with a `fromSkin` companion, and no
  `NS.SkinResolve`. The only `Resolve` is the degraded facade's at `core/SkinSetup.lua:329-332`, which has no Scope
  without the library. Proof:
  `grep -rnE 'S\.Resolve|SkinResolve|\.Resolve\(|hud\.' core modules settings` returns only `core/SkinSetup.lua:329`.
- The docs say so explicitly: `docs/ARCHITECTURE.md:310-312` ("no HUD, so there are no style settings, no `fromSkin`
  companions"). R-4's per-skin `hud.font` therefore changes nothing visible here. The popup draws the body and title
  faces (`font.body` / `font.title`), and SKIN-6's per-skin family list (`docs/smoke-tests.md:812-817`) is about
  those faces, not the HUD face.

## 3. Tests that pin current behaviour

| Test | Pins | Change for v1.81.0 |
|---|---|---|
| `tests/test_skin_picker.lua:202-205` "skin picker: the title names this addon": `assertEqual(window(NS).title:GetText(), "Choose a skin for " .. NS.BRAND_NAME)` | the R-11 title (`NS.BRAND_NAME = "Ka0s WhatGroup"`, `core/CoreSetup.lua:39`; the label reaches the library through `RegisterOwner{ label = NS.BRAND_NAME }`, `core/SkinSetup.lua:371-376`) | **Must change.** Assert the title `"Choose a skin"` and the owner's label `Ka0s WhatGroup` on the new line above the dropdown, read from whatever field LK-11 exposes. Rename the case, for example "the title asks for a skin and the addon's name sits above the dropdown", and regenerate `docs/test-cases.md:745`. `NS.SkinPickerSpec()` (`core/SkinSetup.lua:232-240`) passes no label, so the addon needs **no code change** for R-11. |
| `tests/test_skin_picker.lua:75-95` | `spec.tab == "Appearance"` (the tab key) | Stays. R-10 renames the tab in the standard only; the library's key stays `"Appearance"` (`libs/LibKa0s/OptionsAppearance.lua:3,47,590`, `OptionsSkinPicker.lua:505`). |
| `tests/test_skinsetup.lua:258-283` | strip keys `Master controls \| Notifications \| Appearance \| Keybindings`, label "Skin" | Stays (R-10 is standard-only). |
| `tests/test_frame_skin.lua:85-184` (the popup's strings, Close button and live repaint) | `S.Text` / `S.Button` paint on the default Scope (`ignorePanel = true`) | Stay. These are the guard that LK-05 keeps `S.Text` without opts unscoped (1c). |
| `tests/test_frame_skin.lua:257-269`, `tests/test_skinsetup.lua:341-352` | degraded `S.Text` / facade | Stay. |
| `tests/test_skin_tools.lua:69-93` | Test notification button painted; Ka0s Default paints like every skin; the default Scope leaves it stock | Stay (R-2 keeps the panel switch). |
| `tests/test_skin_tools.lua:127-143` | debug console and copy window painted for the owner (on Obsidian, `ignorePanel = false`) | Stays green whether or not LK-06 puts tool windows under the panel Scope. If LK-06 does, **add** a sibling: with `ignorePanel = true` the console is stock. |
| `tests/test_surface_parity.lua:231-239` | degraded facade carries every live facade key (`core/SkinSetup.lua:317-325`) | **Goes red if v1.81.0 adds a facade member** (LK-10 `DrawsKey`, an LK-01/05 Scope read). Add the name to the degraded list in the WG-RV commit. |
| `tests/test_skinsetup.lua:326-339` | `NS.SKIN_FALLBACK` (`core/SkinSetup.lua:97-105`) equals Ka0s Default | Stays: `win.*`, `title.text`, `divider` and `text.highlight` are not moved by LK-09 (`q.*` only). |
| `tests/test_skin_literals.lua:146-188` | no color literal outside the seam | Stays. |
| `tests/test_libka0s.lua:52-77` | MODULES lists each file at a positive integer minor; the comment at `:64` names the Skin key "7.15.11.5.9.2.4 at v1.80.0" | The assertions stay (minors are only checked > 0). **Roll the comment** to v1.81.0's key. Add a file to the expected list only if the release adds one to a major listed there. |
| `tests/loader.lua:24-118` (`LIBKA0S`, every file of `libs/LibKa0s/LibKa0s.xml` in XML order); comments `:44`, `:99` | the XML order | **Must change if v1.81.0 adds, removes or reorders a library file** (the XML-order check fails otherwise). Roll the `:44` key comment. |
| `tests/test_vendor_sync.lua` (kit `tests/_kit/vendor_sync.lua`) | the payload equals the tag on `CLAUDE.md:48` | Moves with WG-RV (provenance line). |
| `tests/test_mediasetup.lua` (icon declaration `CLAUDE.md:49`: close, copy, clear, eye, settings) | the icon prune | Moves only if LK-11 adds an icon to the picker. |

## 4. Smoke checks and doc passages whose expectation changes

`docs/smoke-tests.md` is 1025 lines, so there is room. Note: `modules/Frame.lua` is 1467 lines, 33 under the cap, but
nothing here touches it.

| Where | Today | After v1.81.0 | Ruling |
|---|---|---|---|
| **SKIN-18** `docs/smoke-tests.md:873-881`, title at `:875` | "a small window titled **Choose a skin for Ka0s WhatGroup** opens ..." | "titled **Choose a skin**, with **Ka0s WhatGroup** on its own line above the dropdown, never cut off". Fail clause: a truncated name, or a title that still carries the name. | R-11 |
| **SKIN-22** `:901-907` | "one picker opens, naming one addon" | Still true (the name is now the line above the dropdown). Optionally say "its name line reads one addon". | R-11 |
| **SKIN-8** `:821-829` | Scope on/off on a **non-default** skin | Unchanged as written. **Add** a clause: untick Ignore settings panel on **Ka0s Default** → General's tab strip and page panel wear the Ka0s look, no longer the stock tab art (`libs/LibKa0s/OptionsTabs.lua:495,503` lose `stock`). | R-2 |
| **SKIN-9** `:830-834` | on Azeroth with the default Scope, the console and Copy window wear the skin | Unchanged **unless LK-06 puts library tool windows under the panel Scope**. If it does, the check needs "with Ignore settings panel off", plus a "stock with it on" clause, because the default Scope would leave the console stock. **Depends on LK-06.** | R-5 |
| **SKIN-10** `:835-841` | "the minimap button, its hover tooltip and its right-click menu all look as they did before the run" | If LK-06 skins the launcher's tooltip and menu ("launcher" is on LK-06's list, `00_PLAN.md`), they wear the skin, so this check must move them out of the "stays Blizzard's" list and say under which Scope. **Depends on LK-06.** | R-5 |
| **SKIN-17** `:866-872` | Ignore fonts → every popup string in the game's face | Unchanged (the popup is not HUD; `S.Text` already obeys it). | R-1 |
| **SKIN-6** `:812-817` | per-skin popup families; WoW Default in Friz Quadrata | Unchanged: these are body and title faces, not `hud.font`. Only if LK-04 also gives **WoW Default** a body face does this change; check the release notes. | R-4 |
| **SKIN-1** `:769-780`, SKIN-2 `:781-791`, SKIN-20 `:888-894` | Ka0s Default popup look; tab labeled Skin (fail if "labeled Appearance"); the close mark | Unchanged. SKIN-20's close mark gets LK-03's tint restore with no visible change on a single skin. | — |
| Pending sign-off `:1009-1025` | lists SKIN-1..24 as owed | Add the amended checks (SKIN-18, and SKIN-8/9/10 as they move), citing this bundle. | — |

Docs:

- `docs/test-cases.md:745`: regenerate from `lua tests/run.lua --list` after the R-11 test rename
  (`tests/run.lua:14`).
- `docs/ARCHITECTURE.md:330-337` (the first-run picker paragraph) does not quote the title. Optionally add "titled
  *Choose a skin*, the addon's name above the dropdown" (R-11).
- `docs/ARCHITECTURE.md:338-344` ("Owners on every library surface"): add the Scope behaviour of the console, copy
  window and launcher if LK-06 changes it (R-5).
- `docs/settings-panel.md:546` names "LibKa0s v1.80.0" as the version drawing the Skin tab. Roll it to v1.81.0 with the
  re-vendor.
- `docs/settings-panel.md:555-556` (Scope: "the popup and the debug console still wear the skin" with Ignore settings
  panel on) and `:390` (the same in the row table) become wrong for the console **if LK-06 scopes it**.
- `docs/settings-panel.md:568-580` ("What the tab skins when the Scope lets it"): add that under Ka0s Default the tab
  strip is the Ka0s look too (R-2), since this passage describes Ignore settings panel off.
- `docs/settings-panel.md:391`, `docs/schema.md:41`, `docs/ARCHITECTURE.md:305-306` (Ignore fonts: "every string
  keeps the game's face"): true already. No HUD, so R-1 adds nothing.
- Optional comment rewording for R-10 (the standard renames the tab "Skin"): `core/SkinSetup.lua:27,63,379,413` say
  "Appearance row" or "Appearance tab". The key stays `Appearance` (`core/SkinSetup.lua:237`,
  `settings/Schema.lua:318-372`, `settings/OptionsSetup.lua:165-171`), so this is comment-only and optional.
- `README.md`: the Skins credits (`README.md:104-124`) name the eight faces the popup draws. They change only if LK-04
  brings a **new** font file into the payload for a HUD face. WhatGroup draws no HUD, but the payload ships the file
  and the README credits shipped faces (`README.md:121-124`: "The fonts and the icons are bundled inside the LibKa0s
  payload"). **If LK-04 adds an OFL face, add its credit.**
- `CLAUDE.md:48` provenance line → `v1.81.0`. `CLAUDE.md:49` icon declaration changes only if LK-11 adds an icon.

## 5. Current state

- Branch: `master`, tracking `origin/master`, **clean** (`git status --porcelain` printed 0 lines). HEAD `d8e52f4`
  "Merge feat/2026-10-29-skinning-rollout: the LibKa0s skinning rollout". No other local branches.
- Vendored LibKa0s: **v1.80.0** (`CLAUDE.md:48`: "Bundles [LibKa0s](...) v1.80.0 (MIT)."). Icons: `CLAUDE.md:49`
  "LibKa0s icons: close, copy, clear, eye, settings." (The LibKa0s checkout is on `master` at `ea1d92d`, newest tag
  `v1.80.0`.)
- Gate on master, run 2026-10-30:
  - `~/.claude/dev-copilot/bin/ka0s-bounded lua tests/run.lua` (tail):
    `1025 passed, 0 failed, 1 skipped, 1026 total`. The skip is the kit's diagnostics-contract opt-out case ("this
    addon keeps the default ... the case above holds it"), which is expected.
  - `~/.claude/dev-copilot/bin/ka0s-bounded luacheck .`: `Total: 0 warnings / 0 errors in 69 files`.
  - **Green.**

## 6. Nothing to change: exceptions rows (WG-01)

WG-01 has nothing to delete. Proposed `exceptions.tsv` rows, each run from the WhatGroup root:

| Claim | Proof command (expected: no output) |
|---|---|
| no `stockDefault` / `stock` caller (R-2) | `grep -rnE 'stockDefault\|stock *=' core modules settings defaults locales` |
| no HUD face/outline resolution and no Ignore-fonts patch (R-1) | `grep -rnE 'hud\.(font\|outline)\|GetIgnore\|FontsIgnored\|IgnoreFonts\|SkinResolve' core modules settings defaults locales` |
| no hand-rolled Scope guard, no custom-widget use (R-5) | `grep -rnE 'GetIgnore\|ReorderList\|WidgetsReorder\|DragHandle' core modules settings` |
| no `ResetToSkin` call (R-6) | `grep -rnE 'ResetToSkin' core modules settings defaults` |
| no `__DrawsKey` reach-in (R-9) | `grep -rn 'DrawsKey' core modules settings defaults tests/*.lua` |
| no close-button tint handling (R-3) | `grep -rnE 'SetVertexColor\|S\.CloseButton\|Skin\.CloseButton' core modules settings` |
| no literal stand-ins for `gtip.*` / `q.*` (R-7, R-8) | `grep -rnE '"q\.\|gtip\.\|GetItemQualityColor\|ITEM_QUALITY' core modules settings defaults locales` |

(The `\|` in the table cells is `|` on the command line.)

What WG still owes:

- **WG-RV:**
  - The payload, from `git archive v1.81.0`.
  - `CLAUDE.md:48`.
  - `tests/loader.lua`'s file list and its `:44` comment, plus the `tests/test_libka0s.lua:64` comment.
  - Any new facade name in `core/SkinSetup.lua:317-325`.
  - `docs/settings-panel.md:546`.
  - The README font credit if LK-04 adds a face.
- **WG-02:**
  - The R-11 test (`tests/test_skin_picker.lua:202-205`) and `docs/test-cases.md:745`.
  - SKIN-18, plus SKIN-8 for R-2.
  - SKIN-9, SKIN-10 and the settings-panel Scope sentences, conditional on LK-06's Scope call.
  - The pending sign-off list.
