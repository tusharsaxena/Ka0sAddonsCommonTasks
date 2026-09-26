# In-client smoke tests: NavRail adoption (MultiMeters#55, KickCD#33, the v1.61.0 re-vendor)

**The owner runs these checks in the client and fills the Result column.** Claude writes the checks
and never marks one passed. Record `pass`, `fail: <what you saw>` or `skip: <why>`, then the date.
The MultiMeters checks also go into MultiMeters' `docs/smoke-tests.md` as section 36 (NR-MM-04), and
the KickCD checks into KickCD's `docs/smoke-tests.md` as section 36 (NR-KC-04). The re-vendor check
has no per-addon section: it covers the library copy each addon ships.

**Setup:** every addon on `feat/2026-09-26-navrail-adoption`, after NR-MM-04 and NR-KC-04, each
carrying LibKa0s v1.61.0. Two meter windows in MultiMeters (Windows -> General -> New window makes
the second one). In KickCD, a target and a focus you can pick (a training dummy and a second dummy
work).

## The re-vendor (M1)

| # | Check | Expected | Source | Result |
|---|---|---|---|---|
| RV-S1 | Disable AuraMaster, `/reload`, then open the settings of AbsorbTracker, BankLedger, ConsumableMaster, LootHistory, PanelMaster, PartyFrameEnhanced, PrettyChat and WhatGroup, one page each. With AuraMaster disabled, the Options copy loaded is one of these addons' own v1.61.0 copies. | Every page looks exactly as it did on v1.60.0: tab strips, content panels and scroll bars where they were. None of these pages draws a rail, and a page with no rail must not move. | Global Constraints (rail width 0 is byte-identical); NR-XX-01 | |

## MultiMeters: the Windows page (#55)

Open the panel with `/mm config`.

| # | Check | Expected | Source | Result |
|---|---|---|---|---|
| MM-S1 | Look at the Settings tree under Ka0s Multi Meters. | General · Windows · Profiles. There are no Frame, Header, Bars, Tooltip, Visibility or Columns entries, indented or not. | spec §A1; NR-MM-04 | |
| MM-S2 | Open Windows. | The Active window picker is the band across the top, full width. The rail is on the left with General · Frame · Header · Bars · Tooltip · Visibility · Columns, and the page opens on General. The rail's top edge is level with the top of the tab art (the tab itself, not the empty space above it). | spec §A2; options-ui-§13, §14 | |
| MM-S3 | Rail -> Bars, then scroll to the bottom of the Bar tab. | Only the controls move. The band, the rail and the tab strip stay where they are. | spec §A2 | |
| MM-S4 | Frame -> Size and position, then Bars, then Frame again. | Frame opens on Size and position. Repeat with Columns -> Header background, then General, then Columns: Columns opens on Header background. | spec §A3 (per-entry tabs); NR-MM-02 | |
| MM-S5 | On Bars -> Border, pick the other window in the band. | The page stays on Bars -> Border, and the values shown are the other window's. Pick the first window again: the same. | options-ui-§14 (the rail is not a picker); NR-MM-02 | |
| MM-S6 | On General: rename the window in the name box and press Enter, click New window, Duplicate window, then Delete window and confirm. Then, under the Copy settings from heading, pick the other window as Source window, pick Bars under Settings to copy, and click Copy. | General shows one tab, named General. Each act does what it did on the old Window tab, and the band follows the new or duplicated window. The copy changes only the active window's Bars settings to the source's. | spec §A2 (Copy folded into General); R2 | |
| MM-S7 | Columns -> Columns tab. Start dragging a block by its handle, and while the mouse is still down, click Frame on the rail. Release. Then go back to Columns. | The page moves to Frame with no drag handle left on any Frame row. Back on Columns, every block is there, in an order you can read, and dragging still works. | Review Focus 1; NR-MM-02 | |
| MM-S8 | With the first window active: change a Frame setting (Size and position -> Width) and a Header setting (Title bar -> Header height). Select Frame and click Defaults. Then select General and click Defaults. Then change the column order on Columns, select Columns and click Defaults. | Frame's Defaults puts only the Frame rows back, on the active window only: Header height keeps your value, and the other window is unchanged. General's Defaults changes nothing and prints one line saying General has no settings to restore; the window keeps its name. Columns' Defaults restores the shipped column list and the header text and background settings. | Review Focus 2; spec §A3 (Defaults); R1 | |
| MM-S9 | Open Windows, then enter combat (attack a training dummy). Try clicking a rail entry. Leave combat. | The whole page, rail included, is under the combat cover with "Settings are locked during combat." Nothing under it can be clicked, and one gray "locked" line prints. After combat the page draws normally, on the entry you were on. | options-ui-§2, §13 | |
| MM-S10 | `/reload`, then open Windows as the first page of the session. | The tabs sit in one row to the right of the rail from the first frame. None is drawn under the rail, and none is stacked one per row. | Global Constraints; NR-MM-02 | |
| MM-S11 | Hover each rail entry. | Each shows a tooltip saying what the entry holds. The rail looks like a tree pane (gold entries, the selected one white on a blue bar), visibly different from the gold tabs. | spec §A2 (rail tooltips) | |

## KickCD: the Grid page (#33)

Open the panel with `/kcd config`.

| # | Check | Expected | Source | Result |
|---|---|---|---|---|
| KC-S1 | Look at the Settings tree under Ka0s KickCD. | General · Grid · Spells · Profiles. There are no Icons, Cast bar or Text Label entries. | spec §B1; NR-KC-04 | |
| KC-S2 | Open Grid. | The Unit picker is the band across the top, full width. The rail is on the left with Icons · Cast bar · Text Label, and the page opens on Icons. The rail's top edge is level with the top of the tab art. | spec §B2; options-ui-§13, §14 | |
| KC-S3 | Rail -> Cast bar, then scroll to the bottom of the Interruptible tab. | Only the controls move. The band, the rail and the tab strip stay where they are. | spec §B2 | |
| KC-S4 | Cast bar -> Font, then Icons, then Cast bar again. | Cast bar opens on Font. Text Label -> Placement, Icons, Text Label: it opens on Placement. | spec §B3 (per-entry tabs); Review Focus 3 | |
| KC-S5 | Untick General -> Units -> "Use same styling as Target". On Grid -> Cast bar -> Font, pick Focus in the band. | The page stays on Cast bar -> Font, and the values shown are Focus's. | options-ui-§14 (the rail is not a picker); NR-KC-02 | |
| KC-S6 | Tick "Use same styling as Target" again. Open Grid with Focus in the band and click each rail entry. Then click the link in the note. | The rail is there on a linked Focus. Each entry draws its full tab strip, grayed and not clickable, with only the "Linked to Target..." note under it. The link opens General on its Units tab. | spec §B3 (linked Focus); R9 | |
| KC-S7 | Untick the link again. With Target in the band, change a Cast bar setting and an Icons setting for Target, and a Cast bar setting for Focus. Select Cast bar and click Defaults. | Only Target's Cast bar settings go back to defaults. Target's Icons setting and Focus's Cast bar setting keep your values. The Defaults tooltip says it restores the selected unit's settings in the section on screen. | Review Focus 4; spec §B3 (Defaults); R8 | |
| KC-S8 | Open Grid, then enter combat. Try clicking a rail entry. Leave combat. | The whole page, rail included, is under the combat cover with "Settings are locked during combat." Nothing changes, and one gray "locked" line prints. After combat the page draws normally, on the entry you were on. | options-ui-§2, §13 | |
| KC-S9 | `/reload`, then open Grid as the first page of the session. | The tabs sit in one row to the right of the rail from the first frame. None is drawn under the rail. | Global Constraints; NR-KC-02 | |
| KC-S10 | Type `/kcd reset castbar`. | The reply says the page-shaped reset is gone and points at Grid -> Cast bar's Defaults button (for the unit in the band), or `/kcd reset <path>`. | spec §B3 (slash wording); R13 | |
| KC-S11 | Hover each rail entry. | Each shows a tooltip saying what the entry holds. | spec §B2 (rail tooltips) | |
