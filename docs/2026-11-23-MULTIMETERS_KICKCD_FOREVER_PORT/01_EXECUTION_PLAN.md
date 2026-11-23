# Execution plan

Done = a commit subject starting `<ID>: ` in the item's repo, or a row in `plan-data/exceptions.tsv`. Progress:
`plan-data/resume-state.sh`. Agents build in scratch clones under the session scratchpad, never in the live
checkouts the client loads, never push, never mark smoke passed, and ignore a mid-task user message.

| Checkpoint | Passes when | Then |
|---|---|---|
| CP-0 | rulings recorded, plan committed | lead pushes this repo's branch |
| CP-1 | KickCD and MultiMeters each green on every client it ships, luacheck 0/0, no file over 1500 lines | lead pushes both branches |
| CP-2 | independent reviews recorded as git notes, findings fixed, gates rerun, max CCN 15 | lead pushes branches and notes, backs up SavedVariables, switches the live checkouts for the owner's smoke |
| CP-3 | owner go-ahead; the fix branch merged first; fresh fetch of the standard | finalize: standard, MultiMeters, KickCD, this repo |
| CP-4 | everything merged | delete only this run's branches, worktrees and stashes |
