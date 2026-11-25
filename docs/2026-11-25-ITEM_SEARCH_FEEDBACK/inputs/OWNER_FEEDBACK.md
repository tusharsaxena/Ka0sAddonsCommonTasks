# Owner feedback on the Item Search build (2026-11-25), verbatim

Given after Item Search (`docs/2026-11-25-ITEM_SEARCH/`) was merged and tried in game on WoW Forever.
Screenshots 62 to 70 were attached in the conversation and are described in brackets.

> Some feedback on the Item Search build
>
> TOOLTIP [Image #62: Mana Potion tooltip with the Drop Watcher · Item Search block]
>
> 1. The Ctrl-Alt-D shortcut doesnt seem to work
> 2. Remove the magnifying glass before the DropWatcher section header
> 3. [Image #63: Medium Leather tooltip, Crafting lists about 60 recipes across Blacksmithing, Engineering and Leatherworking]
>    - have a restriction on how many items are show under each of the headers - drops from, sold by, crafting, etc - show max 5 by default but make it configurable
>      - this is only for tooltip; item search window shuld be complete
>    - by default show only professions you know (also configurable)
>      - do this for both toolti pand iteam seach window
>    - have some sort of sorting logic for every section which prioritizes showing information useful to you
>      - e.g. for crafts, prioritize recipes you know, sorted by skill up chance
>      - e.g. for drops priroitize enemies near your level range if thats possible; or nearby zones
>      - etc etc
>      - have this kind of logic both for tooltip and item search window
> 4. Isntead of colored dots for the crafting indicator, use arrows and relevant glyphs - color up arrow for recipes with skill up; something in light gray for no skill up, something in dark gray for unknow recipes
>    - do this for both tooltip and iteam search window
>
> ITEAM SEARCH WINDOW [Image #64: the window beside Drop Watcher's]
>
> 1. Title shuld include Drop Watcher
> 2. Remove the CLTRL-ALT-D text in footer
> 3. [Image #65: the item header, "Heavy Leather / Common · Trade Goods · Leather · id 4234"] Font size doesnt match up with the rest of dropwatcher - make it match
> 4. Remove recent searches - not relevant
> 5. When a "Matches" element is selected, highliught that
> 6. Clear button text is not centered
> 7. Link in chat button text is not useful - remove it - however make it so that shift clicking on the icon or item name here [Image #66: the item header] will do the same thing
> 8. Change the layout of the "results" section [Image #67: one long list with DROPS FROM, SOLD BY, QUESTS, CRAFTING headings]
>    - have a tab like interface on top which shows all the differeht section headings (e.g. drops from, sold by, quests, etc)
>    - Each tab can have its own unique column structure relevant to what it is showing - design this for me (ux mockup)
>    - Space out the columns better - you have more space available, use it
> 9. Need tooltips and mouseover highlighting and alternate row coloring everywhere in this Item Search window - following Ka0s tooltip guidelines
> 10. Need section headers and actions everywhere in item search - SkillMaster is a good example [Image #68: Skill Master's window, section headers with a chevron, gold title and filter, list and pop-out actions]
> 11. [Image #69: a drops row ending in a white → arrow] i dont like thi set waypoint arrow - change it to something better
> 12. Use TomTom or LibKa0s waypoint arrow for setting waypoints
> 13. ItemSearch window should not have a lock
> 14. Item Search window should be resizable
> 15. [Image #70: DROPS FROM list with many "Object 153462" rows] What are these Object <some number> in the drops from? This is not useful at all - if you cannot resolve it, at least filter them out
>
> GENERAL
>
> 1. Is forever-db still an optional dependency for other addons - or just dropwatcher now? Ideally it should be just dropwatcher now
>
> Lots of changes - spec this out; show me ux mockups and build this

## The owner's answer to the one question asked

- **ForeverDB in Outfitter Reborn and Skill Master:** "Remove from both". Only Drop Watcher reads
  ForeverDB after this run.
