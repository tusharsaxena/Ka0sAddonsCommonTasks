# Resume: smoke round 5

1. Run `./resume-state.sh`. An item is done when a commit whose subject holds `<id>: ` is on
   `feat/2026-11-01-full-skinning` in the repo that owns it (any repo for `*`), or when it has an `exceptions.tsv` row.
   The script also prints the local tag, and any repo that is dirty or on the wrong branch.
2. Read `00_PLAN.md` (the lead's calls), then `items.tsv`, then `inputs/INVESTIGATION.md` for each item's diagnosis.
   Images are in `inputs/images/`.
3. On a dirty tree, read it, then finish it or stash it. Never reset work you have not read. Never touch Outfitter.
4. The run is `plan-data/run.js`. Relaunch it through the Workflow tool with `scriptPath` pointing at that file. Each
   agent skips ids that have already landed, so a relaunch is safe at any point.
5. After M3, wait for the owner's smoke results and go-ahead. Then merge with `/dev-copilot:finalize`, push tag v1.85.0,
   close LibKa0s #71 and #72 spaced apart (#70 stays open), and delete the branches, stashes and worktrees.
