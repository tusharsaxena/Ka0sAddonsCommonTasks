# Resume round 7

1. `./resume-state.sh` prints OPEN items, DIRTY trees and wrong branches. Git is the state. WowAddonStandards is the
   worktree `../.worktrees/WowAddonStandards-r7` (the main checkout belongs to the Outfitter agent: never switch it).
2. A dirty tree is an interrupted item. Read it, then continue or stash it. Never reset it.
3. Relaunch `plan-data/run.js` with Workflow scriptPath and resumeFromRunId. Builders skip ids that already have a commit.
4. Subagents cannot push to master or write GitHub (permission classifier); the lead does merges, pushes and issue writes.
5. Merge only after the owner's go-ahead; then delete the branch everywhere and `git worktree remove` the standards worktree.
