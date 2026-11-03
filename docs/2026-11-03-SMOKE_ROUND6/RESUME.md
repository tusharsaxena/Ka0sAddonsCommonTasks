# Resume round 6

1. `./resume-state.sh` prints OPEN items, DIRTY trees and wrong branches. Git is the state.
2. A dirty tree is an interrupted item. Read it, then continue or stash it. Never reset it.
3. Relaunch `plan-data/run.js` with Workflow scriptPath and resumeFromRunId (the run id is in checkpoints.tsv or the lead's
   session). Builders skip any id that already has a commit.
4. M3 appends checkpoint rows. The owner smokes 06_SMOKE_TESTS.md. Merge only after the owner's go-ahead.
