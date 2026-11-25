# Execution record

The workflow was `wf_e7c91d8b-103` (10 agents, 0 errors). Builders worked in `~/ka0s-scratch/isfb/<Repo>`. The lead merged
each branch onto that repo's live `master` inside the scratch clone, re-gated the merge, then fast-forwarded the live repo
and pushed it.

## What was built

- **LibKa0s v1.116.0** (tag pushed, `cbd82ed3`). `LibKa0s-ForeverDB-1.0` minor 3 adds `Object(id)`, an object's name, with
  kit revision 64. Drop Watcher is the library's only ForeverDB consumer.
- **Drop Watcher** (ISF-DW-00 to 08, plus the ISF-REV fixes):
  - the key is bound as `ALT-CTRL-D`, the chord order the client matches, and re-tried once per character; the dead
    `CTRL-ALT-D` is cleared only when it ran Item Search;
  - objects are named, same-named ones are merged, unnamed ones are dropped;
  - every section is ranked for you, the tooltip is capped at Rows per section (5 by default), there is an "Only
    professions you know" filter, and the recipe glyphs are arrow, dash and padlock;
  - the window is rebuilt with "Drop Watcher" in the title, no lock, resizing, a tab of tables per section, section
    headers with Filter, Sort and Reset, tooltips, hover and alternating rows, a highlighted match, shift-click to link,
    and no recent searches;
  - waypoints use a map-pin icon and go to TomTom or Drop Watcher's arrow, never the client's map waypoint.
- **Outfitter Reborn** (ISF-OR-01) no longer reads ForeverDB. The schema goes from 1 to 2, and the Forever missing-item
  description comes from the client's item info alone.
- **Skill Master** (ISF-SM-01) no longer reads ForeverDB. SF-SM-02 is reverted, the schema goes from 12 to 13, and the
  seed tooling keeps using ForeverDB as offline evidence.

## Review (ISF-REV)

There were two independent reviewers, one on Drop Watcher and one on LibKa0s, Outfitter Reborn and Skill Master. Neither
found a blocker.

- **Fixed (one major).** The tooltip was over its perf ceilings on Forever (22336 and 10152 bytes against 17500 and 6500).
  After the fix it is 17248 and 6144, and the ceilings were not raised.
- **Fixed (minors):**
  - the resize repaint now reuses the last build;
  - the Crafting tab's filter follows the setting;
  - quests are ranked after their level is known;
  - the dead `row.limited` key is gone;
  - the unnamed-object log is written once per item;
  - Outfitter Reborn's no-read scan is stricter.
- **Open, for the owner:** the minors that came back as decisions are under "Calls made without asking" below.

## Lead gate on the merge results (2026-11-25)

| Repo | Merge | Retail | Forever | luacheck | seeds | perf |
|---|---|---|---|---|---|---|
| LibKa0s | 0be9a569 | 5238/0 | 5238/0 | 0/0 (393) | 18 | n/a |
| DropWatcher | b1113a6 | 2803/0 | 2778/0 | 0/0 (297) | 32 | green both clients |
| OutfitterReborn | 87cff59 | 1632/0 | 1612/0 | 0/0 (207) | 17 | n/a |
| SkillMaster | 002536f | 893/0 | 893/0 | 0/0 (170) | 24 | n/a |

**Conflicts.** There was one, in Drop Watcher's `docs/smoke-tests.md`, against master's IS-SMOKE record. It hit
ITEM-SEARCH-2, 7, 10 and 12. The resolution keeps the branch's superseded notes and the owner's "Passed (owner,
2026-11-25)" results. The file is still CRLF.

## Calls made without asking (beyond 03_SPEC §12)

- **Outfitter Reborn on Forever:** the missing-item list is always described (quality color and level) when the client has
  the item cached. The old ForeverDB switch is deleted by schema step 2, and no switch replaces it. Smoke row ISF-OR-3
  carries an "owner to confirm" note.
- **Drop Watcher, Sold by and Quests:**
  - the Stock and Requires columns, the per-vendor price and the quest objective counts are dropped, because
    `LibKa0s-ForeverDB-1.0` does not expose `vendx` stock, requirements or price, or objective counts;
  - the faction, profession and product icons are text only.

  These are recorded in Drop Watcher's `docs/known-limitations.md`. A LibKa0s issue to expose them is not filed yet.
- **Waypoints:** TomTom can be picked while it is not installed, and then falls back to Drop Watcher's arrow. The arrow's
  settings block is dimmed rather than hidden.
- **The key re-try:** a character whose key was already defaulted is re-tried only when the dead chord was actually
  cleared, so a player who removed the key keeps it removed.
- **The setting name:** the key hint keeps the existing `itemSearch.tooltip.hint` setting, not a new `tipKeyHint`.

## Smoke owed (owner)

- Drop Watcher: ITEM-SEARCH-19 to 30. The Forever arrow (26, 27) was never seen in a client.
- Outfitter Reborn: ISF-OR-1 to 4.
- Skill Master: ISF-SM-01-1.
