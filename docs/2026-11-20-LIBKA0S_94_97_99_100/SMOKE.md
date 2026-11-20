# In-game smoke for the LibKa0s #94, #97, #99, #100 run

Run these in the client, Retail and then WoW Forever where the addon ships both. Skill Master ships
WoW Forever only; Bank Ledger, Kick CD, Loot History, Multi Meters, PGF Extension and WhatGroup ship
Retail only. Each check's full steps and its `Result:` field are in that addon's `docs/smoke-tests.md`
on the run branch `feat/2026-11-20-libka0s-94-97-99-100`. Fill the Result there, or tell the lead and
the lead records it. Nothing here is marked passed until the owner says so.

Every addon now vendors LibKa0s v1.108.0 (test kit revision 58) and references standard v2.116.0.

## Everywhere: option defaults follow the skin (LibKa0s#97, ruling R-2)

- **Fresh profile.** A new profile's colors, fonts, outlines, shadows, borders and bar textures read
  *Use the skin's ...* ticked (or *From skin* for Font flags). Switch skins with `/<addon> skin` or the
  skin picker (Ka0s Default, then Obsidian, WoW Midnight or High Contrast) and every one of them moves
  at once, with no `/reload`. Meaning colors (class, quality, good and bad, band and role hues) do not
  move.
- **Stored picks.** On a profile saved before this build, a color or look you picked yourself keeps
  drawing and its *Use the skin's ...* box reads unticked. Values still at the old defaults move onto
  the skin once (one `[Migrate]` line with debug on); untick a box, `/reload`, and it stays unticked.
- **Font shadow.** In any font block, **Font shadow** is grayed while **Use the skin's shadow** is
  ticked, and comes alive when you untick it. Each companion row shows once, never twice, and the color
  swatches stay live.
- **Owner OVERRIDEs stay put.** For example, Aura Master's bar border and text glow stay black, Panel
  Master's panels keep the player's look, and preview stand-ins (PFE's party frame, Range Master's
  preview nameplate) keep the host frame's look under every skin.

## Footer marks (LibKa0s#94)

A footer lays out only the marks it shows. In Drop Watcher, narrow the window and check that the words
run up to the first shown icon, with no blank slot where a hidden icon would sit (FEED-112).

## Strip tooltip on a secret position (LibKa0s#99)

In a dungeon, a drag strip whose position reads secret (Aura Master, a container attached under a
parent holding auras) still shows its tooltip, centered above the nearest container whose position
reads, never at the cursor and never missing (DRAG-21).

## Callout drag strip (LibKa0s#100)

The call-out's strip reads **?** · settings · close. Combat Trail is the only addon that creates a
call-out (SM-CT-RM98, SM-CT-RM100).

## Per addon

| Addon | Checks | What they cover |
|---|---|---|
| Absorb Tracker | SKIN-47 | Font shadow is grayed while *Use the skin's shadow* is ticked, and works when unticked. LOOK-1's Font shadow step now unticks the companion first |
| Aura Master | DRAG-21, SKIN-54, SKIN-55, SKIN-56; DRAG-20 changed (its secret-strip case moved to DRAG-21) | A secret strip's tooltip above its nearest readable container. Strip edges follow a skin switch; the Spark has no skin-color row. New containers follow the skin with the bar border and text glow kept black; an upgraded profile moves once (schema v21) and keeps picked and preset colors |
| Bank Ledger (Retail) | PANEL-33, PANEL-34, SKIN-49; PANEL-7, PANEL-21, PANEL-22, PANEL-23, PANEL-28 and SKIN-5 rewritten | Row stripe and hover opacities follow the skin (0.08 and 0.16 under Ka0s Default) behind two new *Use the skin's ...* boxes; an upgrade keeps a moved slider (schema v7). Minimum quality labels take the skin's quality colors on a skinned settings page |
| Combat Trail | SM-CT-N22 to SM-CT-N26, SM-CT-H20 to SM-CT-H23, SM-CT-R31 (both clients); SM-CT-RM99, SM-CT-RM100 (Retail); re-pinned SM-CT-RM84, SM-CT-RM91, SM-CT-RM92, SM-CT-RM98 (Retail) | Lane background, GCD ticks, now line, stack and name text, HUD fight clock outline, pace line, spell-row borders, pet paw tint and every Insights bar follow the skin, and old picks survive. The race call-out takes the skin's font, outline and shadow with the owner's black 2 px glow at offset 1,1 and *Use the skin's color* off (SD-CT-DEF). Its strip now has a close X that turns the countdown off, and the gear opens the Callout tab |
| Consumable Master | BAR-45, SKIN-48, SKIN-49; SKIN-31 changed | Label block companions show once and Font shadow grays with its companion. Settings descriptions wear the skin's face on first draw. Under Ka0s Default the bar's and flyout's edge is now black, not dark gray (U-16) |
| Drop Watcher | FEED-112, SKIN-53, SKIN-54, SKIN-55, ROLLS-22; SKIN-52 amended | The footer's words use the width a hidden icon frees. The tables' Font color gets its own *Use the skin's color*. An expanded row uses the skin's selection wash, apart from hover. The Edit message box is in the skin's face and input color. The Rolls countdown bar, winner wash and `[YOU]` draw in the skin's accent |
| Kick CD (Retail) | SKIN-49, SKIN-50 | Font shadow grays with its companion; cast-bar fill and cooldown tint have no skin box (meaning colors). The charges badge's shadow follows the skin, matching the countdown |
| Loot History (Retail) | SKIN-55, SKIN-56 | The ledger reset prompt's headings take the skin's tooltip-title color. An open row menu repaints at a skin switch without reopening |
| Multi Meters (Retail) | SKIN-53, SKIN-54, SKIN-55, SKIN-56, SKIN-57; GRID-25 and GRID-35 amended (their mid-pull half is now SKIN-53) | Mid-pull the segment picker is the skinned Ka0s menu, not the client's. Custom bar color and background, classless rows and their tooltip bars and lines follow the skin; an old profile keeps a picked Custom color (v27 step) |
| Outfitter Reborn | SD1 to SD12 (Retail and Forever) | The optimize progress bar, push-button and checkbox labels, item rows, tooltip lines (outfit, Equipment Sets, categories, minimap, character tab) and the equip message take the skin's colors and faces. An uncolored glyph draws the skin's icon tint. The Outfit Bar's background block has no duplicate skin row |
| Panel Master | SKIN-45, SKIN-46 | The panel editor shows no *Use the skin's ...* box, and a skin switch leaves every panel, and a new one, as the player made it; only the unlock outline and label follow |
| Party Frame Enhanced | SKIN-44, SKIN-45 | Font shadow grays with its companion on the Text tabs. The stand-in's *(test)* mark takes the skin's muted color while the stand-in keeps the imitated frame's look. The run note also reopens INSTALL-4 (a clean load) |
| PGF Extension (Retail) | No new check: "No user-visible change, so no smoke check is added" (SD-SK-PGFE declares panel surfaces for the kit; no option default moves) | A clean load with no Lua error |
| PrettyChat | RV-108, SKIN-35 | A clean load on v1.108.0 with every mark drawn. The `/pc test` report's labels and header in the console follow the skin; chat lines keep their colors |
| Quick Comms | PREVIEW-14, PLOOK-13, THANK-13; SKIN-7 rewritten | End preview is the skin's push button (U-28). The pad body takes the skin's window gradient or art. The thank toast's text and Thank button wear the skin |
| Range Master | INSTALL-5, DRAW-6 to DRAW-10, CONT-12 to CONT-14, ANCHOR-12; CONT-10 changed | An upgrade moves untouched looks onto the skin once. The Bar dot takes the skin's border and Glass gloss; Fixed colors, outline, shadow, container border and spell chips follow the skin, with Band-mode colors kept. New companion rows, Style tiles following the Scope, the frame picker label in the skin's accent, and the preview nameplate unchanged by a skin switch |
| Skill Master (Forever) | SM-SKIN-3 to SM-SKIN-8 | Data bars take the Glass gloss; detached windows show one skin row per block. The arrow text follows a skin switch live. Tooltips read the tooltip gold and grays. Trainer popup cards get a hover wash (SkillMaster#9). Settings eye marks take the icon tint |
| Skin Tester | SHOW-57, SHOW-58, SHOW-59, SHOW-60 | The Values GetFont line, the menu cascade's submenu arrows, the face lines and the HUD face lines take the worn skin's colors |
| WhatGroup (Retail) | No new check: "no check of its own. The release moves call-outs, arrows, charts, data bars, footers and option composers, and this addon builds none of them" | A clean load with no Lua error; the library-absent popup draws as before |

## Known, not defects

Low-severity review observations you may notice in game:

- **Outfitter Reborn.** Picking white in the icon browser now stores no color and draws the skin's icon
  tint (U-22), so a pure white glyph is no longer possible.
- **Kick CD.** The charges badge draws no shadow with Ignore fonts on, which matches the countdown.
- **Multi Meters.** Under Ka0s Default the tooltip's classless spell bar is the gold accent, while the
  cell's classless fill stays slate.
- **Consumable Master.** SKIN-31's old Passed line predates U-16's black edge, so a re-run is owed.
