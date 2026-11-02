# Resume: smoke round 3

1. Run `./resume-state.sh`. An item is done when a commit whose subject holds `<id>: ` is on `feat/2026-11-01-full-skinning` in the repo that owns it, or when it has an `exceptions.tsv` row. It also prints the local tag and any dirty repo or repo on the wrong branch.
2. Read `00_PLAN.md`, then `items.tsv`. Images are in `inputs/images/`.
3. On a dirty tree, read it, then finish it or stash it. Never reset work you have not read.
4. The whole run is `plan-data/run.js`. Relaunch it through the Workflow tool with `scriptPath` pointing at that file. Each agent skips ids that have already landed, so a relaunch is safe at any point. If the session that ran it is still alive, pass `resumeFromRunId` to reuse cached stages.
5. Checkpoints: M1 is done when R3-REL has landed and the tag points at it. M2 is done when every M2 id has landed. M3 is done when the R3-GATE row is in `checkpoints.tsv` and the branches are pushed.
6. After M3, wait for the owner's smoke results and go-ahead. Then run `/dev-copilot:finalize` across the repos, push tag v1.85.0, and close LibKa0s #71 and #72 spaced apart (#70 stays open). Delete every branch, stash and worktree this run and its parents made. Never merge or push a tag without the go-ahead.
