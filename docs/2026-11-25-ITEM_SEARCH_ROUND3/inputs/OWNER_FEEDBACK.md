# Owner feedback, Item Search round 3 (2026-11-25), verbatim

This was given after the Item Search feedback run (`docs/2026-11-25-ITEM_SEARCH_FEEDBACK/`) was merged and tried in game on
WoW Forever. Screenshots 88 to 107 were attached in the conversation and are described in brackets.

> DROP WATCHER - Item Search
> [Image #88: Linen Cloth tooltip with the Drop Watcher · Item Search block above ItemTree's block] [Image #89: the Item Search window, Linen Cloth, Crafting tab]
>
> 1. Have cosnsietncy between the crafting skill up arrow in the tooltip and in the window
>    - Make it more like the tooltip, but a thick arrow
> 2. [Image #90: tooltip Crafting rows, gray boxed-minus glyphs] I dont like the gylph for crafting with no longer gives a skill - use a left-right arrow (<--> something like this) glyph instead in the same grey color
> 3. [Image #92: Crafting tab, Skill column "40 70 90 110" orange only on Learn at rows] The skill column should also include orange skill
> 4. [Image #91: Peacebloom tooltip] In the tooltip, show the skill somewhere as well (either immediately after recipe name, or a s a separate "column")
> 5. [Image #93: Crafting tab header] Sorting should also be possible by clicking on column names
> 6. [Image #94: Drops from, creature names in red, objects white] Whats the reason for the color coding of the source?
> 7. [Image #95: Peacebloom Drops from: "Peacebloom Object ×3", "School of Fish"] For gathered items, is it possible to source "node type" as a separate tab (something like "Gathered from")? Not in "Drops from" tab
> 8. [Image #96: Sold by: Zone "–" and Price "–" on all three vendors, two "can't buy"] Why is zone and price empty?
>    - Also - what does "can't buy" mean?
> 9. Pressing Ctrl-Alt-D
>    - when hovering over an item (and tooltip is shown) should open the Iteam Search window on that it
>    - when not hovering over an item should tollge showing/hiding the item search window
> 10. [Image #97: Drops from, many rows with no zone and no pin] Why do so many sources not have a waypoint entry?
> 11. [Image #98: DW "Chance ↓" thin arrow] The column sort indicator should be like the one in LootHistory [Image #99: LootHistory "Item ▼" solid triangle]
> 12. [Image #100, #101: the glyph column hugging the table's left edge] Leftmost icon column is too far tooo the left
> 13. [Image #104: window Quests "!" / "?"] [Image #105: tooltip Quests "!" / "?"] Quest icons
>     - Quests not yet picked up, use the exclamation icon instead [Image #103: the game's yellow "!"]
>     - Quests picked up and not completed, use question mark
>     - Quests picked up, completed but not yet turned in, use a green question mark
>     - Quests completed and turned in, use green check mark (not background green square)
> 14. [Image #106: the tooltip's "Drop Watcher · Item Search" title under a short accent rule]
>     - Remove the "Drop Wtahcer - Item Search" header text
>     - The separator - make it look more like this [Image #107: ItemTree's full-width thin line, "Keep 43" badge left, "ItemTree" right] - comes from ItemTree
>     - I like the "Keep/Toss" badge on top left - and addon name "Drop Watcher" on top right of that section - replicate that (but swap it around - badge on top right)
>       - Define a logic and confidence score - look into ItemTree

## The owner's answers to the questions asked after the recon (`RECON.md`)

| Question | Answer |
|---|---|
| Where missing spawn spots come from (items 8, 10) | "World coords, then Full": convert ForeverDB's base world coordinates (`spw`) to map positions, and also read ForeverDB_Full's fuller table when it is installed |
| What orange shows in the Skill column (item 3) | "Ignore this, leave it as it is": **item 3 is dropped** |
| The tooltip badge design (item 14) | "Verdict + score": Keep / Hold / Sell / Toss, a 0–100 score, a confidence (High/Medium/Low, Low never says Toss), and reason lines |
| Header sort (item 5) | "Didn't look clickable": add a hover highlight and the LootHistory-style arrow |
| What the Source color means (item 6) | "By rank, color code the type column as well" |
