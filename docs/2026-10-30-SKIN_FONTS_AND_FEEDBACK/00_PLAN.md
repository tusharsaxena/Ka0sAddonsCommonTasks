# Plan: skin fonts and feedback (LibKa0s v1.82.0, standard v2.93.0)

The owner's 15-item batch after the skin library follow-ups passed smoke (`inputs/OWNER_FEEDBACK.md`, screenshots in
`inputs/screenshots/`). M0's inventory is `inputs/inventory/` (reports A to K and the critic Z); the calls taken from it
are `DECISIONS.md`. The manifest is `items.tsv`; `./resume-state.sh` reads progress from git; `RESUME.md` restarts a
crashed run.

## Owner item to plan item

| # | Owner item | Items |
|---|---|---|
| 1 | Overrides reset on a skin change | LK-07 |
| 2-4 | Expressway, Prototype, Fira Sans Medium, shipped | LK-01, LK-02, WS-01 |
| 5 | Equal widths, Ka0s Default the baseline; HUD too | LK-05, LK-06, every XX-01 |
| 5b | Characters some faces cannot draw | LK-12, BL-02, LH-02, WS-01 |
| 6 | Reset buttons; Scope alignment | LK-08 |
| 7 | Remove unused fonts | LK-01 |
| 8 | PGFE expand/collapse glyph and alignment | PG-02 |
| 9 | AuraMaster TEST marker; glow regression | AM-02, AM-03, KC-03, WS-01 |
| 10 | DropWatcher dropdown, Proc default, hidden sections; two issues | DW-02..04, LK-10, IS-01, IS-02 |
| 11 | Anchor titles cut off; sim placeholder anchor; issue | LK-09, AM-03, KC-02, IS-03, WS-01 |
| 12 | `/xx skin` | LK-11, every XX-01, WS-01 |
| 13 | Outline by default, as a setting; every addon stores flags | LK-03, LK-04, every XX-01, WS-01 |
| 14 | MultiMeters issues | IS-04, IS-05 |
| 15 | QuickComms animations (existing #13); test dial glyphs | IS-06, QC-02 |

## Milestones

- **M0, done.** Inventory, decisions, baselines (`plan-data/baselines.tsv`: each repo's gate totals on master).
- **M1, library and standard.** LibKa0s items in id order, one writer at a time, each with an independent review
  and fix round, then LK-90: the release run (`/dev-copilot:bump-version`-grade battery, CCN 15, 1500-line cap) and
  a **local** tag v1.82.0. WS-01 runs alongside (its own repo). ST-01 after LK-90. Checkpoint: gates green, branches
  and review notes pushed, the tag not pushed.
- **M2, the addons.** All 15 in parallel, one agent per repo, each in id order: the re-vendor (XX-01) first, carrying
  every stub and facade the tag needs in one commit, then that addon's own items. A library gap found here follows
  RESUME §5 (an `LK-A<n>` addendum, a re-cut local tag, `XX-RV2`). Each addon gets an independent review and a fix
  round. Checkpoint: as M1.
- **M3, GitHub issues.** IS-01..07, one write at a time with a pause between, each recorded in `exceptions.tsv`
  with a `gh issue view` proof.
- **M4, report.** `99_REPORT.md` (what landed, lead decisions taken during the run, gate totals against the
  baselines) and `06_SMOKE_TESTS.md` (the in-client index; every repo's own checks in its `docs/smoke-tests.md`).
  Then stop for the owner's smoke pass and go-ahead.
- **M5, finalize on the go-ahead only.** WowAddonStandards, then LibKa0s (and its tag), then the Skin Tester and
  the addons, then this repo: merge `--no-ff`, push, delete branches, check stashes and worktrees.

## Order inside M1

LK-01 (payload) → LK-02 (faces) → LK-03 (outline) → LK-04 (flags and font group) → LK-05 (sizes, measured with
outline on) → LK-06 (HUD scale) → LK-07, LK-08 (Skin tab) → LK-09 (strip re-fit, after the sizes) → LK-10, LK-11,
LK-12 → LK-13 (docs) → LK-90. Each file's LibStub minor moves once in the release (D-23).

## Rules every implementer follows

- Work on `feat/2026-10-30-skin-fonts-feedback`, in the main checkout (the game loads `GIT/<Addon>`). One repo,
  one writer. Commit subjects start `<ID>: `; trailers as the session gives them. Never push, merge or tag; the lead
  pushes at checkpoints.
- The green gate of the repo's own `CLAUDE.md`: `~/.claude/dev-copilot/bin/ka0s-bounded lua tests/run.lua`, then
  `~/.claude/dev-copilot/bin/ka0s-bounded luacheck .` (0/0), the 1500-line cap, CCN 15 through the vendored
  complexity suite. Never raw lizard. Never edit `libs/` or `tests/_kit/` except by re-vendoring the tag.
- Tests first where behavior changes. No smoke check is ever marked passed by the run.
