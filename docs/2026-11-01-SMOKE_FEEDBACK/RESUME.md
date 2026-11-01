# Resume: smoke feedback

1. `./resume-state.sh`: done means a commit subject holding `<id>: ` on `feat/2026-11-01-full-skinning`. SF-REL and SF-GATE have their own evidence in `checkpoints.tsv`.
2. Read `00_PLAN.md`, then `items.tsv`. Images are in `inputs/images/`.
3. Dirty tree: read it, finish it or stash it. Never reset unread work.
4. M1 then M2 run from the script in `plan-data/`; agents skip landed ids. M3 waits for the owner to say the limit has reset; it needs a library change, so a further re-cut and re-vendor.
5. Smoke list after M2 and M3: the checks whose expected result changed. Nothing merges without the owner's go-ahead. After the merge delete every branch, stash and worktree this run and its parent made.
6. PanelMaster question from the owner: answered in chat, see `checkpoints.tsv`.
