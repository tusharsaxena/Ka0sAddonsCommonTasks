# The owner's rulings, 2026-11-10

The request: "Lets start with the migration of the next addon. Up next, i want the QuickComms addon ported to
Forever. Grill me on how i want core differences between Retail and Forever handled for this. Also build this
feature while we're at it for both retail and forever: https://github.com/tusharsaxena/QuickComms/issues/15. On a
related note, remove the Sample controls page from the SkinTester Settings panel; also make it ignore settings panel
for the skinning; only skin the SkinTester window." Plus the standing run guidelines (owner-run-guidelines).

QuickComms#15 is titled "Support emotes" and every other field is TBD.

## Answers, verbatim

| # | Question (short) | Answer |
|---|---|---|
| R1 | Which content kinds exist on Forever beyond open world, dungeon and raid? | "Battlegrounds, Raids (new list of raids specific to Forever)" (arenas, Mythic+, delves, scenarios not ticked) |
| R2 | Where do the Forever instance, battleground and arena ids come from? | "Map IDs + probe (Recommended)" |
| R3 | Spec and Role rows on Forever? | "Do #3 [keep both, Forever spec ids, work out role from it], and build out the function to save spec and determine role as a reusable LibKa0s module" |
| R4 | Send path on Forever? | "Same secure path (Recommended)" |
| R5 | What tells a tank from a DPS on Forever? | "Use a combination of #1 [talents, the tree with most points, player can override, saved per character] and #3 [whatever the spec API returns, saved per character]" |
| R6 | What does an emote callout do? | "Both kinds (custom /e and built in emotes). Also build a seed list of common emotes that can be used in the open world as well" |
| R7 | Chat line and emote on one press? | "One action per callout, but add a GH issue to do both. Also GH issue to use the ping system, and add target raid markers. A message can combine all" |
| R8 | SkinTester's Ignore settings panel? | "Default on, keep toggle" (so the showroom's panel samples stay skinned, as the option said) |
| R9 | (mid-run) DpsRace | "mark dpsrace as Retail only - there are no training dummies in forever so this makes no sense", then "make that change in the forever port documentation and in ADDONS.md and anywhere else it may be needed". Done as `QFE-DPS` in DpsRace (TOC gating, README, DEPENDENCIES, scope) and WowAddonStandards (roster), plus amendments to the step-5 classification and the port design |

## Calls Claude made after the questions (the owner said to decide the rest)

- C1. Role resolution order: the player's override, then the role the group assigned, then (Forever only) the
  talent group with the most points spent mapped through a per-class seed, then the spec API's role. The talent step
  comes before the API on Forever because one spec per class makes the API's role class-wide, wrong for hybrids.
- C2. The Forever spec list is read from the client at run time (`GetNumSpecializationsForClassID` /
  `GetSpecializationInfoForClassID`, both present on Forever), not seeded. Retail keeps its seed.
- C3. On Forever the When editor hides the Mythic+, delve, scenario, arena and housing content values, the key-level
  row and the difficulty row (Forever's difficulty ids are unknown until probed). The M+ and Arena built-in groups are
  not seeded on Forever.
- C4. The probe writes into QuickComms' own SavedVariables (`global.probes`), never a new SavedVariables global.
- C5. The emote seed is one list for both clients: Blizzard's `EmoteList` and `TextEmoteSpeechList`
  (`ChatEmoteConstants.lua`) are byte-identical on Forever 1.60.1 (70862) and Retail 12.1.5 (70783).
- C6. The three follow-up issues (R7) are filed on QuickComms: combined actions, pings, raid target markers.
