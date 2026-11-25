# Execution plan

- **Branch:** `feat/2026-11-25-item-search-round3`. It exists in LibKa0s, DropWatcher and this repo.
- **Where it's built:** the clones `~/ka0s-scratch/isr3/LibKa0s` and `~/ka0s-scratch/isr3/DropWatcher`.
  Their `master` is the live `master`. The lead fetches each branch into the live repo without checking it
  out, then pushes it when the owner authorizes that.
- **State is git:** an item is done when a commit whose subject starts `<ID>: ` is on its repo's branch
  (`plan-data/resume-state.sh`). One commit may carry several ids (`ISR3-DW-01 + ISR3-DW-02: ...`). An
  item that lands with no commit goes in `plan-data/exceptions.tsv`, with a command that proves it. The
  manifest is `plan-data/items.tsv`.

| Milestone | Items | Checkpoint |
|---|---|---|
| M0 | ISR3-PLAN | The bundle is committed on this repo's branch. |
| M1 | ISR3-LK-01, ISR3-LK-REL, ISR3-DW-00 | LibKa0s is green on both kit profiles, with `pytest tools/seeds`. v1.117.0 is tagged locally (annotated) on the release-record commit, and its manifest preconditions are read. Drop Watcher is green after the re-vendor. |
| M2 | ISR3-DW-01 to ISR3-DW-05 | After each item, Drop Watcher's full gate is green, including `tests/perf.lua` on both clients with the ceilings unchanged, or a raise named in the calls. |
| M3 | ISR3-DW-06, ISR3-REV | The docs, the settings page, the schema step and the smoke rows ITEM-SEARCH-31 to 43 are written, unrun. Review findings are fixed or recorded. The lead re-gates both repos. |

**The order.** One track: LibKa0s, then Drop Watcher, item by item in id order. Every Drop Watcher item
touches the Item Search modules, so they run in sequence and never in parallel. Then two independent
reviewers: one for Drop Watcher, one for LibKa0s and the re-vendor. Then a fix pass, committed as
`ISR3-REV: ...`. Reviews are recorded as `refs/notes/ka0s-review` notes.

**What each Drop Watcher item covers** (spec section in brackets):
- **ISR3-DW-00 (§3):** the re-vendor, the icon additions, the prune, the delta bundle and the minor-4
  pin.
- **ISR3-DW-01 (§4.1):** the glyphs, `GLYPH_SIZE`, TipMarks' size argument, `TABS.INSET`, centered
  glyph and mark columns, the header hover, the sort triangles, and removing `ph:arrow-up` and `ph:minus`
  from the declaration and re-pruning.
- **ISR3-DW-02 (§4.2):** `IS.SkillParts` with its memo, the crafting row's right side and the
  `craftSkill` setting; the hairline with `dw.tipRule` and `RULE_INSET`; the label line; the title
  removed; the quest marks and `MARK_SIZE`; `Compat.QuestReady` and the `ready` state.
- **ISR3-DW-03 (§4.3, §4.4, §4.6):** the rank tones; `IS.IsTestSource`; `IS.GatherKind`,
  `core/GatherNodes.lua`, the Gathered from tab, its ranking and its tooltip section; the
  `ItemSearchPrices` module and `recordPrices`; per-row prices; "<Side> only"; "No known spawn"; the Full
  policy and `fullDB`; schema step 18. It also runs the offline measurements: the test-name pattern
  over the build's names, the node-table check, and the Full load's KB and time. Their numbers go in the
  commit message and the execution record.
- **ISR3-DW-04 (§4.7):** `IK.Decide` and `IK.TOOLTIPS`.
- **ISR3-DW-05 (§4.5):** `ItemSearchVerdict.lua`, `ItemInfoByID`'s sell price and bind type, the badge
  and reason lines, the `badge` and `reasons` settings, and the verdict memo.
- **ISR3-DW-06 (§5, §7, §8):** the settings page's final order, `settings-panel.md`, `schema.md`,
  known limitations, forever probes, performance, validate-seeds, the module map, the README,
  `test-cases.md` regenerated with the badge, and the smoke rows.

**Who runs what:**
- **The workflow:** the builders, the two reviewers and the fix pass.
- **The lead:** every push, every GitHub write, the merge and the tag push. Each of those waits for the
  owner.

**The gate, per repo, before every commit:**
- `~/.claude/dev-copilot/bin/ka0s-bounded lua tests/run.lua`, with `KA0S_KIT_CLIENT` unset and with
  `KA0S_KIT_CLIENT=forever`, 0 failed both times;
- `~/.claude/dev-copilot/bin/ka0s-bounded luacheck .`, 0 warnings and 0 errors;
- `python3 -m pytest -q -p no:cacheprovider tools/seeds`, in both repos (both have it);
- `tests/perf.lua` on both clients, where the repo has it (Drop Watcher);
- the 1500-line cap, and CCN ≤ 15 for new or changed functions (the kit's sighted lizard shadow, never
  raw `lizard`). If the complexity suite writes a `docs/automated-tests/` bundle or changes `RESULTS.md`
  as a side effect, those are restored, except in ISR3-LK-REL's release record, which writes one on
  purpose;
- files stay CRLF where `.gitattributes` says so (both addon repos).

**Never:** a push, a merge, a version bump of Drop Watcher, a tag push, a GitHub write, a row of
ForeverDB copied into a repo, ItemTree code or art, `COMBAT_LOG_EVENT_UNFILTERED`, or a smoke row marked
passed.

**Merging** waits for the owner's go-ahead. So do pushing the v1.117.0 tag and closing any issue.
