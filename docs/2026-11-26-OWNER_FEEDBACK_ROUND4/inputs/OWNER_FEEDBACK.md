# Owner feedback, round 4 (2026-11-26), verbatim

Given after round 3 (Item Search), the Combat Sequence, RangeMaster's band set per character and AuraMaster's preset icon
time text were merged and tried in game. Screenshots 118 to 144 were attached in the conversation and are described in
brackets.

> Combat Trail - Combat Sequence
>
> - [Image #119: the HUD in sim, Combat Sequence "No events yet."] [Image #120: the HUD in test mode, "No events yet."]
>   [Image #118: Results in test mode, "No combat sequence was saved for this fight"] Combat sequence doesnt have test mode or
>   sim mode data
> - [Image #121: Combat Sequence rows: Time right-aligned, Event, a separate icon column, Spell centered] Make all columns left
>   aligned
>   - Have the icon be a part of the spell column with one character gap between icon and spell name
>   - Make this change in DPS HUD and Results window
> - [Image #122: the HUD at its current width with space to spare] Start off with teh window at min width for new profiles
> - [Image #123: Combat Sequence headers "Time ▼ Event Spell" in plain text] Column headers should look like column headers in
>   Loot History [Image #124: LootHistory's header band: muted gold labels on a darker band, a solid ▼ sort triangle]
>   - Make this change in DPS HUD and Results window
> - [Image #125: the HUD with a large empty gap above Combat Sequence] Min height of the DPS HUD should be big enough to fit 3
>   rows of spell breakdown and 3 rows of combat sequence
>   - Default height should still be 5 rows each
>   - When dragging and resizing the HUD, it should increase/reduce # of rows in Combat Sequence and Damage Profile equally.
>     - e.g. start at 5 rows each; then resize to 4 each, then 3 each
>     - It's ok if there is an interrim - ie go from 5/5 to 5/4 to 4/4 to 4/3 to 3/3 etc
>     - should apply both reduction and increase in height (growth)
> - [Image #139: the Casts / Pet / Buffs / Debuffs chips] Make the chips hidden by default
> - [Image #140: the Combat Sequence heading's eye and detach (down-arrow) marks] Change the detach icon to something more
>   relevant (also attached icon in detahced window header [Image #144: the detached window's title bar "← ⚙ ✕"])
>   - [Image #142: ">"][Image #143: "<"] Use this from CT results window header instead
>
> DropWatcher - ItemSearch
>
> - [Image #126: Drops from: Source colored (Rare gray-blue, Elite gold), Type "Object ×4 / Creature / Container / Rare /
>   Elite"] Give a unqiue color to every type and color code  Type columns accoringly
>   - Keep Creature as White
>   - Do not color source anymore
> - [Image #127: window Recipe glyphs: two different gray "↔" glyphs, one thin, one with dotted ends] Why are there different
>   <-> icons for grey skill ups?
>   - i dont like this icon anyways - choose a thick dash instead (matches thematically with the skill up arrow) - keep the
>     grey color
>   - both in tooltip and in ItemSearch window
> - [Image #128: tooltip header "Drop Watcher" left, "🔒 Keep 65 · High" right] Move the "Keep 65" part right next to the
>   DropWatcher header
>   - [Image #129: ItemTree's badge: a filled bright-green box "🔒 Keep" with a darker-green box "108" joined to it] Make it
>     more like a badge like this
>   - Remove the High/Medium/etc confidence bit
>   - Explain to me what the 65 means her eexactly
> - Not able to capture a screenshot, but there is a flickering horizontal separator line in the tooltip
>   - [Image #130: the full Peacebloom tooltip; the hairline above "Drop Watcher"] The separator above DropWatcher is
>     flickering
>   - There is anotehr flickering line very dim - somewhere in the itemtree section
>     - this is following the same frequency of flickering as the one above the DropWatcher section (and looks the same as
>       well)
> - [Image #131: Sold by: Maria Lumere, Hula'mahi "Horde only", Selina Weston "Horde only"] Add the vendor cost
>   - Also filter out other faction vendors by default (toggleable via settings)
> - [Image #132: Quests: "! My First Alchemy Set" ... "level 10"]
>   [Quest Icon] [Quest Name] ([Quest Level])                [Giver - e.g. Odd Child - Westfall]
> - [Image #133: window Crafting row "Incense Candle", Profession "–", Skill "–"; ItemTree says "Made by Herbalism",
>   "Requires Herbalism (20)"] Why is Incense candle profession = "-"
> - [Image #134: tooltip Crafting rows "55 75 95 · Alchemy", profession name plain] Give unique colors to ll professions
>   (doesnt overlap with skill up colors)
>   - color in tooltip, and in profession column of ItemSearch window
> - [Image #135: Crafting tab, Elixir of Minor Defense, Skill "55 75 95"; the row tooltip "Your rank: 29 · Orange: sure to
>   skill up"] Lets address the skill column
>   - This recipe is still orange to me - so the skill coulmn here (and in tooltip) should reflect that somehow
>   - why is this happending?
>
> Range  Master - Band Sets
>
> - Created a new profile (SmokeTest4) on my paladin
>   - [Image #136: Band set dropdown on the paladin, "Paladin (default)" checked] correctly assigned a paladin band set
>   - Then logged on my hunter - selected the same SmokeTest4 profile
>   - [Image #137: on the hunter, "Paladin" checked, "Hunter (default)" listed] Paladin bandset is still selected
>   - My expectation - first time a character logs in to a profile...
>     - the right class specific bandset should be assigned to that character
>     - this persists through profile swaps, login attempts, etc
>     - this only changes if a user manually selects a different profile
>   - [Image #138: "Your band sets" lists Paladin, Melee / Ranged, Caster 40, Healer, Hunter (default)] Only bandsets that have
>     been assigned to a character should show up in "Your band sets"
>     - Right now it appears on new profile creation, all the shipped presets - general and shipped presets - classes
>       (relevant to characters i have) are in "Your band sets"
>     - Add this incrementally as new characters actually select that profile, rather than all of these being created on
>       new profile creation
>
> General
>
> - Combat Trail decisions: your two earlier rulings LG22 and LG27 are still owed.
>   - WHat decisions are owed? Ask me these first

The owner's run guidelines were pasted again with this batch (ask upfront, then decide; a resumable checkpointed plan; a
branch with incremental commits; push at milestones; merge only on go-ahead; clean up at the end; ultracode workflows).
