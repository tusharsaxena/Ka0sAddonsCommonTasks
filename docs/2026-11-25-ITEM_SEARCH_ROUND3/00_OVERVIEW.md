# Item Search round 3 (2026-11-25)

The owner's third pass over Drop Watcher's Item Search, after the feedback run
(`docs/2026-11-25-ITEM_SEARCH_FEEDBACK/`) was merged and tried on WoW Forever. Two repos:

- **LibKa0s:** `LibKa0s-ForeverDB-1.0` minor 4. Spawn spots come from ForeverDB's world coordinates
  (`spw`, converted to map positions through ForeverDB's own `umaa` and `zbord` tables) and from
  ForeverDB_Full's `spz` when that addon is loaded, which happens on demand and never in combat. Vendor
  prices also come from `vendx`. Kit revision 65. Released as v1.117.0 with a local tag only.
- **Drop Watcher:**
  - thick skill-up arrows and a left-right "no skill-up" arrow, drawn at the same size in the tooltip
    and the window;
  - an inset first column, and column headers that highlight on hover and show LootHistory's sort
    triangles;
  - skill breakpoints on the tooltip's recipe rows;
  - quest marks in the game's style, including a new "ready to turn in" state;
  - a tooltip block that opens with an ItemTree-like hairline, then "Drop Watcher" and a
    Keep / Hold / Sell / Toss badge with a score and a confidence;
  - source names and the Type column colored by creature rank;
  - a "Gathered from" tab and tooltip section;
  - test and dev sources filtered out;
  - prices recorded at vendors, and "Horde only" / "Alliance only" in place of "can't buy";
  - zones and waypoints for most of the sources that had none;
  - Ctrl-Alt-D shows a hovered item and otherwise toggles the window.

Item 3 (orange on the Skill column) was dropped by the owner.

## Files, in reading order

1. `inputs/OWNER_FEEDBACK.md`: the 14 items verbatim, and the owner's answers to the recon's questions.
2. `inputs/RECON.md`: the measured recon, with file:line evidence and options.
3. `03_SPEC.md`: what gets built, item by item, and the calls made without asking.
4. `04_EXECUTION_PLAN.md`: the items, milestones and checkpoints.
5. `plan-data/`: the manifest, the resume script, the exceptions and the checkpoint log.
6. `RESUME.md`: how a fresh session picks up.
7. `EXECUTION_RECORD.md`: written during and after the run.
