# Smoke tests: full skinning

**Fully exit and restart the client before you start. A `/reload` is not enough, because this run added files** (library icons, `core/WidgetsSetup.lua` in PremadeGroupsFilterExtension, a new skin border). Turn Lua errors on with `/console scriptErrors 1`. Any Lua error or taint warning fails the check you are on.

Nothing on this list has passed. Every Result is blank for you to fill in. The ID is the check's ID in that addon's `docs/smoke-tests.md`, where the full steps are; each row here is the short form. Your results then go into each addon's file.

How to read the list:

- Each ID has one Result row. Sections 3 and 4 point at IDs; their Result rows are in section 2 or 5.
- **[Old]** needs a profile from before this build. You have run this branch in game already, so a profile you test on may already have moved. A profile that has moved carries `skin.fullSkinReset = true` in SavedVariables. If it has, restore a backup from before this run, or write "already moved" in Result.
- **[No lib]** means rename `libs/LibKa0s` aside, `/reload`, check, then put it back. Leave these until the end of each addon.

Scope: everything this run added or re-opened. Older owed lines still in the addons' Pending sign-off sections are not repeated here.

## 1. The order

1. Restart the client.
2. Section 2, Check these first.
3. Section 3, Ka0s Default look changes: accept or reject each.
4. Section 4, the per-skin walk.
5. Section 5, addon by addon.

## 2. Check these first

### QuickComms: the dial's animations

| ID | Do | Pass | Result |
|---|---|---|---|
| ANIM-12 | Dial page, Animation tab: Scale in and fade at 0.5 s, then 2 s. Open and close a dial with a long title such as "Quick Comms: World". Reverse one mid-way. Send on a slice at 2 s | No shimmer, no letter jitter, no truncation or ellipsis at any moment. Each string stays on its slice, nothing jumps at landing, the sent slice's label pulses | |
| ANIM-17 | Rotate and scale, first in-game trial | The ring swings about 120° as it grows and winds back as it shrinks. Fills, shine and masks turn cleanly about the center, no mask edge shows, icons and text stay upright, the hub stays level | |
| ANIM-18 | Squash and Flip, first in-game trial. Only a client can prove the one-axis scale | The art really stretches on one axis, masks and slices included, and nothing snaps back at a leg's end or at landing. Text stretches with it. If the dial only shrinks evenly, the client took the substitute: write that down | |

### QuickComms: the pad in each skin

`/qc test` for a pad, every box at its default. Compare a hairline with that skin's window edge on the settings or Preview window.

| ID | Do | Pass | Result |
|---|---|---|---|
| PLOOK-1 | Ka0s Default | Dark buttons with a soft gradient, gentle gloss, thin gray edge. Header and titles draw no band. Fail: the old flat wash, or gloss brighter than Obsidian's | |
| PLOOK-2 | Obsidian | Gloss about a third lighter, hairline edges on bands and buttons | |
| PLOOK-3 | Azeroth | Leather buttons, lighter gloss, hairline gold-brown band edges | |
| PLOOK-4 | Glass | Gloss cap a third lighter; band edges a thin frosted line, not the thick pale frame | |
| PLOOK-5 | High Contrast | White hairlines on bands and buttons, no shine. Fail: a band edge heavier than a button's | |
| PLOOK-6 | Ember | Ember buttons, lighter gloss, hairline band edges | |
| PLOOK-7 | WoW Default | Dark window, gray edge, gray bands with gold text, clear red buttons with a soft sheen. Fail: any white band or edge, or maroon buttons | |
| PLOOK-8 | WoW Midnight | Night-violet buttons, gold hairlines, lighter gloss | |
| PLOOK-9 | WoW Forever | Charcoal buttons, lighter gloss, hairline band edges | |
| PLOOK-10 | Pad, Buttons and Dial, Slices: Use the skin's shine ticked, then unticked | Ticked: Shine strength is gray, a dial on the skin's look reads as light as the pad. Unticked: the row wakes and your stored value draws under every skin | |
| PLOOK-11 | WoW Default, pick a Texture on the Skin tab, then back to the skin's own | Buttons take it, then return to flat red. A page dot's edge is dark, not white | |

### QuickComms: layering (two things to judge)

| ID | Do | Pass | Result |
|---|---|---|---|
| LAYER-6 | Open a bag addon, a meter and a Ka0s settings window. Drag a pad over them. Open a dial by key over them. Open `/qc debug` under the pad | Pad and dial draw on top and click. **Judge the deviation:** pads sit at DIALOG, so they also draw over settings and Blizzard popups. Say whether you keep that, and whether a pad over the console reads wrong | |
| LAYER-7 | With a pad over settings, Preview as… on, dial 1 open: open the preview window, a callout popup, the icon browser, a dropdown, the color picker, a delete confirm | Each opens over what it should. **Judge the deviation:** the dial is at FULLSCREEN, not the FULLSCREEN_DIALOG issue #14 proposed, so the modals can still cover a preview dial. Spec: `QuickComms/docs/superpowers/specs/2026-11-01-pad-dial-strata-design.md`, rulings 1 and 2 | |

### PartyFrameEnhanced: Show border

An earlier step on this branch (schema v5, between `ab05a0c` and `a376cf8`) may have ticked Show border on your profile. Code cannot tell that from a tick you made. Look at each of the three and put it as you want it: untick any not wanted, re-tick any lost.

| ID | Do | Pass | Result |
|---|---|---|---|
| (no ID) | Cast Bars, Bar: Show border | As you want it, set by hand | |
| (no ID) | Target Frames, Bar: Show border | As you want it, set by hand | |
| (no ID) | Pet Frames, Bar: Show border | As you want it, set by hand | |
| SKIN-38 | [Old] Before updating: Target Frames Show border off with a style picked, Cast Bars on with a style. Update, log in under Ka0s Default | Target Frames stays unticked and draws nothing, style still stored. Cast Bars stays ticked and draws | |
| SKIN-25 | New profile, Ka0s Default, Cast Bars, Bar: then tick Show border. Try Azeroth | Unticked draws nothing. Ticked draws the stored style at its thickness under a None skin (Ka0s Default, Obsidian, Glass, Ember, WoW Forever). Under a skin with its own style, the skin's style wins | |

### DpsRace: your three additions

| ID | Do | Pass | Result |
|---|---|---|---|
| (no ID) | The 42 dummies. Target a dummy from your city-hub captures and `/dr target` | It prints the name, creature ID and category you gave it. The catalog grew from 5 to 42 (`09f02e7`); your own list's now redundant entries stop applying. No check in `docs/smoke-tests.md` names the new rows | |
| SM-DR-TA17 | General: read the New-best toast tab, press Test toast | Toast sound row present, Toast duration at 10, toast stays 10 seconds. A stored duration stays yours | |
| SM-DR-FS1 | New-best toast: leave Toast sound on Default, press Test toast | The alert you have always heard plays | |
| SM-DR-FS2 | Open Toast sound, press a row's play button, pick a sound, Test toast, reopen the list | Default first, then every LibSharedMedia sound. The toast plays the pick, not the alert | |
| SM-DR-FS3 | With that pick, untick Play a sound, change the sound, Test toast; tick it, Test toast | Row stays live while unticked. Silent, then the latest pick plays | |
| SM-DR-FS4 | Pick a sound, disable the addon that registered it, `/reload`, Test toast | The row still reads the key, the alert plays | |

## 3. Ka0s Default look changes: accept or reject

Each of these moves pixels under Ka0s Default on purpose. You ruled that they stay and are named here. Reject any you don't want and it comes back out.

| Addon | What changed | Check | Accept or reject |
|---|---|---|---|
| WhatGroup | Title sits 2 px higher; teleport icon gains an edge | SKIN-1, SKIN-32 | |
| BankLedger | Tabs gain a dark backing, full-width underline and faint rule | SKIN-35 | |
| BankLedger | Footer gains a dark band | SKIN-35 | |
| BankLedger | Export title bar 30 high, was 26 | SKIN-36 | |
| LootHistory | Tabs gain a dark backing | SKIN-43 | |
| LootHistory | Holdings header gains the History header's faint band | SKIN-43, LED-13 | |
| DropWatcher | Idle tabs 0.62 to 0.7 gray, a touch lighter | SKIN-43 | |
| MultiMeters | Centered title | SKIN-28, SKIN-37 | |
| MultiMeters | Faint band behind the column labels | SKIN-28, SKIN-34 | |
| MultiMeters | Border around each unit icon | SKIN-28, SKIN-34 | |
| PremadeGroupsFilterExtension | Level box, copy box and copy label white to 0.9 gray | SKIN-44 | |
| PartyFrameEnhanced | Cast bar icon gains a 2 px edge | SKIN-36 | |
| QuickComms | Ka0s Default buttons: fuller body, edge, gradient and gloss | PLOOK-1, BUTTON-1 | |
| Every addon with a simulator | Steps title band 30 high | any `sim` run | |
| Every addon | An owned tooltip title takes `gtip.title` | hover a strip or Sim tooltip | |
| Addons with a library strip | A strip's icon wears `icon.tint` | any `test` strip | |

## 4. The per-skin walk

Goal check: change the skin and every addon changes with it, HUD backgrounds, borders and glow included, while the settings panel stays stock until you clear the Scope.

Start with the showroom, since it prints each skin's values: `/st show`, then SHOW-34, SHOW-35 and SHOW-36 in section 5. Then put every HUD on screen and step through Obsidian, Azeroth, Glass, High Contrast, Ember, WoW Default, WoW Midnight, WoW Forever and back to Ka0s Default, with no `/reload`.

| Step | Pass | Checks in section 5 | Result |
|---|---|---|---|
| HUD text, fill and shadow on each skin | Change live in every addon. Class, meaning and warning colors do not change | AT SKIN-36, 37; AM SKIN-36, 37; KC SKIN-37, 40; CM SKIN-32, 33; DR FS7; DW SKIN-39; MM SKIN-29, 30; PF SKIN-33, 35; QC FSKIN-2, 3, 4 | |
| HUD backgrounds on each skin | Each skin draws its own `bar.bg`, and non-default skins differ from each other | AT SKIN-36; AM SKIN-36; KC SKIN-37; CM SKIN-32; DR FS15; ST SHOW-36 | |
| Bar borders | Azeroth, High Contrast, WoW Default and WoW Midnight draw their own style. The other skins defer to Show border and your stored style | AT SKIN-41; AM SKIN-36; CM SKIN-37; DR FS16; MM SKIN-40; PF SKIN-25; QC FSKIN-12; ST SHOW-34 | |
| Icon borders | Each skin's own color and size | AM SKIN-36; DW SKIN-40; KC SKIN-37; WG SKIN-32; DR FS11; MM SKIN-34; PF SKIN-36 | |
| Glow | Each skin's own glow color. DropWatcher's off-spec glow changes once on leaving Ka0s Default, then stays the same in every skin (see 99_REPORT.md, known limits) | AM SKIN-40; DW SKIN-40; KC SKIN-37 | |
| Gloss under Glass | A soft shine that ends where the fill ends, none under other skins | AT SKIN-40; AM SKIN-41; KC SKIN-41; MM SKIN-33; PF SKIN-36; DR FS17 | |
| Windows | Title bars, tabs, footers and row hover follow the skin | BL SKIN-35, 36; LH SKIN-43; DW SKIN-43; WG SKIN-32; MM SKIN-4 | |
| Settings panel, Scope set (default) | Stock look under every skin in every addon | PM SKIN-20; PC SKIN-6; QC FSKIN-8 | |
| Settings panel, Scope cleared | Untick Ignore settings panel: headings, marks, scroll arrows, tooltip bodies and the delete confirmation wear the skin. Tick it again: stock, with no reload | PC SKIN-30, 31; PM SKIN-33, 34, 35; AM SKIN-42; KC SKIN-42; CM SKIN-36; MM SKIN-36; QC FSKIN-9; ST PROFILE-3 | |

## 5. Addon by addon

### LibKa0sSkinTester

| ID | Do | Pass | Result |
|---|---|---|---|
| SHOW-34 | Values section: Ka0s Default, Azeroth, WoW Default, Obsidian | BarBorder line reads the stored three, then "Solid, shown true, 1 thick", "Blizzard Tooltip, shown true, 2 thick", then the stored three | |
| SHOW-35 | Library widgets: hover the HoverArt sample under Ka0s Default, then Glass | The client's wash, then `list.hoverArt`, desaturated | |
| SHOW-36 | Click every card with Textures, Values and Panels in view | Each non-default skin's bar track, glow swatch and cover dim are its own. Ka0s Default's did not move | |
| SHOW-30 | HUD faces: Ka0s Default, Azeroth, Obsidian, High Contrast | Numbers, label and bar change color; shadow line reads none, then 1, -1, then 2, -2 on High Contrast | |
| SHOW-31 | Overlays: read the marks, pick Azeroth | Info mark, green tick and a line's mark draw and follow the skin. Fail: a blank or client icon | |
| SHOW-32 | Obsidian: Overlays, Values, Faces and widths | The samples tell the truth: Ka0s Matte bar, skin's icon edge, every readout right | |
| SHOW-33 | Overlays in Azeroth; hover the drag handle on Library widgets | Strip icon takes the tint, tooltip title the skin's title color | |
| SHOW-9 | Hover "Hover me", click the dropdown, click tabs | Tooltip in the skin's background, border and text colors; skinned menu; tabs move | |
| SHOW-28 | `/st show` in Obsidian, Controls' dropdown rows | Five captioned dropdowns, no LSM30 cell, first two wear Obsidian's fill and edge | |
| SHOW-29 | Library widgets: drag the corner box, scroll, move window, close, reopen, Escape mid-drag | Resizes and stays in its cell; first size back on reopen; grip still works | |
| PANEL-5 | Untick Ignore settings panel, Obsidian, Sample controls | One heading over the sample rows with their skin companions, all in the skin | |
| PANEL-13 | Sample controls: untick the font, texture and border companions | Five pickers, each previewing its entries | |
| PANEL-14 | Sample controls: open the font and border rows, under Obsidian then Glass | Both pull-outs wear the skin with a preview on every row, rows line up | |
| PANEL-15 | New profile, Obsidian, Sample controls; then pick Glass | Companions ticked, pickers gray showing the skin's values; swatch stays live; they follow the switch | |
| PROFILE-3 | Scope cleared, Obsidian, Profiles, Delete a Profile; repeat with Scope set; raise another addon's Ace dialog | Skinned, then stock, then stock for the other addon. Nothing else on the page moved | |

### QuickComms (rest)

Done above: ANIM-12, ANIM-17, ANIM-18, PLOOK-1 to 11, LAYER-6, LAYER-7.

| ID | Do | Pass | Result |
|---|---|---|---|
| ANIM-1 | [Old] Open and close a dial by key on your own profile | Turns and grows over 0.2 s, turns and shrinks over 0.2 s, about the dial's center | |
| ANIM-2 | Shine and glow on, open and close slowly at 0.3 s on two skins | No pop at landing, no missing slice edges, no double image | |
| ANIM-3 | Fade, Scale in and fade, Fan, None at 0.5 s and 2 s | Open and Close each offer the same 20 entries, no Scale and fade; Duration hidden on None; Pad page has no Animation tab | |
| ANIM-4 | Set Close to None, then Open to None | Each changes that one thing on that one dial | |
| ANIM-5 | In combat, tap the key and click a slice within 0.1 s; Escape on the next open | Line goes out at once, the slice stays bright and pulses; Escape is a plain collapse | |
| ANIM-6 | Spam the key, in and out of combat | Reverses with no jump, ends fully opaque or gone | |
| ANIM-7 | `/console taintLog 2`, run ANIM-5 and 6, read `Logs\taint.log` | No QuickComms entry, no blocked popup | |
| ANIM-8 | `/qc disable` mid-animation, or start a perf capture | Nothing stays on screen; `/qc enable` brings it back whole | |
| ANIM-9 | Preview as… on; edit a setting | Preview dial plays its open; rebuilds with no flicker | |
| ANIM-10 | Dial open, Alt-Z twice, watch a cinematic | Nothing plays out or back; it returns whole; next real close and open play | |
| ANIM-11 | `/qc toggle` a pad, in and out of combat, Fade on Mouseover | Shows and hides at once, no copy drawn | |
| ANIM-13 | The four scale styles | Grow or settle about the center; text sharp and whole | |
| ANIM-14 | Spirals, Orbit, Shatter, rings of 4 and 8 | Each slice turns as one, no gap inside a slice; icons and labels upright | |
| ANIM-15 | Burst, Stagger pop, Pop at 2 s | Small overshoot, no snap; text overshoots with the art | |
| ANIM-16 | Drop; Slide with each Direction, Open and Close | Bounces to rest; direction row only on Slide; text moves with the art | |
| ANIM-19 | Flash | Soft bloom, gone at landing, no square edge | |
| ANIM-20 | [Old] A profile that ran this branch: one dial on the spirals, one on Scale and fade 0.7 s, one with other picks | First shows Rotate and scale 0.2 s both ways, second Scale in and fade 0.7 s, third keeps its picks | |
| LAYER-8 | Key-opened dial: click a pad, the settings, the world in combat, the preview window | Dial closes and the pad does not send; preview window takes its click | |
| LAYER-9 | `/qc skin` with a pad in the upper middle; first-run picker too | Picker draws over the pad and clicks | |
| FSKIN-1 | New profile, Ka0s Default, pad and dial | Did not move, but for the named buttons and shine strength | |
| FSKIN-2 | Obsidian, Azeroth with a pad up | Window fill and edge, header text, bands, buttons all change live | |
| FSKIN-3 | Same, a dial open and paged | Slices, hub, pointer, arrows, pill, dots, labels change; in combat at combat end | |
| FSKIN-4 | High Contrast, Obsidian, Ka0s Default; Ignore fonts; untick Use the skin's shadow | Shadow 2 px, 1 px, black 1, -1; stored shadow under Ignore fonts; box decides when unticked | |
| FSKIN-5 | Azeroth, Glass, High Contrast; untick texture and shine boxes | Texture and shine follow as listed; unticked draws your look | |
| FSKIN-6 | Untick Use the skin's color on Background, pick red, switch skins; Hub border under High Contrast | Red stays; no swatch grays; Hub border size grays only under a skin's real border | |
| FSKIN-7 | [Old] Log in on a profile with your own colors, reload, untick a box | Follows the skin once; colors kept behind boxes; unticked stays through reload, Defaults, profile switch | |
| FSKIN-8 | Any non-default skin | Class colors, glyph colors, game icons and send flashes keep their meaning; panel stock under default Scope | |
| FSKIN-9 | Scope cleared on Azeroth; tick it back | Ka0s marks in the skin's tint, stock on tick; tooltip titles in the title color on any skin | |
| FSKIN-10 | Azeroth, open and close a dial, then Fan | The animation copy wears the skin, no flash of Ka0s Default | |
| FSKIN-11 | First-run picker's eye over a pad | Each pick repaints pad and dial; close puts them back | |
| FSKIN-12 | Window: Use the skin's border, your style at 4. Obsidian, High Contrast, Azeroth, WoW Default, WoW Midnight; untick | Yours under Obsidian; the skin's under the four; yours when unticked; Ka0s Default with no pick has no band edge | |
| SKIN-5 | Pad and dial up, every skin, no reload | Labels redraw in each skin's HUD face | |
| SKIN-6 | Pad, Header: the Use the skin's boxes on a non-default skin | Each box hands over as written; under Obsidian the border rows stay live | |
| SKIN-11 | Skin tab: Font and Texture overrides, then back | Ticked blocks take them, unticked keep their pick, the console stays mono | |
| SKIN-12 | Non-default skin, give Buttons its own face, tick Ignore fonts | Windows, settings and the HUD go to their own faces, colors kept | |
| SKIN-13 | EllesmereUI on | Skin source offers it; repaints live | |
| BUTTON-1 | New pad; Pad, Buttons: size, color, border rows | Fuller look; each row does what it says | |
| SHINE-1 | New pad; each Shine look | No shine on a new pad; each look draws | |

### PartyFrameEnhanced (rest)

Done above: SKIN-25, SKIN-38, the three Show border rows.

| ID | Do | Pass | Result |
|---|---|---|---|
| INSTALL-4 | Clean load on the vendored library | No Lua error. The check still names v1.84.0's minors; it was reopened by the re-vendor | |
| SKIN-1 | [Old] Tick Show border on Target Frames only, update, log in under Ka0s Default | Ka0s bar and Prototype text. Your colors and shadows stop drawing, as ruled. Sizes unchanged | |
| SKIN-4 | Every skin, HUD showing | Every bar and text redraws, no reload | |
| SKIN-5 | Untick font, texture and border companions on Target Frames, switch skins | That section keeps your pick, others follow | |
| SKIN-24 | Ka0s Default, tick Ignore fonts | HUD text returns to each section's Font | |
| SKIN-27 | New profile, Cast Bars, Text | Font flags reads From skin; the Font outline setting decides the outline | |
| SKIN-32 | New profile, Ka0s Default | Orange, green, lighter green, black 0.6 and white as before, no shadow | |
| SKIN-33 | `/pfe unlock`, Obsidian, Azeroth, High Contrast | Plain fill and text change on cast, target and pet | |
| SKIN-34 | Obsidian: channel, empowered, uninterruptible, interrupted; NPC reactions; class color | Each keeps its meaning color | |
| SKIN-35 | Azeroth, High Contrast, Ka0s Default; Ignore fonts; untick shadow | Skin's shadow, heavier, none; stored row decides | |
| SKIN-36 | Glass; then the cast icon on each skin; hide the icon; click a click-to-target frame | Shine ends with the fill. 2 px icon edge follows the skin and hides with the icon. Frame still clicks | |
| SKIN-37 | [Old] Own color, shadow, Thick outline; update, reload, relog, Defaults | Follows once; colors back on untick; unticked survives other pages' Defaults | |
| PANEL-8 | Cast Bars tabs | Five tabs as written, no Border tab | |
| UNIT-9 | Target Frames, tick Show border, pick a style, mark a target | Skull draws over the edge; same on Pet Frames | |
| LAYER-2 | Size 12 border on all three | Texts, spark, shield and marker draw over the border | |

### DpsRace (rest)

Done above: SM-DR-TA17, SM-DR-FS1 to FS4.

| ID | Do | Pass | Result |
|---|---|---|---|
| C23 | Open the Share channel menu | Skinned Ka0s menu, right entries grayed | |
| SM-DR-SK2 | [Old] Note your picks, install, open the HUD and Results | Ka0s face and bar under Ka0s Default, boxes ticked, sizes as noted | |
| SM-DR-SK9 | Azeroth, race running: untick Live figures' color, change size and color; Ember; re-tick | Your size and color stay; the face follows; re-tick follows the skin | |
| SM-DR-SK13 | Ember: hover cells and a spell row; right-click a run; Delete | Tooltip lines in Ember, skinned menu, game's popup | |
| SM-DR-CH7 | Toggle chart and pace bar mid-race; change their rows | Each lands on the next redraw | |
| SM-DR-BS3 | Open Bar texture and Border style on the bars | Previews; border rows live under None skins | |
| SM-DR-BS5 | Raise background opacity, set a border, on the seven bars | Fills the whole length, border surrounds it | |
| SM-DR-BS7 | Obsidian, Glass, High Contrast on defaults | Blue bars keep their hue; textures and tracks follow; a skin's border draws | |
| SM-DR-FS5 | [Old] Custom Live figures color, Spell text shadow, a bar border color | Boxes ticked, swatches hold your values, unticking brings them back and it holds | |
| SM-DR-FS6 | Fresh profile, Ka0s Default, `/dr sim` | Gray figures, white spell text, shadows, green and red clocks, blue bars as before | |
| SM-DR-FS7 | HUD running: Ember, Glass, High Contrast | Text and shadow follow; clocks and bars keep their hues | |
| SM-DR-FS8 | Use class color on Spell text, chart background, a bar border | Class color under every skin | |
| SM-DR-FS9 | Untick Font shadow with its skin box ticked, tick Ignore fonts | Stored shadow answers; color follows | |
| SM-DR-FS10 | Right-click a Runs row, Share, Ignore for late casts, Flags, Usage edit, result card's Share | Skinned menu at the pointer, clamped; clicking a title leaves it open | |
| SM-DR-FS11 | Spell icons on HUD, detail, chart, compare, timeline | Each wears the skin's icon border; hides with Show spell icons off | |
| SM-DR-FS12 | Narrow Results until Back shows; scroll a long Runs list | Arrow wears the icon tint; scroll bar has a faint track | |
| SM-DR-FS13 | Test strip under Ember | Icon takes `icon.tint` | |
| SM-DR-FS14 | Ember, custom Bar text: a lost run's dash beside figures, scroll | Dash stays muted gray at full opacity, figures keep bar text color | |
| SM-DR-FS15 | Fresh profile: result card and detail on each skin | Ka0s Default's washes and dim unchanged; others their own | |
| SM-DR-FS16 | Spell bar border: your style, thickness 2. Ka0s Default, Ember, then the four | Yours under None skins; the skin's under the four | |
| SM-DR-FS17 | Glass; untick texture on Spell bars | Gloss on rows, chart and pace bar; plain when unticked | |

### AbsorbTracker

| ID | Do | Pass | Result |
|---|---|---|---|
| SKIN-1 | [Old] Give Player its own look on two profiles, update | Ka0s texture, no border, Prototype; see the check for what stays | |
| SKIN-5 | `/at unlock`, every skin | Fill and background take each skin's texture, no reload | |
| SKIN-6 | Untick texture and border companions | Pickers wake and draw; tick returns the skin | |
| SKIN-24 | [No lib] Rename libs aside | No error, no picker, stored picks draw | |
| SKIN-25 | `/at get`, `/at set skin.skin`, `/at diagnostics` | Get true, set repaints, bad name refused, `[Media]` lines right | |
| SKIN-35 | New profile, Ka0s Default | Blue fill, gray background, white number, no shadow | |
| SKIN-36 | `/at unlock`: Obsidian, Azeroth, High Contrast | Fill, number, background and border change and differ per skin | |
| SKIN-37 | Azeroth, High Contrast, Ka0s Default; Ignore fonts | Shadow, heavier, none; stored decides under Ignore fonts | |
| SKIN-38 | Appearance, Player: untick a companion; tick Use class color | Swatch draws at once, never gray; class color beats the companion | |
| SKIN-39 | [Old] Own colors, shadow, THICKOUTLINE; update | Follows once; comes back on untick; second profile moved too | |
| SKIN-40 | Glass; other skins; Glass with texture unticked | Shine on the fill's top half, ends with the fill; none elsewhere | |
| SKIN-41 | Ka0s Default with a style, Azeroth, Obsidian | Yours draws, Azeroth's 1 px Solid replaces it and rows gray, yours back | |
| SKIN-42 | [Old] Profile that never picked a border; one that picked another style | No edge; the pick stays and draws | |
| MIGRATE-2 | Log out, read SavedVariables; `/at debug on` | `schemaVersion = 9`, `[Init]` reads schema v9 | |

### AuraMaster

| ID | Do | Pass | Result |
|---|---|---|---|
| SKIN-1 | [Old] Two profiles on the previous build, full restart, Ka0s Default | Ka0s bar and the HUD face in both | |
| SKIN-4 | Bars, icons and Text containers, every skin | Fill, background and strings redraw, no reload | |
| SKIN-9 | Bars container: untick Use the skin's texture, font | Pickers wake, your pick stays over a skin switch | |
| SKIN-31 | [Old] Your three `PLYR TXT` containers on Ka0s Kait | They draw the skin's face first, as ruled. Untick Use the skin's font: Ka0s Kait and the glow return | |
| SKIN-35 | New profile, Ka0s Default | Blue fill, half-black background, white text, 1 px black icon borders, gold label | |
| SKIN-36 | Obsidian, Azeroth, High Contrast; WoW Default on laid-out icons | Colors and borders change. A live switch to WoW Default keeps a flat border until `/reload` | |
| SKIN-37 | Azeroth, High Contrast, Ka0s Default; Ignore fonts; untick shadow | Skin's, heavier, none; stored decides | |
| SKIN-38 | Bars, Icons, Text and Layout boxes; a target or focus container on an NPC | Boxes present; untick moves only that element; a class toggle with no class follows the skin | |
| SKIN-39 | [Old] Own colors, shadow, THICKOUTLINE, glow; update | Follows once; comes back on untick; survives reload and other Defaults | |
| SKIN-40 | Text glow on Ka0s Default, another skin; untick color | Black ring, skin's glow, your color. Warning tints do not move | |
| SKIN-41 | Glass with bars; in combat on a dummy `/am set skin.skin ka0s` and back | Shine drains with the fill both ways; no Lua error or taint on the combat switch | |
| SKIN-42 | Scope cleared, Azeroth: Container values, spell lists, overlap line | Follow the skin; stock with Scope set | |

### KickCD

| ID | Do | Pass | Result |
|---|---|---|---|
| SKIN-2 | [Old] Two profiles with own picks, install | Reset runs once, picks kept behind boxes | |
| SKIN-5 | `/kcd unlock`, every skin | Grids, cast bar and labels repaint, no reload; meaning colors stay | |
| SKIN-7 | Azeroth: the Use the skin's boxes | One each, picker gray when ticked | |
| SKIN-36 | [Old] Own HUD fonts before installing | Draw the skin's face first, as ruled; unticking brings yours back | |
| SKIN-37 | `/kcd unlock`, all ticked, Ka0s Default then each skin | Every pixel as before on Ka0s Default; each skin its own colors, glow, background and icon border | |
| SKIN-38 | Azeroth: the new boxes | Fifteen per unit, ticked, swatches stay live | |
| SKIN-39 | [Old] Loud colors, THICKOUTLINE, shadow on two profiles | Follows; flags From skin; colors kept | |
| SKIN-40 | Ka0s Default, Obsidian, back; untick shadow on the label | None, black drop shadow, gone; label keeps yours | |
| SKIN-41 | Glass, `/kcd sim`, both cast states; untick texture on Interruptible | Shine ends with the fill; that state goes plain and stays plain | |
| SKIN-42 | Spells, Scope set then cleared on Azeroth; open another addon's icon list | Blizzard marks, Ka0s marks, Blizzard back; other addon untouched | |
| GRID-10 | Change glow type, glow color and text mid-cooldown | Applies at once; glow color needs its box unticked | |
| LABEL-8 | Untick color, pick a bright one, switch Attach to | Text changes, color stays | |
| PANEL-33 | Units, Icons tabs | Layout as written | |
| PANEL-34 | Units, Cast bar tabs | Layout as written | |
| DEGRADED-16 | [No lib] `/kcd unlock` | Stored picks, client's font and bar since the Ka0s media is missing | |

### ConsumableMaster

| ID | Do | Pass | Result |
|---|---|---|---|
| SKIN-1 | [Old] Note the look, update | No edge on the bar, 2 px white button edge, Prototype, on purpose | |
| SKIN-2 | WoW Default, untick border; Labels untick font | Rows wake, your style or none; your pick or Prototype | |
| SKIN-4 | Unlocked, flyout open, nine skins | Edges and faces redraw, no reload | |
| SKIN-6 | Scope cleared, each skin, walk the pages | Every row wears the skin | |
| SKIN-23 | [No lib] | No picker, no error, stored styles and colors | |
| SKIN-25 | Fresh profile, Labels | Font flags From skin, first in its list | |
| SKIN-31 | New profile, Ka0s Default | Backdrop, white edges, gold labels, stack counts, flyout as before | |
| SKIN-32 | Obsidian, Azeroth, High Contrast | Labels, counts, fills and edges change, no reload | |
| SKIN-33 | Azeroth, High Contrast, Ka0s Default; Ignore fonts; untick | Skin's, heavier, none; Font shadow decides | |
| SKIN-34 | The four pages on Azeroth | Each swatch has its box; class color beats it | |
| SKIN-35 | [Old] Own colors, shadow, Thick outline | Follows; `skin.fullSkinReset = true`; colors back on untick | |
| SKIN-36 | Scope cleared, Azeroth: Macros, Stat Priority, Buttons; drag a row | Ka0s marks in the skin's colors, on the carried copy too | |
| SKIN-37 | Ka0s Default new profile; `/cm set macroBar.barBorderStyle Blizzard Dialog` | No edge, then that edge at your thickness; a skin's real style wins | |
| SKIN-38 | Stack count on Ka0s Default, Obsidian, Ignore fonts | Same pixels; skin's shadow; own face | |
| INSTALL-5 | Edit SavedVariables as written | Flags read None, no outline | |
| PROFILE-2 | New profile `Alt` | Migration lines as written | |
| PROFILE-5 | Switch back, read SavedVariables | No second migration; `schemaVersion = 6`, `skin.fullSkinReset = true` | |
| BAR-2 | Macro Bar's seven tabs | Row counts as written | |
| BAR-4 | Border blocks | Rows and gray rule as written | |
| BAR-12 | Bar and button appearance | Each row responds | |
| BAR-13 | Labels tab | Rows as written | |
| BAR-29 | Round-trip a color through the picker and CLI | Same channels after `/reload` | |
| BAR-30 | Delete channels in SavedVariables | No error, one answer | |

### MultiMeters

| ID | Do | Pass | Result |
|---|---|---|---|
| SKIN-28 | New profile, Ka0s Default, compare with the last build | Numbers, labels, shadows and tooltip backdrop as before, but for the named changes | |
| SKIN-29 | Test mode, three skins | Numbers, labels and tooltip text change; class fills stay | |
| SKIN-30 | Azeroth, High Contrast, Ka0s Default; Ignore fonts; hover a world unit | Shadows as written; a world tooltip is not left changed | |
| SKIN-31 | The companions; untick one; set Class mode | Swatch draws at once; modes come first | |
| SKIN-32 | [Old] Own colors, THICKOUTLINE; update, reload, swap, Defaults | Follows once; unticked stays | |
| SKIN-33 | Glass; mid-pull | Shine ends with the fill; no Lua error with secrets | |
| SKIN-34 | Each skin; untick boxes; WoW Default mid-pull | Band and icon border follow; none on an empty row; no error | |
| SKIN-35 | Segment control out of combat; mid-pull; hide with the menu open | Skinned menu with title and divider; client's menu mid-pull | |
| SKIN-36 | Scope cleared: Columns, drag a block; ticked | Ka0s marks; client's art when ticked, carried copy too | |
| SKIN-37 | Each skin at minimum width; untick alignment | No overlap with the fight name; Export band as tall as the console's | |
| SKIN-38 | Azeroth, WoW Midnight; untick font; Ignore fonts | Bold title face; picked face | |
| SKIN-39 | Ka0s Default, Obsidian; High Contrast by eye | None, then stripe and marker. Look at High Contrast too: its stripe is opaque and the check does not walk it | |
| SKIN-40 | Show border, style, thickness 3 on each kind of skin | Yours under None, the skin's under a real style | |
| WIN-1 | Hover the title bar | Seven controls; close turns red under the pointer in Skin modes | |
| WIN-49 | Beside DpsRace's HUD | Title matches | |
| PANEL-54 | Header page | Rows as written | |
| GRID-25 | Click the segment control | Skinned menu out of combat | |
| SKIN-2 | Ka0s Default: export, console, perf, sim, settings, tooltips | Colors as before | |
| SKIN-4 | Two windows, every skin | Chrome repaints, no reload | |
| SKIN-5 | Obsidian: untick companions | That surface goes back to its pick | |
| SKIN-11 | Export modal, three skins | Wears the skin; 30 px band, rows 4 px lower | |
| DEGRADED-11 | [No lib] | The pre-skin look, no error | |

### DropWatcher

| ID | Do | Pass | Result |
|---|---|---|---|
| SKIN-37 | Fresh client start, `/dw sim` | No Lua error; Steps band 30 high, and the look changes it lists | |
| SKIN-38 | New profile, Ka0s Default, `/dw test` | Flat black icon border, #19FF19 and #3FC7EB glows, soft black table shadow | |
| SKIN-39 | Azeroth, High Contrast, Ka0s Default; Ignore fonts | Compare the offset: skin's, 2, -2, 1, -1 | |
| SKIN-40 | Two non-default skins, `/dw test` | Main glow and icon border take each skin's own; off-spec follows `sem.warband` | |
| SKIN-41 | Window and Alerts boxes; untick; Use class color | Swatch draws at once; class and quality colors win | |
| SKIN-42 | [Old] Own colors, shadow off, Thick outline; update, reload, Defaults | Follows; comes back; stays | |
| SKIN-43 | Ka0s Default, then another skin | Backing, 0.7 idle tab, column band, footer band, white row wash, also from a cell inside | |
| SKIN-2 | Ka0s Default: `/dw test`, both tabs and layouts | Every color as before, with the listed changes | |
| SKIN-14 | Every skin, `/dw test` | Icon border takes each skin's style and thickness | |
| SKIN-30 | Tables block; a profile that never touched them | Rows as written; tables as before | |
| GLOW-9 | Untick the skin's color, pick a red | Your swatch draws; class color as written | |

### BankLedger

| ID | Do | Pass | Result |
|---|---|---|---|
| SKIN-1 | Ka0s Default: walk windows | As before, with the listed changes only | |
| SKIN-35 | Ka0s Default `/bl show`, click tabs | Backing, gold underline, faint rule, band edge to edge | |
| SKIN-36 | Ledger, session, Export | All 30 high, centered, close unclipped | |
| SKIN-37 | Ka0s Default, Obsidian | Grips and arrows stay, then take the skin | |
| LEDG-36 | Export to CSV | Library close mark, 18×18 on a 30 px bar | |
| DIAG-7 | Open the console and Copy box | Same edge, 18×18 close on a 30 px bar | |
| DEGRADED-16 | [No lib] Open the ledger | Gold and gray tabs, 2 px underline, no backing, click moves both | |

### LootHistory

| ID | Do | Pass | Result |
|---|---|---|---|
| SKIN-1 | Ka0s Default: walk tabs | As before, in its face and bar | |
| SKIN-43 | Ka0s Default, Azeroth, Ember | Tabs and header bands follow, no reload | |
| SKIN-44 | Timeline: Total only on three skins | Thin edge; tick follows a click anywhere; hover still works | |
| SKIN-45 | Right-click a row; grip; Export title | Gray marks, then Azeroth's tint; labels readable | |
| SKIN-46 | Azeroth: scroll bars, minimap tooltip, `/lh test`, `/lh sim` | Chevrons; tooltip colors; tinted mark; 30 high Steps band | |
| HIST-43 | Ka0s Default: `/lh show`, Export | As before, with the tab backing | |
| HIST-44 | Ka0s Default: History | As before | |
| INS-23 | Ka0s Default: Insights | As before, but for the scroll bars' step buttons | |
| LED-13 | Ka0s Default: Holdings | As before, with the header band | |
| TL-18 | Ka0s Default: Timeline | As before, with the Total only box | |
| DEGRADED-15 | [No lib] `/lh show` | No backing, gold active, small gold tick | |

### WhatGroup

| ID | Do | Pass | Result |
|---|---|---|---|
| SKIN-1 | Ka0s Default, `/wg test` | As before, with the six listed changes | |
| SKIN-10 | High Contrast, Azeroth | What stays Blizzard's stays | |
| SKIN-32 | `/wg test` on a mapped dungeon, every skin | Title centered on one band; icon edge each skin's own, 1 or 2 px | |
| SKIN-33 | High Contrast minimap tooltip; `/wg debug`; Scope cleared | Tooltip colors; 30 high console; headings and chevrons in the skin | |
| POPUP-11 | `/wg test notify` | Regions in place, title 2 px higher; bar drags | |

### PremadeGroupsFilterExtension

| ID | Do | Pass | Result |
|---|---|---|---|
| APPLY-17 | Server regions dropdown | Any heads the Ka0s menu, divider under it; ticking as written | |
| APPLY-19 | Hover every option and each menu row | Each has a tooltip | |
| SKIN-17 | Non-default skin: panel states | Grays as written | |
| SKIN-43 | Open the panel's dropdowns; a 32-letter preset name | Ka0s menu; the long name stays on one line | |
| SKIN-44 | Ka0s Default, Ember: tooltips and boxes | White name over gold body; 0.9 gray boxes | |
| SKIN-45 | Scope cleared: settings pages; minimap tooltip | Marks show, none blank; tooltip follows | |
| SKIN-46 | A listing with an unknown realm | Gray `?`; Ember's disabled color on the next repaint | |

### PanelMaster

| ID | Do | Pass | Result |
|---|---|---|---|
| SKIN-20 | Azeroth, High Contrast, Scope set: tooltips, popups, chat, minimap | Client's frame, yellow words, stock popups | |
| SKIN-32 | Open every page and editor tab, Obsidian, both Scopes | No Lua error, no blank mark | |
| SKIN-33 | Scope cleared: hover Panel name, Ka0s Default then Obsidian | Yellow, then the skin's emphasis; yellow on tick | |
| SKIN-34 | Scope cleared, Obsidian: Size and position | Headings in the section heading face | |
| SKIN-35 | Scope cleared, Obsidian: delete a profile; repeat ticked | Skinned box, then stock | |

### PrettyChat

| ID | Do | Pass | Result |
|---|---|---|---|
| RV-85 | `/reload`, every page, `/pc debug`, copy window, `/pc skin` | No library error, every mark draws | |
| SKIN-6 | Azeroth: Categories notes, list hover | Muted color with Scope cleared; hover body follows | |
| SKIN-28 | Ka0s Default, Obsidian: console and copy window | 30 high, the one expected Ka0s Default change | |
| SKIN-29 | Minimap tooltip, Ka0s Default then Obsidian | Unchanged, then the skin's colors | |
| SKIN-30 | Scope cleared on Obsidian | Tooltip body, Slash Commands rows and chevrons in the skin | |
| SKIN-31 | Scope cleared: delete a throwaway profile; ticked; a non-Ka0s addon | Skinned, stock, stock | |
