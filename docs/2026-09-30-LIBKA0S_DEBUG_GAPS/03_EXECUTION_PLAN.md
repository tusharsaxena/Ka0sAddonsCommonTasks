# Execution plan

Frozen once execution starts; progress lives in git (see `RESUME.md`).

| M | What | Items | Runs as |
|---|---|---|---|
| M0 | Plan bundle | DG-PLAN-01 | inline |
| M1 | LibKa0s v1.65.0, then standard v2.73.0, then wow-addon | DG-LIB-01 → DG-STD-01 → DG-PLUG-01 | one workflow, each reviewed (up to 2 fix rounds) |
| M2 | Adoption in all eleven addons | DG-<XX>-01 ×11 | same workflow, 11 in parallel after M1, reviewed |
| M3 | Record, push | DG-FIN-01 | inline |

Per item: read the spec and the repo's CLAUDE.md; branch; tests first; gate green through `ka0s-bounded`; commit
`<ID>: ...` (several commits allowed, one per gap or step); independent review signs off with a
`refs/notes/ka0s-review` note "OK <ID>" or lists defects fixed as `<ID>R: ...`. At milestone ends: `checkpoints.tsv`
row, branches and notes pushed. No merge, no pushed tag without the owner's go-ahead. A red gate, a conflict or a
decision only the owner can make stops that repo and is reported.
