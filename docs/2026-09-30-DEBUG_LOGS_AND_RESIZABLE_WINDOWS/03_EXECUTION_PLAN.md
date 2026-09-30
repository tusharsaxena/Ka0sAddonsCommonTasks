# Execution plan

Frozen once execution starts; progress lives in git (see `RESUME.md`). Branch in every touched repo:
`feat/2026-09-30-debug-logs-and-resize`.

## Milestones

| M | What | Items | Runs as |
|---|---|---|---|
| M0 | Plan bundle committed | DL-PLAN-01 | inline |
| M1 | Standard v2.70.0 + LibKa0s v1.64.0 (local tag) | DL-STD-01, DL-LIB-01 | one workflow, 2 repos in parallel, each adversarially reviewed |
| M2 | Re-vendor v1.64.0 + standards ref v2.70.0 + resize smoke checks, all eleven | DL-<XX>-01 ×11 | one workflow, 11 repos in parallel, reviewed |
| M3 | 060 audit and fill, all eleven | DL-<XX>-02 ×11 | one workflow (may batch), reviewed against the coverage map |
| M4 | In-game checks, report, record | DL-FIN-01 | inline |

## Order and dependencies

- DL-STD-01 and DL-LIB-01 have no dependency and run in parallel (both work from `02_SPEC.md`).
- DL-<XX>-01 needs DL-LIB-01 (the local tag) and DL-STD-01 (the version it cites).
- DL-<XX>-02 needs that repo's -01 (it reads the new standard text and writes on the new vendor).
- DL-FIN-01 needs everything.

## Per item

1. Read `02_SPEC.md` § for the item and the repo's `CLAUDE.md`.
2. Branch (first item in the repo cuts it from `master`).
3. Implement, test first where the item adds behavior.
4. Gate green through the bounded runner (`~/.claude/wow-addon/bin/ka0s-bounded`). Fix moved citations;
   regenerate test-case lists or badges if a count moved. CRLF files stay CRLF.
5. Commit `<ID>: ...` (the session's attribution lines).
6. Independent review: a separate agent re-reads the diff against the spec and the standard, runs the
   gate, and either signs off (git note `refs/notes/ka0s-review`, "OK <ID>") or lists defects. Defects
   are fixed as `<ID>R: ...` commits and re-reviewed (at most two rounds, then stop and report).

## Checkpoints and pushes

At the end of each milestone: every touched repo clean, gate green, a row appended to `checkpoints.tsv`
(evidence: heads, test counts, luacheck), and the feature branches pushed to origin
(`git push -u origin feat/2026-09-30-debug-logs-and-resize`, plus `refs/notes/ka0s-review`). The LibKa0s
tag is not pushed. No merge to any master until the owner says so; then the finalize procedure (merge
`--no-ff`, gate on the merge, push master, push the tag, delete branches) runs per repo, the standard
and LibKa0s first.

## Stops

A red gate, a spec/standard conflict, a merge conflict, or a finding that needs an owner decision stops
that repo's chain (others continue) and is reported. Nothing is forced.
