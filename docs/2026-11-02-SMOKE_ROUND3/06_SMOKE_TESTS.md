# Smoke tests: the owner's third smoke round (2026-11-02 to 2026-11-03)

**Fully exit and restart the client before you start. A `/reload` is not enough.** This round ships a new font file (Ka0s Ubuntu, LibKa0s R3-L6), and the client only loads a new font file on a fresh start. It also deletes Ka0s Friz Quadrata TT and moves stored picks of it. Every check below assumes the re-cut LibKa0s v1.85.0 (fd57b83), re-vendored into all 16 addons. Turn Lua errors on with `/console scriptErrors 1`. Any Lua error or taint warning fails the check.

Nothing here has passed. Every Result is blank for you to fill in. An ID is the check's ID in that addon's `docs/smoke-tests.md`, where the full steps are; the short form is here. IDs starting `SR3-` are new on this list only and have no addon file. They cover library items whose only witness is a window you open by hand. Order: A is the library, B is DpsRace, C is the step delay sliders, D is the skin fonts, E is the per-addon checks this round added or re-opened.

## A. Library (R3-L1, R3-L2, R3-L3, R3-FIX)

| ID | Do | Pass | Result |
|---|---|---|---|
| ST SHOW-28 (re-opened, R3-L1) | `/st show` in Obsidian, Controls' five dropdowns; General > Skin, clear Scope > Ignore settings panel; open each; pick Glass; tick Ignore settings panel again | With the box clear, AceGUI Dropdown, Ka0sMedia_Font and Ka0sMedia_Statusbar look like the skinned WowStyle1 one: a flat box in the skin's fill and edge, label left-aligned, one chevron in the skin's arrow color, no gold button. Each open list wears the skin, the font rows in their own faces and the bar rows with their swatches. All five follow Glass. With the box ticked again those three go back to stock | |
| ST PANEL-5 (re-opened, R3-L1) | Untick Ignore settings panel, pick Obsidian, Settings > AddOns > Ka0s Skin Tester > Sample controls; pick Glass on General and come back | One heading over the sample rows and companions, all in the skin; the dropdown and the five media pickers wear the skinned dropdown look; the page follows Glass | |
| ST PANEL-14 (re-opened, R3-L1) | Same page: open the font row and the border row under Obsidian, then Glass | Both closed rows are the skinned box with their preview kept, lined up with the rows around them; both pull-outs wear the skin with a preview on every row | |
| SR3-1 | Any addon's own settings page with an AceGUI dropdown and a font or texture picker (for example LootHistory's Skin tab, or DpsRace's HUD Appearance), Ignore settings panel unticked, in Obsidian then Ka0s Default | The dropdown and the picker wear the skinned dropdown look of SHOW-28, the picker keeps its font or texture preview in the box, the open list is skinned. Ticking Ignore settings panel puts the page back to stock | |
| SR3-2 (R3-L2) | `/st show`, Overlays, the "FadeNineSlice (left) beside stock" sample, in Obsidian, Ka0s Default, Azeroth and WoW Default | The left box has a visible 1 px edge in the skin's border color in all four skins, like the MakeResizable box (image 93), and stays visible on Obsidian's black. Fail: a box with no edge (images 85 to 87) or an edge thicker than 1 px | |
| ST SHOW-39 (new, R3-L3) | `/st show` in Ka0s Default, Azeroth, WoW Default and Obsidian: Overlays' IconBorder sample, Addon surfaces' icon border, Controls' SquareIcon (crop) + IconBorder | Each icon zoomed in, its own art edge gone, inside a 1 px outline in the skin's icon border color, the same thickness in every skin. Fail: the art's gray frame inside the outline, a 2 px edge in Ka0s Default or Azeroth, a tooltip-style edge in WoW Default | |
| ST SHOW-41 (new, R3-FIX) | Controls in Obsidian: SquareIcon (crop) + IconBorder, switch skins twice; then Options > Graphics > UI Scale, change it and come back | The crop stays as tight as SquareIcon left it after each switch. After the UI scale change every IconBorder outline and FadeNineSlice edge in the showroom is still exactly 1 px | |
| SR3-3 (R3-FIX) | DpsRace `/dr test running` with spell rows on; move the HUD's *Scale* setting two steps, then back | The spell icons' outline is 1 px after every scale change, never 2 px or blurred. (A window scale change; the UI scale case is SHOW-41) | |
| DR SM-DR-R3FIX1 (new, R3-FIX) | `/dr test running` with spell rows on; a run's detail with *Compare vs best* and its timeline; Ka0s Default, Obsidian, WoW Default | Every spell icon on the HUD rows, the compare rows and the timeline pairs shows its art cropped inside the 1 px outline, never the beveled Blizzard edge inside it (image 103) | |
| ST SHOW-32 (re-opened, R3-L3) | Obsidian: Overlays, Values, Faces and widths, then Azeroth | As its file says; the IconBorder sample and SquareIcon carry the 1 px skin edge | |

## B. DpsRace (R3-DR-1 to R3-DR-5)

| ID | Do | Pass | Result |
|---|---|---|---|
| DR SM-DR-R3DR1 (new) | Fresh client start; `/dr test running` with clocks on *Elapsed and time left* and every *Use the skin's font* ticked; pick Ka0s Default, Obsidian, WoW Forever, Glass | The green *Elapsed* and red *Left* numbers draw each skin's HUD face (Prototype, Expressway, Fira Sans SemiBold, Avant Garde), never JetBrains Mono with its dotted zero, and change at once on each pick, as the Damage and DPS figures and the spell rows do. Green and red kept, no outline | |
| DR SM-DR-SF11 (re-opened by R3-DR-1) | HUD > HUD Appearance, *Elapsed clock* and *Time left clock*; `/dr test`; pick another skin | Each clock has *Use the skin's font* ticked, its picker shows the skin's face, both clocks draw in it; the picker is free once unticked | |
| DR SM-DR-R3DR2 (new) | Create a new profile, switch to it, open the race window and the Race page; switch back to your own profile | The idle HUD selects 1:00 and *Arm Race* arms 1:00; *Default race length* reads 1:00. Your own profile keeps its length | |
| DR SM-DR-DL4 (amended) | New profile, open the race window | The idle HUD offers 1:00 (2:00 before R3-DR-2) | |
| DR SM-DR-R3DR3 (new) | New profile with the HUD closed; HUD > Race HUD and Race > Auto-arm; walk up to Silvermoon's training dummies and target one; walk away; switch back | *Show near a training dummy* ticked, *Arm on a training dummy* not. The HUD opens on the Arm Race screen near the dummies, nothing arms, it closes a few seconds after you walk away. Your profile keeps what it stored | |
| DR SM-DR-TA1 (amended) | New profile: untick *Show near a training dummy*, target a dummy with both rows off | Nothing opens and nothing arms | |
| DR SM-DR-R3DR4 (new) | With runs stored, `/dr hud show`: target a dummy you have a 1:00 best on, click 0:30, *Custom* (a length never raced), 1:00; another dummy type, then none; switch spec; hover the card, click it; `/dr test` and another skin | *Your best · <spec> · <type> · 1:00* in the label color between the Target card and *Arm Race*; the card shows the best's DPS large in the HUD face, damage dim on the right, *date · ilvl · top spell* dim below; *Arm Race · beat <DPS>*. Every change swaps it at once; no best reads "No race yet: this one sets the mark", no target "Target a dummy to see your best". Hover: tooltip with the full run. Click: Results on that run. It follows the skin and nothing else in the layout moves (image 101) | |
| DR R1 (amended) | `/dr hud show` with no target, then target the Golem | The idle body now includes the *Your best* section; nothing overlaps | |
| DR SM-DR-R3DR5 (new) | A profile that never styled a bar: a run that is not its board's best, tick *Compare vs best*; put the Runs list's bars beside it; pick Obsidian, Glass, High Contrast | The *This run* blue and *Runner-up* gold bars are as bright as the Runs list's bars (image 104), not image 103's dim ones, each in its own hue; every white figure reads clearly; only the texture follows the skin | |
| DR SM-DR-BS2 (amended) | *Compare vs best* on a non-best run, then on the best | The bars as bright as the Runs list's (R3-DR-5); which column is blue and the *Difference* colors unchanged | |
| DR SM-DR-FS11 (re-opened, R3-L3) | Spell icons on the HUD, a run's detail, the chart's cooldown icons, the compare and the timeline | Each wears the skin's 1 px icon border, black under Ka0s Default; hides with *Show spell icons* off | |

## C. Simulation step delay (R3-SIM-KC, R3-SIM-MM, R3-FIX)

| ID | Do | Pass | Result |
|---|---|---|---|
| KC SIM-15 (new) | `/kcd config` > General > Simulator: set *Simulation step delay* to 4, `/kcd sim start pull`; mid-run drag it to 1; `/kcd get sim.stepDelay`; `/kcd set sim.stepDelay 0.3`; General's Defaults | One slider 0.5 to 10 in 0.5 steps, at 1. Steps about 4 s apart, then the waiting step keeps its 4 s and later ones come about 1 s apart. The get answers the value, 0.3 is refused, Defaults puts it back to 1 | |
| KC SIM-16 (new, R3-FIX) | Step delay 4, `/kcd sim start pull`; then `/kcd sim start miss`; set it back to 1 | The target's cast bar is still filling when your kick plays and the kick ends it; no kick lands on a finished cast and no bar sits full; at "Shadowcaster casts again while your kick cools" the kick icon is still cooling. In `miss` the third kick is refused on cooldown and an unkicked cast ends by itself when its bar fills | |
| MM SIM-13 (new) | Settings > General > Behavior > Simulator: step delay 4, `/mm sim start dungeon`; mid-run set it to 1 | About 4 s between steps, then about 1 s from the step after next; the slider runs 0.5 to 10 in 0.5 steps and ships at 1 | |

## D. Skin fonts (R3-L4 to R3-L7, R3-FRIZ)

| ID | Do | Pass | Result |
|---|---|---|---|
| SR3-4 (R3-L4) | Loot History in Obsidian, then Ka0s Default (images 95, 96) | The Date column shows "02-Nov-2026" whole in Obsidian, as in Ka0s Default; the body text is one step smaller and still reads well | |
| SR3-5 (R3-L5) | Loot History's table in Obsidian, then Glass, Ember, WoW Default, WoW Midnight, WoW Forever, Azeroth | The alternate row background is clearly visible in every one, not faint; a hovered plain row still reads differently from a striped row | |
| SR3-6 (R3-L6) | Pick WoW Default; look at a window (Loot History or BankLedger), a settings page (Settings > AddOns > Ka0s Skin Tester > Sample controls, Ignore settings panel unticked) and a HUD (DpsRace `/dr test running`, or MultiMeters) | All three draw Ka0s Ubuntu (body, titles and HUD figures), visibly unlike Ka0s Default's Prototype, no square boxes for glyphs; Loot History's Date column fits (image 98 truncated it) | |
| SR3-7 (R3-L7, R3-FRIZ) | Before updating, in two addons (for example LootHistory's Skin tab Font and DpsRace's *Live figures* Font) pick *Ka0s Friz Quadrata TT* and log out; install, fully restart, open both | Both now read *Ka0s Ubuntu* and draw in Ubuntu; no picker lists Ka0s Friz Quadrata TT; Blizzard's own *Friz Quadrata TT* is still offered and a pick of it is kept | |
| Per-addon Friz migration (new) | As each file says: ST SHOW-40, AT MIGRATE-7, AM SKIN-46, BL SKIN-40, CM SKIN-41, DR SM-DR-R3FRIZ, DW SKIN-44, KC SKIN-43, LH SKIN-48, MM SKIN-43, PM SKIN-36, PF SKIN-39, PG SKIN-48, PC SKIN-32, QC FSKIN-13, WG SKIN-34 | A stored Ka0s Friz pick reads and draws Ka0s Ubuntu after the update; a Blizzard Friz pick is kept | |
| WoW Default face, re-opened (R3-FRIZ) | ST SHOW-13, SHOW-19; AT SKIN-33, MIGRATE-2; AM SKIN-4; BL SKIN-9, PROFILE-14; CM SKIN-4, PROFILE-5; DR SM-DR-FP1; DW SKIN-15, SKIN-32; KC SKIN-6; LH SKIN-7; MM the HUD faces row; PM SKIN-24, INSTALL-8; PF SKIN-4; PC SKIN-22; QC SKIN-5; WG SKIN-6 | As each file says, with WoW Default on Ka0s Ubuntu and the schema stamps it now names | |

## E. Icon edges in the addons (R3-L3, R3-FIX), re-opened or new

| ID | Do | Pass | Result |
|---|---|---|---|
| AM SKIN-35, SKIN-36 | New profile on Ka0s Default; then Obsidian, Azeroth, High Contrast, WoW Default | 1 px icon borders in every skin, the art zoomed; colors follow the skin | |
| CM SKIN-42 (new) | *Use the skin's border* ticked; Ka0s Default, Azeroth, Ember, WoW Midnight, WoW Default; untick | Flat 1 px button border in every skin, never 2 px or tooltip art; unticked, your style comes back | |
| DW SKIN-45 (new), SKIN-14, SKIN-38, SKIN-40, SKIN-3, ICON-1 (amended) | `/dw test`, *Use the skin's border* ticked, the same five skins | Every item icon (rows, cards, toast) has a flat 1 px edge; glows as SKIN-38 and SKIN-40 say | |
| KC SKIN-1, SKIN-37 | `/kcd unlock`, Ka0s Default then each skin | Every icon and the cast bar icon a 1 px edge in the skin's color, art zoomed | |
| MM SKIN-28, SKIN-34 | Each skin; WoW Default mid-pull | Unit icon edge a flat 1 px outline in every skin, WoW Default included, no tooltip art; none on an empty row; no error mid-pull | |
| PF SKIN-36 | Glass, then the cast bar icon in each skin; hide the icon | 1 px edge in the skin's icon color, art zoomed, hides with the icon | |
| QC SKIN-1, FSKIN-14 (new) | A pad's Icons border with *Use the skin's border*, each skin | 1 px edge in every skin | |
| WG SKIN-1, SKIN-32 | `/wg test` on a mapped dungeon, every skin | The teleport icon is zoomed inside a 1 px outline in every skin, no tooltip edge on WoW Default | |

## Carry-over

Every other check on the two earlier lists (`docs/2026-11-01-FULL_SKINNING/06_SMOKE_TESTS.md`, `docs/2026-11-01-SMOKE_FEEDBACK/06_SMOKE_TESTS.md`) is recorded there as passed on 2026-11-02 and is not repeated here.
