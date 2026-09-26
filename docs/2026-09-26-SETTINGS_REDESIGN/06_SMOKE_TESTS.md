# In-client smoke tests: AuraMaster settings redesign (#6)

**The owner runs these checks in the client and fills the Result column.** Claude writes the checks
and never marks one passed. Record `pass`, `fail: <what you saw>` or `skip: <why>`, then the date. The
same list goes into AuraMaster's `docs/smoke-tests.md` under "Settings redesign (#6)" (SR-AM-06).

**Setup:** AuraMaster on `feat/2026-09-26-settings-redesign` (after SR-AM-06), carrying LibKa0s v1.61.0.
Open a character with the starter containers: #1 Player buffs (bars), #2 Player debuffs (icons) and
#4 Player cooldowns (text). Open the panel with `/am`.

Checks S1-S8 are the spec's §8, in its words. S9-S16 are this plan's additions, and each one names
where it comes from.

| # | Check | Expected | Source | Result |
|---|---|---|---|---|
| S1 | Look at the Settings tree under Ka0s Aura Master. | General · Containers · Profiles. There are no Filters, Layout, Bars, Icons or Text entries, indented or not. | spec §8.1 | |
| S2 | Open Containers with #1 selected. | The band is on top (Container picker and New container). The rail is on the left with General · Filters · Layout · Bars. The rail's top edge is level with the top of the tabs: the tab art, not the empty space above it. | spec §8.2, D5 | |
| S3 | Rail -> Bars -> General, then scroll to the bottom. | Only the controls move. The band, the rail and the tab strip stay put. | spec §8.3 | |
| S4 | On Bars, pick #2 (icons) in the band. Then on Bars again with #1, change General -> Style to Icons. | The style entry renames to Icons, its tabs follow, and the page is on Icons, not General. | spec §8.4, D6 | |
| S5 | Filters -> Categories, then Layout, then back to Filters. | Filters opens on Categories. | spec §8.5, D8 | |
| S6 | Change a Layout setting and a Bars setting on #1. Then, with Layout selected, click Defaults. | Only the Layout rows go back to defaults, on #1 only. The Bars change stays, and other containers are untouched. | spec §8.6, D9 | |
| S7 | Layout -> Anchor -> Pick a frame..., then click a frame. Repeat and cancel with Esc. | Both times the settings window reopens on Containers -> Layout. | spec §8.7, Review Focus 5 | |
| S8 | Open Containers, then enter combat (attack a training dummy). | The whole page is under the combat cover, the rail included, with "Settings are locked during combat." Nothing under it can be clicked. | spec §8.8, options-ui-§2 | |
| S9 | `/reload`, then open Containers as the first page of the session. | The tabs sit in one row to the right of the rail from the first frame. They are not stacked one per row, and none is drawn under the rail. | Review Focus 1 (SR-LK-01) | |
| S10 | Look at the rail, and hover each entry. | It has the tree-pane look (a dark fill and a thin gray tooltip border). Entries are gold, the selected one is white on a blue bar, and hovering highlights. Each entry shows a tooltip that says what the section holds. It is visibly different from the gold tabs. | spec §2, A13 | |
| S11 | Close the panel. Right-click a container's drag handle or its `?`. | The panel opens on Containers with that container in the band, on the section you last left. It does not jump to General. | A9 (SR-AM-04) | |
| S12 | Filters -> Categories -> "See spells" on a spell-list category. | It lands on the General page's Spell Categories tab, with that category selected. | A10 (unchanged behavior) | |
| S13 | Delete every container (Containers -> General -> Delete, each). Then click New container. | With none, the rail lists General alone, with "No containers yet. Click New container, or type /am new." After New container, Filters, Layout and Bars appear. | A12 | |
| S14 | Rename #1, change its Unit, then click Defaults on General. | Enabled, Unit, Aura type and Style go back to defaults. The name you typed is kept. | spec §3, D9 | |
| S15 | In combat, try clicking a rail entry. Leave combat. | During combat nothing changes and one gray "locked" line prints. After combat the page draws normally. | A1 (SR-LK-01) | |
| S16 | Open the settings of another Ka0s addon, such as KickCD or MultiMeters. | Their tab strips, content panels and scroll bars are exactly where they were. The library minor AuraMaster ships is the one loaded for every Ka0s addon, and a page with no rail must not move. | Global Constraints (rail width 0 is byte-identical) | |
