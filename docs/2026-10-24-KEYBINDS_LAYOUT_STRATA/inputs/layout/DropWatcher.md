# DropWatcher — settings layout analysis

Item 020. Read-only analysis of `../DropWatcher` on `master` (2026-10-24). Sources: `settings/*.lua`,
`settings/SchemaRows.lua` (every hand-written row), `settings/Panel.lua` (Master controls),
`settings/ComposedRows.lua` (Icons › Border), `settings/PageEditors.lua` (host tabs, hooks),
`docs/settings-panel.md`, and options-ui-§5/§6/§7/§13/§15/§16/§17.

No proposal changes a setting key, default, range or behaviour. Moving a row between pages does move
what that page's **Defaults** button resets and which `/dw list` section prints it (options-ui-§13: the
Defaults blast radius is the page). feedback-24 made the same kind of move without a migration, because
a page key is not a stored path. Every such consequence is called out next to its change.

## Current map

Order on screen. "A | B" means two rows that share one flow line. `(solo)` is a row alone on its line.
`[sub: X]` is a `subgroup` heading inside a tab. Widget types: cb = checkbox, dd = dropdown, sl =
slider, sw = color swatch, eb = edit box, btn = button.

Registration order: General `settings/Panel.lua:87`, then the six pages in `PAGES`
(`settings/Pages.lua:27-53`, registered at `:75`), then Profiles `settings/Profiles.lua:46`.
Inside a page, the tab order is the order of each tab's first row in `settings/SchemaRows.lua:571-579`.

```
Ka0s Drop Watcher (landing)                  Panel.lua:25 BuildMainContent (untabbed, options-ui-§13 exempt)
  logo · TOC notes · "Slash Commands" + one line per NS.COMMANDS

General                                      Panel.lua:76 buildGeneralPage; Defaults = global reset (asks)
  Tab "Master controls"                      Panel.lua:44 MasterControls (composed, options-ui-§15)
    Enable Ka0s Drop Watcher (cb, enabled)   | General visibility (dd, visibility)
    Master scale (sl, scale)                 | Master alpha (sl, alpha)
    Lock frame (cb, locked)                  | Debug console (cb, state.debugConsole, session)
    Minimap button (cb, global.minimap.shown)| Test mode (cb, state.testMode, session)
    [Reset position (btn)                    | Reset all settings (btn, asks)]   composer tail, Panel.lua:68
  Tab "Simulator"                            SchemaRows.lua:563
    Simulation step delay (sl 0.5-10, sim.stepDelay)   (alone)

Situations                                   Pages.lua:28 (afterGroup table, beforeClear park)
  Tab "Situations"                           SchemaRows.lua:219
    Auto-open the window (cb, autoOpen)      (alone: the next rows are skipRender)
    <table> PageEditors.lua:258 SituationTable, one line per K.SITUATIONS entry (10):
      Situation | Track (cb, situations.<k>.track) | Auto-open (cb, situations.<k>.autoOpen)
                | Quality (dd, situations.<k>.quality) | Loot rule (dd, trade.rules.<k>)
      lines: Mythic+, Dungeon, Follower dungeon, Raid Finder, Raid, Delve, Scenario, PvP,
             Open world group, Solo

Drops  (page key "feed")                     Pages.lua:35 (afterGroup Quality readout, pairWith Clear history)
  Tab "Quality"                              SchemaRows.lua:267
    Minimum quality (dd, feed.quality.mode)  | Always show upgrades for me (cb, feed.quality.upgradeOverride)
    Fixed minimum (dd, feed.quality.fixed)   | Quality floor (dd, feed.quality.floor)
    "In force now: Quality: …" (readout)     PageEditors.lua:60
    "A situation can set a quality of its own: the Quality column on the Situations page."  PageEditors.lua:64
  Tab "Items"                                SchemaRows.lua:279
    [sub: Item kinds]
      Gear only (cb, feed.gearOnly)          | Tier tokens (cb, feed.includeTokens)
    [sub: Item level]
      Minimum item level (dd, feed.minIlvlMode) (solo)
      Absolute minimum (sl 0-1000, feed.minIlvl) | Levels under my average (sl 0-100, feed.relativeIlvl)
  Tab "Retention"                            SchemaRows.lua:297
    [sub: History]
      Keep history for (dd, history.retentionDays, account-wide) | Clear history (btn, asks)  PageEditors.lua:88
    [sub: Session]
      Clear on boss kill (cb, feed.clearOnBossKill)

Comparison                                   Pages.lua:39 (two host tabs)
  Tab "Scoring"                              SchemaRows.lua:307
    Score with (dd, comparison.scorer)       | Sidegrade band (sl 0-20, comparison.sidegradeBand)
    Compare against items in my bags (cb, comparison.compareOwned) | Protect heirlooms (cb, comparison.heirloomProtect)
  Tab "Weights"  (host tab, map comparison.weights)       PageEditors.lua:365
    secondary strip: one tab per spec of your class
    note "Used when Score with is My weights, or Automatic without Pawn …"
    6 sliders 0-5 (primary stat, Stamina, 4 secondaries) paired, then Import a Pawn scale (eb)
  Tab "Unwanted types"  (host tab, map comparison.undesired)  PageEditors.lua:393
    secondary strip: one tab per spec
    note "Ticked types are never called an upgrade for this specialization."
    one cb per weapon type of your class (+ Shields where a spec carries one)

Messages                                     Pages.lua:45 (host tab Templates)
  Tab "Sending"                              SchemaRows.lua:328
    Offer transmog asks (cb, messages.transmogAsk) | Ask once (cb, messages.oneAsk)
    Edit before sending (cb, messages.editFirst)   | Announce channel (dd, messages.announceChannel)
  Tab "Auto-ask"                             SchemaRows.lua:340
    Ask automatically (cb, messages.autoAsk.enabled) (solo)
    Delay (seconds) (sl 3-30, messages.autoAsk.delay) | Least gain (item levels) (sl 1-50, messages.autoAsk.minGain)
  Tab "Templates"  (host tab)                PageEditors.lua:519
    [Tokens] chips {player} … {mygain}
    [Your messages] Ask (eb, messages.templates.ask), Ask for transmog (….transmog),
                    Ask for off-spec (….askOffSpec), Offer (….offer), Announce (….announce)
    [Preview] the message being edited
    Reset templates (btn)

Window                                       Pages.lua:48 (chrome: Columns note)
  Tab "Layout"                               SchemaRows.lua:369
    Window layout (dd, window.mode)          | Open in compact view during a run (cb, window.compactInRuns)
    Row height (sl, window.rowHeight)        | Font size (sl 0-max, window.fontSize, 0 = Default)
  Tab "Columns"                              SchemaRows.lua:387
    note "The full layout's Drops table. History shows every column; …"   PageEditors.lua:73
    [sub: Shown columns]
      Ilvl (window.columns.ilvl)  | Slot (….slot)
      Type (….armorType)          | Looter (….looter)
      Me (….me)                   | Them (….them)
      Trade (….trade)             | Trade window (….tradeWindow)
      Actions (….actions)
    [sub: Trade window]
      Mark a trade window ending within (seconds) (sl 0-1800 step 60, trade.warnAt)
  Tab "Starting view"                        SchemaRows.lua:400
    [sub: View]
      Interesting (cb, feed.view.interesting) | Likely tradeable (cb, feed.view.likely)
      Usable by me (cb, feed.view.usable)     | Upgrade for me (cb, feed.view.upgrade)
    [sub: Content and sort]
      Content (dd, feed.content)              | Sort (dd, feed.sort)
  Tab "Icons"                                SchemaRows.lua:555 + ComposedRows.lua:33
    [sub: Zoom]
      Icon zoom (sl 0-0.25, icons.zoom)
    [sub: Border]  (BorderGroup, options-ui-§16)
      Show border (cb, icons.borderShow)
      Border style (dd LSM, icons.borderStyle) | Border thickness (px) (sl 1-16, icons.borderSize)
      Border color (sw, icons.borderColor)     | Use class color (cb, icons.useClassColorBorder)
      Color by item quality (cb, icons.borderQuality)

Alerts                                       Pages.lua:51
  Tab "Toast"                                SchemaRows.lua:414
    Show a toast (cb, toast.enabled) (solo)
    Least gain (item levels) (sl 1-50, toast.minGain) | Duration (seconds) (sl 2-30, toast.duration)
    Show in combat (cb, toast.inCombat)               | Play a sound (cb, toast.sound)
    Scale (sl 50-200 %, toast.scale)
  Tab "Upgrade glow"                         SchemaRows.lua:490
    [sub: Effect]
      Main spec glow (cb, glow.main.enabled)          | Off-spec glow (cb, glow.offSpec.enabled)
      Main spec style (dd, glow.main.type)            | Off-spec style (dd, glow.offSpec.type)
      Main spec color (sw, glow.main.color)           | Off-spec color (sw, glow.offSpec.color)
      Use class color (main spec) (cb)                | Use class color (off-spec) (cb)
    [sub: Offset]        X offset main | off;  Y offset main | off                           (4)
    [sub: Pixel border]  lines, frequency, line length (0 = automatic), thickness, dark border (10)
    [sub: Auto cast sparkles] particles, frequency, scale                                     (6)
    [sub: Button (rotating rays)] frequency                                                   (2)
    [sub: Proc (flipbook)] duration (seconds), start animation                               (4)

Profiles                                     Profiles.lua:10 (AceDBOptions, untabbed, options-ui-§3)
```

**Counts.** 9 pages (landing, 7 tabbed settings pages, Profiles). 18 tabs: General 2, Situations 1,
Drops 3, Comparison 3, Messages 3, Window 4, Alerts 2. 146 schema rows: General 9, Situations 41
(1 drawn by the flow engine and 40 by the table), Drops 11, Comparison 6 (2 of them maps), Messages 12,
Window 27, Alerts 40 (Toast 6, Upgrade glow 34). That is 99 rows the flow engine draws, plus host-drawn
controls: 40 table cells, 6 weight sliders and the import box per spec, N weapon-type checkboxes per
spec, 5 template editors and 3 buttons (Clear history, Reset templates, and the reset pair).

**Planned (item 015).** General gains a **Keybindings** tab for the one binding that exists today,
`CLICK DropWatcherToggleWindow:LeftButton` (`Bindings.xml`, labelled "Toggle Drop Watcher window" in
`core/LauncherSetup.lua:46-47`).

## Problems

| id | file:line | problem |
|---|---|---|
| DRO-P01 | Pages.lua:28, SchemaRows.lua:219 | **The Situations page is a one-tab page whose content belongs to Drops.** Its Track column says whether a situation's loot is listed at all, and its Quality column overrides Drops › Quality's mode. Both answer the question the Drops page exists for ("what the addon lists at all"). Setting up quality for a raid takes Drops › Quality, then the Situations page, then back again. That is a page switch for one task. |
| DRO-P02 | PageEditors.lua:64 | Drops › Quality's closing line sends the player to **another page** ("the Quality column on the Situations page"). This hint exists because of DRO-P01. |
| DRO-P03 | SchemaRows.lua:374 | **"Open in compact view during a run" sits far from what it depends on, and its label says less than it does.** It only applies to an *auto*-open (tooltip: "When the window opens by itself …"), and auto-open is on another page (Situations › Auto-open the window). Read alone, the label suggests every open during a run is compact, which is wrong. |
| DRO-P04 | SchemaRows.lua:329-337 | **Messages › Sending pairs unrelated rows on each line.** It reads *Offer transmog asks* (which asks you get) next to *Ask once* (how a send behaves), then *Edit before sending* next to *Announce channel*. The two per-send behaviours (Ask once, Edit before sending) are split across two lines. |
| DRO-P05 | SchemaRows.lua:329, PageEditors.lua:519 | *Offer transmog asks* turns on the use of the *Ask for transmog* template, which is edited on another tab (Templates). This is a dependent pair split across tabs. Mitigated by the tooltip; one-tab-per-section (options-ui-§13) rules out a merge. |
| DRO-P06 | SchemaRows.lua:490-548 | **Upgrade glow is drawn only on window surfaces** (the Drops table, the compact card, the detail card's header, and never the toast; see the row tooltips at :501/:503 and docs/settings-panel.md › Upgrade glow), yet it lives on Alerts next to the toast. It also draws over the Window › Icons border (Glow.lua:47). Styling an item icon fully means visiting Window › Icons and Alerts › Upgrade glow, on two pages. feedback-24's reason, "neither is part of the window", holds for the toast but not for the glow. |
| DRO-P07 | SchemaRows.lua:490-548 | The Upgrade glow tab is 34 rows. With one style chosen per glow, at most 1 of the 4 style subsections is live for each glow, so about 16 rows sit dimmed. That is a long scroll. Splitting it would add tab switching between "pick a style" and "tune it", so no split is proposed (see Upstream suggestions). |
| DRO-P08 | SchemaRows.lua:563-568 | General › Simulator is a lonely one-row tab. It is acceptable under options-ui-§13 (a one-tab section is legal), and options-ui-§15 forbids folding it into Master controls (it is not addon-wide in the canonical sense). With the planned Keybindings tab, its strip position matters: a dev/test knob would sit before the binding a player actually looks for. |
| DRO-P09 | SchemaRows.lua:566 | "Simulation step delay" is the only timed slider without a unit in its label. Compare "Delay (seconds)" (:347), "Duration (seconds)" (:423) and "Mark a trade window ending within (seconds)" (:393). |
| DRO-P10 | SchemaRows.lua:428 | Toast's "Scale" is a bare word. In the same addon "Master scale" exists, *(Review: `/dw list` prints the path `toast.scale`, not the label, so only the on-tab reading matters.)* |
| DRO-P11 | SchemaRows.lua:282 | "Tier tokens" reads as a noun, not a switch. Its tooltip is "List tier tokens too." and its partner is "Gear only". |
| DRO-P12 | SchemaRows.lua:299 | "Clear on boss kill" does not say what is cleared. Its tooltip says "the session's drops" (the Drops tab's This session list), not the History, which is the subsection just above it. Read under the Retention tab it can be mistaken for clearing history. |
| DRO-P13 | PageEditors.lua:91 | "Clear history" asks for confirmation but carries no ellipsis. BankLedger has "Purge ledger…" and DpsRace "Delete all runs…", and the Master controls "Reset all settings" also asks. Ellipsis use is inconsistent within the addon and across the collection. |
| DRO-P14 | SchemaRows.lua:393 | "Mark a trade window ending within (seconds)" is a sentence fragment that leads with a verb. Every other slider label is a noun phrase. |
| DRO-P15 | SchemaRows.lua:390 (WindowGroup.lua:118-147) | The column checkboxes reuse the table header labels. "Ilvl" is an abbreviation the rest of the panel spells out (Sort's "Item level", Drops' "Minimum item level"). "Me" and "Them" are meaningless out of the table and only the tooltip explains them. |
| DRO-P16 | SchemaRows.lua:400-403 | Starting view › View: "all unticked is All" (the default) appears in no label or tooltip. A player who unticks everything cannot tell what will happen. |
| DRO-P17 | SchemaRows.lua:349, :421 | Two different settings share the label **"Least gain (item levels)"** (Auto-ask's and Toast's). On their own tabs this is fine. *(Review: `/dw list` prints paths, not labels, and there is no search, so this is not ambiguous anywhere today. See L16, rejected.)* |
| DRO-P18 | SchemaRows.lua:300 | Retention › **Session** is a lonely one-row subsection (Clear on boss kill). Kept, because the alternative (no heading) would put it under the History heading, which DRO-P12 shows is the wrong reading. |
| DRO-P19 | SchemaRows.lua:556-558 | Icons › **Zoom** is a lonely one-row subsection. Kept: the Border block is composed and brings its own heading (options-ui-§16), so Zoom needs one to read as separate. Nit only. |
| DRO-P20 | SchemaRows.lua:369-383 | Window › Layout mixes two subjects without headings: the window's *mode* (Window layout, compact during a run) and the *tables' text* (Row height, Font size). options-ui-§7 asks for subsection headings where a tab mixes kinds of control. |
| DRO-P21 | SchemaRows.lua:328-337 | Messages › Sending likewise mixes "which asks you get" with "how a send goes" without a heading (options-ui-§7, as DRO-P20). |
| DRO-P22 | Pages.lua:27-53 | Page order: General, Situations, Drops, Comparison, Messages, Window, Alerts. Alerts (how you are *told* about an upgrade) comes after Messages (what you *do* about it) and after Window (how it looks). The flow a player lives through is listed → judged → alerted → act. Nit. |
| DRO-P23 | Pages.lua:29, :36 | The Defaults tooltips list each page's contents ("auto-open and every situation's …", "quality, items and how long drops are kept"). They go stale with any move and must be rewritten with it. |
| DRO-P24 | SchemaRows.lua:344 vs the tab label at :340 | The tab is "Auto-ask" and its switch is "Ask automatically", while elsewhere the switch carries the feature's own name ("Show a toast", "Main spec glow"). A terminology nit; kept, because "Ask automatically" is the clearer checkbox. |
| DRO-P25 | SchemaRows.lua:285 vs :143 | Item level terminology drifts: the dropdown value is "Relative to my gear" and the slider is "Levels under my average". Quality's mode, "Match my gear", uses the other phrasing. Nit. |
| DRO-P26 | SchemaRows.lua:519-535 (fixed) | Upgrade glow › Effect puts each Use class color *below* its swatch, not beside it. This is a documented options-ui-§17 deviation and the owner's choice (feedback-21 H6). It is constrained, so no change. |
| DRO-P27 | SchemaRows.lua:240, :297 | *(review)* The Drops page's subject drifts both ways. It already holds Retention › History, which is the window's **History** tab's retention, not the Drops tab's. And L01 would add the situations table, half of whose cells (Auto-open, Loot rule) are window and trade behaviour, not "what is listed". The page title "Drops" covers less than the page holds. Constrains L01's confidence; no rename is proposed, because "Drops" is the name feedback-24 chose. |
| DRO-P28 | SchemaRows.lua:390, :395 | *(review)* Window › Columns ends its Shown columns list with the **Trade window** checkbox (the column) and the very next heading is the subsection **Trade window**. Two adjacent "Trade window" labels read like a duplicate row. |
| DRO-P29 | SchemaRows.lua:565 | *(review)* `sim.stepDelay` has no value format. BankLedger (`fmt = "%.1f s"`) and LootHistory (`fmt = "%.1fs"`) show the unit on the slider's value instead of in the label. |
| DRO-P30 | Bindings.xml:2 | *(review, item 015)* The binding is filed under `category="ADDONS"` with header `BINDING_HEADER_DROPWATCHER = NS.BRAND` (`core/LauncherSetup.lua:45`). Item 015 wants a category named after the addon. That is item 015's change, listed here so the Keybindings tab's label ("Toggle Drop Watcher window") and the Blizzard page stay one string. |

## Proposed changes

`/dw list` prints each row's **path**, never its label (`libs/LibKa0s/Slash.lua:520-521`, `kv` →
`FormatKV(row.path, …)`), and the panel has no settings search. So no relabel below is justified by
"ambiguous in `/dw list` or search"; each stands or falls on how it reads on its own tab.

| id | change | reason | confidence | fixes |
|---|---|---|---|---|
| DRO-L01 | **Fold the Situations page into Drops as its first tab.** Move row `autoOpen` and the 40 `skipRender` rows `situations.<k>.{track,autoOpen,quality}` and `trade.rules.<k>` from `page = "situations"` to `page = "feed"`, group unchanged (`Situations`), so they become Drops › Situations ahead of Quality (`situations()` already runs before `feed()` at `SchemaRows.lua:572-573`, so the tab lands first with no reorder). In `Pages.lua`, delete the `situations` entry (:28-34) and move its `afterGroup[Situations]` and `beforeClear` (and so `rerender`, :68) onto the `feed` entry (:35), beside the existing `afterGroup[Quality]`. Drops' strip becomes **Situations · Quality · Items · Retention**. | Track and the per-situation Quality are "what is listed", the Drops page's own subject. Quality mode and its situation overrides become one tab click apart instead of a page switch. The page count drops from 7 to 6. Consequences: Drops' Defaults now also resets the situations table (loot rules and per-situation auto-open included), and `/dw list`'s `situations` section merges into `feed`. **This reverses part of feedback-24** (`6f4cb22`, 2026-10-21), which created the Situations page three days ago, and half the table's cells (Auto-open, Loot rule) are not "what is listed" (P27). Flagged for the owner, like L17. | 50% | P01, P02 |
| DRO-L02 | Reword the Quality readout's pointer (`PageEditors.lua:64`, locale `enUS_Settings.lua:315-316`) from "…the Quality column on the Situations page." to "…the Quality column on the Situations tab." | Follows L01. The hint now points one tab left, not to another page. | 90% (if L01) | P02 |
| DRO-L03 | Rewrite the Drops Defaults tooltip (`Pages.lua:36`) to "Reset the Drops page's settings (situations, quality, items and how long drops are kept) to their defaults." and drop the Situations one (:29, locale :309-310). | Keeps the tooltip true after L01. | 95% (if L01) | P23 |
| DRO-L04 | **General's strip: Master controls · Keybindings · Simulator.** Item 015's Keybindings tab is a host tab with no schema row, so it goes in the General render's `opts.tabs` with `before = L["Simulator"]`. The library places a row-less host tab by `before` (`libs/LibKa0s/OptionsTabs.lua:1203-1206`, `placeTab`). Simulator stays last. | A binding is a player setting and the simulator step delay is a test tool, so the common one should come first. options-ui-§15 fixes only the first tab. | 70% | P08 |
| DRO-L05 | Relabel `sim.stepDelay` "Simulation step delay" → **"Simulation step delay (seconds)"**. | Unit in the label, like every other timed slider in this addon (:347, :423, :393, :482). The collection alternative (a value `fmt`, P29) is in Cross-addon notes. | 55% | P09 |
| DRO-L06 | Relabel `window.compactInRuns` "Open in compact view during a run" → **"Compact view when it auto-opens in a run"**. Keep it on Window › Layout, beside Window layout. | It is a layout choice, so it stays by the layout dropdown, but the label must say it only touches an auto-open (its tooltip, :375: "When the window opens by itself…"). The draft's "Auto-open in compact view during a run" reads as if the checkbox *makes* the window auto-open, which is the master `autoOpen`'s job. Moving it to Drops › Situations next to "Auto-open the window" was considered (35%); it would split the two layout rows instead. | 60% | P03 |
| DRO-L07 | Window › Layout: add subsections **"Mode"** (`window.mode`, `window.compactInRuns`) and **"Tables"** (`window.rowHeight`, `window.fontSize`). The row order is unchanged. | Two subjects on one tab (options-ui-§7). The headings say that Row height and Font size are the drop tables', which today only the tooltips say. Neither heading repeats the tab name (§7). | 50% | P20 |
| DRO-L08 | Messages › Sending: reorder to **Ask once \| Edit before sending**, then **Announce channel \| Offer transmog asks**. | The two per-send switches share a line. Each line then reads as one thought instead of two half-thoughts. Subsection headings were the alternative (P21, 40%), but a 4-row tab with two 2-row headings reads worse than the reorder. | 55% | P04, P21 |
| DRO-L09 | Relabel `toast.scale` "Scale" → **"Toast scale"**. | On its own tab "Scale" is understandable, so this is a naming-pattern nit only: the addon's other size rows name their object ("Master scale", "Icon zoom", "Row height"). The draft's `/dw list` reason does not hold (see the note above the table). | 40% | P10 |
| DRO-L10 | Relabel `feed.includeTokens` "Tier tokens" → **"Include tier tokens"**. | Reads as a switch, like its partner "Gear only". | 55% | P11 |
| DRO-L11 | Relabel `feed.clearOnBossKill` "Clear on boss kill" → **"Clear this session's drops on boss kill"**. Keep it under Retention › Session. | Says it is the session list, not the history above it. | 60% | P12, P18 |
| DRO-L12 | Relabel the button "Clear history" → **"Clear history…"** (`PageEditors.lua:91`, and the tooltip title at :94). | Collection convention for a button that asks first (BankLedger "Purge ledger…", DpsRace "Delete all runs…"). Note the addon's own **Reset all settings** also asks and carries no "…", and its wording is fixed by options-ui-§12/§15, so within DropWatcher this change creates one inconsistency while removing another. See Upstream suggestions. | 45% | P13 |
| DRO-L14 | Give the column checkboxes settings-only labels (a `settingsLabel` beside `label` in `WindowGroup.COLUMNS`, `modules/WindowGroup.lua:114-150`, read at `SchemaRows.lua:390`): **"Item level"** for Ilvl, **"Me (my gear)"** for Me, **"Them (looter's gear)"** for Them. The others keep the header word. The table header text is unchanged. | Out of the table, "Ilvl", "Me" and "Them" need the tooltip to be understood. A display string only; `window.columns.<key>` is untouched. | 40% | P15 |
| DRO-L15 | Append to each of the four `feed.view.*` tooltips (`SchemaRows.lua:131-138`): "With none ticked, a fresh tab lists every drop." | Says the default (View: All) on screen. A tooltip change only. | 60% | P16 |
| DRO-L17 | **Move the Upgrade glow tab from Alerts to Window, after Icons.** Rows `glow.*` go from `page = "alerts"` to `page = "window"`. Window's strip becomes **Layout · Columns · Starting view · Icons · Upgrade glow** (five tabs; check it still fits one strip row at default scale, options-ui-§13 SHOULD), and Alerts keeps **Toast** alone (a legal one-tab page). Rewrite both Defaults tooltips (`Pages.lua:49`, `:52`). | Verified: the glow is applied only on window surfaces (`WindowGroup.lua:886`, `CompactGroup.lua:400`, `DetailCard.lua:404`; never `Toast.lua`) and draws over the Icons border (`Glow.lua:47`). Every item-icon look then sits on one page, two tabs apart. **This reverses part of feedback-24, the owner's own regroup**, whose stated reason ("neither is part of the window", `docs/settings-panel.md:212`) is wrong for the glow. Consequence: Window's Defaults also resets the glow, and Alerts becomes a one-tab, six-row page. | 45% | P06 |
| DRO-L20 | *(review)* Rename the Columns subsection **"Trade window"** → **"Ending soon"** (`SchemaRows.lua:395`). The slider label stays as feedback-24 set it. | Removes the two adjacent "Trade window" labels (P28). The heading then names what the one row under it does. | 45% | P28 |

## Considered and rejected

| id | change | why rejected | confidence |
|---|---|---|---|
| DRO-L13 | Relabel `trade.warnAt` "Mark a trade window ending within (seconds)" → "Trade window warning (seconds before it ends)". | The current label is feedback-24's own wording, chosen three days ago (`6f4cb22`, "Labels: … Mark a trade window ending within"). The noun-phrase gain is small. L20 deals with the real collision (P28) without overriding the owner's words. | 35% |
| DRO-L16 | Relabel the two minimum-gain sliders "Least gain to ask (item levels)" and "Least gain to toast (item levels)". | The draft's reason was ambiguity in `/dw list` and search, but `/dw list` prints paths (`messages.autoAsk.minGain`, `toast.minGain`) and there is no search. Each slider sits on its feature's own tab, so the shared label is unambiguous on screen. | 35% |
| DRO-L18 | Page order General · Drops · Comparison · Alerts · Messages · Window. | Below 40% in the draft too. It moves pages players learned three days ago for a narrative-order gain. | 35% |
| DRO-L19 | The `feed.minIlvlMode` value text "Relative to my gear" → "Relative to my average". | A value-text change only (the stored `relative` is unchanged), but the gain is a nit, and "my gear" is also Quality's phrasing ("Match my gear"), so it trades one drift for another. | 35% |
| — | Split Upgrade glow into Effect / Styles tabs (P07). | It adds the tab switching the brief wants to avoid. | — |
| — | Move `messages.transmogAsk` onto the Templates host tab (P05). | A host tab draws only its own rows, and the tooltip already links the two. | — |
| — | Rename the "Auto-ask" tab (P24), or touch Master controls (fixed by options-ui-§15), or move the Use class color companions (P26, a documented deviation). | Constrained or no gain. | — |
| — | *(review)* Fold Alerts › Toast into Messages as its first tab (page "Alerts & messages"), so Toast's and Auto-ask's minimum-gain sliders sit one tab apart and the page count drops by one more. | It mixes a passive on-screen alert with outgoing chat under a compound page name, and with L17 not taken it would split Toast from Upgrade glow. | 35% |
| — | *(review)* Fold Window › Icons and Upgrade glow into one "Icons" tab. | 41 rows on one tab; the composed Border block also needs its own heading (options-ui-§16). Two tabs side by side (L17) gets most of the gain. | 30% |

## Proposed map

All changes at 40% or more are applied; L01 and L17 are shown applied too, because the owner can
strike them.

```
Ka0s Drop Watcher (landing)                  unchanged

General
  Tab "Master controls"                      unchanged (options-ui-§15)
  Tab "Keybindings"                          NEW (item 015), host tab, before = Simulator   [L04]
                                             Toggle Drop Watcher window ⇄ Blizzard Settings › Keybindings
  Tab "Simulator"
    Simulation step delay (seconds) (sl, sim.stepDelay)                               [L05]

Drops  (page key "feed")                                                              [L01]
  Tab "Situations"
    Auto-open the window (cb, autoOpen)
    <situations table: Situation | Track | Auto-open | Quality | Loot rule> × 10      (unchanged)
  Tab "Quality"
    Minimum quality (dd)                     | Always show upgrades for me (cb)
    Fixed minimum (dd)                       | Quality floor (dd)
    "In force now: …"
    "A situation can set a quality of its own: the Quality column on the Situations tab."   [L02]
  Tab "Items"
    [sub: Item kinds]  Gear only (cb)        | Include tier tokens (cb)              [L10]
    [sub: Item level]  Minimum item level (dd: Off / Absolute / Relative to my gear) (solo)
                       Absolute minimum (sl) | Levels under my average (sl)
  Tab "Retention"
    [sub: History]  Keep history for (dd)    | Clear history… (btn)                  [L12]
    [sub: Session]  Clear this session's drops on boss kill (cb)                     [L11]

Comparison                                   unchanged
  Tab "Scoring"   Score with | Sidegrade band;  Compare against items in my bags | Protect heirlooms
  Tab "Weights"   (host: spec strip, note, 6 sliders, Import a Pawn scale)
  Tab "Unwanted types" (host: spec strip, note, weapon-type checkboxes)

Messages
  Tab "Sending"
    Ask once (cb)                            | Edit before sending (cb)              [L08]
    Announce channel (dd)                    | Offer transmog asks (cb)              [L08]
  Tab "Auto-ask"
    Ask automatically (cb) (solo)
    Delay (seconds) (sl)                     | Least gain (item levels) (sl)
  Tab "Templates"                            unchanged (Tokens, Your messages ×5, Preview, Reset templates)

Window
  Tab "Layout"
    [sub: Mode]    Window layout (dd)        | Compact view when it auto-opens in a run (cb)   [L06, L07]
    [sub: Tables]  Row height (sl)           | Font size (sl)                        [L07]
  Tab "Columns"
    note (unchanged)
    [sub: Shown columns]  Item level | Slot;  Type | Looter;  Me (my gear) | Them (looter's gear);
                          Trade | Trade window;  Actions                             [L14]
    [sub: Ending soon]    Mark a trade window ending within (seconds) (sl)           [L20]
  Tab "Starting view"
    [sub: View]  Interesting | Likely tradeable;  Usable by me | Upgrade for me   (tooltips +L15)
    [sub: Content and sort]  Content | Sort
  Tab "Icons"
    [sub: Zoom]    Icon zoom
    [sub: Border]  composed block (unchanged)
  Tab "Upgrade glow"                         moved from Alerts, rows unchanged     [L17]
    [sub: Effect] … [sub: Offset] … [sub: Pixel border] … [sub: Auto cast sparkles] …
    [sub: Button (rotating rays)] … [sub: Proc (flipbook)] …

Alerts
  Tab "Toast"
    Show a toast (cb) (solo)
    Least gain (item levels) (sl)            | Duration (seconds) (sl)
    Show in combat (cb)                      | Play a sound (cb)
    Toast scale (sl)                                                                 [L09]

Profiles                                     unchanged
```

**Counts after.** 8 pages (landing, 6 tabbed settings pages, Profiles), in today's order minus
Situations. 19 tabs: General 3 (with the new Keybindings tab), Drops 4, Comparison 3, Messages 3,
Window 5, Alerts 1. There are still 146 schema rows and none is added or removed (Keybindings' bindings
are client state, not schema rows; item 015 decides that). Tests that pin the page list and strips
(`tests/test_settings_pages.lua:18-23, :93`, `tests/test_schema_rows.lua:229, :368`) move with L01/L17.

## Cross-addon notes

- **Simulation step delay.** DropWatcher puts it on its own General › Simulator tab. BankLedger and
  LootHistory put it on General › Interface. Same label, different place. One rule for the collection
  would help: either a last **Simulator** tab on General everywhere or always on Interface. The unit
  differs too: BankLedger and LootHistory show it on the value (`fmt = "%.1f s"` vs `"%.1fs"`, two
  spellings), and DropWatcher shows none (L05 puts it in the label, as this addon does for its other
  timed sliders). Pick one form collection-wide.
- **History retention and purge.** DropWatcher: Drops › Retention (Keep history for + Clear history).
  LootHistory and BankLedger: General › **History**. DpsRace: a **History** page. The tab name differs
  (Retention vs History) and so does the button wording (Clear / Purge / Delete, with and without "…").
  Suggest one tab name (**History**) and a "…" on every button that confirms. DropWatcher cannot take
  the tab name History without renaming its `History` subsection, because options-ui-§7 forbids a
  subgroup that repeats its tab. It also keeps a session row there, so it is noted here rather than
  proposed.
- **Row height / font size.** DropWatcher: Window › Layout. LootHistory: General › Interface (row height).
  The same concept sits on a window page in one addon and on General in another.
- **Per-situation settings.** DropWatcher: Situations (→ Drops › Situations after L01). AuraMaster:
  Containers › Filters › Situations. QuickComms: Groups › When. The tab name "Situations" agrees across
  DropWatcher and AuraMaster.
- **Glow.** The style names already follow KickCD's ("Pixel border", "Auto cast sparkles", …).
  KickCD's tab is "Ready glow" and DropWatcher's is "Upgrade glow", both named by meaning. Consistent.
- **Keybinding label (item 015).** Today it is "Toggle Drop Watcher window" under header `NS.BRAND`.
  For the collection, settle one verb and noun pattern ("Toggle <Addon> window") and use the brand name
  ("Ka0s Drop Watcher") as the Keybindings category everywhere.
- **Ellipsis on confirming buttons.** "Reset all settings" (options-ui-§12/§15, every addon) asks and has
  no "…"; BankLedger's "Purge ledger…" and DpsRace's "Delete all runs…" do. L12 follows the latter.
- **Test mode / Debug console / Minimap button.** Composed, identical everywhere (options-ui-§15). No action.

## Upstream suggestions

- **options-ui-§7, "a tab that mixes control types MUST carry subsection headings".** Read literally,
  this flags almost every small DropWatcher tab, because a checkbox next to a dropdown is "mixed"
  (Quality, Scoring, Sending, Auto-ask, Layout, Toast). The examples in the rule (bar / background /
  border) are about *subjects*. Suggest rewording it to "mixes **subjects**", so audits don't push
  one-row headings onto 4-row tabs.
- **Long style-switched tabs (Upgrade glow, 34 rows, ~16 always dimmed).** DropWatcher's own rule is
  "dimmed, never hidden". A library affordance would remove most of the scroll without hiding a value
  the CLI still reaches: a subsection that collapses while every row in it is `disabledIf`-dimmed, with
  a click to expand. KickCD's Ready glow (34 rows) has the same shape.
- **Ellipsis convention.** Codify in options-ui-§12 or §8: a button that opens a confirmation ends in
  "…" ("Reset all settings…" would then follow, which is a §15 wording change and the owner's call).
- **Units in labels.** Codify "(seconds)", "(px)" and "(item levels)" suffixes for numeric sliders
  whose unit is not obvious. DropWatcher is nearly consistent already.
- **Keybindings tab position.** If item 015 lands a Keybindings tab on every windowed addon's General
  page, options-ui-§15 or §13 should fix its position (suggest: **second**, right after Master
  controls), so it is the same place in every addon, as Master controls is.

## Review

Independent review against `../DropWatcher` on `master`, 2026-10-24. Verified every page and tab
builder (`settings/Pages.lua`, `Panel.lua`, `SchemaRows.lua`, `ComposedRows.lua`, `PageEditors.lua`)
and recounted every row.

- **Current map: accurate.** Page, tab, subgroup and row order, pairings and the 146-row count all match
  the code (10 situations in `core/Constants.lua:364`, 34 glow rows, 7 Icons rows). No row changed.
- **Added problems P27-P30**: the Drops page's subject drift (which weakens L01), the doubled
  "Trade window" label on Columns, the step-delay slider's missing value format against
  BankLedger/LootHistory, and the binding's `ADDONS` category (item 015's).
- **Removed a false rationale.** `/dw list` prints paths, not labels (`libs/LibKa0s/Slash.lua:520-521`),
  and there is no settings search. L09 dropped to 40% with a different reason; L16 fell to 35%.
- **L01 recalibrated 60% → 50%** and flagged as reversing feedback-24 (`6f4cb22` created the
  Situations page on 2026-10-21), the same treatment the draft gave L17. Also noted that its Defaults
  scope now includes loot rules and per-situation auto-open.
- **L04 made concrete**: a row-less host tab placed by `before` (`OptionsTabs.lua:1203-1206`), so it
  needs no fake schema row.
- **L06 relabel rewritten**: the draft's "Auto-open in compact view…" reads as if the checkbox turns
  auto-open on. Now "Compact view when it auto-opens in a run". 65% → 60%.
- **L12 lowered 50% → 45%**: the addon's own fixed "Reset all settings" has no ellipsis.
- **L13 rejected (35%)**: it rewords a label the owner chose in feedback-24. **L20 added (45%)** in its
  place: rename the subsection heading, which fixes the real collision (P28).
- **L17 evidence checked**: the glow is applied only in `WindowGroup.lua:886`, `CompactGroup.lua:400` and
  `DetailCard.lua:404`, never on the toast. Added the one-strip-row check for a five-tab Window page.
- **Moved L13, L16, L18 and L19 (all under 40%)** into a new "Considered and rejected" table, with two
  more consolidations considered and rejected (Toast into Messages; Icons plus Upgrade glow).
- **Proposed map and counts redone** without the rejected items. Page order is unchanged, apart from
  Situations going away. Listed the tests that pin the page list.
- **No change alters a key, default, range or behaviour.** L14 adds a display-only field. L01 and L17
  change only each page's Defaults scope and `/dw list` section heading, and both are flagged.

