# Resume: smoke round 4

1. Run `./resume-state.sh`. An item is done when a commit whose subject holds `<id>: ` is on
   `feat/2026-11-01-full-skinning` in the repo that owns it, or when it has an `exceptions.tsv` row. It also prints the
   local tag and any dirty repo or repo on the wrong branch.
2. Read `00_PLAN.md`, then `items.tsv`, then `inputs/INVESTIGATION.md` for each item's diagnosis. Images are in
   `inputs/images/`.
3. On a dirty tree, read it, then finish it or stash it. Never reset work you have not read. Never touch Outfitter.
4. The M1 run is `plan-data/run-m1.js`. Relaunch it through the Workflow tool with `scriptPath` pointing at that file;
   each agent skips ids that have already landed, so a relaunch is safe at any point.
5. M2 starts only after the owner signs off on `R4_MOCKUP.html` (record the choice in `R4_SIGNOFF.md`).
6. M3: R4-GATE row in `checkpoints.tsv`, branches pushed. Then wait for the owner's smoke results and go-ahead; merge
   with `/dev-copilot:finalize`, push tag v1.85.0, close LibKa0s #71 and #72 spaced apart (#70 stays open).
