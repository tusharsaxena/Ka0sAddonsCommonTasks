# Addendum: Azeroth's border (2026-10-28)

Added during execution, after `99_REPORT.md` was first written. The owner, with Loot History open in
Azeroth, Ember and WoW Midnight:

> Azeroth skin has a much thicker border than other skins (e.g. [Ember], [WoW Midnight]) make the
> border of Azeroth consistent with other skins

Azeroth drew a 3px leather edge with its 1px gold inner rule just inside it, a 4px frame. Ember draws
a 1px edge and a rule (2px); WoW Midnight a 2px gold edge and a rule (3px).

| Id | Repo | Commit | What |
|---|---|---|---|
| R5-09 | LibKa0s | `2224a8c` | Azeroth's `win.borderSize` 3 -> 1: Ember's 2px frame, the leather line outside and the gold rule inside. SkinDefs minor 13, Skin key 5.13.10.3.8.1.3. A new case holds every flat window frame (edge plus rule) to at most 3px, red on minor 12. Two stale minors in the API docs corrected on the way (the Skin document's files-and-minors row, the Options document's OptionsScroll). |
| R5-07 | LibKa0s | `b2f6ec6` | Release record `20261028-120744` (lint 0/0, 3031 passed / 2 skipped, max CCN 15); local tag `v1.78.0` re-cut onto it, not pushed. |
| R5-10 | LootHistory | `9183969` | Re-vendor; SkinDefs 13 pinned. 1788 passed / 1 skipped, lint 0/0. |
| R5-11 | LibKa0sSkinTester | `ce468f9` | Re-vendor. 486 passed / 1 skipped, lint 0/0. |

My call: 2px, Ember's frame, rather than 3px, Midnight's, because Ember is the other skin with a thin
edge and a colored rule inside it, and the owner's complaint was thickness.

## Owner smoke

| Id | Where | Expected | Result |
|---|---|---|---|
| R5-S10 | Loot History in Azeroth, then Ember and WoW Midnight | Azeroth's frame is a thin leather line with the gold rule inside it, as thin as Ember's; the corners stay unbroken | |
