# LootHistory — settings layout analysis

Item 020. Read-only analysis of `../LootHistory` on `master`. No setting key, default, range or
behaviour changes anywhere below. Every change is a move, a regroup, a reorder or a reword.

Sources read: `settings/Panel.lua`, `settings/Schema.lua`, `settings/OptionsSetup.lua`,
`settings/Profiles.lua`, `settings/Slash.lua` (popups), `core/Constants.lua` (option lists),
`libs/LibKa0s/OptionsCompose.lua` (`O.MasterControls`), `docs/settings-panel.md`,
`tests/test_schema.lua` and `tests/test_panel.lua` (the layout invariants the suites pin), and
`../WowAddonStandards/standards/standards/options-ui.md` §6, §7, §13, §14 and §15.

## Current map

Settings tree: **Ka0s Loot History** (landing page) > **General** > **Profiles**.

```
Ka0s Loot History  [landing page; untabbed, exempt from the strip, options-ui-§13]
│   built: OptionsSetup.lua:239 (buildMain) -> Panel.lua:1057 P.BuildMain -> Panel.lua:898 buildMainContent
│   logo (300px) · tagline · "Slash Commands" heading · one Label per NS.COMMANDS row
│
├── General  [subcategory; registered Panel.lua:1095; renderer Panel.lua:1001; strip GENERAL_TABS Panel.lua:972]
│   │   page chrome: breadcrumb header + Defaults button (= the global reset, Panel.lua:1075)
│   │
│   ├── Tab 1  Master controls      [composed: Schema.lua:76 -> LibKa0s OptionsCompose.lua:458;
│   │                                stamped Schema.lua:160; afterGroup Panel.lua:948]
│   │     line 1  Enable Loot History ............ checkbox  settings.enabled
│   │             General visibility ............. dropdown  settings.visibility
│   │     line 2  Master scale ................... slider    settings.scale
│   │             Master alpha ................... slider    settings.alpha
│   │     line 3  Lock frame ..................... checkbox  settings.locked
│   │             Debug console .................. checkbox  state.debugConsole   (session-only)
│   │     line 4  Minimap button ................. checkbox  minimap.shown        (global store)
│   │             Test mode ...................... checkbox  state.testMode       (session-only)
│   │     line 5  [Reset position] [Reset all settings]   button pair (afterGroup)
│   │
│   ├── Tab 2  Capture              [rows Schema.lua:280-329; afterGroup Panel.lua:940]
│   │     line 1  Minimum quality (detailed records)  dropdown  settings.qualityThreshold
│   │             Record currency ................ checkbox  settings.recordCurrency
│   │     line 2  Track holdings and losses ...... checkbox  settings.trackLedger
│   │             Record gold .................... checkbox  settings.recordGold
│   │     line 3  Exclude quest items ............ checkbox  settings.excludeQuestItems
│   │             (empty cell: settings.excludedSources is type=table and draws no widget)
│   │     block   "Record data from" InlineGroup, one checkbox per C.SOURCE_OPTIONS entry, inverted
│   │             settings.excludedSources  (host-drawn, Panel.lua:60 makeMultiCheck)
│   │
│   ├── Tab 3  AH Price             [rows Schema.lua:339-355; afterGroup Panel.lua:945 -> :781]
│   │     subgroup heading "Pricing"
│   │     line 1  Enable AH pricing .............. checkbox  settings.auction.enabled
│   │     subgroup heading "Price sources"  (declared by the skipRender row settings.auction.capture)
│   │     block   description Label (Panel.lua:787)
│   │     block   price table, 11 pooled rows (Panel.lua:781-890); columns
│   │             [drag handle] [tick] Addon | Price Module (+ⓘ) | On (checkbox) | Status
│   │             backs settings.auction.capture + the carve-out settings.auction.priority
│   │
│   ├── Tab 4  Interface            [rows Schema.lua:370-418]
│   │     subgroup heading "Window"
│   │     line 1  Window scale ................... slider    settings.windowScale
│   │             Row height ..................... slider    settings.rowHeight
│   │     line 2  Timeline lines ................. slider    settings.timelineMaxLines
│   │     subgroup heading "Simulator"
│   │     line 3  Simulation step delay .......... slider    settings.sim.stepDelay
│   │
│   ├── Tab 5  History              [rows Schema.lua:439-480; afterGroup Panel.lua:946 -> :101]
│   │     line 1  Keep history for ............... dropdown  settings.retentionDays        (global)
│   │             Keep Timeline days for ......... dropdown  settings.rollupRetentionDays  (global)
│   │     line 2  Show transfers by default ...... checkbox  settings.showTransfers
│   │     line 3  storage readout Label | [Purge history…] button   (renderHistory, Panel.lua:101)
│   │
│   └── Tab 6  Filters              [bespoke: Panel.lua:979 -> buildFiltersTab :444; lists FILTER_TABS :411]
│         secondary strip (O.SubTabStrip, Panel.lua:467): Blacklist | Whitelist | Currencies
│         each sub-tab (makeFilterSection, Panel.lua:293):
│           description Label · [Clear all] (30% button, Panel.lua:275) · IdList: add box
│           ("Add item id, link or name" / "Add currency id, link or name") + 2-column entry list
│
└── Profiles  [AceDBOptions page, registered last, Panel.lua:1106 -> Profiles.lua:26; exempt from the strip]
```

**Counts.** 3 pages (landing, General, Profiles), 2 of them Blizzard subcategories. 6 primary tabs
on General plus 3 secondary sub-tabs under Filters. 23 schema rows (8 Master controls, 6 Capture,
2 AH Price, 4 Interface, 3 History). On screen that is 20 schema widgets, 1 inverted multi-check
group, 1 11-row price table, 2 composer-emitted buttons (Reset position, Reset all settings, from
`O.MasterControls`' afterGroup), 2 host buttons (Purge history…, and Clear all drawn once per filter
sub-tab) and 3 id-lists.

Layout pins that any change below must move in the same commit: `tests/test_panel.lua:333` (the
per-tab subsection heading list, `Interface = { "Window", "Simulator" }`), the label pins on
"Minimum quality (detailed records)" (test_panel.lua:115, :148, :151, :182, :267, :425), the strip
index pins (:166, :190), the ≥ 2 rows per tab rule (test_schema.lua:716), and the label prose in
`docs/settings-panel.md`, `docs/schema.md`, `docs/smoke-tests.md` and `README.md`.

## Problems

| id | file:line | problem |
|---|---|---|
| LOO-P01 | Schema.lua:441 vs Constants.lua:191 | The **Keep history for** tooltip says "'Never' keeps everything", but the dropdown's option is **Always**, so the tooltip names a choice the player cannot find. The Constants comment at :182 says "Never" too. The Timeline row beside it (Schema.lua:461) correctly says 'Always'. |
| LOO-P02 | Schema.lua:474-480 | **Show transfers by default** is a default for the History *window's* Direction filter, a view setting. It sits on the History *settings* tab, which is otherwise about how long data is kept and how to purge it. A player tuning the window has to visit Interface and then History. |
| LOO-P03 | Schema.lua:474, Panel.lua:972 | "History" names three different things: the settings tab (retention), the window's first tab (the table) and "the History window" itself. **Show transfers by default** on the History settings tab reads as if it configures the History settings tab. |
| LOO-P04 | Schema.lua:280-329 | **Capture** mixes two subjects with no subsection heading: the *loot record* gates (quality, currency, quest items, sources) and the *ledger* (holdings, gold). options-ui-§7 says a tab mixing kinds of control MUST carry subsection headings, and this tab mixes a dropdown, checkboxes and a full-width multi-check group. |
| LOO-P05 | Schema.lua:297-311, Collector.lua:313 | **Record gold** does nothing unless **Track holdings and losses** is on (`if not (trackLedger and recordGold)`), but neither the layout nor the tooltip says so. They happen to pair on one line now only by declaration order. |
| LOO-P06 | Schema.lua:299-300 | The **Track holdings and losses** tooltip says "(from the next update) every gain, loss and transfer". The update shipped, so the parenthesis is stale. |
| LOO-P07 | Schema.lua:313, render | **Exclude quest items** ends up alone on line 3 with an empty right cell, and it is separated from the quality gate, the other item-level gate. |
| LOO-P08 | Schema.lua:291-292, Panel.lua:420-421 | The terminology does not match. Tooltips and list descriptions say "per-source mute list" and "muted source", but the control the player sees is labelled **Record data from** and is ticked to *record*, not to mute. |
| LOO-P09 | Panel.lua:972-980 | Tab order splits one task. "What gets recorded" lives on **Capture** (tab 2) and **Filters** (tab 6), with AH Price, Interface and History in between, so blocking an item after unticking a source means four tabs of travel. |
| LOO-P10 | Schema.lua:341 | The **Pricing** subsection heading over the lone **Enable AH pricing** row is a one-row section that nearly repeats its tab ("AH Price"). The test only catches an exact repeat (test_panel.lua:361). |
| LOO-P11 | Panel.lua:976, Schema.lua:341 | The tab is called **AH Price**, its toggle **Enable AH pricing**, and the docs say "AH pricing". The tab name is the odd one out, and as a singular noun it reads as a single value rather than a feature. |
| LOO-P12 | Panel.lua:826-827 | The price-table headers are Title Case (**Price Module**) while every other label in the panel is sentence case ("Price sources", "Row height"). |
| LOO-P13 | Schema.lua:378 | The **Window scale** tooltip, "Scale of the History browser window.", does not say that it multiplies on top of **Master scale**, which is two tabs away (the docs say it does). It also uses "History browser window", a third name for the window. |
| LOO-P14 | Schema.lua:398-405 | **Timeline lines** is alone on line 2 of the Window subsection. |
| LOO-P15 | Schema.lua:412-418 | The **Simulator** subsection holds one row, so it is a lonely section. It is consistent with BankLedger's Interface > Simulator, so it is kept on purpose (see Cross-addon notes). |
| LOO-P16 | Schema.lua:459 | **Keep Timeline days for** is awkward ("keep days for 90 days") and does not parallel **Keep history for** directly beside it. |
| LOO-P17 | Schema.lua:281 | **Minimum quality (detailed records)** carries its qualifier as a parenthesis in the label. BankLedger calls the same concept **Minimum quality**. The nuance belongs in the tooltip, which already explains it. |
| LOO-P18 | Panel.lua:279 | **Clear all** opens a confirm dialog but has no ellipsis, while **Purge history…** (Panel.lua:113) follows the ellipsis-means-dialog convention. |
| LOO-P19 | Panel.lua:413-428 | The three list descriptions state the point-in-time rule three different ways: a long parenthesis on Blacklist, nothing on Whitelist, "Point-in-time —" on Currencies. |
| LOO-P20 | Panel.lua:411-426 | The sub-tab labels use mixed axes. **Blacklist** and **Whitelist** name the list type and leave out "items"; **Currencies** names the object type and leaves out "blacklist". |
| LOO-P21 | Schema.lua:248-250 | The **Test mode** tooltip says it fills "the History window and Insights". It also fills Holdings and the Timeline (docs/settings-panel.md, and the strip tip at Browser.lua:888). |
| LOO-P22 | Panel.lua:972 (planned) | The planned **Keybindings** tab has no position defined yet. If each of the 7 addons slots it in a different place, the cross-addon "learn one page, know them all" property of options-ui-§13 breaks. |
| LOO-P23 | Master controls + Interface + History | Window furniture is spread over three tabs: Lock frame, Reset position and Master scale on Master controls; Window scale, Row height and Timeline lines on Interface; Show transfers on History. The Master controls part is **fixed by options-ui-§15** (canonical set, MUST NOT split), so only the Interface/History split is fixable (LOO-P02). |
| LOO-P24 | Panel.lua:1075 + Master controls | The page's **Defaults** button and **Reset all settings** are the same act, drawn twice on one page. This is **mandated** by options-ui-§12/§13 and is not changed here (see Upstream suggestions). |
| LOO-P25 | Schema.lua:313 | **Exclude quest items** is the only negatively phrased toggle among positive "Record …" rows (Record currency, Record gold, Record data from). Rewording it to "Record quest items" would invert the stored meaning, which is **forbidden**, so this is noted only. |
| LOO-P26 | Panel.lua:781, Schema.lua:339 | The price table stays fully interactive when **Enable AH pricing** is off. Dimming it would be a behaviour change, so it is out of scope for 020 and noted only. |
| LOO-P27 | Schema.lua:277-279 | The schema comment describing Capture's pairing ("Exclude quest items opens the second") is stale since trackLedger and recordGold were added. It is a code comment, but it is the layout's own documentation. |
| LOO-P28 | Panel.lua:420, Schema.lua:291-292 | Two more names for **Minimum quality**: the Whitelist description says "fall below your **quality threshold**" and the Record currency tooltip says "ignores the **minimum-quality filter**". The control the player can find is labelled "Minimum quality (detailed records)". Same class as LOO-P08. |
| LOO-P29 | locales/enUS.lua:23, Bindings.xml (planned item 015) | The planned **Keybindings** tab holds **one** control in LootHistory (the addon ships one binding, `CLICK LootHistoryToggleWindow:LeftButton`). The addon's own rule "no tab holds fewer than two controls" (test_schema.lua:716, "a tab over one control is a click that reveals a single dropdown") counts schema groups only, so it will not fire if the binding is not a schema row, but the tab breaks its spirit. The owner asked for the tab by name, so it stays; the exemption has to be written down (Upstream suggestion 7). |
| LOO-P30 | Panel.lua:972 (planned) | Seven primary tabs (Master controls, Capture, AH Price, Interface, History, Filters, Keybindings) at roughly 75-115px each may wrap the strip to a second row on the settings canvas at default UI scale. options-ui-§13 permits a wrap but says a page SHOULD fit one row. Not measured in-session; it is the owner's in-client check. |
| LOO-P31 | Panel.lua:963-967 | Filters' current last position is **deliberate**: the comment records that "Filters moved from third to last so the five shared tabs sit in the shared order" with BankLedger. LOO-P09's travel cost is real, but any reorder reverses a recorded decision and has to land in both addons. |

## Proposed changes

| id | change | reason | confidence | fixes |
|---|---|---|---|---|
| LOO-L01 | Reword the `settings.retentionDays` tooltip "'Never' keeps everything" → "'Always' keeps everything" (Schema.lua:441), and the Constants.lua:182 comment to match. | The tooltip must name an option that exists. | 95% | P01 |
| LOO-L02 | Move row **Show transfers by default** (`settings.showTransfers`) from History > (no subsection) to Interface > subsection History window, directly after **Timeline lines**, so the two pair on line 2. | It is a window view default, not a retention setting. It also fills the empty cell beside Timeline lines, and History keeps 2 stored rows, so the ≥2 rule (test_schema.lua:716) still holds. | 75% | P02, P03, P14, P23 |
| LOO-L03 | Rename the Interface subsection heading **Window** → **History window** (`subgroup` on windowScale, rowHeight, timelineMaxLines and now showTransfers). Move the test_panel.lua:333 pin with it. | It disambiguates from the export and copy windows and from Master scale, and matches the name the tooltips use after L12/L19. It does not repeat the tab name, so test_panel.lua:361 still passes. Against it: it puts the word "History" on a second tab (P03's own complaint), and BankLedger's equivalent is the plural **Windows**. | 50% | P03, P13 |
| LOO-L04 | Split **Capture** into two subsections. **Loot**: line 1 `Minimum quality` (qualityThreshold) \| `Exclude quest items` (excludeQuestItems); line 2 `Record currency` (recordCurrency), then the **Record data from** picker. **Ledger**: line 1 `Track holdings and losses` (trackLedger) \| `Record gold` (recordGold). Implementation: the picker currently hangs off `afterGroup`, which fires after the *group's* last row, so the host either renders Capture's two subgroup slices with two `O.RenderRows` calls (picker between them; Panel.lua:1049 already calls RenderRows by hand) or the library gains an after-subgroup hook. The fallback if neither is wanted is **Ledger first, Loot second**, which keeps the picker last with zero host change (55%). | options-ui-§7 requires the headings. It puts the two item gates side by side, lets Record currency sit directly above the source picker it obeys, and puts the parent toggle (ledger) left of its dependent (gold). | 65% | P04, P05, P07, P27 |
| LOO-L05 | Append to the `settings.recordGold` tooltip: "Needs Track holdings and losses." | Says in words a dependency that already exists (Collector.lua:313). | 85% | P05 |
| LOO-L06 | Drop "(from the next update)" from the `settings.trackLedger` tooltip (Schema.lua:299-300). | Stale. | 90% | P06 |
| LOO-L07 | One name per control in prose. (a) "Obeys the per-source mute list; ignores the minimum-quality filter" → "Obeys Record data from; ignores Minimum quality" (`settings.recordCurrency` tooltip, Schema.lua:291-292). (b) Whitelist description (Panel.lua:420-421) "fall below your quality threshold, come from a muted source" → "fall below Minimum quality, come from a source unticked under Capture ▸ Record data from". Tooltip and description text only. | One name for one control; a player can search the panel for the words the tooltip uses. | 85% | P08, P28 |
| LOO-L08 | Reorder GENERAL_TABS (Panel.lua:972) to **Master controls, Capture, Filters, AH Price, Interface, History** (+ Keybindings, L18). This needs the same move in BankLedger (Master controls, Capture, Filters, Interface, History) so the shared five stay in shared order, as the Panel.lua:963-968 comment requires; rewrite that comment and the Schema.lua:422 "the Filters tab that follows it" comment. Update the test_panel STRIP pins (tab indices at :166, :190). | It puts "what gets recorded" (Capture → Filters) on adjacent tabs. AH Price still directly follows the recording tabs it qualifies. It **reverses a recorded decision** (P31: Filters was third once and was moved last for the BankLedger convergence), so it is two-repo and owner-visible. | 55% | P09, P31 |
| LOO-L09 | Rename tab **AH Price** → **AH Pricing** (the `group` of the two AH rows, the GENERAL_TABS key, the AFTER_GROUP key at Panel.lua:945, and docs). This is a group, not a stored path, so no migration (options-ui-§15). Ripple: the literal "AH Price" is pinned in nine test files (tests/panel_support.lua, test_panel.lua, test_panel_auction.lua, test_schema.lua, test_profiles.lua, test_auctionprice.lua, test_libka0s.lua, test_mediasetup.lua, test_widgets.lua) and about a dozen living docs. The Holdings column header "AH Price" (HoldingsTab.lua:36) stays: a column names a value, so it is correctly singular. | Matches the toggle "Enable AH pricing" and the docs' own term. The gain is one word; the cost is a wide rename and a tab name players already know. | 45% | P11 |
| LOO-L10 | Remove `subgroup = "Pricing"` from `settings.auction.enabled` (Schema.lua:341), so the toggle opens the tab unheaded and **Price sources** is the one subsection break before the table. | It removes a one-row near-duplicate heading. The tab still separates its two kinds of control with a heading (options-ui-§7: "break them up"). If an audit reads §7 as "every block headed", keep it but rename to **Master switch** instead. | 50% | P10 |
| LOO-L11 | Price-table header **Price Module** → **Price module** (Panel.lua:826). | Sentence case like every other label. | 70% | P12 |
| LOO-L12 | `settings.windowScale` tooltip → "Scale of the History window, multiplied on top of Master scale (Master controls)." | It surfaces the cross-tab relationship and uses one name for the window. | 85% | P13 |
| LOO-L13 | Label **Keep Timeline days for** → **Keep Timeline history for** (Schema.lua:459). | Parallel with **Keep history for** on the same line. | 65% | P16 |
| LOO-L14 | Label **Minimum quality (detailed records)** → **Minimum quality** (Schema.lua:281); the tooltip is unchanged and already carries the "detailed record" nuance. Only with L04 (under a **Loot** heading the short label is unambiguous). Six label pins in test_panel.lua move with it. | Matches BankLedger and drops the label parenthesis. Against it: the parenthesis is the only on-screen hint that the ledger still sees every item, and the Loot heading carries only part of that. | 50% | P17 |
| LOO-L15 | Button **Clear all** → **Clear all…** (Panel.lua:279). | Ellipsis = opens a dialog, like Purge history…. | 80% | P18 |
| LOO-L16 | Give all three list descriptions one closing sentence: "Applies to future loots only; rows already recorded are left as they are." Trim Blacklist's parenthesis to its first sentence plus this one; add it to Whitelist (whose removal is also point-in-time per docs); replace Currencies' "Point-in-time —" clause. | Same rule, same words. | 70% | P19 |
| LOO-L17 | Sub-tab label **Currencies** → **Currency blacklist** (Panel.lua:426), keeping **Blacklist** and **Whitelist** as they are, and the one chat line that cites the path (BrowserTable.lua "Manage in Settings ▸ General ▸ Filters ▸ Currencies." → "▸ Currency blacklist."). | It fixes the axis mismatch where it actually is: two item lists named by list type and one named by object type. Keeping Blacklist/Whitelist bare keeps them identical to BankLedger's Filters sub-tabs (BankLedger Panel.lua:414, :418), where every list is an item list. Rewritten from "Item blacklist \| Item whitelist \| Currency blacklist" (45%), which would have diverged from BankLedger and re-added the words the Panel.lua:360-363 comment trimmed. | 55% | P20 |
| LOO-L18 | Planned Keybindings tab: add it as the **last** primary tab, named **Keybindings**, holding the "Toggle Loot History window" binding (CLICK LootHistoryToggleWindow:LeftButton, Bindings.xml; label from locales/enUS.lua) under no subsection (one subject). It is a one-control tab (P29), so it needs the exemption in Upstream suggestion 7 and, if the binding is ever made a schema row, a named exemption in test_schema.lua:716. | Last is the only position that can be identical in all 7 windowed addons, whose tab sets differ. It also keeps the shared BankLedger order intact. | 75% | P22, P29 |
| LOO-L19 | **Test mode** tooltip (Schema.lua:248) → "Fill the History window (History, Insights, Holdings and Timeline) with a sample loot history and holdings…" (rest unchanged). | Tooltip matches what the mode shows. | 80% | P21 |
| LOO-L20 | Rewrite the Schema.lua:277-279 comment to describe the L04 lines. | Keeps the declaration-order-is-layout comment true. | 90% | P27 |

**Considered and rejected (under 40%)**

| id | change | why rejected | confidence |
|---|---|---|---|
| LOO-L21 | Rename tab **History** → **Retention** in LootHistory *and* BankLedger. | It would remove the triple meaning of "History" (P03) once L02 leaves the tab holding only keep-for rows and purge, but it reverses a deliberate two-addon convergence (Panel.lua:963-968, Maintenance → History) and "Retention" is jargon next to "Keep history for". | 35% |
| LOO-R01 | Move the planned binding onto Interface (beside Simulation step delay) instead of a one-control Keybindings tab (P29). | The owner asked for a Keybindings tab inside General by name (item 015), and it must look the same in all 7 windowed addons. | 15% |
| LOO-R02 | Merge **History** (retention) into **Capture** to cut a tab. | Capture is "what is written", History is "how long it is kept and how to delete it"; mixing a confirm-gated prune row into the capture toggles puts a destructive control among everyday ones. It also breaks BankLedger parity. | 25% |
| LOO-R03 | Fold Filters' three sub-tabs into one scrolling tab with three subsections. | Each IdList is unbounded and two-column; three on one scroll pushes the Currencies list off-screen. options-ui-§13 explicitly permits a secondary strip for "a list of like subjects". | 20% |

Not changed, by rule: the Master controls set and its order (options-ui-§15), Master controls first
(§15, anti-pattern #68), Profiles last (§3), the landing page's untabbed form (§5/§13), the Defaults
button (§12/§13), and Filters' secondary strip (permitted by §13; LootHistory has no nav rail, so
the three-level ban is not hit).

## Proposed map

All of LOO-L01..L20 are applied (L17 in its rewritten form); L21 is rejected.

```
Ka0s Loot History  [landing page — unchanged]
│
├── General
│   ├── Tab 1  Master controls      [unchanged — options-ui-§15]
│   │     line 1  Enable Loot History ............ checkbox  settings.enabled
│   │             General visibility ............. dropdown  settings.visibility
│   │     line 2  Master scale ................... slider    settings.scale
│   │             Master alpha ................... slider    settings.alpha
│   │     line 3  Lock frame ..................... checkbox  settings.locked
│   │             Debug console .................. checkbox  state.debugConsole
│   │     line 4  Minimap button ................. checkbox  minimap.shown
│   │             Test mode ...................... checkbox  state.testMode     (tooltip L19)
│   │     line 5  [Reset position] [Reset all settings]
│   │
│   ├── Tab 2  Capture
│   │     subgroup heading "Loot"
│   │     line 1  Minimum quality ................ dropdown  settings.qualityThreshold   (L14)
│   │             Exclude quest items ............ checkbox  settings.excludeQuestItems
│   │     line 2  Record currency ................ checkbox  settings.recordCurrency     (tooltip L07)
│   │     block   "Record data from" multi-check   settings.excludedSources
│   │     subgroup heading "Ledger"
│   │     line 3  Track holdings and losses ...... checkbox  settings.trackLedger        (tooltip L06)
│   │             Record gold .................... checkbox  settings.recordGold         (tooltip L05)
│   │
│   ├── Tab 3  Filters              (moved from 6th, L08)
│   │     secondary strip: Blacklist | Whitelist | Currency blacklist                  (L17)
│   │     each: description (unified closing sentence, L16) · [Clear all…] (L15) · IdList
│   │
│   ├── Tab 4  AH Pricing           (renamed, L09)
│   │     line 1  Enable AH pricing .............. checkbox  settings.auction.enabled   (no heading, L10)
│   │     subgroup heading "Price sources"
│   │     block   description Label
│   │     block   price table: [handle] [tick] Addon | Price module (+ⓘ) | On | Status   (L11)
│   │
│   ├── Tab 5  Interface
│   │     subgroup heading "History window"                                            (L03)
│   │     line 1  Window scale ................... slider    settings.windowScale        (tooltip L12)
│   │             Row height ..................... slider    settings.rowHeight
│   │     line 2  Timeline lines ................. slider    settings.timelineMaxLines
│   │             Show transfers by default ...... checkbox  settings.showTransfers      (moved, L02)
│   │     subgroup heading "Simulator"
│   │     line 3  Simulation step delay .......... slider    settings.sim.stepDelay
│   │
│   ├── Tab 6  History
│   │     line 1  Keep history for ............... dropdown  settings.retentionDays      (tooltip L01)
│   │             Keep Timeline history for ...... dropdown  settings.rollupRetentionDays (L13)
│   │     line 2  storage readout Label | [Purge history…]
│   │
│   └── Tab 7  Keybindings          (new, planned item 015, L18)
│         line 1  Toggle Loot History window ..... keybinding (synced with Settings ▸ Keybindings ▸ Ka0s Loot History)
│
└── Profiles  [unchanged]
```

Counts after: 3 pages, 7 primary tabs (6 + Keybindings) plus 3 sub-tabs, 23 schema rows
(unchanged) plus the planned binding row. Rows per schema tab: Master controls 8, Capture 6,
AH Pricing 2, Interface 5, History 2. Every tab still holds ≥ 2, so test_schema.lua:716 holds.

Tasks that now take one tab instead of two or more: tune the History window (Interface only);
decide what gets recorded (Capture, then the adjacent Filters); set data lifetime (History only).

## Cross-addon notes / Upstream suggestions

**Cross-addon notes**

- **BankLedger shares five tab names and their order** (Panel.lua:963-968). L08 (Filters after
  Capture) must land in both, or not at all (L21 is rejected). The BankLedger schema has the same
  `Interface > Simulator > Simulation step delay` placement, so LOO-P15 stays a deliberate lonely
  section, kept for consistency.
- **Minimum quality**: BankLedger says "Minimum quality". L14 converges on it.
- **Record vs Track**: LootHistory says "Record currency / Record gold" and BankLedger says
  "Track items / Track gold" for the same kind of capture toggle. The collection should pick one
  verb, for example "Record" for writing history rows and "Track" for holdings.
- **Retention**: both addons use "Keep history for" with a `RETENTION_OPTIONS` list. Checked:
  BankLedger's tooltip already says 'Always' (BankLedger Schema.lua:144) and its Constants comment
  says "Always" (Constants.lua:181), so LOO-P01/L01 is LootHistory's alone and converges on BankLedger.
- **Filters sub-tabs**: BankLedger's Filters strip is **Blacklist | Whitelist** (Panel.lua:414, :418).
  The rewritten L17 keeps both names identical and renames only LootHistory's third, currency-only
  list.
- **Clear all**: BankLedger's id-list button is also a bare "Clear all" behind a confirm
  (BankLedger Panel.lua:252), so L15 must land in both.
- **AH Price (column) vs AH Pricing (tab)**: if L09 is taken, the Holdings window column keeps
  "AH Price" (HoldingsTab.lua:36). That is correct (a column holds a value), not drift.
- **Keybindings tab position**: L18 proposes **last tab, named "Keybindings"** for all 7 windowed
  addons (BankLedger, DpsRace, DropWatcher, LootHistory, MultiMeters, QuickComms, WhatGroup).
  Today LootHistory's `Bindings.xml` uses `category="ADDONS"` with `header="LOOTHISTORY"`
  (BINDING_HEADER_LOOTHISTORY = NS.BRAND "Ka0s Loot History"). The item-015 per-addon category
  should be named after the same string as the settings category, "Ka0s Loot History".
- **addonName vs brand**: the Master controls row reads "Enable **Loot History**" while the
  category, the window title and the binding header say "**Ka0s** Loot History". Every addon should
  decide whether `addonName` carries the "Ka0s" prefix, and do it the same way.
- **Ellipsis convention** (L15): every confirm-gated button in every addon should end in "…".
- **Window subsection naming** (L03): an addon with one primary window should name its window
  subsection after the window ("History window", "Ledger window") rather than "Window". BankLedger
  today has **Windows** (plural, two windows: Session window and the ledger) and **Table rows**, so
  the collection rule is "name the window(s) the rows shape", not one fixed word.

**Upstream suggestions (WowAddonStandards / LibKa0s)**

1. **options-ui-§7, an after-subgroup seam.** `afterGroup` is the only host seam, so a host-drawn
   block (here the source picker) can only sit at the end of a tab. That forces the subsection
   order to follow the widget rather than the mental model (L04). Suggest `afterSubgroup[<name>]`
   in the flow engine.
2. **options-ui-§15, composer tooltips that can be extended.** The composed "Lock frame: Stop the
   frame being dragged" undersells LootHistory, where it also stops resizing and covers the export
   modal. Suggest a `tooltipSuffix` per canonical row, keeping the label fixed.
3. **options-ui-§12/§13, Defaults button vs Reset all settings.** On a single-subcategory addon
   like this, the page's Defaults button and Master controls' Reset all settings are the same act
   twice on one page (LOO-P24). The standard could let a page whose Defaults blast radius equals
   §12's global reset omit the Defaults button.
4. **options-ui-§13, a canonical position for the new Keybindings tab** (L18), written into the
   standard with item 015 so the 7 addons cannot diverge.
5. **options-ui-§7, a lint for near-repeat headings.** test_panel.lua:361 pins only exact equality
   (subgroup ≠ group). A heading that is a stem of its tab ("Pricing" under "AH Price") passes. A
   standard note ("a subgroup MUST NOT restate its tab, including by stem") would close it.
6. **Simulator placement.** Several addons now carry a one-row `Interface > Simulator` subsection.
   The standard could name its home once (Interface > Simulator, or a Master controls `extra`
   beside Test mode under §15's extension rule) so it is placed identically everywhere.
7. **A one-control Keybindings tab must be legal** (LOO-P29). LootHistory (and any addon with only
   the window-toggle binding) will draw a Keybindings tab holding one control, which the
   collection's "no tab holds fewer than two controls" practice forbids. Item 015's standard text
   should exempt the Keybindings tab by name, so an audit does not file it and an addon does not pad
   it.
8. **options-ui-§13, strip width.** With Keybindings added, LootHistory reaches seven primary tabs
   (LOO-P30). The standard could state a tab budget (for example six at default scale) or confirm
   that a wrapped strip on a Keybindings-bearing page is expected.

## Review

Independent review, 2026-10-24, against `../LootHistory` on `master` at 82e1921 (read-only).

- **Current map verified** against Schema.lua (row order, groups, subgroups, labels, tooltips),
  Panel.lua (AFTER_GROUP :939-947, GENERAL_TABS :972-979, FILTER_TABS :411-428, price headers
  :826-827, Defaults :1075, registration :1095/:1107) and Constants.lua:182-192. It was accurate.
  Corrected the button count (Reset position and Reset all settings are composer-emitted, not
  bespoke) and added a list of the test and doc pins every change must move with.
- **No proposed change alters a setting.** Every change is a tooltip, label, heading, comment,
  tab order or tab name; none touches a key, default, range, `onChange` or stored path. L02 moves a
  row between groups, which is layout only (a `group` is never a stored path, options-ui-§15).
- **Problems added**: P28 (two more names for Minimum quality in tooltip and list prose), P29 (the
  planned Keybindings tab holds one control in this addon), P30 (seven tabs may wrap the strip),
  P31 (Filters' last position is a recorded deliberate decision, which L08 reverses).
- **Changes rewritten**: L07 widened to cover P28; L08 now discloses the reversal and the two
  comments to rewrite (65% → 55%); L09 now lists its nine-test-file ripple and
  keeps the Holdings "AH Price" column (55% → 45%); L14 notes the six test pins and what the
  parenthesis still tells the player (55% → 50%); L03 notes BankLedger's plural and the extra
  "History" it introduces (60% → 50%); L17 rewritten to rename only **Currencies** →
  **Currency blacklist**, keeping parity with BankLedger (45% → 55%); L18 now flags the one-control
  tab.
- **Rejected**: L21 (35%) moved to a new "Considered and rejected" table, with three more options
  I weighed and dropped (binding on Interface, merging History into Capture, unrolling Filters'
  sub-tabs).
- **Cross-addon** checks done in BankLedger: its retention tooltip is already correct; its
  Filters sub-tabs and Clear all button are listed so L15/L17 stay aligned; its window subsection
  is "Windows". **Upstream** suggestions 7 (one-control Keybindings tab) and 8 (strip width) added.
