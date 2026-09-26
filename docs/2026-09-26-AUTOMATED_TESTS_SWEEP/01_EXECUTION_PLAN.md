# Automated-tests sweep — execution plan (2026-09-26)

**Input:** `00_FIX_QUEUE.md`, which lists ATS-01 to ATS-24 from the 2026-09-26 `/wow-addon:automated-tests`
sweep of eleven addons and LibKa0s.
**Owner's instruction (2026-09-26):** fix everything in P1–P6 now and file no GitHub issues. Work on a
branch, commit incrementally, push feature branches at milestones, and never merge without a go-ahead.
When the fixes are done, re-run `/wow-addon:automated-tests` in every addon and in LibKa0s. Execution runs as
workflows.
**Owner's rulings:** ATS-19 is kept as designed (see `exceptions.tsv`). Pushes are feature branches only.

The manifest is `items.tsv`, which has 80 items. Git is the only state, so `./resume-state.sh` shows where
the run stands. `RESUME.md` explains how to pick the run up.

## Branch, commits, reviews

- One branch in every touched repo: **`feat/2026-09-26-automated-tests-sweep`**. Cut it from `master`
  (`main` here) in the M0 record item. The sweep's uncommitted bundle travels with it.
- **One item is one commit.** Its subject is `<ID>: <what changed>`, and its body cites the `ATS-nn`
  it traces to. When an existing issue is fixed, the body carries `Fixes #N` so that the owner's merge
  closes it. Nothing is closed by hand. Commit messages end with the session's attribution trailers.
- **Independent review per item** (M1, M2). A separate agent reviews the item's diff against the
  item's title, the repo's `CLAUDE.md` and the standard sections it touches. It records a verdict as a
  `refs/notes/ka0s-review` note on the commit. A defect it finds is fixed as `<ID>R: …`, which is
  reviewed again.
- Line endings follow each repo's `.gitattributes`. The addons and LibKa0s are CRLF.
- **Never** `reset --hard` or `checkout .` unread work. **Never** edit a frozen bundle
  (`docs/automated-tests/<stamp>/`, `docs/audits/`, `docs/reviews/`). **Never** edit an addon's
  `tests/_kit/` or `libs/LibKa0s/` by hand: they arrive by re-vendor only.

## Rules every fix item follows

- **Peels (file splits)** move code along a real seam, which is a set of functions that do not reach into
  each other's locals. A peel is a move, not a rewrite, and it changes no behavior. A new source file joins
  the TOC or XML load order in the right place. A new test file is wired into `tests/run.lua` (or the repo's
  runner list), and the case count before and after the peel must match exactly. Targets: test files end
  below 1000 (out of the band), and source files end at or below the target in the item's title. If a file's
  `RESULTS.md` watch-list row or its `CLAUDE.md` / `ARCHITECTURE.md` census row changes, update it in the
  same commit.
- **CCN items** (AM-ATS-05, MM-ATS-04, WG-ATS-01) are only fixed with one of the four refactor shapes
  `performance-§11` permits. Other constraints: no behavior change, no per-call allocation, and no
  extraction whose only purpose is lowering the number (anti-pattern #52). A function with no honest
  shape is left as it is. The commit body says why, and the item still lands (with a test or doc touch,
  or as an `exceptions.tsv` row with proof).
- **Perf items** (AM-ATS-01, CM-ATS-01) bisect with `tests/perf.lua` through the bounded runner, over the
  range in the title, in a throwaway worktree so the branch tree is never disturbed. Only a
  `bytes/iter` figure counts; `ms/iter` is noise under load. The fix removes avoidable allocation
  within `performance-§11`. If the cost turns out to be an intended feature, the item lands as a
  documentation commit that names the bisected commit and the feature, and updates `docs/performance.md`
  or the perf notes.
- **Gate per item:** the repo's green gate from its own `CLAUDE.md`, run through
  `~/.claude/wow-addon/bin/ka0s-bounded`. That means `luacheck .` at 0/0, the headless tests with 0
  failures, `lizard` with no function above CCN 15, and no authored file over 1500 lines. A red gate
  stops that repo's chain.
- **LibKa0s module ripple** (LK-ATS-01, and any peel that creates a new `LibKa0s/*.lua`) follows the
  `OptionsTabs.lua` worked example that #32 describes. That covers the `LibKa0s.xml` row, the `lib.MODULES`
  entry, its own LibStub minor with a paired shell guard, a `tests/majors.lua` row, the Options version-key
  component, the `docs/api/` page and the regenerated manifest.

## Milestones

### M0 — Record (13 items)

- **ATS-PLAN** commits this bundle on the sweep branch here.
- **`<P>-ATS-00`**, one per repo: cut the branch and commit the 2026-09-26 sweep bundle and `RESULTS.md`
  exactly as the sweep left them.
- **Checkpoint M0:** 13/13, every tree clean, then push the branch in all 13 repos.

### M1 — Upstream (12 items)

- **LibKa0s**, strictly in order LK-ATS-01 → 10:
  - #32/#33: the OptionsWidgets id peel and the test split.
  - The six shelf-life band entries, together with the two files at 1493 and `testkit/test_prose.lua`.
  - The runner fixes for ATS-20 and ATS-21.
  - The v1.62.0 release, with a **local** tag only.
- **wow-addon**, in parallel with LibKa0s: WA-ATS-01 (the hook matches commands, not prose), then
  WA-ATS-02 (the skill's subagent write path and a unique log path).
- **Checkpoint M1:**
  - 12/12 items, all reviewed.
  - The LibKa0s full battery is green: the census is empty and `test_layout_cap` is green.
  - `v1.62.0` resolves locally.
  - Push LibKa0s and wow-addon feature branches along with `refs/notes/ka0s-review`. The tag is not pushed.

### M2 — Addons (28 items)

- The eleven addon chains are independent of each other and run in parallel. Within a repo, items run
  strictly in `items.tsv` order.
- The perf bisects (AM-ATS-01, CM-ATS-01) come **before** their repo's re-vendor, so that the bisect range
  is not muddied.
- Every addon re-vendors v1.62.0 (`<P>-ATS-RV`), following `/wow-addon:revendor-libka0s`'s copy rules. The copy
  comes from the local tag, and the bundle goes under `docs/revendor/`. The candidate-adoption interview
  is out of scope: record "no adoption in this item".
- **Checkpoint M2**, per addon as its chain completes:
  - The chain is reviewed.
  - The full battery is green.
  - No authored file is over 1500 lines.
  - Push the feature branch and its notes.

### M3 — Re-run and record (13 items)

- **`<P>-ATS-99`**, 12 repos in parallel: a fresh `/wow-addon:automated-tests` run. The main session writes
  `ANALYSIS.md` if a subagent cannot. Refresh every carried Disposition cell to today's figures (ATS-23),
  then commit the bundle and `RESULTS.md`.
- **ATS-REC-01** writes `99_REPORT.md` here: each item's outcome, the final run table, the checkpoints, and
  what remains for the owner.
- **Checkpoint M3:** push all 13 branches.

### M4 — Sync docs and finalize (14 items; added on the owner's instruction, 2026-09-26, before execution)

- **`<P>-ATS-SD`**, for the 13 touched repos (the 11 addons, LibKa0s, wow-addon), in parallel:
  run `/wow-addon:sync-docs` on the sweep branch and commit the result as `<P>-ATS-SD: …`.
  If there is no drift, record an `exceptions.tsv` row with the proving command.
- **ATS-FIN** runs `/wow-addon:finalize` across every touched repo in dependency order: LibKa0s, then
  wow-addon, then the eleven addons, then this repo. Each repo is merged into `master`/`main` with
  `--no-ff`, pushed, and its sweep branch deleted. The owner's instruction to finalize is the go-ahead
  for the merge. `finalize` decides whether the local `v1.62.0` tag is pushed, and it asks the owner if
  that is not established. **No addon version is bumped.** The item is done when an `exceptions.tsv` row
  proves every merge (`git branch --merged master` shows no sweep branch remaining, and
  `git log --merges -1` shows the merge in each repo).

## Traceability

| Queue | Items |
|---|---|
| ATS-01 | CM-ATS-01 |
| ATS-02 | AM-ATS-01 |
| ATS-03 | LK-ATS-03, 04, 05, 06, 10 |
| ATS-04 | LK-ATS-01, 02 |
| ATS-05 | PM-ATS-01 |
| ATS-06 | LK-ATS-03, 06 |
| ATS-07 | LK-ATS-07 |
| ATS-08, 09, 15 | AM-ATS-02, 03, 04 |
| ATS-10 | PM-ATS-02 |
| ATS-11 | AT-ATS-01 |
| ATS-12 | MM-ATS-01, 02, 03 |
| ATS-13 | KC-ATS-01 |
| ATS-14 | CM-ATS-02 |
| ATS-16 | WG-ATS-01 |
| ATS-17 | MM-ATS-04 |
| ATS-18 | AM-ATS-05 |
| ATS-19 | `exceptions.tsv` (the owner's ruling: keep as designed) |
| ATS-20, 21 | LK-ATS-08, 09, then every `<P>-ATS-RV` |
| ATS-22 | WA-ATS-01, 02 |
| ATS-23 | every `<P>-ATS-99` |
| ATS-24 | BL-ATS-01 |
