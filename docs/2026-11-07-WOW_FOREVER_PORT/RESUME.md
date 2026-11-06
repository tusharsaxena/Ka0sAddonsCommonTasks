# Resuming the WoW Forever port (steps 1–4)

The plan is `02_EXECUTION_PLAN.md`, the design is `01_DESIGN.md`, the run branch is `feat/2026-11-07-wow-forever-port`, and git is the only state.

1. Run `bash docs/2026-11-07-WOW_FOREVER_PORT/plan-data/resume-state.sh`. It prints the OPEN items, the total, any repo that is DIRTY, and any repo that is on another branch. An item is done when its repo has a commit, on the run branch or on master, whose subject starts `<ID>: `. One subject may carry several ids, as in `A + B: `. An item can also be done because it is listed in `plan-data/exceptions.tsv`.
2. If a repo is DIRTY, read the diff before doing anything. An Ace3 copy or a LibKa0s re-vendor is idempotent and can be redone. Never `reset --hard` or `checkout .` work you have not read. Either continue it or stash it.
3. Work in milestone order: M1 standard, then gate A, then M2 LibKa0s, then M3 dev-copilot, then gate B and the plugin reload, then M4 addons, then M5.
   - **Gates A and B are owner decisions.** After CP-1 and CP-3, ask the owner and wait. A gate is done when master in that repo has a `WFP-GATE-A:` or `WFP-GATE-B:` merge commit.
   - Before M4, confirm the installed plugin reports 2.8.0.
4. At each checkpoint:
   - re-run the gate;
   - add the review note (`refs/notes/ka0s-review`);
   - push the branch and the notes (the lead session does this, never a subagent);
   - log a row in `checkpoints.tsv`.
   The LibKa0s `v1.92.0` tag stays local until WFP-FIN.
5. Smoke belongs to the owner, through `03_SMOKE_TESTS.md`. WFP-FIN runs only on the owner's go-ahead. After it, delete every run branch, stash and worktree.
