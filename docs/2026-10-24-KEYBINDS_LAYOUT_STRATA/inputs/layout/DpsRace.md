# DpsRace — settings layout analysis

Read from `../DpsRace` on `master` (clean), 2026-10-24: all of `settings/` (`Schema.lua`, `OptionsSetup.lua`,
`General.lua`, `Race.lua`, `Live.lua`, `History.lua`, `Profiles.lua`, `Slash.lua`), `defaults/Profile.lua`,
`core/LauncherSetup.lua` + `Bindings.xml` (the three bindings), `core/DpsRace.lua` (what *General visibility*
gates), the `modules/Hud*.lua` / `modules/Results*.lua` readers of each row, `docs/settings-panel.md`, and the
vendored composer `libs/LibKa0s/OptionsCompose.lua:458` (`O.MasterControls`, LibKa0s v1.76.0). Standard:
`options-ui.md` §5, §7, §13, §14, §15.

## Current map

Pages: **6** (landing, General, Race, Live breakdown, History, Profiles), of which **4** hold schema rows.
Primary tabs: **6** (General 2, Race 2, Live breakdown 1, History 1). Secondary tabs: 0. Nav rail: none.
Schema rows: **22** (7 composed Master rows, alpha omitted, incl. 3 session/own-storage rows; 15 addon rows:
2 `hud.*`, 8 `race.*`, 4 `live.*`, 1 `global.history.keep`). Bespoke
non-row controls: **5** (Reset position, Reset all settings, the History stored-count line, the *Danger zone*
heading, *Delete all runs…*). Page order = TOC registration order (`DpsRace.toc:133-141`).

Two-column grid; `|` separates the two cells of one line, `—` is an empty cell. `[sub: X]` is a `subgroup`
heading (options-ui-§7, not suppressed on a tabbed page).

```
Ka0s DPS Race (landing)              OptionsSetup.lua:46 buildMain -> library BuildLandingPage(NS.LANDING, General.lua:12)
  logo 300x300 · TOC notes · "Slash Commands" heading · one label per NS.COMMANDS row    (no settings)

General                              General.lua:142 build, registered General.lua:158 (renderer General.lua:153)
  [header Defaults]                  General.lua:146-149 "Restore every General setting on this profile…"
  Tab 1  Master controls             composed General.lua:48 H.MasterControls{omit={alpha}}; reactions/own storage General.lua:70-107
    line 1  Enable Ka0s DPS Race (CheckBox, enabled)        |  General visibility (Dropdown, visibility)
    line 2  Master scale (Slider 0.5-2, scale)              |  —            (Master alpha omitted)
    line 3  Lock frame (CheckBox, locked)                   |  Debug console (CheckBox, state.debugConsole, session)
    line 4  Minimap button (CheckBox, global.minimap.shown) |  Test mode (CheckBox, state.testMode, session)
    tail    [Reset position] | [Reset all settings]         masterTail, General.lua:153
  Tab 2  Race HUD                    General.lua:115-139
    line 1  Show the race HUD (Dropdown, hud.showMode)      |  Race clock (Dropdown, hud.clock)

Race                                 Race.lua:59 NS.RegisterTabbedPage -> OptionsSetup.lua:65
  [header Defaults]                  "Restore every Race setting on this profile to its addon default."
  Tab 1  Race                        Race.lua:24-44
    [sub: Length]
      line 1  Default race length (Dropdown 0:30…5:00, race.defaultLength) | —
    [sub: Sounds]
      line 2  Countdown cue sound (CheckBox, race.countdownCue) | Buzzer raid warning and sound (CheckBox, race.buzzer)
    [sub: Final countdown]
      line 3  Center-screen countdown (CheckBox, race.centerCountdown) | Countdown from (s) (Slider 3-10, race.finalCountdown)
  Tab 2  Scoring rules               Race.lua:46-56
      line 1  Late-cast grace (s) (Slider 0-5/0.1, race.grace) | Damage-restart gap (s) (Slider 3-15, race.restartGap)
      line 2  Sticky-combat hint after (s) (Slider 5-60, race.hintDelay) | —

Live breakdown                       Live.lua:33 NS.RegisterTabbedPage
  [header Defaults]                  "Restore every Live breakdown setting on this profile…"
  Tab 1  Live breakdown              Live.lua:14-31
    [sub: Rows]
      line 1  Rows shown (Slider 3-15, live.rows)          |  Live reads per second (Slider 2-10, live.hz)
    [sub: Display]
      line 2  Show spell icons (CheckBox, live.icons)       |  Show live DPS (CheckBox, live.showDps)

History                              History.lua:88 NS.RegisterTabbedPage (afterGroup History.lua:77)
  [header Defaults]                  "Restore Runs to keep to its addon default. Stored runs are not touched."
  Tab 1  History
    [sub: Storage]
      line 1  Runs to keep (Slider 0-10000, global.history.keep) | —
      text    "Stored now: N runs (about K KB of saved variables)."   History.lua:79
    heading Danger zone                                              History.lua:80
      [Delete all runs…] | —                                         History.lua:81

Profiles                             Profiles.lua:9 build, registered Profiles.lua:42 (AceDBOptions, untabbed, options-ui-§13 exemption)

(not in the panel) Settings > Keybindings > AddOns > "Ka0s DPS Race" header    Bindings.xml:8-12, labels LauncherSetup.lua:40-43
  Toggle race HUD · Toggle results window · Arm / cancel race
```

Counts: 6 pages, 6 primary tabs, 22 schema rows, 6 subgroup headings (Race 3, Live breakdown 2, History 1),
1 builder heading, 3 key bindings.

## Problems

| id | where | problem |
|---|---|---|
| DPS-P01 | `Live.lua:33` | **A whole page for four rows.** *Live breakdown* is a one-tab page holding two lines. Changing anything about the HUD's look means a page hop for two lines of content. |
| DPS-P02 | `General.lua:116,129` vs `Live.lua:15-27` | **The HUD's settings are split across two pages.** *When* it shows and *what its clock shows* sit on General > Race HUD, while *what its rows show* (count, icons, live DPS, read rate) sit on another page. All six rows are read by the same `modules/Hud.lua:278-284 commonView` and all six react with `NS.Hud.Refresh()`. A player tuning the HUD visits two pages. |
| DPS-P03 | `Live.lua:11`, `Live.lua:35` | **The page name hides the subject.** "Live breakdown" doesn't say "HUD", and two of its four rows aren't the breakdown: *Show live DPS* is the KPI figure above the rows, and *Live reads per second* is the meter poll rate. |
| DPS-P04 | `Race.lua:53` | **`race.hintDelay` is not a scoring rule.** The defaults file is explicit that only `grace` and `restartGap` freeze into a run's record (`defaults/Profile.lua:13-18`). The hint delay only decides when the HUD's waiting body suggests ways to drop combat (`modules/Hud.lua:228`). It sits under a tab whose two other rows carry "Applies to new runs", so it reads as if it re-grades runs too. |
| DPS-P05 | `Race.lua:30` | **The countdown cue is cut off from the countdown it plays with.** Its tooltip says it sounds "at 10, 5, 3, 2 and 1 seconds left, **and** with each number of the center countdown" (so it is partly independent of the center numbers and starts at 10 s whatever *Countdown from* says), and all three rows re-arm through the same `Countdown.Refresh` (`Race.lua:22`), but the cue sits under *Sounds* and the numbers under *Final countdown*. |
| DPS-P06 | `Race.lua:30-36` | **"Sounds" groups by medium, not by moment.** It holds the 10…1 cue (the run-up) and the buzzer (the end). The buzzer row is mostly a raid warning (a visual), so it doesn't really fit "Sounds" either. The tab's natural order is the race's timeline: length → countdown → buzzer. |
| DPS-P07 | `Race.lua:46-56` | **Tab switch for one line.** Once P04 is fixed, *Scoring rules* holds two sliders (one line). The Race page's 2 tabs then hold 4 lines in total. |
| DPS-P08 | `Race.lua:41` | **"Countdown from (s)" is ambiguous.** The cue also "counts down" (it fires from 10 whatever this says), so the label could be read as the cue's start. It sets only where the center numbers start. |
| DPS-P09 | `Race.lua:54` | **Inconsistent tooltip.** *Sticky-combat hint after (s)* is the only slider on the page whose tooltip doesn't state its range (siblings say "0 to 5 seconds", "3 to 15 seconds", "3 to 10"). |
| DPS-P10 | `Live.lua:15-27` | **Subgroups don't match their rows.** *Rows* holds the poll rate (not a row property). *Display* holds *Show live DPS* (a figure, not row display), while *Show spell icons*, which is a row property, sits under Display and not under Rows. |
| DPS-P11 | `General.lua:116` + composer `OptionsCompose.lua:477-478` | **Two "when does the HUD show" controls on two tabs, and neither mentions the other.** *General visibility* (Master controls) gates only the HUD (`core/DpsRace.lua:78-87`, read by `modules/Hud.lua:692`). *Show the race HUD* (Race HUD tab) is the HUD's own rule. A player who picks *Always* and sees no HUD has no pointer to *General visibility = Never*. Master controls is fixed (options-ui-§15), so the fix has to be wording. |
| DPS-P12 | `General.lua:48-66`, composer `OptionsCompose.lua:482,490,555` | **The generic Master tooltips misdescribe this addon.** *Lock frame*: "Stop the frame being dragged". It locks only the HUD (drag and grip); the Results window ignores it (`modules/Results.lua:159` drags unconditionally, and `Results.lua:11-12` says so). *Master scale*: "Scales the whole addon's display". It scales the HUD and the Results window but not the center-screen countdown. *Reset position*: "Move the frame back to where it started". It resets **two** windows, and their **sizes** too (`General.lua:61-64`, `docs/settings-panel.md:53`). *General visibility*: "this addon's display". It gates the HUD only. |
| DPS-P13 | `General.lua:51` (fixed by options-ui-§15) | Line 2 of Master controls is *Master scale* alone with an empty right cell, because alpha is omitted. The standard fixes this shape: an omitted canonical row leaves its hole, and an `extra` must not fill it. Recorded, not changed. See Upstream suggestions. |
| DPS-P14 | `Live.lua:14,17` | *Rows shown* doesn't say which rows. The HUD also has chips, KPI boxes and the target card. "Spell rows" is what the tooltip means. |
| DPS-P15 | `Race.lua:26` | **Lonely one-row subgroup.** *Length* heads a single dropdown, and its heading repeats the row's own noun ("Length" over "Default race length"). Tolerable, because the tab mixes control types and §7 requires headings. |
| DPS-P16 | `History.lua:70-86` | *Runs to keep* is a 0–10000 slider with step 1. At default UI scale one pixel is about 30 runs, so an exact value is only reachable via `/dr set` or the slider's edit box. Widget choice is out of scope here (the range and type stay). Recorded for the owner. |
| DPS-P17 | `History.lua:79` | Nitpick: the stored-count line comes **after** the limit. Reading order "you have N runs → keep at most M" would put it first, but it is an `afterGroup` text row and the flow engine has no before-group seam. Not worth a library change. No change proposed. |
| DPS-P18 | (planned 015) | **No slot yet for the Keybindings tab.** DpsRace has **three** bindings (HUD, Results, Arm/cancel), the most of any windowed addon except QuickComms. They sit under the generic *AddOns* list with header "Ka0s DPS Race" (`Bindings.xml:8`, `LauncherSetup.lua:40`). |
| DPS-P19 | `LauncherSetup.lua:41-43` | **Binding names drift from the collection's pattern.** "Toggle race HUD" and "Toggle results window" vs BankLedger "Toggle the ledger window", DropWatcher "Toggle Drop Watcher window", LootHistory "Toggle Loot History window". Inside the addon the HUD is consistently "the race HUD" in sentence case (row *Show the race HUD*, `/dr hud` and `/dr lock` help, `Slash.lua:32,39`); the tab "Race HUD" is the same sentence case with the first word capitalised, so that is not a drift. The real drift is "results window": the addon's own prose names that window *Results* (`/dr results` help "Open the Results window", window title "DPS Race — Results", `Results.lua:145`). |
| DPS-P21 | `History.lua:80` vs options-ui-§7 | **Builder-drawn heading.** §7 says a section/subsection heading "is declared by a row, never drawn by a builder", but *Danger zone* is `H.Section` from the after-group hook. It cannot be a `subgroup` because *Delete all runs…* is not a schema row. Grey zone in the standard, not a layout defect; recorded under Upstream suggestions. No change proposed. |
| DPS-P22 | `General.lua:146-149` (planned 015) | **The General Defaults button will sit over a tab that is not profile state.** Bindings live in the client's binding set (account or character), not in AceDB, so neither the page Defaults nor *Reset all settings* nor `/dr list` reaches them. Today's tooltip "Restore every General setting on this profile" would read as covering the new Keybindings tab. |
| DPS-P20 | `General.lua:146-149`, `Live.lua:36` | Knock-on of any move between pages: each page's header **Defaults** restores *that page's* rows. Where the HUD rows live decides which Defaults button resets them, and `/dr list` groups by `page › group` (`Slash.lua:161`). Not a defect today, but it constrains P01/P02. |

## Proposed changes

| id | change | reason | confidence | fixes |
|---|---|---|---|---|
| DPS-L01 | **Fold the Live breakdown page into General > Race HUD.** Move `live.rows`, `live.icons`, `live.showDps`, `live.hz` from page `live` > group *Live breakdown* to page `general` > group *Race HUD*, after `hud.clock`. Only the rows' `page` / `group` / `subgroup` fields change; the `live.*` paths, defaults, ranges and `onChange = redraw` stay. Delete the *Live breakdown* page registration (`Live.lua:33-37`). The rows can stay declared in `Live.lua` (it loads after `General.lua`, `DpsRace.toc:133-141`, so they sort after the `hud.*` rows) or move into `General.lua`. Drop `live` from `VALID_PAGES` (`Schema.lua:195`). | Every HUD setting in one tab: one page fewer, no hop to tune the HUD. All six rows are read by one `commonView` (`Hud.lua:278-284`). Three lines fit the canvas without scrolling. Side effects, none of them a setting change: General's page Defaults now also restores the four live rows (right, they are HUD rows like `hud.*`; options-ui-§13 keeps it page-wide), and `/dr list` groups them as `general › Race HUD` instead of `live › Live breakdown` (`Slash.lua:161`). `/dr get/set live.*` is unchanged. | 80% | P01, P02, P03, P20 |
| DPS-L02 | Give the merged *Race HUD* tab two subgroups: **"Display"** (`hud.showMode`, `hud.clock`) and **"Live breakdown"** (the four `live.*` rows). | options-ui-§7: a tab mixing dropdowns, sliders and checkboxes MUST carry subsection headings, and neither may repeat the tab name ("Race HUD"). "Display" covers both *whether* the HUD shows and *what its clock shows*; the first draft's "Window" fitted only the show mode. "Live breakdown" survives as the subheading players already know from the old page. | 80% | P02, P03 |
| DPS-L03 | Re-pair the live rows by declaration order inside the one *Live breakdown* subgroup: line 1 *Spell rows shown* (`live.rows`) \| *Show spell icons* (`live.icons`); line 2 *Show live DPS* (`live.showDps`) \| *Live reads per second* (`live.hz`). `startsLine` moves from `live.icons` to `live.showDps`. | Each line becomes one subject: what the spell rows show, then the live figure and how often it refreshes. Ends the P10 mismatch without a third heading. | 70% | P10 |
| DPS-L04 | Relabel `live.rows` **"Rows shown" → "Spell rows shown"**. Tooltip unchanged (it already says "How many spells…"). | Says which rows (the HUD has chips, KPIs and a target card too). | 60% | P14 |
| DPS-L05 | Append to the `hud.showMode` tooltip: **"General visibility on Master controls still applies: while it hides the addon, the HUD stays hidden whatever this says."** | Connects the two show rules that §15 forces onto separate tabs (`core/DpsRace.lua:78-87` is checked before the HUD's own rule, `Hud.lua:692`). Wording covers *Never* and the two combat modes, not only *Never*. | 75% | P11 |
| DPS-L06 | **Re-section the Race tab along the race's timeline.** Subgroups become **Length** → **Countdown** → **At the buzzer** → **Scoring rules** (was Length → Sounds → Final countdown, plus a separate tab). Rename subgroup "Final countdown" → "Countdown". Move `race.countdownCue` from *Sounds* into *Countdown*, on its own line **first** (`Countdown cue sound` \| —), then `Center-screen countdown` \| `Center countdown from (s)`. | The cue and the numbers re-arm together and play together. The cue goes first because it starts first (always at 10 s left) and does not depend on the center numbers being on; the dependent pair (checkbox + its slider) stays on one line. Ordered by when things happen in a race. | 70% | P05, P06 |
| DPS-L07 | Move `race.buzzer` into the new **At the buzzer** subgroup; the *Sounds* subgroup goes away. | The buzzer is the race's end event (raid warning and sound), not just "a sound". | 80% | P06 |
| DPS-L08 | **Move `race.hintDelay` from the Scoring rules tab to Race > At the buzzer**, paired right of `race.buzzer`. Same page, so the Race Defaults scope is unchanged. | It is not frozen into runs (`defaults/Profile.lua:13-18`) and never re-grades one; it only times the HUD's post-buzzer hint (`Hud.lua:228-229`). It pairs with the buzzer. That leaves *Scoring rules* exactly the two record-frozen rows. | 75% | P04 |
| DPS-L09 | **Merge the Scoring rules tab into the Race tab** as its last subgroup **"Scoring rules"** (`race.grace` \| `race.restartGap`), i.e. change their `group` to *Race* and give them `subgroup = "Scoring rules"`. The Race page becomes a one-tab page (options-ui-§13 permits it). | After L08 the tab is one line. A tab click for one line is the switching the owner wants gone. The rules keep their own heading, and their tooltips already say "Applies to new runs". Lower confidence: a separate tab did visually fence off "these settings are recorded into runs". | 60% | P07 |
| DPS-L10 | Relabel `race.finalCountdown` **"Countdown from (s)" → "Center countdown from (s)"**. | Ties it to its parent row and keeps it from being read as the cue's start (the cue fires from 10 s whatever this says). | 70% | P08 |
| DPS-L11 | Add the range to the `race.hintDelay` tooltip: "… suggests ways to drop it. **5 to 60 seconds.**" | Every other slider on the page states its range. | 85% | P09 |
| DPS-L13 | **Add the Keybindings tab (015) as the LAST tab of General**: Master controls \| Race HUD \| **Keybindings**. Rows in order: *Toggle race HUD*, *Toggle Results window*, *Arm / cancel race*. Settings > Keybindings shows them under the category **"Ka0s DPS Race"** (owner answer 1; already the `BINDING_HEADER_DPSRACE` text, `LauncherSetup.lua:40`). The tab's controls are **not** schema rows: page Defaults, *Reset all settings* and `/dr list` must not touch them. | Same slot in all 7 windowed addons (matches BankLedger's BAN-L14). Bindings are set once, so they go at the end of the strip, after the tab players actually tune. **Constrained by the standard as written:** launcher-§6 today mandates `category="ADDONS"`, and options-ui-§13 derives every tab from a schema `group` ("every row carries a group"). Both need the 015 upstream change (a binding-tab surface in LibKa0s and a launcher-§6 amendment) before this lands; nothing here should be done host-side around them. | 75% | P18 |
| DPS-L14 | Binding labels: **"Toggle results window" → "Toggle Results window"**. "Toggle race HUD" and "Arm / cancel race" unchanged. Labels only: the `CLICK DpsRace…:LeftButton` binding names are permanent (`Bindings.xml:5`, launcher-§6) and do not change. | "Results" is the window's own name everywhere else in the addon (`Slash.lua:34`, title `Results.lua:145`). "Toggle race HUD" already follows launcher-§6's `Toggle <window>` and the addon's sentence-case "race HUD"; the first draft's "Toggle Race HUD window" broke that and doubled the noun (a HUD *is* the window). | 55% | P19 |
| DPS-L16 | Append to the General page Defaults tooltip (`General.lua:147`): "**Key bindings are not changed.**" Only once L13 lands. | The tab strip will show Keybindings beside rows the button does reset (P22). One sentence stops a player expecting their keys to be cleared or restored. | 60% | P22 |
| DPS-L15 | Doc ripple (no layout effect): rewrite `docs/settings-panel.md` *Pages*, *The tree* and launcher sections; the file-head comments of `Race.lua:1-4`, `Live.lua:1-3`, `General.lua:110-112`, `OptionsSetup.lua:59`, `defaults/Profile.lua:13-15,29`, `DpsRace.toc:135`; `docs/schema.md:37-40` ("Live breakdown page" → "General > Race HUD"), `docs/profiles.md:9`, `docs/module-map.md:64,67`, `docs/ARCHITECTURE.md:61`, `docs/testing.md:75`, `docs/test-cases.md:361,367`, `docs/smoke-tests.md:46,48`. Locale: drop the now-unused `Sounds`, `Final countdown`, `Rows`, the Live page Defaults tooltip and (if no longer referenced) `Live breakdown` as a page title; keep `Display` (already a key, `locales/enUS.lua:320`, reused by L02); add `Countdown`, `At the buzzer`, `Spell rows shown`, `Center countdown from (s)`, `Toggle Results window` (`locales/enUS.lua:286-333`). Re-pin the row/page order in `tests/test_settings.lua`. | The docs, smoke tests and the order pin describe the old tree. | 90% | — |

## Considered and rejected

| change | confidence | why rejected |
|---|---|---|
| DPS-L12 (first draft): host-side tooltip suffixes on the composed *Lock frame*, *Master scale*, *General visibility* rows, set in the `General.lua:98-106` loop | 35% | options-ui-§15: "the rows are composed, not hand-written … so no two addons can drift", and the set "MUST NOT" be edited. A host rewriting composed copy is exactly that drift, done once per addon. P12 is real, but the fix is the composer `notes` field under Upstream suggestions; a host stopgap would be thrown away when it lands, and still cannot reach *Reset position*. |
| Fold the (one-tab, after L09) Race page into General as a fourth tab | 30% | A tab click replaces a page click, so no switching is saved, and General's page Defaults would grow to nearly the global reset's scope, blurring the options-ui-§12 / §13 distinction between the two buttons. |
| Move *History* into the Race page as a tab | 35% | Account-wide storage with a destructive act, a different subject from race behaviour; one page is cheap. |
| Move `race.hintDelay` to General > Race HUD (it is a HUD behaviour) | 35% | It is timed off the buzzer, and the Race page is where the race's timeline lives (L06-L08). Either is defensible; the Race page keeps the HUD tab to display-only settings. |
| Split the Race HUD tab into "Opening" (`hud.showMode`) and "While the race runs" (clock + live rows) | 35% | One more line and one heading for a purer split; loses the "Live breakdown" name players know. L02 is good enough. |
| Put `hud.showMode` into Master controls through `extra` | 20% | §15 requires an extra to be addon-wide; it is the HUD's own rule. |
| Reorder the stored-count line above *Runs to keep* | 30% | P17: needs a before-group seam in the library. |

Net effect: **6 → 5 pages**, **6 → 4 primary tabs before 015** (General 2, Race 1, History 1), **5 with
Keybindings**. Schema rows are unchanged at 22. Subgroup headings: 6 → 7. Tuning the HUD drops from 2 pages to 1 tab. Setting
up a race (length, countdown, buzzer, scoring) drops from 2 tabs to 1.

## Proposed map

```
Ka0s DPS Race (landing)              unchanged

General                              General.lua build
  [header Defaults]                  restores Master + all six HUD rows (L01); tooltip + "Key bindings are not changed." (L16)
  Tab 1  Master controls             unchanged (options-ui-§15)
    line 1  Enable Ka0s DPS Race (CheckBox, enabled)        |  General visibility (Dropdown, visibility)
    line 2  Master scale (Slider, scale)                    |  —
    line 3  Lock frame (CheckBox, locked)                   |  Debug console (CheckBox, state.debugConsole, session)
    line 4  Minimap button (CheckBox, global.minimap.shown) |  Test mode (CheckBox, state.testMode, session)
    tail    [Reset position] | [Reset all settings]
  Tab 2  Race HUD                                                                       L01, L02
    [sub: Display]                                                                      L02
      line 1  Show the race HUD (Dropdown, hud.showMode) [tooltip L05] | Race clock (Dropdown, hud.clock)
    [sub: Live breakdown]
      line 2  Spell rows shown (Slider 3-15, live.rows) [L04]  |  Show spell icons (CheckBox, live.icons)      L03
      line 3  Show live DPS (CheckBox, live.showDps)           |  Live reads per second (Slider 2-10, live.hz)  L03
  Tab 3  Keybindings                 (015, L13; synced with Settings > Keybindings > Ka0s DPS Race)
      Toggle race HUD          [key 1] [key 2]                (label unchanged)
      Toggle Results window    [key 1] [key 2]                L14
      Arm / cancel race        [key 1] [key 2]
      (not schema rows: outside page Defaults, Reset all settings and /dr list)

Race                                 Race.lua RegisterTabbedPage (one-tab page)
  [header Defaults]                  unchanged wording; now also covers race.hintDelay (it was already on this page)
  Tab 1  Race
    [sub: Length]
      line 1  Default race length (Dropdown, race.defaultLength) | —
    [sub: Countdown]                                                                    L06
      line 2  Countdown cue sound (CheckBox, race.countdownCue)  |  —                    L06
      line 3  Center-screen countdown (CheckBox, race.centerCountdown) | Center countdown from (s) (Slider 3-10, race.finalCountdown)  L10
    [sub: At the buzzer]                                                                L07, L08
      line 4  Buzzer raid warning and sound (CheckBox, race.buzzer) | Sticky-combat hint after (s) (Slider 5-60, race.hintDelay) [tooltip L11]
    [sub: Scoring rules]                                                                L09
      line 5  Late-cast grace (s) (Slider 0-5/0.1, race.grace) | Damage-restart gap (s) (Slider 3-15, race.restartGap)

History                              unchanged
  [header Defaults]
  Tab 1  History
    [sub: Storage]
      line 1  Runs to keep (Slider 0-10000, global.history.keep) | —
      text    Stored now: N runs (about K KB of saved variables).
    heading Danger zone
      [Delete all runs…] | —

Profiles                             unchanged
```

Counts after: 5 pages (landing, General, Race, History, Profiles), 5 primary tabs (General 3, Race 1, History
1), 22 schema rows (unchanged), 7 subgroup headings (Race HUD 2, Race 4, History 1), 3 key bindings (now also
on General > Keybindings).

## Cross-addon notes

- **Keybindings tab slot:** last tab of General in every windowed addon. Agrees with BankLedger BAN-L14.
- **Binding label pattern:** launcher-§6 says `Toggle <window>`. Recommend "Toggle <window name>", no article,
  with "window" appended only when the name is not already a display noun: "Toggle Results window",
  "Toggle Drop Watcher window", but "Toggle race HUD" (not "Toggle Race HUD window"). Keep the casing the
  addon's own prose uses for that window. Extra, non-window bindings use a verb phrase ("Arm / cancel race").
- **Keybindings tab vs Defaults:** in every windowed addon the General Defaults tooltip should say that key
  bindings are not changed (DPS-L16), and the tab must stay outside *Reset all settings* and `/<slash> list`.
- **Launcher menu wording drift:** the launcher's *Show window* entry toggles the HUD (`docs/settings-panel.md:128`),
  while the binding says "Toggle race HUD". Not a settings row, but the same act should have one name everywhere.
  Worth checking for every addon whose window has a launcher entry.
- **Danger-zone heading:** DpsRace's History tab uses a `Danger zone` builder heading before a destructive
  act. No other windowed addon uses that phrase (grep of BankLedger/DropWatcher/LootHistory/MultiMeters/
  QuickComms/WhatGroup `settings/` and `locales/`), even where they have a purge/delete act. Pick one convention.
- **Addon-specific display tabs on General:** DpsRace puts its HUD tab on General after Master controls.
  Addons should agree on whether "the primary display's own settings" live on General or on a page of their
  own. This proposal keeps them on General because the HUD *is* the addon's positionable display, and Master
  scale/lock already act on it there.
- **Per-page Defaults scope** follows the page. When any addon moves rows between pages (as L01 does), its
  page Defaults tooltips should be re-read.

## Upstream suggestions

- **options-ui-§15, host-specific tooltip suffix for composed rows.** The composer's generic tooltips ("Stop
  the frame being dragged", "Move the frame back to where it started") are wrong for any addon with more than
  one window or a lock that covers only one of them. Proposal: a `MasterControls{ notes = { locked = "…",
  scale = "…", visibility = "…", resetPosition = "…" } }` field the composer appends to its own tooltip. That
  keeps the label and base copy canonical and lets the host say what the row actually touches. (The first draft's host-side
  stopgap, DPS-L12, was rejected as §15 drift; this field is the only fix. *Reset position* can't be reached
  without it.)
- **options-ui-§15, the omitted-row hole.** An addon without Master alpha draws *Master scale* alone on line 2.
  The asymmetry argument the standard makes for *Minimap button* applies here too: let the canonical rows
  reflow when a frame-only row is omitted (scale | lock, then console | minimap…). Or say explicitly that the
  hole is intended, so audits stop flagging it.
- **options-ui-§7, headings over non-row acts.** §7 says a heading is "declared by a row, never drawn by a
  builder", yet a destructive act after a group (DpsRace's *Danger zone* over *Delete all runs…*) has no row
  to declare it. Either bless an after-group act heading (one wording, e.g. "Danger zone", collection-wide) or
  give acts a schema-declarable form.
- **launcher-§6 / options-ui-§13 for 015.** launcher-§6 mandates `category="ADDONS"`, and §13 builds tabs only
  from schema `group`s. The Keybindings tab and per-addon categories need both amended, plus a library surface
  for a non-schema tab, before any addon adopts L13.
- **options-ui-§7, a "before-group" seam** (the mirror of after-group) would let a read-out such as History's
  stored count sit above the row it informs. Low priority.

## Review

Independent review, 2026-10-24, against `../DpsRace` `master` (settings/, core/LauncherSetup.lua, Bindings.xml,
core/DpsRace.lua, modules/Hud.lua, modules/Results.lua, locales/enUS.lua, docs/) and options-ui §7, §13, §15 and
launcher-§6.

- **Counts corrected.** Schema rows are 22, not 20: the composer emits 7 Master rows with alpha omitted
  (enabled, visibility, scale, locked, debugConsole, minimap, testMode), not 9, and there are 15 addon rows,
  not 11. Subgroup headings today are 6 (Race 3, Live 2, History 1), not 4, and 7 after, not 6.
- **P05 sharpened.** The cue also fires at 10/5/3/2/1 s on its own, so it is not purely the center countdown's
  sound. That made L06 put the cue line first.
- **P19 corrected.** "race HUD" is used consistently in sentence case across the addon, and a "Race HUD" tab
  label is not a drift. The HUD's title is "DPS Race", not "Race HUD". The real drift is "results" vs
  "Results". **L14 rewritten:** keep "Toggle race HUD" (the first draft's "Toggle Race HUD window" broke the
  addon's casing and doubled the noun), and change only "Toggle results window" → "Toggle Results window".
- **L12 moved to Considered and rejected (50% → 35%).** Rewriting composed Master-row copy from the host is the
  per-addon drift §15 forbids. The upstream composer field is the fix.
- **L02 heading "Window" → "Display".** "Window" did not fit the race clock. Confidence 85% → 80%.
- **L06 reordered** (cue first) and confidence lowered from 75% to 70%. **L08** lowered from 80% to 75%: the
  alternative home (the HUD tab) is defensible.
- **L13 now cites the standard rules it collides with** as written (launcher-§6 `category="ADDONS"`, and
  options-ui-§13 "every row carries a group"). It states that the tab's controls are not schema rows.
- **Added P21** (builder-drawn *Danger zone* heading vs §7), **P22 + L16** (General Defaults tooltip once
  Keybindings exists), and matching Cross-addon and Upstream notes.
- **L01 side effects made explicit:** `/dr list` grouping changes, `/dr get/set` paths do not, and General
  Defaults covers the live rows. L15's ripple list now has the locale, smoke-test, schema, profiles,
  module-map, ARCHITECTURE, testing and test-cases references, which grep found.
- **Setting-change check:** no proposed change alters a key, default, range, type or `onChange`. L01, L03,
  L06-L09 change only `page`, `group`, `subgroup`, `startsLine` and declaration order. L04, L10 and L14 are
  labels. L05, L11 and L16 are tooltips.
- The "Not proposed" paragraph became the **Considered and rejected** table, with two more rejections (fold
  Race into General; split the HUD tab).
