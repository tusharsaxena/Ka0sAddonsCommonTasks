# PremadeGroupsFilterExtension — settings layout analysis

Scope: item 020 (layout only: no key, default, range or behaviour changes). Read from
`../PremadeGroupsFilterExtension` at `master` (e5b741a) on 2026-10-24: `settings/{OptionsSetup,Schema,SchemaSetup,Panel,Slash,Profiles}.lua`,
`defaults/Profile.lua`, `modules/{Panel,EUISkin,Regions,RegionTags}.lua`, `core/{EUIBridge,LauncherSetup,DebugLogSetup}.lua`,
`locales/enUS.lua`, `docs/settings-panel.md`, and the vendored `libs/LibKa0s/OptionsCompose.lua` (Master controls
composer, :458-574).

PGFE is **not** one of the seven addons with a primary window. Its only surface is the filter panel attached under
Premade Groups Filter's dialog (`modules/Panel.lua`), whose visibility follows PGF's dialog, so it has no toggle verb
and no `Bindings.xml`. The planned General > Keybindings tab does not apply here, and nothing below assumes it.

The attached filter panel holds the per-character filter options (`char.filters.*`). Those are **not** schema rows
and are not part of the settings menu (`settings/Schema.lua:4-9`, `docs/settings-panel.md:5-7`). They are covered
here only where a settings-page row shares a label or tooltip with the panel.

## Current map

Page order is TOC order (`PremadeGroupsFilterExtension.toc`: `settings\Panel.lua` registers General, then
`settings\Profiles.lua` registers Profiles last). Widget types: CB checkbox, CP colour picker (no alpha), BTN button,
TXT text/status line (not a schema row), EB read-only edit box (not a schema row).

```
Ka0s Premade Groups Filter Extension (landing)   settings/OptionsSetup.lua:94 (buildMain) -> settings/Panel.lua:30-42 (BuildLandingPage)
  untabbed (options-ui-§13 exemption)
  - logo (media/logos/premadegroupsfilterextension.logo.tga), tagline (TOC Notes)
  - Section "Slash Commands": one label per NS.COMMANDS row, settings/Slash.lua:22-52, in this order:
      help, config, enable, disable, version, list, get, set, reset, resetall, profile, debug,
      diagnostics, apply, clear                                                    (15 rows)

General                                          settings/Panel.lua:348-367 (CreatePanel :349, RenderTabbedSchema :358)
  Header band: [Defaults BTN] (defaultsButton = true, :351-355) -> the same reset-all popup as below
               (options-ui-§12: the header Defaults button and Reset all settings are one act)
  Tab "Master controls"                          composed: Helpers.MasterControls, settings/Panel.lua:49-73
                                                 (frameless = true, omit visibility; no test mode)
    [Enable Ka0s Premade Groups Filter Extension  CB enabled]   [Debug console  CB state.debugConsole (session)]
    [Minimap button  CB global.minimap.shown]                                    (alone on its line)
    [Reset all settings BTN -> StaticPopup PREMADEGROUPSFILTEREXTENSION_RESET_ALL]  (alone; frameless, no Reset position;
                                                 drawn by the after-group hook MASTER_TAIL, :345-346)
  Tab "Filters"                                  settings/Panel.lua:80-95 (library default tab body)
    [Toggle PGF Extension Filters  CB filtersActive]   [Show server regions in the Group Finder  CB showRegionTags]
  Tab "Region colors"                            settings/Panel.lua:105-168 (host tab, renderRegionTab :141)
    Heading "US realms (by data center)"                                          :147
      TXT preview: OCE LA CHI MEX BZL in their current colours (GameFontHighlightLarge) :148
      [OCE  CP regionColors.oce]  [LA   CP regionColors.la]   [CHI  CP regionColors.chi]   (3 per line, :111/:157)
      [MEX  CP regionColors.mex]  [BZL  CP regionColors.bzl]
    Heading "EU realms (by language)"
      TXT preview: ENG GER FRA ITA SPA POR RUS
      [ENG  CP regionColors.eng]  [GER  CP regionColors.ger]  [FRA  CP regionColors.fra]
      [ITA  CP regionColors.ita]  [SPA  CP regionColors.spa]  [POR  CP regionColors.por]
      [RUS  CP regionColors.rus]                                                    (alone)
    (12px gap) [Reset region colors BTN -> Settings.ResetRegionColors]              :162-167
    (Both portals are always drawn, although a player only ever sees one portal's tags: NS.Regions.GetPortal(),
     modules/Regions.lua:31-33. On KR/TW/CN no tag is drawn at all.)
  Tab "EllesmereUI skin"                         settings/Panel.lua:180-338 (host tab, renderEuiTab :317)
    [Use the EllesmereUI skin  CB euiSkin]  (disabled while any condition fails)    :322
    (12px gap)
    TXT condition 1  "EllesmereUI and its Blizzard Skin module are loaded"  (+ hint when failing)
    TXT condition 2  "EllesmereUI third-party skinning is on"
    TXT condition 3  "PremadeGroupsFilterExtension is on in EllesmereUI's Third-Party Addons list"
    TXT condition 4  "Premade Groups Filter's own EllesmereUI skin is on"  (or one of three failing variants)
    (8px gap)
    TXT state line   ("The skin is applied." / "...is off." / ...)                  :333
    EB  "Get Premade Groups Filter - EllesmereUI Skin (select, then Ctrl+C):" <CurseForge URL>
        (only when the PGF skin is not installed; decided at render time)          :337, :252-277
    (The five TXT lines are AceGUI InteractiveLabels with their own hover tooltips, :284-305, :308-314.)

Profiles                                         settings/Profiles.lua:10-46 (AceDBOptions via AceConfigDialog; untabbed exemption;
                                                 defaultsButton = false)
```

Counts: **3 pages** (landing, General, Profiles), **4 tabs** (all on General), **18 schema rows** (Master controls 3,
Filters 2, Region colors 12, EllesmereUI skin 1), plus 3 buttons (header Defaults, Reset all settings, Reset region
colors), 2 preview lines, 5 status lines and 1 conditional link box. The Profiles page is AceDBOptions' own table.

## Problems

Severity: **H** high (a task needs a tab switch, or a label misleads), **M** medium, **L** low/nitpick.

- **PRE-P01 (H): the region-tag switch and its colours sit on different tabs.** `showRegionTags`, which turns the tags
  on or off, is on *Filters* (`settings/Panel.lua:90-92`). The twelve tag colours it governs are on *Region colors*
  (`:113-124`). Tuning the tags is a single task, yet it needs a tab switch. The colours tab also never says the tags
  can be turned off, so a player who turned them off sees pickers with no visible effect.
- **PRE-P02 (H): the *Filters* tab holds no filters.** Its two rows are a master switch for the addon's managed PGF
  block (`filtersActive`) and a display toggle for Group Finder rows (`showRegionTags`), and the second is not a
  filter at all. The actual filter options (key level, regions, playstyle, composition, leader, age, presets) live only
  on the attached panel, and nothing in the settings tells the player so. Someone opening General > Filters to change
  a filter finds two checkboxes and no route to the filters (`settings/Panel.lua:80-95`, `docs/settings-panel.md:5-7`).
- **PRE-P03 (M): "Toggle PGF Extension Filters" is a poor checkbox label.** "Toggle" is redundant on a checkbox,
  because every checkbox toggles. "PGF Extension" is neither the addon's name (*Premade Groups Filter Extension*) nor
  PGF's. Title Case also breaks the sentence case every other row uses ("Show server regions…", "Debug console",
  "Minimap button"). (`locales/enUS.lua:70`; the label is shared with the attached panel's first row,
  `modules/Panel.lua:276`, and quoted in `L.MSG_INACTIVE`, `locales/enUS.lua:65`.)
- **PRE-P04 (M): the `filtersActive` tooltip is written for the attached panel and reads wrong on the settings
  page.** On the settings page it says "writes the block back from **the options below**", but nothing is below it
  there. It also says "**Also on the settings page**" while the player is on the settings page.
  (`locales/enUS.lua:71`, used at `settings/Panel.lua:86` and `modules/Panel.lua:278`.)
- **PRE-P05 (M): the `euiSkin` tooltip points the wrong way.** "Needs every condition listed **above**", but at the
  owner's request the switch is drawn **first**, with the conditions under it (`settings/Panel.lua:188` vs
  `:316-331`).
- **PRE-P06 (M): the "US realms (by data center)" heading is inaccurate.** Two of its five tags are not data centres:
  MEX is "the Latin American (Spanish) realms" and BZL is "the Brazilian (Portuguese) realms", which are language
  groups, and OCE is Oceanic, which is not "US" to a player (`locales/enUS.lua:97-101,112`;
  `modules/Regions.lua:11-14`). In Blizzard's terms the bucket is the US *portal*, which covers the Americas and
  Oceania.
- **PRE-P07 (M): terminology drifts across one feature.** The same thing is called *server regions* (the
  `showRegionTags` label, the panel's "Server regions" filter), *region colors* (the tab), *realms* (the portal
  headings), *region tag* (the colour tooltip, the reset tooltip) and *region* (the picker tooltips). A player has to
  work out that "server region", "realm region" and "region tag" all mean the same thing
  (`locales/enUS.lua:73-74,84,111-116`). Note that two of these are legitimately different nouns: the panel's
  *Server regions* is a **filter** over the leader's server region, and the tag is the **display** of it. Only the
  display side should converge on "region tag"; the filter keeps "Server regions".
- **PRE-P08 (L): the PGF skin link box sits far from the line that mentions it.** Condition 4's tooltip says "the
  link appears below when it is missing" (`CONDITION_TIPS.pgf`, `settings/Panel.lua:312`), but the box is drawn after
  the 8px gap **and** after the state line, so a different line sits between condition 4 and the link
  (`settings/Panel.lua:326-337`).
- **PRE-P09 (L): the colour pickers' labels are bare codes.** OCE, LA, CHI, MEX, BZL, ENG… are the tag text, which
  is useful, but what each code means is only in the hover tooltip (`settings/Panel.lua:119-120`). Each picker has a
  third of the width, which is room for "OCE — Oceanic".
- **PRE-P10 (L): the EU block leaves RUS alone on its line.** At three pickers per line, five US tags give 3+2 and
  seven EU tags give 3+3+1 (`settings/Panel.lua:111,156-158`). Four per line gives 4+1 and 4+3. Neither is perfect,
  and the lone RUS is the more visible orphan.
- **PRE-P11 (L): the preview lines have no label.** A line of coloured codes under a heading reads as decoration
  until you notice it changes when you pick a colour (`settings/Panel.lua:148`).
- **PRE-P12 (L): the "Reset region colors" button text says less than its tooltip.** The tooltip says "every
  **region tag**", the button says "region colors". Fixing PRE-P07 fixes this too (`settings/Panel.lua:164-165`).
- **PRE-P13 (L): the Master controls tab is mostly empty.** Being frameless, it holds Enable | Debug console, then
  Minimap button alone, then Reset all settings alone. That is correct by options-ui-§15 (frameless omits exactly
  scale, alpha, lock and reset position) and is listed only as context for PRE-L09. **Constrained: no change
  proposed inside the canonical set.**
- **PRE-P14 (L): the Enable label may crowd its half-width cell.** "Enable Ka0s Premade Groups Filter Extension"
  (≈ 43 characters) goes in a 50% cell, so at small UI scales it wraps or clips against *Debug console*. The label is
  fixed by options-ui-§15 ("Enable `<AddonName>`") and composed from `addonName` (`settings/Panel.lua:52`,
  `OptionsCompose.lua:473`). **Constrained**; see the upstream suggestions.
- **PRE-P15 (L): the EllesmereUI tab is a wall of red for most players.** Players without EllesmereUI see one
  disabled checkbox and four red "not ready" lines on a tab that cannot apply to them (`settings/Panel.lua:317-338`).
  It is informative, but it is the noisiest tab for the players who need it least. options-ui-§13 ("every row
  carries a group", one tab per section) keeps the row on a tab. **No hide proposed**; see PRE-L12.
- **PRE-P16 (L): the slash command list puts the feature verbs last.** `apply` and `clear` are what a player of this
  addon actually types, and they come after `diagnostics` (`settings/Slash.lua:49-51`). **But this is the collection's
  convention**: QuickComms (`… debug diagnostics perf check test preview why`) and DropWatcher (`… debug diagnostics
  perf lock unlock show …`) also list the reserved verbs first and the feature verbs after them. See *Considered and
  rejected* (PRE-L16).
- **PRE-P17 (L): the General page's file-header comment and many docs describe the four-tab layout and quote the
  current labels** (`settings/Panel.lua:2-13`; `docs/settings-panel.md:11,37-55`; `docs/schema.md:13-15`;
  `docs/profiles.md:4`; `docs/scope.md:23`; `docs/data-flow.md:18,68`; `docs/module-map.md:69`;
  `docs/ARCHITECTURE.md:12,101,106-107,309`; `docs/smoke-tests.md:54-57,203-237`; `README.md:53,73,87`). Tests pin the
  tab names and group: `tests/test_euisettings.lua:56-65` (tab order string), `tests/test_regiontags.lua:104,137-143`
  (`group == "Region colors"`, `SelectTab("general", "Region colors")`). Any change below has to update them in step.
- **PRE-P18 (L): the Region colors tab never says which portal is the player's.** Both portals are drawn for every
  player, but a player only ever sees one portal's tags (`modules/Regions.lua:31-33`). A US player tuning *ENG* sees
  nothing change and has no hint why.

## Proposed changes

Every change keeps every setting's key, default, range and behaviour. A moved schema row keeps its place in
`/pgfe list` here: `showRegionTags` is already listed between `filtersActive` and `regionColors.*`, and stays there,
because `FILTER_ROWS` is added before `REGION_ROWS` (slash-commands-§3: the listing follows the panel).

| id | change | reason | confidence | fixes |
|---|---|---|---|---|
| PRE-L01 | Move row *Show server regions in the Group Finder* (`showRegionTags`) from Tab *Filters* to Tab *Region colors* (renamed by L02), as the **first** row, solo, above the US heading, under a subsection heading **"Display"** (options-ui-§7: a tab that mixes control types MUST break them up with subsection headings, and the tab would now mix a checkbox, colour pickers and a button). Implementation, both points load-bearing: (a) give the row `group = REGION_GROUP` but keep it in its **own** row list, added **before** `REGION_ROWS`, and **never** inside `REGION_ROWS`: `Settings.ResetRegionColors` (`:134-139`) walks `REGION_ROWS`, so a row added there would make *Reset region tag colors* also reset `showRegionTags`, which is a behaviour change; (b) `renderRegionTab` indexes `byKey[row.regionKey]` (`:145`), which raises "table index is nil" for a row with no `regionKey`, so it must pick the switch out first (`row.path == "showRegionTags"`) and draw it with `Helpers.RenderField` before the first portal `Section`. | Puts the parent switch on the same tab as its twelve dependants, so the tags are a single-tab task. | 80% | P01, P02 |
| PRE-L02 | Rename Tab *Region colors* → **Region tags**. Update `L["Region colors"]` (its key and value: the key is the English source string) and every comment, doc and test that names it (P17). | The tab now holds the on/off switch as well as the colours. "Region tags" is what the feature is called in every tooltip. | 75% | P01, P07 |
| PRE-L03 | Relabel `showRegionTags`: "Show server regions in the Group Finder" → **"Show region tags in the Group Finder"**. Tooltip: change only the noun, "Put the group leader's region tag (OCE, LA, CHI, ENG, GER, ...) in front of each Group Finder listing, and each applicant's tag in front of their name. …"; the PremadeRegions sentence is unchanged. The attached panel's *Server regions* filter keeps its name (P07 note). | One noun for the display feature. The tab now says *Region tags*, and the row should match its tab. | 70% | P07 |
| PRE-L04 | Keep Tab *Filters* with `filtersActive` alone (solo), and add an explanatory TXT line under it (not a setting), drawn through the after-group seam (options-ui-§6: `AFTER_GROUP[FILTER_GROUP]`, beside the existing `MASTER_TAIL` entry at `:345-346`), so the tab stays on the library's default body: **"The filter options are on the panel under Premade Groups Filter's window: open the Group Finder, choose Dungeons, and it appears below PGF's filters."** | The settings tree's natural "where do I change the filters?" question then has an answer. The tab stays truthful once `showRegionTags` leaves it. | 70% | P02 |
| PRE-L05 | Relabel `filtersActive`: "Toggle PGF Extension Filters" → **"Use the extension's filters"** (sentence case, 27 characters, fits the attached panel's 300px row). Update `L.MSG_INACTIVE` in the same change: "The extension's filters are off; tick *Use the extension's filters* first." | Drops the redundant "Toggle" and the made-up "PGF Extension" name, and matches the collection's sentence case. "The extension" rather than "this addon": on the attached panel, which sits inside PGF's own window, "this addon" can read as PGF. The label is shared with the attached panel, so both surfaces stay in step. | 60% | P03 |
| PRE-L06 | Reword `L.FILTERS_ACTIVE_TOOLTIP` so it is true on both surfaces: "Off: removes this addon's block from Premade Groups Filter's advanced filter, and Apply does nothing until you tick it again. Your own filter text and the dungeon ticks are left as they are. On: writes the block back from the filter panel's options. The same switch is on the filter panel and in Settings (General > Filters). Separate from Enable, which turns the whole addon off." If the owner takes L09 instead of L04, the path in the tooltip becomes "General > Master controls". | Removes "the options below" and "also on the settings page", which are both false on the settings page. One string still serves both surfaces. | 80% | P04 |
| PRE-L07 | Fix the `euiSkin` tooltip: "Needs every condition listed above" → **"Needs every condition listed below"** (`settings/Panel.lua:188`, locale key in step). | The conditions are drawn under the switch. This is a factual error. | 95% | P05 |
| PRE-L08 | Move the PGF skin link box (EB) to directly under condition 4, before the 8px gap and the state line. Order: switch, gap, conditions 1-4, **link box (when missing)**, gap, state line. | Condition 4's "the link appears below" then points at the next widget. The state line stays the tab's closing summary. | 55% | P08 |
| PRE-L09 | *(Alternative to L04, owner's call; not recommended by default.)* Move `filtersActive` into Tab *Master controls* as a composer `extra` row on its own line after *Minimap button* (`MasterControls{ extra = { … } }`, `startsLine`, options-ui-§15 last bullet), and delete Tab *Filters* (tabs 4 → 3). The row keeps its `onChange` (`Apply.OnFiltersToggled`) and is not `sessionOnly`. | Fewer tabs, and the "turn the filters off" switch sits beside "turn the addon off", which is exactly the distinction its tooltip draws. Against: §15 says an extra must be addon-wide "the way the canonical rows do", and a reviewer could read `filtersActive` as a feature switch, which is what the file comment at `settings/Panel.lua:77-79` says today. L04's pointer line would have nowhere to go. | 45% | P02, P13 |
| PRE-L10 | Rename portal headings: "US realms (by data center)" → **"Americas and Oceania (US realms)"**; "EU realms (by language)" → **"Europe (EU realms)"**. | Accurate for MEX, BZL and OCE, and symmetric. The "by language / by data center" parenthetical was wrong for 3 of the 12 tags. | 65% | P06 |
| PRE-L11 | Prefix each preview line with a dim label, e.g. `|cff999999Preview:|r OCE LA CHI MEX BZL`. | Tells the player the coloured line is a live preview of their picks. | 45% | P11 |
| PRE-L12 | On the EllesmereUI tab, when condition 1 fails (EllesmereUI not loaded), draw one grey line under the switch, **"Only for EllesmereUI users. Nothing here applies without it."**, and keep the four condition lines as they are. | Tells a non-EllesmereUI player in one line that they can ignore the tab, without hiding any row (options-ui-§13 keeps the tab). Partly redundant with condition 1's own hint ("Install and enable EllesmereUI…"), hence the low score. | 40% | P15 |
| PRE-L13 | Picker labels: "OCE" → **"OCE — Oceanic"**, "LA" → "LA — Los Angeles", "CHI" → "CHI — Chicago", "MEX" → "MEX — Latin America", "BZL" → "BZL — Brazil", "ENG" → "ENG — English", "GER" → "GER — German", "FRA" → "FRA — French", "ITA" → "ITA — Italian", "SPA" → "SPA — Spanish", "POR" → "POR — Portuguese", "RUS" → "RUS — Russian". Settings-page labels only, from a new locale table; `NS.Regions.LABELS` stays as the tag text, so the panel menu and the Group Finder rows are unchanged. | Shows what each code means without a hover. The longest label ("MEX — Latin America", 19 characters) fits a ⅓ cell. | 50% | P09 |
| PRE-L14 | Relabel the reset button "Reset region colors" → **"Reset region tag colors"**. | The noun matches L02, L03 and the button's own tooltip. | 55% | P12 |
| PRE-L17 | Update every comment, doc, smoke-test step and test listed under P17 to the new map and labels, in the same commit as the change it describes. The two tests that pin `"Region colors"` and the tab-order string change with L02; the test titles that quote "Toggle PGF Extension Filters" change with L05. | Keeps the docs true (documentation drift) and the suite green. Required whenever any of L01-L14 or L18 lands. | 95% | P17 |
| PRE-L18 | *(New.)* Mark the player's own portal heading with a dim suffix, e.g. "Europe (EU realms) |cff999999— your realms|r", read from `NS.Regions.GetPortal()` at render time. Do **not** reorder the portals: the panel order would then differ per player from `/pgfe list` (slash-commands-§3). | A player tuning the other portal's colours learns why nothing changes. Text only. | 45% | P18 |

### Considered and rejected

- **PRE-L15 (was 30%): `PICKERS_PER_LINE` 3 → 4.** It only helps if L13 is not taken (L13's longer labels need the
  ⅓ width), it trades the lone RUS for a lone BZL, and it is a nitpick on a tab most players open once.
- **PRE-L16 (was 40%, now 20%): reorder `NS.COMMANDS` so `apply, clear` follow `config`.** The current order — reserved
  verbs first, feature verbs after `diagnostics` — is the collection's convention (QuickComms, DropWatcher). Moving
  PGFE's alone would make it the odd one out on the landing page and in `/pgfe help`, which is the inconsistency
  item 020 is meant to remove. If the owner wants feature verbs first, it is a collection-wide rule for
  slash-commands-§4, not a PGFE change.
- **Reordering the portals so the player's own comes first.** Panel order would then differ per player from
  `/pgfe list` (slash-commands-§3). L18 marks the portal instead.
- **Renaming condition 3's "PremadeGroupsFilterExtension".** It is the folder name, but it is exactly the text
  EllesmereUI's Third-Party Addons list shows, which is what the player has to find.

Not proposed:
- Changing the Master controls rows or order, because options-ui-§15 forbids it (P13, P14).
- Removing the header *Defaults* button or the duplicate *Reset all settings*: options-ui-§12 mandates both, as one act.
- Hiding the EllesmereUI tab without EllesmereUI. That would break options-ui-§13's "every row carries a group",
  and the conditions are the help text (P15).
- Greying the colour pickers while `showRegionTags` is off. It would be a new `disabledIf`, which is UI behaviour,
  so it is left out under "no behaviour change". If the owner wants it, it is a one-line `disabledIf` per row,
  at 60% confidence.
- Moving any attached-panel filter option into the settings page. That would add settings to a schema that
  deliberately excludes them (`settings/Schema.lua:7-9`).

## Proposed map

With the recommended set (L01-L08, L10-L14, L17, L18; **not** L09):

```
Ka0s Premade Groups Filter Extension (landing)   settings/Panel.lua:30-42 (unchanged builder)
  untabbed
  - logo, tagline
  - Section "Slash Commands": help, config, enable, disable, version, list, get, set, reset, resetall, profile,
                              debug, diagnostics, apply, clear                      (15 rows, order unchanged)

General
  Header band: [Defaults BTN]                    (unchanged: options-ui-§12)
  Tab "Master controls"                          (unchanged: options-ui-§15)
    [Enable Ka0s Premade Groups Filter Extension  CB enabled]   [Debug console  CB state.debugConsole]
    [Minimap button  CB global.minimap.shown]
    [Reset all settings BTN]
  Tab "Filters"
    [Use the extension's filters  CB filtersActive]                                (solo)
    TXT "The filter options are on the panel under Premade Groups Filter's window: open the Group Finder,
         choose Dungeons, and it appears below PGF's filters."                     (after-group hook)
  Tab "Region tags"
    Heading "Display"
      [Show region tags in the Group Finder  CB showRegionTags]                     (solo)
    Heading "Americas and Oceania (US realms)"   (+ dim "— your realms" on the player's portal)
      TXT "Preview:" OCE LA CHI MEX BZL
      [OCE — Oceanic  CP regionColors.oce]  [LA — Los Angeles  CP regionColors.la]  [CHI — Chicago  CP regionColors.chi]
      [MEX — Latin America  CP regionColors.mex]  [BZL — Brazil  CP regionColors.bzl]
    Heading "Europe (EU realms)"
      TXT "Preview:" ENG GER FRA ITA SPA POR RUS
      [ENG — English  CP regionColors.eng]  [GER — German  CP regionColors.ger]  [FRA — French  CP regionColors.fra]
      [ITA — Italian  CP regionColors.ita]  [SPA — Spanish  CP regionColors.spa]  [POR — Portuguese  CP regionColors.por]
      [RUS — Russian  CP regionColors.rus]
    [Reset region tag colors BTN]                (resets the 12 colours only, as today)
  Tab "EllesmereUI skin"
    [Use the EllesmereUI skin  CB euiSkin]   (tooltip: "...listed below...")
    TXT (only when EllesmereUI is not loaded) "Only for EllesmereUI users. Nothing here applies without it."
    (12px gap)
    TXT condition 1..4
    EB  PGF skin CurseForge link (only when missing)                                 (moved up)
    (8px gap)
    TXT state line

Profiles                                         (unchanged; AceDBOptions)
```

Counts after: 3 pages, 4 tabs, 18 schema rows (Master controls 3, Filters 1, Region tags 13, EllesmereUI skin 1).
With L09 instead of L04 it would be 3 tabs (Master controls 4, Region tags 13, EllesmereUI skin 1).

## Cross-addon notes / Upstream suggestions

Cross-addon notes:
- **"Feature switch" placement.** PGFE puts an addon-wide feature switch (`filtersActive`) on its own General tab
  and not in Master controls. QuickComms' *Preview as* went the other way, through the composer's `extra`
  (options-ui-§15). The collection should settle the test for "addon-wide the way the canonical rows do", so that
  the same kind of switch lands in the same place in every addon.
- **Third-party skin surface.** PGFE has a whole *EllesmereUI skin* tab (switch, four live condition lines, state
  line, link box). QuickComms also registers an EllesmereUI skin (`QuickComms/settings/CalloutPopup_Skin.lua`) with no
  switch or status tab in its settings. One concept is surfaced two ways. If both keep a skin, they should share a
  tab name ("EllesmereUI skin") and a shape, or the status-lines tab should become a library composer.
- **Colour tabs.** PGFE's *Region tags* is a host-drawn picker grid with a local reset button. Addons with a
  "reset these colours" act should word it the same way ("Reset <thing> colors") and put it at the foot of the tab.
- **Sentence case.** "Toggle PGF Extension Filters" is the only Title Case row label in PGFE. Check the other addons
  for the same drift.
- **Slash verb order.** PGFE, QuickComms and DropWatcher all list reserved verbs first and feature verbs last. Keep
  that as the convention (or change it collection-wide), not per addon.
- **Defaults tooltip wording.** PGFE, QuickComms and DropWatcher share "Reset every %s setting to its default. Asks
  for confirmation." on the General header button, while the reset resets the active profile only (options-ui-§12).
  If the wording is revisited, revisit it for all three together.
- **Not a window addon.** PGFE gets no Keybindings tab and no binding category under item 015.

Upstream suggestions (WowAddonStandards / LibKa0s):
- **options-ui-§15, Enable label length.** "Enable `<AddonName>`" with the full "Ka0s …" title makes the longest row
  label in several addons and crowds a 50% cell (PRE-P14). Suggest allowing the composer a `shortName`, for example
  "Enable Premade Groups Filter Extension", or letting the Enable row take its line alone (`solo`) when the label
  overflows the cell.
- **options-ui-§15, frameless Master controls.** A frameless addon's tab is two lines and a button. The standard
  could say outright whether a frameless addon's addon-wide feature switch qualifies as an `extra` (PRE-L09), because
  today that is a judgement call each addon makes differently.
- **options-ui-§7 / §13, explanatory text rows.** There is no first-class "help line" row type for a tab that
  needs to point elsewhere (PRE-L04, L12). Hosts draw a `TextRow` by hand. A schema-declared `note` row, rendered
  dim and full width and skipped by `/list`, would keep that out of host code.
- **options-ui-§7, a lead switch above subsections.** §7 makes PRE-L01 add a one-checkbox "Display" heading. A tab
  whose first row is the on/off switch for everything under it could reasonably carry that switch unheaded; the
  standard could allow one leading master-switch row before the first subsection heading.

## Review

Independent review against the code at `master` e5b741a (2026-10-24). Changes made to this file:

- **Current map.** Added the General page's header *Defaults* button (`defaultsButton = true`,
  `settings/Panel.lua:351-355`), which the map omitted; noted that *Reset all settings* is drawn by the
  `MASTER_TAIL` after-group hook; noted that the status lines are InteractiveLabels with tooltips; noted that both
  portals are always drawn although a player sees only one; noted Profiles has no Defaults button. Button count
  2 → 3.
- **PRE-L01 rewritten (85% → 80%).** As written it said to add `showRegionTags` "in `REGION_ROWS` order". That would
  have changed behaviour: `Settings.ResetRegionColors` walks `REGION_ROWS`, so *Reset region colors* would also reset
  `showRegionTags`. It would also crash `renderRegionTab` (`byKey[nil]`). Both are now spelled out. Added the
  options-ui-§7 subsection heading ("Display") the mixed-control tab requires, which the original did not mention.
- **PRE-L05 relabel changed** from "Use this addon's filters" to "Use the extension's filters" (65% → 60%): on the
  attached panel inside PGF's window, "this addon" is ambiguous.
- **PRE-L04** now names the mechanism (options-ui-§6 after-group seam) so the tab stays on the library body
  (75% → 70%). **PRE-L06** notes the tooltip's path follows the L04/L09 choice.
- **PRE-L16 moved to *Considered and rejected* (40% → 20%):** the current verb order is the collection convention
  (QuickComms, DropWatcher), so the change would add inconsistency. P16 updated to say so.
- **PRE-L15 (30%) moved to *Considered and rejected*,** as the brief requires for anything under 40%.
- **PRE-P17 / PRE-L17 widened:** the original listed only `settings/Panel.lua` and `docs/settings-panel.md`. The labels
  and tab names are also in seven other docs, the README FAQ, the smoke tests, and two tests that pin
  `"Region colors"` and the tab-order string.
- **PRE-P07** now separates the filter noun (*Server regions*, kept) from the display noun (*region tag*), and L03
  says the panel filter keeps its name.
- **New PRE-P18 / PRE-L18 (45%)**: mark the player's own portal; reordering was considered and rejected because of
  slash-commands-§3.
- **Recalibrated:** L08 60 → 55, L10 70 → 65, L11 50 → 45, L12 50 → 40, L13 55 → 50. L07, L17 unchanged at 95.
- **Proposed map**: slash order unchanged, new labels, "Display" heading, portal marker. Added cross-addon notes
  (verb order, Defaults tooltip wording) and one upstream suggestion (§7 lead switch).
- Checked and found correct: the Master controls composition (frameless, no visibility, Enable | Debug console,
  Minimap alone, Reset alone; `OptionsCompose.lua:458-574`), all line references in the original map, and that no
  proposed change alters a key, default, range or `onChange`.
