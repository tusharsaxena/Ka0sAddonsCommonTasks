# RESUME: MultiMeters + KickCD to WoW Forever

State 2026-11-23: research done; the owner's question round is open. Nothing is built.

1. Read `inputs/research/SYNTHESIS.md`, then `critic.md`, which overrides it, then `factcheck.md`.
2. Get the owner's answers to the critic's section 5, Q1 to Q8 (Q0 is resolved: the MultiMeters base branch
   `fix/2026-11-23-r2-restore-probe-fixes` exists at f1b0d79).
3. Write `00_DESIGN.md` (the rulings verbatim), `01_EXECUTION_PLAN.md`, `plan-data/items.tsv` (SYNTHESIS section 4,
   amended by the critic) and `plan-data/resume-state.sh`, then run the build as workflows.

Owner's guidelines for this run: ask up front, then decide alone; a resumable checkpointed plan; branch
`feat/2026-11-23-multimeters-kickcd-forever-port`, incremental commits; push at milestones; no merge without the
owner's go-ahead; delete the run's branches, stashes and worktrees after the merge; workflows for orchestration.

The client loads the checkouts live: build outside them, switch one only at a green checkpoint, and back up both
clients' SavedVariables first. MultiMeters stacks on the fix branch; a push of its port branch carries that commit.
