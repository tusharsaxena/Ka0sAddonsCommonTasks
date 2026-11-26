# Addendum A1: more SkillMaster changes (2026-11-26, during M2)

The owner, verbatim: "Some more changes in skill master. [Image #27] [Image #28] - Detached windows, when joined,
are no longer resizable. [Image #29] Allow detaching sub categories (e.g. Alliance, Othert here). [Image #30] Or
any of the nested sub categories here. [Image #31] or sub categories here. [Image #32] Rework the journal: Track
reputations, and currencies gain/loss here as well; add filters for all column headers; Check if any other rework
for journal is required. ASdd it to current ongoing work. Also go ahead and merge everything as soon as its ready
to merge. At the end of all the tasks in the workflow, give me a summary of what all has changed and what i need
to smoke test (give me details, dont ask me to check a MD file)."

Screenshots: `inputs/27.png` and `28.png` (two detached blocks, Primary Professions and Reputations, then joined into
one "Primary · Reputations" window with no resize grip), `29.png` (Reputations window: Alliance, Steamwheedle Cartel,
Other), `30.png` (Statistics: Character › Wealth, Consumables, Reputation, Gear; Player vs. Player; Combat),
`31.png` (Currencies: Player vs. Player, Professions & Tradeskills), `32.png` (Journal, Log tab: Date, Time,
Skill, Change, Zone; Honor Points rows already appear; right column: All time picker, Skill-ups, ETA to cap, New
session, Clear log).

**Merge rule from here:** each repo merges as soon as it is built, reviewed and green (the owner's go-ahead
above). SkillMaster round 5 (R5-SM-01..07 + review) merged at b6ba05b before this addendum was built; these items
go on a new `feat/2026-11-26-owner-feedback-round5` branch cut from that master.

| id | item | lead call |
|---|---|---|
| R5-SM-08 | A window made by joining detached blocks can be resized again | The joined window gets the same resize grip and size memory as a single window. Fix the cause and add a test (join two blocks → the grip is there and resizing works; unjoin → each keeps its own). |
| R5-SM-09 | Detach any sub-category: reputation headers (Alliance, Steamwheedle Cartel, Other), the Statistics categories at any depth (Character, Wealth, Consumables, Player vs. Player…), currency headers | Every foldable sub-header gets the same detach mark the block headers have. A detached sub-category is its own window like a detached block (moves, joins, remembers its place and fold state, survives /reload), and it leaves its parent while detached. Its key is stable: faction header id or name, statistics category id, currency header name. |
| R5-SM-10 | The Journal tracks reputation and currency gains and losses | Each change becomes a log row (faction or currency, signed amount, standing change where one happens), alongside skill-ups. The existing Honor Points rows suggest part of this exists; build on it. No row for the login baseline. Saved-variable schema bump with a migration if the row shape changes. |
| R5-SM-11 | Filters on every Journal column header | Date, Time, Skill (renamed for the wider content, e.g. "Name"), Change and Zone each get a header filter (e.g. date range or day, kind: skill / reputation / currency, name, gains vs losses, zone). Filters combine, show they are active, and clear in one click. The summary column follows the filter. |
| R5-SM-12 | Any other Journal rework that's needed | The builder reviews the Journal against the new contents (reputations and currencies in Skill-ups, ETA to cap, New session, Clear log, the Alts tab) and fixes what no longer fits. Each change is listed in the report. |
