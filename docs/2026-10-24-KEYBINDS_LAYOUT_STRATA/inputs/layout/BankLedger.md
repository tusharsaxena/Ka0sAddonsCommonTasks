# BankLedger — settings layout analysis

Read from `../BankLedger` on `master` (clean), 2026-10-24: all of `settings/` (`Schema.lua`, `OptionsSetup.lua`,
`Panel.lua`, `Profiles.lua`, `Slash.lua`), `core/Constants.lua` (value lists), `core/LauncherSetup.lua` +
`Bindings.xml` (the one binding), `modules/LedgerTable.lua` (the row menu's chat route into the panel),
`docs/settings-panel.md`, `README.md`, and the vendored composer `libs/LibKa0s/OptionsCompose.lua:458`
(`O.MasterControls`) and flow engine `libs/LibKa0s/OptionsWidgets.lua:1385` (`RenderRows`). Standard:
`options-ui.md` §3, §5, §6, §7, §13, §15; `launcher.md` §6.

## Current map

Pages: **3** (landing, General, Profiles), of which **2** hold settings. Primary tabs: **5** (all on General).
Secondary tabs: **2** (inside Filters). Schema rows: **17** (16 drawn by the flow engine + 1 `skipRender` drawn
by the host). Bespoke non-row controls: **7** (2 reset buttons, storage read-out, Purge, and per filter
sub-tab: blurb, Clear all, IdList).

Two-column grid; `|` separates the two cells of one line, `—` is an empty cell.

```
Ka0s Bank Ledger (landing)            OptionsSetup.lua:81 buildMain -> Panel.lua:521 buildMainContent (registered Panel.lua:709)
  logo 300x300 · tagline · "Slash Commands" heading · one label per COMMANDS row     (no settings)

General                                Panel.lua:720 RegisterOptionsPage("general"), renderer Panel.lua:745 RenderTabbedSchema
  [header Defaults button]             Panel.lua:724 (= the global reset, confirm-gated, Panel.lua:682)
  Tab 1  Master controls               composed: Schema.lua:412 S:ComposeMaster, called OptionsSetup.lua:277; spec Schema.lua:269
    line 1  Enable Bank Ledger (CheckBox, settings.enabled)  |  General visibility (Dropdown, settings.visibility)
    line 2  Master scale (Slider, settings.windowScale)       |  Master alpha (Slider, settings.alpha)
    line 3  Lock frame (CheckBox, settings.locked)            |  Debug console (CheckBox, state.debugConsole, session)
    line 4  Minimap button (CheckBox, minimap.shown, global)  |  Test mode (CheckBox, state.testMode, session)
    tail    [Reset position] | [Reset all settings…]          Panel.lua:204 -> S.masterTail (OptionsCompose.lua:567-572)
  Tab 2  Capture                       Schema.lua:38-75
    line 1  Track items (CheckBox, settings.trackItems)       |  Track gold (CheckBox, settings.trackMoney)
    line 2  Minimum quality (Dropdown, settings.qualityThreshold) | —
    tail    InlineGroup "Record movements to and from" (MultiCheck grid, settings.excludedStores, inverted):
              Character Bank · Warband Bank · Guild Bank      Panel.lua:184 renderStoreGrid -> :72 makeMultiCheck (hook Panel.lua:207)
  Tab 3  Interface                     Schema.lua:82-127
    subgroup "Windows"
      line 1  Session window (CheckBox, settings.showSessionWindow) | —
    subgroup "Table rows"
      line 2  Row stripe opacity (Slider, settings.rowStripeAlpha) | Row hover opacity (Slider, settings.rowHoverAlpha)
    subgroup "Simulator"
      line 3  Simulation step delay (Slider, settings.sim.stepDelay) | —
  Tab 4  History                       Schema.lua:142
    line 1  Keep history for (Dropdown, settings.retentionDays, ACCOUNT-WIDE) | —
    tail    storage read-out (TextRow: "N movements recorded over D days. / Database size: ≈ X  (estimated)")
            [Purge ledger…] | —                               Panel.lua:121 renderStorage (hook Panel.lua:208)
  Tab 5  Filters                       Schema.lua:454 (renderer-only row), Panel.lua:431 buildFiltersTab (hook Panel.lua:507)
    secondary strip: Blacklist | Whitelist                     Panel.lua:413 FILTER_TABS
    selected list:   blurb (Label) · [Clear all] · IdList ("Add an item by id, link or name" + entries, 2 columns)
                                                               Panel.lua:361 makeFilterSection (Clear all :370, IdList :389)

Profiles                               Profiles.lua:30 PP.Build, registered Panel.lua:756 (AceDBOptions; no Defaults button,
                                       Profiles.lua:41; one Fill SimpleGroup anchored to the body at 8px insets, Profiles.lua:50-64)
```

Key binding (not in the panel today): one, `CLICK BankLedgerToggleWindow:LeftButton`, `Bindings.xml:2`,
header `BINDING_HEADER_BANKLEDGER = "Ka0s Bank Ledger"` and name "Toggle the ledger window"
(`core/LauncherSetup.lua:154-155`, pinned by `tests/test_launcher.lua:856-857`), listed under Key Bindings >
AddOns (`category="ADDONS"`, which launcher-§6 currently mandates).

Strings outside the panel that name a panel location (any move must keep them true):
`modules/LedgerTable.lua:854` MANAGE_ROUTE ("manage it in Settings ▸ General ▸ Filters ▸ Blacklist/Whitelist"),
`README.md:92` (step delay "on the Interface tab"), `:131` (General ▸ History ▸ Keep history for), `:138`
("Record movements to and from" on the Capture tab), `:139` (General ▸ Filters ▸ Blacklist),
`docs/settings-panel.md:20, :256` (tab/subgroup table).

## Problems

| id | file:line | problem |
|---|---|---|
| BAN-P01 | Schema.lua:83, :123 | **Interface is three subjects on a 3-line tab, two of them lonely.** "Windows" holds one checkbox and "Simulator" holds one slider; each one-row subsection costs a full Heading (two dividers + spacers) for a single control, so the tab draws 3 headings for 4 controls. |
| BAN-P02 | Schema.lua:120-127 | **Simulation step delay is a developer/test control filed under "Interface",** and neither its subgroup nor its tooltip names `/bl sim`, the slash-only tool it paces (Schema.lua:912-917: "Slash-only … no launcher entry, no key binding"). A player who has never typed `/bl sim` meets a knob for something the panel never introduces. |
| BAN-P03 | Schema.lua:83 | **"Session window" is a noun on a checkbox**, where every other checkbox on the page is a verb phrase ("Track items", "Lock frame", "Enable Bank Ledger"). Read cold it could be a section label. It also does not match the window's own title, "Ka0s Bank Ledger - Current Banking Session" (SessionWindow.lua:34), or the slash help's "banking-session window" (Schema.lua:843). |
| BAN-P04 | Schema.lua:53 | **Minimum quality sits alone on line 2 of Capture with an empty right cell**, and its dependency on the item toggle is invisible: it governs items only (gold has no quality), but nothing says so and it is not paired with "Track items". |
| BAN-P05 | Schema.lua:54-55 vs Panel.lua:419 | **The quality gate and its override are on different tabs.** "Whitelisted items ignore this" (Capture tooltip) and "always recorded, even when they fall below your minimum quality" (Filters > Whitelist blurb) describe one rule split across Capture and Filters: answering "what will be recorded?" needs Capture + Filters/Blacklist + Filters/Whitelist, i.e. three views. |
| BAN-P06 | Schema.lua:39, :46 vs :69 | **Terminology drift inside one tab:** "Track items" / "Track gold" then "Record movements to and from". Ka0s Loot History says "Record gold" for the same concept (`LootHistory/settings/Schema.lua:306`). |
| BAN-P07 | Panel.lua:74-75 | **The store grid is the only boxed block on the page** (an AceGUI InlineGroup with its own title), so Capture mixes unboxed flow rows and one bordered box; it reads as a different kind of control than it is. Its title is a sentence fragment ("Record movements to and from") acting as a heading. |
| BAN-P08 | Panel.lua:155 vs Schema.lua:143 | **"Purge ledger…" on a tab named History, beside "Keep history for"**, while its own confirm says "Delete ALL Ka0s Bank Ledger history?" (Slash.lua:9). Loot History's button is "Purge history…" (`LootHistory/settings/Panel.lua:113`). |
| BAN-P09 | Panel.lua:141-142 | Read-out says "≈ X  (estimated)": the ≈ and "(estimated)" say the same thing twice. The ledger window's footer says "Database ≈ X" (Browser.lua:731), so "Database" is the established word and "≈" alone is the established hedge. |
| BAN-P10 | Schema.lua:143-145 | **"Keep history for" is account-wide while every neighbour is per-profile**, and the only cue is the tooltip's last sentence. A player switching profiles expects it to change and it does not. |
| BAN-P11 | Panel.lua:370 vs :389 | **Filters: the destructive "Clear all" is drawn ABOVE the add box and the list**, so the first control under the blurb empties the list; the everyday control (add box) is second. Every other destructive act on the page (Purge, Reset all) is the last thing on its tab. |
| BAN-P12 | Panel.lua:414-420 | **Filters blurbs are asymmetric and long.** "Adding an id to one list removes it from the other" is only on Whitelist though it is equally true from Blacklist (`F:_move`, Filters.lua:83-91, moves either way); the Blacklist blurb is a 3-clause sentence with a parenthetical and an em dash. |
| BAN-P13 | Schema.lua:100-112 | "Row stripe opacity" / "Row hover opacity" vs the fixed "Master alpha" two tabs away: "opacity" and "alpha" for one property on one page (the canonical label is fixed by options-ui-§15, so only the BL side can move, and it is already the better word). No BL change; upstream only. |
| BAN-P14 | Panel.lua:729-731, Schema.lua:422 | Two controls on one page for one act: header **Defaults** and Master controls **Reset all settings** both raise `KA0S_BANKLEDGER_RESETALL`. Fixed by options-ui-§5/§12/§15 — not changeable here (see Upstream suggestions). |
| BAN-P15 | Schema.lua:393-394 | **Test mode covers only the ledger window.** The session window's preview (`/bl session`, `SW:TogglePreview`) is chat-only, so placing the session window needs a slash command the panel never mentions. Behavioural, out of 020's scope — the tooltip can at least name `/bl session`. |
| BAN-P16 | (new tab) | **Planned Keybindings tab has no agreed slot.** With 6 tabs the strip is longer (options-ui-§13 SHOULD fit one row; a wrap is permitted); it must land in the same position in all 7 windowed addons. BL has one binding today; its name "Toggle the ledger window" carries an article no other Ka0s binding name uses, and launcher-§6 currently requires `category="ADDONS"`, which the owner's per-addon category answer overrides — a standard change, not a BL-only one. |
| BAN-P17 | Schema.lua:84-85 | Session window tooltip "Show a small live window listing what you move while a bank is open" does not say it appears automatically at a bank; "Turning this off never stops capture — only the window" is the useful half and comes last. |
| BAN-P18 | Profiles.lua:41-64 | Profiles page gives no hint that retention, the minimap button and the ledger itself are NOT in a profile (docs/profiles.md says so; the page does not). Only reachable by reading the Defaults tooltip on another page. |
| BAN-P19 | Schema.lua:71-72 | Store grid tooltip "Tick a store to RECORD movements…" shouts with caps; the grid is the only control whose stored sense is inverted, which the label already handles — the caps are unnecessary. |
| BAN-P20 | OptionsCompose.lua:490 (via Schema.lua:349) | **"Lock frame" tooltip is the composer's generic "Stop the frame being dragged."** BankLedger has three movable windows (ledger, session, export — all through `NS.Util.ApplyMasterFrame`, Export.lua:381), so "the frame" names none of them. The host already overrides the composer's Test mode tooltip through `S.MASTER_DECOR` (Schema.lua:393), so the same seam is open here. The tail's "Reset position" tooltip ("Move the frame back to where it started.") has the same defect but is composer-owned with no host override (upstream). |
| BAN-P21 | LedgerTable.lua:854, README.md:92,138,139 | **Panel routes are spelled in code and docs.** The row menu prints "manage it in Settings ▸ General ▸ Filters ▸ Blacklist."; the README names tabs and the store-grid label. Any tab move or relabel below must update these in the same commit or the chat line sends the player to a tab that no longer exists. |

## Proposed changes

No setting key, default, range, value list or behaviour changes. "Line" = one two-column line. Every change
that renames a tab, label or location updates the strings listed in BAN-P21 in the same commit.

| id | change | reason | confidence | fixes |
|---|---|---|---|---|
| BAN-L01 | Merge Interface's "Windows" subgroup and "Table rows" subgroup into one subgroup **"Windows"**: line 1 *Show session window* (settings.showSessionWindow) \| —; line 2 *Row stripe opacity* \| *Row hover opacity*. (Set `subgroup = "Windows"` on the two tint rows, Schema.lua:102,109; mark the session row `solo` so the tints still pair — `solo` is a layout field, options-ui-§6.) | Both answer "how do my windows look and behave"; drops one heading and one lonely section. Risk: options-ui-§7 wants a heading per *kind* of control and the code comment (Schema.lua:78-80) deliberately split "windows you can switch on" from "row tints"; a reviewer can read the merge as two kinds under one heading. Loot History's equivalent subgroup is "Window" (singular, `LootHistory/settings/Schema.lua:377`) and already mixes scale with row height. | 60% | P01 |
| BAN-L02b | Keep *Simulation step delay* on Interface as the last line; rename its subgroup to **"Simulator (/bl sim)"** and reword the tooltip to start "Paces /bl sim: how many seconds the simulator waits between steps as it plays. …" (rest unchanged). | Introduces the tool the knob belongs to, inside the standard's comfort zone. Must be decided together with Loot History, whose Interface tab has the same "Simulator" subgroup (`LootHistory/settings/Schema.lua:416`). | 65% | P02 |
| BAN-L03 | Relabel *Session window* → **"Show session window"**; tooltip reordered: "Opens the Current Banking Session window at a bank, listing what you move. Turning this off never stops capture, only the window." | Verb-phrase checkbox like every other; tooltip leads with when it appears and names the window by its title. | 85% | P03, P17 |
| BAN-L04 | Relabel *Track items* → **"Record items"**, *Track gold* → **"Record gold"**. | One verb on Capture ("Record movements to and from" is already there); matches Loot History's "Record gold". | 70% | P06 |
| BAN-L05 | Relabel *Minimum quality* → **"Minimum item quality"**; tooltip: "Only record items at or above this quality. Gold is not affected. Items on the Whitelist (Filters tab) are always recorded." | Says it governs items only and names where its override lives, so the cross-tab rule is discoverable from either side. | 80% | P04, P05 |
| BAN-L06 | Reorder Capture: line 1 *Record items* \| *Minimum item quality*; line 2 *Record gold* \| —. (Schema order trackItems, qualityThreshold, trackMoney; the composer-free rows only.) Side effect: `/bl list` prints the rows in the new order (presentation, not a setting). | Puts the quality gate beside the toggle it depends on; gold's own line says gold has no further options. Moves the empty cell rather than removing it. | 55% | P04 |
| BAN-L07 | Store grid: drop the InlineGroup box and draw the three checkboxes as a plain Flow `SimpleGroup` under a schema-declared subsection heading: give the `settings.excludedStores` row `subgroup = "Banks to record"` (Schema.lua:67-69). The flow engine's `startSubgroup` runs for `skipRender` rows too (OptionsWidgets.lua:1386-1389), and the row is the tab's last, so the heading lands directly above the `afterGroup` grid — no builder-drawn heading (options-ui-§7: "a subsection is still never drawn by a builder"). Host change: `makeMultiCheck` (Panel.lua:74-75) uses `SimpleGroup` with no title. Tooltip "RECORD" → "record". The row's `label` stays "Record movements to and from" (CLI/tests see it). | One visual language per tab; the subgroup heading is the standard's own device for a tab that mixes kinds of control (options-ui-§7); "Banks" is the word the three options themselves use. README.md:138 updates to the new heading. | 50% | P07, P19 |
| BAN-L09 | Relabel *Purge ledger…* → **"Purge history…"**; read-out second line "Database size: ≈ X  (estimated)" → **"Database size: ≈ X"**. Button tooltip: "Delete every recorded movement on this account. Your settings are left alone. Asks first." | One noun on the tab and in its own confirm ("Delete ALL … history?", Slash.lua:9); matches Loot History's button; drops the double hedge while keeping the ledger window footer's word "Database" (Browser.lua:731). | 75% | P08, P09 |
| BAN-L10 | Relabel *Keep history for* → **"Keep history for (all profiles)"**. | Makes the one account-wide stored row visibly different from its per-profile neighbours, at no layout cost. Should be the same suffix in every addon with a `db.global` row (Cross-addon notes). | 55% | P10 |
| BAN-L11 | Filters: draw **Clear all after the IdList** (swap the `makeClearAll` and `O.IdList` calls, Panel.lua:370/389), on its own line. | Destructive act last, as Purge and Reset all are; the add box becomes the first control under the blurb. Cost: on a long list the button is a scroll away, which is acceptable for a bulk delete. | 60% | P11 |
| BAN-L12 | Filters blurbs: Blacklist → "Never recorded from now on. Rows already in your ledger stay; delete them from the ledger window if you want them gone." Whitelist → "Always recorded, even below your minimum item quality." Both end with "An item can be on one list only; adding it here takes it off the other." | Symmetric, shorter, names the shared rule on both (true both ways, Filters.lua:83-91). | 80% | P12 |
| BAN-L13 | Test mode tooltip (Schema.lua:393, host decor): append "To place the session window, use /bl session." | Makes the only placement route for the second window discoverable from the panel (wording only). | 60% | P15 |
| BAN-L14 | Add the planned **Keybindings** tab as the **last** tab of General (after Filters). Binding name "Toggle the ledger window" → **"Toggle ledger window"** (locale key at LauncherSetup.lua:155 and the pin at tests/test_launcher.lua:857 move with it); category becomes "Ka0s Bank Ledger" per the owner's answer, which requires launcher-§6's `category="ADDONS"` and its "Key Bindings → AddOns" README wording to change upstream first. | Same slot in all 7 windowed addons (last is the only slot every addon can honour without displacing a shared tab); bindings are touched rarely, so they belong at the end of the strip. | 80% | P16 |
| BAN-L15 | Profiles page: a one-line Label above the AceDBOptions group: "A profile holds your settings, both filter lists and saved views. Your recorded history, how long it is kept and the minimap button are shared by every profile." Implementation: the renderer (Profiles.lua:50-64) anchors its Fill container at the body's top-left; the label needs its own frame there and the container re-anchored below it. | States the profile boundary where profiles are managed. Text only. Only worth it if every addon with account-wide rows does the same, or the Profiles pages drift. | 50% | P18 |
| BAN-L16 | Lock frame tooltip override in `S.MASTER_DECOR["settings.locked"]` (Schema.lua:349): "Stop the ledger, session and export windows being dragged." (label untouched — options-ui-§15 forbids renaming; tooltips are host decor, as Test mode's already is). | Names the three windows the one switch governs instead of a generic "the frame". | 55% | P20 |

Totals: 15 changes. Recommended set if the owner wants only ≥ 65%: L02b, L03, L04, L05, L09, L12, L14.

## Proposed map

With all ≥ 50% changes applied:

```
Ka0s Bank Ledger (landing)                       unchanged

General
  [header Defaults button]                       unchanged
  Tab 1  Master controls                          canonical, options-ui-§15 (labels and order unchanged)
    Enable Bank Ledger | General visibility
    Master scale | Master alpha
    Lock frame (tooltip names the three windows) | Debug console                                   L16
    Minimap button | Test mode (tooltip names /bl session)                                         L13
    [Reset position] | [Reset all settings…]
  Tab 2  Capture
    line 1  Record items (settings.trackItems) | Minimum item quality (settings.qualityThreshold)   L04 L05 L06
    line 2  Record gold (settings.trackMoney) | —                                                 L04 L06
    subgroup "Banks to record"                                                                     L07
      Character Bank · Warband Bank · Guild Bank (settings.excludedStores, inverted, unboxed)
  Tab 3  Interface
    subgroup "Windows"                                                                             L01
      line 1  Show session window (settings.showSessionWindow) | —   (solo)                        L03
      line 2  Row stripe opacity (settings.rowStripeAlpha) | Row hover opacity (settings.rowHoverAlpha)
    subgroup "Simulator (/bl sim)"                                                                 L02b
      line 3  Simulation step delay (settings.sim.stepDelay) | —
  Tab 4  History
    line 1  Keep history for (all profiles) (settings.retentionDays) | —                           L10
    tail    "N movements recorded over D days." / "Database size: ≈ X"                             L09
            [Purge history…] | —                                                                    L09
  Tab 5  Filters
    secondary strip: Blacklist | Whitelist
    selected list: blurb (shared last sentence) · IdList · [Clear all]                             L11 L12
  Tab 6  Keybindings                                                                               L14 (015)
    Toggle ledger window  [key 1] [key 2]   (synced with Settings > Keybindings > Ka0s Bank Ledger)

Profiles
  one-line profile-boundary label · AceDBOptions                                                   L15
```

Counts after: 3 pages, 6 tabs (5 + Keybindings), 2 secondary tabs, 17 schema rows (unchanged), 3 subgroup
headings across Capture/Interface (was 3: Windows, Table rows, Simulator → Banks to record, Windows,
Simulator (/bl sim)). No tab is removed, so page/tab switching is unchanged in count; what drops is the
cross-tab hunting (L05, L12 point at each other's tab) and a boxed control.

## Considered and rejected

| id | change | why rejected | confidence |
|---|---|---|---|
| BAN-L02 | Move *Simulation step delay* to **Master controls** through the composer's `extra` slot (`startsLine`, after *Minimap button \| Test mode*). | Allowed by options-ui-§15's extras rule (it is addon-wide and stored), but it puts the pacing knob of a slash-only developer tool (Schema.lua:912-917) on the tab every player opens first, one line above the resets; Quick Comms' "Preview as", the precedent, is a player-facing preview. It would also split BL from Loot History unless both move, and README.md:92 names the Interface tab. L02b fixes the discoverability problem without that cost. | 35% |
| BAN-L08 | Merge **Filters into Capture** (the Blacklist \| Whitelist strip becomes Capture's tail; Filters tab removed). | options-ui-§13 permits a secondary strip where "one tab's content is itself a list of like subjects"; Capture would be rows + grid + a strip, which is outside that permission. It breaks the shared tab vocabulary with Loot History (Schema.lua:28-32), pushes the store grid under a potentially long IdList, and requires rewording MANAGE_ROUTE (LedgerTable.lua:854) and README.md:139. L05 + L12 deliver the cross-reference without a merge. | 30% |
| — | Pair *Purge history…* into the right cell beside *Keep history for*. | Purge is a confirm-gated act drawn by `O.InlineButtonPair`; a button in a schema pair cell needs the `pairWith` hook and would put the destructive act on the first line of the tab. | 25% |
| — | Rename the *History* tab to "Retention". | "History" is the shared tab name with Loot History and the ledger window's own tab name (Browser.lua:203); "Retention" would be the odd one out. | 20% |

## Cross-addon notes / Upstream suggestions

Cross-addon notes:

- **Capture vocabulary.** BL "Track items/Track gold" vs LH "Record gold". Converge on "Record …" (L04) in
  both; LH's "Minimum quality (detailed records)" and BL's proposed "Minimum item quality" should follow one
  label pattern.
- **Purge wording.** BL "Purge ledger…" vs LH "Purge history…" on tabs both named History (L09).
- **Simulator subgroup.** BL and LH both put "Simulation step delay" on Interface under "Simulator" (the only
  two addons with that row). L02b's "Simulator (/bl sim)" must be mirrored as "Simulator (/lh sim)" in LH, or
  neither changes.
- **Window subgroup name.** BL "Windows" (plural, two windows) vs LH "Window" (singular, one). Correct as is
  if the noun counts the addon's windows; record that as the rule so a third addon does not guess.
- **Filters tab.** BL and LH share the "Filters with a secondary strip" shape on purpose (Schema.lua:28-32);
  keep it (L08 rejected).
- **Keybindings tab position.** Recommend "last tab of General" in all 7 windowed addons. Binding names today:
  BL "Toggle the ledger window", LH "Toggle Loot History window", DW "Toggle Drop Watcher window", MM "Toggle
  meter windows", DpsRace "Toggle results window" / "Toggle race HUD", WG "Toggle group popup", QC "Toggle
  Comms Pads". Under a per-addon category the addon name in LH/DW labels is redundant; one pattern
  ("Toggle <window noun>", no article, no addon name) should be applied to all of them together.
- **"opacity" vs "alpha".** Every addon's own rows should say "opacity" (the canonical BarGroup already says
  "Bar opacity"); only Master controls says "alpha".
- **Account-wide rows.** Any addon with a row stored in `db.global` (BL retention, LH retention, every addon's
  minimap row) should mark it the same way; pick one suffix ("(all profiles)") collection-wide. The minimap
  row's canonical label cannot take it (options-ui-§15), so the suffix applies to host rows only.
- **Lock frame tooltip.** Every addon with more than one movable window has the same generic composer tooltip;
  each should override it in its decor table the same way (L16), or the composer should take a host string.

Upstream suggestions (WowAddonStandards / LibKa0s):

1. **options-ui-§15: "Master alpha" → "Master opacity".** The composer's own BarGroup says "Bar opacity"; the
   canonical row is the odd one out. A label change on a composed row moves no stored path.
2. **options-ui-§5/§12: the General page's header Defaults and "Reset all settings" are the same act on one page**
   (P14). Consider letting a page whose first tab is Master controls drop the header Defaults button (or make
   it a link that jumps to the Master controls tab), so one act has one control.
3. **options-ui-§15 extras:** state explicitly whether a test/sim pacing control (BL/LH "Simulation step delay")
   qualifies as an addon-wide extra; this review read it as allowed but unwise (L02 rejected).
4. **Test mode scope (preview-mode / options-ui-§15):** say whether an addon with two positionable windows needs
   test mode to cover both (BL's session window is placed only via `/bl session`, P15).
5. **launcher-§6:** the owner's per-addon Key Bindings category contradicts the rule's `category="ADDONS"`,
   its "Key Bindings → AddOns" README wording and its `Toggle <window>` label example; the rule must change
   before any addon's `Bindings.xml` does (L14).
6. **OptionsCompose `MasterControls`:** accept host tooltips for the tail's *Reset position* (and a documented
   decor route for *Lock frame*), so a multi-window addon can say which windows it means (P20).

## Review

Independent review, 2026-10-24, against the code on `master`.

- **Current map corrected.** Profiles line refs were wrong (`Profiles.lua:310/:323/:331` do not exist; the file is
  68 lines): now `:30` PP.Build, `:41` CreatePanel, `:50-64` renderer. Added the composer tail ref
  (OptionsCompose.lua:567-572), the makeMultiCheck/Clear all/IdList refs, the binding's test pin, and a list of
  strings outside the panel that name panel locations (new P21). The rest of the map checked out row by row.
- **New problems:** P20 (generic "Lock frame" tooltip on a three-window addon; Reset position likewise),
  P21 (route strings in LedgerTable.lua:854 and README). P03 extended with the window's actual title; P09 with
  the window footer's "Database ≈" wording; P16 with the launcher-§6 conflict; P02 reworded (the "player's
  mental model" claim was unverifiable).
- **Changes rewritten:** L07 used a builder-drawn heading (`O.Section` from the host), which options-ui-§7
  forbids; rewritten to a schema `subgroup` on the skipRender row, which the flow engine already honours.
  L09's "Estimated size: ≈ X" still said the estimate twice; now "Database size: ≈ X", matching the window
  footer. L14 now names the launcher-§6 dependency and the test that pins the label. L15 now states the
  anchoring work it needs. L03 tooltip names the window by its title.
- **New change:** L16 (Lock frame tooltip via the existing host decor seam).
- **Recalibrated:** L01 75→60 (§7 kinds-of-control risk), L02b 70→65, L11 65→60, L15 55→50.
  **Rejected:** L02 45→35 (dev knob on the first tab; L02b covers it), L08 40→30 (outside the §13 secondary-strip
  permission; breaks shared vocabulary and route strings); two further ideas listed with reasons.
- **Setting-change check:** no change touches a key, default, range, value list or behaviour. L06 changes
  `/bl list` order (presentation only); L14's label rename moves a locale key and a test pin but not the
  binding name, which launcher-§6 makes permanent.
- Recommended ≥ 65% set updated (L01 and L11 dropped from it).
