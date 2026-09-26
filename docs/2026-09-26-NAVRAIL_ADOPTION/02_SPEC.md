# NavRail adoption: the MultiMeters Windows page (#55) and the KickCD Grid page (#33)

- **Date:** 2026-09-26
- **Status:** design decided by the owner on 2026-09-26. The owner waived spec and plan review and
  asked for the build to run straight through, as with AuraMaster. This addendum writes the owner's
  text down in the AuraMaster spec's shape and resolves the points it leaves open (§9).
- **Issues:** MultiMeters#55, KickCD#33.
- **Pattern:** AuraMaster's shipped redesign (#6). Spec
  `../AuraMaster/docs/superpowers/specs/2026-09-26-settings-redesign-design.md`; plan and record
  `../2026-09-26-SETTINGS_REDESIGN/03_EXECUTION_PLAN.md` and `99_REPORT.md`; code on AuraMaster
  `master` `b51aee8`, `settings/OptionsSetup.lua` (the section registry :184-209,
  `Helpers.RenderContainerPage` :546-568, `SelectSection` :575-589, the `SelectTab` route :594-598,
  `NS.OpenOptionsPage` :313-331).
- **Library:** LibKa0s v1.61.0 (published; tag `v1.61.0` on `c6183bd`). `O.NavRail(ctx, spec)`,
  in `OptionsNav.lua` minor 1.
- **Standard:** v2.69.0 (published). options-ui-§13 sanctions the rail; options-ui-§14 puts the band
  above the rail and the strip and says the rail is not a picker.

## 1. What the owner asked for

- The pattern AuraMaster shipped goes to MultiMeters and KickCD: a pinned band on top holding the one
  picker, a pinned nav rail on the left for the first level, and each entry's own pinned tab strip
  to its right for the second, over the one scroll.
- **MultiMeters (#55):** the Windows page becomes the one page per window. The six window sub-pages
  fold into it.
- **KickCD (#33):** a new Grid page replaces the Icons, Cast bar and Text Label pages.
- **First, the re-vendor:** every addon except AuraMaster takes LibKa0s v1.61.0.

## 2. The shared design

Both pages follow AuraMaster's Containers page exactly where the two apply.

```
┌────────────────────────────────────────────────────────────────────────┐
│ <the one picker: Active window / Unit>                  (band, pinned) │
├───────────────┬────────────────────────────────────────────────────────┤
│ Entry 1       │ [Tab A] [Tab B] [Tab C]                (strip, pinned) │
│ Entry 2 ◄     ├────────────────────────────────────────────────────────┤
│ Entry 3       │  the selected entry's selected tab                     │
│ …             │  (the page's own scroll: the only thing that moves)    │
│ (rail, 120)   │                                                        │
└───────────────┴────────────────────────────────────────────────────────┘
```

- **Draw order is `PageBanner` -> `NavRail` -> `TabStrip`** on every full render. The rail reads the
  band the banner reserved, and the strip reads the inset the rail recorded (`LibKa0s/OptionsNav.lua`,
  `O.NavRail`'s docstring).
- **A rail entry is a former page key.** Its rows keep `page`, their paths and their defaults, so
  the CLI, profiles and the resets are untouched.
- **Session state only.** `ctx.activeSection` and `ctx.sectionTabs[entry]` (per-entry tab memory)
  live on the ctx and are never persisted (options-ui-§13). The tab is stashed **before anything
  moves the entry**: a rail click, a deep link or a render. That catches the library's own strip
  clicks, which never call back into the host (AuraMaster plan, A6).
- **Changing the instance in the band keeps the entry and its tab** (options-ui-§14, "The rail is not
  a picker").
- **The rail is refused in combat by the library** (`dressEntry`'s `O.__combatRefused()`), and the
  combat cover covers it. Hosts add no guard of their own.
- **Width 120**, the library default, so no host passes a width.

## 4. Library: the v1.61.0 re-vendor (all ten addons)

- Copy `LibKa0s/` from the tag `v1.61.0` into `libs/LibKa0s/`, exactly as SR-AM-01 did. Between
  v1.60.0 and v1.61.0 only four files change: `LibKa0s.xml` (+1 line), `Options.lua` (minor 24 -> 25),
  `OptionsTabs.lua` (minor 4 -> 5) and the new `OptionsNav.lua` (minor 1). The Options major key goes
  from `24.31.4.7.4` to `25.31.5.7.4.1`.
- `testkit/` is byte-identical at both tags (kit revision 27), so `tests/_kit/` is **not** copied.
  The dry run confirmed that each addon's `tests/_kit` equals the tag's `testkit`.
- The only new public Options member is `NavRail`. Each host's library-absent stub gains a `NavRail`
  no-op so the Options surface-parity case stays green. ConsumableMaster is the exception: its stub
  projects a named `OPTIONS_SEAM` list that does not include `NavRail`, so its fix is its
  `tests/test_libka0s.lua` inventory instead (R18).
- Four hosts spell their library list out by hand, contrary to the v1.61.0 CHANGELOG's claim that an
  XML-derived list needs no change. WhatGroup's `tests/loader.lua` and LootHistory's
  `tests/test_libka0s.lua` gain `OptionsNav.lua`. ConsumableMaster's `tests/test_libka0s.lua` Options
  inventory gains the file and its paired minor. KickCD's `tests/test_options_panel.lua` Options-file
  count goes from 5 to 6.
- The CLAUDE.md provenance line reads v1.61.0. Docs that state the version vendored now roll with
  it, and historical mentions ("introduced in v1.60.0") stay.
- With no rail drawn, the inset is 0 and every other page is laid out byte-identically.

## 5. Standard

No change. v2.69.0 already sanctions both pages. One owner decision departs from it, KickCD's
Defaults scope (§B3, R8). It is recorded as a ratified deviation in KickCD's register, and NR-REC-01
lists it as a candidate for the standard.

---

## A. MultiMeters: the Windows page (#55)

### A1. What changes in the tree

General · Windows · Profiles. Frame, Header, Bars, Tooltip, Visibility and Columns leave the tree, and
the D6 nesting mark (`NS.SubPageLabel`, `settings/OptionsSetup.lua:94-106`) goes with them. There is
nothing left to nest.

### A2. The page

- **Band:** the Active window picker, `H.WindowBanner` (`settings/Windows.lua:218-244`), unchanged. It
  is full width above the rail and the strip. It is the only picker, and `NS.State.activeWindowId`
  stays the one selection, written only through `NS.State.SetActiveWindow`.
- **Rail:** General · Frame · Header · Bars · Tooltip · Visibility · Columns, keyed by page key
  (`windows`, `frame`, `header`, `bars`, `tooltip`, `visibility`, `columns`), never by label: "General"
  is also the addon page's name and the first tab of Frame and Tooltip. Each entry has a tooltip.
- **General (key `windows`):** one tab, named General (options-ui-§14's General-acts escape: General
  is the rail's first entry, and the page opens on it). It holds two headed blocks:
  - **Window:** the name box (Enter renames), New window, Duplicate window, Delete window (confirmed).
  - **Copy settings from** (the owner's ruling: the former Copy from tab, folded in): the source
    window picker, Settings to copy (the group filter) and Copy.
- **Frame, Header, Bars, Tooltip, Visibility:** each entry's strip is its former page's
  `RenderTabbedSchema` strip, unchanged.
- **Columns:** its bespoke three-tab strip (Columns, Header text, Header background) and the block
  editor, unchanged. RenderTabbedSchema's host tabs stay declined (issue #53).

### A3. What changes, and what does not

- **Schema:** unchanged. No row's `path`, `page`, `group`, `default` or `label` moves. `/mm get`,
  `/mm set`, `/mm list`, `/mm reset`, profiles, `WindowManager:CopyFrom` and `CONFIG_CHANGED`
  sections are untouched.
- **Session state:** `ctx.activeSection`, `ctx.activeTab` and `ctx.sectionTabs`. None is persisted.
- **The Columns reorder cancel:** `NS.CancelReorder(ctx)` runs **first** in every Windows-page render,
  before `ClearScroll`. The seven entries share one ctx, and a rail click, a window switch or a tab
  click all clear the scroll. The call is a no-op when nothing is being dragged.
- **Defaults:** the Windows page gains the Defaults button (it declined one before). A click reads
  `ctx.activeSection` **at click time**, because `EnsureDefaultsButton` captures the handler once, at
  the first show. The rows resolve against the active window through `NS.GetSetting`/`NS.SetByPath`,
  so a row walk resets **only the active window**.
  - Frame, Header, Bars, Tooltip and Visibility: `H.RestoreDefaults(entry, ctx)`, the rows the
    sub-page's own button restored.
  - Columns: its own pair in one bulk bracket, the shipped column list plus the `columnHeader` rows,
    exactly as the sub-page's button did.
  - General: nothing (R1).
  - There is one tooltip, worded to fit every entry. It is captured once, like the handler.
- **Deep links:** `NS.OpenOptionsPage(key)` is new. A former sub-page key opens Windows at that entry,
  `windows` keeps the entry the player left, and any other key opens its own page.
  `Helpers.SelectSection(key, tab)` is the one seam that moves the entry (refused in combat). The
  host's `Helpers.SelectTab` routes an entry key to it, so a link written against a page key still
  lands.
- **Wording that names a retired page** is rewritten to "Windows > X": the band tooltip ("every other
  page"), the column refusal, the Scale, Opacity and Lock descriptions, and the statistic-colors note.

### A6. MultiMeters changes, by file

- `settings/OptionsSetup.lua`: the section registry above the fork (`NS.RegisterWindowSection`,
  `NS.WindowSection`, `SECTION_ORDER`); the live arm gains `Helpers.RenderWindowPage`,
  `Helpers.RestoreActiveSection`, `Helpers.__bindWindowsPage`, `Helpers.SelectSection`, the
  `SelectTab` route, category capture and `NS.OpenOptionsPage`; the stub gains their no-ops; the D6
  block and `NS.SubPageLabel` go.
- `settings/Windows.lua`: the General section (one tab, two blocks) replaces the Window / Copy from
  pair; the page builds with Defaults and renders through `RenderWindowPage`.
- `settings/Frame.lua`, `Header.lua`, `Bars.lua`, `Tooltip.lua`, `Visibility.lua`: each registers its
  section, and after NR-MM-04 registers nothing else. The files stay, so the TOC and the load-order
  tests keep their shape.
- `settings/Columns.lua`: the section's strip and body become a render hook, and its Defaults pair a
  defaults hook. The sub-page goes in NR-MM-04.
- `locales/enUS.lua`: rail tooltips, the Defaults tooltip, General's no-restore line and "Source
  window" are added; retired keys are removed with their last caller; reworded keys are renamed.
- Tests: `tests/test_windows_rail.lua` (new), `test_options_panel.lua`, `test_columns.lua`,
  `test_degraded.lua`, `test_surface_parity.lua`, `test_schema_paths.lua`.
- Docs: `docs/settings-panel.md`, `docs/common-tasks.md`, `docs/module-map.md`,
  `docs/ARCHITECTURE.md`, `README.md`, `docs/schema.md`, `docs/smoke-tests.md` (a new §36),
  `docs/test-cases.md`.

### A7. Out of scope

The General (addon) page and Profiles. Any change to what a setting does. The header gear's
destination (R3). Moving the create control into the band (the owner kept the band to the picker).

### A8. Smoke checks

MM-S1 … MM-S11 in `06_SMOKE_TESTS.md`, copied to MultiMeters' `docs/smoke-tests.md` §36 by NR-MM-04.

---

## B. KickCD: the Grid page (#33)

### B1. What changes in the tree

General · Grid · Spells · Profiles. Icons, Cast bar and Text Label leave the tree.

### B2. The page

- **Band:** the Unit picker, today's `L["Unit"]` `PageBanner` in `Helpers.RenderUnitPanel`
  (`settings/Panel_Render.lua:113-130`), unchanged. It is the one picker, shared by all three
  entries, writing `NS.State.viewedUnit` through `Helpers.SetViewedUnit`. It is session-only, as it
  is today.
- **Rail:** Icons · Cast bar · Text Label (keys `icons`, `castbar`, `label`), each with a tooltip.
  There is no General entry: the page has no page-wide act besides the picker, so options-ui-§14's
  escape does not apply, and the page opens on Icons.
- **Each entry's strip** is its former page's strip: Icons has 6 tabs, Cast bar 8 and Text Label 3.

### B3. What changes, and what does not

- **Schema:** unchanged. Every row keeps `panel`, `section`, `unit` and its `units.<unit>.<page>.*`
  path. `/kcd list|get|set`, `defaults/Profile.lua`, profiles, `SchemaForPanel` and
  `Slash.lua`'s `PAGE_ORDER` are untouched.
- **Linked Focus:** the rail is drawn between the band and **either** strip path: the
  `RenderTabbedSchema` path, or `RenderLinkedUnit`'s hand-drawn inert strip plus the link note. So a
  linked Focus keeps the rail, and each entry shows its full, inert strip and the note.
- **Per-entry tab memory** and the band switch work as in §2.
- **Defaults:** restores the **active entry's rows for the unit in the band**, and the other unit is
  untouched (the owner's ruling; R8). The Grid page's own handler walks
  `Helpers.SchemaForPanel(entry, ViewedUnit())` inside one bulk bracket, `reset <entry>`, so the
  console still logs one `[Set] reset <entry>: N rows` line. The library's `O.RestoreDefaults` is not
  changed: it still resets every unit when called directly, and `tests/test_settings_log.lua` keeps
  pinning that. The Defaults tooltip says it acts on the selected unit.
- **Deep links:** `Helpers.OpenPageTab("icons"|"castbar"|"label", tab)` opens Grid at that entry and
  tab. `Helpers.SelectSection` and the `SelectTab` route are as in MultiMeters.
  `OpenPageTab("general", L["Units"])`, the linked-Focus note's link, is unchanged.
- **Slash:** `/kcd reset icons|castbar|label` still answers that it is gone. The answer now names
  Grid -> <entry>'s Defaults.

### B6. KickCD changes, by file

- `settings/Panel_Render.lua`: the Grid registry (`Helpers.RegisterGridSection`,
  `Helpers.GridSection`), `Helpers.RenderGridPage`, `Helpers.__bindGridPage`, the chrome hook on
  `Helpers.RenderUnitPanel`, `Helpers.RestoreGridSection`, `Helpers.SelectSection` and the
  `SelectTab` route. This file is host code on **both** arms, so the stub needs only `NavRail`.
- `settings/Grid.lua` (new): the page builder, registered between General and Spells.
- `settings/Icons.lua`, `Castbar.lua`, `Label.lua`: each registers its section. After NR-KC-04 their
  builders are gone; the row declarations stay.
- `settings/Panel_Widgets.lua`: `OpenPageTab` routes an entry key to Grid.
- `settings/Slash.lua`: the retired-reset answer.
- `locales/enUS.lua`: `L["Grid"]`, three rail tooltips and the Defaults tooltip.
- `KickCD.toc`: `settings\Grid.lua` after `settings\Label.lua`, with its notes.
- Tests: `tests/test_grid.lua` (new), `test_options_panel.lua`.
- Docs: `docs/settings-panel.md`, `docs/module-map.md`, `docs/ARCHITECTURE.md` (the deviation row),
  `README.md`, `docs/schema.md`, `docs/smoke-tests.md` (a new #36), `docs/test-cases.md`.

### B7. Out of scope

The General, Spells and Profiles pages. The linked-Focus behavior itself (KC-20's case stays green
unchanged). Any change to what a setting does. Moving Defaults narrowing into the library.

### B8. Smoke checks

KC-S1 … KC-S11 in `06_SMOKE_TESTS.md`, copied to KickCD's `docs/smoke-tests.md` #36 by NR-KC-04.

---

## 9. Resolutions of the points the owner's text leaves open

| # | Where | Resolution |
|---|---|---|
| R1 | MM Defaults on the General entry | General restores **nothing** and prints `L["General has no settings to restore. The window's name is kept."]`. Its only schema row is `window.name` (`settings/Schema.lua:176-182`, default "Multi Meters"), so a row walk would rename the window, and the library has no per-row `noReset`. options-ui-§13 bounds a railed Defaults by "the set the folded sub-page's own button restored", and the Windows page had no button (`settings/Windows.lua:483-486`), so that set is empty. A button that silently does nothing is what `Windows.lua`'s own `manager()` comment calls the worst version, hence the line. |
| R2 | MM General's shape | One tab named General, as options-ui-§14's escape requires ("one `General` tab"). It has two `H.Section` headings: Window, and Copy settings from. The source dropdown's label becomes `L["Source window"]` so it does not repeat the heading above it; its tooltip is kept. The `Copy from` tab key has no enUS row and simply stops being used. |
| R3 | MM deep links with no caller | The seam is built and tested (`NS.OpenOptionsPage`, `Helpers.SelectSection`, the `SelectTab` route, the per-page category capture AuraMaster uses). The header gear (`modules/HeaderControls.lua:358-366`) keeps opening the main panel. Sending it to Windows would change what a click does, and the owner did not ask for that. It is a follow-up (NR-REC-01). |
| R4 | MM Columns' reorder controller on a shared ctx | `NS.CancelReorder(ctx)` is the first statement of `Helpers.RenderWindowPage`, so it runs before every clear, whatever triggered the render. Columns' own strip `onSelect` keeps calling `RefreshPanel(ctx, true)` with no clear of its own. Review Focus 1 pins the rail-switch path. |
| R5 | MM Defaults tooltip | One tooltip that fits every entry: `L["Restore the active window's settings in the section on screen to their shipped values. On Columns that includes the shipped column list. General has nothing to restore: the window's name is kept."]`. The panel captures it once. The Columns sub-page's own tooltip key retires with the sub-page (NR-MM-04). |
| R6 | MM bespoke entries | A section spec takes an optional `render(ctx)`, which draws the strip and body under the band and rail, and an optional `defaults(ctx)`. General and Columns supply both; the other five use `RenderTabbedSchema(ctx, key)` and `RestoreDefaults(key, ctx)`. |
| R7 | MM page files | They stay, each shrunk to one `NS.RegisterWindowSection` call and its comment, so `MultiMeters.toc`, `tests/test_loadorder.lua` (:259-270, :320-326) and the layout keep their shape. The registry sits above the fork in `settings/OptionsSetup.lua`, so it exists on both arms, and a library-absent load still knows the sections. |
| R8 | KC Defaults scope | Built as the owner ruled: the selected unit only. It is narrower than options-ui-§13's "the set the folded sub-page's own button restored" (that button reset both units: `libs/LibKa0s/Options.lua:986-1007`, `settings/Panel.lua:77-81`). NR-KC-03 adds the ratified-deviation row to `docs/ARCHITECTURE.md`, with the re-check trigger "the standard states a railed page's Defaults for a page whose band picks one of several instances". The library's `RestoreDefaults` and its every-unit contract are unchanged. |
| R9 | KC linked Focus under a rail | `Helpers.RenderUnitPanel(ctx, panelKey, afterGroup, chrome)` gains an optional fourth argument, which it calls right after parking the band widget and before either strip path. The Grid page passes the rail there. Direct callers (tests, fixtures) pass nothing and draw exactly what they draw today. |
| R10 | KC first entry | Icons. KickCD's page has no page-wide acts besides the picker, so there is no General entry. options-ui-§14's escape is optional and does not apply. |
| R11 | KC deep links | `Helpers.OpenPageTab` checks `Helpers.GridSection(pageKey)` first: it selects the entry and its tab, then opens `grid`'s category. The `SelectTab` route and `SelectSection` mirror MultiMeters'. `NS.Settings.categoryFor.grid` is captured by the existing wrapper. |
| R12 | Where KC's registry lives | `settings/Panel_Render.lua`, which is host code decorating `NS.Settings.Helpers` on **both** arms (it loads after `settings/OptionsSetup.lua`, whose stub returns early). So the stub needs `NavRail` alone, and `tests/test_surface_parity.lua` (library surface vs stub) needs no ignore entry. |
| R13 | KC `/kcd reset <page>` | It still answers with where the capability went: `general` -> "the General page's Defaults button", and `icons`/`castbar`/`label` -> "Grid -> <entry>'s Defaults button (for the unit in the band)". `tests/test_slash.lua:236-243` keeps passing, since each answer still names "Defaults". |
| R14 | Re-vendor mechanics | `git archive v1.61.0 LibKa0s` into a temp dir, then copy into `libs/LibKa0s/` (SR-AM-01's method, which gives byte-identical CRLF). `tests/_kit` is diffed and not copied. Every file edited in an addon is CRLF (`* text=auto eol=crlf`). A plain `sed` insert drops the `\r` and turns the kit's eol gate red in seven addons (the dry run did exactly that), so every edit is normalized with the plan's `crlf` shorthand. |
| R15 | MM wording | "on the Columns page" -> "under Windows > Columns", "on the Frame page" -> "under Windows > Frame", and similarly for the others. The statistic-colors note reads "(Windows > Bars)", "Windows > Bars > Text style" and "(Windows > Columns)". `>` is the separator the note already uses. Keys are the English strings, so the key moves with its value, and any test pinning the old string moves in the same commit. |
| R16 | Commit order inside each addon | The page is built beside the old pages first (NR-MM-02, NR-KC-02), then the links and Defaults (03), then the old pages retire (04). Every commit is green. In the window between 02 and 04 the tree briefly has both shapes, but nothing is pushed. |
| R17 | KC unit switch and per-entry tabs | The band's `onSelect` keeps calling `Helpers.RefreshAllPanels()`. The Grid page's renderer stashes and restores the entry's tab around it, so a unit switch keeps the entry and the tab, as options-ui-§14 requires. |
| R18 | CM's stub and the owner's "each stub gains the `NavRail` no-op" (D1) | ConsumableMaster's stub gains **no** `NavRail`, a departure from the letter of D1. Its `tests/test_surface_parity.lua:264` checks the stub against a named `OPTIONS_SEAM` list, the members host code actually calls (the grep recipe above it), not against the whole live surface, and it has no `SelectTab` either. The list's own comment (:257-263) refuses a stub "for a member no page reads", and no ConsumableMaster page draws a rail, so a `NavRail` no-op would be dead code against the host's documented rule. D1's purpose (parity stays green) holds without it, and the library change is caught instead by `tests/test_libka0s.lua`'s Options inventory, which NR-CM-01 updates. If the owner wants the letter of D1, the no-op is harmless (`OPTIONS_SEAM` ignores it) and is a one-line addition to NR-CM-01. |
