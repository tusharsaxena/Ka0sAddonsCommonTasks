# Execution plan

- **Branch:** `feat/2026-11-25-item-search-feedback`. It exists in LibKa0s, DropWatcher, OutfitterReborn,
  SkillMaster and this repo.
- **Where it's built:** clones under `~/ka0s-scratch/isfb/`. The lead fetches each branch into the live
  repo without checking it out, then pushes it.
- **State is git:** an item is done when a commit whose subject starts `<ID>: ` is on its repo's branch
  (`plan-data/resume-state.sh`). The manifest is `plan-data/items.tsv`.

| Milestone | Items | Checkpoint |
|---|---|---|
| M0 | ISF-PLAN | The bundle and mockups are committed. |
| M1 | ISF-LK-01, ISF-LK-REL, ISF-OR-01, ISF-SM-01, ISF-DW-00 to ISF-DW-04 | Each repo's gate is green on both kit profiles. |
| M2 | ISF-DW-05 to ISF-DW-08 | Drop Watcher's full gate is green. The smoke rows are written. |
| M3 | ISF-REV | Review findings are fixed or recorded. The lead re-gates all four repos and pushes the branches. |

**Who runs what:**
- **The workflow:**
  - three tracks run in parallel: LibKa0s then Drop Watcher in order, Outfitter Reborn, and Skill
    Master;
  - then one reviewer for Drop Watcher and one for LibKa0s, Outfitter Reborn and Skill Master;
  - then a fix pass.
- **The lead:** every push and GitHub write.

**The gate, per repo:**
- `~/.claude/dev-copilot/bin/ka0s-bounded lua tests/run.lua`, under both `KA0S_KIT_CLIENT` unset and
  `KA0S_KIT_CLIENT=forever`;
- `~/.claude/dev-copilot/bin/ka0s-bounded luacheck .` with 0 warnings and 0 errors;
- `pytest tools/seeds`, where the repo has it;
- the repo's own extra gates, from its CLAUDE.md;
- files stay CRLF (`.gitattributes`).

**Merging** waits for the owner's go-ahead. So do pushing the v1.115.0 and v1.116.0 tags and closing
any issue.
