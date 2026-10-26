# LibKa0sSkinTester Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** A Ka0s addon, `LibKa0sSkinTester`. Typing `/st` or `/skintester` opens a skin selector and a
showroom window that paints every element a Ka0s skin can paint, one skin at a time.

**Architecture:**
- **Scaffold.** `/dev-copilot:wow-new-addon` scaffolds a fully compliant addon that vendors LibKa0s
  v1.78.0.
- **Owner.** The addon registers as skin owner `LibKa0sSkinTester` and keeps its skin choice in AceDB.
- **Selector.** Swatch cards call `Skin:SetChoice` and write the choice back to the profile.
- **Showroom.** A window of sections. Each section builds its sample frames and paints them through one
  wrapper, `NS.Showroom:Paint(name, target, ...)`. The wrapper calls the owner's facade and records which
  primitive names were used, so a headless test can hold that set to `lib.VOCAB`.
- **Value displays.** Getters and `sem.*` colors are drawn from tokens and redrawn on
  `Skin:OnLooksChanged`.

**Tech Stack:**
- Lua 5.1, WoW Retail API (`## Interface` per the scaffold).
- Ace3 (AceAddon, AceDB, AceConsole, AceGUI, AceConfig).
- LibKa0s v1.78.0: `LibKa0s-Skin-1.0`, `LibKa0s-Widgets-1.0`, `LibKa0s-Options-1.0`, the Core window shell.
- The vendored test kit, revision 43, including `mock_paint.lua`.

**Spec:** `docs/2026-10-26-SKIN_TESTER/00_DESIGN.md` (Ka0sAddonsCommonTasks). Executors read both.

## Global Constraints

- **Repository:** `../LibKa0sSkinTester` (sibling of this repo), default branch `master`. GitHub
  `tusharsaxena/LibKa0sSkinTester`, public.
- **Identity:** folder and owner name `LibKa0sSkinTester`; label and TOC title `Ka0s Skin Tester`;
  SavedVariables `LibKa0sSkinTesterDB`.
- **Slash:** `/st` and `/skintester`.
- **CurseForge:** never published. The TOC omits `X-Curse-Project-ID` and carries, in its position,
  `# X-Curse-Project-ID: never published on CurseForge (a developer showroom for the Ka0s skins)`.
- **LibKa0s:** vendored from the local tag `v1.78.0` (`7bc3e9b` today), never checked out. Re-vendored
  with LootHistory at every later re-cut.
- **Skins listed:** the nine Ka0s skins, in `Skin:Skins()` order. EllesmereUI is never offered.
- **Painting:** every skinnable sample is painted only through `Skin:For("LibKa0sSkinTester")` or the
  library's own widgets. The tester's own drawing is limited to the value displays.
- **Settings panel:** no library Appearance tab, and no "Copy to every Ka0s addon" anywhere.
- **Green gate:** `lua tests/run.lua` and `~/.claude/dev-copilot/bin/ka0s-bounded luacheck .`, both 0/0,
  and no authored file over 1500 lines.
- **Commits:** subjects start `ST-NN: `. The cross-repo feature branch is `feat/2026-10-26-skin-tester`.
  The scaffold's birth commit lands on the new repo's `master`, because a new repo has no other branch
  to start from.

## Review Focus

1. **A skin change while the window is closed.** The window opened afterwards must show the current
   skin. Pinned in Task 4: `showroom: opened after a skin change, it wears the new skin`.
2. **A `/reload` on a non-default skin.** The tester must open on the saved skin, not Ka0s Default.
   Pinned in Task 3: `selector: the saved skin is applied at load`.
3. **An unknown or stale saved key,** for example a skin later renamed. The tester must fall back to Ka0s
   Default without an error. Pinned in Task 3: `selector: an unknown saved skin falls back to ka0s`.
4. **Clicking the card of the skin already chosen.** This must be a no-op: no repaint, no error. Pinned
   in Task 3: `selector: clicking the current card does nothing`.
5. **`/st` owned by another addon.** `/skintester` must still open the window, and the collision must be
   reported once. Pinned in Task 7.

---

### Task 1 (ST-01): Scaffold the addon and its GitHub repo

**Files:** everything `/dev-copilot:wow-new-addon` writes in `../LibKa0sSkinTester`.

**Interfaces:**
- Produces: the scaffold's namespace `NS` (the addon's `select(2, ...)` table), its AceAddon object, its
  settings registration, its launcher, and its primary window module. Later tasks fill that window.
  Each later task names the scaffold file it edits, taken from the scaffold's own module map
  (`docs/module-map.md`).

- [ ] **Step 1:** Run `/dev-copilot:wow-new-addon` with these inputs:
  - name `LibKa0sSkinTester`, title `Ka0s Skin Tester`, slash `st` and `skintester`;
  - a primary window ("Show window", the showroom), no lock and no test mode;
  - LibKa0s icons `close`, `info`;
  - not published on CurseForge, with the TOC comment above.
- [ ] **Step 2:** Run the green gate. Expect 0 failed and luacheck 0/0.
- [ ] **Step 3:** Commit on `master` as `ST-01: Scaffold Ka0s Skin Tester, born compliant`.
- [ ] **Step 4:** Create the GitHub repo and push `master`:
  `gh repo create tusharsaxena/LibKa0sSkinTester --public --source . --push`. Expect the repo URL to be
  printed and `origin/master` to exist.
- [ ] **Step 5:** `git checkout -b feat/2026-10-26-skin-tester`.

### Task 2 (ST-02): Put the addon on the roster

**Files:** Modify `../WowAddonStandards/standards/ADDONS.md` (the in-scope table), on branch
`feat/2026-10-26-skin-tester`.

- [ ] **Step 1:** Add the row, in alphabetical position by addon name:
  `| Ka0s Skin Tester | ../../LibKa0sSkinTester/ | https://github.com/tusharsaxena/LibKa0sSkinTester | Enabled · Show window (the skin showroom) |`
  Then add one sentence under the table: the tester is a roster addon that is never published on
  CurseForge.
- [ ] **Step 2:** `git grep -n -i "fifteen\|15 addons\|15 roster"` across the standard. Update every count
  claim that names the roster size.
- [ ] **Step 3:** Run `bash scripts/check-standard.sh`. Expect `all checks passed`.
- [ ] **Step 4:** Commit as `ST-02: Add Ka0s Skin Tester to the roster (never on CurseForge)`.

### Task 3 (ST-03): Skin owner and the selector

**Files:**
- Create: `modules/SkinChoice.lua` (the owner registration and the profile read and write) and
  `modules/Selector.lua` (the swatch row).
- Modify: the TOC load list, and the AceDB defaults: `profile.skin = { source = "ka0s", skin = "ka0s" }`.
- Test: `tests/test_selector.lua`.

**Interfaces:**
- Produces:
  - `NS.SkinChoice.OWNER = "LibKa0sSkinTester"`.
  - `NS.SkinChoice.Facade()`, which answers `Skin:For(OWNER)`.
  - `NS.SkinChoice.Current()`, which answers the skin key.
  - `NS.SkinChoice.Pick(key)`, which answers `changed`.
  - `NS.Selector.Build(parent)`, which answers the frame (`frame.cards[key]`, with `card.key` and
    `card.selected`).
- `Pick` calls `Skin:SetChoice(OWNER, "ka0s", key)`. When that answers changed, it writes
  `profile.skin.skin = key`.
- Registration passes `get`, `set`, `label = "Ka0s Skin Tester"`.

- [ ] **Step 1: Write the failing tests.**
  - `selector: one card per Ka0s skin, in Skins() order`: `#cards == 9`, and the keys equal the
    `Skin:Skins()` keys in order.
  - `selector: clicking a card applies and saves the skin`: after a click on `obsidian`,
    `Skin:GetChoice` answers `"ka0s","obsidian"`, `profile.skin.skin == "obsidian"`, and only the
    obsidian card is selected.
  - `selector: the saved skin is applied at load`: with `profile.skin.skin = "glass"` and the addon
    loaded, the choice is `"glass"`.
  - `selector: an unknown saved skin falls back to ka0s`: with the saved value `"nope"`, the choice is
    `"ka0s"` and nothing raises.
  - `selector: clicking the current card does nothing`: a click on the current card answers changed
    false, and `Skin:Repaint` is not called (spy).
  - `selector: no EllesmereUI card and no copy button`: no card key is `"eui"`, and no frame under the
    selector carries the library's copy label.
- [ ] **Step 2:** Run `ka0s-bounded lua tests/run.lua`. Expect the six to fail.
- [ ] **Step 3:** Implement `SkinChoice` and `Selector`. Each card shows the skin's `label` and its four
  `swatches` (from `Skin:Skins()`). The selected card wears `text.accent` through the facade
  (`S.Card` / `S.StateButtonLabel`).
- [ ] **Step 4:** Run the gate. Expect green.
- [ ] **Step 5:** Commit as `ST-03: Skin owner and the swatch selector`.

### Task 4 (ST-04): The showroom window and its paint wrapper

**Files:**
- Create: `modules/Showroom.lua` (the section registry, the paint wrapper and the layout, in a scroll
  body).
- Modify: the scaffold's primary-window module, so it hosts the selector on top and the showroom below.
- Test: `tests/test_showroom.lua`.

**Interfaces:**
- Produces:
  - `NS.Showroom:Paint(name, target, ...)`. It calls `NS.SkinChoice.Facade()[name](target, ...)`, sets
    `NS.Showroom.used[name] = true`, and answers what the primitive answered.
  - `NS.Showroom:AddSection(key, title, build)`. `build(body, paint)` answers its height, where
    `paint = function(name, ...) return NS.Showroom:Paint(name, ...) end`. Sections are laid out in
    registration order.
  - `NS.Showroom:Caption(parent, text)`, which answers a FontString painted `S.Text(fs, "muted")`.
- The window itself is painted with `Shell`, `TitleBar`, `CloseButton` and `Footer` through `Paint`.

- [ ] **Step 1: Write the failing tests.**
  - `showroom: the window is painted through the wrapper`: after the window opens, `used.Shell`,
    `used.TitleBar`, `used.CloseButton` and `used.Footer` are all true.
  - `showroom: opened after a skin change, it wears the new skin`: pick `ember` while the window is
    closed, then open it. With the paint recorder (`mock_paint.lua`), the shell's backdrop color equals
    `Skin:Color(OWNER, "win.bg")` under ember.
  - `showroom: a skin change repaints every sample`: open the window, pick `contrast`, and every frame
    recorded under `NS.Showroom` shows a recorder entry after the pick.
- [ ] **Step 2:** Run. Expect FAIL.
- [ ] **Step 3:** Implement. The window is toggled by the scaffold's Show window handler, `/st` and the
  key binding.
- [ ] **Step 4:** Run the gate. Expect green.
- [ ] **Step 5:** Commit as `ST-04: The showroom window and its paint wrapper`.

### Task 5 (ST-05): The sections: every primitive

**Files:**
- Create: `modules/ShowroomChrome.lua`, `ShowroomControls.lua`, `ShowroomLists.lua`, `ShowroomText.lua`,
  `ShowroomPanels.lua`, `ShowroomOverlays.lua`. Each calls `NS.Showroom:AddSection` once.
- Test: `tests/test_showroom_coverage.lua`.

**Interfaces:**
- Consumes: `AddSection`, `Paint`, `Caption` (Task 4); the library widgets `W.SearchBox`, `W.Dropdown`,
  `W.TestStrip` with `opts.owner = OWNER`.
- Section contents, exactly as the spec lists them. Each sample is captioned with its primitive and
  state, for example `Button (primary)`:
  - **Chrome:** Tab ×3 with SetTabSelection.
  - **Controls:** Button normal, primary and disabled; WhiteButtonLabel; StateButtonLabel on and off;
    PageButton prev and next; SquareIcon; EditBox via `W.SearchBox` with a hint; Dropdown via
    `W.Dropdown`; Checkbox checked and unchecked; Slider.
  - **Lists:** SortHeaderBar; ListRow plain, stripe, hover and selected; ScrollBar.
  - **Text:** Text in all nine roles; Font; White.
  - **Panels:** Panel; Inset; Card; Divider; Drawer open and closed; Strip test and sim; Cover;
    NavItem selected and not.
  - **Overlays:** Tooltip on a library-owned tooltip frame shown on hover; MenuFrame (the dropdown's
    menu, plus a standing sample); a confirm popup (a plain frame painted Shell plus Button, never a
    StaticPopup); `W.TestStrip`; FadeRegions on a `UIPanelButtonTemplate` button beside a plain one;
    FadeNineSlice on a NineSlice frame beside a plain one; IconBorder; ApplyBarFill on a StatusBar.

- [ ] **Step 1: Write the failing test** `showroom: every lib.VOCAB name is shown`. Open the window,
  then for each `name` in `LibStub("LibKa0s-Skin-1.0").VOCAB` assert
  `NS.Showroom.used[name] or NS.Values.shown[name]`. The failure message lists the missing names.
- [ ] **Step 2:** Run. Expect FAIL, listing the primitives not yet shown.
- [ ] **Step 3:** Implement the six section files.
- [ ] **Step 4:** Run. Expect only the getter names still missing (Task 6 shows them).
- [ ] **Step 5:** Commit as `ST-05: Showroom sections for every paint primitive`.

### Task 6 (ST-06): Value displays: getters and semantic colors

**Files:**
- Create: `modules/ShowroomValues.lua`.
- Test: `tests/test_showroom_values.lua`.

**Interfaces:**
- Produces: `NS.Values.shown`, a set of the names this section displays. It holds `GetAccentColor`,
  `GetPanelColor`, `GetFont`, `GlowColor`, `ChartStyle` and `BarStyle`.
- Each display is a labeled swatch (`SetColorTexture`). `GetFont` shows a sample line in that face.
  `BarStyle` shows a sample bar with its texture. `ChartStyle` shows its series as a row of swatches.
- The `sem.*` lines read every token key starting `sem.` from `Skin:ResolveSkin(Current())`, sorted, each
  through `Skin:Color(OWNER, key)`.
- Everything redraws in a `Skin:OnLooksChanged(OWNER, fn)` handler.

- [ ] **Step 1: Write the failing tests.**
  - `values: every getter is displayed`: each of the six names is in `NS.Values.shown`.
  - `values: every sem token has a line`: the number of `sem.` lines equals the number of `sem.` keys in
    the resolved table, which is at least 20.
  - `values: a skin change redraws them`: pick `azeroth`, and the `sem.good` line's text color equals
    `Skin:Color(OWNER, "sem.good")` under azeroth.
- [ ] **Step 2:** Run. Expect FAIL.
- [ ] **Step 3:** Implement.
- [ ] **Step 4:** Run the gate, including the Task 5 coverage test. Expect all green.
- [ ] **Step 5:** Commit as `ST-06: Value displays for the getters and every sem token`.

### Task 7 (ST-07): The settings panel sample page and the `/st` collision

**Files:**
- Modify: the scaffold's settings files. Add a page `Sample controls` holding a heading, a checkbox, a
  slider, a dropdown and a color swatch, bound to `profile.sample.*`. The page has no Appearance tab.
- Modify: the scaffold's slash registration.
- Test: `tests/test_settings_sample.lua`, `tests/test_slash.lua`.

**Interfaces:**
- Consumes: the scaffold's Options instance.
- The page's AceGUI widgets are painted with `Skin:PaintAceTree(OWNER, container)`.
- The collision check runs at `PLAYER_LOGIN`. If `SlashCmdList` already holds a handler for `/st` that is
  not this addon's, the addon prints one tagged line naming `/skintester` and keeps only `/skintester`.

- [ ] **Step 1: Write the failing tests.**
  - `settings: the sample page wears the owner's skin`: pick `obsidian`, open the page, and the
    checkbox's box color equals `check.bg` under obsidian.
  - `settings: no Appearance tab and no copy button`: no tab label `Appearance` or `Styles` exists, and
    no copy-label widget exists.
  - `slash: /skintester opens the window`.
  - `slash: a foreign /st is reported once and left alone`: pre-seed `SLASH_OTHER1 = "/st"`, then load.
    Exactly one chat line is printed, `/st` still calls the other handler, and `/skintester` opens the
    window.
- [ ] **Step 2:** Run. Expect FAIL.
- [ ] **Step 3:** Implement.
- [ ] **Step 4:** Run the gate. Expect green.
- [ ] **Step 5:** Commit as `ST-07: Sample settings page; /st collision reported once`.

### Task 8 (ST-08): Docs, smoke file, push

**Files:**
- Modify: the scaffold's README, `docs/ARCHITECTURE.md`, `docs/smoke-tests.md` and the generated
  `docs/test-cases.md`, all to match.
- Create: `docs/2026-10-26-SKIN_TESTER/02_SMOKE_TESTS.md` and `99_REPORT.md` (this repo).

- [ ] **Step 1:** Run `/dev-copilot:sync-docs` in the tester repo, as a content sync.
- [ ] **Step 2:** Write `02_SMOKE_TESTS.md`. Every row starts with Result blank, and only the owner fills
  it in. The rows:
  - ST-S1: symlink the addon and restart the client, then `/st`.
  - ST-S2: each card repaints the window.
  - ST-S3: the choice survives a `/reload`.
  - ST-S4: every section is legible in each skin, with illegible ones recorded as skin defects.
  - ST-S5: the settings sample page follows the skin.
  - ST-S6: combat open and switch.
  - ST-S7: `/skintester`, and `/st` with any collision line.
  - ST-S8: the minimap button and the key binding.
  - ST-S9: with Loot History installed, both addons look the same on the same skin.
- [ ] **Step 3:** Run the gate in the tester repo, and `check-standard` in WowAddonStandards.
- [ ] **Step 4:** Commit and push `feat/2026-10-26-skin-tester` in LibKa0sSkinTester, WowAddonStandards
  and this repo. Then stop for the owner's smoke test; merging waits for the go-ahead.
