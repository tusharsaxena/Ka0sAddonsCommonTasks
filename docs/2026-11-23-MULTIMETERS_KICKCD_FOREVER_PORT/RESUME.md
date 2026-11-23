# RESUME: MultiMeters + KickCD to WoW Forever

State 2026-11-23: rulings in 00_DESIGN.md; plan in 01_EXECUTION_PLAN.md and plan-data/; build running.

1. `bash plan-data/resume-state.sh` (from this bundle, with the live checkouts as siblings) lists what is done.
2. The build runs in scratch clones; a finished item is a commit there, fetched into the live repo as the run branch
   by the lead. A clone lost with the scratchpad means: re-clone the run branch from the live repo and carry on.
3. Rulings: `00_DESIGN.md`. Research: `inputs/research/` (critic.md over SYNTHESIS.md, factcheck.md over readers).

Owner's guidelines for this run: ask up front, then decide alone; a resumable checkpointed plan; branch
`feat/2026-11-23-multimeters-kickcd-forever-port`, incremental commits; push at milestones; no merge without the
owner's go-ahead; delete the run's branches, stashes and worktrees after the merge; workflows for orchestration.

The client loads the checkouts live: build outside them, switch one only at a green checkpoint, and back up both
clients' SavedVariables first. MultiMeters stacks on the fix branch; a push of its port branch carries that commit.
