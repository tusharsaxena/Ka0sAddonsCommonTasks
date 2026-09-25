# CLAUDE.md — Ka0sAddonsCommonTasks

A planning and record workspace for work that spans **several** Ka0s repositories. It is not an addon
and holds no addon code. `README.md` is the charter; read it first.

## The collection

Every Ka0s repo is a sibling of this one, under `/mnt/d/Profile/Users/Tushar/Documents/GIT/`, so refer to
them as `../<Repo>`.

- **Upstreams:** `WowAddonStandards` (the Ka0s WoW Addon Standard), `LibKa0s` (the shared library and test
  kit, vendored into every addon) and `wow-addon` (the Claude Code plugin behind `/wow-addon:*`).
- **Addons:** `../WowAddonStandards/standards/ADDONS.md` is the single source of truth for which addons
  are in scope. Never copy that list into this repo, because a copy goes stale.
- Other directories under `GIT/` (for example `steamdb` or `weakaura_sounds`) are not part of the
  collection. Leave them alone.
- Every collection repo's default branch is `master`. This repo's default branch is `main`.

Each repo has its own `CLAUDE.md`, and that file governs work inside the repo: its green gate, its
standards-compliance rules and its conventions. When you work in `../<Repo>`, follow that repo's
`CLAUDE.md` as well as this one.

## Where specs and plans go

Decide first whether the work belongs to one repo or to several.

- **Single-repo work, for example an AuraMaster feedback batch.** The spec and the checkpointed plan go
  in **that repo** and are committed on its feature branch:
  - `docs/superpowers/specs/<YYYY-MM-DD>-<topic>-design.md`
  - `docs/superpowers/plans/<YYYY-MM-DD>-<topic>.md`

  This applies even when the session was started from this directory. Nothing for that work is written
  here.
- **Cross-repo work** (a collection-wide review remediation, a LibKa0s adoption sweep, anything that
  reasons about the collection as a whole) goes here as a dated bundle, `docs/<YYYY-MM-DD>-<TOPIC>/`.
- **Anything with a better home goes there:** a rule belongs in `WowAddonStandards`, a command or agent in
  `wow-addon`, shared code in `LibKa0s`, and one addon's script in that addon.

## Bundle conventions

- Name the folder `docs/<YYYY-MM-DD>-<UPPER_SNAKE_TOPIC>/`, dated the day the bundle is created.
- Number the files in reading order. A typical large bundle has `00_OVERVIEW.md`,
  `01_CONSOLIDATED_FINDINGS.md`, `02_UPSTREAM_CHANGES.md`, `03_SPEC.md`, `04_EXECUTION_PLAN.md`,
  `05_TRACEABILITY.md`, `06_SMOKE_TESTS.md` and an execution record. Smaller exercises use fewer files,
  such as `00_PLAN.md` and `99_REPORT.md`. Addenda made during execution get their own named file, for
  example `M5_LAUNCHER_TOOLTIP.md`.
- **Bundles are frozen once executed.** The plan records what was intended, and rewriting it afterwards
  destroys that record. Record later developments in the execution record, `RESUME.md` or
  `checkpoints.tsv`, or in a new bundle. Never edit the plan.
- Inputs that planning drew on, such as review and audit findings or owner scope notes, go in `inputs/`.
  Machine-readable plan data and executor scripts go in `plan-data/`.

## Resumable, checkpointed plans

For long multi-repo runs, follow the pattern in `docs/2026-09-23-REVIEW_AND_STANDARDS_AUDIT_REMEDIATION/`:

- **Git is the only state.** An item is done when a commit whose subject starts `<ID>: ` exists in the repo
  that owns it. One commit may carry several ids: `LK-01 + LK-02: ...`. Items that legitimately land with
  no commit go in `exceptions.tsv`, each with a command that proves the claim.
- `items.tsv` is the manifest: id, milestone, repo, title, dependencies, effort, smoke checks, and the
  finding ids and issue refs it traces to.
- `resume-state.sh` computes progress straight from git, so nothing depends on a status table a crashed
  session may have left stale.
- `RESUME.md` tells a fresh session how to pick up from any point: find the state, clean up an interrupted
  item, relaunch, and run the milestone checkpoint.
- `checkpoints.tsv` logs each milestone that passed its checkpoint and was pushed, with the evidence: test
  totals and the pushed heads.
- Independent reviews are recorded as `refs/notes/ka0s-review` git notes, and those notes are pushed
  with the branch.
- On a dirty tree, never `reset --hard` or `checkout .` work you have not read. Continue it or stash it.

## Git and publishing rules

- Each cross-repo exercise works on one feature branch in every repo it touches, with the same name in
  each repo, for example `feat/2026-09-23-review-audit-remediation`.
- **Commit** incrementally, and **push feature branches** at milestone checkpoints, only when the owner
  has authorized it for that piece of work.
- **Never** merge into `master`/`main`, push a tag, bump an addon version or cut a release without the
  owner's explicit go-ahead. Once the owner approves, `/wow-addon:finalize` does the merge.
- Merge `--no-ff`, then delete the feature branch.
- Commit messages end with the session's attribution trailers.
- Space out bulk GitHub writes (issue create and edit), because rate limits hurt more than slowness.

## Verification

- Every addon's green gate is in its own `CLAUDE.md`. It is typically `lua tests/run.lua`, `luacheck .`
  (0 warnings / 0 errors) and `lizard -l lua -x "./libs/*" -x "./tests/_kit/*" .` (no function above
  CCN 15), plus the 1500-line file cap.
- For long batteries, use the bounded runner at `/home/tushar/.claude/wow-addon/bin/ka0s-bounded`.
- In-client smoke tests are the owner's to run. Record their results in the bundle's smoke-test file and
  never mark a smoke check as passed yourself.
- For regressions, bisect before theorizing. A commit message documents only the change its author knew
  about.

## Useful commands

- `/wow-addon:finalize`: sync docs, commit, merge, push and delete branches, across repos in dependency
  order.
- `/wow-addon:issue-summary`: issue counts across the whole collection.
- `/wow-addon:execution-status`: where a planned run stands.
- `/wow-addon:revendor-libka0s`, `/wow-addon:revendor-standards`: push upstream changes into addons.
